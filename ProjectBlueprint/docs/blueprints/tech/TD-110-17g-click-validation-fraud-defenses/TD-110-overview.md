---
id: TD-110
title: "**1.7.G Click validation & fraud defenses**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-110-17g-click-validation-fraud-defenses\TD-110-overview.md"
parent_id: 
anchor: "TD-110"
checksum: "sha256:ca4b7e814e5a6d3a28a81b992a7b58e8eb46cca6b7e4a963948779ab41369dd1"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-110"></a>
## **1.7.G Click validation & fraud defenses**

**Instrumentation:**

- Every impression returns a unique ***impression_id*** embedded in the card.
- Clicks POST back with *{ impression_id }* + signed token; server enriches with *ip_hash*, *ua_hash*, *anon_fp_hash*, *user_id*.

**Dedup & windows:**

- Deduplicate multiple clicks from the **same session+impression** within **T seconds** (e.g., 45s).
- Only bill the **first valid click** per impression.

**Invalid click detection (near‑real‑time):**

- Heuristics: excessive frequency per IP block/FP, impossible geos vs city, bot UA, scroll‑less clicks, zero‑dwell.
- Scores and thresholds → if invalid: log *invalid_click* and **do not bill**.
- If billed earlier and later flagged in batch re‑processing → issue **make‑good credit** (ledger *kind='credit'*).

**Abuse control:**

- Rate‑limit by IP block/FP; hard ban patterns into WAF; suspicious campaigns auto‑pause with alert to Admin.
