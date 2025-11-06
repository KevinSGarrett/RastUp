---
id: TD-449
title: "**1.22.14 Telemetry, SLOs & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-449-12214-telemetry-slos-cost\TD-449-overview.md"
parent_id: 
anchor: "TD-449"
checksum: "sha256:05da8fc6a0b9d12961f11ce2e6923000f4f6918585feab80139bbfd8df734ffd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-449"></a>
## **1.22.14 Telemetry, SLOs & cost**

- **Events:** *checkout.start\|confirm\|success\|fail*, *refund.create*, *dispute.open\|won\|lost*, *transfer.create\|paid*, *payout.paid\|failed*.
- **KPIs:** checkout conversion, authorization/capture rates, refund %, dispute %, T+N transfer SLA, webhook latency.
- **SLOs:** payment success p50 ≥ **96% (cards)**; webhook processing p95 ≤ **2s**; transfer execution after completion p95 ≤ **15m**; D+1 reconciliation completeness by **08:00 UTC**.
- **Cost posture:** Stripe only at launch; **ACH** only when volume justifies; no third‑party fraud SaaS initially—rely on Stripe Radar + our risk flags; serverless webhooks & nightly reconciliation to keep compute low.
