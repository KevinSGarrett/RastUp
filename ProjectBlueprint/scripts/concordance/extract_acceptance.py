from __future__ import annotations
import os, re, json
from pathlib import Path

ACC_RE = re.compile(r'^\s*#{1,6}\s+(Acceptance|Acceptance Criteria|Criteria|Success Metrics)\b', re.I)
GWT_RE = re.compile(r'^\s*(Given|When|Then|And|But)\b', re.I)
MUST_RE = re.compile(r'\b(must|shall|should|required|acceptable)\b', re.I)

def extract_blocks(text: str) -> list[str]:
    lines=text.splitlines()
    i=0; n=len(lines); out=[]
    while i<n:
        if ACC_RE.match(lines[i]):
            j=i+1; buff=[]
            while j<n and not lines[j].startswith('#'):
                buff.append(lines[j]); j+=1
            cand='\n'.join(buff).strip()
            if cand: out.append(cand)
            i=j
        else:
            i+=1
    if not out:
        g=[]
        for ln in lines:
            if GWT_RE.match(ln) or ('- ' in ln and MUST_RE.search(ln)):
                g.append(ln)
        if g: out.append('\n'.join(g))
    return out

def main():
    repo=Path('.'); nontech=repo/'docs'/'blueprints'/'non-tech'
    acc_dir=repo/'docs'/'blueprints'/'acceptance'; acc_dir.mkdir(parents=True,exist_ok=True)
    coverage={'nt_total':0,'nt_with_criteria':0,'ids':[]}
    for p in nontech.glob('**/*.md'):
        if p.name.endswith('all.md'): continue
        text=p.read_text(encoding='utf-8',errors='ignore')
        m=re.search(r'<a id="([^"]+)"></a>', text)
        if not m: continue
        _id=m.group(1)
        coverage['ids'].append(_id)
        coverage['nt_total']+=1
        blocks=extract_blocks(text)
        out = acc_dir/f"{_id}.md"
        if blocks:
            coverage['nt_with_criteria']+=1
            body = "\n\n---\n\n".join([f"`\n{b}\n`" for b in blocks])
        else:
            body = "_No explicit acceptance criteria detected in source — stub generated._\n\n- [ ] Define Given/When/Then for this section.\n"
        out.write_text(f"# Acceptance — {_id}\n\n{body}\n", encoding='utf-8')
    (repo/'docs'/'reports'/'blueprint-coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
