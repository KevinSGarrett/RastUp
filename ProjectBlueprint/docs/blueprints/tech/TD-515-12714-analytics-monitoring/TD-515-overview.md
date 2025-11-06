---
id: TD-515
title: "**1.27.14 Analytics & monitoring**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-515-12714-analytics-monitoring\TD-515-overview.md"
parent_id: 
anchor: "TD-515"
checksum: "sha256:0c1a94a44ea21d304d46c2a3262016ca4a216dcd4ef958909736c814d6d2156e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-515"></a>
## **1.27.14 Analytics & monitoring**

- **GSC** integration per environment (prod only).
- **Event taxonomy:** *seo.published*, *seo.noindex_applied*, *seo.sitemap.emit*, *seo.redirect.hit*, *seo.ogimage.render*.
- **Dashboards:** impressions/clicks by city/role, CTR by directory, profile/studio coverage (% indexable), sitemap submission health, crawl errors over time.
- **Alarms:** surge in 5xx, sitemap job failures, spike in *noindex_applied* beyond baseline (could indicate Safe‑Mode flagging).
