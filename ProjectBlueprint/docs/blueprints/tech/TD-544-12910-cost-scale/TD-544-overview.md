---
id: TD-544
title: "**1.29.10 Cost & scale**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-544-12910-cost-scale\TD-544-overview.md"
parent_id: 
anchor: "TD-544"
checksum: "sha256:82bf90e3de284f0a521189c0fd73844af24c222699c115d1ccc9a15861f00c0f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-544"></a>
## **1.29.10 Cost & scale**

- S3 + CloudFront only (no DAM SaaS). Lifecycle: originals to IA after 30 days; web renditions after 90 days.
- Rekognition moderation optional toggle by environment.
- Typesense fields: title, city, genres, role, recency; small documents (no full captions indexing at launch).
