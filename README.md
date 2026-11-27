# Awesome RSI Applications

递归自我改进（Recursive Self-Improvement，RSI）的应用论文清单，配套我们正在撰写的综述。

已有的 RSI 综述和清单大多按机制组织（改的是模型还是脚手架、闭环到什么程度）。这份清单按**应用领域**组织，回答一个问题：**RSI 在各应用领域走到了哪一步**。

目前收录 115 篇，每篇都按同一组字段标注，可以横向比较。

> **人工确认：0 / 115。** 每篇论文都必须由一位真实的开发人员对照原文确认后才算正式收录；“确认”一列标明了确认人，标为“待确认”的条目是 AI 助手起草的初步标注，请勿直接引用。
>
> **状态：进行中。** 64 篇读了原文，49 篇只读到摘要或片段，2 篇未能读取；“阅读”一列标明了每篇的情况，“待核对”表示信息不足以判断。引用前请核对原文。

## 目录

- [各领域走到了哪一步](#各领域走到了哪一步)
- [如何阅读这份清单](#如何阅读这份清单)
- [论文清单](#论文清单)
- [数据与更新方式](#数据与更新方式)
- [相关资源](#相关资源)

## 各领域走到了哪一步

各领域论文在自指深度（R0–R4）上的分布。一篇论文可以有多个领域标签，所以各行合计之和大于论文总数。

| 领域 | R0 | R1 | R2 | R3 | R4 | 待核对 | 合计 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0. AI 研发自身 | 5 | 7 | 17 | 14 | 5 | 0 | 48 |
| 1. 工程科学 | 4 | 2 | 10 | 1 | 3 | 1 | 21 |
| 2. 自然科学 | 8 | 20 | 4 | 4 | 1 | 3 | 40 |
| 3. 物理与具身 | 2 | 7 | 2 | 13 | 1 | 1 | 26 |
| 4. 社会科学 | 2 | 7 | 0 | 3 | 0 | 1 | 13 |

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

### 0. AI 研发自身（48 篇）

通用的 AI 优化自身，不限于某个应用领域。可与 1–4 类并列标注。

| 编号 | 论文 | 首发 | 子类 | 改进对象 | R | 反馈来源 | 闭环 | 证据 | 自称 | 阅读 | 确认 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P041 | [STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) | 2022-03 | 数据与权重的自适应 | 用自生成的推理微调权重，每轮从原始模型重训 | R3 | 自动评测 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P042 | [Large Language Models Can Self-Improve](https://arxiv.org/abs/2210.11610) | 2022-10 | 数据与权重的自适应 | 用自生成的推理数据微调权重，仅一轮 | R3 | 自评 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P043 | [Reflexion](https://arxiv.org/abs/2303.11366) | 2023-03 | 智能体自我改进 | 言语反思记忆 | R1 | 自动评测；自评 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P044 | [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144) | 2023-08 | 智能体自我改进 | 经验洞见列表与成功轨迹池 | R1 | 自动评测 | 全自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P045 | [OPRO: Large Language Models as Optimizers](https://arxiv.org/abs/2309.03409) | 2023-09 | 智能体自我改进 | 仅外部产物（提示、问题的解），优化器自身不变 | R0 | 自动评测 | 全自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P046 | [Promptbreeder](https://arxiv.org/abs/2309.16797) | 2023-09 | 智能体自我改进 | 任务提示，以及生成它们的变异提示 | R4（限于提示层） | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P001 | [STOP: Self-Taught Optimizer](https://arxiv.org/abs/2310.02304)（另见 1） | 2023-10 | 智能体自我改进；算法发现 | 改进器程序改进自身 | R4 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P047 | [DSPy](https://arxiv.org/abs/2310.03714) | 2023-10 | 智能体自我改进 | 流水线模块的提示与示例，可选微调权重 | R1 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P048 | [Self-Play Fine-Tuning](https://arxiv.org/abs/2401.01335) | 2024-01 | 数据与权重的自适应 | 自博弈迭代微调权重 | R3 | 自评 | 全自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P049 | [Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020) | 2024-01 | 数据与权重的自适应 | 权重，含自身的评判能力 | R3 | 自评 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P050 | [TextGrad](https://arxiv.org/abs/2406.07496)（另见 2） | 2024-06 | 智能体自我改进；化学与材料 | 仅外部产物（提示、代码、分子、放疗计划） | R0 | 自动评测；学习型评判 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P051 | [Meta-Rewarding Language Models](https://arxiv.org/abs/2407.19594) | 2024-07 | 数据与权重的自适应 | 权重，同时改进执行与评判 | R3 | 自评 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P002 | [ADAS: Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435) | 2024-08 | 智能体自我改进 | 元智能体用代码设计新智能体，元智能体自身不变 | R0 | 自动评测 | — | — | 未自称 | 摘要 | 待确认 |
| P003 | [The AI Scientist](https://arxiv.org/abs/2408.06292) | 2024-08 | 自动化 ML 研究 | 产出研究想法、实验和论文，不改自身 | R0 | 自动评测；学习型评判 | — | — | 未自称 | 摘要 | 待确认 |
| P004 | [Gödel Agent](https://arxiv.org/abs/2410.04444) | 2024-10 | 智能体自我改进 | 运行时改写自身逻辑 | R2，或 R4 待核对 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P074 | [rStar-Math](https://arxiv.org/abs/2501.04519)（另见 2） | 2025-01 | 数据与权重的自适应；数学 | 策略模型与偏好模型的权重 | R3 | 自动评测 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P005 | [SICA: A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228)（另见 1） | 2025-04 | 智能体自我改进；软件工程 | 编程智能体的自身代码 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P059 | [The AI Scientist-v2](https://arxiv.org/abs/2504.08066) | 2025-04 | 自动化 ML 研究 | 产出假设、实验和论文，不改自身 | R0 | 学习型评判；人类评审 | 全自动 | 任务内 | 未自称 | 摘要 | 待确认 |
| P006 | [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954)（另见 1） | 2025-05 | 智能体自我改进；软件工程 | 编程智能体的自身代码，档案库演化 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P007 | [SEAL: Self-Adapting Language Models](https://arxiv.org/abs/2506.10943) | 2025-06 | 数据与权重的自适应 | 模型生成自己的微调数据和更新指令，改权重 | R3 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P052 | [R-Zero: Self-Evolving Reasoning LLM from Zero Data](https://arxiv.org/abs/2508.05004) | 2025-08 | 数据与权重的自适应 | 出题者与解题者的权重 | R3 | 自评 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P008 | [Huxley-Gödel Machine](https://arxiv.org/abs/2510.21614)（另见 1） | 2025-10 | 智能体自我改进；软件工程 | 编程智能体的自身代码，按后代分支效用选择 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P053 | [Agentic Context Engineering](https://arxiv.org/abs/2510.04618) | 2025-10 | 智能体自我改进 | 不断演化的上下文手册 | R1 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P054 | [Alita-G](https://arxiv.org/abs/2510.23601) | 2025-10 | 智能体自我改进 | 可复用的工具库 | R1 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P055 | [Agent0](https://arxiv.org/abs/2511.16043) | 2025-11 | 数据与权重的自适应 | 课程智能体与执行智能体的权重 | R3 | 自评 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P056 | [MemEvolve: Meta-Evolution of Agent Memory Systems](https://arxiv.org/abs/2512.18746) | 2025-12 | 智能体自我改进 | 自身的记忆架构代码与经验库 | R2 | 自动评测 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P009 | [Group-Evolving Agents](https://arxiv.org/abs/2602.04837)（另见 1） | 2026-02 | 智能体自我改进；软件工程 | 以智能体群组为演化单位，组内共享经验 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P057 | [Hyperagents](https://arxiv.org/abs/2603.19461)（另见 1、3） | 2026-03 | 智能体自我改进；软件工程；奖励与课程的自动设计 | 任务智能体和修改它的元智能体，含自我修改过程 | R4 | 自动评测；学习型评判；仿真 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P058 | [Bilevel Autoresearch](https://arxiv.org/abs/2603.23420) | 2026-03 | 自动化 ML 研究 | 内层回路的搜索代码，外层不改自身 | R2 | 自动评测 | 全自动 | 任务内 | 自我改进（文中说明未展示 RSI） | 全文 | 待确认 |
| P060 | [SIA: Self Improving AI with Harness & Weight Updates](https://arxiv.org/abs/2605.27276)（另见 1、2、4） | 2026-05 | 智能体自我改进；系统优化；生物与医药；法律 | 脚手架与 LoRA 权重 | R3 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P010 | [The Red Queen Gödel Machine](https://arxiv.org/abs/2606.26294)（另见 1、2） | 2026-06 | 智能体自我改进；软件工程；数学 | 智能体与评估器共同演化 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P033 | [ENPIRE](https://arxiv.org/abs/2606.19980)（另见 3） | 2026-06 | 自动化 ML 研究；机器人技能习得 | 真机自动研究回路，改策略和训练代码 | R3 | 真实实验 | — | — | 自我改进 | 摘要 | 待确认 |
| P061 | [MLEvolve](https://arxiv.org/abs/2606.06473) | 2026-06 | 自动化 ML 研究 | 候选 ML 代码、搜索日程与记忆，不改自身脚手架 | R1 | 自动评测；学习型评判 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P062 | [Self-Harness](https://arxiv.org/abs/2606.09498)（另见 1） | 2026-06 | 智能体自我改进；软件工程 | 自身脚手架（提示、工具、运行策略） | R2 | 自动评测 | 全自动 | 跨任务 | 自我改进（文中说明不是递归） | 全文 | 待确认 |
| P022 | [Self-Modifying Lean Proof Agents](https://arxiv.org/abs/2607.17352)（另见 2） | 2026-07 | 智能体自我改进；数学 | 证明智能体自身，基准随之共同演化 | R2 | 形式验证 | — | — | 自我改进 | 摘要 | 待确认 |
| P063 | [Frontis-MA1](https://arxiv.org/abs/2607.28568) | 2026-07 | 自动化 ML 研究 | 算子策略的权重，搜索脚手架不变 | R3 | 自动评测 | 全自动 | 跨任务 | 未自称（文中说明尚未实现 RSI） | 全文 | 待确认 |
| P064 | [Mendel Gödel Machine](https://arxiv.org/abs/2608.07645)（另见 1） | 2026-08 | 智能体自我改进；软件工程 | 智能体自身源码与脚手架 | R2 | 自动评测 | 全自动 | 跨任务 | RSI | 全文 | 待确认 |
| P065 | [HELIX: Model-Harness Co-evolution](https://arxiv.org/abs/2608.13951)（另见 1） | 2026-08 | 智能体自我改进；软件工程 | 脚手架配方；权重更新只提出未执行 | R2 | 自动评测 | 全自动 | 任务内 | RSI（作为目标） | 全文 | 待确认 |
| P066 | [Meta^n: Recursive Self-Improvement through Emergent Depth](https://arxiv.org/abs/2608.24735) | 2026-08 | 智能体自我改进 | 叠加在求解器之上的策略层与辅助代码 | R4 | 待核对 | 待核对 | 待核对 | RSI | 摘要 | 待确认 |
| P011 | [AIDE²: Recursive Self-Improvement of AI Research Agents](https://arxiv.org/abs/2609.26457) | 2026-09 | 自动化 ML 研究 | 研究智能体自身的代码 | R2，或 R4 待核对 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P023 | [ScienceBuddy](https://arxiv.org/abs/2609.17523)（另见 2） | 2026-09 | 智能体自我改进；生物与医药 | 嵌套的脚手架改进与模型训练 | R3 | 自动评测；人类评审 | — | — | RSI | 摘要 | 待确认 |
| P067 | [Self Improvement via Fast Tree-search](https://arxiv.org/abs/2609.19526)（另见 1） | 2026-09 | 智能体自我改进；软件工程 | 自身编程智能体的脚手架代码 | R2 | 自动评测；学习型评判 | 全自动 | 跨任务 | RSI | 全文 | 待确认 |
| P068 | [ReSAIL](https://arxiv.org/abs/2609.39306)（另见 3） | 2026-09 | 数据与权重的自适应；开放式具身学习 | 迭代自蒸馏更新权重 | R3 | 自动评测 | 全自动 | 跨任务 | RSI（称为通向 RSI 的路径） | 全文 | 待确认 |
| P017 | [Organon](https://arxiv.org/abs/2610.33046)（另见 1、2） | 2026-10 | 算法发现；芯片设计与系统优化；数学 | 搜索策略、记忆、诊断工具，以及自身的适应过程 | R4 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P024 | [SwarmRSI](https://arxiv.org/abs/2610.20431)（另见 2） | 2026-10 | 智能体自我改进；跨子类 | 可继承的研究状态：假设、程序、证据 | R1 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P026 | [MolRSI](https://arxiv.org/abs/2610.39714)（另见 2） | 2026-10 | 智能体自我改进；化学与材料；生物与医药 | 工作流、模型架构和跨任务记忆 | R2 | 仿真 | — | — | RSI | 摘要 | 待确认 |
| P012 | [Evaluation-Free Recursive Self-Improvement for Coding Agents](https://arxiv.org/abs/2611.21056)（另见 1） | 2026-11 | 智能体自我改进；软件工程 | 编程智能体的自身代码，不做候选任务评测 | R2 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P027 | [SciMARS](https://arxiv.org/abs/2611.12552)（另见 2） | 2026-11 | 智能体自我改进；跨子类 | 任务内的脚手架自适应 | R2 | 仿真 | — | — | RSI | 摘要 | 待确认 |

### 1. 工程科学（21 篇）

软件工程、算法发现、芯片设计与系统优化。闭环只经过数字环境。

| 编号 | 论文 | 首发 | 子类 | 改进对象 | R | 反馈来源 | 闭环 | 证据 | 自称 | 阅读 | 确认 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P001 | [STOP: Self-Taught Optimizer](https://arxiv.org/abs/2310.02304)（另见 0） | 2023-10 | 智能体自我改进；算法发现 | 改进器程序改进自身 | R4 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P013 | [FunSearch: Mathematical Discoveries from Program Search with LLMs](https://www.nature.com/articles/s41586-023-06924-6)（另见 2） | 2023-12 | 算法发现；数学 | 演化外部程序 | R0 | 自动评测 | — | — | 未自称 | 摘要 | 待确认 |
| P005 | [SICA: A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228)（另见 0） | 2025-04 | 智能体自我改进；软件工程 | 编程智能体的自身代码 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P006 | [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954)（另见 0） | 2025-05 | 智能体自我改进；软件工程 | 编程智能体的自身代码，档案库演化 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P014 | [AlphaEvolve](https://arxiv.org/abs/2506.13131)（另见 2） | 2025-06 | 算法发现；芯片设计与系统优化；数学 | 演化外部算法代码 | R0 | 自动评测 | — | — | 未自称 | 摘要 | 待确认 |
| P008 | [Huxley-Gödel Machine](https://arxiv.org/abs/2510.21614)（另见 0） | 2025-10 | 智能体自我改进；软件工程 | 编程智能体的自身代码，按后代分支效用选择 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P009 | [Group-Evolving Agents](https://arxiv.org/abs/2602.04837)（另见 0） | 2026-02 | 智能体自我改进；软件工程 | 以智能体群组为演化单位，组内共享经验 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P057 | [Hyperagents](https://arxiv.org/abs/2603.19461)（另见 0、3） | 2026-03 | 智能体自我改进；软件工程；奖励与课程的自动设计 | 任务智能体和修改它的元智能体，含自我修改过程 | R4 | 自动评测；学习型评判；仿真 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P060 | [SIA: Self Improving AI with Harness & Weight Updates](https://arxiv.org/abs/2605.27276)（另见 0、2、4） | 2026-05 | 智能体自我改进；系统优化；生物与医药；法律 | 脚手架与 LoRA 权重 | R3 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P069 | [Learning from Repair Experience](https://arxiv.org/abs/2605.30105) | 2026-05 | 软件工程 | 漏洞修复经验库 | R1 | 自动评测；学习型评判 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P071 | [GRAFT-ATHENA](https://arxiv.org/abs/2605.11117)（另见 2） | 2026-05 | 算法发现；物理与地球科学 | 共享知识库（动作图、记忆） | R1 | 仿真；学习型评判 | 半自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P010 | [The Red Queen Gödel Machine](https://arxiv.org/abs/2606.26294)（另见 0、2） | 2026-06 | 智能体自我改进；软件工程；数学 | 智能体与评估器共同演化 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P062 | [Self-Harness](https://arxiv.org/abs/2606.09498)（另见 0） | 2026-06 | 智能体自我改进；软件工程 | 自身脚手架（提示、工具、运行策略） | R2 | 自动评测 | 全自动 | 跨任务 | 自我改进（文中说明不是递归） | 全文 | 待确认 |
| P015 | [CoEvoP&R](https://arxiv.org/abs/2607.17398) | 2026-07 | 芯片设计与系统优化 | 用布线反馈共同演化布局目标 | R0 | 自动评测 | — | — | 未自称 | 摘要 | 待确认 |
| P064 | [Mendel Gödel Machine](https://arxiv.org/abs/2608.07645)（另见 0） | 2026-08 | 智能体自我改进；软件工程 | 智能体自身源码与脚手架 | R2 | 自动评测 | 全自动 | 跨任务 | RSI | 全文 | 待确认 |
| P065 | [HELIX: Model-Harness Co-evolution](https://arxiv.org/abs/2608.13951)（另见 0） | 2026-08 | 智能体自我改进；软件工程 | 脚手架配方；权重更新只提出未执行 | R2 | 自动评测 | 全自动 | 任务内 | RSI（作为目标） | 全文 | 待确认 |
| P016 | [Self-Evolving Algorithm-Design Agents](https://arxiv.org/abs/2609.38757) | 2026-09 | 算法发现 | 待核对 | 待核对 | 待核对 | — | — | 自我改进 | 摘要 | 待确认 |
| P067 | [Self Improvement via Fast Tree-search](https://arxiv.org/abs/2609.19526)（另见 0） | 2026-09 | 智能体自我改进；软件工程 | 自身编程智能体的脚手架代码 | R2 | 自动评测；学习型评判 | 全自动 | 跨任务 | RSI | 全文 | 待确认 |
| P070 | [PEAR: AutoResearch for Industrial Search Systems](https://arxiv.org/abs/2609.35031) | 2026-09 | 芯片设计与系统优化 | 电商搜索系统的策略参数（外部产物） | R0 | 学习型评判；真实实验 | 半自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P017 | [Organon](https://arxiv.org/abs/2610.33046)（另见 0、2） | 2026-10 | 算法发现；芯片设计与系统优化；数学 | 搜索策略、记忆、诊断工具，以及自身的适应过程 | R4 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P012 | [Evaluation-Free Recursive Self-Improvement for Coding Agents](https://arxiv.org/abs/2611.21056)（另见 0） | 2026-11 | 智能体自我改进；软件工程 | 编程智能体的自身代码，不做候选任务评测 | R2 | 自动评测 | — | — | RSI | 摘要 | 待确认 |

### 2. 自然科学（40 篇）

数学、化学与材料、生物与医药、物理与地球科学。

| 编号 | 论文 | 首发 | 子类 | 改进对象 | R | 反馈来源 | 闭环 | 证据 | 自称 | 阅读 | 确认 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P013 | [FunSearch: Mathematical Discoveries from Program Search with LLMs](https://www.nature.com/articles/s41586-023-06924-6)（另见 1） | 2023-12 | 算法发现；数学 | 演化外部程序 | R0 | 自动评测 | — | — | 未自称 | 摘要 | 待确认 |
| P050 | [TextGrad](https://arxiv.org/abs/2406.07496)（另见 0） | 2024-06 | 智能体自我改进；化学与材料 | 仅外部产物（提示、代码、分子、放疗计划） | R0 | 自动评测；学习型评判 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P072 | [DREAM: Autonomous Self-Evolving Research on Biomedical Data](https://arxiv.org/abs/2407.13637) | 2024-07 | 生物与医药 | 生成的研究问题与分析代码（外部产物） | R0 | 学习型评判 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P073 | [ChemAgent: Self-updating Library](https://arxiv.org/abs/2501.06590) | 2025-01 | 化学与材料 | 外部记忆库（规划与执行记忆） | R1 | 自动评测；学习型评判 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P074 | [rStar-Math](https://arxiv.org/abs/2501.04519)（另见 0） | 2025-01 | 数据与权重的自适应；数学 | 策略模型与偏好模型的权重 | R3 | 自动评测 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P075 | [Accelerating Scientific Discovery with Co-Scientist](https://arxiv.org/abs/2502.18864) | 2025-02 | 生物与医药 | 智能体提示与上下文记忆 | R1 | 学习型评判 | 全自动 | 任务内 | RSI | 全文 | 待确认 |
| P076 | [Robin](https://arxiv.org/abs/2505.13400) | 2025-05 | 生物与医药 | 仅外部产物（假设、实验方案） | R0 | 真实实验；学习型评判；人类评审 | 半自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P014 | [AlphaEvolve](https://arxiv.org/abs/2506.13131)（另见 1） | 2025-06 | 算法发现；芯片设计与系统优化；数学 | 演化外部算法代码 | R0 | 自动评测 | — | — | 未自称 | 摘要 | 待确认 |
| P077 | [OriGene: A Self-Evolving Virtual Disease Biologist](https://doi.org/10.1101/2025.06.03.657658) | 2025-06 | 生物与医药 | 未能读取 | 待核对 | 待核对 | 待核对 | 待核对 | 待核对 | 未读 | 待确认 |
| P018 | [STELLA](https://arxiv.org/abs/2507.02004) | 2025-07 | 生物与医药 | 推理模板库和自动扩充的工具库 | R1 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P078 | [Operating Advanced Scientific Instruments with AI Agents that Learn on the Job](https://arxiv.org/abs/2509.00098) | 2025-08 | 化学与材料 | 系统提示与人工纠正记忆 | R1 | 人类评审；真实实验 | 人在回路 | 任务内 | 未自称 | 全文 | 待确认 |
| P079 | [Mephisto](https://arxiv.org/abs/2510.08354) | 2025-10 | 物理与地球科学 | 知识库与记忆 | R1 | 自动评测；学习型评判 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P080 | [PhysMaster](https://arxiv.org/abs/2512.19799) | 2025-12 | 物理与地球科学 | 候选解与跨任务经验记忆 | R1 | 学习型评判 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P081 | [CASCADE: Cumulative Agentic Skill Creation](https://arxiv.org/abs/2512.23880) | 2025-12 | 化学与材料 | 提示、记忆与可执行技能 | R1 | 自动评测；人类评审 | 半自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P082 | [S1-NexusAgent](https://arxiv.org/abs/2602.01550) | 2026-02 | 跨子类 | 经验与技能库 | R1 | 学习型评判 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P083 | [Using a GPT-5-driven Autonomous Lab to Optimize Cell-Free Protein Synthesis](https://doi.org/10.64898/2026.02.05.703998) | 2026-02 | 生物与医药 | 未能读取 | 待核对 | 待核对 | 待核对 | 待核对 | 待核对 | 未读 | 待确认 |
| P084 | [From Experiments to Expertise](https://arxiv.org/abs/2603.13191) | 2026-03 | 物理与地球科学 | 持久知识库 | R1 | 仿真；自评 | 半自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P085 | [Self-Evolving AI Agents for Protein Discovery and Directed Evolution](https://arxiv.org/abs/2603.27303) | 2026-03 | 生物与医药 | 摘要未说明 | 待核对 | 待核对 | 待核对 | 待核对 | 自我改进 | 摘要 | 待确认 |
| P019 | [Agentic LLM Reasoning in a Self-Driving Lab for Lithium Halide Spinel Conductors](https://arxiv.org/abs/2604.11957) | 2026-04 | 化学与材料 | 待核对 | R0 | 真实实验 | — | — | 未自称 | 摘要 | 待确认 |
| P086 | [SKILLFOUNDRY](https://arxiv.org/abs/2604.03964) | 2026-04 | 跨子类 | 技能库与领域知识树 | R1 | 自动评测；学习型评判 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P087 | [End-to-End Autonomous Scientific Discovery on a Real Optical Platform](https://arxiv.org/abs/2604.27092) | 2026-04 | 物理与地球科学 | 主要是外部产物，另有跨研究复用的经验记录 | R0，或 R1 待核对 | 真实实验；仿真；学习型评判 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P020 | [LLM-AutoSciLab](https://arxiv.org/abs/2605.24043) | 2026-05 | 化学与材料 | 主动实验的闭环科学发现 | R0 | 待核对 | — | — | 未自称 | 摘要 | 待确认 |
| P021 | [ImProver 2](https://arxiv.org/abs/2605.22885) | 2026-05 | 数学 | 迭代自我改进的证明优化模型 | R3 | 形式验证 | — | — | 自我改进 | 摘要 | 待确认 |
| P060 | [SIA: Self Improving AI with Harness & Weight Updates](https://arxiv.org/abs/2605.27276)（另见 0、1、4） | 2026-05 | 智能体自我改进；系统优化；生物与医药；法律 | 脚手架与 LoRA 权重 | R3 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P071 | [GRAFT-ATHENA](https://arxiv.org/abs/2605.11117)（另见 1） | 2026-05 | 算法发现；物理与地球科学 | 共享知识库（动作图、记忆） | R1 | 仿真；学习型评判 | 半自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P088 | [DrugSAGE](https://arxiv.org/abs/2605.15461) | 2026-05 | 生物与医药 | 技能库与跨任务经验记忆 | R1 | 自动评测 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P010 | [The Red Queen Gödel Machine](https://arxiv.org/abs/2606.26294)（另见 0、1） | 2026-06 | 智能体自我改进；软件工程；数学 | 智能体与评估器共同演化 | R2 | 自动评测 | — | — | 自我改进 | 摘要 | 待确认 |
| P089 | [Autonomous Heterogeneous Catalyst Discovery with a Self-Evolving Multi-Agent Digital Twin](https://arxiv.org/abs/2606.05050) | 2026-06 | 化学与材料 | 案例库、知识库、技能库与检索策略 | R1 | 仿真 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P090 | [A Self-Evolving Agentic System for Biological Protocols](https://arxiv.org/abs/2606.31763) | 2026-06 | 生物与医药 | 技能库与多层记忆 | R1 | 真实实验；人类评审；自动评测 | 半自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P022 | [Self-Modifying Lean Proof Agents](https://arxiv.org/abs/2607.17352)（另见 0） | 2026-07 | 智能体自我改进；数学 | 证明智能体自身，基准随之共同演化 | R2 | 形式验证 | — | — | 自我改进 | 摘要 | 待确认 |
| P091 | [LabEvolver](https://arxiv.org/abs/2607.27690)（另见 3） | 2026-07 | 化学与材料；机器人技能习得 | 经验记忆与倾倒控制参数 | R1 | 真实实验；仿真 | 全自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P092 | [GeoForge](https://arxiv.org/abs/2608.10494) | 2026-08 | 物理与地球科学 | 非参数记忆（工作流图、经验、技能） | R1 | 自动评测；学习型评判 | 全自动 | 待核对 | 自我改进 | 全文 | 待确认 |
| P023 | [ScienceBuddy](https://arxiv.org/abs/2609.17523)（另见 0） | 2026-09 | 智能体自我改进；生物与医药 | 嵌套的脚手架改进与模型训练 | R3 | 自动评测；人类评审 | — | — | RSI | 摘要 | 待确认 |
| P093 | [ADMET-EvO](https://arxiv.org/abs/2609.10121) | 2026-09 | 生物与医药 | 研究策略与证据账本，不改自身代码 | R1 | 自动评测 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P094 | [Hypothesis-Driven Autonomous Materials Synthesis](https://arxiv.org/abs/2609.18598) | 2026-09 | 化学与材料 | 自然语言的“理解”文档与分析代码技能库 | R1 | 真实实验；学习型评判 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P017 | [Organon](https://arxiv.org/abs/2610.33046)（另见 0、1） | 2026-10 | 算法发现；芯片设计与系统优化；数学 | 搜索策略、记忆、诊断工具，以及自身的适应过程 | R4 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P024 | [SwarmRSI](https://arxiv.org/abs/2610.20431)（另见 0） | 2026-10 | 智能体自我改进；跨子类 | 可继承的研究状态：假设、程序、证据 | R1 | 自动评测 | — | — | RSI | 摘要 | 待确认 |
| P025 | [Semantic Representation for Agentic Self-Play in Automated Laboratories](https://arxiv.org/abs/2610.32755)（另见 3） | 2026-10 | 生物与医药；机器人技能习得 | 跨轮次累积的操作规则和观测模型 | R1 | 真实实验 | — | — | 待核对 | 摘要 | 待确认 |
| P026 | [MolRSI](https://arxiv.org/abs/2610.39714)（另见 0） | 2026-10 | 智能体自我改进；化学与材料；生物与医药 | 工作流、模型架构和跨任务记忆 | R2 | 仿真 | — | — | RSI | 摘要 | 待确认 |
| P027 | [SciMARS](https://arxiv.org/abs/2611.12552)（另见 0） | 2026-11 | 智能体自我改进；跨子类 | 任务内的脚手架自适应 | R2 | 仿真 | — | — | RSI | 摘要 | 待确认 |

### 3. 物理与具身（26 篇）

机器人技能习得、奖励与课程的自动设计、开放式具身学习。

| 编号 | 论文 | 首发 | 子类 | 改进对象 | R | 反馈来源 | 闭环 | 证据 | 自称 | 阅读 | 确认 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P096 | [Self-Improving Robots (MEDAL++)](https://proceedings.mlr.press/v229/sharma23b.html) | 2023 | 机器人技能习得 | 策略与奖励函数的权重 | R3 | 真实实验；仿真 | 半自动 | 任务内 | 自我改进 | 摘要 | 待确认 |
| P028 | [Voyager](https://arxiv.org/abs/2305.16291) | 2023-05 | 开放式具身学习 | 不断增长的技能库 | R1 | 仿真 | — | — | 未自称 | 摘要 | 待确认 |
| P095 | [RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation](https://arxiv.org/abs/2306.11706) | 2023-06 | 机器人技能习得 | 微调上一代通用模型并自生成下一轮训练数据 | R3 | 待核对 | 待核对 | 待核对 | 自我改进 | 片段 | 待确认 |
| P029 | Eureka: Human-Level Reward Design via Coding LLMs | 2023-10 | 奖励与课程的自动设计 | 用代码生成并迭代奖励函数 | R0 | 仿真 | — | — | 未自称 | 摘要 | 待确认 |
| P097 | [AutoRT](https://arxiv.org/abs/2401.12963) | 2024-01 | 机器人技能习得 | 仅外部产物（采集的机器人数据） | R0 | 真实实验；人类评审；学习型评判 | 半自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P098 | [HIL-SERL: Precise and Dexterous Robotic Manipulation via Human-in-the-Loop RL](https://arxiv.org/abs/2410.21845) | 2024-10 | 机器人技能习得 | 策略与 Q 函数的权重 | R3 | 真实实验；人类评审 | 人在回路 | 任务内 | 未自称 | 全文 | 待确认 |
| P099 | [ConRFT](https://arxiv.org/abs/2502.05450) | 2025-02 | 机器人技能习得 | VLA 动作头与评论家的权重 | R3 | 真实实验；人类评审 | 人在回路 | 任务内 | 未自称 | 全文 | 待确认 |
| P030 | [Self-Improving Embodied Foundation Models](https://arxiv.org/abs/2509.15155) | 2025-09 | 机器人技能习得 | 机器人群自主练习，改策略权重 | R3 | 真实实验；仿真 | — | — | 自我改进 | 摘要 | 待确认 |
| P100 | [π0.6*: A VLA That Learns from Experience](https://arxiv.org/abs/2511.14759) | 2025-11 | 机器人技能习得 | VLA 策略与价值函数的权重 | R3 | 真实实验；人类评审 | 人在回路 | 任务内 | 自我改进 | 全文 | 待确认 |
| P031 | [SIMA 2](https://arxiv.org/abs/2512.04797) | 2025-12 | 开放式具身学习 | 虚拟世界中自主生成经验并改进 | R3 | 仿真 | — | — | 自我改进 | 摘要 | 待确认 |
| P101 | [SOP: Scalable Online Post-Training for VLA Models](https://arxiv.org/abs/2601.03044) | 2026-01 | 机器人技能习得 | VLA 权重，机器人群在线后训练 | R3 | 真实实验；人类评审 | 人在回路 | 任务内 | 未自称 | 全文 | 待确认 |
| P032 | [RISE: Self-Improving Robot Policy with Compositional World Model](https://arxiv.org/abs/2602.11075) | 2026-02 | 机器人技能习得 | 在世界模型的想象轨迹里改进策略 | R3 | 仿真 | — | — | 自我改进 | 摘要 | 待确认 |
| P102 | [VLAW](https://arxiv.org/abs/2602.12063) | 2026-02 | 机器人技能习得 | VLA 策略、世界模型与奖励模型的权重 | R3 | 真实实验；学习型评判 | 半自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P057 | [Hyperagents](https://arxiv.org/abs/2603.19461)（另见 0、1） | 2026-03 | 智能体自我改进；软件工程；奖励与课程的自动设计 | 任务智能体和修改它的元智能体，含自我修改过程 | R4 | 自动评测；学习型评判；仿真 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P103 | [MineEvolve](https://arxiv.org/abs/2603.13131) | 2026-03 | 开放式具身学习 | 外部行为知识库（技能与补救措施） | R1 | 仿真 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P104 | [Learning While Deploying: Fleet-Scale RL](https://arxiv.org/abs/2605.00416) | 2026-05 | 机器人技能习得 | 机器人群共享的 VLA 策略权重 | R3 | 真实实验；人类评审 | 半自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P033 | [ENPIRE](https://arxiv.org/abs/2606.19980)（另见 0） | 2026-06 | 自动化 ML 研究；机器人技能习得 | 真机自动研究回路，改策略和训练代码 | R3 | 真实实验 | — | — | 自我改进 | 摘要 | 待确认 |
| P105 | [HARBOR](https://arxiv.org/abs/2606.08610) | 2026-06 | 奖励与课程的自动设计 | 奖励与任务代码（外部产物）和调参经验记忆 | R1 | 仿真；自动评测 | 半自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P034 | [ASPIRE](https://arxiv.org/abs/2607.00272) | 2026-07 | 机器人技能习得 | 验证后的代码修复存入技能库 | R1 | 待核对 | — | — | 自我改进 | 摘要 | 待确认 |
| P091 | [LabEvolver](https://arxiv.org/abs/2607.27690)（另见 2） | 2026-07 | 化学与材料；机器人技能习得 | 经验记忆与倾倒控制参数 | R1 | 真实实验；仿真 | 全自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P106 | [Zero2Skill](https://arxiv.org/abs/2607.14047) | 2026-07 | 机器人技能习得 | 来自操作员语言纠正的纠错记忆 | R1 | 学习型评判；人类评审 | 半自动 | 任务内 | 未自称 | 摘要 | 待确认 |
| P107 | [Self-Evolving Embodied Agents via Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026-08 | 机器人技能习得 | 文本技能与上下文构建脚手架，模型权重冻结 | R2 | 仿真；学习型评判 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P068 | [ReSAIL](https://arxiv.org/abs/2609.39306)（另见 0） | 2026-09 | 数据与权重的自适应；开放式具身学习 | 迭代自蒸馏更新权重 | R3 | 自动评测 | 全自动 | 跨任务 | RSI（称为通向 RSI 的路径） | 全文 | 待确认 |
| P108 | [RoboFoundry](https://arxiv.org/abs/2609.32862) | 2026-09 | 机器人技能习得 | 自身的支撑系统（记忆规则、技能代码、提示），权重冻结 | R2 | 自动评测；真实实验；学习型评判 | 全自动 | 跨任务 | 自我改进 | 全文 | 待确认 |
| P109 | [EmbodiRSI](https://arxiv.org/abs/2609.38905) | 2026-09 | 机器人技能习得 | 机器人操作策略；系统自身是否改变未说明 | 待核对 | 仿真；真实实验 | 待核对 | 任务内 | RSI | 摘要 | 待确认 |
| P025 | [Semantic Representation for Agentic Self-Play in Automated Laboratories](https://arxiv.org/abs/2610.32755)（另见 2） | 2026-10 | 生物与医药；机器人技能习得 | 跨轮次累积的操作规则和观测模型 | R1 | 真实实验 | — | — | 待核对 | 摘要 | 待确认 |

### 4. 社会科学（13 篇）

经济与金融、社会仿真、预测、已部署的服务型智能体、政策与教育、法律。

| 编号 | 论文 | 首发 | 子类 | 改进对象 | R | 反馈来源 | 闭环 | 证据 | 自称 | 阅读 | 确认 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P110 | [SOTOPIA-π](https://arxiv.org/abs/2403.08715) | 2024-03 | 社会仿真 | 行为克隆与自强化微调权重；文中说明不能迭代改进 | R3 | 学习型评判 | 全自动 | 跨任务 | 未自称 | 全文 | 待确认 |
| P114 | [FinCon](https://arxiv.org/abs/2407.06567) | 2024-07 | 经济与金融 | 提示层面的投资信念（言语强化，不微调） | R1 | 待核对 | 待核对 | 待核对 | 待核对 | 摘要 | 待确认 |
| P115 | [AgentCourt](https://arxiv.org/abs/2408.08089) | 2024-08 | 法律 | 律师智能体的演化知识库 | R1 | 仿真；人类评审 | 待核对 | 待核对 | 自我改进 | 摘要 | 待确认 |
| P035 | [AI-Agent School](https://arxiv.org/abs/2510.11290) | 2025-10 | 政策与教育；社会仿真 | 智能体通过经验、反思、优化更新记忆库 | R1 | 仿真 | — | — | 自我改进 | 摘要 | 待确认 |
| P111 | [QuantEvolve](https://arxiv.org/abs/2510.18569) | 2025-10 | 经济与金融 | 仅外部产物（交易策略代码） | R0 | 自动评测；学习型评判 | 全自动 | 任务内 | 未自称 | 全文 | 待确认 |
| P060 | [SIA: Self Improving AI with Harness & Weight Updates](https://arxiv.org/abs/2605.27276)（另见 0、1、2） | 2026-05 | 智能体自我改进；系统优化；生物与医药；法律 | 脚手架与 LoRA 权重 | R3 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P112 | [AlphaMemo](https://arxiv.org/abs/2606.20625) | 2026-06 | 经济与金融 | 搜索过程记忆 | R1 | 自动评测 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P036 | [Eco3S](https://arxiv.org/abs/2607.26588) | 2026-07 | 经济与金融；社会仿真 | 迭代修改社会经济仿真的实验设计 | R0 | 仿真 | — | — | 未自称 | 摘要 | 待确认 |
| P113 | [ForeDreamer](https://arxiv.org/abs/2608.20920) | 2026-08 | 预测 | 经验库与生成的工具 | R1 | 自动评测；学习型评判 | 全自动 | 任务内 | 自我改进 | 全文 | 待确认 |
| P037 | [EvolveTrade](https://arxiv.org/abs/2609.17632) | 2026-09 | 经济与金融 | 从自身交易经验改写工具使用策略（系统提示） | R1 | 待核对 | — | — | 自我改进 | 摘要 | 待确认 |
| P038 | [EvoForesight](https://arxiv.org/abs/2610.29784) | 2026-10 | 预测 | 强化学习加技能积累 | R3 | 真实实验 | — | — | RSI | 摘要 | 待确认 |
| P039 | [Steward: Governed Self-Evolution for Autonomous Investing](https://arxiv.org/abs/2610.30557) | 2026-10 | 经济与金融 | 按实际结果评分后修改提示，核心规则不可自改 | R1 | 真实实验 | — | — | 自我改进 | 摘要 | 待确认 |
| P040 | [CARE: Grounded Recursive Self-Improvement for Production Customer-Service Agents](https://arxiv.org/abs/2611.02839) | 2026-11 | 已部署的服务型智能体 | 待核对 | 待核对 | 待核对 | — | — | RSI | 摘要 | 待确认 |

## 数据与更新方式

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
