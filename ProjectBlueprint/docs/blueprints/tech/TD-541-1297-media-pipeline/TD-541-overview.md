---
id: TD-541
title: "**1.29.7 Media pipeline**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-541-1297-media-pipeline\TD-541-overview.md"
parent_id: 
anchor: "TD-541"
checksum: "sha256:0c316edb76c409ce1424470443e95422db8911fd2c7ccadb4bebc14f6a1aa28d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-541"></a>
## **1.29.7 Media pipeline**

- **Upload** via presigned S3; client sends *x-amz-meta-sfw-band*.
- **Lambda transform**: generate web‑optimized images (e.g., 1920/1280/640 px) + poster for video; strip EXIF; enforce max duration/size.
- **Moderation check (optional)**: Rekognition Moderation; if score \> threshold, set *status='pending'* and send to T&S queue.
- **Caching**: CloudFront with aggressive caching; image URLs include content hash to bust on update.
