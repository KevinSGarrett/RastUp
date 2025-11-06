---
id: TD-170
title: "**1.10.X Telemetry, dashboards & SLOs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-170-110x-telemetry-dashboards-slos\TD-170-overview.md"
parent_id: 
anchor: "TD-170"
checksum: "sha256:93e192e5fb2a55835f3998c59afd6a7df586dddb5f682830cbce342270eaf352"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-170"></a>
## **1.10.X Telemetry, dashboards & SLOs**

**X.1 Metrics**

- Volume per channel, delivery %, soft/hard bounces, complaints, opens, clicks, unsubscribe rate, digest suppression %, send latency (event→queue→provider), cost per 1k sends (email/SMS), push invalid token rate.

**X.2 SLOs**

- Event→queued **≤ 150 ms p95**; queued→provider **≤ 1 s p95**.
- Delivery rate ≥ **98.5%** on transactional (ex‑bounces/complaints).
- Complaint rate ≤ **0.1%**; hard bounce ≤ **0.3%** rolling 7‑day.
- In‑app notification fetch **≤ 120 ms p95**.

**X.3 Alerts**

- Bounce/complaint spikes by provider; quiet‑hours scheduler backlog; SMS spend anomalies; push invalid token surges.
