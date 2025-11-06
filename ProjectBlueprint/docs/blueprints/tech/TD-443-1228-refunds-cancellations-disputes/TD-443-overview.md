---
id: TD-443
title: "**1.22.8 Refunds, cancellations & disputes**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-443-1228-refunds-cancellations-disputes\TD-443-overview.md"
parent_id: 
anchor: "TD-443"
checksum: "sha256:7be248e9bb2bb7f6430e256e922e185f9899453e1afd77f4e621706945731aad"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-443"></a>
## **1.22.8 Refunds, cancellations & disputes**

- **Refunds**: compute per policy; create Stripe Refunds; write *refund_ledger*. Partial refunds supported.

- **Disputes**: on *charge.dispute.created* → **pause transfer** if pending; if already paid, prepare potential clawback.

  - Evidence pack = messages, deliverables, ToS acceptance, studio confirmations; submit via API or dashboard.
  - On closure: if **lost**, finalize refund ledger; claw back provider payout; if **won**, release reserve/hold.

**Artifact — refund policy JSON (for UI)**  
**Recommended path:** *payments/policy/refund-policy.json*

*{*  
*"before_accept": {"buyer":"100%", "provider":"0%"},*  
*"accepted_gt_48h": {"buyer":"subtotal - cancel_fee", "provider":"cancel_fee"},*  
*"accepted_lt_48h": {"buyer":"partial at platform discretion", "provider":"minimum_guarantee"}*  
*}*
