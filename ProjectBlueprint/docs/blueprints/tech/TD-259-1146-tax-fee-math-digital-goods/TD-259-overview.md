---
id: TD-259
title: "**1.14.6 Tax & fee math (digital goods)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-259-1146-tax-fee-math-digital-goods\TD-259-overview.md"
parent_id: 
anchor: "TD-259"
checksum: "sha256:db6ccb9b972f4a8fae4d8aaa8f601be3e13b2c7c332952973697efd06ae3a6cd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-259"></a>
## **1.14.6 Tax & fee math (digital goods)**

- **Buyer line items** (per order/invoice):

*subtotal_cents (creator’s content)*  

- content_tax_cents (digital services tax; adapter calculates)
- platform_fee_cents (0 at MVP unless policy says otherwise)
- platform_fee_tax_cents  
  = total_cents (charged)

<!-- -->

- **Platform revenue**: **only** the **platform_fee_cents** (and recognized when **collected**) per §1.9; we are not MoR for creator content unless explicitly configured (default: platform MoR for *platform fee*, not for content price; content is pass‑through).
- **Jurisdictions**: use adapter flags to treat content as **digital service**; store tax summary per invoice/order for audit.
