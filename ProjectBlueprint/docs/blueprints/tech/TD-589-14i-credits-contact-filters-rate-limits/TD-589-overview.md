---
id: TD-589
title: "**1.4.I Credits, contact filters & rate limits**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-589-14i-credits-contact-filters-rate-limits\TD-589-overview.md"
parent_id: 
anchor: "TD-589"
checksum: "sha256:0f6ca936ffdf10ee60fec5f91be772d27de14b3acc741fd50ce00d02f88303c7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-589"></a>
## **1.4.I Credits, contact filters & rate limits**

- **New conversation credits** per month (configurable); **bonus credits** for verified users (as defined elsewhere). Replies and confirmed booking threads are **unlimited**.

NonTechBlueprint

- **Contact filters**: talent may require **ID‑Verified only**, minimum details (date, city, budget) before a Message Request is allowed to bypass.

NonTechBlueprint

- **Rate limits** (Dynamo token bucket):

  - New users: 3 new conversations/hour; 20/day.
  - Verified: 10/hour; 100/day.
  - Bursts punished (cool‑down) if \>2 similar messages in 60s.
