import json, datetime
from pathlib import Path

ROOT = Path(".")
LEDGER = ROOT/"docs"/"logs"/"cost-ledger.jsonl"
SAFE   = ROOT/"ops"/"flags"/"safe-mode.json"
BOOST  = ROOT/"ops"/"flags"/"boost.json"
OUT    = ROOT/"docs"/"orchestrator"/"SUMMARY.md"

def sum_ledger():
    total = 0.0
    if LEDGER.exists():
        for ln in LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(ln); total += float(d.get("usd",0.0))
            except: pass
    return round(total,2)

def main():
    spent = sum_ledger()
    safe  = SAFE.exists()
    boost = None
    if BOOST.exists():
        try: boost = json.loads(BOOST.read_text(encoding="utf-8")).get("remaining")
        except: pass
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(f"""# Budget Summary

**As of:** {ts} UTC

- **Cap:** $75.00  
- **Spent (ledger):** **${spent:.2f}**  
- **Mode:** {"ECONOMY" if spent >= 60 else "NORMAL"}  
- **SAFE-MODE:** {"ON" if safe else "OFF"}  
- **Boost:** {"none" if boost is None else f"${boost:.2f}"}  

_Source: ledger = docs/logs/cost-ledger.jsonl_
""", encoding="utf-8")
    print(f"spent=${spent:.2f} safe={'ON' if safe else 'OFF'} boost={boost if boost is not None else 'none'}")

if __name__ == "__main__":
    main()
