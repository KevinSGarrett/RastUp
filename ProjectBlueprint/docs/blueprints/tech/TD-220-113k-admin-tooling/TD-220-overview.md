---
id: TD-220
title: "**1.13.K Admin tooling**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-220-113k-admin-tooling\TD-220-overview.md"
parent_id: 
anchor: "TD-220"
checksum: "sha256:bb8b41de1a70798aa0360f882233b5755fccd45308f085b93b1c5a5f2cc03c23"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-220"></a>
## **1.13.K Admin tooling**

- **Schema registry** web UI (read‑only) listing events & versions with examples.
- **Backfill runner** for late events (replay a partition/day without clobbering existing Parquet).
- **Data dictionary** (Gold) with KPI definitions and SQL behind each card (single source of truth).
- **Access audit**: who queried which tables/partitions (CloudTrail/Lake Formation).
