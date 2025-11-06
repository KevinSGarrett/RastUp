from __future__ import annotations
import os, re, csv
from pathlib import Path

MAX_COLS = 8
MAX_WIDTH = 240
RE_TABLE_ROW = re.compile(r'^\s*\|.*\|\s*$')

def table_blocks(lines):
    i=0; n=len(lines)
    while i<n:
        if RE_TABLE_ROW.match(lines[i]):
            start=i
            while i<n and RE_TABLE_ROW.match(lines[i]): i+=1
            yield start, i
        else:
            i+=1

def export_table(rows, csv_path: Path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for r in rows: w.writerow(r)

def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    out=[]; i=0; changed=False
    for start,end in table_blocks(lines):
        while i<start: out.append(lines[i]); i+=1
        block = lines[start:end]
        width=max(len(x) for x in block)
        parsed=[]
        for r in block:
            inner=r.strip().strip("|")
            cols=[c.strip() for c in inner.split("|")]
            parsed.append(cols)
        if max(len(r) for r in parsed)>MAX_COLS or width>MAX_WIDTH:
            csv_name = path.stem + f".table_{start}.csv"
            export_table(parsed, path.parent / csv_name)
            out.append(f"[Table exported to CSV]({csv_name})")
            changed=True; i=end
        else:
            out.extend(block); i=end
    while i<len(lines): out.append(lines[i]); i+=1
    if changed: path.write_text("\n".join(out)+"\n", encoding="utf-8")
    return changed

def main():
    root=Path("docs/blueprints")
    for d in [root/"non-tech", root/"tech"]:
        if not d.exists(): continue
        for p in d.glob("**/*.md"):
            if p.name.endswith("all.md"): continue
            process_file(p)

if __name__=="__main__":
    main()
