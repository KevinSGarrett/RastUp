"""
CLI for orchestrator knowledge plumbing: build, audit, read, query.

Supports:
- python -m orchestrator.knowledge build
- python -m orchestrator.knowledge audit --strict
- python -m orchestrator.knowledge read --path PATH --first N
- python -m orchestrator.knowledge query --text "..." --k 5

Writes are confined to docs/* to respect SAFE‑MODE guardrails.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


# Resolve repo root relative to this file to be cross‑platform
REPO = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO / "docs"
BP_DIR = DOCS_DIR / "blueprints"
PLAIN_DIR = BP_DIR / "plain"
INDEX_DIR = DOCS_DIR / "index"

SECTIONS = BP_DIR / "sections.json"
NT_DOCX = BP_DIR / "Combined_Master_PLAIN_Non_Tech_001.docx"
TD_ODT = BP_DIR / "TechnicalDevelopmentPlan.odt"


def _safe_mode() -> bool:
    return (REPO / "ops" / "flags" / "safe-mode.json").exists()


def build(chunk_size: int = 1200, overlap: int = 200) -> Tuple[int, str]:
    """Run the index build script to refresh normalized outputs and indices."""
    py = sys.executable
    script = REPO / "scripts" / "blueprints" / "build_index.py"
    if not script.exists():
        return 1, f"missing: {script}"
    args = [py, str(script)]
    # pass explicit knobs to ensure deterministic outputs when specified
    if chunk_size is not None:
        args += ["--chunk-size", str(int(chunk_size))]
    if overlap is not None:
        args += ["--overlap", str(int(overlap))]
    r = subprocess.run(args, cwd=str(REPO), text=True, capture_output=True)
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode, out.strip()


def audit(strict: bool) -> Tuple[int, str]:
    msgs: List[str] = []
    ok = True

    # Legacy presence checks (optional now)
    msgs.append(f"NT source: {'OK' if NT_DOCX.exists() else 'MISS'} ({NT_DOCX.name})")
    msgs.append(f"TD source: {'OK' if TD_ODT.exists() else 'MISS'} ({TD_ODT.name})")

    # Expected normalized + indices
    checks = [
        (PLAIN_DIR, PLAIN_DIR.is_dir(), "plain/ directory exists"),
        (BP_DIR / "nt-index.json", (BP_DIR / "nt-index.json").exists(), "nt-index.json"),
        (BP_DIR / "td-index.json", (BP_DIR / "td-index.json").exists(), "td-index.json"),
        (SECTIONS, SECTIONS.exists(), "sections.json"),
        (BP_DIR / "toc-cache.json", (BP_DIR / "toc-cache.json").exists(), "toc-cache.json"),
        (INDEX_DIR / "manifest.json", (INDEX_DIR / "manifest.json").exists(), "manifest.json"),
        (INDEX_DIR / "chunks.jsonl", (INDEX_DIR / "chunks.jsonl").exists(), "chunks.jsonl"),
        (INDEX_DIR / "segments.jsonl", (INDEX_DIR / "segments.jsonl").exists(), "segments.jsonl"),
    ]
    for p, exists, label in checks:
        if exists:
            msgs.append(f"OK: {label}")
        else:
            msgs.append(f"MISS: {label}")
            ok = False

    # Validate sections.json shape
    if SECTIONS.exists():
        try:
            data = json.loads(SECTIONS.read_text(encoding="utf-8", errors="ignore"))
            n = len(data) if isinstance(data, list) else 0
            msgs.append(f"sections.json entries={n}")
        except Exception as e:
            msgs.append(f"ERR: sections.json invalid: {e}")
            ok = False

    rc = 0 if (ok or not strict) else 1
    return rc, "\n".join(msgs)


def _resolve_read_path(p: str) -> Path:
    """Resolve a user path to a readable file under docs/blueprints or plain/."""
    raw = Path(p)
    if raw.is_absolute():
        return raw
    # Try relative to plain/ first, then to blueprints/
    cand1 = PLAIN_DIR / raw
    if cand1.exists():
        return cand1
    # If user passed a source path under docs/blueprints, map to plain equivalent
    cand2 = BP_DIR / raw
    if cand2.exists():
        return PLAIN_DIR / (cand2.name if cand2.is_file() else str(raw))
    # If user already included 'plain/' prefix
    if str(raw).startswith("plain/"):
        cand3 = BP_DIR / raw
        if cand3.exists():
            return cand3
    # Fallback into repo relative
    return (REPO / raw)


def read_path(path: str, first: int) -> Tuple[int, str]:
    p = _resolve_read_path(path)
    if not p.exists():
        return 1, f"not found: {path}"

    # Support directory inputs by selecting a representative file
    if p.is_dir():
        # Prefer normalized markdown in the directory
        md_files = sorted([x for x in p.glob("*.md") if x.is_file()])
        candidates = md_files or sorted([x for x in p.iterdir() if x.is_file()])
        if not candidates:
            return 1, f"no files under directory: {path}"
        p = candidates[0]

    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return 1, f"read error: {e}"
    lines = txt.splitlines()
    n = max(1, int(first)) if first and first > 0 else len(lines)
    out = "\n".join(lines[:n])
    return 0, out


def _tokenize(s: str) -> List[str]:
    return [t for t in re.split(r"[^A-Za-z0-9]+", s.lower()) if t]


def query(text: str, k: int = 5) -> Tuple[int, str]:
    """Naive term‑frequency retrieval over chunks.jsonl. Returns top‑k matches."""
    idx = INDEX_DIR / "chunks.jsonl"
    if not idx.exists():
        return 1, "missing: docs/index/chunks.jsonl — run build first"
    q_tokens = _tokenize(text)
    if not q_tokens:
        return 1, "empty query"

    hits: List[Tuple[float, Dict[str, str]]] = []
    try:
        with idx.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row: Dict[str, str] = json.loads(line)
                except Exception:
                    continue
                body = str(row.get("text", "")).lower()
                score = 0.0
                for t in q_tokens:
                    # simple term frequency; mildly weight exact word matches
                    score += body.count(t)
                if score > 0:
                    hits.append((score, row))
    except Exception as e:
        return 1, f"query error: {e}"

    hits.sort(key=lambda x: x[0], reverse=True)
    k = max(1, int(k))
    top = hits[:k]
    if not top:
        return 0, "(no matches)"

    def preview(s: str, max_len: int = 280) -> str:
        s = (s or "").strip().replace("\n", " ")
        return s if len(s) <= max_len else s[: max_len - 1] + "…"

    lines = []
    for i, (score, row) in enumerate(top, start=1):
        lines.append(
            f"{i}. [{row.get('chunk_id')}] {row.get('title')} — {row.get('path')}\n   {preview(row.get('text',''))}"
        )
    return 0, "\n".join(lines)


def main(argv: List[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="orchestrator.knowledge")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Build normalized blueprints and indices")
    p_build.add_argument("--chunk-size", type=int, default=1200)
    p_build.add_argument("--overlap", type=int, default=200)

    p_audit = sub.add_parser("audit", help="Audit presence/shape of indices")
    p_audit.add_argument("--strict", action="store_true")

    p_read = sub.add_parser("read", help="Read a normalized blueprint file")
    p_read.add_argument("--path", required=True)
    p_read.add_argument("--first", type=int, default=40)

    p_query = sub.add_parser("query", help="Query chunks for text")
    p_query.add_argument("--text", required=True)
    p_query.add_argument("--k", type=int, default=5)

    ns = ap.parse_args(argv or sys.argv[1:])

    if ns.cmd == "build":
        rc, msg = build(ns.chunk_size, ns.overlap)
        if msg:
            print(msg)
        raise SystemExit(rc)

    if ns.cmd == "audit":
        rc, msg = audit(ns.strict)
        print(msg)
        raise SystemExit(rc)

    if ns.cmd == "read":
        rc, msg = read_path(ns.path, ns.first)
        if msg:
            print(msg)
        raise SystemExit(rc)

    if ns.cmd == "query":
        rc, msg = query(ns.text, ns.k)
        if msg:
            print(msg)
        raise SystemExit(rc)


if __name__ == "__main__":
    main()
