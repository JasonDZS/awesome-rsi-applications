# 如何添加一篇论文

一篇论文从推荐到收录走五步。前三步由填写人完成，后两步在 Issue 页面上由确认人完成。确认人不需要改任何文件。

| 步骤 | 谁来做 | 在哪里 |
| --- | --- | --- |
| 1. 推荐论文 | 任何人 | 新建 Issue |
| 2. 基于 Issue 开分支 | 填写人 | 本地或 GitHub 网页 |
| 3. 读论文、填标注、提交 | 填写人 | 分支上的一个文件 |
| 4. 审阅 | 确认人 | Issue 页面 |
| 5. 确认 | 确认人 | 在 Issue 评论 `/confirm` |

**唯一的硬规则：每篇论文都必须由一位真实的开发人员对照原文确认。** AI 助手可以帮忙读论文、起草标注，但不能确认。

## 第 1 步：推荐论文

用[“推荐论文”表单](../../issues/new?template=add-paper.yml)开一个 Issue，填标题、链接和一两句推荐理由。领域标签可选。记下 Issue 的编号，下面用 `12` 举例。

收录范围：系统用自己的产出改进自己或后继系统，并且这个改进回路落在某个应用领域上。只满足一部分条件的边界案例（R0）也收，会如实标注。

## 第 2 步：基于 Issue 开分支

在 Issue 页面右侧 **Development → Create a branch**，把分支命名为 `paper/issue-12`；或者在本地：

```bash
git switch -c paper/issue-12 origin/main
python3 scripts/new_paper.py 12
```

`new_paper.py` 会读取 Issue（需要 `gh` 命令行工具），生成 `data/pending/issue-12.yml`，标题、链接和领域标签已经填好。没有 `gh` 时用 `python3 scripts/new_paper.py 12 --title "……" --url https://……`。

没有仓库写权限的人先 fork，在 fork 里做同样的事。

## 第 3 步：读论文，填标注，提交

打开 `data/pending/issue-12.yml`。每个字段上方的注释写明了含义和允许的取值，一行一个字段：

```yaml
# 自指深度：R0 仅外部产物 / R1 提示、记忆、技能库 / R2 脚手架与自身代码 / R3 权重与训练流程 / R4 改进“改进过程”本身
R: R2 脚手架与自身代码

# 自指深度的依据：原文章节或语句
r_evidence: §3.2，智能体直接修改自己的 Python 代码库
```

填写时注意：

- **必填**：标题、链接、首发年月、领域标签、阅读深度。其余字段尽量填。
- **如实填写阅读深度。** 只读了摘要就写 `仅摘要`，这样的标注可以提交，但在读过全文之前不能被确认。
- **不推断。** 原文没写的不要补。拿不准的写 `待核对`，验证成本没有报告就写 `未报告`。
- **判断要有出处。** 自指深度、反馈来源、闭环程度、证据强度这四项，写上原文的章节或页码。
- **把拿不准的地方写进 `review_points`。** 这是确认人主要看的内容。每条写清楚具体问题、可选的取值和各自的依据、你建议哪一个和理由、去原文哪里看。例如：

  ```yaml
  review_points: |
    1. **自指深度是 R1 还是 R2？**
       - A. R1：正文实验只往工具库里添加工具（§4.1）。
       - B. R2：附录 B 提到智能体会改写自己的工具选择逻辑。
       - 建议 A。附录 B 的做法没有出现在实验里；如果你在实验设置里看到它被实际评测，应选 B。
  ```
- 取值里不能有竖线 `|`。不要填写编号和确认信息。

各字段的详细口径见 [`annotation-rules.md`](.agents/skills/paper-reading/references/annotation-rules.md)。也可以让 AI 助手用仓库自带的 `paper-reading` 技能起草，但内容要由你自己对照原文核对。

检查并提交：

```bash
python3 scripts/check_data.py
git add data/pending/issue-12.yml
git commit -m "Annotate paper for #12"
git push -u origin paper/issue-12
gh pr create --fill          # 或在网页上发起 pull request
```

一个 pull request 只包含这一个文件。

## 第 4 步：在 Issue 页面审阅

pull request 一发起，标注就会以表格的形式出现在 **Issue #12 的页面**上，后面跟着“需要你核对的点”和格式问题（如果有）。

确认人对照原文核对，重点看自指深度及其依据、反馈来源、闭环程度、证据强度，以及填写人列出的核对点。

- **有不同意见**：直接在 Issue 里评论要改什么、依据是什么。填写人修改文件并推送后，页面上的标注会换成新的版本。
- **没有问题**：进入第 5 步。

## 第 5 步：确认

确认人在 Issue 里单独评论一行：

```
/confirm
```

流程会检查：

- 评论者是真人账号，并且在[确认人名单](.github/confirmers.txt)里；
- 页面上显示的标注就是分支上最新的版本（评论之前分支又有更新的话，需要等新标注出现后重新确认）；
- 标注没有格式问题，阅读深度是全文或部分全文；
- pull request 只改了这一个标注文件。

全部通过后，流程给论文分配编号（`P116` 这样），写入 `data/papers.tsv` 并记下确认人和日期，更新 README，关闭 pull request 和 Issue。任何一项不通过，流程会在 Issue 里说明原因，不做任何改动。

确认人可以确认自己填写的论文，前提是本人在确认人名单里。

## 其他情况

- **纠正已收录论文的标注**：开一个 Issue，写明论文编号、应该改成什么、原文依据。由维护者修改 `data/papers.tsv`。
- **加入确认人名单**：向 `.github/confirmers.txt` 提 pull request，由维护者审核。
- **归不进现有的领域或子类**：照最接近的填，在 `review_points` 里提出，由维护者决定是否新增。
- **手工改确认信息**：不允许。pull request 里改动 `status`、`confirmed_by`、`confirmed_at` 会被检查拦下。
