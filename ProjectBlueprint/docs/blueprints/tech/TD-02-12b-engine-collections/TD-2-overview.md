---
id: TD-2
title: "**1.2.B Engine & collections**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-02-12b-engine-collections\TD-2-overview.md"
parent_id: 
anchor: "TD-2"
checksum: "sha256:a9b4b6c063fdc7605ec5c6ca74c1e1a478d353db6bc033cdad4a7d625ae4114d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-2"></a>
## **1.2.B Engine & collections**

We implement the Search Service to be **engine‑agnostic** with a default **Typesense** deployment (low fixed cost), and an optional **OpenSearch** backend behind the same adapter.

**Collections**

- *people_v1* — one document per **Service Profile** (SP).
- *studios_v1* — one document per **Studio**.

**Sharding/partitioning**

- Logical shards by *city* and *role* (we keep physical topology simple at MVP—one node w/ replica or small serverless OCU cap).
- Daily compaction to prune stale docs; reindex per city when policy/flags change.
