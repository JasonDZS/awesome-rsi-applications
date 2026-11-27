#!/usr/bin/env python3
"""Convert an "添加论文" issue (GitHub issue form) into a row of data/papers.tsv.

Usage:
  gh issue view 12 --json body -q .body | python3 scripts/issue_to_row.py            # print the row
  gh issue view 12 --json body -q .body | python3 scripts/issue_to_row.py --append   # append to the TSV
  python3 scripts/issue_to_row.py issue_body.md --append

The maintainer should review the appended row, then run scripts/build_readme.py.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "papers.tsv"

# issue-form label -> TSV column
LABELS = {
    "论文标题": "title", "链接": "url", "首发年月": "date", "发表状态": "venue",
    "领域标签": "tags", "子类": "subclass", "任务": "task", "纳入标准": "criteria",
    "改进对象": "object", "自指深度": "R", "自指深度的依据": "r_evidence",
    "反馈来源": "feedback", "闭环程度": "loop", "累积方式": "accumulation",
    "改进轮数": "rounds", "验证成本": "cost", "失败可逆性": "reversibility",
    "自称程度": "claim", "证据强度": "evidence", "主要结果": "result",
    "失败与局限": "limits", "阅读深度": "reading", "置信度": "confidence", "备注": "notes",
}
EMPTY = {"_No response_", "None", ""}


def strip_paren(s):
    """'自动评测（测试、基准、回测）' -> '自动评测'"""
    return re.split(r"[（(]", s, maxsplit=1)[0].strip()


def one_line(s):
    return re.sub(r"\s+", " ", s).replace("|", "/").strip()


def parse(body):
    sections = re.split(r"^### +", body, flags=re.M)[1:]
    raw = {}
    for sec in sections:
        label, _, value = sec.partition("\n")
        col = LABELS.get(label.strip())
        if col:
            raw[col] = value.strip()
    row = {}
    for col, v in raw.items():
        if v in EMPTY:
            row[col] = ""
        elif col == "tags":
            row[col] = ";".join(sorted(set(re.findall(r"(?:^|,\s*)([0-4])\b", v))))
        elif col == "subclass":
            items = [re.sub(r"^[0-4]\s*·\s*", "", strip_paren(x)) for x in v.split(",")]
            row[col] = "；".join(i for i in items if i)
        elif col == "criteria":
            checked = re.findall(r"- \[[xX]\] *(闭环|自指|累积)", v)
            row[col] = "；".join(checked)
        elif col == "R":
            m = re.match(r"R[0-4]", v)
            row[col] = m.group(0) if m else "待核对"
        elif col == "feedback":
            row[col] = "；".join(strip_paren(x) for x in v.split(",") if x.strip())
        elif col in {"loop", "accumulation", "cost", "reversibility", "claim", "evidence",
                     "reading", "confidence"}:
            row[col] = strip_paren(v)
        else:
            row[col] = one_line(v)
    return row


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    append = "--append" in sys.argv
    body = Path(args[0]).read_text(encoding="utf-8") if args else sys.stdin.read()

    with DATA.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        columns = reader.fieldnames
        existing = list(reader)

    row = parse(body)
    missing = [c for c in ("title", "url", "date", "tags", "reading") if not row.get(c)]
    if missing:
        sys.exit(f"missing required fields: {', '.join(missing)}")
    dup = [r["id"] for r in existing if row["url"] and r["url"] == row["url"]]
    if dup:
        sys.exit(f"already in the list as {dup[0]}")

    last = max(int(r["id"][1:]) for r in existing)
    row["id"] = f"P{last + 1:03d}"
    line = "|".join(row.get(c, "") for c in columns)
    if append:
        with DATA.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"appended {row['id']}: {row['title']}", file=sys.stderr)
    else:
        print(line)


if __name__ == "__main__":
    main()
