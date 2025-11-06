---
id: TD-260
title: "**1.14.7 Accounting & GL (platform side)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-260-1147-accounting-gl-platform-side\TD-260-overview.md"
parent_id: 
anchor: "TD-260"
checksum: "sha256:ace1fbff5af544553fb8b36b75da27c6031c8266cfa373b9a1168a7e94723bc2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-260"></a>
## **1.14.7 Accounting & GL (platform side)**

- **At capture** (order or invoice paid):

*Dr Cash:Stripe total_cents*  
*Cr Liability:CreatorPayable subtotal_cents + content_tax_cents (if pass-through)*  
*Cr Deferred:PlatformFees platform_fee_cents*  
*Cr Liability:TaxPayable:PlatformFeeTax platform_fee_tax_cents*  

- **At payout to creator**:

*Dr Liability:CreatorPayable transfer_amount_cents*  
*Cr Cash:Stripe transfer_amount_cents*  

- **When fee recognized** (immediate on invoice/order paid if we treat fee as earned at sale for Fan‑Sub):

*Dr Deferred:PlatformFees platform_fee_cents*  
*Cr Revenue:PlatformFees platform_fee_cents*  

- **Refunds/Chargebacks** mirror §1.9 logic (reverse earned if applicable).

If we configure **platform fee = 0** at MVP, platform revenue on Fan‑Sub is **\$0** and accounting is simpler; we still incur Stripe fees as expense.
