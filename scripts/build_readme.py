#!/usr/bin/env python3
"""Generate README.md from data/papers.tsv.

Usage: python3 scripts/build_readme.py
The paper list in README.md is generated; edit data/papers.tsv, not the README.
"""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "papers.tsv"
OUT = ROOT / "README.md"

DOMAINS = {
    "0": ("AI 研发自身", "通用的 AI 优化自身，不限于某个应用领域。可与 1–4 类并列标注。"),
    "1": ("工程科学", "软件工程、算法发现、芯片设计与系统优化。闭环只经过数字环境。"),
    "2": ("自然科学", "数学、化学与材料、生物与医药、物理与地球科学。"),
    "3": ("物理与具身", "机器人技能习得、奖励与课程的自动设计、开放式具身学习。"),
    "4": ("社会科学", "经济与金融、社会仿真、预测、已部署的服务型智能体、政策与教育、法律。"),
}
LEVELS = ["R0", "R1", "R2", "R3", "R4"]
UNKNOWN = "待核对"


def load():
    with DATA.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="|"))
    for r in rows:
        r["tag_list"] = [t for t in r["tags"].split(";") if t]
        m = re.match(r"R[0-4]", r["R"])
        r["level"] = m.group(0) if m else UNKNOWN
    return rows


def cell(text):
    return text if text else "—"


def confirm(r):
    if r['status'] == '已确认':
        return f"✅ @{r['confirmed_by']}"
    return '待确认'


def paper_link(r):
    return f"[{r['title']}]({r['url']})" if r["url"] else r["title"]


def matrix(rows):
    lines = ["| 领域 | " + " | ".join(LEVELS) + f" | {UNKNOWN} | 合计 |",
             "| --- | " + " | ".join(["---"] * (len(LEVELS) + 2)) + " |"]
    for d, (name, _) in DOMAINS.items():
        c = Counter(r["level"] for r in rows if d in r["tag_list"])
        total = sum(c.values())
        nums = " | ".join(str(c.get(lv, 0)) for lv in LEVELS)
        lines.append(f"| {d}. {name} | {nums} | {c.get(UNKNOWN, 0)} | {total} |")
    return "\n".join(lines)


def domain_table(rows, d):
    sel = sorted((r for r in rows if d in r["tag_list"]), key=lambda r: (r["date"], r["id"]))
    lines = ["| 编号 | 论文 | 首发 | 子类 | 改进对象 | R | 反馈来源 | 闭环 | 证据 | 自称 | 阅读 | 确认 |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sel:
        other = [t for t in r["tag_list"] if t != d]
        also = f"（另见 {'、'.join(other)}）" if other else ""
        lines.append(
            f"| {r['id']} | {paper_link(r)}{also} | {r['date']} | {r['subclass']} | "
            f"{cell(r['object'])} | {cell(r['R'])} | {cell(r['feedback'])} | "
            f"{cell(r['loop'])} | {cell(r['evidence'])} | {cell(r['claim'])} | {cell(r['reading'])} | {confirm(r)} |"
        )
    return len(sel), "\n".join(lines)


def main():
    rows = load()
    n = len(rows)
    reading = Counter(r["reading"] for r in rows)
    confirmed = sum(r["status"] == "已确认" for r in rows)
    parts = []
    parts.append(f"""# Awesome RSI Applications

递归自我改进（Recursive Self-Improvement，RSI）的应用论文清单，配套我们正在撰写的综述。

已有的 RSI 综述和清单大多按机制组织（改的是模型还是脚手架、闭环到什么程度）。这份清单按**应用领域**组织，回答一个问题：**RSI 在各应用领域走到了哪一步**。

目前收录 {n} 篇，每篇都按同一组字段标注，可以横向比较。

> **人工确认：{confirmed} / {n}。** 每篇论文都必须由一位真实的开发人员对照原文确认后才算正式收录；“确认”一列标明了确认人，标为“待确认”的条目是 AI 助手起草的初步标注，请勿直接引用。
>
> **状态：进行中。** {reading.get('全文', 0)} 篇读了原文，{reading.get('摘要', 0) + reading.get('片段', 0)} 篇只读到摘要或片段，{reading.get('未读', 0)} 篇未能读取；“阅读”一列标明了每篇的情况，“待核对”表示信息不足以判断。引用前请核对原文。

## 目录

- [各领域走到了哪一步](#各领域走到了哪一步)
- [如何阅读这份清单](#如何阅读这份清单)
- [论文清单](#论文清单)
- [数据与更新方式](#数据与更新方式)
- [相关资源](#相关资源)

## 各领域走到了哪一步

各领域论文在自指深度（R0–R4）上的分布。一篇论文可以有多个领域标签，所以各行合计之和大于论文总数。

{matrix(rows)}

基于当前标注的几点观察（样本有限，属于候选发现）：

- **AI 研发自身最成熟。** 改自身脚手架和代码（R2）的工作集中在这一类，R4 也主要出现在这里。
- **真实实验闭环的科学工作停在 R0 或 R1。** 用湿实验或真实仪器作反馈的工作，改的是记忆和技能库，没有一篇改脚手架或权重。
- **真机上的权重改进几乎都离不开人。** 在真实机器人上训练权重的工作多为人在回路或半自动，且只在训练任务上评测。
- **社会科学最薄，但金融可能是例外。** 金融有回测和真实盈亏这类快而量化的反馈。

## 如何阅读这份清单

**纳入标准。** 一项工作需满足：闭环（生成、评估、再生成）、自指（被改进的对象包含系统自身的一部分）、累积（改进被保留并参与后续改进）。只满足闭环、只改外部产物的工作作为边界案例收录，标为 R0。

**领域标签**可多选。第 0 类表示通用的 AI 优化自身；1–4 类按实验任务所在的应用领域标注。

**自指深度 R0–R4**：改的是什么。

| 等级 | 含义 |
| --- | --- |
| R0 | 仅外部产物（边界案例） |
| R1 | 提示、记忆、技能库 |
| R2 | 脚手架与自身代码 |
| R3 | 权重与训练流程 |
| R4 | 改进“改进过程”本身 |

R0–R4 与物理 RSI 综述（[arXiv:2610.18842](https://arxiv.org/abs/2610.18842)）的 L0–L5 不是同一套分级，两者的轴不同，不能一一对应。

**其他列**

| 列 | 取值 |
| --- | --- |
| 反馈来源 | 形式验证；自动评测（测试、基准、回测）；仿真；真实实验（湿实验、真机、线上）；人类评审；学习型评判（另一个模型打分）；自评（被改进的模型给自己打分）。可多选 |
| 闭环 | 人在回路；半自动；全自动 |
| 证据 | 任务内（只在训练或调优所用的任务上见效）；跨任务（在留出或其他任务上见效）；跨任务且独立验证 |
| 自称 | RSI；自我改进（含自演化）；未自称 |
| 阅读 | 全文；摘要；片段；未读 |
| 确认 | 待确认；或确认人的 GitHub 用户名 |

## 论文清单
""")
    for d, (name, desc) in DOMAINS.items():
        count, table = domain_table(rows, d)
        parts.append(f"### {d}. {name}（{count} 篇）\n\n{desc}\n\n{table}\n")
    parts.append("""## 数据与更新方式

**确认规则。** 每篇进入清单的论文都必须由一位真实的开发人员确认：本人读过原文，核对过各列标注，并在数据里记下自己的 GitHub 用户名和日期。AI 助手可以起草标注，但不能确认；自动化账号不能作为确认人。

流程：

1. **提交**：任何人用 [“添加论文”表单](../../issues/new?template=add-paper.yml)提交。只有标题、链接、首发年月、领域标签、阅读深度五项必填。
2. **入库为待确认**：维护者运行 `gh issue view <编号> --json body -q .body | python3 scripts/issue_to_row.py --append`，把表单内容转成 [`data/papers.tsv`](data/papers.tsv) 里的一行，`status` 为 `待确认`。
3. **人工确认**：一位开发人员对照原文核对后，把该行的 `status` 改为 `已确认`，填上 `confirmed_by`（GitHub 用户名）和 `confirmed_at`（YYYY-MM-DD）。
4. **合并**：运行 `python3 scripts/check_data.py` 和 `python3 scripts/build_readme.py`，提交 pull request。数据文件的改动需要代码所有者审核，CI 会检查数据格式、确认信息是否完整，以及 README 是否与数据一致。

数据文件以 `|` 分隔，一行一篇，共 28 列。除上表展示的列以外，还有发表状态、任务、纳入标准、自指深度的依据、累积方式、改进轮数、验证成本、失败可逆性、主要结果、失败与局限、置信度和备注；早期收录的论文这些列多数还是空的。**信号可靠性**不单独标注，按反馈来源中最弱的一档得出，由强到弱为：形式验证、自动评测、真实实验、仿真、人类评审与学习型评判、自评。不要直接改 README 里的表格，它由脚本生成。

- 纠正已有标注请提 issue 或 pull request，并附上判断依据（原文中的章节或语句）。

## 相关资源

- [awesome-rsi](https://github.com/lobehub/awesome-rsi)：按机制组织的 RSI 清单，含基准与安全分区。
- [Awesome-Self-Evolving-Scientific-Agents](https://github.com/REAL-Lab-NU/Awesome-Self-Evolving-Scientific-Agents)：科学发现方向的自演化智能体清单。
- [Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops](https://arxiv.org/abs/2607.07663)：按“改进什么 × 闭环程度”组织的综述。
- [Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104)：按基础模型更新与脚手架更新组织的综述。
- [Who Improves the Robot? Toward Physical Recursive Self-Improvement](https://arxiv.org/abs/2610.18842)：物理与具身方向的专门综述。
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)：自演化智能体综述。
""")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({n} papers)")


if __name__ == "__main__":
    main()
