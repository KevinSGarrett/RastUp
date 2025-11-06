---
id: TD-514
title: "**1.27.13 Safe‑Mode & SFW gating (SEO)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-514-12713-safemode-sfw-gating-seo\TD-514-overview.md"
parent_id: 
anchor: "TD-514"
checksum: "sha256:39734f071484f4341a36aa8d723edc8e35d268c53394d1f015fe225160894ce9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-514"></a>
## **1.27.13 Safe‑Mode & SFW gating (SEO)**

- **Indexable pages must be Safe‑Mode clean**: if any visible component would render NSFW previews, return *noindex,nofollow*.
- **Profile/studio completeness:** below threshold → **noindex** to avoid thin content.
- **Fan‑Sub (paid)**: *noindex* on all paid content and collection pages; preview pages (teasers) are SFW.
