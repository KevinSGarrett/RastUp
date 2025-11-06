from __future__ import annotations
import argparse, os, re, sys
from typing import List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
import assign_ids  # type: ignore

RE_HEADING = re.compile(r"^(#{2,6})\s+(.*)\s*$")
RE_ANCHOR  = re.compile(r'^\s*<a\s+id="([^"]+)"></a>\s*$')

def _read(path:str)->List[str]:
    with open(path,"r",encoding="utf-8") as f:
        return f.read().splitlines()

def _write(path:str, lines:List[str])->None:
    with open(path,"w",encoding="utf-8",newline="\n") as f:
        f.write("\n".join(lines)+("\n" if not lines or lines[-1]!="\n" else ""))

def _parse(lines:List[str])->List[Tuple[int,int,str,Optional[int]]]:
    raw=[]
    for i,l in enumerate(lines):
        m=RE_HEADING.match(l)
        if not m: continue
        lvl=len(m.group(1))
        if 2<=lvl<=4: raw.append((i,lvl,m.group(2).strip()))
    out=[]; stack=[]
    for idx,(ln,lvl,title) in enumerate(raw):
        parent=None
        while stack and stack[-1][1]>=lvl: stack.pop()
        if stack: parent=stack[-1][0]
        out.append([ln,lvl,title,parent]); stack.append((idx,lvl))
    return [(int(a),int(b),str(c),(int(d) if d is not None else None)) for a,b,c,d in out]

def annotate(doc_type:str, md_path:str)->int:
    lines=_read(md_path)
    heads=_parse(lines)
    ord2id=assign_ids.assign_ids_for_doc(doc_type, md_path)
    changed=0
    for ordinal,(ln,lvl,title,parent) in reversed(list(enumerate(heads))):
        sec_id=ord2id.get(ordinal); 
        if not sec_id: continue
        insert_at=ln
        if insert_at>0 and RE_ANCHOR.match(lines[insert_at-1]):
            m=RE_ANCHOR.match(lines[insert_at-1])
            if m and m.group(1)!=sec_id:
                lines[insert_at-1]=f'<a id="{sec_id}"></a>'; changed+=1
        else:
            lines.insert(insert_at, f'<a id="{sec_id}"></a>'); changed+=1
    if changed: _write(md_path,lines)
    print(f"[annotate_inplace] {doc_type} anchors inserted/updated: {changed}")
    return changed

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nt",help="Path to NT-all.md")
    ap.add_argument("--td",help="Path to TD-all.md")
    a=ap.parse_args()
    if not a.nt and not a.td: ap.error("Provide --nt and/or --td.")
    if a.nt: annotate("NT", a.nt)
    if a.td: annotate("TD", a.td)

if __name__=="__main__":
    main()
