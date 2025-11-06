---
id: TD-86
title: "**1.5.Q Work packages (Cursor 4‑agent lanes)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-86-15q-work-packages-cursor-4agent-lanes\TD-86-overview.md"
parent_id: 
anchor: "TD-86"
checksum: "sha256:1e3e7a97b4059e9517759bf3ad2dc47335f5e2e806ab797d552dbc262b8dadc6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-86"></a>
## **1.5.Q Work packages (Cursor 4‑agent lanes)**

- **Agent A — Docs CMS & Templates**  
  WP‑DOCS‑01: SQL for *doc_clause*, *doc_template*, *doc_pack*, *doc_instance*, *doc_sign_event*.  
  WP‑DOCS‑02: Clause & Template authoring UI in Admin (create/edit/publish, preview with variable binding).  
  WP‑DOCS‑03: Variable resolver library (maps from *leg*/*LBG*/profile/brief to variables).
- **Agent B — Rendering & Storage**  
  WP‑REND‑01: Markdown→PDF renderer (headless) with layout json; S3 write; SHA‑256 hash.  
  WP‑REND‑02: Evidence export builder (ZIP + JSON manifest).
- **Agent C — E‑sign Adapter**  
  WP‑SIGN‑01: Envelope create/void; signer link flows; webhooks with HMAC verify; status mapper.  
  WP‑SIGN‑02: Retry and error handling; email change + re‑send; expiration handling.
- **Agent D — Product Integration**  
  WP‑CHK‑DOCS‑01: Checkout gating (Docs‑Before‑Pay) + GraphQL mutations (*createDocPack*, *markDocSigned*).  
  WP‑MSG‑DOCS‑01: Messaging Project Panel “Docs & e‑sign” tab + action cards.  
  WP‑QA‑DOCS‑01: Full test matrix above in CI & sandbox.
