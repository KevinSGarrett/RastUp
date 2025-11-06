---
id: TD-141
title: "**1.9.F Taxes on platform fees**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-141-19f-taxes-on-platform-fees\TD-141-overview.md"
parent_id: 
anchor: "TD-141"
checksum: "sha256:cfb475a7e489b94bbf5f84ffa21262ddd47f004ef0eae5c0c28d1dc1d3184ab5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-141"></a>
## **1.9.F Taxes on platform fees**

- Use same **Tax adapter** as §1.3 (TaxJar/Avalara/Stripe Tax).
- Quote **per leg** for *platform_fee_cents* → *platform_fee_tax_cents* using the buyer’s tax nexus vs city gate rules.
- Record *TaxPayable:PlatformFeeTax* at capture; reverse appropriately on refunds.
- Include platform fee tax lines in buyer receipts and in platform tax reports.
