---
id: TD-437
title: "**1.22.2 Pricing & fee model (baseline)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-437-1222-pricing-fee-model-baseline\TD-437-overview.md"
parent_id: 
anchor: "TD-437"
checksum: "sha256:70b29db2cba0afe31b73c19febe74ea9bf981f8d7508cb2d59407f20dbbc92f8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-437"></a>
## **1.22.2 Pricing & fee model (baseline)**

- **Buyer pays:** *subtotal* (package + add‑ons) + *buyer_fee* (platform) + taxes (if applicable).
- **Provider receives:** *subtotal* minus Stripe processing (from provider’s share) minus optional **provider take** if we ever use it.
- **Platform receives:** *buyer_fee* (+ optional provider take).
- **Refund/chargeback policy** controls who eats which fees.

**Artifact — fee policy matrix**  
**Recommended path:** *payments/policy/fee-matrix.md*

*- Buyer cancels before provider accepts: Full refund; all fees returned.*  
*- Buyer cancels \>48h after accept: Refund subtotal minus cancellation fee to provider; platform fee refunded.*  
*- No-show: Provider receives minimum guarantee; platform may refund buyer fee at discretion.*  
*- Dispute lost: Full refund; provider payout clawback; platform fee refunded unless provider fraud is proven.*
