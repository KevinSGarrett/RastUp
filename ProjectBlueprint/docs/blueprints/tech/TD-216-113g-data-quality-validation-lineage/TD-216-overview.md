---
id: TD-216
title: "**1.13.G Data quality, validation & lineage**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-216-113g-data-quality-validation-lineage\TD-216-overview.md"
parent_id: 
anchor: "TD-216"
checksum: "sha256:87eba40638e38011431271c156365738296ba9402336f46fbd2a0eeb463ff842"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-216"></a>
## **1.13.G Data quality, validation & lineage**

- **Contract tests**: every event schema tested in CI; unknown event fields flagged but preserved in Bronze.
- **Great Expectations** (or **Deequ**) on Silver/Gold: uniqueness of ids, non‑nulls, ranges (e.g., *rating between 1..5*), monotonicity (e.g., payout queue should drain).
- **Lineage**: dbt docs + event schema registry show upstream/downstream for each mart.
- **Alerts**: failed expectations page Ops; large deltas in GMV/CTR vs 7‑day average trigger review.
