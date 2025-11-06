---
id: TD-558
title: "**1.3.10 Disputes & chargebacks**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-558-1310-disputes-chargebacks\TD-558-overview.md"
parent_id: 
anchor: "TD-558"
checksum: "sha256:da00ffa68809daeecc9202195eb994befe2a7f25d37fcf34f418153000677ae3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-558"></a>
## **1.3.10 Disputes & chargebacks**

- **In‑app disputes**: buyer/provider can open a dispute within the review window. System creates *booking.dispute* and routes a **T&S case** to Admin (§1.26). Evidence collection (photos, deliverables, chat history) with timestamps. Outcomes: *resolved_buyer* (refund), *resolved_provider* (payout), or *split* (partial).
- **Stripe chargebacks**: listen to *charge.dispute.\** webhooks; auto‑attach internal evidence pack (contracts, deliverables, chat logs) and submit via Stripe’s API; mark dispute status *chargeback*.
- **Deposit capture** (studios only): governed by §1.24 policy; not part of talent bookings.
