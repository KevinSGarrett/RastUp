---
id: TD-301
title: "**1.16.L Performance & cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-301-116l-performance-cost\TD-301-overview.md"
parent_id: 
anchor: "TD-301"
checksum: "sha256:edc7b8442ee8704cda55ca33cca6daf88654291b7eca96d8d7008264680fd1b6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-301"></a>
## **1.16.L Performance & cost**

- **Schedulers**: EventBridge scheduled Lambdas (cron & daily); no long‑running workers.
- **Search**: pre‑compute **match hashes** to reduce index scans for alerts; use Typesense filters efficiently.
- **Storage**: S3 for sharecards, lifecycle → Intelligent‑Tiering @30d; CloudFront cache hits ≥95%.
- **Email**: SES shared IPs; digest batches to keep costs low.
- **Dynamo**: TTL‑based dedupe tables; RCU/WCU caps.
- **Budgets**: alarms on SES sends/day, Lambda duration, Dynamo capacity.
