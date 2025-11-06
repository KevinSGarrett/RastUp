---
id: TD-350
title: "**1.17.13 SEO‑Safe Experimentation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-350-11713-seosafe-experimentation\TD-350-overview.md"
parent_id: 
anchor: "TD-350"
checksum: "sha256:00fa858b4864121d2dbbd7809ffa95431ca8cb60a95a4ed2be1d048dd6865c30"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-350"></a>
## **1.17.13 SEO‑Safe Experimentation**

- **No client‑side cloaking**: bots must see a stable, indexable version (avoid A/B that changes indexable content for bots only).
- Keep experiments **server‑side** (SSR/ISR) or **non‑indexable** UI variations.
- For content experiments (titles, descriptions), roll out by **entity cohorts**; revalidate ISR pages on change.
