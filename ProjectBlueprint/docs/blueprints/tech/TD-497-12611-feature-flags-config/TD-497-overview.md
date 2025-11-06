---
id: TD-497
title: "**1.26.11 Feature flags & config**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-497-12611-feature-flags-config\TD-497-overview.md"
parent_id: 
anchor: "TD-497"
checksum: "sha256:709d930a50cf8095be1d65ff62e0f5f74cf8e9aa6321a7090346c83243122046"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-497"></a>
## **1.26.11 Feature flags & config**

- Flags: **Instant Book eligibility**, **response SLA**, **deposit capture policy**, **city activation**, **Studio Lite requirement for IB**, **Saved‑search digests cadence**.
- Backed by DynamoDB table with typed schema, exposed read‑only to clients via CDN JSON for fast boot (signed, cache‑controlled).
