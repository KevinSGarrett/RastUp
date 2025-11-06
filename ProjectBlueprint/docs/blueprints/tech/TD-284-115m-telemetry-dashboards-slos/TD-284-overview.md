---
id: TD-284
title: "**1.15.M Telemetry, dashboards & SLOs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-284-115m-telemetry-dashboards-slos\TD-284-overview.md"
parent_id: 
anchor: "TD-284"
checksum: "sha256:7e1c7c4278ad061881810a1506ec93e717d2034e536c36f286255a092164ff4c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-284"></a>
## **1.15.M Telemetry, dashboards & SLOs**

**SLOs**

- First response: **≤ 8h** (normal), **≤ 1h** (urgent).
- Resolution: **≤ 72h** average for non‑chargeback; **≤ network deadline** for chargebacks.
- SLA breach rate **\< 5%** rolling 30 days.

**Dashboards**

- Volume by type/subtype & city; backlog aging; SLA breach trend.
- Refund rate by reason; goodwill spend; chargeback **win rate**; DMCA volume/outcomes.
- Payout holds applied/released and exposure at risk.

**Events**

- *support.case.open\|assign\|status_change\|close*, *support.refund.proposed\|succeeded\|failed*,
- *support.hold.apply\|release*, *chargeback.notified\|represented\|won\|lost*,
- *dmca.received\|hidden\|restored*.
