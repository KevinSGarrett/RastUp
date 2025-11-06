---
id: TD-203
title: "**1.12.M Cost guardrails**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-203-112m-cost-guardrails\TD-203-overview.md"
parent_id: 
anchor: "TD-203"
checksum: "sha256:13fa3bccf544b91d300261cc4f1b750a644e26be6a6c44b9c0a09c131e7fa6da"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-203"></a>
## **1.12.M Cost guardrails**

- **Budgets & alarms** per account; Slack/email alert on 20%/50%/80% of monthly cap.

- Right‑sizing defaults:

  - Aurora Serverless v2 min ACU 0.5–1.0; autoscale up to 4–8 ACU at launch.
  - Typesense: 1 small node; OpenSearch OCU cap = 2–4 (off by default).
  - Lambda memory set to the cheapest point that meets p95; provisioned concurrency **off** unless needed.
  - S3 lifecycle rules on by default.
  - NAT usage minimized (prefer VPC endpoints; egress audit).

- **CI “cost bump” gate**: if IaC diff raises projected monthly spend over threshold, require finance approval.
