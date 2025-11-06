---
id: TD-577
title: "**1.4.10 Observability, KPIs & Cost**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-577-1410-observability-kpis-cost\TD-577-overview.md"
parent_id: 
anchor: "TD-577"
checksum: "sha256:3f3317ef23223dfa734a8fb0d8face5d2060f2991dfdabe3735f2383f4fb82a8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-577"></a>
## **1.4.10 Observability, KPIs & Cost**

- **Events**: *msg.request.open\|accept\|decline\|block*, *msg.send*, *card.send\|accept\|decline*, *inbox.search*, *push.send\|open*, *digest.send\|open*.
- **KPIs**: request→accept rate, time‑to‑first‑response, card completion rate, reschedule success, extras attach rate, dispute rate, block/report rate.
- **Cost controls**: S3 lifecycle (attachments → IA in 90d), thumbnail transforms cached, push/email via pay‑as‑you‑go (Pinpoint/SES).
