---
id: TD-34
title: "**1.3.O Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-34-13o-error-taxonomy-clientsafe\TD-34-overview.md"
parent_id: 
anchor: "TD-34"
checksum: "sha256:17f9777c00f0f9ecbfa474e97ab4872768c8d29e99012bcd41353d54dcea3fee"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-34"></a>
## **1.3.O Error taxonomy (client‑safe)**

- *CHK_DOCS_REQUIRED* — pack not complete.
- *CHK_STUDIO_CONFLICT* — studio unavailable at requested time.
- *CHK_CARD_ACTION_REQUIRED* — 3DS step required.
- *CHK_ACH_NOT_VERIFIED* — bank link incomplete.
- *CHK_ATOMIC_FAIL* — one leg failed validation; nothing charged.
- *REFUND_POLICY_BLOCK* — requested refund outside policy window.
- *DEPOSIT_CLAIM_DENIED* — claim exceeds policy/evidence.

Error payloads include *code*, *message*, *hint*, *corrId*, and suggested next steps.
