---
id: TD-76
title: "**1.5.G E‑sign adapter (Dropbox Sign / DocuSign)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-76-15g-esign-adapter-dropbox-sign-docusign\TD-76-overview.md"
parent_id: 
anchor: "TD-76"
checksum: "sha256:ed612f99ae111191ee3bc97f2754ebaeb76490a5ba08ebf0897045b8ef53c585"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-76"></a>
## **1.5.G E‑sign adapter (Dropbox Sign / DocuSign)**

**Adapter contract**

- *create_envelope(doc_id, signer_map, pdf_s3)* → returns *envelope_id*, signer URLs (embedded) or email invites.
- *void_envelope(envelope_id, reason)* (on re‑issue).
- Webhooks: *envelope.sent*, *recipient.viewed*, *recipient.signed*, *envelope.completed*, *envelope.declined*, *envelope.voided*, *envelope.expired*.

**Security & idempotency**

- HMAC‑verified webhooks; store *provider_event_id*; dedupe.
- Signer links time‑limited; deep links route through our app to enforce auth and logging.

**Signer experience**

- In‑app embedded signing preferred; email fallback.
- Save/resume; clear error for expired/voided.

**Failure handling**

- *ENVELOPE_EMAIL_BOUNCE* → allow email change & re‑send (admin or user).
- *ENVELOPE_EXPIRED* → re‑issue pack (new doc version).
