---
id: TD-250
title: "**1.14.N Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-250-114n-error-taxonomy-clientsafe\TD-250-overview.md"
parent_id: 
anchor: "TD-250"
checksum: "sha256:4eb939e1950c9eba2d1ddfdda26b6195580478856ebd3cf29eb39079d0473566"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-250"></a>
## **1.14.N Error taxonomy (client‑safe)**

- *FANSUB_IDV_REQUIRED* — user not age‑verified.
- *FANSUB_CREATOR_NOT_PUBLISHED* — creator page not live.
- *FANSUB_PRICE_OUT_OF_RANGE* — violates pricing policy.
- *FANSUB_ENTITLEMENT_REQUIRED* — trying to access locked content.
- *FANSUB_REQUEST_STATE_INVALID* — bad action order.
- *FANSUB_MEDIA_BLOCKED* — preview failed safety checks.
- *PAYMENT_FAILED* — Stripe failure; include retriable hints.

Each error includes *code*, *message*, *hint*, *corrId*.
