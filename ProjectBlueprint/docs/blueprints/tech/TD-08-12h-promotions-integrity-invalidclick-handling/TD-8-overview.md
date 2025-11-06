---
id: TD-8
title: "**1.2.H Promotions integrity (invalid‑click handling)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-08-12h-promotions-integrity-invalidclick-handling\TD-8-overview.md"
parent_id: 
anchor: "TD-8"
checksum: "sha256:f01b113e054aa42adffb4a3578451e1b2b5d32f98a41a09aa2f2097f791664a4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-8"></a>
## **1.2.H Promotions integrity (invalid‑click handling)**

- Real‑time click stream with fingerprinting (device, IP block, user id, session id).
- **Deduplicate** multiple clicks from same session/user within T seconds.
- **Invalid click rules**: excessive repeat clicks, out‑of‑geo anomalies, bot signals → flagged and **not billed**.
- **Make‑good credits** auto‑issued for flagged traffic (logged as ledger entries).
- Holdouts (A/B) maintain an organic control set for unbiased impact analysis.
