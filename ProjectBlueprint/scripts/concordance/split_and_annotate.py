from __future__ import annotations
import argparse, datetime as dt, hashlib, os, re, sys
from typing import Dict, List, Optional, Tuple

# Import sibling module plainly (no importlib.exec_module)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
import assign_ids  # type: ignore

RE_HEADING = re.compile(r"^(#{2,6})\s+(.*)\s*$")

def _read(path: str) -> List[str]:
    with open(path,"r",encoding="utf-8") as f:
        return f.read().splitlines()

def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8",newline="\n") as f:
        f.write(text)

def _parse(lines: List[str]) -> List[Tuple[int,int,str,int,int,Optional[int]]]:
    raw=[]
    for i,l in enumerate(lines):
        m=RE_HEADING.match(l)
        if not m: continue
        lvl=len(m.group(1))
        if 2<=lvl<=4: raw.append((i,lvl,m.group(2).strip()))
    out=[]
    for idx,(ln,lvl,title) in enumerate(raw):
        end=raw[idx+1][0] if idx+1<len(raw) else len(lines)
        out.append([idx,lvl,title,ln,end,None])
    stack=[]
    for j,item in enumerate(out):
        _,lvl,_,_,_,_=item
        while stack and stack[-1][1]>=lvl: stack.pop()
        parent=stack[-1][0] if stack else None
        item[5]=parent
        stack.append((j,lvl))
    return [(int(a),int(b),str(c),int(d),int(e),(int(f) if f is not None else None)) for a,b,c,d,e,f in out]

def _slug(s: str) -> str:
    s=re.sub(r"[^a-zA-Z0-9\s\-]+","",s).strip().lower()
    return re.sub(r"\s+","-",s)[:80] or "section"

def _sha(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()

def _yaml(meta: Dict[str,str]) -> str:
    def yv(v):
        if v is None or v=="":
            return "null"
        s=str(v)
        if re.search(r'[:#\-\n"]', s):
            s=s.replace('"','\\"')
            return f'\"{s}\"'
        return s
    keys=("id","title","parent","source","path","checksum","last_modified")
    return "---\n" + "\n".join(f"{k}: {yv(meta.get(k,''))}" for k in keys) + "\n---\n"

def split_one(doc_type: str, all_md_path: str, source_docx: str, out_dir: str, log_path: str) -> None:
    lines=_read(all_md_path)
    heads=_parse(lines)
    idx_to_id=assign_ids.assign_ids_for_doc(doc_type, all_md_path)

    created=[]
    now=dt.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"

    for idx,lvl,title,start,end,parent in heads:
        if lvl not in (2,3): continue
        sec_id=idx_to_id[idx]
        parent_id=idx_to_id.get(parent) if parent is not None else ""
        slug=_slug(title)
        rel=os.path.join(out_dir, f"{sec_id}--{slug}.md").replace("\\","/")
        anchor=f'<a id="{sec_id}"></a>'
        body="\n".join(lines[start:end]).rstrip()+"\n"
        body_for_checksum="\n".join(lines[start+1:end])
        meta={"id":sec_id,"title":title,"parent":(parent_id or ""), "source":source_docx,
              "path":rel,"checksum":_sha(body_for_checksum),"last_modified":now}
        _write(rel, _yaml(meta)+anchor+"\n"+body)
        created.append(rel)

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path,"w",encoding="utf-8") as f:
        for p in created:
            f.write(f"CREATED {p}\n")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nt",help="Path to NT-all.md")
    ap.add_argument("--td",help="Path to TD-all.md")
    ap.add_argument("--source-docx",required=True,help="Original DOCX path recorded in front-matter")
    a=ap.parse_args()
    if not a.nt and not a.td:
        ap.error("Provide --nt and/or --td.")
    if a.nt:
        split_one("NT", a.nt, a.source_docx, out_dir=os.path.join("docs","blueprints","non-tech"), log_path=os.path.join("docs","reports","split-nt.log"))
        print("[split_and_annotate] NT split complete.")
    if a.td:
        split_one("TD", a.td, a.source_docx, out_dir=os.path.join("docs","blueprints","tech"), log_path=os.path.join("docs","reports","split-td.log"))
        print("[split_and_annotate] TD split complete.")

if __name__=="__main__":
    main()
