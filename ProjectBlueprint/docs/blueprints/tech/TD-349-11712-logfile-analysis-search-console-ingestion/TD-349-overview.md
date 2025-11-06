---
id: TD-349
title: "**1.17.12 Log‑File Analysis & Search Console Ingestion**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-349-11712-logfile-analysis-search-console-ingestion\TD-349-overview.md"
parent_id: 
anchor: "TD-349"
checksum: "sha256:e4c6f4d9f9230d545a16e9ded56077da9cabc9d9c32b7ca1204aa08ca434298e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-349"></a>
## **1.17.12 Log‑File Analysis & Search Console Ingestion**

- Export **edge logs** (CloudFront) + **app access logs** to S3; model into Athena (§1.13).
- Build **crawl dashboard**: hits by bot UA, 200/3xx/4xx, coverage of sitemaps, crawl waste on non‑indexable pages.
- Ingest **GSC** performance/coverage via API to the lake; build SEO funnel (impressions→clicks→profile views→checkout).

**Artifact — Athena table (simplified)**  
*Recommended path:* *data/sql/cf_logs.sql*

*CREATE EXTERNAL TABLE IF NOT EXISTS cf_logs (*  
*dt string, time string, x_edge_location string, sc_status int, cs_method string,*  
*cs_uri_stem string, cs_uri_query string, cs_user_agent string, cs_referer string*  
*)*  
*PARTITIONED BY (date string)*  
*ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'*  
*LOCATION 's3://logs/cloudfront/';*
