from __future__ import annotations
import json, os, re, hashlib
from pathlib import Path
from typing import Dict

FM_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
TITLE_RE = re.compile(r'^\s*title:\s*"(.*)"\s*$', re.M)
ID_LINE_RE = re.compile(r'^\s*id:\s*([A-Z]+-[0-9.]+)\s*$', re.M)
PARENT_RE = re.compile(r'^\s*parent_id:\s*([A-Z]+-[0-9.]+)?\s*$', re.M)

def sha256(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

def parse_fm(text: str) -> dict:
    m=FM_RE.match(text)
    if not m: return {}
    block=m.group(1)
    # minimal parse: id, title, parent_id
    fm={}
    mid=ID_LINE_RE.search(block)
    if mid: fm['id']=mid.group(1)
    mt=TITLE_RE.search(block)
    if mt: fm['title']=mt.group(1)
    mp=PARENT_RE.search(block)
    if mp: fm['parent_id']=(mp.group(1) or "")
    return fm

def main():
    repo=Path('.'); bp=repo/'docs'/'blueprints'
    nt_dir=bp/'non-tech'; td_dir=bp/'tech'
    nt_map: Dict[str,dict]={}; td_map: Dict[str,dict]={}

    def scan_dir(d: Path):
        out={}
        for p in d.glob('**/*.md'):
            if p.name.endswith('all.md'): continue
            t=p.read_text(encoding='utf-8',errors='ignore')
            fm=parse_fm(t)
            # id fallback from anchor
            _id=fm.get('id')
            if not _id:
                ma=ANCHOR_RE.search(t)
                _id=ma.group(1) if ma else None
            if not _id: continue
            # title fallback from first heading if needed
            title=fm.get('title') or ''
            if not title:
                mh=re.search(r'^(#{2,6})\s+(.*)\s*$', t, re.M)
                if mh: title=mh.group(2)
            body = re.sub(r'^---\n.*?\n---\n','',t,flags=re.S)
            out[_id]={
                "title": title,
                "path": p.as_posix(),
                "anchor": _id,
                "parent": fm.get("parent_id",""),
                "checksum": sha256(body)
            }
        return out

    if nt_dir.exists(): nt_map=scan_dir(nt_dir)
    if td_dir.exists(): td_map=scan_dir(td_dir)
    (bp/'nt-index.json').write_text(json.dumps(nt_map,indent=2,ensure_ascii=False),encoding='utf-8')
    (bp/'td-index.json').write_text(json.dumps(td_map,indent=2,ensure_ascii=False),encoding='utf-8')

    # Build a simple tree
    def build_tree(ix: dict):
        nodes={k:{"id":k,"title":v.get("title",""),"path":v["path"],"anchor":k,"children":[]} for k,v in ix.items()}
        for k,v in ix.items():
            parent=v.get("parent")
            if parent and parent in nodes:
                nodes[parent]["children"].append(nodes[k])
        roots=[nodes[k] for k,v in ix.items() if not v.get("parent")]
        return roots
    toc={"NT": build_tree(nt_map), "TD": build_tree(td_map)}
    (bp/'toc-cache.json').write_text(json.dumps(toc,indent=2,ensure_ascii=False),encoding='utf-8')

if __name__=="__main__":
    main()
