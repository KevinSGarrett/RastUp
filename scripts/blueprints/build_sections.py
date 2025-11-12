#!/usr/bin/env python3
# Rebuild NT (DOCX) sections and merge with TD windows → sections.json
# Compatible with large docs; stdlib only.

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Repo root → docs/blueprints/*
ROOT = Path(__file__).resolve().parents[2]
BP_DIR = ROOT / "docs" / "blueprints"

NT_DOCX = BP_DIR / "Combined_Master_PLAIN_Non_Tech_001.docx"
TD_JSON = BP_DIR / "sections.td.json"       # written by build_td_windows.py
NT_JSON = BP_DIR / "sections.nt.json"
COMBINED_JSON = BP_DIR / "sections.json"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def _err(msg: str) -> None:
    print(f"[build_sections] {msg}", file=sys.stderr)


def _is_valid_docx(p: Path) -> bool:
    return p.exists() and zipfile.is_zipfile(p)


def _extract_nt_entries(docx_path: Path):
    """
    Parse word/document.xml and extract Heading1..Heading6 paragraphs.
    Produce entries with stable IDs: NT-H{level}-{####} and para ranges.
    """
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")

    root = ET.fromstring(xml)
    paras = list(root.findall(".//w:p", NS))

    # Collect (para_index, level, title)
    provisional = []
    for idx, p in enumerate(paras):
        level = None
        ppr = p.find("w:pPr", NS)
        if ppr is not None:
            pstyle = ppr.find("w:pStyle", NS)
            if pstyle is not None:
                val = pstyle.get(f"{{{W_NS}}}val")
                if val:
                    m = re.match(r"Heading([1-6])$", val, re.I)
                    if m:
                        level = int(m.group(1))
        # Text of the paragraph
        title = "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()
        if level and title:
            provisional.append({"level": level, "title": title, "para_start": idx})

    # Assign para_end = next start - 1 (or last paragraph)
    for i, e in enumerate(provisional):
        end = (len(paras) - 1) if i == len(provisional) - 1 else provisional[i + 1]["para_start"] - 1
        e["para_end"] = end

    # Assign stable IDs per level
    counters = {i: 0 for i in range(1, 7)}
    entries = []
    for e in provisional:
        counters[e["level"]] += 1
        eid = f"NT-H{e['level']}-{counters[e['level']]:04d}"
        entries.append(
            {
                "id": eid,
                "kind": "NT",
                "title": e["title"],
                "level": e["level"],
                "para_start": e["para_start"],
                "para_end": e["para_end"],
            }
        )
    return entries


def main():
    if not NT_DOCX.exists():
        _err(f"ERROR: NT DOCX not found at {NT_DOCX}")
        sys.exit(2)
    if not _is_valid_docx(NT_DOCX):
        _err(f"ERROR: '{NT_DOCX.name}' is not a valid .docx (OOXML/zip).")
        _err("Open the original in Word/LibreOffice and 'Save As' .docx, or run:")
        _err(f'  soffice --headless --convert-to docx --outdir "{BP_DIR}" "{NT_DOCX}"')
        sys.exit(2)

    BP_DIR.mkdir(parents=True, exist_ok=True)

    # Build NT entries
    nt_entries = _extract_nt_entries(NT_DOCX)
    NT_JSON.write_text(json.dumps(nt_entries, ensure_ascii=False, indent=2), encoding="utf-8")

    # Merge TD windows if present
    td_entries = []
    if TD_JSON.exists():
        try:
            td_entries = json.loads(TD_JSON.read_text(encoding="utf-8"))
        except Exception as e:
            _err(f"WARNING: failed to read TD windows '{TD_JSON.name}': {e}")

    combined = nt_entries + td_entries
    COMBINED_JSON.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {len(nt_entries)} NT entries → {NT_JSON}")
    print(f"TD entries merged: {len(td_entries)}")
    print(f"Combined sections → {COMBINED_JSON} (total {len(combined)})")


if __name__ == "__main__":
    main()
