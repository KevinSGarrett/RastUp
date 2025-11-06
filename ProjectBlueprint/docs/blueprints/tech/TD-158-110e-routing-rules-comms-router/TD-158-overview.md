---
id: TD-158
title: "**1.10.E Routing rules (Comms Router)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-158-110e-routing-rules-comms-router\TD-158-overview.md"
parent_id: 
anchor: "TD-158"
checksum: "sha256:43cca4a74b3ab5f58c2a2c8297e47dfd03c11caa2b0c75a07290bc466b882f95"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-158"></a>
## **1.10.E Routing rules (Comms Router)**

**Input**: domain event *{name, user_id(s), cause_ref, payload}*.

**Steps**

952. **Select template(s)** for event + role (buyer/seller/admin).
953. **Apply preferences** and **quiet hours** for the recipient (skip or schedule).
954. **Dedupe** using *dedupe_key* (e.g., *THREAD:{id}:{minute}* for rapid message bursts; *BOOKING:{lbg}:{state}*).
955. **Batch**: gather multiple low‑priority items into digest (e.g., daily message digest).
956. **Render** with locale detection; push to channel queues with idempotency keys.

**Critical overrides**

- Security, legal, receipts ignore quiet hours and opt‑out (except SMS jurisdiction where consent is required—then fallback to email/in‑app).
- If a channel is suppressed (hard bounce/complaint), auto‑fallback to in‑app + email to an alternate verified address (if present).
