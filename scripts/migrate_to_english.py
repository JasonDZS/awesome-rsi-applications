#!/usr/bin/env python3
"""Convert controlled values written in the old Chinese vocabulary to the English one.

  python3 scripts/migrate_to_english.py data/pending/issue-5.yml      # rewrite in place
  python3 scripts/migrate_to_english.py data/local/drafts.tsv --out drafts-en.tsv

Handles .tsv data files and data/pending/*.yml annotation files. Only fields with a fixed
vocabulary are converted (status, tags-adjacent enums, feedback, criteria, subfield, venue,
reading, ...). Free text (task, object, r_evidence, rounds, result, limits, notes, review_points)
must be translated by a person; the script lists every field that still contains Chinese.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402

VALUES = {
    "待核对": pl.UNCLEAR, "未报告": pl.NOT_REPORTED,
    "待确认": pl.STATUS_PENDING, "已确认": pl.STATUS_CONFIRMED,
    # feedback
    "形式验证": "formal verification", "自动评测": "automated evaluation", "仿真": "simulation",
    "真实实验": "real-world experiment", "人类评审": "human review", "学习型评判": "learned judge",
    "自评": "self-evaluation",
    # criteria
    "闭环": "closed loop", "自指": "self-reference", "累积": "accumulation",
    # loop, accumulation, cost, reversibility, evidence, confidence
    "人在回路": "human-in-the-loop", "半自动": "semi-automatic", "全自动": "fully automatic",
    "单轮": "single round", "单一谱系的多代迭代": "multi-generation single lineage",
    "种群或档案库式的开放演化": "open-ended population or archive",
    "秒到分钟": "seconds to minutes", "小时": "hours", "天到周": "days to weeks",
    "月以上或必须人工": "months or longer, or requires humans",
    "完全可逆": "fully reversible", "有消耗可重试": "retryable at a cost", "不可逆": "irreversible",
    "任务内": "in-task", "跨任务": "cross-task", "跨任务且独立验证": "cross-task, independently verified",
    "高": "high", "中": "medium", "低": "low",
    # reading
    "全文": "full text", "部分全文": "partial text", "仅摘要": "abstract only",
    "摘要": "abstract", "片段": "excerpt", "未读": "unread",
    # claim
    "自我改进": "self-improvement", "未自称": "not claimed",
    # subfields
    "智能体自我改进": "Agent self-improvement", "数据与权重的自适应": "Data and weight self-adaptation",
    "自动化 ML 研究": "Automated ML research", "软件工程": "Software engineering",
    "算法发现": "Algorithm discovery", "芯片设计与系统优化": "Chip design and systems optimization",
    "系统优化": "Chip design and systems optimization",
    "数学": "Mathematics", "化学与材料": "Chemistry and materials", "生物与医药": "Biology and medicine",
    "物理与地球科学": "Physics and earth sciences", "跨子类": "Cross-subfield",
    "机器人技能习得": "Robot skill acquisition", "奖励与课程的自动设计": "Automated reward and curriculum design",
    "开放式具身学习": "Open-ended embodied learning", "经济与金融": "Economics and finance",
    "社会仿真": "Social simulation", "预测": "Forecasting", "已部署的服务型智能体": "Deployed service agents",
    "政策与教育": "Policy and education", "法律": "Law",
}
MULTI = {"subclass", "criteria", "feedback"}
SINGLE = {"loop", "accumulation", "cost", "reversibility", "evidence", "confidence", "reading", "status"}
CJK = re.compile(r"[　-〿一-鿿＀-￯]")


def convert(key, value):
    v = value.strip()
    if not v:
        return value
    if key in MULTI:
        return "; ".join(VALUES.get(x, x) for x in pl.split_multi(v))
    if key in SINGLE:
        return VALUES.get(v, v)
    if key == "venue":
        return re.sub(r"\s*预印本$", " preprint", v)
    if key == "R":
        if v == "待核对":
            return pl.UNCLEAR
        m = re.fullmatch(r"(R[0-4])，或 (R[0-4]) 待核对", v)
        if m:
            return f"{m.group(1)} or {m.group(2)} (unclear)"
        m = re.fullmatch(r"(R[0-4])（限于(.+?)层）", v)
        return f"{m.group(1)} (limited to the {m.group(2).replace('提示', 'prompt')} level)" if m else v
    if key == "claim":
        m = re.fullmatch(r"(RSI|自我改进|未自称|待核对)(（.*）)?", v)
        if m:
            head = VALUES.get(m.group(1), m.group(1))
            return head + (f" ({m.group(2)[1:-1]})" if m.group(2) else "")
    return value


def migrate_tsv(src, dst):
    cols, rows = pl.load_tsv(src)
    for r in rows:
        for k in r:
            r[k] = convert(k, r[k] or "")
    pl.save_tsv(rows, dst)
    return [(r.get("id", "?"), k) for r in rows for k in cols if CJK.search(r.get(k) or "")]


def migrate_yml(src, dst):
    out, left = [], []
    for line in Path(src).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z_]+):[ \t]*(.*)$", line)
        if m and m.group(2) != "|":
            line = f"{m.group(1)}: {convert(m.group(1), m.group(2))}".rstrip()
        out.append(line)
    text = "\n".join(out) + "\n"
    Path(dst).write_text(text, encoding="utf-8")
    raw = pl.parse_pending(text)
    left = [(Path(src).name, k) for k, v in raw.items() if CJK.search(v)]
    if any(CJK.search(l) for l in out if l.lstrip().startswith("#")):
        left.append((Path(src).name, "comments"))
    return left


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out", help="write here instead of rewriting the file in place")
    a = ap.parse_args()
    dst = a.out or a.file
    left = (migrate_yml if a.file.endswith(".yml") else migrate_tsv)(a.file, dst)
    print(f"wrote {dst}")
    if left:
        print("Still contains Chinese, translate by hand:")
        for where, key in left:
            print(f"  {where}: {key}")


if __name__ == "__main__":
    main()
