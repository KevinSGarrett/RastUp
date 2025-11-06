---
id: TD-343
title: "**1.17.6 Image & Video SEO (SFW‑only)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-343-1176-image-video-seo-sfwonly\TD-343-overview.md"
parent_id: 
anchor: "TD-343"
checksum: "sha256:c226312d2c8e6003875e572d6a9d60264204d6f357523a02401f16b089cd049b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-343"></a>
## **1.17.6 Image & Video SEO (SFW‑only)**

**Images**

- Filenames: kebab‑case with role/city cues, e.g., *houston-photographer-jane-doe-portrait-01.webp*.
- Always set *width*/*height* to prevent CLS; use *srcset*/*sizes*; serve AVIF/WebP with JPEG fallback.
- *alt* text: short literal description; **no keyword stuffing**; for decorative images, *alt=""*.
- Lazy‑load below‑the‑fold; **preload** the hero (LCP) image.

**Videos** (case studies, studio tours)

- Use ***VideoObject*** JSON‑LD with SFW poster frames; duration and upload date.
- Provide **captions**; avoid auto‑play with sound (INP risk).

**Artifact — VideoObject JSON‑LD**  
*Recommended path:* *web/lib/ldjson/video.ts*

*export const videoLd = (v) =\> ({*  
*"@context": "*[*https://schema.org*](https://schema.org)*",*  
*"@type": "VideoObject",*  
*"name": v.title,*  
*"description": v.desc,*  
*"thumbnailUrl": \[v.posterSfw\],*  
*"uploadDate": v.publishedISO,*  
*"duration": \`PT\${v.durationSeconds}S\`,*  
*"contentUrl": v.hlsPublicPreview*  
*});*
