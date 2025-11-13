# orchestrator/blueprint_indexer.py
#
# One-time (or occasionally repeated) indexer for the two big blueprint docs.
# It:
#   - Reads the Non-Technical and Technical plans
#   - Splits them into section-based markdown files with stable IDs
#   - Writes JSON indexes for orchestrator + Cursor agents
#
# Outputs:
#   docs/blueprints/nt/NT-<section>.md
#   docs/blueprints/td/TD-<section>.md
#   docs/blueprints/nt-index.json
#   docs/blueprints/td-index.json
#   docs/blueprints/toc-cache.json

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]

NT_PATH = REPO_ROOT / "ProjectBlueprint" / "Combined_Master_PLAIN_Non_Tech_001.docx"
TD_PATH = REPO_ROOT / "ProjectBlueprint" / "TechnicalDevelopmentPlan.odt"

DOCS_BP_DIR = REPO_ROOT / "docs" / "blueprints"


@dataclass
class Section:
    id: str              # e.g. "NT-1.5.Q"
    doc_type: str        # "nt" | "td"
    section_number: str  # e.g. "1.5.Q"
    title: str
    lines: List[str]
    source: str          # filename


def _log(msg: str) -> None:
    print(f"[blueprint_indexer] {msg}")


def _extract_docx_lines(path: Path) -> List[str]:
    import docx  # type: ignore

    if not path.exists():
        _log(f"NT docx not found at {path}")
        return []

    try:
        doc = docx.Document(str(path))
    except Exception as e:  # pragma: no cover
        _log(f"ERROR: python-docx could not open NT docx ({path}): {e}")
        _log("Hint: open in Word/LibreOffice and 'Save As' a fresh .docx, then rerun.")
        return []

    lines: List[str] = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            lines.append(text)
    return lines


def _extract_odt_lines(path: Path) -> List[str]:
    from odf.opendocument import load  # type: ignore
    from odf import teletype  # type: ignore

    if not path.exists():
        _log(f"TD odt not found at {path}")
        return []

    try:
        doc = load(str(path))
        text = teletype.extractText(doc)
    except Exception as e:  # pragma: no cover
        _log(f"ERROR: odfpy could not open TD odt ({path}): {e}")
        return []

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines


SECTION_ID_RE = re.compile(
    r"""^
        (?P<num>           # numeric/alpha section id
            \d+(?:[.\-]\d+)*   # 1 or 1.23 or 1.23.4
            (?:[.\-][A-Z])?    # optional .Q / -G etc
        )
        \s+
        (?P<title>.+)$     # rest of the line is title
    """,
    re.VERBOSE,
)


def _normalise_token(token: str) -> str:
    # Strip leading § etc, trailing punctuation, and normalise weird dashes.
    t = token.strip()
    t = t.lstrip("§")
    t = t.rstrip(".:;—–-")
    t = t.replace("‑", "-").replace("–", "-").replace("—", "-")
    return t


def _iter_sections_from_lines(
    lines: List[str], doc_type: str, source_name: str
) -> List[Section]:
    sections: List[Section] = []
    current: Section | None = None

    for line in lines:
        if not line.strip():
            continue

        parts = line.split(None, 1)
        if not parts:
            continue

        first = _normalise_token(parts[0])
        rest = parts[1].strip() if len(parts) > 1 else ""

        # Try regex match for headings like "1.5.Q Work packages ..."
        m = SECTION_ID_RE.match(f"{first} {rest}") if rest else None

        if m:
            section_number = m.group("num")
            title = m.group("title").strip()

            # Close previous section
            if current is not None:
                sections.append(current)

            sec_id = f"{doc_type.upper()}-{section_number}"
            current = Section(
                id=sec_id,
                doc_type=doc_type,
                section_number=section_number,
                title=title,
                lines=[],
                source=source_name,
            )
        else:
            if current is not None:
                current.lines.append(line)
            else:
                # Skip preface text before the first numbered section
                continue

    if current is not None:
        sections.append(current)

    return sections


def _write_section_files(sections: List[Section]) -> list[dict]:
    DOCS_BP_DIR.mkdir(parents=True, exist_ok=True)
    index_entries: list[dict] = []

    for sec in sections:
        subdir = DOCS_BP_DIR / sec.doc_type
        subdir.mkdir(parents=True, exist_ok=True)

        filename = f"{sec.id}.md"
        rel_path = Path("docs") / "blueprints" / sec.doc_type / filename
        full_path = REPO_ROOT / rel_path

        header = f"# {sec.section_number} {sec.title}\n\n"
        body = "\n\n".join(sec.lines).rstrip() + "\n" if sec.lines else ""

        frontmatter = (
            "---\n"
            f"id: {sec.id}\n"
            f"doc_type: {sec.doc_type}\n"
            f"source: {sec.source}\n"
            f"section_number: {sec.section_number}\n"
            "---\n\n"
        )

        full_path.write_text(frontmatter + header + body, encoding="utf-8")

        index_entries.append(
            {
                "id": sec.id,
                "doc_type": sec.doc_type,
                "section_number": sec.section_number,
                "title": sec.title,
                "file": rel_path.as_posix(),
                "source": sec.source,
            }
        )

    return index_entries


def build_blueprint_index() -> dict:
    _log(f"REPO_ROOT = {REPO_ROOT}")
    _log(f"NT doc: {NT_PATH}")
    _log(f"TD doc: {TD_PATH}")

    nt_sections: List[Section] = []
    td_sections: List[Section] = []

    # Non-technical plan
    nt_lines = _extract_docx_lines(NT_PATH)
    if nt_lines:
        _log(f"Extracting NT sections from {NT_PATH.name}...")
        nt_sections = _iter_sections_from_lines(nt_lines, "nt", NT_PATH.name)
        _log(f"Found {len(nt_sections)} NT sections.")
    else:
        _log("WARNING: No NT sections extracted (doc missing or unreadable).")

    # Technical plan
    td_lines = _extract_odt_lines(TD_PATH)
    if td_lines:
        _log(f"Extracting TD sections from {TD_PATH.name}...")
        td_sections = _iter_sections_from_lines(td_lines, "td", TD_PATH.name)
        _log(f"Found {len(td_sections)} TD sections.")
    else:
        _log("WARNING: No TD sections extracted (doc missing or unreadable).")

    nt_index = _write_section_files(nt_sections) if nt_sections else []
    td_index = _write_section_files(td_sections) if td_sections else []

    # Write JSON indexes
    DOCS_BP_DIR.mkdir(parents=True, exist_ok=True)

    if nt_index:
        (DOCS_BP_DIR / "nt-index.json").write_text(
            json.dumps(nt_index, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        _log(f"Wrote {len(nt_index)} NT index entries to {DOCS_BP_DIR/'nt-index.json'}")

    if td_index:
        (DOCS_BP_DIR / "td-index.json").write_text(
            json.dumps(td_index, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        _log(f"Wrote {len(td_index)} TD index entries to {DOCS_BP_DIR/'td-index.json'}")

    toc_cache = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nt": nt_index,
        "td": td_index,
    }
    (DOCS_BP_DIR / "toc-cache.json").write_text(
        json.dumps(toc_cache, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    _log(f"Wrote TOC cache to {DOCS_BP_DIR/'toc-cache.json'}")

    return {
        "nt_sections": [asdict(s) for s in nt_sections],
        "td_sections": [asdict(s) for s in td_sections],
        "nt_index": nt_index,
        "td_index": td_index,
    }


def main() -> None:
    out = build_blueprint_index()
    _log(
        f"Done. nt_sections={len(out.get('nt_sections', []))}, "
        f"td_sections={len(out.get('td_sections', []))}"
    )


if __name__ == "__main__":
    main()
