---
id: TD-509
title: "**1.27.8 Pagination & faceted navigation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-509-1278-pagination-faceted-navigation\TD-509-overview.md"
parent_id: 
anchor: "TD-509"
checksum: "sha256:665faaee93c14f5be906e8be1155538ce3ab6bd3add23a68cfdf907a7d7bb98a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-509"></a>
## **1.27.8 Pagination & faceted navigation**

- **Pagination:** use *?page=n*; include *rel="next"*/*rel="prev"*; noindex pages beyond a reasonable depth (e.g., *page \> 20* → *noindex,follow*).
- **Facets:** for UX we keep ANY/ALL filters (genres, amenities, price) but we **noindex** any URL with *any=*/*all=*; canonical points to base listing with the same city/role.
- **Sorts:** *sort* is canonically preserved; others are stripped.
