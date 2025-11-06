---
id: TD-234
title: "**1.13.K (expanded) — Admin & Runbooks**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-234-113k-expanded-admin-runbooks\TD-234-overview.md"
parent_id: 
anchor: "TD-234"
checksum: "sha256:4a0da0fd2e3223786da716b0f1d89187ccfac732449f5d13b650b7006fa81820"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-234"></a>
## **1.13.K (expanded) — Admin & Runbooks**

- **Schema registry site** generated from */schemas/\*\*.json* + dbt docs; published to internal Amplify Hosting.

- **Backfill runner**: Step Functions flow

  - pick date range
  - CTAS Bronze→Silver for those partitions
  - rebuild impacted Gold models
  - verify Great Expectations → if fail, auto‑rollback.

- **Incident runbooks**:

  - *Pipeline lag*: pause heavy CTAS, widen Firehose buffers, notify Ops, degrade BI refresh to daily only.
  - *High Athena spend*: identify runaway queries in workgroup metrics; kill/limit; pin dashboards to SPICE only.
  - *Schema break*: move invalid events to *\_bad* quarantine; hotfix schema or add adapter transform.
