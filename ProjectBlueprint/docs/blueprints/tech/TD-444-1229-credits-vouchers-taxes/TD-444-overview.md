---
id: TD-444
title: "**1.22.9 Credits, vouchers & taxes**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-444-1229-credits-vouchers-taxes\TD-444-overview.md"
parent_id: 
anchor: "TD-444"
checksum: "sha256:111f627353ea9cecf61c004d36f83763e319c878cea32368163083260056e21a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-444"></a>
## **1.22.9 Credits, vouchers & taxes**

- **Credits (referral/promos)** reduce **platform fee** (buyer_fee) only unless promo explicitly subsidizes subtotal.
- If a promo reduces **subtotal**, it’s platform‑funded; treat as **negative revenue** in analytics.
- **Tax** on platform fees depends on jurisdiction; at launch either (a) enable **Stripe Tax** for the fee component, or (b) restrict to jurisdictions where fees are non‑taxable. Provider service tax remains provider’s responsibility at launch; we show guidance.

**Artifact — platform invoice MJML (fee line item)**  
**Recommended path:** *comms/templates/invoice_platform_fee.mjml*  
*(Structure mirrors §1.16 MJML; includes order id, buyer fee, tax (if any), and payment method.)*
