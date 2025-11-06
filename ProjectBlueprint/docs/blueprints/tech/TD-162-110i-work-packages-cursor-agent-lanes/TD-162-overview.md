---
id: TD-162
title: "**1.10.I Work packages (Cursor agent lanes)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-162-110i-work-packages-cursor-agent-lanes\TD-162-overview.md"
parent_id: 
anchor: "TD-162"
checksum: "sha256:f828455945f8b8e8b29100b2dc7ef27779d00ddd1f7942aa76e8d23283447cf0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-162"></a>
## **1.10.I Work packages (Cursor agent lanes)**

- **Agent B — Comms Core**  
  WP‑COMMS‑01: SQL for templates/prefs/quiet‑hours/messages/suppression/in‑app.  
  WP‑COMMS‑02: Comms Router & Renderer (MJML compile, variable resolver, locale fallback).  
  WP‑COMMS‑03: Channel workers (SES, APNs/FCM, SNS/Twilio) with idempotency & retries.
- **Agent A — Web (Settings & UX)**  
  WP‑WEB‑COMMS‑01: Notification Preferences UI + Quiet Hours UI + List‑Unsubscribe landing.  
  WP‑WEB‑COMMS‑02: In‑app notification center (bell, unread counts, pagination, mark read).
- **Agent C — Integrations/Deliverability**  
  WP‑DLV‑01: Domain auth (SPF/DKIM/DMARC), bounce/complaint webhooks, suppression list processor.  
  WP‑DLV‑02: Link tracking & UTM, open pixel (email only) with privacy guardrails.
- **Agent D — Admin & QA**  
  WP‑ADM‑COMMS‑01: Template manager (versioning, preview, publish with dual approval for legal/security).  
  WP‑QA‑COMMS‑01: Full test matrix automation (see Part 2), synthetic provider sandboxes.
