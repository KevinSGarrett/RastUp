---
id: TD-583
title: "**1.4.C Presence, typing, delivery & read receipts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-583-14c-presence-typing-delivery-read-receipts\TD-583-overview.md"
parent_id: 
anchor: "TD-583"
checksum: "sha256:1661365cb57e921b66869456d3f46b8401edbb79bd2ba3585d2f7cd7ef8aa901"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-583"></a>
## **1.4.C Presence, typing, delivery & read receipts**

**Presence / typing**

- **DynamoDB** items: *msg_typing* (*pk=threadId*, *sk=userId*, TTL=10s).
- AppSync real‑time subscriptions broadcast **aggregate** typing states (user ID list + TTL).
- Display “Active 2h ago” using last message or last read.

NonTechBlueprint

**Delivery/Read**

- Delivery = server accepted & fanned out (✓✓ hollow).
- Read = recipient updated *thread_participant.last_read_ts* beyond message ts (✓✓ filled).
- Push open events can opportunistically update read state.
