---
id: TD-556
title: "**1.3.8 Fees, tax, currencies**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-556-138-fees-tax-currencies\TD-556-overview.md"
parent_id: 
anchor: "TD-556"
checksum: "sha256:c9eafb45c37b9a3a786f47a040c4e89c95f9e46e2572a2d25ec20a472c26306c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-556"></a>
## **1.3.8 Fees, tax, currencies**

- **Platform fee** line item shown in **Summary & Fees** section of checkout (plus taxes if applicable).

NonTechBlueprint

- **Taxes**: optional Stripe Tax at launch; if disabled, show “taxes may apply” for certain jurisdictions and keep it off the critical path.
- **Currencies**: *currency* stored per order; start with *usd*.
