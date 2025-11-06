---
id: TD-32
title: "**1.3.M Telemetry (immutable events)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-32-13m-telemetry-immutable-events\TD-32-overview.md"
parent_id: 
anchor: "TD-32"
checksum: "sha256:0ffabb53e3ab0458a60a40ab3bacc2b088fd85e1bff9deadefb6e271475d5912"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-32"></a>
## **1.3.M Telemetry (immutable events)**

- *lbg.create*, *leg.create*, *checkout.start*, *docs.pack.create*, *docs.envelope.signed*,
- *payment.intent.created*, *payment.intent.requires_action*, *payment.capture.succeeded\|failed*,
- *deposit.auth.authorized\|captured\|voided\|expired*,
- *amendment.added*, *tax.quote*, *tax.commit*,
- *payout.queued\|paid\|failed*, *refund.created\|succeeded\|failed*,
- *dispute.opened\|evidence_submitted\|won\|lost*.

These feed Bronze→Silver→Gold with money checks (Σsplits = charge, Σpayouts + fees + refunds = charge over time).
