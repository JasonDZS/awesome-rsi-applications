#!/usr/bin/env python3
"""Turn the annotation carried in an issue body into data/pending/issue-<N>.yml.

  python3 scripts/intake.py body.md --out issue-12.yml [--old old-body.md]

Run by the paper-intake workflow. An issue can carry a whole annotation in an "Annotation"
section (a fenced yaml block), as produced by the annotation page or pasted into the
"Recommend a paper" form. The issue text is untrusted input: it is parsed as flat key/value
data, only known fields are kept, and the file is written out again in canonical form.

Exit codes: 0 file written; 3 nothing to do (no annotation, or --old has the same annotation);
1 the annotation cannot be parsed (the reason is printed).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402

FORM = {"title": "Paper title", "url": "Link", "tags": "Domain tags"}


def sections(body):
    out = {}
    for m in re.finditer(r"^### (.+?)[ \t]*\r?\n(.*?)(?=^### |\Z)", body or "", re.S | re.M):
        value = m.group(2).strip()
        out[m.group(1).strip()] = "" if value == "_No response_" else value
    return out


def annotation_text(body):
    """The text of the Annotation section, without its code fence; '' if there is none."""
    text = sections(body.replace("\r\n", "\n")).get("Annotation", "")
    m = re.match(r"^```[a-zA-Z]*\n(.*?)\n?```\s*$", text, re.S)
    return (m.group(1) if m else text).strip()


def build(body):
    sec = sections(body.replace("\r\n", "\n"))
    raw = pl.parse_pending(annotation_text(body))
    row = {k: v for k, v in raw.items() if k in pl.PENDING_KEYS}
    # the form fields are the fallback for what the annotation leaves empty
    if not row.get("title"):
        row["title"] = sec.get(FORM["title"], "")
    if not row.get("url"):
        row["url"] = sec.get(FORM["url"], "")
    if not row.get("tags"):
        row["tags"] = ";".join(re.findall(r"- \[[xX]\] ([0-4])", sec.get(FORM["tags"], "")))
    row["url"] = pl.canonical_url(row.get("url", ""))
    dropped = sorted(k for k in raw if k not in pl.PENDING_KEYS)
    return row, dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("body")
    ap.add_argument("--out", required=True)
    ap.add_argument("--old", help="the issue body before an edit; nothing is done if its annotation is the same")
    args = ap.parse_args()

    body = Path(args.body).read_text(encoding="utf-8")
    if not annotation_text(body):
        sys.exit(3)
    if args.old and annotation_text(Path(args.old).read_text(encoding="utf-8")) == annotation_text(body):
        sys.exit(3)
    try:
        row, dropped = build(body)
    except ValueError as exc:
        print(f"The Annotation section could not be read: {exc}")
        sys.exit(1)
    Path(args.out).write_text(pl.dump_pending(row), encoding="utf-8")
    if dropped:
        print("Ignored fields that annotators do not set: " + ", ".join(dropped))


if __name__ == "__main__":
    main()
