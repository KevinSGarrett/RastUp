---
id: TD-117
title: "**1.7.N Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-117-17n-performance-cost\TD-117-overview.md"
parent_id: 
anchor: "TD-117"
checksum: "sha256:f79a020357aa2471a628575b579c488ddc18c29dfe923d142f8c135a0388ff7a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-117"></a>
## **1.7.N Performance & cost**

- **Server path**: ad selection is a lightweight filter + sample on a cached active list per *(surface, city, role)*; no heavy joins.
- **Cache**: refresh active campaigns every 30–60s; query‑result cursors keep rotation stable.
- **Storage**: events compacted hourly; cold storage lifecycle after 90 days.
- **Compute**: fraud scoring runs in near‑real‑time with modest concurrency; batch re‑processing off‑peak.
