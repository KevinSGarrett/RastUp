---
id: TD-252
title: "**1.14.P Work packages (Cursor 4‑agent lanes)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-252-114p-work-packages-cursor-4agent-lanes\TD-252-overview.md"
parent_id: 
anchor: "TD-252"
checksum: "sha256:f65744697b075a860bcd945bbeee9aea849e9a2fed93dc287d1674794859a475"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-252"></a>
## **1.14.P Work packages (Cursor 4‑agent lanes)**

- **Agent C — Domain/API**  
  WP‑FS‑01: SQL for *fansub\_\** tables; GraphQL resolvers; entitlement cache.  
  WP‑FS‑02: Action cards for requests; tie‑ins to §1.4 flows; receipts & lineage.
- **Agent B — Payments/Taxes**  
  WP‑FS‑PAY‑01: Stripe Billing subs; PPV/tips PaymentIntents; Connect payouts; tax adapter lines.  
  WP‑FS‑PAY‑02: Webhooks normalization (*invoice.\**, *payment_intent.\**, *charge.\**) + idempotency.
- **Agent A — Web**  
  WP‑FS‑WEB‑01: Creator page, PPV catalog, subscribe/tip/buy flows; thread UI for requests.  
  WP‑FS‑WEB‑02: Watermarked preview renderer; entitlement‑aware media components.
- **Agent D — Safety/Admin/QA**  
  WP‑FS‑SAFE‑01: NSFW scan + watermarking pipeline; anticircumvention in captions.  
  WP‑FS‑ADM‑01: DMCA/moderation/finance consoles; audits.  
  WP‑FS‑QA‑01: Full test matrix automation; synthetic earnings reports.
