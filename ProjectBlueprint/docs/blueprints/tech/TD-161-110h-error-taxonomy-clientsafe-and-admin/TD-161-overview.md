---
id: TD-161
title: "**1.10.H Error taxonomy (client‑safe and admin)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-161-110h-error-taxonomy-clientsafe-and-admin\TD-161-overview.md"
parent_id: 
anchor: "TD-161"
checksum: "sha256:3dbf489c092467c922dbb7361aaa636786d463b00c7f845ab367a4fd25c886b6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-161"></a>
## **1.10.H Error taxonomy (client‑safe and admin)**

- *COMMS_PREF_BLOCKED* — user opted out for that category/channel.
- *COMMS_QUIET_HOURS* — scheduled due to quiet hours (not an error; informational).
- *COMMS_SUPPRESSED* — address on suppression list (hard bounce/complaint).
- *COMMS_TEMPLATE_MISSING_VAR* — variable resolver missing data (developer error; logged).
- *COMMS_PROVIDER_FAIL* — provider transient error; retried with backoff.
- *COMMS_RATE_LIMITED* — SMS or push throttled.
