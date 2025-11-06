---
id: TD-418
title: "**1.20.N Telemetry & crash reporting**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-418-120n-telemetry-crash-reporting\TD-418-overview.md"
parent_id: 
anchor: "TD-418"
checksum: "sha256:0c784333be42f83514b4295e97b6ea9ca69cf1557304f212ca62bed5d855109b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-418"></a>
## **1.20.N Telemetry & crash reporting**

- PWA: first‑party analytics via *navigator.sendBeacon*; CWV field data per route; soft‑error logging.
- RN: minimal crash reporter (e.g., Sentry‑like equivalent can be added later) but keep SDKs lean; at launch, start with OS crash logs + our event pipeline.
- **Mobile event taxonomy** aligns with §1.13 (e.g., *app.install*, *pwa.install_prompt*, *push.opt_in*, *message.send*, *upload.start/success*, *booking.start/complete*).
