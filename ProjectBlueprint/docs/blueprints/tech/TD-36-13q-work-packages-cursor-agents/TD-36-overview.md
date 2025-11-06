---
id: TD-36
title: "**1.3.Q Work packages (Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-36-13q-work-packages-cursor-agents\TD-36-overview.md"
parent_id: 
anchor: "TD-36"
checksum: "sha256:759a24efcf164484f455833f961161f863641e27afaf83671321ce6a08812a38"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-36"></a>
## **1.3.Q Work packages (Cursor agents)**

- **Agent B (Domain/API)**  
  WP‑CHK‑01: SQL migrations for lbg/leg/charge/split/deposit/tax_txn/refund/dispute/payout/amendment.  
  WP‑CHK‑02: GraphQL mutations/queries/subscriptions (see 1.3.I).  
  WP‑CHK‑03: Step Functions saga + Lambda handlers; idempotency store.
- **Agent C (Integrations)**  
  WP‑INT‑PAY‑01: Stripe adapter (PI, SI, transfers, refunds, disputes) + webhooks + mappers.  
  WP‑INT‑TAX‑01: Tax adapter (quote/commit/refund).  
  WP‑INT‑ESIGN‑01: Doc pack builder (Dropbox Sign/DocuSign) + gating.
- **Agent A (Web)**  
  WP‑WEB‑CHK‑01: Checkout UI with LBG container, attach‑studio pane, docs step, payment step, acceptance window UI, receipts.  
  WP‑WEB‑CHK‑02: Overtime/extras flows from thread/project panel.
- **Agent D (Admin & QA)**  
  WP‑ADM‑FIN‑01: Finance panel (ledger, payouts, reserves, refunds).  
  WP‑ADM‑SUP‑01: Support tools (policy simulator, cancel/refund wizard).  
  WP‑QA‑CHK‑01: E2E scenarios 1–10; synthetic Stripe/Tax/ESign sandboxes.
