---
id: TD-224
title: "**1.13.O Work packages (Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-224-113o-work-packages-cursor-agents\TD-224-overview.md"
parent_id: 
anchor: "TD-224"
checksum: "sha256:501929c4bdbe3404babb3d5d5cb20c666dfd38283b5be8bc3c3bff552d1e152d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-224"></a>
## **1.13.O Work packages (Cursor agents)**

- **Agent C — Ingestion & Modeling**  
  WP‑DATA‑ING‑01: Event schemas & validation; EventBridge + Firehose S3 pipeline.  
  WP‑DATA‑ING‑02: Bronze→Silver ETL (Glue/Athena CTAS) + dbt project skeleton.
- **Agent B — Quality & Privacy**  
  WP‑DATA‑QTY‑01: Great Expectations suite; alerts; DSAR tombstone flow; Lake Formation grants.
- **Agent A — BI & Experiments**  
  WP‑DATA‑BI‑01: QuickSight datasets & dashboards; SPICE schedules; data dictionary.  
  WP‑EXP‑01: Assignment & exposure logging; guardrail metric jobs; analysis notebooks.
- **Agent D — Ops & Admin**  
  WP‑DATA‑OPS‑01: NRT materialized views (ops); backfill runner; schema registry UI.  
  WP‑COST‑01: Athena scanned‑bytes monitor; lifecycle & partition housekeeping jobs.
