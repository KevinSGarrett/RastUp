---
id: TD-26
title: "**1.3.G Refunds & cancellations**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-26-13g-refunds-cancellations\TD-26-overview.md"
parent_id: 
anchor: "TD-26"
checksum: "sha256:307fe7310e070e11c54d439f942cf0b2de66f821650674f54af387b862dcd273"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-26"></a>
## **1.3.G Refunds & cancellations**

**Policy engine**

- Encodes time‑banded refunds per leg (e.g., 72h+, 24–72h, \<24h).
- Computes buyer refund and seller forfeiture; **platform fees** refundability follows policy.
- **Group cancellation**: apply each leg’s policy independently; the group summary is a sum (displayed on the group receipt).

**Technical flow**

- Create *refund* records per leg; call Stripe *refunds.create* with *amount*; reconcile via webhooks; update receipts and Gold facts.
