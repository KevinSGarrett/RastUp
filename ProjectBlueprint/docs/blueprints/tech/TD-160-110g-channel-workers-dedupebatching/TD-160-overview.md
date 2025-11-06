---
id: TD-160
title: "**1.10.G Channel workers & dedupe/batching**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-160-110g-channel-workers-dedupebatching\TD-160-overview.md"
parent_id: 
anchor: "TD-160"
checksum: "sha256:5a23141a25b6fa94803d6de60ed071d22278ce101b395ccd1ceccbfa956087bc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-160"></a>
## **1.10.G Channel workers & dedupe/batching**

**Email worker (SES)**

- Receives rendered HTML + text, sets **SPF/DKIM domains**, **List‑Unsubscribe** headers, adds **message‑id** for threading, queues to SES.
- Stores a copy of rendered HTML in S3 and writes *comms_message*.

**Push worker**

- Sends to device tokens (APNs/FCM) with *collapse_key* to dedupe on device; respects per‑device language; drops invalid tokens and prunes from *comms_tokens*.

**SMS worker**

- Enforces country gating and high cost flags; trims body to length; inserts short links; checks suppression and opt‑in.
- Templated STOP/HELP footer where required.

**Batching**

- **Message digest**: compile last N thread updates into one email if user inactive for M minutes; include counts and deep links.
- **Review reminders**: send at 24 h and 72 h unless user already reviewed; cancel if review arrives.

**Idempotency & replays**

- All workers use *(template_name, user_id, cause_ref, version)* as idempotency key; retries do not duplicate sends or audits.
