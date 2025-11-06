---
id: TD-223
title: "**1.13.N Test plan (CI + stage)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-223-113n-test-plan-ci-stage\TD-223-overview.md"
parent_id: 
anchor: "TD-223"
checksum: "sha256:9b31262efab9008558d515f7e673bc3cfee9afc00122fc894154814294e4f4cb"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-223"></a>
## **1.13.N Test plan (CI + stage)**

**Contracts & ingestion**

1347. Validate JSON Schemas for all events; generate fixtures; reject malformed example.
1348. Simulate Firehose → S3 path; partitions and Glue catalog creation verified.

**Transforms**  
3) Build Silver facts with sample events; ensure referential integrity; Great Expectations pass.  
4) Build Gold marts; compare against golden KPIs.

**Ops freshness**  
5) NRT materialized views update within 10 min under synthetic load.

**Experimentation**  
6) Bucketing sticky across login; exposure logged once; per‑variant metrics computed.

**Privacy & DSAR**  
7) DSAR tombstone leads to exclusion in Silver/Gold; Bronze read‑time exclusion works; legal hold override blocks purge.

**BI**  
8) SPICE extracts refresh; dashboards render within targets.

**Cost**  
9) Athena queries using partition filters; scanned bytes within budget; lifecycle transitions occur.
