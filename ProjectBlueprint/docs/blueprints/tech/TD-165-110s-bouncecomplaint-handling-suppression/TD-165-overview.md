---
id: TD-165
title: "**1.10.S Bounce/complaint handling & suppression**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-165-110s-bouncecomplaint-handling-suppression\TD-165-overview.md"
parent_id: 
anchor: "TD-165"
checksum: "sha256:bf7b174214eefd0e09c1d8a6cf3ccc9e78a4499fb5e2fb15993dbad77f918a3c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-165"></a>
## **1.10.S Bounce/complaint handling & suppression**

**S.1 Webhooks → suppression list**

- **Hard bounce** or **complaint** → write *comms_suppression* (*channel='email'*, *reason='hard_bounce'\|'complaint'*, *address_hash=SHA256(email)*), set *comms_message.status='bounced'\|'complained'*.
- **Soft bounces** (4xx) → retry with backoff; if ≥3 within 72h → convert to suppression (*reason='manual'*) pending user correction.

**S.2 Unsubscribe & re‑permissioning**

- **List‑Unsubscribe**: one‑click HTTPS endpoint sets *comms_pref.email.promotions=false* (and any non‑critical marketing categories).
- Re‑permission only via explicit user action in settings; no automatic re‑enable after a bounce/complaint.

**S.3 Global blocklist**

- Maintain **platform blocklist** (legal/compliance). Any send to these addresses is dropped with *status='suppressed'* and audited.
