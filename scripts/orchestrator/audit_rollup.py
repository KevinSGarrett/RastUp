import json, hashlib, datetime
from pathlib import Path

ROOT   = Path(".")
LEDGER = ROOT/"docs"/"logs"/"cost-ledger.jsonl"
APPR   = ROOT/"ops"/"approvals"
BOOST  = ROOT/"ops"/"flags"/"boost.json"
QUEUE  = ROOT/"ops"/"queue.jsonl"
OUT    = ROOT/"docs"/"orchestrator"/"AUDIT.jsonl"
STATE  = ROOT/"ops"/"cache"/"audit_state.json"

def now(): return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def load_state():
    if STATE.exists():
        try: return json.loads(STATE.read_text(encoding="utf-8"))
        except: pass
    return {"ledger_pos": 0, "approvals": {}, "boost_hash": ""}

def save_state(s): 
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2), encoding="utf-8")

def file_lines(p: Path):
    return p.read_text(encoding="utf-8").splitlines() if p.exists() else []

def hash_text(s: str): 
    return hashlib.sha256(s.encode("utf-8","ignore")).hexdigest()[:16]

def append_event(ev: dict):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")

def roll_ledger(st):
    lines = file_lines(LEDGER)
    start = st.get("ledger_pos", 0)
    for i, ln in enumerate(lines[start:], start=start):
        try:
            d = json.loads(ln)
            ev = {
                "ts_write": now(),
                "kind": "ledger",
                "ts": d.get("ts"),
                "model": d.get("model"),
                "usd": d.get("usd"),
                "details": d.get("details", {})
            }
            append_event(ev)
        except: pass
        st["ledger_pos"] = i + 1

def roll_approvals(st):
    seen = st.get("approvals", {})
    if not APPR.exists(): return
    for p in sorted(APPR.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            slug = d.get("slug") or p.stem
            sig = hash_text(json.dumps(d, sort_keys=True))
            if seen.get(slug) != sig:
                ev = {"ts_write": now(), "kind":"approval", "slug":slug, "status":d.get("status"), "usd":d.get("usd"), "title":d.get("title")}
                append_event(ev)
                seen[slug] = sig
        except: pass
    st["approvals"] = seen

def roll_boost(st):
    text = BOOST.read_text(encoding="utf-8") if BOOST.exists() else ""
    sig = hash_text(text)
    if st.get("boost_hash") != sig:
        ev = {"ts_write": now(), "kind":"boost", "content": json.loads(text) if text else None}
        append_event(ev)
        st["boost_hash"] = sig

def roll_queue_snapshot():
    q = file_lines(QUEUE)
    if q:
        try:
            last = json.loads(q[-1])
            ev = {"ts_write": now(), "kind":"queue_snapshot", "size": len(q), "tail": last}
            append_event(ev)
        except:
            append_event({"ts_write": now(), "kind":"queue_snapshot", "size": len(q)})

def main():
    st = load_state()
    roll_ledger(st)
    roll_approvals(st)
    roll_boost(st)
    roll_queue_snapshot()
    save_state(st)
    print(f"AUDIT appended. ledger_pos={st['ledger_pos']} approvals={len(st['approvals'])} boost_hash={st['boost_hash']}")

if __name__ == "__main__":
    main()
