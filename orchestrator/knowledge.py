# orchestrator/knowledge.py
from __future__ import annotations
import argparse, json, os, pathlib, re, sys, subprocess, time
from typing import Iterable, List, Dict, Tuple

REPO = pathlib.Path(__file__).resolve().parents[1]
BLUEPRINTS = REPO / "docs" / "blueprints"
PLAIN = BLUEPRINTS / "plain"
INDEX = REPO / "docs" / "index"
SEGMENTS = INDEX / "segments.jsonl"
MANIFEST = INDEX / "manifest.json"

_WORD = re.compile(r"[A-Za-z0-9_]+")
STOP = {"the","a","an","of","and","or","to","in","for","on","at","by","is","it","that","this","with","as","be","are","from","was","were","can","will","not","no","do","does","did"}
def _tok(s: str) -> List[str]:
    return [w.lower() for w in _WORD.findall(s) if len(w) > 2 and w.lower() not in STOP]

def iter_segments() -> Iterable[Dict]:
    if not SEGMENTS.exists():
        return
    with SEGMENTS.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue

def search_segments(query: str, k: int = 10) -> List[Dict]:
    q = _tok(query)
    if not q:
        return []
    scored: List[tuple[float,int,Dict]] = []
    i = 0
    for i, row in enumerate(iter_segments(), start=1):
        text = (row.get("text") or "").lower()
        title = (row.get("title") or "").lower()
        score = 0.0
        for t in q:
            c = text.count(t)
            if c:
                score += 1.0 + 0.5 * (c - 1)
        score += 2.0 * sum(1 for t in q if t in title)
        if score > 0:
            scored.append((score, i, row))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [r for _,__,r in scored[:k]]


def _safe_mode() -> bool:
    """
    SAFE-MODE: if ops/flags/safe-mode.json exists, avoid destructive actions.
    """
    return (REPO / "ops" / "flags" / "safe-mode.json").exists()


def _latest_source_mtime() -> float:
    """
    Return latest mtime among blueprint sources (excluding normalized/plain and index outputs).
    """
    latest = 0.0
    if not BLUEPRINTS.exists():
        return latest
    for p in BLUEPRINTS.rglob("*"):
        if not p.is_file():
            continue
        if "plain" in p.parts:
            continue
        if p.suffix.lower() in {".md", ".txt", ".docx", ".odt", ".pdf"}:
            try:
                latest = max(latest, p.stat().st_mtime)
            except Exception:
                continue
    return latest


def _need_rebuild() -> Tuple[bool, str]:
    """
    Decide whether index rebuild is needed.
    Criteria: missing manifest/segments or sources newer than both.
    """
    if not MANIFEST.exists() or not SEGMENTS.exists():
        return True, "missing_artifacts"
    try:
        manifest_m = MANIFEST.stat().st_mtime
        segments_m = SEGMENTS.stat().st_mtime
    except Exception:
        return True, "stat_error"
    floor = min(manifest_m, segments_m)
    latest = _latest_source_mtime()
    if latest == 0.0:
        # No sources found; if artifacts exist we treat as up-to-date
        return False, "no_sources"
    return (latest > floor, "sources_newer" if latest > floor else "up_to_date")


def _cli_build() -> int:
    if _safe_mode():
        print(json.dumps({"ok": True, "skipped": True, "reason": "safe_mode"}))
        return 0
    need, reason = _need_rebuild()
    if not need:
        print(json.dumps({"ok": True, "changed": False, "reason": reason}))
        return 0
    script = REPO / "scripts" / "blueprints" / "build_index.py"
    cmd = [sys.executable, str(script)]
    try:
        rc = subprocess.call(cmd)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{e}"}))
        return 1
    # brief settle to flush FS timestamp granularity on some filesystems
    time.sleep(0.1)
    ok = MANIFEST.exists() and SEGMENTS.exists()
    print(json.dumps({"ok": bool(rc == 0 and ok), "changed": True, "reason": "rebuilt"}))
    return 0 if rc == 0 and ok else 1


def _audit(strict: bool = False) -> Tuple[bool, Dict]:
    exists_manifest = MANIFEST.exists()
    exists_segments = SEGMENTS.exists()
    result: Dict[str, object] = {
        "safe_mode": _safe_mode(),
        "paths": {
            "manifest": str(MANIFEST.relative_to(REPO)),
            "segments": str(SEGMENTS.relative_to(REPO)),
        },
        "exists": {"manifest": exists_manifest, "segments": exists_segments},
        "warnings": [],
        "errors": [],
        "tools": {
            "docx": _probe_import("docx"),
            "odfpy": _probe_import("odf.opendocument"),
            "pypdf": _probe_import("PyPDF2"),
        },
    }
    ok = exists_manifest and exists_segments
    if not exists_manifest:
        result["errors"].append("manifest.json missing")  # type: ignore[index]
    if not exists_segments:
        result["errors"].append("segments.jsonl missing")  # type: ignore[index]
    # Validate JSON formats lightly
    if exists_manifest:
        try:
            json.loads(MANIFEST.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            ok = False
            result["errors"].append("manifest.json unreadable/invalid JSON")  # type: ignore[index]
    if exists_segments:
        try:
            # peek first line only
            with SEGMENTS.open("r", encoding="utf-8", errors="ignore") as f:
                line = f.readline()
                if line.strip():
                    json.loads(line)
        except Exception:
            ok = False
            result["errors"].append("segments.jsonl unreadable/invalid JSONL")  # type: ignore[index]

    # Tooling warnings
    for name, avail in list(result["tools"].items()):  # type: ignore[index]
        if not avail:
            result["warnings"].append(f"optional tool missing: {name}")  # type: ignore[index]

    if strict and not ok:
        return False, result
    return True, result


def _probe_import(mod: str) -> bool:
    try:
        __import__(mod)
        return True
    except Exception:
        return False

def _to_plain_candidate(path: str) -> pathlib.Path:
    p = pathlib.Path(path)
    if p.suffix.lower() in {".md", ".txt"} and "plain" in p.parts:
        return (REPO / path) if not p.is_absolute() else p
    # map source → plain twin
    stem = pathlib.Path(path).stem + ".md"
    return PLAIN / stem

def read_source(path: str) -> str:
    """
    Prefer normalized 'plain/*.md'. If not present, try the given path verbatim.
    """
    p = _to_plain_candidate(path)
    try_first = [p]
    if not p.as_posix().startswith("docs/blueprints/plain"):
        try_first.append(REPO / path)
    for cand in try_first:
        if cand.exists():
            try:
                return cand.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
    return ""

def _cli_query(text: str, k: int, as_json: bool) -> None:
    rows = search_segments(text, k=k)
    if as_json:
        out = [
            {
                "rank": idx,
                "chunk_id": r.get("chunk_id"),
                "title": r.get("title"),
                "domain": r.get("domain"),
                "path": r.get("path"),
                "plain_rel": r.get("plain_rel"),
            }
            for idx, r in enumerate(rows, start=1)
        ]
        print(json.dumps(out, ensure_ascii=False))
        return
    for idx, r in enumerate(rows, start=1):
        path = r.get("path") or r.get("plain_rel") or ""
        title = r.get("title", "")
        print(f"[{idx}] {title}  — {path}")

def _cli_show(path: str, first: int) -> None:
    out = read_source(path)
    if not out:
        print(f"NOT FOUND or unreadable: {path}")
        return
    lines = out.splitlines()[:first]
    print("\n".join(lines))


def _cli_read(path: str) -> None:
    out = read_source(path)
    if not out:
        print(f"NOT FOUND or unreadable: {path}")
        return
    print(out)

def main(argv: List[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="Rebuild knowledge indexes if needed")
    a = sub.add_parser("audit", help="Verify presence and shape of knowledge artifacts")
    a.add_argument("--strict", action="store_true", help="Fail when missing or invalid")

    q = sub.add_parser("query", help="Search normalized knowledge segments")
    q.add_argument("--text", required=True)
    q.add_argument("--k", type=int, default=5)
    q.add_argument("--json", action="store_true", help="Emit results as JSON array")

    s = sub.add_parser("show", help="Show first N lines of a source/normalized file")
    s.add_argument("--path", required=True)
    s.add_argument("--first", type=int, default=60)

    r = sub.add_parser("read", help="Read full normalized or raw content for a path")
    r.add_argument("--path", required=True)
    args = ap.parse_args(argv or sys.argv[1:])
    if args.cmd == "build":
        sys.exit(_cli_build())
    elif args.cmd == "audit":
        ok, report = _audit(strict=getattr(args, "strict", False))
        print(json.dumps({"ok": ok, **report}, ensure_ascii=False))
        if getattr(args, "strict", False) and not ok:
            sys.exit(2)
    elif args.cmd == "query":
        _cli_query(args.text, args.k, getattr(args, "json", False))
    elif args.cmd == "show":
        _cli_show(args.path, args.first)
    elif args.cmd == "read":
        _cli_read(args.path)

if __name__ == "__main__":
    main()
