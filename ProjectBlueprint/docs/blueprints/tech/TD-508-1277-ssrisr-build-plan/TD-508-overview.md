---
id: TD-508
title: "**1.27.7 SSR/ISR build plan**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-508-1277-ssrisr-build-plan\TD-508-overview.md"
parent_id: 
anchor: "TD-508"
checksum: "sha256:2d9d7c129751534ea7029866e432b7a1fcd27175e5601b85d65c5cd865dcfb6a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-508"></a>
## **1.27.7 SSR/ISR build plan**

- **Directories (City/Role/Genre):** ISR with *revalidate: 300–900s* depending on city activity; pre‑render top 200 city/role combos.
- **Profiles/Studios:** SSR with *revalidate: 300s*; if completeness \< threshold or NSFW band \>= 2, render **SFW gate + noindex**.
- **Guides:** pure static builds, trigger rebuild on edit (CMS).

**Fallbacks:** bots see server‑rendered paginated HTML (not infinite scroll) with *rel="next/prev"* pagination links.
