---
id: TD-511
title: "**1.27.10 Media, OpenGraph & Twitter cards**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-511-12710-media-opengraph-twitter-cards\TD-511-overview.md"
parent_id: 
anchor: "TD-511"
checksum: "sha256:93032a9c79082ad75367c993a5ebf13b599e52c30ff6e429a300800a91b1c0ac"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-511"></a>
## **1.27.10 Media, OpenGraph & Twitter cards**

- **Profile OG image:** server‑side composited SFW headshot + name + city.
- **Studio OG image:** first SFW gallery image + title + city.
- **Guides OG:** hero image + title.
- All OG images render via an edge image function (Next Image Response) and cached.

**Recommended path:** *web/app/(public)/p/\[handle\]/opengraph-image.tsx*
