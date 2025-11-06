---
id: TD-609
title: "**1.6.13 Cost & scaling**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-609-1613-cost-scaling\TD-609-overview.md"
parent_id: 
anchor: "TD-609"
checksum: "sha256:4ca8a04cd018485615208b49bb74fdc4ff0d72d5bd22cbdf314306f7e8f7fd96"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-609"></a>
## **1.6.13 Cost & scaling**

- **KB**: static rendering + CloudFront → near‑zero marginal cost.
- **Search**: Typesense small cluster (2–3 nodes) with nightly snapshot; shard by locale when needed.
- **Ticketing**: start with **3–5 Zendesk seats**; scale seats as tickets/100 bookings rises. Keep **Zammad** adapter ready if vendor costs outweigh value.
- **Goal alignment**: deflection + macros drive lower **cost/ticket** as volume grows, per your KPI section.

NonTechBlueprint
