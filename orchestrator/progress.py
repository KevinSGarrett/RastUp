# orchestrator/progress.py
import json, os, re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

REPO = Path(os.environ.get("REPO_ROOT", r"C:\RastUp\RastUp"))
QUEUE = REPO / "ops" / "queue.jsonl"
PROGRESS = REPO / "docs" / "PROGRESS.md"
MATRIX = REPO / "docs" / "runbooks" / "access-readiness-matrix.md"

def load_queue() -> List[dict]:
    items = []
    if not QUEUE.exists(): return items
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try: items.append(json.loads(line))
        except Exception: pass
    return items

def phase_of(item_id: str) -> str:
    m = re.match(r"^WBS-(\d+)", str(item_id))
    return m.group(1) if m else "?"

def access_coverage() -> Tuple[int,int]:
    if not MATRIX.exists(): return (0,0)
    text = MATRIX.read_text(encoding="utf-8")
    rows = [l for l in text.splitlines() if "|" in l]
    pass_n = sum(1 for r in rows if re.search(r"\bPASS\b", r, re.I))
    fail_n = sum(1 for r in rows if re.search(r"\bFAIL\b", r, re.I))
    total = pass_n + fail_n
    return (pass_n, total)

def compute() -> str:
    items = load_queue()
    by_phase: Dict[str, Dict[str, float]] = {}
    done_total = 0.0
    for it in items:
        w = float(it.get("weight", 0.0))
        ph = phase_of(it.get("id",""))
        d = by_phase.setdefault(ph, {"weight":0.0, "done":0.0})
        d["weight"] += w
        if str(it.get("status","")).lower() == "done":
            d["done"] += w
            done_total += w
    p, t = access_coverage()
    acc_line = f"{(p / t * 100.0):.1f}%" if t else "N/A"
    lines = []
    lines.append("# Project Progress")
    lines.append("## Summary")
    lines.append(f"- Overall completion: {done_total*100:.2f}%")
    lines.append(f"- Access coverage: {acc_line}")
    lines.append(f"- Last update: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append("## Phase Breakdown (WBS)")
    lines.append("| Phase | Weight | % Done |")
    lines.append("|------:|-------:|-------:|")
    for ph in sorted(by_phase.keys(), key=lambda s: int(s) if s.isdigit() else 999):
        w = by_phase[ph]["weight"] or 0.0
        pct = (by_phase[ph]["done"]/w*100.0) if w>0 else 0.0
        lines.append(f"| {ph} | {w:.2f} | {pct:.1f}% |")
    lines.append("")
    return "\n".join(lines)

def main():
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS.write_text(compute(), encoding="utf-8")
    print(str(PROGRESS))

if __name__ == "__main__":
    main()
