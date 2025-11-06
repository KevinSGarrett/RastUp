---
id: TD-185
title: "**1.11.M Error taxonomy (client‑safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-185-111m-error-taxonomy-clientsafe\TD-185-overview.md"
parent_id: 
anchor: "TD-185"
checksum: "sha256:d5a176207fece6f4a5709f740314397aa1d13527fdb7af61c7011b7435535421"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-185"></a>
## **1.11.M Error taxonomy (client‑safe)**

- *STUDIO_INCOMPLETE* — cannot publish; missing fields or media.
- *STUDIO_CONFLICT_BUFFER* — requested time conflicts after buffers/cleaning.
- *STUDIO_BLACKOUT* — requested time falls in blackout.
- *STUDIO_RATE_NOT_FOUND* — no applicable rate for requested window.
- *STUDIO_VERIFY_REQUIRED* — action requires verified studio (e.g., promotions).
- *STUDIO_MEDIA_BLOCKED* — preview blocked by safety rules.

Errors return *code*, *message*, *hint*, and a correlation id.
