import re, json
from pathlib import Path
from docx import Document
from odf.opendocument import load as odf_load
from odf import text

ROOT = Path(".")
NT_SRC = ROOT/"docs/blueprints/Combined_Master_PLAIN_Non_Tech_001.docx"
TD_SRC = ROOT/"docs/blueprints/TechnicalDevelopmentPlan.odt"
OUT_NT = ROOT/"docs/blueprints/nt-index.json"
OUT_TD = ROOT/"docs/blueprints/td-index.json"
OUT_TOC = ROOT/"docs/blueprints/toc-cache.json"

ID_NT = re.compile(r"^(NT-\d+(?:\.\d+)*)\b")
ID_TD = re.compile(r"^(TD-\d+(?:\.\d+)*)\b")

def read_docx_paras(p: Path):
    doc = Document(str(p))
    return [pr.text.strip() for pr in doc.paragraphs]

def read_odt_paras(p: Path):
    odt = odf_load(str(p))
    paras = []
    for ptag in odt.getElementsByType(text.P):
        s = "".join(node.data for node in ptag.childNodes if node.nodeType == node.TEXT_NODE).strip()
        paras.append(s)
    return paras

def index_from_paras(paras, id_regex, source_file):
    items=[]   # [{id,title,para,line_start,line_end}]
    toc={}     # id -> {file, start, end}
    # detect IDs by paragraph leading token
    id_positions=[]
    for i, line in enumerate(paras):
        m = id_regex.match(line)
        if m:
            id_positions.append((m.group(1), i, line))
    # build ranges (next id start - 1); if only one, range to EOF
    for idx,(idv, start, line) in enumerate(id_positions):
        end = (id_positions[idx+1][1]-1) if idx+1 < len(id_positions) else len(paras)-1
        items.append({"id": idv, "title": line, "file": str(source_file).replace("\\","/"),
                      "para_start": start, "para_end": end})
        toc[idv] = {"file": str(source_file).replace("\\","/"), "para_start": start, "para_end": end}
    return items, toc

# Non-Tech (DOCX)
nt_paras = read_docx_paras(NT_SRC) if NT_SRC.exists() else []
nt_items, nt_toc = index_from_paras(nt_paras, ID_NT, NT_SRC)

# Tech (ODT)
td_paras = read_odt_paras(TD_SRC) if TD_SRC.exists() else []
td_items, td_toc = index_from_paras(td_paras, ID_TD, TD_SRC)

OUT_NT.write_text(json.dumps(nt_items, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_TD.write_text(json.dumps(td_items, ensure_ascii=False, indent=2), encoding="utf-8")
OUT_TOC.write_text(json.dumps({"nt": nt_toc, "td": td_toc}, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Indexed NT={len(nt_items)} TD={len(td_items)} IDs from originals.")
