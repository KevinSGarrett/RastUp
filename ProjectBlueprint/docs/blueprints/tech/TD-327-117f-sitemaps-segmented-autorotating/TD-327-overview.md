---
id: TD-327
title: "**1.17.F Sitemaps (segmented, auto‑rotating)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-327-117f-sitemaps-segmented-autorotating\TD-327-overview.md"
parent_id: 
anchor: "TD-327"
checksum: "sha256:bc56afe9388f18c772d6af1a3abc9b8ec07c61bb49d91acdbf599bd50eaf1b70"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-327"></a>
## **1.17.F Sitemaps (segmented, auto‑rotating)**

**Recommended path:** *web/pages/sitemap.xml.ts* *(ISR function)*

- **Sitemap Index** */sitemap.xml* lists child maps:

  - */sitemaps/people-0.xml*, */sitemaps/people-1.xml*, … (sharded by hash)
  - */sitemaps/studios-0.xml*, …
  - */sitemaps/cities.xml*, */sitemaps/stories.xml*

- **lastmod** from *updated_at*; **changefreq** = *weekly* for people/studios, *daily* for cities during launch, *monthly* later.

- Exclude de‑published, unverified, or NSFW‑blocked pages.

**Example child sitemap XML**

*\<?xml version="1.0" encoding="UTF-8"?\>*  
*\<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\>*  
*\<url\>*  
*\<loc\>https://rastup.com/p/{{handle}}\</loc\>*  
*\<lastmod\>{{updatedISO}}\</lastmod\>*  
*\<changefreq\>weekly\</changefreq\>*  
*\<priority\>0.8\</priority\>*  
*\</url\>*  
*\</urlset\>*
