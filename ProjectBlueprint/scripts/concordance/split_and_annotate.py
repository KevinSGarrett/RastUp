from __future__ import annotations
import argparse, datetime as dt, hashlib, os, re, sys
from typing import Dict, List, Tuple, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path: sys.path.insert(0, SCRIPT_DIR)
import assign_ids  # type: ignore

RE_HEADING = re.compile(r"^(#{2,6})\s+(.*)\s*$")

def _read(path: str) -> List[str]:
    with open(path,"r",encoding="utf-8") as f: return f.read().splitlines()

def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8",newline="\n") as f: f.write(text)

def _parse(lines: List[str]) -> List[Tuple[int,int,str,int,int,Optional[int]]]:
    raw=[]; out=[]
    for i,l in enumerate(lines):
        m=RE_HEADING.match(l)
        if not m: continue
        lvl=len(m.group(1))
        if 2<=lvl<=4: raw.append((i,lvl,m.group(2).strip()))
    for idx,(ln,lvl,title) in enumerate(raw):
        end=raw[idx+1][0] if idx+1<len(raw) else len(lines)
        out.append([idx,lvl,title,ln,end,None])
    stack=[]
    for j,item in enumerate(out):
        _,lvl,_,_,_,_=item
        while stack and stack[-1][1]>=lvl: stack.pop()
        parent=stack[-1][0] if stack else None
        item[5]=parent; stack.append((j,lvl))
    return [(int(a),int(b),str(c),int(d),int(e),(int(f) if f is not None else None)) for a,b,c,d,e,f in out]

def _slug(s: str) -> str:
    import re
    s=re.sub(r"[^a-zA-Z0-9\s\-]+","",s).strip().lower()
    return re.sub(r"\s+","-",s)[:80] or "section"

def _sha256(text: str) -> str:
    import hashlib
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

def split(doc_type: str, all_md_path: str, out_root: str, source_docx: str) -> List[str]:
    lines=_read(all_md_path)
    heads=_parse(lines)
    ord2id=assign_ids.assign_ids_for_doc(doc_type, all_md_path)
    written=[]
    now=dt.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
    src_doc = "NonTechBlueprint.docx" if doc_type=="NT" else "TechDevBlueprint.docx"

    out_dir = os.path.join(out_root, "non-tech" if doc_type=="NT" else "tech")

    def h2_folder(h2_id: str, title: str) -> str:
        h2_num = h2_id.split("-")[1].split(".")[0]
        prefix = "NT" if doc_type=="NT" else "TD"
        return f"{prefix}-{int(h2_num):02d}-{_slug(title)}"

    nodes=[]
    for ord,lvl,title,start,end,parent in heads:
        sid=ord2id[ord]
        pid=ord2id.get(parent) if parent is not None else None
        nodes.append((sid,lvl,title,start,end,pid))

    for i,(sid,lvl,title,start,end,pid) in enumerate(nodes):
        if lvl!=2: continue
        h2_id=sid; h2_title=title; h2_start=start; h2_end=end
        folder=os.path.join(out_dir, h2_folder(h2_id,h2_title))
        os.makedirs(folder, exist_ok=True)

        children=[(sid2,lvl2,title2,s2,e2,pid2)
                  for sid2,lvl2,title2,s2,e2,pid2 in nodes
                  if lvl2==3 and pid2==h2_id]

        if not children:
            body="\n".join(lines[h2_start:h2_end]).rstrip()+"\n"
            body_only="\n".join(lines[h2_start+1:h2_end])
            fname=f"{h2_id}-overview.md"
            path=os.path.join(folder,fname)
            ctitle = h2_title.replace('"','\\"')
            fm=(f"---\n"
                f"id: {h2_id}\n"
                f"title: \"{ctitle}\"\n"
                f"source_doc: \"{src_doc}\"\n"
                f"source_path: \"{path.replace('\\\\','/')}\"\n"
                f"parent_id: \n"
                f"anchor: \"{h2_id}\"\n"
                f"checksum: \"{_sha256(body_only)}\"\n"
                f"last_modified: \"{now}\"\n"
                f"doc_kind: \"{doc_type}\"\n"
                f"h_level: 2\n"
                f"---\n"
                f"<a id=\"{h2_id}\"></a>\n")
            _write(path, fm+body); written.append(path)
        else:
            # H2 overview with links to children
            overview_lines=["### Overview","","This H2 is split into the following H3 parts:",""]
            for (cid,_,ctitle,_,_,_) in children:
                child_slug=_slug(ctitle)
                cfname=f"{cid}-{child_slug}.md"
                overview_lines.append(f"- [{ctitle}]({cfname}#{cid})")
            overview_text="\n".join(overview_lines) + "\n"
            fname=f"{h2_id}-overview.md"; path=os.path.join(folder,fname)
            ctitle = h2_title.replace('"','\\"')
            fm=(f"---\n"
                f"id: {h2_id}\n"
                f"title: \"{ctitle}\"\n"
                f"source_doc: \"{src_doc}\"\n"
                f"source_path: \"{path.replace('\\\\','/')}\"\n"
                f"parent_id: \n"
                f"anchor: \"{h2_id}\"\n"
                f"checksum: \"{_sha256(overview_text)}\"\n"
                f"last_modified: \"{now}\"\n"
                f"doc_kind: \"{doc_type}\"\n"
                f"h_level: 2\n"
                f"---\n"
                f"<a id=\"{h2_id}\"></a>\n")
            _write(path, fm+overview_text); written.append(path)

            for (cid,_,ctitle,s2,e2,_) in children:
                body="\n".join(lines[s2:e2]).rstrip()+"\n"
                body_only="\n".join(lines[s2+1:e2])
                cf=f"{cid}-{_slug(ctitle)}.md"
                cpath=os.path.join(folder,cf)
                ctitle_q = ctitle.replace('"','\\"')
                cfm=(f"---\n"
                     f"id: {cid}\n"
                     f"title: \"{ctitle_q}\"\n"
                     f"source_doc: \"{src_doc}\"\n"
                     f"source_path: \"{cpath.replace('\\\\','/')}\"\n"
                     f"parent_id: {h2_id}\n"
                     f"anchor: \"{cid}\"\n"
                     f"checksum: \"{_sha256(body_only)}\"\n"
                     f"last_modified: \"{now}\"\n"
                     f"doc_kind: \"{doc_type}\"\n"
                     f"h_level: 3\n"
                     f"---\n"
                     f"<a id=\"{cid}\"></a>\n")
                _write(cpath, cfm+body); written.append(cpath)

    with open(os.path.join("docs","reports","split.log"),"w",encoding="utf-8") as f:
        for p in written: f.write(p.replace("\\","/")+"\n")
    return written

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nt",help="Path to NT-all.md")
    ap.add_argument("--td",help="Path to TD-all.md")
    ap.add_argument("--out-root",default=os.path.join("docs","blueprints"))
    ap.add_argument("--source-docx",default="docs/blueprints/raw/NonTechBlueprint.docx")
    a=ap.parse_args()
    if not a.nt and not a.td: ap.error("Provide --nt and/or --td.")
    if a.nt: split("NT", a.nt, a.out_root, a.source_docx)
    if a.td: split("TD", a.td, a.out_root, a.source_docx)

if __name__=="__main__":
    main()
