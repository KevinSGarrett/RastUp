---
id: TD-494
title: "**1.26.8 Observability & SLAs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-494-1268-observability-slas\TD-494-overview.md"
parent_id: 
anchor: "TD-494"
checksum: "sha256:562a2cc75315aad45b991ef6635e65a0994039ca875e810685d0bff97d8173aa"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-494"></a>
## **1.26.8 Observability & SLAs**

- **Event taxonomy:** *admin.login*, *admin.case.create\|act\|close*, *admin.user.suspend\|reinstate*, *admin.refund\|hold\|release*, *admin.template.publish*, *admin.search.pin*, *admin.synonym.upsert*, *admin.flag.set*, *admin.audit.view*.

- **Dashboards:** case backlog & aging, time‑to‑first‑response, time‑to‑resolution, dispute outcomes, refund rate, appeal win rate, moderator workload, finance queue length, search pin performance.

- SLOs:

  - Reports triaged p95 ≤ 4h (business hours)
  - Disputes resolved p95 ≤ 5 days
  - Finance webhook→action p95 ≤ 15m
  - Audit write availability 99.99%
