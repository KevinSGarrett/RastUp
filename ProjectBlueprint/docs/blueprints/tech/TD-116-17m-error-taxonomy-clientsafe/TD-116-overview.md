---
id: TD-116
title: "**1.7.M Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-116-17m-error-taxonomy-clientsafe\TD-116-overview.md"
parent_id: 
anchor: "TD-116"
checksum: "sha256:2a9ab8ec88bb8cafe5602ba4057d12752af1a8fb6989d67ae6580a9d2f44ee00"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-116"></a>
## **1.7.M Error taxonomy (client‑safe)**

- *PROMO_ELIGIBILITY_FAILED* — trust, completeness, or policy not met.
- *PROMO_CPC_BELOW_FLOOR* — CPC under city/role floor.
- *PROMO_BUDGET_EXHAUSTED* — daily/total budget hit.
- *PROMO_INVALID_CITY* — city not allowlisted.
- *PROMO_PAYMENT_FAILED* — top‑up failed.
- *PROMO_SUSPENDED* — admin or auto policy suspension.
- *PROMO_CLICK_INVALIDATED* — click rejected; user is never shown this, used in logs/analytics.
