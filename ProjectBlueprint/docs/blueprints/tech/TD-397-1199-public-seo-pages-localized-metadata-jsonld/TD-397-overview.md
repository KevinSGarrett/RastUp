---
id: TD-397
title: "**1.19.9 Public SEO pages: localized metadata & JSON‑LD**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-397-1199-public-seo-pages-localized-metadata-jsonld\TD-397-overview.md"
parent_id: 
anchor: "TD-397"
checksum: "sha256:0bdc76995a431e1ba3899cde0a7b1616047c533d3d52dc4d00c1366b63af0d10"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-397"></a>
## **1.19.9 Public SEO pages: localized metadata & JSON‑LD**

**Head helper**  
**Recommended path:** *web/seo/meta.tsx*

*export function PageMeta({ titleKey, descKey, params }) {*  
*const title = t(titleKey, params);*  
*const desc = t(descKey, params);*  
*return (*  
*\<\>*  
*\<title\>{title}\</title\>*  
*\<meta name="description" content={desc} /\>*  
*{/\* SFW OG image per §1.17 \*/}*  
*\</\>*  
*);*  
*}*  

**Localized JSON‑LD:** translate *headline*, *description*, *addressLocality* etc., but **never** substitute 18+ images.
