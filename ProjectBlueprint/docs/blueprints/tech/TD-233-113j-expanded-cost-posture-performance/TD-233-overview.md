---
id: TD-233
title: "**1.13.J (expanded) — Cost Posture & Performance**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-233-113j-expanded-cost-posture-performance\TD-233-overview.md"
parent_id: 
anchor: "TD-233"
checksum: "sha256:08b86749c392cf6da102c07513830c6a09b6067ea5205ea4dff22f3be7713d77"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-233"></a>
## **1.13.J (expanded) — Cost Posture & Performance**

- **Firehose**: small buffers to limit latency; GZIP + dynamic partitioning; DLQ for failed records.

- **Athena**:

  - Enforce **workgroup** with **encryption on**, **query bytes cap**, and **results location** per env.
  - Use **CTAS** with *bucketed_by* only if needed (careful with cost).
  - Partition filters **always applied** (*WHERE dt BETWEEN …*); add **city partition** to high‑volume facts (search, promotions) when warranted.

- **Glue**: schedule transforms during off‑peak; use minimal DPUs (e.g., 2–3) and **Athena CTAS** for many transforms to avoid Glue cost.

- **QuickSight**: prefer SPICE; schedule no more than 4–6 daily refreshes; monitor SPICE capacity and prune unused visuals.

**Budget alarms (per env):** S3 storage, Athena scanned bytes, Glue DPU‑hours, QuickSight capacity, Firehose PUTs.
