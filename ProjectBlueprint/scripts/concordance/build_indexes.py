#!/usr/bin/env python3
"""
build_indexes.py — Scan split files and build:
  - docs/blueprints/nt-index.json
  - docs/blueprints/td-index.json
  - docs/blueprints/toc-cache.json
Also validates uniqueness of IDs and anchors.

Usage:
  python scripts/concordance/build_indexes.py
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO = Path(__file__).resolve().parents[2]
BP = REPO / "docs" / "blueprints"
NT_DIR = BP / "non-tech"
TD_DIR = BP / "tech"
TOC_PATH = BP / "toc-cache.json"
NT_INDEX = BP / "nt-index.json"
TD_INDEX = BP / "td-index.json"
REPORTS = REPO / "docs" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')

def parse_frontmatter(text: str) -> Dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    import yaml
    return yaml.safe_load(m.group(1)) or {}

def scan_dir(d: Path) -> Dict[str, Dict]:
    out = {}
    for p in sorted(d.glob("*.md")):
        if p.name.endswith("all.md"): continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        fm = parse_frontmatter(text)
        m = ANCHOR_RE.search(text)
        anchor = f"#{fm.get('id')}" if fm.get("id") else (f"#{m.group(1)}" if m else None)
        _id = fm.get("id")
        if _id and anchor:
            out[_id] = {
                "title": fm.get("title", ""),
                "path": p.as_posix(),
                "anchor": anchor,
                "parent": fm.get("parent")
            }
    return out

def build_tree(index: Dict[str, Dict]) -> Dict:
    # Build parent->children mapping
    tree = {}
    for _id, meta in index.items():
        tree.setdefault(_id, {"title": meta["title"], "children": []})
    for _id, meta in index.items():
        parent = meta.get("parent")
        if parent:
            tree.setdefault(parent, {"title": index[parent]["title"] if parent in index else "", "children": []})
            tree[parent]["children"].append(_id)
    # Sort children numerically where possible
    for node in tree.values():
        node["children"].sort(key=lambda s: [int(x) if x.isdigit() else x for x in s.replace("NT-","").replace("TD-","").split(".")])
    return tree

def validate(nt_map: Dict[str, Dict], td_map: Dict[str, Dict]) -> List[str]:
    errors = []
    # Unique IDs across both
    ids = set()
    for m in (nt_map, td_map):
        for k in m.keys():
            if k in ids:
                errors.append(f"Duplicate ID across corpora: {k}")
            ids.add(k)
    # Anchor consistency
    for m in (nt_map, td_map):
        for k, v in m.items():
            if not v["anchor"].endswith(k):
                errors.append(f"Anchor mismatch for {k}: {v['anchor']}")
    return errors

def main():
    nt_map = scan_dir(NT_DIR) if NT_DIR.exists() else {}
    td_map = scan_dir(TD_DIR) if TD_DIR.exists() else {}

    (NT_INDEX).write_text(json.dumps(nt_map, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (TD_INDEX).write_text(json.dumps(td_map, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    toc = {"NT": build_tree(nt_map), "TD": build_tree(td_map)}
    (TOC_PATH).write_text(json.dumps(toc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    errors = validate(nt_map, td_map)
    (REPORTS / "index_validate.json").write_text(json.dumps({"errors": errors}, indent=2))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
