#!/usr/bin/env python3
"""Validate data/papers.tsv and data/pending/*.yml. Exits non-zero on any problem.

  python3 scripts/check_data.py                    # validate everything
  python3 scripts/check_data.py --base base.tsv    # also forbid hand-edited confirmations (used in CI for PRs)

Confirmation rule: a paper is confirmed by a human developer commenting /confirm on its issue.
The workflow then writes status/confirmed_by/confirmed_at. Nobody edits those columns by hand.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402


def check_tsv(errors):
    cols, rows = pl.load_tsv()
    if cols != pl.COLUMNS:
        sys.exit(f"papers.tsv 的表头不对：{cols}")
    ids, urls = set(), set()
    for n, r in enumerate(rows, start=2):
        where = f"papers.tsv 第 {n} 行（{r.get('id')}）"
        if None in r or None in r.values():
            errors.append(f"{where}：列数不对")
            continue
        if not r["id"] or r["id"] in ids:
            errors.append(f"{where}：编号为空或重复")
        ids.add(r["id"])
        if r["url"] and r["url"] in urls:
            errors.append(f"{where}：链接重复")
        urls.add(r["url"])
        row = dict(r)
        if not row["url"]:
            row["url"] = "https://example.invalid"   # a few early rows have no link yet
        errors.extend(pl.validate(row, where, legacy_ok=True))
        errors.extend(pl.validate_confirmation(r, where))
    return rows


def check_pending(errors, rows):
    known = {r["url"]: r["id"] for r in rows if r["url"]}
    count = 0
    for path in sorted(pl.PENDING_DIR.glob("*")):
        rel = path.relative_to(pl.ROOT).as_posix()
        if path.name == ".gitkeep":
            continue
        count += 1
        if not pl.PENDING_RE.match(rel):
            errors.append(f"{rel}：文件名应为 issue-<Issue 编号>.yml")
            continue
        try:
            raw = pl.parse_pending(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(f"{rel}：{exc}")
            continue
        for key in raw:
            if key in pl.CONFIRM_COLS or key == "id":
                errors.append(f"{rel}：不要填写 {key}，编号和确认信息由 /confirm 流程写入")
            elif key not in pl.PENDING_KEYS:
                errors.append(f"{rel}：未知字段 {key}")
        row = pl.normalise(raw)
        errors.extend(pl.validate(row, rel))
        if row.get("url") in known:
            errors.append(f"{rel}：这篇论文已收录为 {known[row['url']]}")
    return count


def check_against_base(errors, rows, base_path):
    """In a pull request, confirmation columns must be identical to the base branch."""
    _, base = pl.load_tsv(base_path)
    before = {r["id"]: r for r in base}
    for r in rows:
        old = before.get(r["id"])
        new_conf = [r[c] for c in pl.CONFIRM_COLS]
        if old is None:
            if new_conf != ["待确认", "", ""]:
                errors.append(f"{r['id']}：PR 里新增的行必须是待确认；确认只能通过在 Issue 评论 /confirm 完成")
        elif new_conf != [old[c] for c in pl.CONFIRM_COLS]:
            errors.append(f"{r['id']}：确认信息不能手工修改；确认只能通过在 Issue 评论 /confirm 完成")


def main():
    errors = []
    rows = check_tsv(errors)
    pending = check_pending(errors, rows)
    if "--base" in sys.argv:
        check_against_base(errors, rows, sys.argv[sys.argv.index("--base") + 1])
    if errors:
        print("\n".join(errors))
        sys.exit(f"共 {len(errors)} 个问题")
    confirmed = sum(r["status"] == "已确认" for r in rows)
    print(f"ok: {len(rows)} papers, {confirmed} confirmed by a human, "
          f"{len(rows) - confirmed} pending confirmation, {pending} annotation file(s) under review")


if __name__ == "__main__":
    main()
