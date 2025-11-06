---
id: TD-66
title: "**1.4.M Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-66-14m-error-taxonomy-clientsafe\TD-66-overview.md"
parent_id: 
anchor: "TD-66"
checksum: "sha256:d1c9b7cf10d87a67d5147826df1ff54eb906f6766c1830825d05cf6dc56c1710"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-66"></a>
## **1.4.M Error taxonomy (client‑safe)**

- *MSG_POLICY_BLOCKED* — text violates anticircumvention policy.
- *MSG_NSFW_BLOCKED* — preview blocked under Safe‑Mode.
- *THREAD_NOT_MEMBER* — user not participant.
- *THREAD_LOCKED* — admin lock.
- *ACTION_INVALID_STATE* — e.g., approve deliverable already closed.
- *ACTION_CONFLICT* — reschedule overlaps; check §1.3 validation.
- *PANEL_VERSION_CONFLICT* — optimistic concurrency failed.
- *UPLOAD_QUARANTINED* — file in safety review.

All error payloads include *code*, *message*, *hint*, *corrId*.
