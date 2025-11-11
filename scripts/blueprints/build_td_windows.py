import json
from pathlib import Path
from odf.opendocument import load as odf_load
from odf import text as odf_text

ROOT    = Path(".")
TD_SRC  = ROOT/"docs/blueprints/TechnicalDevelopmentPlan.odt"
SECTIONS= ROOT/"docs/blueprints/sections.json"
WINDOW  = 20  # paragraphs per window

def odt_paragraphs(p: Path):
    if not p.exists(): return []
    odt = odf_load(str(p))
    paras=[]
    for pr in odt.getElementsByType(odf_text.P):
        txt="".join(n.data for n in pr.childNodes if n.nodeType==n.TEXT_NODE).strip()
        paras.append(txt)
    return paras

def main():
    # load existing sections and drop any TD entries (leave NT intact)
    current=[]
    if SECTIONS.exists():
        try: current = json.loads(SECTIONS.read_text(encoding="utf-8"))
        except: pass
    current = [s for s in current if s.get("kind") != "TD"]

    paras = odt_paragraphs(TD_SRC)
    nonempty_abs = [i for i,t in enumerate(paras) if t]
    td=[]
    if nonempty_abs:
        idx=0; ordn=0
        while idx < len(nonempty_abs):
            start_abs = nonempty_abs[idx]
            end_abs   = nonempty_abs[min(idx+WINDOW-1, len(nonempty_abs)-1)]
            title = (paras[start_abs] or f"TD window starting at para {start_abs}")[:140]
            ordn += 1
            td.append({
                "kind":"TD","level":2,"title":title,
                "file": str(TD_SRC).replace("\\","/"),
                "para_start": start_abs,     # ABSOLUTE paragraph index in the document
                "para_end":   end_abs,       # ABSOLUTE paragraph index in the document
                "id": f"TD-H2-{ordn:04d}"
            })
            idx += WINDOW

    merged = current + td
    SECTIONS.parent.mkdir(parents=True, exist_ok=True)
    SECTIONS.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"TD windows: {len(td)} → {SECTIONS}")

if __name__ == "__main__":
    main()
