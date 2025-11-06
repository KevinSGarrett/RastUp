---
id: TD-466
title: "**1.23.14 Cost & Scale Posture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-466-12314-cost-scale-posture\TD-466-overview.md"
parent_id: 
anchor: "TD-466"
checksum: "sha256:a9996bd1fd7fb5416492e1b2ff39faba79e8ec1d878db259c73b1ad31a99c24f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-466"></a>
## **1.23.14 Cost & Scale Posture**

- **DynamoDB** on‑demand at launch; auto‑scales; write units sized from expected messages/day.
- **AppSync** pay‑per‑connection; set connection idle timeouts; compress payloads.
- **S3** for attachments; lifecycle transition to IA after 30–90 days; delete thumbnails if threads archived (configurable).
- **Typesense** reuse cluster (shared with search) for message snippets; cap stored fields.
