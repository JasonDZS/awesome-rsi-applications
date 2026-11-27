# 给 AI 助手的仓库说明

这是一份 RSI（递归自我改进）应用论文清单。数据在 `data/papers.tsv`，README 由脚本生成。

## 规则

- **绝不确认论文。** 每篇论文必须由真实的开发人员对照原文确认。你可以起草标注，但不能把 `status` 设为 `已确认`，也不能填写 `confirmed_by` 或 `confirmed_at`。
- **不要手改 README 里的表格。** 改 `data/papers.tsv`，然后运行 `python3 scripts/build_readme.py`。
- **提交前运行校验。** `python3 scripts/check_data.py` 必须通过。
- **数据文件以 `|` 分隔。** 文本字段里不能出现 `|`。列的顺序和允许取值以 `scripts/check_data.py` 为准。
- **不要擅自新增领域、子类或枚举取值。** 遇到归不进去的情况，提出来由维护者决定。

## 技能

- 阅读或标注论文时，使用 `.agents/skills/paper-reading/` 里的 `paper-reading` 技能。

## 文件

- `data/papers.tsv`：全部数据，一行一篇。
- `scripts/check_data.py`：校验数据和确认规则。
- `scripts/build_readme.py`：从数据生成 README。
- `scripts/issue_to_row.py`：把“添加论文”表单的 Issue 转成一行数据。
- `CONTRIBUTING.md`：添加论文的分步教程。
