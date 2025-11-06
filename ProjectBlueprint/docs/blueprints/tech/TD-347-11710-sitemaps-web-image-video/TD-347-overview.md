---
id: TD-347
title: "**1.17.10 Sitemaps (Web, Image, Video)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-347-11710-sitemaps-web-image-video\TD-347-overview.md"
parent_id: 
anchor: "TD-347"
checksum: "sha256:9d605c1749e14cf4bd6b42a89e0e585874d3f3e7833351df66321d84d0cb3e94"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-347"></a>
## **1.17.10 Sitemaps (Web, Image, Video)**

**Strategy**

- **Index file** */sitemap.xml* linking to segmented sitemaps (People A‑Z, Studios by city, Case Studies, Cities).
- **Image sitemaps** for people/studios (SFW thumbnails only).
- **Video sitemap** for case studies with videos.

**Artifact — Image sitemap entry (template)**  
*Recommended path:* *web/sitemaps/templates/image-url.xml*

*\<url\>*  
*\<loc\>https://rastup.com/studio/{{slug}}\</loc\>*  
*\<image:image\>*  
*\<image:loc\>https://cdn.rastup.com/sfw/{{imageFile}}\</image:loc\>*  
*\<image:title\>{{imageTitle}}\</image:title\>*  
*\<image:caption\>{{imageCaption}}\</image:caption\>*  
*\</image:image\>*  
*\</url\>*
