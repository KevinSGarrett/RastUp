---
id: TD-214
title: "**1.13.E Near‑real‑time ops views**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-214-113e-nearrealtime-ops-views\TD-214-overview.md"
parent_id: 
anchor: "TD-214"
checksum: "sha256:b99967ecec8df14314de3d186c1dfc9d661b0346a3c935e5f6296d6f4c92b6d9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-214"></a>
## **1.13.E Near‑real‑time ops views**

Some ops metrics (recon gates, payout backlogs, dispute queues) require freshness **\<15 min**.

- Create **NRT materialized views** in S3 via Athena CTAS running every **5–10 min**, small partitions only for today’s hours.
- Admin consoles read from these materialized Parquet tables for stable, fast loads.
