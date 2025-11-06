---
id: TD-68
title: "**1.4.O Work packages (Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-68-14o-work-packages-cursor-agents\TD-68-overview.md"
parent_id: 
anchor: "TD-68"
checksum: "sha256:66351f7248df450ba0b691f232b1eab770740d9ec55916dc3a1e92d22a7e4cb5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-68"></a>
## **1.4.O Work packages (Cursor agents)**

- **Agent B — API / Realtime**  
  WP‑MSG‑01: DDB table & GSIs; resolvers for inbox, thread, messages, project panel; subscriptions.  
  WP‑MSG‑02: Presence/typing TTL flows; read receipts.
- **Agent C — Actions / Domain hooks**  
  WP‑ACT‑01: Implement action cards + state machines; integrate §1.3 services (reschedule, amendments, deposit, dispute).  
  WP‑ACT‑02: Webhook handlers → normalized events → DDB/Aurora updates.
- **Agent A — Web**  
  WP‑WEB‑MSG‑01: Inbox UI, thread UI (role chips, Safe‑Mode), Project Panel tabs with optimistic updates.  
  WP‑WEB‑MSG‑02: Upload UI → scanned previews; external manifest attach; action card components.
- **Agent D — Moderation/QA**  
  WP‑MOD‑01: Anticircumvention filters + UI nudges; T&S console; audit trails.  
  WP‑QA‑MSG‑01: Full test matrix; fixtures; golden snapshots.
