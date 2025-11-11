# scripts/blueprints/build_index.py
"""
Normalize blueprint source documents and build a search-ready index.

Outputs (existing, kept):
- docs/blueprints/plain/*.md        (normalized text for every supported source)
- docs/blueprints/nt-index.json     (non-technical manifest subset)
- docs/blueprints/td-index.json     (technical manifest subset)
- docs/blueprints/sections.json     (full per-file records; backward compatible)
- docs/blueprints/toc-cache.json    (counts + skipped diagnostics)

New / enhanced:
- docs/index/manifest.json          (canonical per-source registry; includes num_chunks)
- docs/index/chunks.jsonl           (JSONL of chunked text with stable chunk_ids)
- docs/index/segments.jsonl         (alias of chunks.jsonl for orchestrator readers)

Supported inputs under docs/blueprints/: .md, .txt, .docx, .odt, .pdf

Usage:
    python scripts/blueprints/build_index.py
    # or with knobs:
    python scripts/blueprints/build_index.py --chunk-size 1200 --overlap 200
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Tuple

# Optional imports guarded so the script still runs without them
try:
    from docx import Document  # python-docx
except Exception:  # pragma: no cover
    Document = None  # type: ignore

try:
    from odf.opendocument import load as odf_load  # odfpy
    from odf import teletype
except Exception:  # pragma: no cover
    odf_load = None  # type: ignore
    teletype = None  # type: ignore

try:
    from PyPDF2 import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None  # type: ignore


REPO = pathlib.Path(__file__).resolve().parents[2]
SRC_DIR = REPO / "docs" / "blueprints"
PLAIN_DIR = SRC_DIR / "plain"
INDEX_DIR = REPO / "docs" / "index"

PLAIN_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED = {".md", ".txt", ".docx", ".odt", ".pdf"}


# ------------------------------
# Helpers
# ------------------------------
def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def norm_whitespace(s: str) -> str:
    # Normalize newlines, strip BOM, collapse spaces/tabs, trim spaces before newlines
    s = s.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"[ \t]+\n", "\n", s)
    return s.strip()


def from_docx(path: pathlib.Path) -> str:
    if Document is None:
        return ""
    try:
        doc = Document(str(path))
        return "\n".join(p.text or "" for p in doc.paragraphs)
    except Exception:
        return ""


def from_odt(path: pathlib.Path) -> str:
    if odf_load is None or teletype is None:
        return ""
    try:
        doc = odf_load(str(path))
        return teletype.extractText(doc.body) or ""
    except Exception:
        return ""


def from_pdf(path: pathlib.Path) -> str:
    if PdfReader is None:
        return ""
    try:
        reader = PdfReader(str(path))
        out = []
        for p in getattr(reader, "pages", []):
            out.append(p.extract_text() or "")
        return "\n".join(out)
    except Exception:
        return ""


def type_of(path: pathlib.Path) -> str:
    """
    Naive domain classifier: try filename, then folder hints.
    Returns "tech" or "non_tech".
    """
    name = str(path).lower()
    nontech_tokens = {
        "non-tech",
        "non_tech",
        "nontech",
        "non technical",
        "nontechnical",
        "plain_non_tech",
    }
    if any(tok in name for tok in nontech_tokens):
        return "non_tech"
    if "technical" in name or "tech" in name:
        return "tech"
    # fallback to folder hint
    return "tech" if "technical" in path.parts else "non_tech"


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def utc_iso(ts: float) -> str:
    # timezone-aware ISO string (fixes utcfromtimestamp deprecation)
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def chunk_text(
    text: str, target: int = 1200, overlap: int = 200, min_chunk: int = 300
) -> Iterable[str]:
    """
    Greedy, paragraph-aware char chunker. Prefers to split on '\n' near 'target'.
    Ensures forward progress and optional overlap between chunks.
    """
    if target <= 0:
        target = 1200
    if overlap < 0:
        overlap = 0
    if overlap >= target:
        overlap = int(target * 0.2)

    n = len(text)
    start = 0
    while start < n:
        end = min(start + target, n)
        search_from = start + int(target * 0.6)
        if search_from >= end:
            search_from = start
        split = text.rfind("\n", search_from, end)
        if split == -1 or split <= start + min_chunk // 2:
            split = end

        chunk = text[start:split].strip()
        if chunk:
            yield chunk

        if split >= n:
            break
        new_start = max(split - overlap, 0)
        if new_start <= start:
            new_start = split
        start = new_start


# ------------------------------
# Core normalization
# ------------------------------
def extract_text_for(path: pathlib.Path) -> str:
    ext = path.suffix.lower()
    if ext in (".md", ".txt"):
        return read_text(path)
    if ext == ".docx":
        return from_docx(path)
    if ext == ".odt":
        return from_odt(path)
    if ext == ".pdf":
        return from_pdf(path)
    return ""


def normalize_one(path: pathlib.Path) -> Tuple[Dict[str, Any], str]:
    """
    Normalize a single source file.
    Returns (record, normalized_text). If the file is unsupported or empty, record contains 'skipped'.
    """
    if path.suffix.lower() not in SUPPORTED:
        return ({"skipped": True, "reason": f"Unsupported ext {path.suffix}"}, "")

    raw = extract_text_for(path)
    text = norm_whitespace(raw)
    if not text:
        return ({"skipped": True, "reason": f"No text extracted from {path.name}"}, "")

    # Write normalized markdown into /plain using the original filename (compat with existing tooling)
    rel = path.relative_to(SRC_DIR)
    plain_name = rel.with_suffix(".md").name
    out = PLAIN_DIR / plain_name
    out.write_text(text + "\n", encoding="utf-8")

    rec = {
        "source_rel": str(rel).replace("\\", "/"),
        "plain_rel": f"plain/{plain_name}",
        "title": path.stem,
        "domain": type_of(path),
        "words": len(text.split()),
        "sha1": sha1(text),
        "mtime": utc_iso(path.stat().st_mtime),
    }
    return (rec, text)


# ------------------------------
# Index build
# ------------------------------
def build_index(chunk_size: int, overlap: int) -> None:
    records: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []
    total_chunks = 0

    chunks_path = INDEX_DIR / "chunks.jsonl"
    segments_path = INDEX_DIR / "segments.jsonl"  # alias for consumers expecting this name
    manifest_path = INDEX_DIR / "manifest.json"

    # Open both JSONL outputs (we'll duplicate writes for compatibility)
    with open(chunks_path, "w", encoding="utf-8") as chunks_out, open(
        segments_path, "w", encoding="utf-8"
    ) as segments_out:
        for p in SRC_DIR.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in SUPPORTED:
                continue
            # Skip outputs/caches
            if "plain" in p.parts:
                continue

            rec, text = normalize_one(p)
            if "skipped" in rec:
                skipped.append({"path": str(p), "reason": rec["reason"]})
                continue

            # Chunk and emit
            doc_sha = rec["sha1"]
            chunks = list(chunk_text(text, target=chunk_size, overlap=overlap, min_chunk=300))
            for idx, ch in enumerate(chunks, start=1):
                chunk_id = f"{doc_sha}-{idx:04d}"
                row = {
                    "chunk_id": chunk_id,
                    "path": rec["source_rel"],
                    "plain_rel": rec["plain_rel"],
                    "title": rec["title"],
                    "domain": rec["domain"],
                    "chunk_index": idx,
                    "total_chunks": len(chunks),
                    "text": ch,
                }
                line = json.dumps(row, ensure_ascii=False)
                chunks_out.write(line + "\n")
                segments_out.write(line + "\n")

            total_chunks += len(chunks)
            rec["num_chunks"] = len(chunks)
            records.append(rec)

    # Partition into technical/non-technical
    nt = [r for r in records if r["domain"] == "non_tech"]
    td = [r for r in records if r["domain"] == "tech"]

    # Write indices/registries (kept for backward compatibility)
    (SRC_DIR / "nt-index.json").write_text(
        json.dumps(nt, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (SRC_DIR / "td-index.json").write_text(
        json.dumps(td, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (SRC_DIR / "sections.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Canonical manifest for consumers
    manifest = {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "root": "docs/blueprints",
        "plain_root": "docs/blueprints/plain",
        "index_root": "docs/index",
        "chunk_size": chunk_size,
        "overlap": overlap,
        "counts": {"sources": len(records), "chunks": total_chunks},
        "sources": records,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Optional cache with diagnostics
    (SRC_DIR / "toc-cache.json").write_text(
        json.dumps(
            {
                "counts": {
                    "all": len(records),
                    "non_tech": len(nt),
                    "tech": len(td),
                    "chunks": total_chunks,
                },
                "skipped": skipped,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Normalized={len(records)} Skipped={len(skipped)} Chunks={total_chunks} "
        "-> plain/*.md + manifest.json + {chunks,segments}.jsonl + nt-index.json + td-index.json"
    )


# ------------------------------
# CLI
# ------------------------------
def parse_args(argv: List[str]) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build blueprint indices and chunks.")
    ap.add_argument(
        "--chunk-size", type=int, default=1200, help="Target chunk size in characters (default: 1200)"
    )
    ap.add_argument(
        "--overlap", type=int, default=200, help="Character overlap between chunks (default: 200)"
    )
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])
    build_index(chunk_size=args.chunk_size, overlap=args.overlap)


if __name__ == "__main__":
    main()
