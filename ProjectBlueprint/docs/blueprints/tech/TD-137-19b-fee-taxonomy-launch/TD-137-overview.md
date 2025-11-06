---
id: TD-137
title: "**1.9.B Fee taxonomy (launch)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-137-19b-fee-taxonomy-launch\TD-137-overview.md"
parent_id: 
anchor: "TD-137"
checksum: "sha256:aed6ffbee9de39801525588baf4450f26af73cfe80414f426dc97e4aacdf64e8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-137"></a>
## **1.9.B Fee taxonomy (launch)**

Keep MVP simple, configurable in AppConfig. All fees are computed **per leg** so partial cancels/refunds work cleanly.

- **Marketplace (buyer) fee** — percentage + floor/ceiling; charged to buyer; per‑leg line *platform_fee_cents*.
- **Platform fee tax** — via tax adapter (city‑aware), per‑leg line *platform_fee_tax_cents*.
- **Payment processing fee** — Stripe fees (variable + fixed); *expense* on the platform (not charged to buyer at MVP).
- **Optional seller fee (withheld)** — **off** at MVP; if enabled later, it reduces seller payout and is recognized as revenue when earned.
- **Rounding** — leg‑local, banker’s only if tax provider requires; otherwise pure cents math.

Result per **leg** at confirmation snapshot:

*buyer_pays_leg_total*  
*= (seller_subtotal + service_tax)*  
* + platform_fee_cents*  
* + platform_fee_tax_cents*  

Totals across legs roll up to **LBG charge amount**.
