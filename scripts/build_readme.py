#!/usr/bin/env python3
"""Generate README.md from data/papers.tsv.

Usage: python3 scripts/build_readme.py
The paper list in README.md is generated; edit data/papers.tsv, not the README.
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paperlib as pl  # noqa: E402

OUT = pl.ROOT / "README.md"
DESCRIPTIONS = {
    "0": "General-purpose AI that improves itself, not tied to one application domain. "
         "May be tagged together with domains 1–4.",
    "1": "Software engineering, algorithm discovery, chip design and systems optimization. "
         "The loop runs only through digital environments.",
    "2": "Mathematics, chemistry and materials, biology and medicine, physics and earth sciences.",
    "3": "Robot skill acquisition, automated reward and curriculum design, open-ended embodied learning. "
         "The loop runs through the physical world or a simulation of it.",
    "4": "Economics and finance, social simulation, forecasting, deployed service agents, "
         "policy and education, law.",
}
LEVELS = list(pl.LEVELS)


def load():
    _, rows = pl.load_tsv()
    for r in rows:
        r["tag_list"] = [t for t in r["tags"].split(";") if t]
        m = re.match(r"R[0-4]", r["R"])
        r["level"] = m.group(0) if m else pl.UNCLEAR
    return rows


def cell(text):
    return text if text else "—"


def confirm(r):
    if r["status"] == pl.STATUS_CONFIRMED:
        return f"✅ @{r['confirmed_by']}"
    return "pending"


def paper_link(r):
    return f"[{r['title']}]({r['url']})" if r["url"] else r["title"]


def matrix(rows):
    lines = ["| Domain | " + " | ".join(LEVELS) + f" | {pl.UNCLEAR.capitalize()} | Total |",
             "| --- | " + " | ".join(["---"] * (len(LEVELS) + 2)) + " |"]
    for d, name in pl.DOMAINS.items():
        c = Counter(r["level"] for r in rows if d in r["tag_list"])
        nums = " | ".join(str(c.get(lv, 0)) for lv in LEVELS)
        lines.append(f"| {d}. {name} | {nums} | {c.get(pl.UNCLEAR, 0)} | {sum(c.values())} |")
    return "\n".join(lines)


def domain_table(rows, d):
    sel = sorted((r for r in rows if d in r["tag_list"]), key=lambda r: (r["date"], r["id"]))
    lines = ["| ID | Paper | First released | Subfield | What is improved | R | Feedback | Loop | "
             "Evidence | Claim | Reading | Confirmed |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in sel:
        other = [t for t in r["tag_list"] if t != d]
        also = f" (also {', '.join(other)})" if other else ""
        lines.append(
            f"| {r['id']} | {paper_link(r)}{also} | {r['date']} | {cell(r['subclass'])} | "
            f"{cell(r['object'])} | {cell(r['R'])} | {cell(r['feedback'])} | "
            f"{cell(r['loop'])} | {cell(r['evidence'])} | {cell(r['claim'])} | {cell(r['reading'])} | {confirm(r)} |"
        )
    return len(sel), "\n".join(lines)


def main():
    rows = load()
    n = len(rows)
    reading = Counter(r["reading"] for r in rows)
    confirmed = sum(r["status"] == pl.STATUS_CONFIRMED for r in rows)
    full = sum(reading.get(x, 0) for x in pl.READ_IN_FULL)
    partial = reading.get("abstract only", 0) + reading.get("abstract", 0) + reading.get("excerpt", 0)
    level_rows = "\n".join(f"| {k} | {v} |" for k, v in pl.LEVELS.items())
    parts = [f"""# Awesome RSI Applications

A list of papers that apply recursive self-improvement (RSI), maintained alongside a survey we are writing.

Most existing RSI surveys and lists are organized by mechanism: whether the model or the scaffold is changed, and how closed the loop is. This list is organized by **application domain** and asks one question: **how far has RSI progressed in each application domain?**

It currently holds {n} paper(s). Every paper is annotated with the same set of fields, so papers can be compared side by side.

> **Human confirmation: {confirmed} / {n}.** A paper is only formally included once a human developer has checked its annotation against the paper. The "Confirmed" column names the confirmer; entries marked "pending" are preliminary annotations drafted by an AI assistant and should not be cited as they are.
>
> **Status: in progress.** {full} paper(s) were read in full or in part, {partial} only as far as the abstract or an excerpt, and {reading.get('unread', 0)} could not be accessed; the "Reading" column gives the details. "{pl.UNCLEAR}" means there was not enough information to decide. Check the original paper before citing.

## Contents

- [How far each domain has progressed](#how-far-each-domain-has-progressed)
- [How to read this list](#how-to-read-this-list)
- [Papers](#papers)
- [Data and contributions](#data-and-contributions)
- [Related resources](#related-resources)

## How far each domain has progressed

Papers in each domain by self-reference depth (R0–R4). A paper can carry several domain tags, so the row totals add up to more than the number of papers.

{matrix(rows)}

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
{level_rows}

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
"""]
    for d, name in pl.DOMAINS.items():
        count, table = domain_table(rows, d)
        parts.append(f"### {d}. {name} ({count})\n\n{DESCRIPTIONS[d]}\n\n{table}\n")
    parts.append("""## Data and contributions

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

**Adding a paper from a link.** With an assistant that supports skills, give it the link and ask it to add the paper. The `add-paper` skill ([`.agents/skills/add-paper/`](.agents/skills/add-paper/SKILL.md)) reads the paper, opens the issue, drafts the annotation, asks you about the uncertain points, and opens the pull request once you have answered. You then check the annotation on the issue page and comment `/confirm`.

To correct an existing annotation, open an issue and cite the evidence (the section or sentence in the paper).

## Related resources

- [awesome-rsi](https://github.com/lobehub/awesome-rsi): an RSI list organized by mechanism, with sections on benchmarks and safety.
- [Awesome-Self-Evolving-Scientific-Agents](https://github.com/REAL-Lab-NU/Awesome-Self-Evolving-Scientific-Agents): self-evolving agents for scientific discovery.
- [Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops](https://arxiv.org/abs/2607.07663): a survey organized by what is improved and how closed the loop is.
- [Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104): a survey organized by foundation-model updates versus scaffold updates.
- [Who Improves the Robot? Toward Physical Recursive Self-Improvement](https://arxiv.org/abs/2610.18842): a survey dedicated to physical and embodied RSI.
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046): a survey of self-evolving agents.
""")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({n} papers)")


if __name__ == "__main__":
    main()
