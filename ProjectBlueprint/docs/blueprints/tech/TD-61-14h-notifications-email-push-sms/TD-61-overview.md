---
id: TD-61
title: "**1.4.H Notifications (email, push, SMS)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-61-14h-notifications-email-push-sms\TD-61-overview.md"
parent_id: 
anchor: "TD-61"
checksum: "sha256:ce0e85389f204ebbe104a284cae986dff990e9bc771bfee2d84b35db3e44772a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-61"></a>
## **1.4.H Notifications (email, push, SMS)**

- **Triggers**: new message (not self), action card state change, deliverable posted, doc sign needed, acceptance window nearing end.
- **Quiet hours**: user‑settable; we queue non‑urgent notifications and send digest.
- **Templates**: centralized in Comms adapter; no sensitive content in SMS; deeplinks to thread/role context.
- **Backpressure**: dedupe within a 2–5 minute window; collapse multiple messages into a single notification.
