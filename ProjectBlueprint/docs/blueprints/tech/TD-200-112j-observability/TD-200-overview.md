---
id: TD-200
title: "**1.12.J Observability**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-200-112j-observability\TD-200-overview.md"
parent_id: 
anchor: "TD-200"
checksum: "sha256:f6d340dcff2db8c1889a0197b6ebd1fef378d6cc4f8b76fc5c27b9c8c3c2ec25"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-200"></a>
## **1.12.J Observability**

- **Metrics**: p50/p95/p99 latency, error rates per resolver/function, queue depths, index lag, OCU/RCU/ACU usage, Stripe/tax/e‑sign error rates.
- **Logs**: structured JSON; correlation ids from edge → backend; PII scrubbers.
- **Tracing**: X‑Ray/OpenTelemetry from AppSync → Lambda → DB.
- **Dashboards/Alerts**: SLO burn alerts, 5xx spikes, RDS ACU thrash, Dynamo throttles, WAF blocks, SES bounce/complaint spikes.
