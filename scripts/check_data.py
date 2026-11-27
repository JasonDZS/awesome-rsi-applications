#!/usr/bin/env python3
"""Validate data/papers.tsv. Exits non-zero on any problem.

The confirmation rule: a paper counts as confirmed only when a human developer has
checked it against the original paper and recorded their GitHub username and the date.
"""
import csv
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "papers.tsv"
COLUMNS = ["id", "title", "url", "date", "venue", "tags", "subclass", "task", "criteria", "object",
           "R", "r_evidence", "feedback", "loop", "accumulation", "rounds", "cost", "reversibility",
           "claim", "evidence", "result", "limits", "reading", "confidence", "notes",
           "status", "confirmed_by", "confirmed_at"]
FEEDBACK = {"形式验证", "自动评测", "仿真", "真实实验", "人类评审", "学习型评判", "自评", "待核对"}
ENUMS = {
    "loop": {"", "人在回路", "半自动", "全自动", "待核对"},
    "accumulation": {"", "单轮", "单一谱系的多代迭代", "种群或档案库式的开放演化", "待核对"},
    "cost": {"", "秒到分钟", "小时", "天到周", "月以上或必须人工", "未报告"},
    "reversibility": {"", "完全可逆", "有消耗可重试", "不可逆", "待核对"},
    "evidence": {"", "任务内", "跨任务", "跨任务且独立验证", "待核对"},
    "reading": {"全文", "部分全文", "仅摘要", "摘要", "片段", "未读"},
    "confidence": {"", "高", "中", "低"},
    "status": {"待确认", "已确认"},
}
# accounts that must never appear as the confirmer: confirmation has to come from a person
NOT_HUMAN = re.compile(r"(\[bot\]$|^claude$|^copilot$|^github-actions$|bot$)", re.I)


def main():
    errors = []
    with DATA.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        if reader.fieldnames != COLUMNS:
            sys.exit(f"unexpected columns: {reader.fieldnames}")
        rows = list(reader)
    seen_ids, seen_urls = set(), set()
    for n, r in enumerate(rows, start=2):
        where = f"line {n} ({r.get('id')})"
        if None in r or None in r.values():
            errors.append(f"{where}: wrong number of fields")
            continue
        if not re.fullmatch(r"P\d{3,}", r["id"]) or r["id"] in seen_ids:
            errors.append(f"{where}: bad or duplicate id")
        seen_ids.add(r["id"])
        if r["url"]:
            if r["url"] in seen_urls:
                errors.append(f"{where}: duplicate url")
            seen_urls.add(r["url"])
        if not r["title"]:
            errors.append(f"{where}: empty title")
        if not re.fullmatch(r"\d{4}(-\d{2})?", r["date"]):
            errors.append(f"{where}: date must be YYYY or YYYY-MM")
        if not re.fullmatch(r"[0-4](;[0-4])*", r["tags"]):
            errors.append(f"{where}: tags must be digits 0-4 joined by ';'")
        if r["R"] and not re.match(r"(R[0-4]|待核对)", r["R"]):
            errors.append(f"{where}: R must start with R0-R4 or be 待核对")
        for item in filter(None, r["feedback"].split("；")):
            if item not in FEEDBACK:
                errors.append(f"{where}: unknown feedback source '{item}'")
        for col, allowed in ENUMS.items():
            if r[col] not in allowed:
                errors.append(f"{where}: {col}='{r[col]}' is not an allowed value")
        by, at = r["confirmed_by"], r["confirmed_at"]
        if r["status"] == "已确认":
            if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", by) or NOT_HUMAN.search(by):
                errors.append(f"{where}: 已确认 needs confirmed_by = a human's GitHub username")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", at):
                errors.append(f"{where}: 已确认 needs confirmed_at = YYYY-MM-DD")
            if r["reading"] not in {"全文", "部分全文"}:
                errors.append(f"{where}: a confirmed paper must have been read (reading = 全文 or 部分全文)")
        elif by or at:
            errors.append(f"{where}: 待确认 rows must leave confirmed_by and confirmed_at empty")
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s) in {DATA.name}")
    confirmed = sum(r["status"] == "已确认" for r in rows)
    print(f"ok: {len(rows)} papers, {confirmed} confirmed by a human, {len(rows) - confirmed} pending")


if __name__ == "__main__":
    main()
