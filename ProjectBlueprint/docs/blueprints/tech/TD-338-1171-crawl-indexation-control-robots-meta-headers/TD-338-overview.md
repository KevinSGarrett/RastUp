---
id: TD-338
title: "**1.17.1 Crawl & Indexation Control (robots, meta, headers)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-338-1171-crawl-indexation-control-robots-meta-headers\TD-338-overview.md"
parent_id: 
anchor: "TD-338"
checksum: "sha256:8a5b3e27406dea80baab8fd6fd4a5bf7ccf6265f4dac0ad385920254d6661ed7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-338"></a>
## **1.17.1 Crawl & Indexation Control (robots, meta, headers)**

**Goals:** Maximize crawl efficiency on **indexable SFW pages**, prevent indexing of **gated/duplicate/thin** pages, and make crawler behavior cheap.

**Policies**

- **Indexable:** Home, City & Role hubs, Search (unfiltered landing variants only), Service Profiles (non‑adult), Studios, Case Studies/Guides, Legal/Help.
- **Noindex:** age‑gated or login‑required pages; any URL with tracking params; filter‑heavy result pages; drafts/preview; checkout/messages/admin; duplicate “print/share” variants.
- **Disallow (robots.txt):** */admin/*, */messages/*, */checkout/*, internal asset routes, *\_next/*.

**Artifacts**

**A) robots.txt (inline)**  
*Recommended path:* *web/public/robots.txt*

*User-agent: \**  
*Disallow: /admin/*  
*Disallow: /messages/*  
*Disallow: /checkout/*  
*Disallow: /\_next/*  
*Disallow: /\*?\* \# parameters not for indexing*  
*Allow: /\$*  
*Allow: /city/*  
*Allow: /studios*  
*Allow: /studio/*  
*Allow: /models*  
*Allow: /photographers*  
*Allow: /videographers*  
*Allow: /creators*  
*Sitemap:* [*https://rastup.com/sitemap.xml*](https://rastup.com/sitemap.xml)

**B) X‑Robots‑Tag header policy (server)**  
*Recommended path:* *web/lib/robots.ts* (pseudocode)

*export function robotsHeaderFor(req, page) {*  
*if (page.isAdult \|\| page.requiresLogin \|\| page.isPreview) return "noindex, nofollow, noarchive";*  
*if (req.url.includes("?")) return "noindex, follow"; // filter/param variants are non-canonical*  
*return "index, follow";*  
*}*  

**C)** ***\<meta name="robots"\>*** **fallback (HTML)**  
Add a server‑generated *\<meta name="robots" content="..."\>* mirroring the header on all public templates.
