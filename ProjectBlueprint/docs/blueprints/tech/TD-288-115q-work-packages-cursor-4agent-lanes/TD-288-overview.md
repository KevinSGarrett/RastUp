---
id: TD-288
title: "**1.15.Q Work packages (Cursor 4‑agent lanes)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-288-115q-work-packages-cursor-4agent-lanes\TD-288-overview.md"
parent_id: 
anchor: "TD-288"
checksum: "sha256:0c9519ecf1bbac862388a1ee5c16a63d321728a6ca9b3f0245ffaab453626d88"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-288"></a>
## **1.15.Q Work packages (Cursor 4‑agent lanes)**

- **Agent C — Domain/API**  
  WP‑SUP‑01: SQL for *support\_\** tables; GraphQL queries/mutations; timeline stitching.  
  WP‑SUP‑02: Refund calculator (ties to §1.3/§1.9); payout hold service.
- **Agent B — Payments/Chargebacks**  
  WP‑SUP‑CB‑01: Chargeback ingest + representment builder; GL side‑effects.  
  WP‑SUP‑DMCA‑01: DMCA intake + hide/restore endpoints; evidence vault.
- **Agent A — Web (Support Center)**  
  WP‑SUP‑WEB‑01: Case list/detail UI, message composer, uploads; booking/order context launchers.  
  WP‑SUP‑WEB‑02: Admin consoles (queues, macros, SLA board, batch actions).
- **Agent D — Comms/QA**  
  WP‑SUP‑COMMS‑01: SES inbound/outbound bridge; templates and quiet hours (hooks §1.10).  
  WP‑SUP‑QA‑01: Test automation for all flows; synthetic chargeback timelines.
