---
id: TD-211
title: "**1.13.B High‑level architecture**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-211-113b-highlevel-architecture\TD-211-overview.md"
parent_id: 
anchor: "TD-211"
checksum: "sha256:e5b002a375990963149797586c08ebfb013b33a269026d9971fc7a5fbeda53ca"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-211"></a>
## **1.13.B High‑level architecture**

- Ingestion (near real‑time):

  - App & web clients send event envelopes to an authenticated **/collect** endpoint (AppSync → Lambda).
  - Backend services publish **domain events** (the ones we enumerated across §§1.3–1.12) to **EventBridge**.
  - External providers (Stripe, e‑sign, SES) → webhook ingesters → normalized events → EventBridge.

- Transport & storage:

  - **EventBridge → Kinesis Firehose → S3** (partitioned *dt=YYYY‑MM‑DD/hour=HH*).
  - Bronze stored as **newline‑delimited JSON**; compaction jobs produce **Parquet** for Athena.
  - **Glue Catalog** defines tables for Bronze and Silver; partitions registered automatically.

- Transformations:

  - **AWS Glue** (PySpark) or **Athena CTAS** jobs to build Silver/Gold on schedules (NRT 5–15 min for ops, hourly/daily for heavy facts).
  - **dbt‑core on Athena** for modeling, tests, and lineage (optional but recommended).

- Serving & BI:

  - **Athena** for ad‑hoc; **QuickSight** (SPICE) for dashboards; optional **Metabase** (open‑source) on top of Athena/Redshift.
  - **Ops pages** in Admin use **materialized views** (Athena CTAS to Parquet) for low‑latency.
