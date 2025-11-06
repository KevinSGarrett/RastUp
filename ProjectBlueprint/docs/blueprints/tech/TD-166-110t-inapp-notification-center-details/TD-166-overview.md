---
id: TD-166
title: "**1.10.T In‑app Notification Center (details)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-166-110t-inapp-notification-center-details\TD-166-overview.md"
parent_id: 
anchor: "TD-166"
checksum: "sha256:a33b4f6dbe194de9ec954b08953a417d3154ada3b0d5c328d729c7fb88b0c9f0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-166"></a>
## **1.10.T In‑app Notification Center (details)**

**T.1 Data & pagination**

- *inapp_notification* (already defined) stores immutable items; add indices for *(user_id, created_at desc)*.
- Pagination: cursor by *(created_at, id)* to ensure stable ordering.

**T.2 UX contract**

- **Bell** icon shows unread count; badge hides during DND/quiet hours logic (but count still increments).
- **Grouping**: coalesce similar events (e.g., “3 new thread updates”).
- **Actions**: “Mark all read”, per‑item “Mark read”, per‑group clear.
- **Pinning**: high‑priority items (security, legal) appear pinned until dismissed.

**T.3 Retention**

- Default retention 90 days; archive older items (user can fetch via “Load older” until 1 year, then cold storage).
- Privacy: no sensitive PII in in‑app bodies; deep link to secure pages.
