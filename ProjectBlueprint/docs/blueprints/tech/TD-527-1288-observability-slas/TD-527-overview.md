---
id: TD-527
title: "**1.28.8 Observability & SLAs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-527-1288-observability-slas\TD-527-overview.md"
parent_id: 
anchor: "TD-527"
checksum: "sha256:dad15625b87cc3274d69a03a0161f7c39e87420063bbc09954471021c761686c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-527"></a>
## **1.28.8 Observability & SLAs**

- **Events:** *admin.login*, *admin.case.create\|act\|close*, *admin.user.suspend\|reinstate*, *admin.refund\|hold\|release*, *admin.search.pin*, *admin.synonym.upsert*, *admin.template.publish*, *admin.flag.set*, *admin.audit.view*.

- **Dashboards:** case backlog/aging, time‑to‑first‑response, time‑to‑resolution, dispute outcomes, refund rate, moderator workload, finance queue length, pin performance.

- SLOs:

  - Report triage p95 ≤ **4h** (business hours)
  - Dispute resolution p95 ≤ **5 days**
  - Finance webhook→action p95 ≤ **15m**
  - Audit write availability **99.99%**
