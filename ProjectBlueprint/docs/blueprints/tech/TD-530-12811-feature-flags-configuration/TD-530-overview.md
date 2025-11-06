---
id: TD-530
title: "**1.28.11 Feature flags & configuration**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-530-12811-feature-flags-configuration\TD-530-overview.md"
parent_id: 
anchor: "TD-530"
checksum: "sha256:0523d223cff541cddfaac5f78f197c91b2cd9397c2992b3816b5402a2543677b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-530"></a>
## **1.28.11 Feature flags & configuration**

- Flags stored in DynamoDB with typed schema; read‑only, signed JSON snapshot exposed via CDN to clients for fast boot.
- Secrets stored in AWS Secrets Manager; no keys in code.
