---
id: TD-323
title: "**1.17.B URL topology (stable, human‑readable)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-323-117b-url-topology-stable-humanreadable\TD-323-overview.md"
parent_id: 
anchor: "TD-323"
checksum: "sha256:e5e474dcfbe8915e7186800889ad1c0790053569fd3e34970239d643363992f5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-323"></a>
## **1.17.B URL topology (stable, human‑readable)**

**People (Service Profiles)**

- */p/{handle}* (canonical)
- */p/{handle}/packages/{slug}* (canonical for package detail)
- */p/{handle}?utm\_\** → 301 → */p/{handle}*

**Studios**

- */s/{slug}* (studio listing)
- */s/{slug}/rates* (rate table, SFW)

**Cities & discovery**

- */city/{city-slug}* — city hub (SFW)
- */city/{city-slug}/people* — SFW grid (server‑filtered)
- */city/{city-slug}/studios* — SFW studios list
- */stories/{slug}* — case studies/guides (SFW hero)

**System**

- */robots.txt*, */sitemap.xml* (+ segmented sitemaps)
- */legal/{tos\|privacy\|dmca}* (indexable)
- */help/\** (indexable FAQ)
- Anything transactional (*/checkout*, */messages*, */admin*) → *noindex, nofollow*.
