---
id: TD-59
title: "**1.4.F Presence, read receipts, typing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-59-14f-presence-read-receipts-typing\TD-59-overview.md"
parent_id: 
anchor: "TD-59"
checksum: "sha256:b99e757eb4133d165c6086850ab3c74cf9b7b098ceb5d86ce462186572d425dd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-59"></a>
## **1.4.F Presence, read receipts, typing**

- **Read receipts**: per participant, store *lastReadMsgId* and *lastReadAt*; messages with ts ≤ lastReadAt show as read.
- **Typing**: client emits ephemeral *typing=true* events throttle‑debounced; server writes presence TTL item; subscription broadcasts.
- **Online**: presence entries updated on ping; absences \> TTL means offline.
