from __future__ import annotations
import os, re, json
from pathlib import Path
from typing import List, Tuple

FM_RE    = re.compile(r'^---\n.*?\n---\n', re.S)   # front-matter block
RE_ID    = re.compile(r'\b(NT|TD)-\d+(?:\.\d+)*\b')
RE_SEC   = re.compile(r'(?:see|refer to|§)\s*(\d+(?:\.\d+){0,2})', re.I)
RE_TITLE = re.compile(r'see\s+“([^”]+)”|see\s+"([^"]+)"', re.I)

# Regions to protect from ANY rewriting:
RE_MD_LINK   = re.compile(r'\[[^\]]*?\]\([^)]+?\)')          # [text](target)
RE_HTML_ANCH = re.compile(r'<a\s+id="[^"]*"\s*></a>', re.I)  # <a id="..."></a>
RE_CODEFENCE = re.compile(r'`.*?`', re.S)                # fenced code blocks

def load_index(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def number_to_id(index_map: dict, num: str) -> str|None:
    q=num.lower()
    for _id,meta in index_map.items():
        t=(meta.get("title") or "").lower()
        if t.startswith(f"section {q}") or t.startswith(f"subsection {q}"): 
            return _id
    return None

def title_to_id(index_map: dict, title: str) -> str|None:
    t=title.strip().lower()
    # exact match first
    for _id,meta in index_map.items():
        mt=(meta.get("title") or "").lower()
        if t==mt: return _id
    # then contains
    best=None; bestlen=10**9
    for _id,meta in index_map.items():
        mt=(meta.get("title") or "").lower()
        if t in mt and len(mt)<bestlen:
            best=_id; bestlen=len(mt)
    return best

def link_to(path: Path, idx_map: dict, target_id: str) -> str|None:
    meta = idx_map.get(target_id)
    if not meta: return None
    rel = os.path.relpath(meta["path"], start=path.parent).replace("\\","/")
    return f"[see {target_id}]({rel}#{target_id})"

def _mask(text: str) -> Tuple[str, List[str]]:
    """Replace protected regions with placeholders \x01{n}\x02 and return (masked, stash)."""
    stash: List[str] = []
    def _do_mask(regex: re.Pattern, s: str) -> str:
        pos = 0
        out = []
        for m in regex.finditer(s):
            out.append(s[pos:m.start()])
            placeholder = f"\x01{len(stash)}\x02"
            stash.append(m.group(0))
            out.append(placeholder)
            pos = m.end()
        out.append(s[pos:])
        return "".join(out)

    masked = text
    for rx in (RE_CODEFENCE, RE_MD_LINK, RE_HTML_ANCH):
        masked = _do_mask(rx, masked)
    return masked, stash

def _unmask(text: str, stash: List[str]) -> str:
    def restore(m):
        idx = int(m.group(1))
        return stash[idx]
    return re.sub(r"\x01(\d+)\x02", restore, text)

def rewrite_body(p: Path, body: str, idx: dict, log: dict) -> str:
    # mask protected regions
    masked, stash = _mask(body)
    orig_masked = masked

    # Direct IDs (avoid doubling; links already masked)
    def r_id(m):
        s = m.group(0)
        ln = link_to(p, idx, s)
        if ln: return ln
        log.setdefault("unresolved_ids", []).append({"file":str(p),"id":s})
        return s
    masked = RE_ID.sub(r_id, masked)

    # Numeric sections
    def r_sec(m):
        num=m.group(1)
        mapped=number_to_id(idx, num)
        if mapped:
            ln=link_to(p,idx,mapped)
            return ln or m.group(0)
        log.setdefault("unresolved_numbers", []).append({"file":str(p),"number":num})
        return m.group(0)
    masked = RE_SEC.sub(r_sec, masked)

    # Title references
    def r_title(m):
        title=m.group(1) or m.group(2) or ""
        mapped=title_to_id(idx,title)
        if mapped:
            ln=link_to(p,idx,mapped)
            return ln or m.group(0)
        log.setdefault("unresolved_titles", []).append({"file":str(p),"title":title})
        return m.group(0)
    masked = RE_TITLE.sub(r_title, masked)

    if masked == orig_masked:
        return body
    return _unmask(masked, stash)

def process_dir(dirpath: Path, idx: dict, log: dict):
    for p in dirpath.glob("**/*.md"):
        if p.name.endswith("all.md"): 
            continue
        t = p.read_text(encoding='utf-8',errors='ignore')

        # Split into FM + body; only rewrite body
        fm_match = FM_RE.match(t)
        if fm_match:
            fm = fm_match.group(0)
            body = t[len(fm):]
            new_body = rewrite_body(p, body, idx, log)
            if new_body != body:
                p.write_text(fm + new_body, encoding='utf-8')
        else:
            new_t = rewrite_body(p, t, idx, log)
            if new_t != t:
                p.write_text(new_t, encoding='utf-8')

def main():
    root=Path("."); reports=root/"docs"/"reports"; reports.mkdir(parents=True,exist_ok=True)
    nt_idx=load_index(root/"docs"/"blueprints"/"nt-index.json")
    td_idx=load_index(root/"docs"/"blueprints"/"td-index.json")
    log={"unresolved_ids":[],"unresolved_numbers":[],"unresolved_titles":[]}
    nt_dir = root/"docs"/"blueprints"/"non-tech"
    td_dir = root/"docs"/"blueprints"/"tech"
    if nt_dir.exists(): process_dir(nt_dir, nt_idx, log)
    if td_dir.exists(): process_dir(td_dir, td_idx, log)
    (reports/"xref-resolutions.json").write_text(json.dumps(log,indent=2),encoding="utf-8")

if __name__=="__main__":
    main()
