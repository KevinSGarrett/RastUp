---
id: TD-590
title: "**1.4.J Safety, attachments & retention**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-590-14j-safety-attachments-retention\TD-590-overview.md"
parent_id: 
anchor: "TD-590"
checksum: "sha256:e212ed4a217de3bf513366d2413257055dea0e3b90d87a10f92ab0f1bb50a93f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-590"></a>
## **1.4.J Safety, attachments & retention**

- **Attachment scanning**: S3 → Lambda AV scan; quarantine until clean; images re‑encoded; videos metadata verified.
- **Safe‑Mode previews**: SFW enforcement in inbox previews (blur/label when required).

NonTechBlueprint

- **Retention**: keep messages indefinitely; auto‑archive stale threads after 180 days (user can unarchive); purge spam after N days.
