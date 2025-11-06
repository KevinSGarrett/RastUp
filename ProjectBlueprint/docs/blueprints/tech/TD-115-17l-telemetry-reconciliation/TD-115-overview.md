---
id: TD-115
title: "**1.7.L Telemetry & reconciliation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-115-17l-telemetry-reconciliation\TD-115-overview.md"
parent_id: 
anchor: "TD-115"
checksum: "sha256:80da5cb2e702c2e74d59c53f1ccdd8d779fe54f506590123bfc4b75266fd6cf6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-115"></a>
## **1.7.L Telemetry & reconciliation**

**Events**

- promo.campaign.create\|activate\|pause\|resume\|end\|suspend
- *promo.policy.update* (with version)
- *promo.impression*, *promo.click*, *promo.invalid_click*
- *promo.spend.debit*, *promo.credit.issue*, *promo.topup.charge.succeeded\|failed*
- promo.recon.variance.notice

**Recon jobs (daily)**

- Compare **Σvalid_clicks × CPC** to **Σledger.spends**; verify against Stripe top‑ups/invoices.
- Variance \> threshold gates campaign serving in affected city until resolved (flag‑gated).
