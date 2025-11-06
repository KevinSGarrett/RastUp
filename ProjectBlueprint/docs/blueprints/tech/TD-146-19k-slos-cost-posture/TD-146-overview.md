---
id: TD-146
title: "**1.9.K SLOs & cost posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-146-19k-slos-cost-posture\TD-146-overview.md"
parent_id: 
anchor: "TD-146"
checksum: "sha256:e6176f856ed023d07b191cd9bf9c2ca5279ec9c09fdb181d378cd29628629938"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-146"></a>
## **1.9.K SLOs & cost posture**

- **SLOs**:

  - Fee compute latency: **\<100 ms** p95.
  - Wallet apply latency: **\<75 ms** p95.
  - Daily close completes by **T+8h** local time; variance gating works.

- **Cost**: entirely serverless; no always‑on compute. S3 lifecycle on statements and exports (cold storage after 90 days). Stripe fees are pass‑through expenses; tax adapter paid per transaction.
