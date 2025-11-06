---
id: TD-83
title: "**1.5.N Error taxonomy**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-83-15n-error-taxonomy\TD-83-overview.md"
parent_id: 
anchor: "TD-83"
checksum: "sha256:de456de795708693c1260642852b99245b4e0932ad1e35e1642a6838f3d337ee"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-83"></a>
## **1.5.N Error taxonomy**

- *DOC_VARS_MISSING* — required variables absent or invalid.
- *DOC_TEMPLATE_GATED* — template not available for city/role.
- *DOC_SIGNER_MISSING* — signer role not mapped to a valid email/user.
- *DOC_RENDER_FAIL* — renderer error (retry with backoff).
- *ENVELOPE_CREATE_FAIL* — provider API error.
- *ENVELOPE_HMAC_INVALID* — webhook rejected.
- *DOC_REISSUE_REQUIRED* — leg change invalidated pack; re‑issue needed.
- *DOC_LEGAL_HOLD* — action blocked until hold removed.

All error payloads include *code*, *message*, *hint*, *corrId*.
