# How to add a paper

A paper goes from recommendation to inclusion in five steps. The annotator does the first three; a confirmer does the last two on the issue page. Confirmers never edit files.

| Step | Who | Where |
| --- | --- | --- |
| 1. Recommend the paper | Anyone | New issue |
| 2. Create a branch from the issue | Annotator | Locally or on GitHub |
| 3. Read, annotate, commit | Annotator | One file on the branch |
| 4. Review | Confirmer | Issue page |
| 5. Confirm | Confirmer | Comment `/confirm` on the issue |

**The one hard rule: every paper must be confirmed by a human developer who has checked it against the paper.** AI assistants may help read papers and draft annotations, but they cannot confirm.

## Step 1: Recommend the paper

Open an issue with the ["Recommend a paper" form](../../issues/new?template=add-paper.yml): title, link, and a sentence or two on why it belongs. Domain tags are optional. Note the issue number; the examples below use `12`.

Scope: a system uses its own outputs to improve itself or its successor, and this improvement loop is applied in some application domain. Borderline cases that meet only part of this (R0) are included too, and marked as such.

## Step 2: Create a branch from the issue

On the issue page, use **Development → Create a branch** and name the branch `paper/issue-12`; or locally:

```bash
git switch -c paper/issue-12 origin/main
python3 scripts/new_paper.py 12
```

`new_paper.py` reads the issue (this needs the `gh` command-line tool) and creates `data/pending/issue-12.yml` with the title, link and domain tags filled in. Without `gh`, use `python3 scripts/new_paper.py 12 --title "..." --url https://...`.

If you do not have write access to the repository, fork it first and do the same in your fork.

## Step 3: Read, annotate, commit

Open `data/pending/issue-12.yml`. The comment above each field gives its meaning and the allowed values. One field per line:

```yaml
# Self-reference depth: R0 External artifacts only / R1 Prompts, memory, skill and tool libraries / R2 Scaffold and own code / R3 Weights and training pipeline / R4 The improvement process itself
R: R2

# Evidence for the depth: section and quotation from the paper
r_evidence: Section 3.2, the agent edits its own Python code base directly
```

While filling it in:

- **Required:** title, link, first-release date, domain tags, reading depth. Fill in the other fields as far as you can.
- **Report your reading depth honestly.** If you read only the abstract, write `abstract only`. Such an annotation can be submitted, but it cannot be confirmed until the paper has been read in full.
- **Do not infer.** Do not add what the paper does not say. If you cannot decide, write `unclear`; if the verification cost is not reported, write `not reported`.
- **Cite the paper for every judgement.** For self-reference depth, feedback source, loop automation and evidence strength, give the section or page.
- **Put anything you are unsure about in `review_points`.** This is what the confirmer reads first. For each point, state the specific question, the candidate values with the evidence for each, which one you recommend and why, and where in the paper to look. For example:

  ```yaml
  review_points: |
    1. **Is the self-reference depth R1 or R2?**
       - A. R1: the experiments in the main text only add tools to the tool library (Section 4.1).
       - B. R2: Appendix B says the agent rewrites its own tool-selection logic.
       - Recommend A. The Appendix B variant does not appear in the experiments; if you find it evaluated in the experimental setup, choose B.
  ```
- Values must not contain `|`. Do not fill in an id or confirmation fields.

Detailed rules for each field are in [`annotation-rules.md`](.agents/skills/paper-reading/references/annotation-rules.md). You can also have an AI assistant draft the annotation with the repository's `paper-reading` skill, but you must check it against the paper yourself.

Check and commit:

```bash
python3 scripts/check_data.py
git add data/pending/issue-12.yml
git commit -m "Annotate paper for #12"
git push -u origin paper/issue-12
gh pr create --fill          # or open the pull request on GitHub
```

A pull request contains only this one file.

## Step 4: Review on the issue page

As soon as the pull request is opened, the annotation appears as a table on the **page of issue #12**, followed by the points to check and any format problems.

The confirmer checks it against the paper, concentrating on the self-reference depth and its evidence, the feedback source, loop automation, evidence strength, and the annotator's points to check.

- **If you disagree:** comment on the issue what should change and why. When the annotator pushes an updated file, the annotation on the page is replaced with the new version.
- **If everything is right:** go to step 5.

## Step 5: Confirm

The confirmer comments on the issue with a single line:

```
/confirm
```

The workflow checks that:

- the commenter is a human account on the [confirmer list](.github/confirmers.txt);
- the annotation shown on the page is the latest version on the branch (if the branch changed before the comment, wait for the new annotation to appear and confirm again);
- the annotation has no format problems, and its reading depth is full text or partial text;
- the pull request changes only this one annotation file.

If all checks pass, the workflow assigns the paper an ID (such as `P116`), writes it to `data/papers.tsv` with the confirmer and the date, updates the README, and closes the pull request and the issue. If any check fails, the workflow explains why on the issue and changes nothing.

Confirmers may confirm papers they annotated themselves, provided they are on the confirmer list.

## Other cases

- **Correcting an existing annotation:** open an issue with the paper ID, what it should say, and the evidence from the paper. A maintainer edits `data/papers.tsv`.
- **Joining the confirmer list:** open a pull request against `.github/confirmers.txt`; a maintainer reviews it.
- **A paper that fits no existing domain or subfield:** use the closest one and raise it in `review_points`; the maintainers decide whether to add a new one.
- **Editing confirmation fields by hand:** not allowed. A pull request that changes `status`, `confirmed_by` or `confirmed_at` is blocked by the checks.
- **Annotation files written in the old Chinese vocabulary:** run `python3 scripts/migrate_to_english.py data/pending/issue-12.yml` to convert the controlled values, then translate the free-text fields it lists.
