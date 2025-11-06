from __future__ import annotations
import argparse, hashlib, json, os, re, sys, time
from typing import Dict, List, Optional, Tuple

# Simple, robust ID map stored at repo root (current working directory)
ID_MAP_FILE = os.path.join(os.getcwd(), "id_map.json")
RE_HEADING = re.compile(r"^(#{2,6})\s+(.*)\s*$")

def _read_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def _parse_headings(lines: List[str]) -> List[Tuple[int,int,str,int,int,Optional[int]]]:
    raw = []
    for i, line in enumerate(lines):
        m = RE_HEADING.match(line)
        if not m: continue
        lvl = len(m.group(1))
        if 2 <= lvl <= 4:
            raw.append((i,lvl,m.group(2).strip()))
    out = []
    for idx,(ln,lvl,title) in enumerate(raw):
        end = raw[idx+1][0] if idx+1 < len(raw) else len(lines)
        out.append([idx,lvl,title,ln,end,None])
    stack: List[Tuple[int,int]] = []
    for j,item in enumerate(out):
        _,lvl,_,_,_,_ = item
        while stack and stack[-1][1] >= lvl:
            stack.pop()
        parent_idx = stack[-1][0] if stack else None
        item[5] = parent_idx
        stack.append((j,lvl))
    return [(int(a),int(b),str(c),int(d),int(e),(int(f) if f is not None else None)) for a,b,c,d,e,f in out]

def _norm_body(lines: List[str], start: int, end: int) -> str:
    body = "\n".join(lines[start+1:end])
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"[^]*", "", body)
    body = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", body)
    body = re.sub(r"\s+", "", body)
    return body[:20000]

def _fp(doc_type: str, level: int, title: str, body_norm: str, doc_path: str) -> str:
    base = f"{doc_type}|L{level}|{re.sub(r'\s+',' ',title).strip().lower()}|{body_norm}|{doc_path.replace('\\\\','/')}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()

def _load_map() -> Dict[str,dict]:
    if not os.path.exists(ID_MAP_FILE): return {}
    with open(ID_MAP_FILE,"r",encoding="utf-8") as f:
        return json.load(f)

def _save_map(m: Dict[str,dict]) -> None:
    with open(ID_MAP_FILE,"w",encoding="utf-8") as f:
        json.dump(m,f,indent=2,ensure_ascii=False,sort_keys=True)

def _next_h2(existing: List[str], prefix: str) -> int:
    mx = 0
    for i in existing:
        if not i.startswith(prefix+"-"): continue
        suf = i[len(prefix)+1:]
        top = suf.split(".")[0]
        try: mx = max(mx,int(top))
        except: pass
    return mx+1

def _next_child(existing: List[str], parent_id: str) -> int:
    mx = 0
    pref = parent_id+"."
    for i in existing:
        if not i.startswith(pref): continue
        rest = i[len(pref):]
        first = rest.split(".")[0]
        try: mx = max(mx,int(first))
        except: pass
    return mx+1

def _alloc(existing: List[str], doc_type: str, level: int, parent_id: Optional[str]) -> str:
    prefix = "NT" if doc_type.upper()=="NT" else "TD"
    if level==2:
        return f"{prefix}-{_next_h2(existing,prefix)}"
    if level==3:
        if not parent_id:
            h2s=[i for i in existing if i.startswith(prefix+"-") and "." not in i]
            parent_id = h2s[-1] if h2s else f"{prefix}-1"
        return f"{parent_id}.{_next_child(existing,parent_id)}"
    # level==4
    if not parent_id:
        h3s=[i for i in existing if i.startswith(prefix+"-") and i.count(".")==1]
        if h3s: parent_id=h3s[-1]
        else:
            h2s=[i for i in existing if i.startswith(prefix+"-") and "." not in i]
            parent_id=h2s[-1] if h2s else f"{prefix}-1"
    return f"{parent_id}.{_next_child(existing,parent_id)}"

def assign_ids_for_doc(doc_type: str, md_path: str) -> Dict[int,str]:
    lines = _read_lines(md_path)
    heads = _parse_headings(lines)
    id_map = _load_map()
    existing = [v["id"] for v in id_map.values() if v.get("doc_type")==doc_type.upper()]
    idx_to_id: Dict[int,str] = {}
    for idx,lvl,title,start,end,parent in heads:
        body_norm=_norm_body(lines,start,end)
        fp=_fp(doc_type,lvl,title,body_norm,md_path)
        if fp in id_map:
            idx_to_id[idx]=id_map[fp]["id"]
            id_map[fp].update({"title":title,"level":lvl,"parent_guess":(idx_to_id.get(parent) if parent is not None else None),"source":md_path,"last_seen":int(time.time())})
            continue
        parent_id = idx_to_id.get(parent) if parent is not None else None
        new_id = _alloc(existing,doc_type,lvl,parent_id)
        existing.append(new_id)
        idx_to_id[idx]=new_id
        id_map[fp]={"id":new_id,"doc_type":doc_type.upper(),"level":lvl,"parent_guess":parent_id,"title":title,"source":md_path,"first_seen":int(time.time()),"last_seen":int(time.time())}
    _save_map(id_map)
    return idx_to_id

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--nt",help="Path to NT-all.md")
    ap.add_argument("--td",help="Path to TD-all.md")
    a=ap.parse_args()
    if not a.nt and not a.td: ap.error("Provide --nt and/or --td.")
    if a.nt:
        assign_ids_for_doc("NT",a.nt)
        print(f"[assign_ids] NT mapping updated for {a.nt}")
    if a.td:
        assign_ids_for_doc("TD",a.td)
        print(f"[assign_ids] TD mapping updated for {a.td}")

if __name__=="__main__":
    main()
