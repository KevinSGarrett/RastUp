---
id: TD-186
title: "**1.11.N Telemetry & lineage**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-186-111n-telemetry-lineage\TD-186-overview.md"
parent_id: 
anchor: "TD-186"
checksum: "sha256:c4b479ecb1279b10f438718154ac698996add2afbefcdab21d05f593ee211e75"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-186"></a>
## **1.11.N Telemetry & lineage**

- studio.create\|update\|publish\|unpublish
- studio.rate.add\|update\|delete
- studio.media.add\|blocked\|delete
- studio.verification.submitted\|approved\|rejected\|revoked
- studio.blackout.add\|delete
- *studio.quote.request\|response* (with amounts)
- Correlate with owner *user_id* and booking *leg_id* where relevant.

Dashboards: verified share by city, quote success rate, conflict rates, amenity filter usage, conversion.
