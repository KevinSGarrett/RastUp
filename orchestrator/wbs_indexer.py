from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Dict, Any

import docx
from docx.opc.exceptions import PackageNotFoundError

from odf.opendocument import load as odf_load
from odf import teletype


# Assume this file lives in C:\RastUp\RastUp\orchestrator\wbs_indexer.py
REPO_ROOT = Path(__file__).resolve().parents[1]

# --- BLUEPRINT INPUT FILES ----------------------------------------------------
# If you end up doing a "Save As" on the NT doc, just change this one line:
NT_DOC = REPO_ROOT / "ProjectBlueprint" / "Combined_Master_PLAIN_Non_Tech_001.docx"
# e.g. after re-saving: NT_DOC = REPO_ROOT / "ProjectBlueprint" / "Combined_Master_PLAIN_Non_Tech_001_FIXED.docx"

TD_DOC = REPO_ROOT / "ProjectBlueprint" / "TechnicalDevelopmentPlan.odt"

# --- OUTPUT LOCATIONS ---------------------------------------------------------
INDEX_DIR = REPO_ROOT / "docs" / "blueprints"
SNAPSHOT_DIR = REPO_ROOT / "docs" / "orchestrator"
INDEX_PATH = INDEX_DIR / "wbs-index.json"
SNAPSHOT_PATH = SNAPSHOT_DIR / "wbs-snapshot.json"


def _log(msg: str) -> None:
    print(f"[wbs_indexer] {msg}")


# --- TEXT EXTRACTION ----------------------------------------------------------


def _extract_docx_text(path: Path) -> str:
    _log("Extracting text from NT docx...")
    if not path.exists():
        _log(f"WARNING: NT docx not found at {path}")
        _log(
            "NT will be skipped for now. "
            "To fix this, make sure the file exists at that path."
        )
        return ""

    try:
        doc = docx.Document(str(path))
    except PackageNotFoundError as e:
        _log(f"WARNING: python-docx could not open NT docx ({path}): {e}")
        _log(
            "NT will be skipped for now. To fix this later, open the file in "
            "Word/LibreOffice and 'Save As' a fresh .docx in the same folder."
        )
        return ""

    parts: List[str] = []
    for p in doc.paragraphs:
        t = (p.text or "").strip()
        if t:
            parts.append(t)

    return "\n".join(parts)


def _extract_odt_text(path: Path) -> str:
    _log("Extracting text from TD odt...")
    if not path.exists():
        _log(f"ERROR: TD odt not found at {path}")
        raise FileNotFoundError(f"TD odt not found at {path}")

    doc = odf_load(str(path))

    # odfpy OpenDocument object doesn't have .childNodes, so use .text or .body
    root = getattr(doc, "text", None) or getattr(doc, "body", None)
    if root is None:
        _log("ERROR: TD odt has no .text or .body element; cannot extract text.")
        raise RuntimeError("TD odt has no .text or .body element")

    text = teletype.extractText(root)
    return text


# --- WBS EXTRACTION -----------------------------------------------------------

# 1) Explicit WBS markers, e.g. "WBS-1.2.3" or "WBS 1.2.3"
_WBS_EXPLICIT_RE = re.compile(r"\bWBS[- ](\d+(?:\.\d+)+)\b")

# 2) Plain numbered headings, e.g. "1.2 Title here", "2.3.4 Something"
_NUMERIC_HEADING_RE = re.compile(r"^\s*(\d+(?:\.\d+)+)\s+(.+)")


def _find_wbs_items(
    text: str,
    source: str,
    treat_plain_numbers_as_wbs: bool = True,
) -> List[Dict[str, Any]]:
    """
    Extract WBS-like items from a text blob.

    - Explicit: lines containing "WBS-1.2" or "WBS 1.2"
    - Numeric headings: lines starting with "1.2 ..." => treated as "WBS-1.2"
    """
    items: List[Dict[str, Any]] = []
    if not text:
        return items

    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue

        # First, look for explicit WBS markers
        m_explicit = _WBS_EXPLICIT_RE.search(line)
        if m_explicit:
            num = m_explicit.group(1)  # e.g. "1.2.3"
            wbs_id = f"WBS-{num}"
            root = f"WBS-{num.split('.')[0]}"
            items.append(
                {
                    "id": wbs_id,
                    "root": root,
                    "source": source,
                    "line_no": idx,
                    "line": line,
                    "origin": "explicit",
                }
            )
            continue

        # Then, treat plain numbered headings as WBS, if enabled
        if treat_plain_numbers_as_wbs:
            m_num = _NUMERIC_HEADING_RE.match(line)
            if m_num:
                num = m_num.group(1)  # e.g. "1.2.3"
                title_text = m_num.group(2).strip()
                wbs_id = f"WBS-{num}"
                root = f"WBS-{num.split('.')[0]}"
                items.append(
                    {
                        "id": wbs_id,
                        "root": root,
                        "source": source,
                        "line_no": idx,
                        "line": line,
                        "title": title_text,
                        "origin": "numeric_heading",
                    }
                )

    return items


# --- MAIN INDEX BUILD ---------------------------------------------------------


def build_wbs_index() -> Dict[str, Any]:
    _log(f"REPO_ROOT = {REPO_ROOT}")
    _log(f"NT doc: {NT_DOC}")
    _log(f"TD doc: {TD_DOC}")

    # NT (non‑technical) – best effort; may be skipped if docx is funky
    nt_text = ""
    if NT_DOC.exists():
        nt_text = _extract_docx_text(NT_DOC)
    else:
        _log(f"WARNING: NT doc not found at {NT_DOC} (skipping NT).")

    nt_items = _find_wbs_items(nt_text, "NT")
    _log(f"Found {len(nt_items)} WBS items in NT.")

    # TD (technical) – ODT
    td_text = _extract_odt_text(TD_DOC)
    td_items = _find_wbs_items(td_text, "TD")
    _log(f"Found {len(td_items)} WBS items in TD.")

    all_items = nt_items + td_items

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    roots = sorted({item["root"] for item in all_items}) if all_items else []

    out: Dict[str, Any] = {
        "repo_root": str(REPO_ROOT),
        "nt_doc": str(NT_DOC),
        "td_doc": str(TD_DOC),
        "total_items": len(all_items),
        "roots": roots,
        "items": all_items,
    }

    INDEX_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    SNAPSHOT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")

    _log(f"Wrote {len(all_items)} WBS items to {INDEX_PATH}")
    _log(f"Wrote snapshot to {SNAPSHOT_PATH}")

    if not all_items:
        print(
            "No WBS-style IDs were found in either document.\n"
            "Expected patterns like 'WBS-1.1: Title of work item', 'WBS 1.1 – Title', "
            "or numbered headings like '1.1 Title'."
        )

    return out


def main() -> None:
    try:
        out = build_wbs_index()
        _log(f"Done. total_items={out.get('total_items', 0)}")
    except Exception as e:
        _log(f"FATAL: {e}")
        raise


if __name__ == "__main__":
    main()
