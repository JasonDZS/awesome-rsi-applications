#!/usr/bin/env python3
"""Take a paper from a link to a pull request awaiting /confirm. Used by the add-paper skill.

  python3 scripts/add_paper.py check <url>
      Is the paper already listed, or does it already have an issue?

  python3 scripts/add_paper.py open --title "..." --url <url> --reason "..." [--tags "0;1"]
      Open the "Recommend a paper" issue, create the branch paper/issue-<N> from the latest
      default branch, and create data/pending/issue-<N>.yml to fill in.

  python3 scripts/add_paper.py submit <N> [--reader "..."] [--trailer "..."] [--footer "..."]
      Validate the annotation, commit only that file, push the branch and open the pull request.
      The annotation then appears on issue #N, where a human confirmer comments /confirm.

This script never confirms a paper. Confirmation is a person commenting /confirm on the issue.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402

TAG_LABELS = [f"{k} {v}" for k, v in pl.DOMAINS.items()]


def git(*args, check=True):
    out = subprocess.run(["git", "-C", str(pl.ROOT), *args], capture_output=True, text=True)
    if check and out.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{(out.stderr or out.stdout).strip()}")
    return out.stdout.strip()


def default_branch():
    ref = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", check=False)
    return ref.split("/", 1)[1] if "/" in ref else "main"


def find_existing(url):
    """Return (listed_id, [issue dicts]) for a paper link."""
    _, rows = pl.load_tsv()
    listed = next((r["id"] for r in rows if pl.same_paper(r["url"], url)), "")
    needle = pl.arxiv_id(url) or pl.canonical_url(url)
    issues = [i for i in pl.gh_api("issues?state=all&per_page=100", paginate=True)
              if "pull_request" not in i and needle and needle in (i.get("body") or "")]
    return listed, issues


def issue_body(title, url, reason, tags):
    """Same layout as the "Recommend a paper" issue form, so scripts/new_paper.py can read it."""
    boxes = "\n".join(f"- [{'X' if label[0] in tags else ' '}] {label}" for label in TAG_LABELS)
    return (f"### Paper title\n\n{title}\n\n### Link\n\n{url}\n\n"
            f"### Why it belongs in the list\n\n{reason}\n\n### Domain tags\n\n{boxes}\n")


def cmd_check(args):
    listed, issues = find_existing(args.url)
    print(f"link: {pl.canonical_url(args.url)}")
    print(f"listed: {listed or 'no'}")
    for i in issues:
        print(f"issue: #{i['number']} ({i['state']}) {i['title']}")
    if not issues:
        print("issue: none")
    sys.exit(1 if listed or issues else 0)


def cmd_open(args):
    url = pl.canonical_url(args.url)
    tags = ";".join(sorted(set(re.findall(r"[0-4]", args.tags))))
    title = " ".join(args.title.split())
    if "|" in title:
        sys.exit("The title must not contain '|'")
    listed, issues = find_existing(url)
    if listed:
        sys.exit(f"Already listed as {listed}. To correct it, open an issue with the evidence instead.")
    if issues and not args.force:
        found = ", ".join(f"#{i['number']} ({i['state']})" for i in issues)
        sys.exit(f"This paper already has an issue: {found}. Continue on that issue's branch, "
                 "or pass --force to open another one.")
    body = issue_body(title, url, args.reason.strip(), tags)
    if args.dry_run:
        print(f"[dry run] would open issue: [Paper] {title}\n\n{body}")
        return
    if git("status", "--porcelain", "-uall"):
        sys.exit("The working tree has uncommitted changes. Commit or stash them first: "
                 "the annotation needs a clean branch.")
    base = default_branch()
    git("fetch", "-q", "origin", base)
    fields = {"title": f"[Paper] {title}", "body": body, "labels": ["paper"]}
    try:
        issue = pl.gh_api("issues", "POST", fields)
    except RuntimeError:                      # no permission to set labels, or the label does not exist
        del fields["labels"]
        issue = pl.gh_api("issues", "POST", fields)
    n = issue["number"]
    git("switch", "-c", f"paper/issue-{n}", "FETCH_HEAD")
    out = subprocess.run([sys.executable, str(Path(__file__).with_name("new_paper.py")), str(n),
                          "--title", title, "--url", url, "--tags", tags], capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"Issue #{n} is open, but creating the annotation file failed:\n{out.stderr.strip()}")
    print(f"issue: #{n} {issue['html_url']}")
    print(f"branch: paper/issue-{n}")
    print(f"file: data/pending/issue-{n}.yml")
    print("next: fill in the file, show the draft and the points to check to the user, and run "
          f"`python3 scripts/add_paper.py submit {n}` only after they have answered.")


def cmd_submit(args):
    n = args.issue
    rel = f"data/pending/issue-{n}.yml"
    branch = f"paper/issue-{n}"
    if git("rev-parse", "--abbrev-ref", "HEAD") != branch:
        sys.exit(f"Switch to the branch {branch} first.")
    path = pl.ROOT / rel
    if not path.exists():
        sys.exit(f"{rel} does not exist.")
    row = pl.normalise(pl.parse_pending(path.read_text(encoding="utf-8")))
    check = subprocess.run([sys.executable, str(Path(__file__).with_name("check_data.py"))],
                           capture_output=True, text=True)
    if check.returncode:
        sys.exit(f"The annotation does not pass the checks yet:\n{(check.stdout + check.stderr).strip()}")
    base = default_branch()
    git("fetch", "-q", "origin", base)
    changed = {line.split(maxsplit=1)[-1].strip('"') for line in git("status", "--porcelain", "-uall").splitlines()}
    changed |= set(filter(None, git("diff", "--name-only", "FETCH_HEAD...HEAD").splitlines()))
    extra = sorted(changed - {rel})
    if extra:
        sys.exit("The pull request may contain only the annotation file, but these also changed: "
                 + ", ".join(extra))
    short = args.short or re.split(r"[:(]", row["title"])[0].strip()
    title = f"Annotate paper for #{n}: {short}"
    if git("status", "--porcelain", "-uall"):
        message = title + ("\n\n" + "\n".join(args.trailer) if args.trailer else "")
        git("add", rel)
        git("commit", "-q", "-m", message)
    git("push", "-q", "-u", "origin", branch)

    reader = args.reader or "state here who read the paper and how much of it"
    body = f"""## Issue

#{n}

This pull request contains only `{rel}`.

## Annotator checklist

- [ ] I read the paper myself, and `reading` says how much (full text / partial text / abstract only): {reader}. `reading` is `{row.get('reading', '')}`. Left for the confirmer to judge against the paper.
- [x] Self-reference depth, feedback source, loop automation and evidence strength each cite the paper
- [x] Anything I was unsure about is in `review_points`, each with options and my recommendation
- [x] I ran `python3 scripts/check_data.py`
- [x] I did not fill in an id or confirmation fields, and did not change `data/papers.tsv`

The annotation appears on the issue page automatically. A confirmer checks it there and comments `/confirm` **on issue #{n}** (not on this pull request); this pull request is then closed automatically and the workflow adds the paper to the list.
"""
    if args.footer:
        body += "\n" + "\n".join(args.footer) + "\n"
    open_prs = [p for p in pl.gh_api("pulls?state=open&per_page=100", paginate=True)
                if p["head"]["ref"] == branch]
    if open_prs:
        pr = open_prs[0]
        print(f"pull request: #{pr['number']} {pr['html_url']} (already open; pushed the update)")
    else:
        pr = pl.gh_api("pulls", "POST", {"title": title, "head": branch, "base": base, "body": body})
        print(f"pull request: #{pr['number']} {pr['html_url']}")
    slug = pl.repo_slug()
    print(f"issue: https://github.com/{slug}/issues/{n}")
    print(f"next: the annotation appears on issue #{n} within a minute or two. A human confirmer checks it "
          "against the paper and comments /confirm there. Do not post that comment yourself.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("url")
    c.set_defaults(func=cmd_check)
    o = sub.add_parser("open")
    o.add_argument("--title", required=True, help="title as printed on the paper")
    o.add_argument("--url", required=True)
    o.add_argument("--reason", required=True, help="one or two sentences: the improvement loop, the domain, why it is relevant")
    o.add_argument("--tags", default="", help="domain tags, e.g. '0;1'")
    o.add_argument("--force", action="store_true", help="open an issue even if one exists for this link")
    o.add_argument("--dry-run", action="store_true", help="print the issue instead of opening it")
    o.set_defaults(func=cmd_open)
    s = sub.add_parser("submit")
    s.add_argument("issue", type=int)
    s.add_argument("--short", default="", help="short paper name for the pull request title")
    s.add_argument("--reader", default="", help="who read the paper and how much, for the checklist")
    s.add_argument("--trailer", action="append", default=[], help="line appended to the commit message (repeatable)")
    s.add_argument("--footer", action="append", default=[], help="line appended to the pull request body (repeatable)")
    s.set_defaults(func=cmd_submit)
    args = ap.parse_args()
    try:
        args.func(args)
    except RuntimeError as exc:
        sys.exit(f"GitHub request failed: {exc}")


if __name__ == "__main__":
    main()
