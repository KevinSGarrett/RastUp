---
id: TD-98
title: "**1.6.K Error taxonomy (client-safe)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-98-16k-error-taxonomy-client-safe\TD-98-overview.md"
parent_id: 
anchor: "TD-98"
checksum: "sha256:3a2655740aab2e441a681b8092788f4f4af713265116ee11c0b73f96d5ee2d5f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-98"></a>
## **1.6.K Error taxonomy (client-safe)**

- *IDV_PROVIDER_UNAVAILABLE* — retry or switch later.
- *IDV_FAILED* — provide appeal/retry path.
- *BG_CONSENT_REQUIRED* — user must accept consents.
- *BG_IN_PROGRESS* — already running; point to status view.
- *SOCIAL_OAUTH_FAILED* — include retry link.
- *TRUST_OVERRIDE_FORBIDDEN* — admin lacked permission/two-person approval.
