---
id: TD-222
title: "**1.13.M SLOs & alerts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-222-113m-slos-alerts\TD-222-overview.md"
parent_id: 
anchor: "TD-222"
checksum: "sha256:2e85e19fef14bb80dd6072d017589818fa0b4b6fbc29f8684471d125bff3294a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-222"></a>
## **1.13.M SLOs & alerts**

- **Ingestion**: EventBridge→S3 (Bronze) **≤ 60 s p95**.
- **NRT views**: Bronze→Silver (ops views) **≤ 10 min p95**.
- **Daily marts**: complete by **T+6h** local.
- **BI**: Dashboards available by **08:00** local; SPICE refresh success **≥ 99%** rolling 7 days.

Alerts on: ingestion lag beyond SLO, quality failures, unusual GMV deltas, ATHENA_SCANNED_BYTES anomalies (cost), QuickSight refresh failures.
