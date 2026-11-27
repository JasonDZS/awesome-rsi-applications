#!/usr/bin/env python3
"""Print the review comment (Markdown) for one annotation file, including any format problems.

  python3 scripts/render_review.py data/pending/issue-12.yml [--source "来自 PR #13"]
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
    errors = [f"不要填写 {k}" if k in pl.CONFIRM_COLS or k == "id" else f"未知字段 {k}"
              for k in raw if k not in pl.PENDING_KEYS]
    row = pl.normalise({k: v for k, v in raw.items() if k in pl.PENDING_KEYS})
    errors += [e.split("：", 1)[1] for e in pl.validate(row, "x")]
    _, rows = pl.load_tsv()
    dup = next((r["id"] for r in rows if row.get("url") and r["url"] == row["url"]), None)
    if dup:
        errors.append(f"这篇论文已收录为 {dup}")
    return row, errors


def main():
    source = sys.argv[sys.argv.index("--source") + 1] if "--source" in sys.argv else ""
    row, errors = load(sys.argv[1])
    print(pl.render_review(row, errors, source))
    if row.get("reading") == "仅摘要":
        print("\n> 阅读深度是“仅摘要”：这份标注可以先放着，但读过全文之前不能确认。")
    print("\n---\n确认人：对照原文核对后，在本 Issue 评论 `/confirm` 即确认收录；"
          "有不同意见就直接评论要改什么，填写人更新分支后这里会刷新。")


if __name__ == "__main__":
    main()
