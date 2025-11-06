---
id: TD-286
title: "**1.15.O Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-286-115o-error-taxonomy-clientsafe\TD-286-overview.md"
parent_id: 
anchor: "TD-286"
checksum: "sha256:39af58c0edaaa24f0bda3f14341b985a2ad317fbbd4333e6b6bc1ed211881953"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-286"></a>
## **1.15.O Error taxonomy (client‑safe)**

- *CASE_NOT_FOUND*, *CASE_ACCESS_DENIED*
- *ATTACHMENT_BLOCKED* (malware/NSFW)
- *REFUND_NOT_ELIGIBLE* (policy)
- *PAYOUT_HOLD_APPLY_FAILED* (admin‑only)
- *CHARGEBACK_DEADLINE_PASSED* (admin‑only)  
  Each with *code*, *message*, *hint*, *corrId*.
