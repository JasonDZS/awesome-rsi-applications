#!/usr/bin/env python3
"""Build the annotation page (a claude.ai artifact) from template.html and the repository's rules and data.

  python3 tools/annotate-page/build.py > annotate.html

The page asks Claude to draft an annotation from a PDF, lets a person settle the uncertain points, and
produces an issue that the paper-intake workflow turns into a branch and a pull request. Rebuild and
republish it when the annotation rules, the allowed values or the list change.
"""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import paperlib as pl  # noqa: E402

_, rows = pl.load_tsv()
cfg = {
    "repo": "JasonDZS/awesome-rsi-applications",
    "built": datetime.date.today().isoformat(),
    "labels": pl.LABELS, "domains": pl.DOMAINS, "subfields": pl.SUBFIELDS, "levels": pl.LEVELS,
    "feedback": pl.FEEDBACK, "criteria": pl.CRITERIA, "enums": pl.ENUMS, "claims": pl.CLAIMS,
    "reading": pl.READING_NEW,
    "papers": [{k: r[k] for k in ("id", "title", "url", "tags", "subclass", "R", "feedback", "evidence", "claim")}
               for r in rows],
    "rules": (ROOT / ".agents/skills/paper-reading/references/annotation-rules.md").read_text(encoding="utf-8"),
}
data = json.dumps(cfg, ensure_ascii=False).replace("<", "\\u003c")
template = (Path(__file__).parent / "template.html").read_text(encoding="utf-8")
assert "/*__DATA__*/" in template
sys.stdout.write(template.replace("/*__DATA__*/", data))
