---
id: TD-281
title: "**1.15.J Payout holds & releases**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-281-115j-payout-holds-releases\TD-281-overview.md"
parent_id: 
anchor: "TD-281"
checksum: "sha256:aeca727738c58028fd5beac9105f8dee76b116bb2a0f8259f5a510c9b82cc66a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-281"></a>
## **1.15.J Payout holds & releases**

- **Apply hold** on leg/order payable when: severe open case, chargeback notice, or DMCA that may require refund.
- **Release** on case close or representment win; **expire** after max window (configurable).
- Visible to seller/creator in **Finance console** with reason and expected timeline.
