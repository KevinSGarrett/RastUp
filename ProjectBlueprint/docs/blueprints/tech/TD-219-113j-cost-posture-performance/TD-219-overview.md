---
id: TD-219
title: "**1.13.J Cost posture & performance**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-219-113j-cost-posture-performance\TD-219-overview.md"
parent_id: 
anchor: "TD-219"
checksum: "sha256:83c843f345ab41ea400b85bc485e1a27bf598a4cc4f03f7f68f8c80f3823f2a8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-219"></a>
## **1.13.J Cost posture & performance**

- **S3**: Parquet + Snappy compression; partition by date (and city when cardinality helps); lifecycle after 90–180 days to colder storage.
- **Athena**: avoid scanning whole buckets—push **partition filters**; ctables store sorted small files for today’s partitions; limit CTAS output file sizes (256–512 MB).
- **Glue**: small DPU reservations; scale jobs by schedule; stop on idle; reuse code across models.
- **QuickSight**: prefer SPICE extracts (charged per user/capacity) with scheduled refresh; keep visuals focused.
- **Redshift Serverless**: disabled at launch; enable behind a flag if Athena latency becomes a blocker; start at smallest RPU with pause when idle.
