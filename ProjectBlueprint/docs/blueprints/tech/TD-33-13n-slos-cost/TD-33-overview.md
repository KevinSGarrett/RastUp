---
id: TD-33
title: "**1.3.N SLOs & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-33-13n-slos-cost\TD-33-overview.md"
parent_id: 
anchor: "TD-33"
checksum: "sha256:1f22f369cd0fee2767d73fe843d94d17a535f1ce9446549fba4e0a791a4811b7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-33"></a>
## **1.3.N SLOs & cost**

- **SLOs:** Checkout p95 \< **2s** (incl. tax/3DS); charge error rate \< **1%** (excluding user cancellations); payout queue drain \< **15 min** after completion; document pack creation \< **3s** p95.
- **Cost:** Stripe pay‑as‑you‑go; deposits are rare operations; tax provider billed per transaction; Step Functions + Lambdas are event‑driven; no always‑on compute.
