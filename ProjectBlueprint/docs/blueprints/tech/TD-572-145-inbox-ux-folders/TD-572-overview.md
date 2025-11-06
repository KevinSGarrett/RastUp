---
id: TD-572
title: "**1.4.5 Inbox UX & folders**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-572-145-inbox-ux-folders\TD-572-overview.md"
parent_id: 
anchor: "TD-572"
checksum: "sha256:3550b81408c19805332a27a0259a7acf1b3a8fb793410d7573d2af78073a12cb"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-572"></a>
## **1.4.5 Inbox UX & folders**

- **Folders** (*inbox_index.folder*):

  - **Action Required** — threads containing pending **Action Cards** or **Message Requests** awaiting the user.
  - **Bookings** — threads linked to confirmed orders or studio bookings.
  - **Offers/Requests** — RTB/Smart Invite negotiations not yet confirmed.
  - **Archived** — user archived.
  - **Spam/Blocked** — declined/blocked senders; auto‑purged after N days.

- **Thread list cells** show: avatar(s), subject, last snippet, badges (**IB**, **Verified Studio**, **Pending Request**, **Action Required**), unread count.

- **Search** (Typesense): participants, words in **text** and **card** payload titles, attachment names (not full contents), date range, “has:cardType”.

- **Pin & mute**: pin a thread to top; mute until a date/time or indefinitely; **Quiet Hours** globally suppress push between times (but keep inbox counters).
