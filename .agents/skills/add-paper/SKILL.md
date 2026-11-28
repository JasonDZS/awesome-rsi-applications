---
name: add-paper
description: Takes a paper from a link to a pull request awaiting confirmation in this repository. Given only a link (arXiv, PDF or publisher page), reads the paper, opens the "Recommend a paper" issue, drafts every field of the annotation, asks the user about each uncertain point with options and a recommendation, and after the user answers opens the pull request; the user then comments /confirm on the issue. Use when the user gives a paper link and asks to add, submit or include it. For reading or re-checking a paper without adding it, use paper-reading instead.
---

# Add a paper from a link

The user gives a link. You do everything up to the pull request; the user makes two decisions:

1. **In this conversation:** they answer the points you were unsure about. Only then do you open the pull request.
2. **On the issue page:** they (or another confirmer) check the annotation against the paper and comment `/confirm`. That comment is the confirmation, and only a person can make it.

Reading and annotating follow the `paper-reading` skill (`.agents/skills/paper-reading/SKILL.md`) and its `references/annotation-rules.md`. Read both before you start; this skill only adds the steps around them.

## Rules that must not be broken

1. **Never confirm.** Do not post `/confirm`, do not run `scripts/confirm.py`, do not write an id, `status`, `confirmed_by` or `confirmed_at`. If the user says "confirm it for me", explain that the confirmation has to be their own comment on the issue.
2. **The user's answer in this conversation is not the confirmation.** It only settles what goes into the pull request. Say so when you hand over.
3. **No pull request before the user has answered.** If nobody is there to answer (an unattended run), stop after step 5 and leave the branch local.
4. **One issue, one branch, one file.** The pull request contains only `data/pending/issue-<N>.yml`. Do not touch `data/papers.tsv` or the README.
5. **Everything the paper-reading skill forbids is forbidden here too:** no inferring what the paper does not say, no new domains, subfields or allowed values, and an honest `reading` value.

## Steps

### 1. Check for duplicates

```bash
python3 scripts/add_paper.py check <link>
```

- Already listed: stop and tell the user the paper ID. Offer to re-check the existing annotation with `paper-reading` instead.
- Has an open issue: tell the user, and ask whether to continue on that issue (branch `paper/issue-<N>`, `python3 scripts/new_paper.py <N>`) rather than opening a second one.
- Has only a closed issue: say so and ask before opening a new one.

### 2. Read the paper

Follow `paper-reading` steps 1 and 3 to 5: get the full text (for arXiv, `https://arxiv.org/pdf/<id>`), read it with the seven questions in mind, assign values by the annotation rules, and compare with the two or three closest papers in `data/papers.tsv`.

If you can only get the abstract, tell the user before going further: an `abstract only` annotation can be submitted but cannot be confirmed. Options: (A) the user supplies the PDF, (B) submit as `abstract only` and finish later, (C) stop. Recommend A.

### 3. Decide whether it is in scope

The list takes systems that use their own output to improve themselves or their successors, with the loop grounded in an application domain; R0 borderline cases (closed loop only) are accepted and labelled as such.

If the paper has no improvement loop at all (a survey, a benchmark, a one-shot method), do not open an issue. Tell the user why, with the options (A) do not add it, (B) add it anyway as an R0 borderline case, and your recommendation.

### 4. Open the issue, the branch and the annotation file

```bash
python3 scripts/add_paper.py open --title "<title as printed>" --url <link> \
  --reason "<one or two sentences: the improvement loop, the domain, the headline result>" --tags "<e.g. 0;1>"
```

This needs a clean working tree. It opens the issue, creates `paper/issue-<N>` from the latest default branch, and creates `data/pending/issue-<N>.yml` with the title, link and tags filled in. Write the reason in plain words from what you read; it is what people see first on the issue.

Then fill in every field of the file, following the comments in it:

- Values must not contain `|`. Multi-valued fields use `; `.
- Put the source for the self-reference depth in `r_evidence` and the sources for the other judgements in `notes`.
- For anything you cannot decide, write `unclear` (for cost: `not reported`) and make it a point to check.
- Write the points to check into `review_points` in the format of the paper-reading skill: the specific question, options A/B (each a value that can actually be entered, with its evidence), your recommendation with the reason and what would change it, and where in the paper to look.

Run `python3 scripts/check_data.py` and fix what it reports.

### 5. Show the draft and ask

Show the user, in the conversation:

- the issue link;
- how much of the paper you read, and what you could not read;
- the full draft annotation as a table (every field and its value, with the source for the four judgement fields);
- the points to check, numbered, each with its options and your recommendation.

Then ask for a decision on each point. Make it easy to answer: "1A 2B", or "go with your recommendations". If your environment has a tool for multiple-choice questions, use it, with your recommended option first. Wait for the answer.

If there are no uncertain points, still show the draft and ask whether to open the pull request.

### 6. Apply the answers

- Update the field values to what the user chose.
- Keep each point in `review_points`, and add one line under it: `Decided before submission: <option>, by the annotator.` The confirmer on the issue page should still see what was uncertain and how it was settled.
- If the user asks for other changes, make them. If a requested value is not an allowed one, say so and give the allowed options instead of inventing a value.
- Run `python3 scripts/check_data.py` again.

### 7. Open the pull request

```bash
python3 scripts/add_paper.py submit <N> --reader "<who read the paper and how much, e.g. read by an AI assistant: main text and appendices A to C>"
```

Add `--trailer "<line>"` or `--footer "<line>"` for any attribution lines your environment requires on commits or pull requests. The command validates the file, refuses if anything else changed, commits, pushes and opens the pull request.

### 8. Hand over

Tell the user, briefly:

- the issue link and the pull request link;
- that the annotation will appear on the issue page within a minute or two;
- that the last step is theirs: check it against the paper and comment `/confirm` **on the issue** (not on the pull request). The workflow then assigns the ID, adds the paper to the list and closes both.

If they want changes after this, edit the file on the same branch and run the `submit` command again; the rendering on the issue page is replaced.

## When something fails

- `open` says the working tree is not clean: do not stash or discard the user's work on your own. Tell them what is uncommitted and ask.
- The issue was opened but a later step failed: do not open a second issue. Continue from the existing one (`git switch -c paper/issue-<N> origin/<default branch>`, then `python3 scripts/new_paper.py <N>`).
- `/confirm` was refused on the issue: the workflow's comment says why (the branch changed after the rendering, a format problem, `abstract only`, or extra files in the pull request). Fix that; the user comments `/confirm` again.
