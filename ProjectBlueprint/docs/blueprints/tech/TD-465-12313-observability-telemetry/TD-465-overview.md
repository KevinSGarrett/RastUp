---
id: TD-465
title: "**1.23.13 Observability & Telemetry**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-465-12313-observability-telemetry\TD-465-overview.md"
parent_id: 
anchor: "TD-465"
checksum: "sha256:db1dd396ee0b2cc35a5d6953e056892d74acef506f2a3a38fc87f35eab7ba615"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-465"></a>
## **1.23.13 Observability & Telemetry**

- **Events:** *msg.thread.open*, *msg.start*, *msg.send*, *msg.delivered*, *msg.read*, *msg.attachment.upload*, *msg.action.submit/accept/decline*, *msg.report*, *msg.block*.
- **KPIs:** response time, response rate, request acceptance rate, booking conversion from thread, dispute rate, spam flag rate, reversal rate after appeal.
- **SLOs:** p95 send‑to‑deliver \< 600 ms; p95 initial inbox load \< 300 ms; push delivery \< 10 s.
