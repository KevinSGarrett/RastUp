---
id: TD-394
title: "**1.19.6 RTL support & logical CSS**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-394-1196-rtl-support-logical-css\TD-394-overview.md"
parent_id: 
anchor: "TD-394"
checksum: "sha256:3ddb787fd0f6d4f3efa52eca1d4f113739aea5d1ad05bdbff461741d927c7a53"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-394"></a>
## **1.19.6 RTL support & logical CSS**

**Base CSS logical props**  
**Recommended path:** *web/styles/rtl.css*

*html\[dir="rtl"\] { direction: rtl; }*  
*.card { padding-inline: 16px; margin-inline: 8px; }*  
*.icon-chevron { transform: scaleX(var(--dir-mult, 1)); }*  
*html\[dir="rtl"\] .icon-chevron { --dir-mult: -1; }*  

**Mirroring images/icons:** use bidirectional icons or auto‑mirrored SVG; avoid text baked into images.
