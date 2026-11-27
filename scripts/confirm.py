#!/usr/bin/env python3
"""Record a human confirmation. Run by the /confirm workflow, never by hand and never by an AI assistant.

  python3 scripts/confirm.py --file issue-12.yml --by <github login> --date YYYY-MM-DD

Checks that the commenter is on the confirmer list and is not an automation account, that the
annotation is valid and was read in full, then appends the row to data/papers.tsv as 已确认.
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
        sys.exit(f"@{args.by} 是自动化账号，不能确认论文。")
    if args.by.lower() not in confirmers():
        sys.exit(f"@{args.by} 不在确认人名单（.github/confirmers.txt）里。")
    row, errors = load(args.file)
    if errors:
        sys.exit("标注还有格式问题，修正后再确认：\n" + "\n".join(f"- {e}" for e in errors))
    if row.get("reading") not in pl.READ_IN_FULL:
        sys.exit("阅读深度是“仅摘要”，读过全文之前不能确认。")

    _, rows = pl.load_tsv()
    new = {c: row.get(c, "") for c in pl.COLUMNS}
    new.update(id=pl.next_id(rows), status="已确认", confirmed_by=args.by, confirmed_at=args.date)
    problems = pl.validate_confirmation(new, new["id"])
    if problems:
        sys.exit("\n".join(problems))
    pl.save_tsv(rows + [new])
    print(new["id"])


if __name__ == "__main__":
    main()
