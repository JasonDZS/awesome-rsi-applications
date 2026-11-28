"""Shared definitions for the paper list: columns, allowed values, parsing and validation."""
import csv
import json
import os
import re
import subprocess
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
    "title": "Title", "url": "Link", "date": "First released", "venue": "Publication status",
    "tags": "Domain tags", "subclass": "Subfield", "task": "Task", "criteria": "Inclusion criteria",
    "object": "What is improved", "R": "Self-reference depth", "r_evidence": "Evidence for the depth",
    "feedback": "Feedback source", "loop": "Loop automation", "accumulation": "Accumulation",
    "rounds": "Improvement rounds", "cost": "Verification cost", "reversibility": "Failure reversibility",
    "claim": "Authors' claim", "evidence": "Evidence strength", "result": "Main result",
    "limits": "Failures and limitations", "reading": "Reading depth", "confidence": "Confidence",
    "notes": "Notes",
}
UNCLEAR = "unclear"          # not enough information to decide; the confirmer has to check
NOT_REPORTED = "not reported"
STATUS_PENDING, STATUS_CONFIRMED = "pending", "confirmed"

DOMAINS = {"0": "AI R&D itself", "1": "Engineering", "2": "Natural sciences",
           "3": "Physical and embodied systems", "4": "Social sciences"}
SUBFIELDS = {
    "0": ["Agent self-improvement", "Data and weight self-adaptation", "Automated ML research"],
    "1": ["Software engineering", "Algorithm discovery", "Chip design and systems optimization"],
    "2": ["Mathematics", "Chemistry and materials", "Biology and medicine", "Physics and earth sciences"],
    "3": ["Robot skill acquisition", "Automated reward and curriculum design", "Open-ended embodied learning"],
    "4": ["Economics and finance", "Social simulation", "Forecasting", "Deployed service agents",
          "Policy and education", "Law"],
}
LEVELS = {"R0": "External artifacts only", "R1": "Prompts, memory, skill and tool libraries",
          "R2": "Scaffold and own code", "R3": "Weights and training pipeline",
          "R4": "The improvement process itself"}
FEEDBACK = ["formal verification", "automated evaluation", "simulation", "real-world experiment",
            "human review", "learned judge", "self-evaluation", UNCLEAR]
CRITERIA = ["closed loop", "self-reference", "accumulation"]
ENUMS = {
    "loop": ["human-in-the-loop", "semi-automatic", "fully automatic", UNCLEAR],
    "accumulation": ["single round", "multi-generation single lineage", "open-ended population or archive",
                     UNCLEAR],
    "cost": ["seconds to minutes", "hours", "days to weeks", "months or longer, or requires humans",
             NOT_REPORTED],
    "reversibility": ["fully reversible", "retryable at a cost", "irreversible", UNCLEAR],
    "evidence": ["in-task", "cross-task", "cross-task, independently verified", UNCLEAR],
    "confidence": ["high", "medium", "low"],
}
CLAIMS = ["RSI", "self-improvement", "not claimed"]       # may be followed by a note in parentheses
READING_NEW = ["full text", "partial text", "abstract only"]
READING_LEGACY = ["abstract", "excerpt", "unread"]      # only in rows drafted before the review workflow
READ_IN_FULL = {"full text", "partial text"}
# accounts that must never be recorded as the confirmer: confirmation has to come from a person
NOT_HUMAN = re.compile(r"(\[bot\]$|^claude$|^copilot$|^codex$|^github-actions$|bot$)", re.I)
# separators accepted in multi-valued fields; "; " is canonical
SPLIT = re.compile(r"\s*[;；、]\s*")
MULTI = ("subclass", "criteria", "feedback")


def repo_slug():
    """owner/repo of this repository: $GH_REPO if set, else parsed from the origin remote."""
    if os.environ.get("GH_REPO"):
        return os.environ["GH_REPO"]
    url = subprocess.run(["git", "-C", str(ROOT), "remote", "get-url", "origin"],
                         capture_output=True, text=True, check=True).stdout.strip()
    m = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?/?$", url)
    if not m:
        raise ValueError(f"cannot tell the GitHub repository from the origin remote: {url}")
    return m.group(1)


def gh_api(path, method="GET", fields=None, paginate=False):
    """Call the GitHub REST API through the gh CLI and return the parsed JSON.

    REST only: some environments (for example cloud agent sessions) block gh's GraphQL commands
    such as `gh issue create` and `gh pr create`.
    """
    cmd = ["gh", "api", f"repos/{repo_slug()}/{path}", "-X", method]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    data = None
    if fields is not None:
        cmd += ["--input", "-"]
        data = json.dumps(fields)
    out = subprocess.run(cmd, input=data, capture_output=True, text=True)
    if out.returncode:
        raise RuntimeError((out.stderr or out.stdout).strip())
    result = json.loads(out.stdout) if out.stdout.strip() else None
    if paginate:
        result = [item for page in result for item in page]
    return result


def arxiv_id(url):
    """The arXiv identifier in a link (without version), or '' if it is not an arXiv link."""
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", url or "")
    return m.group(1) if m else ""


def canonical_url(url):
    """arXiv links are stored as the abstract page without a version; other links are kept as given."""
    url = (url or "").strip()
    return f"https://arxiv.org/abs/{arxiv_id(url)}" if arxiv_id(url) else url


def same_paper(a, b):
    a, b = canonical_url(a), canonical_url(b)
    return bool(a) and a.rstrip("/").lower() == b.rstrip("/").lower()


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
            raise ValueError(f"line {i} cannot be parsed: {line.strip()[:40]}")
        key, value = m.group(1), m.group(2).strip()
        if key in out:
            raise ValueError(f"field {key} appears twice")
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


def split_multi(value):
    return [x for x in SPLIT.split(value or "") if x]


def normalise(row):
    """Canonical separators for multi-valued fields; trims everything else."""
    r = {k: (v or "").strip() for k, v in row.items()}
    if r.get("tags"):
        r["tags"] = ";".join(sorted(set(re.findall(r"[0-4]", r["tags"]))))
    for key in MULTI:
        if r.get(key):
            r[key] = "; ".join(split_multi(r[key]))
    return r


def validate(r, where, legacy_ok=False):
    """Return a list of problems with one row (already normalised)."""
    e = []
    for key in REQUIRED:
        if not r.get(key):
            e.append(f"{where}: required field {LABELS[key]} ({key}) is empty")
    for key, v in r.items():
        if key != "review_points" and v and ("|" in v or "\n" in v):
            e.append(f"{where}: {key} must not contain '|' or a line break")
    if r.get("url") and not re.match(r"https?://\S+$", r["url"]):
        e.append(f"{where}: url is not a valid link")
    if r.get("date") and not re.fullmatch(r"\d{4}(-\d{2})?", r["date"]):
        e.append(f"{where}: date must be YYYY-MM")
    if r.get("tags") and not re.fullmatch(r"[0-4](;[0-4])*", r["tags"]):
        e.append(f"{where}: tags must be digits 0-4 separated by ;")
    if r.get("R") and not re.match(rf"(R[0-4]|{UNCLEAR})", r["R"]):
        e.append(f"{where}: R must start with R0-R4, or be '{UNCLEAR}'")
    for key, allowed in (("feedback", FEEDBACK), ("criteria", CRITERIA)):
        for item in split_multi(r.get(key, "")):
            if item not in allowed:
                e.append(f"{where}: unknown {LABELS[key].lower()} '{item}'; allowed: {', '.join(allowed)}")
    for key, allowed in ENUMS.items():
        if r.get(key) and r[key] not in allowed:
            e.append(f"{where}: {LABELS[key]} ({key}) = '{r[key]}' is not one of: {' / '.join(allowed)}")
    if r.get("claim") and not any(r["claim"] == c or r["claim"].startswith(c + " (") for c in CLAIMS):
        e.append(f"{where}: claim must be one of {', '.join(CLAIMS)}, optionally followed by a note in parentheses")
    readings = READING_NEW + (READING_LEGACY if legacy_ok else [])
    if r.get("reading") and r["reading"] not in readings:
        e.append(f"{where}: reading must be one of: {', '.join(READING_NEW)}")
    return e


def validate_confirmation(r, where):
    e = []
    by, at = r.get("confirmed_by", ""), r.get("confirmed_at", "")
    if r.get("status") == STATUS_CONFIRMED:
        if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", by) or NOT_HUMAN.search(by):
            e.append(f"{where}: a confirmed row needs confirmed_by to be a human GitHub login")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", at):
            e.append(f"{where}: a confirmed row needs confirmed_at as YYYY-MM-DD")
        if r.get("reading") not in READ_IN_FULL:
            e.append(f"{where}: a confirmed paper must have been read in full or in part (reading)")
    elif r.get("status") == STATUS_PENDING:
        if by or at:
            e.append(f"{where}: a pending row must not have confirmed_by or confirmed_at")
    else:
        e.append(f"{where}: status must be '{STATUS_PENDING}' or '{STATUS_CONFIRMED}'")
    return e


def render_review(r, errors=(), source=""):
    """Markdown shown to the confirmer on the issue page."""
    def v(key):
        return r.get(key) or "—"
    tags = "; ".join(f"{t} {DOMAINS[t]}" for t in r.get("tags", "").split(";") if t in DOMAINS) or "—"
    link = f"[{r.get('title', '')}]({r['url']})" if r.get("url") else r.get("title", "")
    lines = [f"### Annotation awaiting confirmation: {link}", ""]
    if source:
        lines += [source, ""]
    lines += ["| Field | Value |", "| --- | --- |",
              f"| First released / publication status | {v('date')} / {v('venue')} |",
              f"| Domain tags | {tags} |"]
    for key in ["subclass", "task", "criteria", "object", "R", "r_evidence", "feedback", "loop",
                "accumulation", "rounds", "cost", "reversibility", "claim", "evidence", "result",
                "limits", "reading", "confidence", "notes"]:
        lines.append(f"| {LABELS[key]} | {v(key)} |")
    lines += ["", "#### Points for you to check", "",
              r.get("review_points") or "The annotator listed no points to check."]
    if errors:
        lines += ["", "#### ⚠️ Format problems (fix before confirming)", ""] + [f"- {x}" for x in errors]
    return "\n".join(lines)
