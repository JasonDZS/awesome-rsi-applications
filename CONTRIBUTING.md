# 如何添加论文

添加一篇论文分五步：提交表单、转成数据行、真人对照原文确认、校验并生成 README、提 PR 合并。前两步任何人都可以做，第三步必须由一位真实的开发人员完成。

**确认规则**：每篇进入清单的论文都必须由一位真实的开发人员对照原文确认。AI 助手可以起草标注，但不能确认；自动化账号不能作为确认人。

## 准备

本机装好 Python 3 和 [GitHub CLI](https://cli.github.com/)（用 `gh auth login` 登录），并克隆仓库：

```bash
git clone https://github.com/JasonDZS/awesome-rsi-applications
cd awesome-rsi-applications
```

## 第 1 步：提交表单

打开仓库的 [Issues](../../issues)，点 New issue，选“添加论文”。

- 必填五项：论文标题、链接、首发年月（如 `2026-09`）、领域标签、阅读深度。
- 其余字段尽量填，拿不准选“待核对”。字段含义见 [README 的“如何阅读这份清单”](README.md#如何阅读这份清单)。
- “自指深度的依据”建议填，写原文章节号或一两句引文，确认时省事。

提交后记下 Issue 编号。下面假设是 `12`。

## 第 2 步：把表单转成一行数据

```bash
git checkout -b add-paper-12
gh issue view 12 --json body -q .body | python3 scripts/issue_to_row.py --append
```

脚本会检查必填项，按链接查重，分配下一个编号（如 `P116`），并把这一行追加到 `data/papers.tsv` 末尾，状态是“待确认”。如果论文已收录，脚本会报出已有的编号并停止。

第一次使用时请看一眼追加出来的那一行是否正确。

## 第 3 步：真人确认

由一位开发人员本人完成：

1. 打开论文原文，对照检查这一行的标注，重点看自指深度、反馈来源、闭环程度、证据强度。有出入就直接改。
2. 把这一行**最后三列**从 `待确认||` 改成：

   ```
   已确认|你的GitHub用户名|2026-11-27
   ```

注意：

- 阅读深度必须是“全文”或“部分全文”才能标为已确认。
- 文本字段里不要出现 `|`，它是分隔符。
- 没有亲自核对过的行，保持“待确认”。

## 第 4 步：校验并重新生成 README

```bash
python3 scripts/check_data.py
python3 scripts/build_readme.py
```

第一条通过时会输出类似 `ok: 116 papers, 1 confirmed by a human, 115 pending`。报错会指明行号和原因，改完再跑。

不要手改 README 里的表格，它由脚本从数据文件生成。

## 第 5 步：提 PR 并合并

```bash
git add -A
git commit -m "Add P116: 论文简称"
git push -u origin add-paper-12
gh pr create --fill --body "Closes #12"
```

PR 页面会带出一份确认清单，请逐项勾选。CI 会自动再跑一遍校验，并检查 README 是否与数据一致。数据文件的改动需要代码所有者审核，通过后合并，对应的 Issue 自动关闭。

## 用 AI 助手辅助阅读

仓库自带一个 `paper-reading` 技能，放在 `.agents/skills/paper-reading/`，遵循开放的 Agent Skills 格式。在仓库目录里启动 Codex 或 Claude Code 等支持该格式的工具，然后让它阅读某篇论文即可，例如：

```
用 paper-reading 技能读一下 https://arxiv.org/abs/2505.22954
```

它会给出每个字段的取值和原文出处、3 到 5 条“需要你核对的点”，以及与清单里相近论文的对照。你可以让它把草稿追加到数据文件里。

它不能替你完成第 3 步：技能只产出“待确认”的草稿。确认时请顺着它给的出处回到原文核对，重点看它列出的核对要点。

- Codex 直接读取 `.agents/skills/`。
- Claude Code 通过 `.claude/skills/paper-reading` 这个符号链接读取同一份文件。在 Windows 上克隆时如果符号链接没有生效，把 `.agents/skills/paper-reading` 复制到 `.claude/skills/` 下即可。
- 仓库级的规则（如“AI 助手不能确认论文”）写在 `AGENTS.md`，`CLAUDE.md` 引用它。

## 其他情况

**只确认已有的论文。** 跳过第 1、2 步，从第 3 步开始。一个 PR 可以确认多篇。

**纠正已有标注。** 直接改 `data/papers.tsv` 里对应的行，在 PR 里写明判断依据（原文章节或语句）。如果改的是一篇已确认的论文，把确认人和确认日期更新为你自己的。

**维护者跳过表单直接添加。** 在 `data/papers.tsv` 末尾手写一行，28 列的顺序见文件第一行表头，`status` 填 `待确认`，然后从第 3 步继续。用表格软件打开时把分隔符设成 `|` 会好编辑一些。

**成为确认人。** 请维护者把你的 GitHub 用户名加进 [`.github/CODEOWNERS`](.github/CODEOWNERS)。

## 数据文件的列

| 组 | 列 |
| --- | --- |
| 基本信息 | `id`、`title`、`url`、`date`、`venue` |
| 归类 | `tags`、`subclass`、`task`、`criteria` |
| 机制 | `object`、`R`、`r_evidence`、`feedback`、`loop`、`accumulation`、`rounds` |
| 反馈回路 | `cost`、`reversibility` |
| 声称与证据 | `claim`、`evidence`、`result`、`limits` |
| 标注信息 | `reading`、`confidence`、`notes` |
| 人工确认 | `status`、`confirmed_by`、`confirmed_at` |

枚举字段的允许取值以 [`scripts/check_data.py`](scripts/check_data.py) 为准。
