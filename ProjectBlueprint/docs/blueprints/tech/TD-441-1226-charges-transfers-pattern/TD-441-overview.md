---
id: TD-441
title: "**1.22.6 Charges & transfers pattern**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-441-1226-charges-transfers-pattern\TD-441-overview.md"
parent_id: 
anchor: "TD-441"
checksum: "sha256:d42a1c988f0fe9498c42c520fce791d47dc5c28a5e2545820eaf34c7f6b5d77a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-441"></a>
## **1.22.6 Charges & transfers pattern**

Choose **one** per order for simplicity:

- Destination charge

  - Charge on connected account; include *application_fee_amount*.
  - **Pros:** Simple split; Stripe handles fee. **Cons:** Fewer methods; less transfer timing control.

- **Separate charges & transfers** (recommended)

  - Charge on platform; attach *transfer_group=order_id*; create **Transfer** to provider on completion.
  - **Pros:** Full payout timing control; clean refunds. **Cons:** Platform temporarily carries liability.
