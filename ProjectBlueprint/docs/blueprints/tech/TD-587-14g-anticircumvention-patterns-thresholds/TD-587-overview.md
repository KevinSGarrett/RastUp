---
id: TD-587
title: "**1.4.G Anti‑circumvention patterns & thresholds**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-587-14g-anticircumvention-patterns-thresholds\TD-587-overview.md"
parent_id: 
anchor: "TD-587"
checksum: "sha256:dcb9b024ef049e2ba145ef57ef751ed651d062a73568341a7fbb99d14d15849f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-587"></a>
## **1.4.G Anti‑circumvention patterns & thresholds**

**Goal:** keep value on‑platform (escrow, protection, reviews) while being fair and transparent.

NonTechBlueprint

**Risk signals (scored):**

- **Keywords & euphemisms** for off‑platform pay: *cash app\|cashapp\|venmo\|zelle\|paypal\|wire\|bank transfer\|invoice me\|outside platform\|off platform\|pay direct\|send to my email\|onlyfans tip\|telegram\|whatsapp\|snap* (+ common variants/obfuscations: *v3nm0*, *ca\$h app*, *wh\*tsapp*).
- **Link domains**: high‑risk (payment/chat domains).
- **New account** + high send rate + copy‑paste patterns.
- **Repeated attachment of QR codes** or payment handles.

**Thresholds/Actions (initial):**

- **Score \< 3** → show **nudge banner**: “Keep payments on RastUp for protection.”
- **3 ≤ score \< 6** → throttle new messages (cool‑down 30–60s), disable external links in that thread.
- **Score ≥ 6 or repeat within 24h** → soft‑block thread; create **Safety card** with prefilled reason; route to Admin case.
- **Gross violation** keywords (e.g., explicit request to bypass escrow) → immediate soft‑block + case.  
  All actions are **transparent** in‑thread, with a link to policy.

NonTechBlueprint
