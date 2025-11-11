# orchestrator/knowledge.py
from __future__ import annotations
import argparse, json, os, pathlib, re, sys
from typing import Iterable, List, Dict

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

def _cli_query(text: str, k: int) -> None:
    rows = search_segments(text, k=k)
    for idx, r in enumerate(rows, start=1):
        path = r.get("path") or r.get("plain_rel") or ""
        title = r.get("title","")
        print(f"[{idx}] {title}  — {path}")

def _cli_show(path: str, first: int) -> None:
    out = read_source(path)
    if not out:
        print(f"NOT FOUND or unreadable: {path}")
        return
    lines = out.splitlines()[:first]
    print("\n".join(lines))

def main(argv: List[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query")
    q.add_argument("--text", required=True)
    q.add_argument("--k", type=int, default=5)
    s = sub.add_parser("show")
    s.add_argument("--path", required=True)
    s.add_argument("--first", type=int, default=60)
    args = ap.parse_args(argv or sys.argv[1:])
    if args.cmd == "query":
        _cli_query(args.text, args.k)
    elif args.cmd == "show":
        _cli_show(args.path, args.first)

if __name__ == "__main__":
    main()
