---
id: TD-339
title: "**1.17.2 Canonicalization & URL Normalization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-339-1172-canonicalization-url-normalization\TD-339-overview.md"
parent_id: 
anchor: "TD-339"
checksum: "sha256:d8deca0832df4d79c8864c5d6e192e8b031f7597989aac92170fa5c3c69f17c2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-339"></a>
## **1.17.2 Canonicalization & URL Normalization**

**Rules**

- **Single canonical per entity** (profile */p/{handle}*, studio */s/{slug}*, package */p/{handle}/packages/{slug}*).
- Strip ***utm\_\******,** ***ref*****, session and cache‑busting** params via 301 to canonical.
- Normalize: lowercase paths, **no trailing slash** (choose one; below assumes none), collapse multiple slashes, decode percent‑encoding.
- City context for hubs: canonical as **query param** (*/models?city=houston*), not path segments—prevents duplicate city pages.

**Artifacts**

**A) Canonical redirect middleware (Next/Edge pseudocode)**  
*Recommended path:* *web/middleware.ts*

*const CANON_QP_BLOCKLIST = \["utm_source","utm_medium","utm_campaign","utm_term","utm_content","ref","gclid","fbclid"\];*  
*export function middleware(req) {*  
*const url = new URL(req.nextUrl);*  
*// Normalize case and trailing slash*  
*url.pathname = url.pathname.toLowerCase().replace(/\\+\$/,'').replace(/\\{2,}/g,'/');*  
*// Strip tracking params*  
*for (const p of CANON_QP_BLOCKLIST) url.searchParams.delete(p);*  
*// If changed, 301 to canonical*  
*if (url.toString() !== req.nextUrl.toString()) return Response.redirect(url, 301);*  
*return;*  
*}*  

**B) Canonical link builder (server)**  
*Recommended path:* *web/lib/canonical.ts*

*export const canonicalFor = (entity) =\>*  
*entity.kind === "person" ? \`https://rastup.com/\${entity.role}/\${entity.slug}\` :*  
*entity.kind === "studio" ? \`https://rastup.com/studio/\${entity.slug}\` :*  
*entity.kind === "package" ? \`https://rastup.com/\${entity.role}/\${entity.slug}/packages/\${entity.pkgSlug}\` :*  
*\`https://rastup.com/\`;*
