---
id: TD-132
title: "**1.8.L Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-132-18l-performance-cost\TD-132-overview.md"
parent_id: 
anchor: "TD-132"
checksum: "sha256:7a4c9f463cc93103101d9c6a73008d98fa014e438df78edbcc1655d0a9cc5fc1"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-132"></a>
## **1.8.L Performance & cost**

- **Reads** dominate; aggregates cached and invalidated on write.
- **Writes** relatively small; classifiers run serverless with concurrency caps.
- S3 storage minimal (preview photos); lifecycle to Intelligent-Tiering after 30 days.
