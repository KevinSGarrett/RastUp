---
id: TD-575
title: "**1.4.8 Notifications & Digests**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-575-148-notifications-digests\TD-575-overview.md"
parent_id: 
anchor: "TD-575"
checksum: "sha256:d695880674cd97ec30dd6c742876703bfb101d49b006995ecbbfe8272009756c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-575"></a>
## **1.4.8 Notifications & Digests**

- **Real‑time**: push (FCM/APNs) + email for mentions, card requests, gate accepts, RTB actions, booking confirmations, reschedules.
- **Digest**: daily/weekly depending on preference; sections (*New requests*, *Pending approvals*, *Upcoming bookings* with ICS links).
- **ICS attachments**: confirmed bookings include **.ics** to add to calendars. (Two‑way sync is covered in §1.24 Phase 2.)
- **Preference schema** (per user): channel toggles per event type; **Quiet Hours** window; override for “booking day” messages.
