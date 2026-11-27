"""Shared definitions for the paper list: columns, allowed values, parsing and validation."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "papers.tsv"
PENDING_DIR = ROOT / "data" / "pending"
PENDING_RE = re.compile(r"^data/pending/issue-(\d+)\.yml$")

COLUMNS = ["id", "title", "url", "date", "venue", "tags", "subclass", "task", "criteria", "object",
           "R", "r_evidence", "feedback", "loop", "accumulation", "rounds", "cost", "reversibility",
           "claim", "evidence", "result", "limits", "reading", "confidence", "notes",
           "status", "confirmed_by", "confirmed_at"]
CONFIRM_COLS = ["status", "confirmed_by", "confirmed_at"]
# keys a contributor fills in data/pending/issue-N.yml (review_points is shown to the confirmer, not stored)
PENDING_KEYS = [c for c in COLUMNS if c != "id" and c not in CONFIRM_COLS] + ["review_points"]
REQUIRED = ["title", "url", "date", "tags", "reading"]

LABELS = {
    "title": "论文标题", "url": "链接", "date": "首发年月", "venue": "发表状态", "tags": "领域标签",
    "subclass": "子类", "task": "任务", "criteria": "纳入标准", "object": "改进对象", "R": "自指深度",
    "r_evidence": "自指深度的依据", "feedback": "反馈来源", "loop": "闭环程度",
    "accumulation": "累积方式", "rounds": "改进轮数", "cost": "验证成本",
    "reversibility": "失败可逆性", "claim": "自称程度", "evidence": "证据强度", "result": "主要结果",
    "limits": "失败与局限", "reading": "阅读深度", "confidence": "置信度", "notes": "备注",
}
DOMAINS = {"0": "AI 研发自身", "1": "工程科学", "2": "自然科学", "3": "物理与具身", "4": "社会科学"}
FEEDBACK = ["形式验证", "自动评测", "仿真", "真实实验", "人类评审", "学习型评判", "自评", "待核对"]
CRITERIA = ["闭环", "自指", "累积"]
ENUMS = {
    "loop": ["人在回路", "半自动", "全自动", "待核对"],
    "accumulation": ["单轮", "单一谱系的多代迭代", "种群或档案库式的开放演化", "待核对"],
    "cost": ["秒到分钟", "小时", "天到周", "月以上或必须人工", "未报告"],
    "reversibility": ["完全可逆", "有消耗可重试", "不可逆", "待核对"],
    "evidence": ["任务内", "跨任务", "跨任务且独立验证", "待核对"],
    "confidence": ["高", "中", "低"],
}
READING_NEW = ["全文", "部分全文", "仅摘要"]
READING_LEGACY = ["摘要", "片段", "未读"]          # only in rows drafted before the review workflow
READ_IN_FULL = {"全文", "部分全文"}
# accounts that must never be recorded as the confirmer: confirmation has to come from a person
NOT_HUMAN = re.compile(r"(\[bot\]$|^claude$|^copilot$|^codex$|^github-actions$|bot$)", re.I)
SPLIT = re.compile(r"\s*[;；,，、]\s*")


def load_tsv(path=DATA):
    with Path(path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        cols = reader.fieldnames
        rows = list(reader)
    return cols, rows


def save_tsv(rows, path=DATA):
    with Path(path).open("w", encoding="utf-8", newline="") as f:
        f.write("|".join(COLUMNS) + "\n")
        for r in rows:
            f.write("|".join(r.get(c, "") for c in COLUMNS) + "\n")


def next_id(rows):
    return f"P{max((int(r['id'][1:]) for r in rows), default=0) + 1:03d}"


def parse_pending(text):
    """Parse the flat `key: value` format of data/pending/issue-N.yml.

    Lines starting with # are comments. `key: |` starts a block that runs over the
    following indented lines. No other YAML features are supported, on purpose.
    """
    out, lines, i = {}, text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_]+):[ \t]*(.*)$", line)
        if not m:
            raise ValueError(f"第 {i} 行无法解析：{line.strip()[:40]}")
        key, value = m.group(1), m.group(2).strip()
        if key in out:
            raise ValueError(f"字段 {key} 出现了两次")
        if value == "|":
            block = []
            while i < len(lines) and (not lines[i].strip() or lines[i][:1] in " \t"):
                block.append(lines[i])
                i += 1
            indent = min((len(b) - len(b.lstrip()) for b in block if b.strip()), default=0)
            value = "\n".join(b[indent:] for b in block).strip()
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key] = value
    return out


def normalise(row):
    """Canonical separators for multi-valued fields; trims everything else."""
    r = {k: (v or "").strip() for k, v in row.items()}
    if r.get("tags"):
        r["tags"] = ";".join(sorted(set(re.findall(r"[0-4]", r["tags"]))))
    for key in ("subclass", "criteria", "feedback"):
        if r.get(key):
            r[key] = "；".join(x for x in SPLIT.split(r[key]) if x)
    return r


def validate(r, where, legacy_ok=False):
    """Return a list of problems with one row (already normalised)."""
    e = []
    for key in REQUIRED:
        if not r.get(key):
            e.append(f"{where}：必填字段 {LABELS[key]}（{key}）为空")
    for key, v in r.items():
        if key != "review_points" and v and ("|" in v or "\n" in v):
            e.append(f"{where}：{key} 不能包含竖线或换行")
    if r.get("url") and not re.match(r"https?://\S+$", r["url"]):
        e.append(f"{where}：url 不是合法链接")
    if r.get("date") and not re.fullmatch(r"\d{4}(-\d{2})?", r["date"]):
        e.append(f"{where}：date 应为 YYYY-MM")
    if r.get("tags") and not re.fullmatch(r"[0-4](;[0-4])*", r["tags"]):
        e.append(f"{where}：tags 应为 0–4 的数字，用 ; 分隔")
    if r.get("R") and not re.match(r"(R[0-4]|待核对)", r["R"]):
        e.append(f"{where}：R 应以 R0–R4 开头，或为 待核对")
    for item in filter(None, r.get("feedback", "").split("；")):
        if item not in FEEDBACK:
            e.append(f"{where}：未知的反馈来源“{item}”，允许：{'、'.join(FEEDBACK)}")
    for item in filter(None, r.get("criteria", "").split("；")):
        if item not in CRITERIA:
            e.append(f"{where}：未知的纳入标准“{item}”，允许：{'、'.join(CRITERIA)}")
    for key, allowed in ENUMS.items():
        if r.get(key) and r[key] not in allowed:
            e.append(f"{where}：{LABELS[key]}（{key}）=“{r[key]}” 不在允许取值内：{'、'.join(allowed)}")
    readings = READING_NEW + (READING_LEGACY if legacy_ok else [])
    if r.get("reading") and r["reading"] not in readings:
        e.append(f"{where}：阅读深度应为 {'、'.join(READING_NEW)}")
    return e


def validate_confirmation(r, where):
    e = []
    by, at = r.get("confirmed_by", ""), r.get("confirmed_at", "")
    if r.get("status") == "已确认":
        if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", by) or NOT_HUMAN.search(by):
            e.append(f"{where}：已确认的行需要 confirmed_by 为真人的 GitHub 用户名")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", at):
            e.append(f"{where}：已确认的行需要 confirmed_at 为 YYYY-MM-DD")
        if r.get("reading") not in READ_IN_FULL:
            e.append(f"{where}：已确认的论文阅读深度必须是全文或部分全文")
    elif r.get("status") == "待确认":
        if by or at:
            e.append(f"{where}：待确认的行不能填写 confirmed_by 或 confirmed_at")
    else:
        e.append(f"{where}：status 应为 待确认 或 已确认")
    return e


def render_review(r, errors=(), source=""):
    """Markdown shown to the confirmer on the issue page."""
    def v(key):
        return r.get(key) or "—"
    tags = "；".join(f"{t} {DOMAINS[t]}" for t in r.get("tags", "").split(";") if t in DOMAINS) or "—"
    link = f"[{r.get('title', '')}]({r['url']})" if r.get("url") else r.get("title", "")
    lines = [f"### 待确认的标注：{link}", ""]
    if source:
        lines += [source, ""]
    lines += ["| 字段 | 取值 |", "| --- | --- |",
              f"| 首发年月 / 发表状态 | {v('date')} / {v('venue')} |",
              f"| 领域标签 | {tags} |"]
    for key in ["subclass", "task", "criteria", "object", "R", "r_evidence", "feedback", "loop",
                "accumulation", "rounds", "cost", "reversibility", "claim", "evidence", "result",
                "limits", "reading", "confidence", "notes"]:
        lines.append(f"| {LABELS[key]} | {v(key)} |")
    lines += ["", "#### 需要你核对的点", "", r.get("review_points") or "填写人没有列出需要核对的点。"]
    if errors:
        lines += ["", "#### ⚠️ 格式问题（修正前不能确认）", ""] + [f"- {x}" for x in errors]
    return "\n".join(lines)
