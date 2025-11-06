---
id: TD-585
title: "**1.4.E Digest generation & batching**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-585-14e-digest-generation-batching\TD-585-overview.md"
parent_id: 
anchor: "TD-585"
checksum: "sha256:e89997471322726c3e299deeb284462c9f47fb8784e53e95a4ad6a6b10b35a1d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-585"></a>
## **1.4.E Digest generation & batching**

- **Daily** digest for active users; **weekly** for low‑activity (opt‑in per preferences).
- Sections: **New requests**, **Pending approvals (cards)**, **Upcoming bookings** (with ICS), **Files received**, **Unanswered messages**.

NonTechBlueprint

- **Timezone‑aware** send windows; quiet‑hours honor (see below).
- **De‑dup logic**: if a transactional email already sent \< N hours ago, show only a summary line.
