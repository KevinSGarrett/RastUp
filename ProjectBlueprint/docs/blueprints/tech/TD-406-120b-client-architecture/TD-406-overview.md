---
id: TD-406
title: "**1.20.B Client architecture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-406-120b-client-architecture\TD-406-overview.md"
parent_id: 
anchor: "TD-406"
checksum: "sha256:65e5d3c5c0fc30e78745166386d9851999808067ee701947d65723af7a0b25ec"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-406"></a>
## **1.20.B Client architecture**

- **PWA shell** (Next.js): app‑router, service worker, manifest, edge caching; GraphQL via AppSync (JWT auth).

- **Native shells** (optional):

  - **React Native** + **Expo** (managed workflow) for iOS/Android.
  - Uses a small native bridge for push tokens, file pickers, camera, and device storage; renders either RN screens or a WebView wrapper for certain flows if we choose a hybrid approach.

- **Shared modules**: auth/session, GraphQL client, feature flags, Safe‑Mode, formatting (ICU), and analytics events shared across PWA and RN.
