#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate TD section windows from the TechnicalDevelopmentPlan.odt without external libs.
Writes TD-only entries to docs/blueprints/sections.td.json.
"""
import json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BLUEPRINTS = REPO / "docs" / "blueprints"
ODT_PATH = BLUEPRINTS / "TechnicalDevelopmentPlan.odt"
TD_TMP = BLUEPRINTS / "sections.td.json"

NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}

def _get_text(el):
    # Join all text nodes recursively (ODT may split across spans)
    chunks = []
    for node in el.iter():
        if node.text:
            chunks.append(node.text)
        if node.tail:
            chunks.append(node.tail)
    return "".join(chunks).strip()

def load_odt_paragraphs(odt_path: Path):
    if not odt_path.exists():
        return []
    with zipfile.ZipFile(odt_path) as z:
        with z.open("content.xml") as f:
            tree = ET.parse(f)
    root = tree.getroot()
    body = root.find(".//office:body/office:text", NS)
    if body is None:
        return []
    paras = []
    for child in body:
        tag = child.tag
        if tag.endswith("}h"):  # text:h (heading)
            txt = _get_text(child)
            lvl = child.attrib.get(f"{{{NS['text']}}}outline-level")
            try:
                lvl = int(lvl) if lvl else 1
            except Exception:
                lvl = 1
            paras.append({"kind": "H", "level": lvl, "text": txt})
        elif tag.endswith("}p"):  # text:p (paragraph)
            txt = _get_text(child)
            if txt.strip():
                paras.append({"kind": "P", "text": txt})
    return paras

def build_td_windows(paras, win_size=20):
    # If headings exist, prefer heading-based sections; else windows
    has_headings = any(p["kind"] == "H" for p in paras)
    entries = []
    if has_headings:
        # Group paragraphs under headings (until next heading of same or higher level)
        idx = 0
        heads = [(i, p) for i, p in enumerate(paras) if p["kind"] == "H"]
        for n, (i, h) in enumerate(heads, start=1):
            level = h.get("level", 2)
            start = i
            # Find next heading with level <= current
            end = len(paras) - 1
            for j in range(i + 1, len(paras)):
                if paras[j]["kind"] == "H" and paras[j].get("level", 2) <= level:
                    end = j - 1
                    break
            entries.append({
                "id": f"TD-H{level}-{n:04d}",
                "kind": "TD",
                "title": h.get("text", "")[:180],
                "level": level,
                "para_start": start,
                "para_end": end,
                "file": str(ODT_PATH.relative_to(REPO)).replace("\\", "/")
            })
    else:
        # Window the non-empty paragraphs
        content_idxs = [i for i, p in enumerate(paras) if p["kind"] == "P"]
        n = 0
        for s in range(0, len(content_idxs), win_size):
            n += 1
            block = content_idxs[s:s+win_size]
            if not block:
                continue
            start, end = block[0], block[-1]
            title = paras[start]["text"][:180]
            entries.append({
                "id": f"TD-WIN-{n:04d}",
                "kind": "TD",
                "title": title,
                "level": 2,
                "para_start": start,
                "para_end": end,
                "file": str(ODT_PATH.relative_to(REPO)).replace("\\", "/")
            })
    return entries

def main():
    paras = load_odt_paragraphs(ODT_PATH)
    td_entries = build_td_windows(paras)
    BLUEPRINTS.mkdir(parents=True, exist_ok=True)
    TD_TMP.write_text(json.dumps(td_entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(td_entries)} TD entries → {TD_TMP}")

if __name__ == "__main__":
    main()
