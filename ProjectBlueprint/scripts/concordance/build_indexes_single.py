from __future__ import annotations
import json, os, re, sys
from typing import List, Optional, Tuple, Dict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
import assign_ids  # type: ignore

RE_HEADING = re.compile(r'^(#{2,6})\s+(.*)\s*$')

def _read(p:str)->List[str]:
    with open(p,'r',encoding='utf-8') as f: return f.read().splitlines()

def _parse(lines:List[str])->List[Tuple[int,int,str,int,int,Optional[int]]]:
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
        item[5]=parent; stack.append((j,lvl))
    return [(int(a),int(b),str(c),int(d),int(e),(int(f) if f is not None else None)) for a,b,c,d,e,f in out]

def _build(doc_type:str, md_path:str):
    lines=_read(md_path)
    heads=_parse(lines)
    ord2id=assign_ids.assign_ids_for_doc(doc_type, md_path)
    rel=md_path.replace("\\","/")
    flat: Dict[str,Dict[str,str]]={}
    line_idx: Dict[str,Dict[str,int]]={}
    nodes={}
    roots=[]
    for ord,lvl,title,start,end,parent in heads:
        sid=ord2id[ord]; pid=ord2id.get(parent) if parent is not None else None
        flat[sid]={"title":title,"path":rel,"anchor":sid,"parent":pid or ""}
        line_idx[sid]={"path":rel,"start_line":start,"end_line":end,"level":lvl}
        node={"id":sid,"title":title,"path":rel,"anchor":sid,"children":[]}; nodes[sid]=node
        if pid:
            nodes.setdefault(pid,{"id":pid,"title":"","path":rel,"anchor":pid,"children":[]})
            nodes[pid]["children"].append(node)
        else:
            roots.append(node)
    return flat, {"tree": roots}, line_idx

def main():
    base=os.path.join("docs","blueprints"); os.makedirs(base,exist_ok=True)
    nt_md=os.path.join("docs","blueprints","non-tech","NT-all.md")
    td_md=os.path.join("docs","blueprints","tech","TD-all.md")
    nt_flat,nt_toc,nt_lines=({},{},{}); td_flat,td_toc,td_lines=({},{},{})

    if os.path.exists(nt_md): nt_flat,nt_toc,nt_lines=_build("NT",nt_md)
    if os.path.exists(td_md): td_flat,td_toc,td_lines=_build("TD",td_md)

    with open(os.path.join(base,"nt-index.json"),"w",encoding="utf-8") as f: json.dump(nt_flat,f,indent=2,ensure_ascii=False)
    with open(os.path.join(base,"td-index.json"),"w",encoding="utf-8") as f: json.dump(td_flat,f,indent=2,ensure_ascii=False)
    with open(os.path.join(base,"toc-cache.json"),"w",encoding="utf-8") as f: json.dump({"NT": nt_toc.get("tree",[]), "TD": td_toc.get("tree",[])},f,indent=2,ensure_ascii=False)
    with open(os.path.join(base,"nt-line-index.json"),"w",encoding="utf-8") as f: json.dump(nt_lines,f,indent=2,ensure_ascii=False)
    with open(os.path.join(base,"td-line-index.json"),"w",encoding="utf-8") as f: json.dump(td_lines,f,indent=2,ensure_ascii=False)
    print(f"[build_indexes_single] NT={len(nt_flat)} TD={len(td_flat)}")

if __name__=="__main__":
    main()
