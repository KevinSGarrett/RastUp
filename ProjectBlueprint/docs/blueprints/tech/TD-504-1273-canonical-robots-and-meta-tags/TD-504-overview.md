---
id: TD-504
title: "**1.27.3 Canonical, robots, and meta tags**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-504-1273-canonical-robots-and-meta-tags\TD-504-overview.md"
parent_id: 
anchor: "TD-504"
checksum: "sha256:0bdcfc775f28dc4ea6bf0643572b17869548a93f3cd32a5d48c5f9c0cc87f50a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-504"></a>
## **1.27.3 Canonical, robots, and meta tags**

**Recommended path:** *web/lib/seo/canonical.ts*

*export function canonicalFor(url: URL) {*  
*const allowed = new Set(\['page','sort'\]);*  
*const kept = \[...url.searchParams.entries()\].filter((\[k\]) =\> allowed.has(k));*  
*const params = new URLSearchParams(kept);*  
*url.search = params.toString();*  
*return url.toString();*  
*}*  

**robots meta logic:**

- Public directories, SFW profiles/studios: *\<meta name="robots" content="index,follow"\>*
- Any page where Safe‑Mode OFF or NSFW band \>= 2 would appear: *\<meta name="robots" content="noindex,nofollow"\>*
- Paid content pages (Fan‑Sub): always *noindex,nofollow*.

**Recommended path:** *web/pages/\_app.tsx* (excerpt)

*const robots = isIndexable(routeCtx) ? "index,follow" : "noindex,nofollow";*  
*\<head\>\<meta name="robots" content={robots} /\>\</head\>*
