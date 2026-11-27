#!/usr/bin/env python3
"""Print the review comment (Markdown) for one annotation file, including any format problems.

  python3 scripts/render_review.py data/pending/issue-12.yml [--source "From #13"]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402


def load(path):
    """Return (row, problems) for an annotation file."""
    try:
        raw = pl.parse_pending(Path(path).read_text(encoding="utf-8"))
    except ValueError as exc:
        return {}, [str(exc)]
    errors = [f"do not fill in {k}" if k in pl.CONFIRM_COLS or k == "id" else f"unknown field {k}"
              for k in raw if k not in pl.PENDING_KEYS]
    row = pl.normalise({k: v for k, v in raw.items() if k in pl.PENDING_KEYS})
    errors += [e.split(": ", 1)[1] for e in pl.validate(row, "x")]
    _, rows = pl.load_tsv()
    dup = next((r["id"] for r in rows if row.get("url") and r["url"] == row["url"]), None)
    if dup:
        errors.append(f"this paper is already listed as {dup}")
    return row, errors


def main():
    source = sys.argv[sys.argv.index("--source") + 1] if "--source" in sys.argv else ""
    row, errors = load(sys.argv[1])
    print(pl.render_review(row, errors, source))
    if row.get("reading") == "abstract only":
        print("\n> Reading depth is 'abstract only': this annotation can stay open, "
              "but it cannot be confirmed until the paper has been read in full.")
    print("\n---\nConfirmer: check the annotation against the paper, then comment `/confirm` on this issue "
          "to add the paper to the list. If you disagree with something, comment what should change; "
          "this rendering is replaced when the annotator updates the branch.")


if __name__ == "__main__":
    main()
