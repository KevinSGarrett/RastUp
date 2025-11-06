---
id: TD-367
title: "**1.18.M SLOs, budgets & costs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-367-118m-slos-budgets-costs\TD-367-overview.md"
parent_id: 
anchor: "TD-367"
checksum: "sha256:d006fd6ab308e66fa4c97dc103206370f5888ecfca1f8cb3ff217d994fdc7230"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-367"></a>
## **1.18.M SLOs, budgets & costs**

**SLOs**

- **Auth availability** ≥ 99.9% monthly.
- **Webhook idempotency** 100% (no double side‑effects).
- **P0 IR response** ≤ 15 min; **P1** ≤ 1 hour.
- **Secrets rotation** success 100% monthly cadence.

**Budgets**

- WAF: managed rules only at start; add Bot Control if abuse appears.
- Security Hub/GuardDuty: monitor costs; scope to prod + stage at launch.
- Logs: 30–90d hot retention; archive to Glacier Instant Retrieval thereafter.
