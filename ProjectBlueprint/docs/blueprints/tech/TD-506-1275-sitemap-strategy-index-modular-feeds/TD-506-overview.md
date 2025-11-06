---
id: TD-506
title: "**1.27.5 Sitemap strategy (index + modular feeds)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-506-1275-sitemap-strategy-index-modular-feeds\TD-506-overview.md"
parent_id: 
anchor: "TD-506"
checksum: "sha256:6afd12cb352002b5c595d9536107ab2ffe8c36ebd6d15d47e1d97d87a6289172"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-506"></a>
## **1.27.5 Sitemap strategy (index + modular feeds)**

- **Sitemap index**: */sitemap.xml* → links to:

  - */sitemaps/cities.xml* (city directories)
  - */sitemaps/people-{A..Z}.xml* (profiles by initial)
  - /sitemaps/studios-{A..Z}.xml
  - */sitemaps/guides.xml* (content hubs)

**Generation:** nightly job (Lambda) using Aurora queries and Typesense to fetch only **indexable** (SFW & published) slugs.  
**Changefreq/priority:** profiles/studios *weekly*, directories *daily* while active.

**Recommended path:** *web/pages/sitemap.xml.ts*

*export async function GET() {*  
*const xml = await buildSitemapIndex();*  
*return new Response(xml, { headers: {'Content-Type':'application/xml'}});*  
*}*
