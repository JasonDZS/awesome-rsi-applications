#!/usr/bin/env python3
"""Record a human confirmation. Run by the /confirm workflow, never by hand and never by an AI assistant.

  python3 scripts/confirm.py --file issue-12.yml --by <github login> --date YYYY-MM-DD

Checks that the commenter is on the confirmer list and is not an automation account, that the
annotation is valid and was read in full, then appends the row to data/papers.tsv as confirmed.
Prints the new paper id on success; prints the reason and exits 1 on refusal.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402
from render_review import load  # noqa: E402

CONFIRMERS = pl.ROOT / ".github" / "confirmers.txt"


def confirmers():
    lines = CONFIRMERS.read_text(encoding="utf-8").splitlines()
    return {x.split("#")[0].strip().lstrip("@").lower() for x in lines} - {""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--by", required=True)
    ap.add_argument("--date", required=True)
    args = ap.parse_args()

    if pl.NOT_HUMAN.search(args.by):
        sys.exit(f"@{args.by} is an automation account and cannot confirm papers.")
    if args.by.lower() not in confirmers():
        sys.exit(f"@{args.by} is not on the confirmer list (.github/confirmers.txt).")
    row, errors = load(args.file)
    if errors:
        sys.exit("The annotation still has format problems; fix them before confirming:\n"
                 + "\n".join(f"- {e}" for e in errors))
    if row.get("reading") not in pl.READ_IN_FULL:
        sys.exit("Reading depth is 'abstract only'; the paper cannot be confirmed until it has been read in full.")

    _, rows = pl.load_tsv()
    new = {c: row.get(c, "") for c in pl.COLUMNS}
    new.update(id=pl.next_id(rows), status=pl.STATUS_CONFIRMED, confirmed_by=args.by, confirmed_at=args.date)
    problems = pl.validate_confirmation(new, new["id"])
    if problems:
        sys.exit("\n".join(problems))
    pl.save_tsv(rows + [new])
    print(new["id"])


if __name__ == "__main__":
    main()
