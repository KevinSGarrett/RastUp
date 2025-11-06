---
id: TD-326
title: "**1.17.E Robots, Safe‑Mode, and** ***noindex*** **policy**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-326-117e-robots-safemode-and-noindex-policy\TD-326-overview.md"
parent_id: 
anchor: "TD-326"
checksum: "sha256:ff6a3c54a712726894efccdcdb11e3e1377b25ee9240849724389def6d92747c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-326"></a>
## **1.17.E Robots, Safe‑Mode, and** ***noindex*** **policy**

**robots.txt (template)**  
**Recommended path:** *web/public/robots.txt*

*User-agent: \**  
*Disallow: /admin/*  
*Disallow: /messages/*  
*Disallow: /checkout/*  
*Disallow: /\_next/*  
*Disallow: /\*?\**  
*Allow: /\$*   
*Allow: /city/*  
*Allow: /p/*  
*Allow: /s/*  
*Sitemap:* [*https://rastup.com/sitemap.xml*](https://rastup.com/sitemap.xml)

**X‑Robots‑Tag headers**

- Add *x-robots-tag: noindex, nofollow* to: drafts, preview routes, filtered result pages with query params, any page with *nsfw_band \>= 2* assets, and takedowns (DMCA).
- When Safe‑Mode is ON for a user, we still index the public SFW page; no 18+ assets are exposed in HTML/JSON‑LD.
