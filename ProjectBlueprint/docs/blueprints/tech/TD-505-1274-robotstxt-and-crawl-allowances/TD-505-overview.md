---
id: TD-505
title: "**1.27.4 robots.txt and crawl allowances**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-505-1274-robotstxt-and-crawl-allowances\TD-505-overview.md"
parent_id: 
anchor: "TD-505"
checksum: "sha256:7540a7a7f4cf79de34546e831f8cfb4d997e6a764828d2cc2f5dcb03e3cf09ae"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-505"></a>
## **1.27.4 robots.txt and crawl allowances**

**Recommended path:** *web/public/robots.txt*

*User-agent: \**  
*Disallow: /api/*  
*Disallow: /checkout/*  
*Disallow: /messages*  
*Disallow: /fan/*  
*Disallow: /\*?\*safeMode=false*  
*Disallow: /\*?\*any=\**  
*Disallow: /\*?\*all=\**  
*Allow: /tx/*  
*Sitemap:* [*https://rastup.com/sitemap.xml*](https://rastup.com/sitemap.xml)

We explicitly disallow combinatorial filters and Safe‑Mode‑off queries.
