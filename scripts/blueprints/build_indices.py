import re, json, os, sys
from pathlib import Path

ROOT = Path(".")
NT_MD = ROOT/"docs/blueprints/NonTech.md"
TD_MD = ROOT/"docs/blueprints/Tech.md"
OUT_NT = ROOT/"docs/blueprints/nt-index.json"
OUT_TD = ROOT/"docs/blueprints/td-index.json"
OUT_TOC = ROOT/"docs/blueprints/toc-cache.json"

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return s

def scan(md_path: Path, id_prefix: str):
    """Return (items, toc) where items = [{id,title,file,anchor,line,level}], toc = {anchor:{file,start,end}}"""
    items, headers = [], []
    if not md_path.exists():
        return items, {}

    with md_path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    # collect headings with line numbers
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m: 
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        # detect explicit IDs like NT-1.2 … in the title if present
        id_match = re.search(rf"\b{id_prefix}-\d+(?:\.\d+)*\b", title, flags=re.IGNORECASE)
        _id = id_match.group(0).upper() if id_match else f"{id_prefix}-auto-{i}"
        anchor = slugify(title) or f"{id_prefix.lower()}-{i}"
        headers.append({"id":_id, "title":title, "line":i, "anchor":anchor, "level":level})

    # compute end lines based on next header of same/higher level
    toc = {}
    for idx, h in enumerate(headers):
        start = h["line"]
        level = h["level"]
        # default to end of file
        end = len(lines)
        for j in range(idx+1, len(headers)):
            if headers[j]["level"] <= level:
                end = headers[j]["line"] - 1
                break
        toc[h["anchor"]] = {"file": str(md_path).replace("\\","/"), "start": start, "end": end}
        items.append({"id": h["id"], "title": h["title"], "file": str(md_path).replace("\\","/"),
                      "anchor": h["anchor"], "line": start, "level": level})
    return items, toc

nt_items, nt_toc = scan(NT_MD, "NT")
td_items, td_toc = scan(TD_MD, "TD")

OUT_NT.write_text(json.dumps(nt_items, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_TD.write_text(json.dumps(td_items, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_TOC.write_text(json.dumps({"nontech": nt_toc, "tech": td_toc}, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Indexed NT={len(nt_items)} TD={len(td_items)} headings.")
