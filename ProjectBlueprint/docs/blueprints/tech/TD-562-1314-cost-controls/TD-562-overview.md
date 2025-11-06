---
id: TD-562
title: "**1.3.14 Cost controls**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-562-1314-cost-controls\TD-562-overview.md"
parent_id: 
anchor: "TD-562"
checksum: "sha256:8b859c9d4ac8eb4aa1d989529d1310bfa7a9098539167ffa77c89db546d24595"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-562"></a>
## **1.3.14 Cost controls**

- One PSP (Stripe) at launch; **no Plaid** needed because **Stripe Financial Connections** covers ACH with lower integration surface and fewer vendors (cheaper to operate). If later needed for broader bank coverage, we can add Plaid behind a feature flag.
- Off‑peak Lambdas (webhooks, transforms) scale to zero; Aurora min ACUs tuned; CloudFront caches static and semi‑static pages.
