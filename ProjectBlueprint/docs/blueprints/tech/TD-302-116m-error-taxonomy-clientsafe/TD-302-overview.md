---
id: TD-302
title: "**1.16.M Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-302-116m-error-taxonomy-clientsafe\TD-302-overview.md"
parent_id: 
anchor: "TD-302"
checksum: "sha256:1c9e43f4bba416351c7ebdb0fe8da7c38159f912f9449be8b8115ad35e1b9ba2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-302"></a>
## **1.16.M Error taxonomy (client‑safe)**

- *ALERT_FREQUENCY_LIMIT* — already sent today for this search.
- *DIGEST_OPTOUT* — user unsubscribed.
- *SAFE_MODE_BLOCKED* — attempting to include 18+ in email.
- *REFERRAL_CAP_EXCEEDED* — monthly cap reached.
- *CREDIT_SCOPE_VIOLATION* — tried to apply buyer credit to non‑fee items.
- Each error returns *code*, *message*, *hint*, and *corrId*.
