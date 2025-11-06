---
id: TD-536
title: "**1.29.2 Architecture (cost‑conscious, elastic)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-536-1292-architecture-costconscious-elastic\TD-536-overview.md"
parent_id: 
anchor: "TD-536"
checksum: "sha256:aeaac04564b41b709ae71f14fadbf792230bd9649f76ea24676d7c6d772acf55"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-536"></a>
## **1.29.2 Architecture (cost‑conscious, elastic)**

- **Frontend:** Next.js (web) SSR for profile tabs; React Native (mobile) with identical data shape.
- **API:** AppSync GraphQL with Lambda resolvers.
- **Storage:** S3 (versioned) for images/video; CloudFront delivery; optional **on‑upload transforms** (thumbs, web‑optimized).
- **Search/Discovery:** Typesense collections for light faceting (“genres”, “city”, “role”), plus profile ranking signals.
- **Moderation & policy:** Safe‑Mode renderer + optional Rekognition moderation check; DMCA/T&S flows via Admin (§1.28).
- **Cost posture:** No external DAM/SaaS. S3 lifecycle → IA/Glacier; CloudFront caching; transforms cached.
