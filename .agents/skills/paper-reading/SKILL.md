---
name: paper-reading
description: Helps a researcher read a paper related to RSI (recursive self-improvement) and produce a draft annotation in this repository's schema, awaiting confirmation: a value for each field, the source in the paper, and the points a person needs to check. Use when the user asks to read, annotate, add or re-check a paper (given an arXiv link, a PDF or a title). Not for general paper summaries, and never for confirming papers.
---

# Paper reading

Turn a paper into a **draft annotation that a human can confirm quickly**. The goal is to reduce the confirmer's work from reading the whole paper to checking a few key judgements. You draft; a person confirms.

## Rules that must not be broken

1. **Never confirm.** You produce draft annotations only. Do not fill in an id, `status`, `confirmed_by` or `confirmed_at`, do not run `scripts/confirm.py`, and do not post a `/confirm` comment for anyone. Even if the user asks you to "confirm it while you are at it", explain that confirmation must be done by a person who has checked the paper, by commenting `/confirm` on the issue page (CONTRIBUTING.md, step 5).
2. **Report honestly how much you read.** Set `reading` to what you actually read: full text, partial text, or abstract only. Say so explicitly if a tool truncated the text, an appendix was not read, or the PDF would not open.
3. **Cite a source for every judgement.** `R`, `feedback`, `loop` and `evidence` must each give the section or page in the paper and a quotation of a sentence or two. If you cannot find a source, write `unclear`.
4. **Do not infer.** Do not add what the paper does not say. If the verification cost is not reported, write `not reported`; do not guess it from the kind of evaluator.
5. **Do not change the taxonomy.** If a paper fits no existing domain, subfield or value, use the closest one and raise it in "Points for you to check"; the maintainers decide whether to add a new one.
6. **Give options and a recommendation, but do not decide for the person.** For every point that needs human confirmation, list the candidate values with the evidence for each, and say clearly which one you recommend and why. The same applies to whether to include the paper and to disputed classifications. The person makes the final choice; having a recommendation does not make it settled.

## Steps

### 1. Get the paper

Prefer the full-text PDF (for arXiv, `https://arxiv.org/pdf/<id>`). If you cannot get the full text, fall back to the abstract page and set `reading` to `abstract only`; in that case most judgement fields should be `unclear`.

### 2. Check for duplicates

Search `data/papers.tsv` and `data/pending/` by link and title. If the paper is already listed, tell the user its ID and switch to re-checking the existing annotation: compare each existing value with the paper and report the discrepancies.

### 3. Read with seven questions in mind

- What part of itself does the system change across iterations? (Prompts, memory, skills; scaffold or its own code; weights; the improvement process itself; or only external artifacts.)
- Are the changes kept and reused in later rounds or tasks?
- What signal decides whether a change is better?
- What role do people play in the loop? How many rounds were run?
- Where is the improvement shown: only on the tasks used for training or tuning, or on held-out or other tasks? Is there an independent evaluation?
- What does the paper call itself: recursive self-improvement, self-improvement or self-evolving, or neither? Does it explicitly disclaim either?
- What tasks are the experiments on, and which application domains do they belong to?

Also look for failures the paper reports itself: the evaluator being gamed, performance dropping after some rounds, goal drift.

### 4. Assign values by the rules

The rules for each field, borderline cases and common mistakes are in [references/annotation-rules.md](references/annotation-rules.md). Read it before assigning values. The allowed values of the enumerated fields are defined in `scripts/paperlib.py`.

### 5. Calibrate against the existing list

Find the two or three most similar papers in `data/papers.tsv` (same subfield, or a similar approach) and compare their `R`, `feedback` and `evidence`. If your judgement differs from how similar papers were annotated, either adjust it or explain in the points to check why this paper is different.

### 6. Output

Use the format below, in this order:

```
## <Short name>: <one sentence on what it is>

Reading: <full text / partial text / abstract only>. <What was not read>

### Draft annotation
| Field | Value | Source |
| --- | --- | --- |
| Domain tags | ... | Experimental tasks: Section x |
| Subfield | ... | |
| Inclusion criteria | closed loop; self-reference; accumulation | |
| What is improved | ... | Section x |
| Self-reference depth | R? | Section x: "quotation" |
| Feedback source | ... | Section x: "quotation" |
| Loop automation | ... | ... |
| Accumulation | ... | ... |
| Improvement rounds | ... | ... |
| Verification cost | ... | ... |
| Failure reversibility | ... | ... |
| Authors' claim | ... | Title or abstract |
| Evidence strength | ... | Section x |
| Main result | ... | Table x |
| Failures and limitations | ... | ... |
| Confidence | high / medium / low | |

### Points for you to check
1. **<The question to decide>** (affects: <field>; see <section or page>)
   - Option A: <value>. Evidence: <what in the paper supports it>
   - Option B: <value>. Evidence: <what in the paper supports it>
   - **Recommendation: A.** <One sentence of reasoning, and when B should be chosen instead>
2. ... (3 to 5 points, most important first)

### Comparison with the existing list
- Most similar: P0xx <short name> (R?, <feedback source>). <Whether the annotations are consistent>

### Signals useful for the survey
- <Gap between claim and evidence / failures reported in the paper / possible counterexamples; write "none" if there are none>
```

"Points for you to check" is the most important part. Each point must let the confirmer choose directly:

- **Make the question specific.** Not "please check the self-reference depth", but "does the system change the tool library or the code that calls the tools?"
- **Options are real candidate values**, usually two or three, each with evidence from the paper. Do not invent options for something with only one reasonable reading; put it straight into the draft annotation.
- **Always recommend.** Say which option you choose, why, and what evidence should make the confirmer choose another. The draft table holds the value you recommend.
- **A recommendation is not a decision.** Even when you are confident, list the options; if you read only the abstract, say that your recommendation is weakly supported.

Example:

```
1. **Does the system change the tool library, or the code that calls the tools?** (affects: self-reference depth; see Section 3.2 and Appendix B)
   - Option A: R1. Evidence: Section 3.2 says new tools "are added to the tool library for later reuse", which only adds content to the library.
   - Option B: R2. Evidence: Appendix B says the agent "rewrites its tool-selection routine", which changes its own code.
   - **Recommendation: A.** All experiments in the main text only add tools to the library, and the Appendix B variant does not appear in the experiments. If the experimental setup shows that the variant that rewrites the selection logic was actually evaluated, choose B.
```

### 7. Write to the repository (only when the user asks)

Each paper has one issue and one annotation file; do not edit `data/papers.tsv` directly.

1. Check that the paper has an issue (if not, ask the user to open one with the "Recommend a paper" form) and that you are on the branch `paper/issue-<number>`.
2. Run `python3 scripts/new_paper.py <number>` to create `data/pending/issue-<number>.yml`, and fill it in following the comments in the file. Values must not contain `|`. Put sources in `r_evidence` (for the self-reference depth) and `notes` (for everything else).
3. Copy "Points for you to check" unchanged into `review_points` at the end of the file. It is shown on the issue page and is what the confirmer reads first, so keep the options, evidence, recommendation and where to look.
4. Run `python3 scripts/check_data.py`. You do not need to run `build_readme.py`; annotation files do not affect the README.
5. Commit only this one file. Tell the user to open a pull request next; a confirmer checks it on the issue page and comments `/confirm`.

When re-checking a paper that is already listed, do not change the data: list the discrepancies with their sources for the user, who raises them in an issue.
