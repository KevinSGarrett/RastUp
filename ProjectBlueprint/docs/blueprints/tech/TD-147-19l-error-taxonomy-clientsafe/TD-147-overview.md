---
id: TD-147
title: "**1.9.L Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-147-19l-error-taxonomy-clientsafe\TD-147-overview.md"
parent_id: 
anchor: "TD-147"
checksum: "sha256:60827eff62a9379f6c57ba651d6c4267a14e60e9ab0612af039a709062034ea2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-147"></a>
## **1.9.L Error taxonomy (client‑safe)**

- *FEE_RULE_MISSING* — no fee rule for city/role.
- *WALLET_INSUFFICIENT_FUNDS* — requested apply exceeds balance.
- *WALLET_STALE_APPLY* — PI amount changed; recompute then apply.
- *GL_EXPORT_RANGE_TOO_LARGE* — split into batches.
- *MOR_MISCONFIGURED* — MoR toggle inconsistent with tax settings (admin‑only).
