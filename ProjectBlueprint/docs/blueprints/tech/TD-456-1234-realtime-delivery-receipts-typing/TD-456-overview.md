---
id: TD-456
title: "**1.23.4 Realtime Delivery, Receipts & Typing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-456-1234-realtime-delivery-receipts-typing\TD-456-overview.md"
parent_id: 
anchor: "TD-456"
checksum: "sha256:fe6b3442b11fa0f996d35b33267dc6406797f1f65a0bdfa246377479ff40eca6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-456"></a>
## **1.23.4 Realtime Delivery, Receipts & Typing**

- **Transport:** AppSync subscriptions (WebSocket).
- **Delivery states:** server writes *DELIVERED* state‑messages for recipients online; **read‑receipts** are explicit *markRead()* mutations that upsert *STATE* messages for *READ*. This maps to “sent ✓, delivered ✓✓, read ✓✓ filled.”

NonTechBlueprint

- **Typing:** ephemeral *STATE TYPING_ON/OFF* messages with TTL (15s), not persisted in Aurora.

**Lambda fan‑out:** Kinesis stream from *msg_messages* → Lambda → push (Pinpoint) when user offline; quiet hours respected (§1.20).
