---
id: TD-268
title: "**1.14.15 Performance & cost budgets**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-268-11415-performance-cost-budgets\TD-268-overview.md"
parent_id: 
anchor: "TD-268"
checksum: "sha256:b695620775af4cbdc466861a8eba93c15f2985fa44f6bb1e63d7455fd443c817"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-268"></a>
## **1.14.15 Performance & cost budgets**

- **Previews only** ensures S3 ≪ cost of finals hosting. Target: ≤ 10 TB/mo egress at launch (cached via CF).
- **Stripe fees** dominate; tune dunning to reduce involuntary churn.
- **Compute**: watermark/transcode Lambdas constrained by concurrency; queue spikes; no provisioned concurrency unless p95 exceeds SLA.
