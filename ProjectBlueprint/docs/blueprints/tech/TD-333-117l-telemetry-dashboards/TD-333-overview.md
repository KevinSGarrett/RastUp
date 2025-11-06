---
id: TD-333
title: "**1.17.L Telemetry & dashboards**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-333-117l-telemetry-dashboards\TD-333-overview.md"
parent_id: 
anchor: "TD-333"
checksum: "sha256:95dcd8313d7de31bfaaabd5cc0eb59b0484d141c14d9f3a12ef6d7aa32c78f26"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-333"></a>
## **1.17.L Telemetry & dashboards**

- **Core Web Vitals (field)**: RUM beacon reports LCP/CLS/INP by route, device, city; dashboard in QuickSight.
- **Crawl health**: sitemap submission status, indexed pages over time, top coverage errors (ingested via Search Console API exporter).
- **SEO funnel**: impressions → clicks → profile views → checkout start → confirmation (hooked into §1.13).
- **Alerting**: LCP regression \> 10% WoW on top city pages, spike in non‑200 response ratio, robots blocking anomalies.
