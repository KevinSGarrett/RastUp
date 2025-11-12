# orchestrator/render_outline.py
import json, os, re
from pathlib import Path
from typing import List, Dict

REPO = Path(os.environ.get("REPO_ROOT", r"C:\RastUp\RastUp"))
QUEUE = REPO / "ops" / "queue.jsonl"
OUTLINE = REPO / "docs" / "OUTLINE.md"

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

def main():
    items = load_queue()
    by_phase: Dict[str, List[dict]] = {}
    for it in items:
        ph = phase_of(it.get("id",""))
        by_phase.setdefault(ph, []).append(it)

    lines = []
    lines.append("# Project Outline (WBS)")
    for ph in sorted(by_phase.keys(), key=lambda s: int(s) if s.isdigit() else 999):
        lines.append(f"\n## Phase {ph}")
        for it in sorted(by_phase[ph], key=lambda x: x.get("id","")):
            checked = "x" if str(it.get("status","")).lower() == "done" else " "
            title = it.get("title","")
            owner = it.get("owner","?")
            lines.append(f"- [{checked}] **{it.get('id','?')}** — {title} — owner: {owner}")
    OUTLINE.parent.mkdir(parents=True, exist_ok=True)
    OUTLINE.write_text("\n".join(lines), encoding="utf-8")
    print(str(OUTLINE))

if __name__ == "__main__":
    main()
