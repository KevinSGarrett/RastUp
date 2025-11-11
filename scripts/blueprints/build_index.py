# scripts/blueprints/build_index.py
import os, sys, json, hashlib, re, pathlib
from datetime import datetime

# Optional imports guarded so script still runs without them
try:
    from docx import Document
except Exception:
    Document = None
try:
    from odf.opendocument import load as odf_load
    from odf import teletype
except Exception:
    odf_load = None
    teletype = None
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC_DIR = REPO / "docs" / "blueprints"
PLAIN_DIR = SRC_DIR / "plain"
PLAIN_DIR.mkdir(parents=True, exist_ok=True)

def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def norm_whitespace(s: str) -> str:
    return re.sub(r"\s+\n", "\n", re.sub(r"[ \t]+", " ", s)).strip()

def from_docx(path: pathlib.Path) -> str:
    if Document is None: return ""
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)

def from_odt(path: pathlib.Path) -> str:
    if odf_load is None or teletype is None: return ""
    doc = odf_load(str(path))
    return teletype.extractText(doc.body)

def from_pdf(path: pathlib.Path) -> str:
    if PdfReader is None: return ""
    reader = PdfReader(str(path))
    return "\n".join((p.extract_text() or "") for p in reader.pages)

def type_of(path: pathlib.Path) -> str:
    # naive domain classifier: tweak as needed
    name = str(path).lower()
    if "non_tech" in name or "non-tech" in name or "nontech" in name:
        return "non_tech"
    if "technical" in name or "tech" in name:
        return "tech"
    # fallback to folder hint
    return "tech" if "technical" in path.parts else "non_tech"

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def normalize_one(path: pathlib.Path) -> dict:
    ext = path.suffix.lower()
    text = ""
    if ext in [".md", ".txt"]:
        text = read_text(path)
    elif ext == ".docx":
        text = from_docx(path)
    elif ext == ".odt":
        text = from_odt(path)
    elif ext == ".pdf":
        text = from_pdf(path)
    else:
        return {"skipped": True, "reason": f"Unsupported ext {ext}"}

    text = norm_whitespace(text)
    if not text:
        return {"skipped": True, "reason": f"No text extracted from {path.name}"}

    # write normalized markdown next to sources
    rel = path.relative_to(SRC_DIR)
    plain_name = rel.with_suffix(".md").name
    out = PLAIN_DIR / plain_name
    out.write_text(text + "\n", encoding="utf-8")

    rec = {
        "source_rel": str(rel).replace("\\", "/"),
        "plain_rel": f"plain/{plain_name}",
        "title": path.stem,
        "domain": type_of(path),
        "words": len(text.split()),
        "sha1": sha1(text),
        "mtime": datetime.utcfromtimestamp(path.stat().st_mtime).isoformat() + "Z",
    }
    return rec

def main():
    supported = {".md", ".txt", ".docx", ".odt", ".pdf"}
    records = []
    skipped = []

    for p in SRC_DIR.rglob("*"):
        if not p.is_file(): continue
        if p.suffix.lower() not in supported: continue
        if p.parts and "plain" in p.parts:  # skip outputs
            continue
        res = normalize_one(p)
        if "skipped" in res:
            skipped.append({"path": str(p), "reason": res["reason"]})
        else:
            records.append(res)

    # partition into technical/non-technical
    nt = [r for r in records if r["domain"] == "non_tech"]
    td = [r for r in records if r["domain"] == "tech"]

    (SRC_DIR / "nt-index.json").write_text(json.dumps(nt, indent=2), encoding="utf-8")
    (SRC_DIR / "td-index.json").write_text(json.dumps(td, indent=2), encoding="utf-8")
    (SRC_DIR / "sections.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    # optional cache for TOC or other derived data
    (SRC_DIR / "toc-cache.json").write_text(json.dumps({
        "counts": {"all": len(records), "non_tech": len(nt), "tech": len(td)},
        "skipped": skipped
    }, indent=2), encoding="utf-8")

    print(f"Normalized={len(records)} Skipped={len(skipped)} -> plain/*.md + nt-index.json + td-index.json")

if __name__ == "__main__":
    main()
