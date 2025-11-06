---
id: TD-187
title: "**1.11.O Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-187-111o-performance-cost\TD-187-overview.md"
parent_id: 
anchor: "TD-187"
checksum: "sha256:f3a0382ccb5d934a1b578a1c9b55bb4612173ab7225d1f04a32667a84bae84d6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-187"></a>
## **1.11.O Performance & cost**

- **Search**: small *studios_v1* index; cache results for 60–120s; availability buckets precomputed daily.
- **Storage**: S3 previews only; lifecycle to Intelligent‑Tiering after 30 days; delete orphans after 30 days.
- **Compute**: Lambdas for scans/transforms; quote engine runs in BFF with memoized rate lookups.
- **Maps/geo**: no heavy polygons at MVP; simple radius; pre‑computed city centroids.
