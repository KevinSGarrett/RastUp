---
id: TD-65
title: "**1.4.L Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-65-14l-performance-cost\TD-65-overview.md"
parent_id: 
anchor: "TD-65"
checksum: "sha256:26a64b2602bffe2b3c2b922512b972f9d310a702141689d4847902e7dc460690"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-65"></a>
## **1.4.L Performance & cost**

- **DynamoDB**: write patterns append‑only; 1KB–8KB avg items; *MSG#ts#id* packs a capped body length (server truncates oversize with link to file). TTL on ephemeral presence rows.
- **AppSync**: subscriptions filtered by *threadId*; pagination uses forward cursors; cache last N cursors per user for back/forward UX.
- **S3/CF**: thumbnails & short previews only; lifecycle to Intelligent‑Tiering after 30 days; egress minimized.
- **Compute**: Lambdas on demand; webhook processors for action side‑effects; no always‑on servers.
