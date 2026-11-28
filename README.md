# Awesome RSI Applications

A list of papers that apply recursive self-improvement (RSI), maintained alongside a survey we are writing.

Most existing RSI surveys and lists are organized by mechanism: whether the model or the scaffold is changed, and how closed the loop is. This list is organized by **application domain** and asks one question: **how far has RSI progressed in each application domain?**

It currently holds 14 paper(s). Every paper is annotated with the same set of fields, so papers can be compared side by side.

> **Human confirmation: 14 / 14.** A paper is only formally included once a human developer has checked its annotation against the paper. The "Confirmed" column names the confirmer; entries marked "pending" are preliminary annotations drafted by an AI assistant and should not be cited as they are.
>
> **Status: in progress.** 14 paper(s) were read in full or in part, 0 only as far as the abstract or an excerpt, and 0 could not be accessed; the "Reading" column gives the details. "unclear" means there was not enough information to decide. Check the original paper before citing.

## Contents

- [How far each domain has progressed](#how-far-each-domain-has-progressed)
- [How to read this list](#how-to-read-this-list)
- [Papers](#papers)
- [Data and contributions](#data-and-contributions)
- [Related resources](#related-resources)

## How far each domain has progressed

Papers in each domain by self-reference depth (R0–R4). A paper can carry several domain tags, so the row totals add up to more than the number of papers.

| Domain | R0 | R1 | R2 | R3 | R4 | Unclear | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0. AI R&D itself | 3 | 0 | 7 | 2 | 2 | 0 | 14 |
| 1. Engineering | 1 | 0 | 7 | 0 | 1 | 0 | 9 |
| 2. Natural sciences | 2 | 0 | 2 | 1 | 1 | 0 | 6 |
| 3. Physical and embodied systems | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 4. Social sciences | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Observations from the annotations so far (tentative, given the sample size):

- **AI R&D itself is the most mature domain.** Work that modifies its own scaffold and code (R2) is concentrated here, and R4 also appears mainly here.
- **Scientific work with real-world experimental feedback stops at R0 or R1.** Systems that use wet-lab experiments or real instruments as feedback modify memory and skill libraries; none modifies its scaffold or weights.
- **Weight-level improvement on real robots almost always involves people.** Work that trains weights on physical robots is mostly human-in-the-loop or semi-automatic, and is evaluated only on the training tasks.
- **Social sciences are the thinnest domain, with finance a possible exception.** Finance has fast, quantitative feedback such as backtests and real profit and loss.

## How to read this list

**Inclusion criteria.** A work must have a closed loop (generate, evaluate, generate again), self-reference (the thing being improved includes part of the system itself), and accumulation (improvements are kept and feed into later improvement). Work that has only a closed loop and changes only external artifacts is included as a borderline case and marked R0.

**Domain tags** can be combined. Domain 0 is general-purpose AI improving itself; domains 1–4 are assigned by the application domain of the experimental tasks.

**Self-reference depth R0–R4**: what is being improved.

| Level | What is improved |
| --- | --- |
| R0 | External artifacts only |
| R1 | Prompts, memory, skill and tool libraries |
| R2 | Scaffold and own code |
| R3 | Weights and training pipeline |
| R4 | The improvement process itself |

R0 marks a borderline case. R0–R4 is not the same scale as the L0–L5 levels of the physical-RSI survey ([arXiv:2610.18842](https://arxiv.org/abs/2610.18842)): the two measure different things and do not map one-to-one.

**Other columns**

| Column | Values |
| --- | --- |
| Feedback | The signal inside the loop that decides whether a change is kept: formal verification; automated evaluation (tests, benchmarks, backtests); simulation; real-world experiment (wet lab, physical robots, online A/B tests); human review; learned judge (a different model scores); self-evaluation (the model being improved scores itself). Several may apply |
| Loop | human-in-the-loop; semi-automatic; fully automatic |
| Evidence | in-task (improvement shown only on the tasks used for training or tuning); cross-task (shown on held-out or other tasks); cross-task, independently verified |
| Claim | RSI; self-improvement (including self-evolving); not claimed |
| Reading | full text; partial text; abstract only (older rows may say abstract, excerpt or unread) |
| Confirmed | pending; or the confirmer's GitHub login |

## Papers

### 0. AI R&D itself (14)

General-purpose AI that improves itself, not tied to one application domain. May be tagged together with domains 1–4.

| ID | Paper | First released | Subfield | What is improved | R | Feedback | Loop | Evidence | Claim | Reading | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P001 | [STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) (also 2) | 2022-03 | Data and weight self-adaptation; Mathematics | Model weights, fine-tuned on self-generated rationales; each iteration retrains from the original model | R3 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P010 | [Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation](https://arxiv.org/abs/2310.02304) (also 1) | 2023-10 | Agent self-improvement; Algorithm discovery | The improver scaffolding program itself (its own Python code that queries the LM to generate and select improvements) | R4 (limited to the scaffold/code level; the underlying LM is unchanged) | automated evaluation | fully automatic | cross-task | RSI (states it is not full RSI because the LM is unchanged) | partial text | ✅ @JasonDZS |
| P002 | [ADAS: Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435) (also 2) | 2024-08 | Agent self-improvement; Mathematics | External artifacts only: the meta agent designs new agents in code (their forward function); the meta agent itself does not change | R0 | automated evaluation | fully automatic | cross-task | not claimed (Section 6 lists self-improvement of the meta agent as future work) | partial text | ✅ @JasonDZS |
| P003 | [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](https://arxiv.org/abs/2408.06292) | 2024-08 | Automated ML research | External artifacts only: research ideas, experiment code edited from the template, and papers; the LLM pipeline itself does not change | R0 | automated evaluation; self-evaluation | fully automatic | in-task | not claimed (Section 9 lists self-improving and self-referential use as future work) | partial text | ✅ @JasonDZS |
| P004 | [Gödel Agent: A Self-Referential Agent Framework for Recursively Self-Improvement](https://arxiv.org/abs/2410.04444) (also 2) | 2024-10 | Agent self-improvement; Mathematics | The agent's own running code, changed by monkey patching: the task policy (solver) and, in the case study, the self-improvement logic itself | R4 (changes to the improvement logic shown only qualitatively, in the Game of 24 case study) | automated evaluation | fully automatic | in-task | RSI | full text | ✅ @JasonDZS |
| P005 | [A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228) (also 1, 2) | 2025-04 | Agent self-improvement; Software engineering; Mathematics | The agent's own Python codebase: tools, sub-agents, prompts and orchestration logic. The best agent so far is also the meta-agent that makes the next change, so the edited code takes part in later improvement steps | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P006 | [Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954) (also 1) | 2025-05 | Agent self-improvement; Software engineering | The coding agent's own Python repository: its tools (e.g. line-range file viewing, string-replacement editing), workflow (several patch attempts, ranking by another FM, history-aware retries, non-empty patch validation) and context handling (auto-summarize at the context limit). The modified agent then carries out the next self-modification; the archive and parent selection stay fixed | R2 | automated evaluation | fully automatic | cross-task | self-improvement | full text | ✅ @JasonDZS |
| P007 | [Self-Adapting Language Models](https://arxiv.org/abs/2506.10943) | 2025-06 | Data and weight self-adaptation | The model's own weights. The outer ReST-EM loop finetunes the model to generate better self-edits (synthetic finetuning data, and on ARC the choice of augmentations, learning rate, epochs and loss tokens); each self-edit is applied to the same model as an SFT update (LoRA or full finetuning) | R3 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P014 | [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) (also 1, 2) | 2025-06 | Automated ML research; Algorithm discovery; Mathematics; Chip design and systems optimization | External artifacts: the user-specified target program for each task (tensor-decomposition algorithms, math constructions, scheduling/kernel heuristics, Verilog, compiler IR); optionally co-evolved meta-prompts. The AlphaEvolve pipeline (prompt sampler, LLM ensemble, evaluators, database) itself is fixed | R0 | automated evaluation; simulation | fully automatic | in-task | not claimed | full text | ✅ @JasonDZS |
| P008 | [Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine](https://arxiv.org/abs/2510.21614) (also 1) | 2025-10 | Agent self-improvement; Software engineering | The coding agent's own code repository (starting from the DGM initial agent, a single LLM loop with bash and file-editing tools): its tools and its attempt and test workflow in coding_agent.py. The selected agent produces its own child, so the modified code also carries out later self-modifications; the HGM tree-search policy (CMP estimate, Thompson sampling, expansion rule, final selection) stays fixed | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P009 | [Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing](https://arxiv.org/abs/2602.04837) (also 1) | 2026-02 | Agent self-improvement; Software engineering | The coding agent's own framework code: its tools, workflow and prompting strategies | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P011 | [The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators](https://arxiv.org/abs/2606.26294) (also 1, 2, 3) | 2026-06 | Agent self-improvement; Software engineering; Mathematics; Automated reward and curriculum design; Automated ML research | The agents' and evaluators' own code (coder, code reviewer, paper writer/reviewer, prover/grader, reward designer) plus the utility itself — the learned evaluator is co-evolved and replaced across epochs; the meta-agent code is also editable, while the scoring/orchestration harness is fixed | R2 | automated evaluation; learned judge; simulation | fully automatic | in-task | RSI | partial text | ✅ @JasonDZS |
| P012 | [Recursive self-improvement of AI research agents](https://arxiv.org/abs/2609.26457) (also 1) | 2026-09 | Agent self-improvement; Cross-subfield | The AI research agent's own harness code: its search/selection policy (bandit over drafting strategies with forking), context-management and failure-memory mechanisms, and robustness safeguards; each accepted rewrite becomes the incumbent edited next | R2 | automated evaluation | fully automatic | cross-task | RSI | full text | ✅ @JasonDZS |
| P013 | [Evaluation-Free Recursive Self-Improvement for Coding Agents](https://arxiv.org/abs/2611.21056) (also 1) | 2026-11 | Agent self-improvement; Software engineering | The agent's own scaffold source-code repository: tools, prompts, utilities and control logic | R2 | formal verification; self-evaluation | fully automatic | cross-task | RSI | full text | ✅ @JasonDZS |

### 1. Engineering (9)

Software engineering, algorithm discovery, chip design and systems optimization. The loop runs only through digital environments.

| ID | Paper | First released | Subfield | What is improved | R | Feedback | Loop | Evidence | Claim | Reading | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P010 | [Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation](https://arxiv.org/abs/2310.02304) (also 0) | 2023-10 | Agent self-improvement; Algorithm discovery | The improver scaffolding program itself (its own Python code that queries the LM to generate and select improvements) | R4 (limited to the scaffold/code level; the underlying LM is unchanged) | automated evaluation | fully automatic | cross-task | RSI (states it is not full RSI because the LM is unchanged) | partial text | ✅ @JasonDZS |
| P005 | [A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228) (also 0, 2) | 2025-04 | Agent self-improvement; Software engineering; Mathematics | The agent's own Python codebase: tools, sub-agents, prompts and orchestration logic. The best agent so far is also the meta-agent that makes the next change, so the edited code takes part in later improvement steps | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P006 | [Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954) (also 0) | 2025-05 | Agent self-improvement; Software engineering | The coding agent's own Python repository: its tools (e.g. line-range file viewing, string-replacement editing), workflow (several patch attempts, ranking by another FM, history-aware retries, non-empty patch validation) and context handling (auto-summarize at the context limit). The modified agent then carries out the next self-modification; the archive and parent selection stay fixed | R2 | automated evaluation | fully automatic | cross-task | self-improvement | full text | ✅ @JasonDZS |
| P014 | [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) (also 0, 2) | 2025-06 | Automated ML research; Algorithm discovery; Mathematics; Chip design and systems optimization | External artifacts: the user-specified target program for each task (tensor-decomposition algorithms, math constructions, scheduling/kernel heuristics, Verilog, compiler IR); optionally co-evolved meta-prompts. The AlphaEvolve pipeline (prompt sampler, LLM ensemble, evaluators, database) itself is fixed | R0 | automated evaluation; simulation | fully automatic | in-task | not claimed | full text | ✅ @JasonDZS |
| P008 | [Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine](https://arxiv.org/abs/2510.21614) (also 0) | 2025-10 | Agent self-improvement; Software engineering | The coding agent's own code repository (starting from the DGM initial agent, a single LLM loop with bash and file-editing tools): its tools and its attempt and test workflow in coding_agent.py. The selected agent produces its own child, so the modified code also carries out later self-modifications; the HGM tree-search policy (CMP estimate, Thompson sampling, expansion rule, final selection) stays fixed | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P009 | [Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing](https://arxiv.org/abs/2602.04837) (also 0) | 2026-02 | Agent self-improvement; Software engineering | The coding agent's own framework code: its tools, workflow and prompting strategies | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P011 | [The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators](https://arxiv.org/abs/2606.26294) (also 0, 2, 3) | 2026-06 | Agent self-improvement; Software engineering; Mathematics; Automated reward and curriculum design; Automated ML research | The agents' and evaluators' own code (coder, code reviewer, paper writer/reviewer, prover/grader, reward designer) plus the utility itself — the learned evaluator is co-evolved and replaced across epochs; the meta-agent code is also editable, while the scoring/orchestration harness is fixed | R2 | automated evaluation; learned judge; simulation | fully automatic | in-task | RSI | partial text | ✅ @JasonDZS |
| P012 | [Recursive self-improvement of AI research agents](https://arxiv.org/abs/2609.26457) (also 0) | 2026-09 | Agent self-improvement; Cross-subfield | The AI research agent's own harness code: its search/selection policy (bandit over drafting strategies with forking), context-management and failure-memory mechanisms, and robustness safeguards; each accepted rewrite becomes the incumbent edited next | R2 | automated evaluation | fully automatic | cross-task | RSI | full text | ✅ @JasonDZS |
| P013 | [Evaluation-Free Recursive Self-Improvement for Coding Agents](https://arxiv.org/abs/2611.21056) (also 0) | 2026-11 | Agent self-improvement; Software engineering | The agent's own scaffold source-code repository: tools, prompts, utilities and control logic | R2 | formal verification; self-evaluation | fully automatic | cross-task | RSI | full text | ✅ @JasonDZS |

### 2. Natural sciences (6)

Mathematics, chemistry and materials, biology and medicine, physics and earth sciences.

| ID | Paper | First released | Subfield | What is improved | R | Feedback | Loop | Evidence | Claim | Reading | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P001 | [STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) (also 0) | 2022-03 | Data and weight self-adaptation; Mathematics | Model weights, fine-tuned on self-generated rationales; each iteration retrains from the original model | R3 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P002 | [ADAS: Automated Design of Agentic Systems](https://arxiv.org/abs/2408.08435) (also 0) | 2024-08 | Agent self-improvement; Mathematics | External artifacts only: the meta agent designs new agents in code (their forward function); the meta agent itself does not change | R0 | automated evaluation | fully automatic | cross-task | not claimed (Section 6 lists self-improvement of the meta agent as future work) | partial text | ✅ @JasonDZS |
| P004 | [Gödel Agent: A Self-Referential Agent Framework for Recursively Self-Improvement](https://arxiv.org/abs/2410.04444) (also 0) | 2024-10 | Agent self-improvement; Mathematics | The agent's own running code, changed by monkey patching: the task policy (solver) and, in the case study, the self-improvement logic itself | R4 (changes to the improvement logic shown only qualitatively, in the Game of 24 case study) | automated evaluation | fully automatic | in-task | RSI | full text | ✅ @JasonDZS |
| P005 | [A Self-Improving Coding Agent](https://arxiv.org/abs/2504.15228) (also 0, 1) | 2025-04 | Agent self-improvement; Software engineering; Mathematics | The agent's own Python codebase: tools, sub-agents, prompts and orchestration logic. The best agent so far is also the meta-agent that makes the next change, so the edited code takes part in later improvement steps | R2 | automated evaluation | fully automatic | in-task | self-improvement | full text | ✅ @JasonDZS |
| P014 | [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131) (also 0, 1) | 2025-06 | Automated ML research; Algorithm discovery; Mathematics; Chip design and systems optimization | External artifacts: the user-specified target program for each task (tensor-decomposition algorithms, math constructions, scheduling/kernel heuristics, Verilog, compiler IR); optionally co-evolved meta-prompts. The AlphaEvolve pipeline (prompt sampler, LLM ensemble, evaluators, database) itself is fixed | R0 | automated evaluation; simulation | fully automatic | in-task | not claimed | full text | ✅ @JasonDZS |
| P011 | [The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators](https://arxiv.org/abs/2606.26294) (also 0, 1, 3) | 2026-06 | Agent self-improvement; Software engineering; Mathematics; Automated reward and curriculum design; Automated ML research | The agents' and evaluators' own code (coder, code reviewer, paper writer/reviewer, prover/grader, reward designer) plus the utility itself — the learned evaluator is co-evolved and replaced across epochs; the meta-agent code is also editable, while the scoring/orchestration harness is fixed | R2 | automated evaluation; learned judge; simulation | fully automatic | in-task | RSI | partial text | ✅ @JasonDZS |

### 3. Physical and embodied systems (1)

Robot skill acquisition, automated reward and curriculum design, open-ended embodied learning. The loop runs through the physical world or a simulation of it.

| ID | Paper | First released | Subfield | What is improved | R | Feedback | Loop | Evidence | Claim | Reading | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P011 | [The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators](https://arxiv.org/abs/2606.26294) (also 0, 1, 2) | 2026-06 | Agent self-improvement; Software engineering; Mathematics; Automated reward and curriculum design; Automated ML research | The agents' and evaluators' own code (coder, code reviewer, paper writer/reviewer, prover/grader, reward designer) plus the utility itself — the learned evaluator is co-evolved and replaced across epochs; the meta-agent code is also editable, while the scoring/orchestration harness is fixed | R2 | automated evaluation; learned judge; simulation | fully automatic | in-task | RSI | partial text | ✅ @JasonDZS |

### 4. Social sciences (0)

Economics and finance, social simulation, forecasting, deployed service agents, policy and education, law.

| ID | Paper | First released | Subfield | What is improved | R | Feedback | Loop | Evidence | Claim | Reading | Confirmed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Data and contributions

**Confirmation rule.** Every paper in the list must be confirmed by a human developer who has read the paper, checked each field of the annotation, and then commented `/confirm` on the paper's issue. The workflow records the confirmer and the date; nobody edits them by hand. AI assistants may draft annotations but cannot confirm them, and automation accounts cannot be confirmers.

The step-by-step guide is in [CONTRIBUTING.md](CONTRIBUTING.md). In short:

1. **Recommend.** Anyone opens an issue with the ["Recommend a paper" form](../../issues/new?template=add-paper.yml); only the title, link and a reason are needed.
2. **Branch.** Whoever takes the paper creates the branch `paper/issue-<number>` and runs `python3 scripts/new_paper.py <number>` to create the annotation file `data/pending/issue-<number>.yml`.
3. **Read and annotate.** Read the paper, fill in the fields, write anything uncertain as points to check (with options and a recommendation), commit, and open a pull request.
4. **Review on the issue page.** The annotation is shown on the issue page automatically. The confirmer checks it against the paper; if they disagree, they comment what should change, and the rendering is replaced when the annotator updates the branch.
5. **Confirm.** The confirmer comments `/confirm` on the issue. The workflow checks that the commenter is a human on the [confirmer list](.github/confirmers.txt), assigns an ID, writes the paper to [`data/papers.tsv`](data/papers.tsv) with the confirmer and date, updates the README, and closes the pull request and the issue.

The data file is `|`-separated, one paper per row, 28 columns. Besides the columns shown above it records publication status, task, inclusion criteria, evidence for the depth, accumulation, improvement rounds, verification cost, failure reversibility, main result, failures and limitations, confidence, and notes. **Signal reliability** is not a separate column: it is the weakest of the paper's feedback sources, from strongest to weakest formal verification, automated evaluation, real-world experiment, simulation, human review and learned judge, self-evaluation. Do not edit the tables in this README; they are generated by a script.

**Reading with an AI assistant.** The repository includes a `paper-reading` skill ([`.agents/skills/paper-reading/`](.agents/skills/paper-reading/SKILL.md)) in the open Agent Skills format, usable from Codex, Claude Code and other tools that support it. It turns a paper into a draft annotation with sources from the paper and a list of points for a person to check. It only produces drafts awaiting confirmation and does not replace human confirmation.

**LaTeX tables and figures** for the survey are generated from the data by [`figure/build_figures.py`](figure/README.md).

**Issues that carry the annotation.** If the issue already contains a complete annotation in its Annotation field, the `paper-intake` workflow creates the branch and the pull request for you; see [CONTRIBUTING.md](CONTRIBUTING.md).

To correct an existing annotation, open an issue and cite the evidence (the section or sentence in the paper).

## Related resources

- [awesome-rsi](https://github.com/lobehub/awesome-rsi): an RSI list organized by mechanism, with sections on benchmarks and safety.
- [Awesome-Self-Evolving-Scientific-Agents](https://github.com/REAL-Lab-NU/Awesome-Self-Evolving-Scientific-Agents): self-evolving agents for scientific discovery.
- [Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops](https://arxiv.org/abs/2607.07663): a survey organized by what is improved and how closed the loop is.
- [Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104): a survey organized by foundation-model updates versus scaffold updates.
- [Who Improves the Robot? Toward Physical Recursive Self-Improvement](https://arxiv.org/abs/2610.18842): a survey dedicated to physical and embodied RSI.
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046): a survey of self-evolving agents.
