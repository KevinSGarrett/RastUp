#!/usr/bin/env python3
"""
extract_acceptance.py — Extract "Acceptance Criteria" and Gherkin-style blocks into
docs/blueprints/acceptance/NT-*.md, linking back to the source anchor.

Why it works now: your NT plan already includes explicit 'Acceptance Criteria' sections
throughout (e.g., §1.1–§1.3), which this scanner captures.  (It’s content-only; IDs/anchors come from split files.) 
"""
from __future__ import annotations
import os, re, sys, json
from pathlib import Path
from typing import List, Tuple

REPO = Path(__file__).resolve().parents[2]
NT_DIR = REPO / "docs" / "blueprints" / "non-tech"
ACC_DIR = REPO / "docs" / "blueprints" / "acceptance"
ACC_DIR.mkdir(parents=True, exist_ok=True)

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
AC_HEAD_RE = re.compile(r"^#{1,6}\s+Acceptance Criteria\b", re.I)
GHERKIN_RE = re.compile(r"^\s*(Given|When|Then|And|But)\b.*", re.I)

def parse_fm(text: str) -> dict:
    m = FM_RE.match(text)
    import yaml
    return yaml.safe_load(m.group(1)) if m else {}

def extract_ac_blocks(text: str) -> List[str]:
    lines = text.splitlines()
    blocks: List[str] = []
    in_ac_section = False
    current: List[str] = []
    for line in lines:
        if AC_HEAD_RE.match(line):
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            in_ac_section = True
            continue
        if in_ac_section:
            if line.startswith("#"):
                # next heading ends AC section
                if current:
                    blocks.append("\n".join(current).strip())
                in_ac_section = False
                current = []
            else:
                current.append(line)
        elif GHERKIN_RE.match(line):
            current.append(line)
        else:
            if current and not GHERKIN_RE.match(line):
                blocks.append("\n".join(current).strip()); current=[]
    if current: blocks.append("\n".join(current).strip())
    return [b for b in blocks if b]

def run():
    written = []
    for p in sorted(NT_DIR.glob("*.md")):
        if p.name.endswith("all.md"): continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        fm = parse_fm(text)
        m = ANCHOR_RE.search(text)
        _id = fm.get("id")
        if not _id or not m: continue
        anchor = m.group(1)
        blocks = extract_ac_blocks(text)
        if not blocks: continue
        out = ACC_DIR / f"{_id}.md"
        header = f"# Acceptance — {_id}: {fm.get('title','')}\n\n_Source_: [{p.name}]({os.path.relpath(p, ACC_DIR).replace(os.sep,'/') }#{_id})\n\n---\n\n"
        body = "\n\n---\n\n".join(f"```\n{b}\n```" for b in blocks)
        out.write_text(header + body + "\n", encoding="utf-8")
        written.append(out.as_posix())
    (REPO / "docs" / "reports" / "acceptance.log").write_text("\n".join(written), encoding="utf-8")

if __name__ == "__main__":
    run()
