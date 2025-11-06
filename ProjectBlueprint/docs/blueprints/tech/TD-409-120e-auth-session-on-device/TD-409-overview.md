---
id: TD-409
title: "**1.20.E Auth & session on device**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-409-120e-auth-session-on-device\TD-409-overview.md"
parent_id: 
anchor: "TD-409"
checksum: "sha256:2009ab3964eefda62321cf9ea9a9f00d28f1cb178f7e43c1bee2c0af0b9a1947"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-409"></a>
## **1.20.E Auth & session on device**

- **Cognito** hosted UI or embedded flows; JWTs stored in **HttpOnly Secure** cookies for Web/PWA; in RN, keep tokens in **secure storage** (Keychain/Keystore).
- **Session refresh** via refresh‑token rotation; background refresh guarded by app state.
- **Device trust**: bind push tokens and device fingerprints to user id for security & rate‑limits (§1.18).
