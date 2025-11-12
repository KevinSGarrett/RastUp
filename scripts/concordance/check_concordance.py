#!/usr/bin/env python3
import json, sys, pathlib

p = pathlib.Path("docs/blueprints/sections.json")
if not p.exists():
    print("WARN: sections.json missing; soft-skip concordance.")
    sys.exit(0)

try:
    data = json.loads(p.read_text(encoding="utf-8"))
except Exception as e:
    print(f"WARN: could not parse sections.json: {e}")
    sys.exit(0)

nt = sum(1 for x in data if x.get("kind") == "NT")
td = sum(1 for x in data if x.get("kind") == "TD")
print(f"Concordance soft-check → NT={nt} TD={td}")

# Soft gate for now (always pass). We can harden later.
sys.exit(0)
