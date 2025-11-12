# orchestrator/knowledge.py
import argparse
import json
import os
from pathlib import Path
from typing import Tuple

REPO = Path(os.environ.get("REPO_ROOT", r"C:\RastUp\RastUp"))
BP_DIR = REPO / "docs" / "blueprints"
SECTIONS = BP_DIR / "sections.json"
NT_DOCX = BP_DIR / "Combined_Master_PLAIN_Non_Tech_001.docx"
TD_ODT = BP_DIR / "TechnicalDevelopmentPlan.odt"

def audit(strict: bool) -> Tuple[int, str]:
    msgs = []
    ok = True
    if NT_DOCX.exists(): msgs.append(f"OK: {NT_DOCX.name}")
    else: msgs.append(f"MISS: {NT_DOCX.name}"); ok = False
    if TD_ODT.exists(): msgs.append(f"OK: {TD_ODT.name}")
    else: msgs.append(f"MISS: {TD_ODT.name}"); ok = False
    if not SECTIONS.exists():
        msgs.append("MISS: sections.json not found"); ok = False
    else:
        try:
            data = json.loads(SECTIONS.read_text(encoding="utf-8"))
            n = len(data) if isinstance(data, list) else 0
            kinds = {str(x.get("kind","")).upper() for x in (data if isinstance(data,list) else [])}
            msgs.append(f"OK: sections.json entries={n} kinds={sorted(kinds)}")
            if "NT" not in kinds or "TD" not in kinds:
                msgs.append("WARN: sections.json missing NT or TD entries")
                if strict: ok = False
        except Exception as e:
            msgs.append(f"ERR: sections.json invalid: {e}"); ok = False
    return (0 if (ok or not strict) else 1), "\n".join(msgs)

def rebuild() -> Tuple[int, str]:
    out = []
    rc_all = 0
    def run(p: Path) -> int:
        import subprocess, sys
        if not p.exists(): return 0
        r = subprocess.run([sys.executable, str(p)], cwd=str(REPO), text=True, capture_output=True)
        out.append(f"$ python {p}\n{(r.stdout or '')}{(r.stderr or '')}")
        return r.returncode
    rc_all |= run(REPO / "scripts" / "blueprints" / "build_td_windows.py")
    rc_all |= run(REPO / "scripts" / "blueprints" / "build_sections.py")
    return rc_all, "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit"); a.add_argument("--strict", action="store_true")
    sub.add_parser("rebuild")
    ns = ap.parse_args()
    if ns.cmd == "audit":
        rc, msg = audit(ns.strict); print(msg); raise SystemExit(rc)
    if ns.cmd == "rebuild":
        rc, msg = rebuild(); print(msg); raise SystemExit(rc)

if __name__ == "__main__":
    main()
