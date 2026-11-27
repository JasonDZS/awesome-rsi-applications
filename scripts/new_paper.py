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

HELP = {
    "title": "论文标题（原文标题）",
    "url": "链接，优先 arXiv 摘要页",
    "date": "首发年月，YYYY-MM",
    "venue": "发表状态：预印本，或会议/期刊名与年份",
    "tags": "领域标签，可多选，用 ; 分隔：" + "，".join(f"{k} {v}" for k, v in pl.DOMAINS.items()),
    "subclass": "子类，多个用 ； 分隔；用 README 里已有的子类名，归不进去就在 review_points 里提出",
    "task": "任务：系统在做什么",
    "criteria": "满足的纳入标准，用 ； 分隔：" + "、".join(pl.CRITERIA) + "（三条都不满足的是 R0 边界案例）",
    "object": "改进对象：被改的是什么（提示、技能库、脚手架代码、权重……）",
    "R": "自指深度：R0 仅外部产物 / R1 提示、记忆、技能库 / R2 脚手架与自身代码 / R3 权重与训练流程 / R4 改进“改进过程”本身",
    "r_evidence": "自指深度的依据：原文章节或语句",
    "feedback": "反馈来源，用 ； 分隔：" + "、".join(pl.FEEDBACK[:-1]),
    "loop": "闭环程度：" + "、".join(pl.ENUMS["loop"][:-1]),
    "accumulation": "累积方式：" + "、".join(pl.ENUMS["accumulation"][:-1]),
    "rounds": "改进轮数：原文报告的轮数或代数，没有报告就写 未报告",
    "cost": "验证成本（只记原文报告的，不推断）：" + "、".join(pl.ENUMS["cost"]),
    "reversibility": "失败可逆性：" + "、".join(pl.ENUMS["reversibility"][:-1]),
    "claim": "自称程度：作者自己怎么称呼这项工作（是否自称 RSI / 自我改进）",
    "evidence": "证据强度：" + "、".join(pl.ENUMS["evidence"][:-1]),
    "result": "主要结果：一句话，带数字",
    "limits": "失败与局限：原文承认的，或你读出来的",
    "reading": "阅读深度：" + "、".join(pl.READING_NEW) + "（仅摘要的论文不能被确认）",
    "confidence": "你对这份标注的置信度：" + "、".join(pl.ENUMS["confidence"]),
    "notes": "备注：其他字段的原文出处等",
}


def issue_fields(number):
    out = subprocess.run(["gh", "issue", "view", str(number), "--json", "title,body"],
                         capture_output=True, text=True, check=True).stdout
    body = json.loads(out)["body"] or ""
    sections = {}
    for m in re.finditer(r"^### (.+?)\n+(.*?)(?=^### |\Z)", body, re.S | re.M):
        value = m.group(2).strip()
        sections[m.group(1).strip()] = "" if value == "_No response_" else value
    tags = ";".join(re.findall(r"- \[[xX]\] ([0-4])", sections.get("领域标签", "")))
    return {"title": sections.get("论文标题", ""), "url": sections.get("链接", ""), "tags": tags}


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
            print("读不到 Issue（需要 gh CLI）。先生成空模板，标题和链接请手工填写。", file=sys.stderr)

    path = pl.PENDING_DIR / f"issue-{args.issue}.yml"
    if path.exists():
        sys.exit(f"{path.relative_to(pl.ROOT)} 已存在")
    _, rows = pl.load_tsv()
    dup = next((r["id"] for r in rows if known["url"] and r["url"] == known["url"]), None)
    if dup:
        sys.exit(f"这篇论文已收录为 {dup}")

    lines = [f"# Issue #{args.issue} 推荐论文的标注。一行一个字段，写成 `字段: 取值`；取值里不能有竖线。",
             "# 拿不准的写 待核对（验证成本写 未报告），并在 review_points 里给出选项和你的建议。",
             "# 不要添加编号和确认信息：确认人在 Issue 页面评论 /confirm 后由流程写入。", ""]
    for key in pl.PENDING_KEYS[:-1]:
        value = known.get(key, "").replace("\n", " ").replace("|", "/")
        lines += [f"# {HELP[key]}", f"{key}: {value}", ""]
    lines += ["# 需要确认人核对的点。每条给出：具体问题、选项（各自的依据）、你的建议和理由、去原文哪里看。",
              "# 这段会原样显示在 Issue 页面上，可以写多行 Markdown，每行前面保留两个空格。",
              "review_points: |",
              "  1. ", ""]
    pl.PENDING_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"已创建 {path.relative_to(pl.ROOT)}")


if __name__ == "__main__":
    main()
