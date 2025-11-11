import re, json, unicodedata
from pathlib import Path
from docx import Document
from odf.opendocument import load as odf_load
from odf import text as odf_text

ROOT = Path(".")
NT_SRC = ROOT/"docs/blueprints/Combined_Master_PLAIN_Non_Tech_001.docx"
TD_SRC = ROOT/"docs/blueprints/TechnicalDevelopmentPlan.odt"
OUT_SECTIONS = ROOT/"docs/blueprints/sections.json"

PAT_SUBSECTION = re.compile(r'^(?:Sub)?Section\s+(\d+(?:\.\d+)*)\b', re.IGNORECASE)
PAT_NUMBERED   = re.compile(r'^\s*(\d+)\)\s+')

def ascii_title(s:str)->str:
    if not s: return ""
    t = unicodedata.normalize("NFKC", s)
    t = (t.replace("“","\"").replace("”","\"").replace("‘","'").replace("’","'").replace("—","-").replace("–","-"))
    return " ".join(t.split())

def docx_sections(p: Path):
    if not p.exists(): return []
    doc = Document(str(p))
    paras = [("P", (getattr(pr.style,"name","") or ""), pr.text.strip()) for pr in doc.paragraphs]
    sections=[]; idx=0
    while idx < len(paras):
        tag, style, text = paras[idx]
        lvl=None
        if style.lower().startswith("heading"):
            try: lvl=int(style.split()[-1])
            except: lvl=2
        if not lvl and text:
            if PAT_SUBSECTION.match(text): lvl=2
            elif PAT_NUMBERED.match(text): lvl=2
        if lvl:
            # start range
            start = idx
            # advance to next header (same or higher)
            j = idx + 1
            while j < len(paras):
                tag2, style2, text2 = paras[j]
                next_is_header = style2.lower().startswith("heading") or PAT_SUBSECTION.match(text2) or PAT_NUMBERED.match(text2)
                if next_is_header: break
                j += 1
            end = max(start, j-1)
            sections.append({
                "kind":"NT","level":lvl,"title":ascii_title(text),
                "file":str(p).replace("\\","/"),
                "para_start":start,"para_end":end,
                "id": None  # fill later
            })
            idx = j; continue
        idx += 1
    # assign stable IDs
    counters={1:0,2:0,3:0,4:0,5:0,6:0}
    for s in sections:
        lvl=s["level"]; counters[lvl]+=1
        s["id"]=f"NT-H{lvl}-{counters[lvl]:04d}"
    return sections

def odt_sections(p: Path):
    if not p.exists(): return []
    odt = odf_load(str(p))
    # flatten as (tag, text)
    blocks=[]
    for h in odt.getElementsByType(odf_text.H):
        txt="".join(n.data for n in h.childNodes if n.nodeType==n.TEXT_NODE).strip()
        blocks.append(("H", txt))
    for pr in odt.getElementsByType(odf_text.P):
        txt="".join(n.data for n in pr.childNodes if n.nodeType==n.TEXT_NODE).strip()
        blocks.append(("P", txt))
    # build sections: each H → following Ps until next H
    sections=[]; i=0; hcounts={}
    while i < len(blocks):
        tag, text = blocks[i]
        if tag=="H" and text:
            lvl=2  # ODT outline levels are unreliable across editors — normalize to H2 for parity
            start=i+1
            j=start
            while j < len(blocks) and blocks[j][0]!="H":
                j+=1
            # map heading range to the paragraph indices among Ps only
            # rebuild a paragraph-only list
            para_indices=[k for k,(t,_) in enumerate(blocks) if t=="P"]
            # find absolute P positions bounding start..j
            # locate first P at/after start
            ps=[k for k in para_indices if k>=start and k<j]
            if ps:
                pstart = para_indices.index(ps[0])
                pend   = para_indices.index(ps[-1])
            else:
                # empty section: map to zero-length window after heading
                ponly=[(k,txt) for k,(t,txt) in enumerate(blocks) if t=="P"]
                pstart=0; pend=min(len(ponly)-1,0)
            hcounts[lvl]=hcounts.get(lvl,0)+1
            sid=f"TD-H{lvl}-{hcounts[lvl]:04d}"
            sections.append({
                "kind":"TD","level":lvl,"title":ascii_title(text),
                "file":str(p).replace("\\","/"),
                "para_start":pstart,"para_end":pend,"id":sid
            })
            i=j; continue
        i+=1
    return sections

def main():
    out=[]
    out += docx_sections(NT_SRC)
    out += odt_sections(TD_SRC)
    OUT_SECTIONS.parent.mkdir(parents=True, exist_ok=True)
    OUT_SECTIONS.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Sections written: {len(out)} → {OUT_SECTIONS}")

if __name__ == "__main__":
    main()
