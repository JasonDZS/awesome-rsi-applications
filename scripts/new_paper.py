#!/usr/bin/env python3
"""Create data/pending/issue-<N>.yml, the annotation file for the paper recommended in issue N.

  python3 scripts/new_paper.py 12                      # reads the issue with the gh CLI
  python3 scripts/new_paper.py 12 --title "..." --url https://arxiv.org/abs/....   # without gh

Run it on a branch named paper/issue-<N>. Fill the file in while reading the paper, then open a
pull request. The confirmer reviews it on the issue page and comments /confirm there.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402

LEVELS = " / ".join(f"{k} {v}" for k, v in pl.LEVELS.items())
HELP = {
    "title": "Title, as printed on the paper",
    "url": "Link; prefer the arXiv abstract page",
    "date": "First released, YYYY-MM",
    "venue": "Publication status: arXiv preprint, or venue and year",
    "tags": "Domain tags, one or more, separated by ; : " + ", ".join(f"{k} {v}" for k, v in pl.DOMAINS.items()),
    "subclass": "Subfield(s), separated by ; . Use a subfield already in the README; "
                "if none fits, raise it in review_points",
    "task": "Task: what the system does in the experiments",
    "criteria": "Inclusion criteria met, separated by ; : " + ", ".join(pl.CRITERIA)
                + " (a paper meeting only the closed loop is an R0 borderline case)",
    "object": "What is improved: prompts, skill library, scaffold code, weights, ...",
    "R": "Self-reference depth: " + LEVELS,
    "r_evidence": "Evidence for the depth: section and quotation from the paper",
    "feedback": "Feedback source(s), separated by ; : " + ", ".join(pl.FEEDBACK[:-1]),
    "loop": "Loop automation: " + " / ".join(pl.ENUMS["loop"][:-1]),
    "accumulation": "Accumulation: " + " / ".join(pl.ENUMS["accumulation"][:-1]),
    "rounds": f"Improvement rounds: rounds or generations reported in the paper, or '{pl.NOT_REPORTED}'",
    "cost": "Verification cost (only as reported, never inferred): " + " / ".join(pl.ENUMS["cost"]),
    "reversibility": "Failure reversibility: " + " / ".join(pl.ENUMS["reversibility"][:-1]),
    "claim": "Authors' claim, from the title and abstract: " + " / ".join(pl.CLAIMS)
             + "; add an explicit disclaimer in parentheses, e.g. self-improvement (states it is not recursive)",
    "evidence": "Evidence strength: " + " / ".join(pl.ENUMS["evidence"][:-1]),
    "result": "Main result: one sentence with numbers",
    "limits": "Failures and limitations: as reported in the paper",
    "reading": "Reading depth: " + " / ".join(pl.READING_NEW) + " (abstract-only annotations cannot be confirmed)",
    "confidence": "Your confidence in this annotation: " + " / ".join(pl.ENUMS["confidence"]),
    "notes": "Notes: sources for the other fields, feedback details, open questions",
}

# issue-form headings; the Chinese ones are kept so issues opened with the old form still work
HEADINGS = {"title": ("Paper title", "论文标题"), "url": ("Link", "链接"), "tags": ("Domain tags", "领域标签")}


def issue_fields(number):
    out = subprocess.run(["gh", "issue", "view", str(number), "--json", "title,body"],
                         capture_output=True, text=True, check=True).stdout
    body = json.loads(out)["body"] or ""
    sections = {}
    for m in re.finditer(r"^### (.+?)\n+(.*?)(?=^### |\Z)", body, re.S | re.M):
        value = m.group(2).strip()
        sections[m.group(1).strip()] = "" if value == "_No response_" else value
    def get(key):
        return next((sections[h] for h in HEADINGS[key] if sections.get(h)), "")
    tags = ";".join(re.findall(r"- \[[xX]\] ([0-4])", get("tags")))
    return {"title": get("title"), "url": get("url"), "tags": tags}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue", type=int)
    ap.add_argument("--title", default="")
    ap.add_argument("--url", default="")
    args = ap.parse_args()

    known = {"title": args.title, "url": args.url, "tags": ""}
    if not (args.title and args.url):
        try:
            known.update({k: v for k, v in issue_fields(args.issue).items() if v})
        except (OSError, subprocess.CalledProcessError, ValueError):
            print("Could not read the issue (needs the gh CLI). Writing an empty template; "
                  "fill in the title and link by hand.", file=sys.stderr)

    path = pl.PENDING_DIR / f"issue-{args.issue}.yml"
    if path.exists():
        sys.exit(f"{path.relative_to(pl.ROOT)} already exists")
    _, rows = pl.load_tsv()
    dup = next((r["id"] for r in rows if known["url"] and r["url"] == known["url"]), None)
    if dup:
        sys.exit(f"This paper is already listed as {dup}")

    lines = [f"# Annotation for the paper recommended in issue #{args.issue}. One field per line, "
             "written as `field: value`; values must not contain '|'.",
             f"# If you cannot decide, write {pl.UNCLEAR} (for cost: {pl.NOT_REPORTED}) and give the options "
             "and your recommendation in review_points.",
             "# Do not add an id or confirmation fields: the workflow writes them after a confirmer comments "
             "/confirm on the issue.", ""]
    for key in pl.PENDING_KEYS[:-1]:
        value = known.get(key, "").replace("\n", " ").replace("|", "/")
        lines += [f"# {HELP[key]}", f"{key}: {value}", ""]
    lines += ["# Points for the confirmer to check. For each: the specific question, the options (with the "
              "evidence for each), your recommendation and why, and where in the paper to look.",
              "# Shown as-is on the issue page. Multi-line Markdown is fine; indent every line by two spaces.",
              "review_points: |",
              "  1. ", ""]
    pl.PENDING_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created {path.relative_to(pl.ROOT)}")


if __name__ == "__main__":
    main()
