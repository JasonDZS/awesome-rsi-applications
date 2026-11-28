# Annotation rules

Rules for each field. The borderline cases come from experience annotating the papers already in the list.

Values are written exactly as listed here (lower case, except subfield names and R levels). Multi-valued fields are separated by `; `.

## Inclusion criteria (criteria)

- **closed loop**: the system generates candidates, they are evaluated, and the evaluation drives the next round.
- **self-reference**: the thing being improved includes part of the system itself, not only external artifacts.
- **accumulation**: improvements are kept and take part in later rounds of improvement.

Work that has only a closed loop is a borderline case and gets `R0`. A paper that meets none of the three does not belong in the list; tell the user and explain why.

## Domain tags (tags)

One or more, written like `0;2`.

- **0 AI R&D itself**: general-purpose AI that improves itself, not tied to one application domain. Applies when the task itself is AI research and development, or when what changes is the agent's own scaffold, code or improvement process. Work that only trains a policy for one application domain (such as a robot policy) is not tagged 0.
- **1 Engineering**: software engineering, algorithm discovery, chip design and systems optimization. The loop runs only through digital environments.
- **2 Natural sciences**: mathematics, chemistry and materials, biology and medicine, physics and earth sciences.
- **3 Physical and embodied systems**: the loop runs through the physical world or a simulation of it. Embodied agents in game environments also belong here.
- **4 Social sciences**: economics and finance, social simulation, forecasting, deployed service agents, policy and education, law.

Domain 0 and domains 1–4 are not mutually exclusive. A self-improving coding agent is tagged `0;1`. Tag 1–4 by the domain of the experimental tasks; a paper with experiments in three domains gets three tags.

## Subfield (subclass)

Use these names; several are separated by `; `.

| Domain | Subfields |
| --- | --- |
| 0 | Agent self-improvement; Data and weight self-adaptation; Automated ML research |
| 1 | Software engineering; Algorithm discovery; Chip design and systems optimization |
| 2 | Mathematics; Chemistry and materials; Biology and medicine; Physics and earth sciences |
| 3 | Robot skill acquisition; Automated reward and curriculum design; Open-ended embodied learning |
| 4 | Economics and finance; Social simulation; Forecasting; Deployed service agents; Policy and education; Law |

`Cross-subfield` is used when the experiments span many subfields and no single one describes the paper.

## Self-reference depth (R)

Use the highest level the paper **actually achieves**.

| Level | What is improved |
| --- | --- |
| R0 | External artifacts only |
| R1 | Prompts, memory, skill and tool libraries |
| R2 | Scaffold and own code |
| R3 | Weights and training pipeline |
| R4 | The improvement process itself |

R4 requires all three of the following:

1. **What is changed is part of how improvements are made**, not part of how tasks are done: what proposes a change (diagnosis, mutation prompts, mutation operators), the procedure that implements it, or how candidates are evaluated and selected (utility, parent selection, archive policy, data generation or training algorithm). Test: if the change only affects how the system performs tasks, it is R2; if it changes which improvements are proposed in later rounds or how they are chosen, it is R4.
2. **It is actually changed in the reported experiments.** A component that "can in principle be modified" but stays fixed does not count.
3. **The changed improvement process is then used to improve the system itself** in later rounds, not only an inner component that is separate from it.

If the paper also shows that the change matters (an ablation of the meta-level change, or a measure of improvement quality across rounds), write plain `R4`. If the only evidence is a qualitative case study or example, write `R4 (shown only qualitatively)` or give the specific case, e.g. `R4 (changes to the improvement logic shown only qualitatively, in the Game of 24 case study)`.

Borderline cases:

- **A meta-agent designs other agents and does not change itself** → R0. The designed agents are external artifacts.
- **An optimizer iteratively optimizes prompts, code or molecules, and the optimizer itself does not change** → R0.
- **A growing tool, skill or experience library** → R1. These are things the agent itself calls later, not external artifacts.
- **What changes is the code that organizes memory, not just what is written into memory** → R2.
- **Weight updates are only proposed, never executed** → not R3; use the level actually achieved.
- **Each round retrains from the original model, but on data produced by the previous round's model** → still R3; say so in the notes.
- **The mutation prompts themselves are also evolved (the part that generates improvements is improved)** → R4, stating which level it is limited to, e.g. `R4 (limited to the prompt level)`.
- **An outer loop changes the inner loop's search code and does not change itself** → R2, not R4.
- **The agent that makes the improvement is the same code as the agent being improved, but the reported changes are task tools or workflow** (e.g. better editing tools that also make later self-modification easier) → R2, not R4.
- **The model changes how its own next round of training data or rewards is produced, and that procedure is then used to train it** → R4, e.g. `R4 (limited to the training-pipeline level)`, but only if the model trained this way is the one that keeps being improved. If a fixed outer step makes the persistent update and the learned procedure only updates temporary copies that are scored and discarded (e.g. SEAL), it is R3. Only retraining on new data is R3.
- **The system games its evaluator** (e.g. deletes what the checker relies on) → not R4; record it under failures and limitations.
- When unsure, write e.g. `R2 or R4 (unclear)` and put the evidence for both readings in the points to check.

## Feedback source (feedback)

The signal **inside the loop** that decides whether a change is kept or discarded. A judge used only in the final evaluation does not count. One or more, separated by `; `.

- **formal verification**: proof checkers, type checking, and similar.
- **automated evaluation**: tests, benchmark scores, backtests, comparison with ground-truth answers.
- **simulation**: physics simulators, world models, social simulations.
- **real-world experiment**: wet-lab experiments, physical robots, online A/B tests, outcomes in real markets or real events.
- **human review**: human scoring, human corrections, expert review.
- **learned judge**: scoring by a **different** model.
- **self-evaluation**: scoring by **the model being improved**, including self-consistency voting, pseudo-labels, and the model acting as its own judge.

The difference between a learned judge and self-evaluation is whether the judge is the model being improved.

Signal reliability is not annotated separately. It is derived from the weakest of the chosen sources, from strongest to weakest: formal verification, automated evaluation, real-world experiment, simulation, human review and learned judge, self-evaluation.

## Loop automation (loop)

- **fully automatic**: no person takes part while the loop runs. People only build and start it.
- **semi-automatic**: people step in at fixed points, such as providing one demonstration, approving before deployment, resetting the environment, or taking over after a failure.
- **human-in-the-loop**: people continuously give feedback or corrections and are part of the feedback signal.

## Accumulation (accumulation)

`single round`; `multi-generation single lineage`; `open-ended population or archive`.

## Verification cost (cost)

The time needed to obtain one trustworthy evaluation: `seconds to minutes`; `hours`; `days to weeks`; `months or longer, or requires humans`. If the paper does not report it, write `not reported`; do not infer it.

## Failure reversibility (reversibility)

- **fully reversible**: e.g. rolling back code.
- **retryable at a cost**: e.g. reagents, samples, robot wear, small losses of real money.
- **irreversible**: e.g. damaged hardware, real effects on people or society.

## Authors' claim (claim)

Judge by the wording of the title and abstract: `RSI` (explicitly uses "recursive self-improvement"); `self-improvement` (self-improving, self-evolving, and similar); `not claimed`.

When the paper explicitly disclaims something, record it in parentheses, e.g. `self-improvement (states it is not recursive)`. Such statements are useful for the survey.

## Evidence strength (evidence)

- **in-task**: improvement shown only on the tasks used for training or tuning. Held-out test sets of the same benchmark and held-out time periods of the same task count as in-task.
- **cross-task**: improvement shown on other tasks, benchmarks or domains that were not used for tuning.
- **cross-task, independently verified**: as above, and confirmed by a third party or an independent evaluation. Evaluations run by the authors themselves are not independent.

## Reading depth (reading)

New annotations use `full text`, `partial text` or `abstract only`. Older data may also contain `abstract`, `excerpt` or `unread`. Only rows with `full text` or `partial text` can be confirmed.

## Other fields

- **venue**: `arXiv preprint`, or the venue and year.
- **result**: one sentence with the key numbers before and after improvement and the benchmark used.
- **limits**: failures and limitations reported by the paper itself, not your own criticism.
- **r_evidence**: the source for the self-reference depth: section number and quotation.
- **notes**: sources for the other fields, feedback details, open questions, points where people intervene.
- **confidence**: how sure you are of the whole annotation: `high`, `medium` or `low`. If you read only the abstract, do not go above `low`.
