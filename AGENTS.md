# 给 AI 助手的仓库说明

这是一份 RSI（递归自我改进）应用论文清单。数据在 `data/papers.tsv`，README 由脚本生成。

## 规则

- **绝不确认论文。** 每篇论文必须由真实的开发人员对照原文确认。确认的方式是确认人在论文的 Issue 页面评论 `/confirm`，之后由流程写入确认信息。你可以起草标注，但不能把 `status` 设为 `已确认`，不能填写 `confirmed_by` 或 `confirmed_at`，不能运行 `scripts/confirm.py`，也不能替任何人发 `/confirm` 评论。
- **新论文写进标注文件，不直接写进数据。** 在分支 `paper/issue-<编号>` 上用 `python3 scripts/new_paper.py <编号>` 生成 `data/pending/issue-<编号>.yml` 并填写；一个 PR 只改这一个文件。不要往 `data/papers.tsv` 里追加新行。
- **不要手改 README 里的表格。** 改 `data/papers.tsv`，然后运行 `python3 scripts/build_readme.py`。
- **提交前运行校验。** `python3 scripts/check_data.py` 必须通过。
- **数据文件以 `|` 分隔。** 文本字段里不能出现 `|`。列的顺序和允许取值以 `scripts/paperlib.py` 为准。
- **不要擅自新增领域、子类或枚举取值。** 遇到归不进去的情况，提出来由维护者决定。
- **需要人确认的事项，要给出选项和建议。** 列出可选的做法、各自的依据，并说明你建议哪一个、为什么。不要只抛出开放式的问题，也不要因为自己有建议就当作已定。

## 技能

- 阅读或标注论文时，使用 `.agents/skills/paper-reading/` 里的 `paper-reading` 技能。

## 文件

- `data/papers.tsv`：全部数据，一行一篇。
- `scripts/check_data.py`：校验数据和确认规则。
- `scripts/build_readme.py`：从数据生成 README。
- `data/pending/issue-<编号>.yml`：待确认论文的标注文件，只存在于分支上。
- `scripts/new_paper.py`：为一个 Issue 生成标注文件。
- `scripts/render_review.py`：把标注文件渲染成 Issue 页面上的审阅内容。
- `scripts/confirm.py`：记录确认，只由 `/confirm` 流程运行。
- `scripts/paperlib.py`：列、允许取值和校验规则的定义。
- `.github/confirmers.txt`：确认人名单。
- `CONTRIBUTING.md`：添加论文的分步教程。
