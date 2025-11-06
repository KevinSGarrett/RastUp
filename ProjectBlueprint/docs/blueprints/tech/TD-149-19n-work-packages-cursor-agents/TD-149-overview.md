---
id: TD-149
title: "**1.9.N Work packages (Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-149-19n-work-packages-cursor-agents\TD-149-overview.md"
parent_id: 
anchor: "TD-149"
checksum: "sha256:d284481eb501e592068eec89baf879464227d8841ef9169d0155563b6109efee"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-149"></a>
## **1.9.N Work packages (Cursor agents)**

- Agent B — Domain/Finance

  - WP‑FIN‑01: SQL migrations for *fee_ledger*, *wallet\_\**, *gl_entry*; fee calculator; MoR switch.
  - WP‑FIN‑02: GL writer and export; tie into §1.3 events; recon joins vs Stripe balance txns.

- Agent C — Integrations

  - WP‑FIN‑TAX‑01: Tax adapter for platform fee tax; refund handling.
  - WP‑FIN‑STR‑01: Stripe balance transaction fetcher; mapping; webhooks.

- Agent A — Web

  - WP‑WEB‑FIN‑01: Wallet UI and statements pages (buyer/seller).
  - WP‑WEB‑FIN‑02: Fee disclosure UI at checkout.

- Agent D — Admin & QA

  - WP‑ADM‑FIN‑01: Finance console (rules, wallet adjustments, GL exports, MoR).
  - WP‑QA‑FIN‑01: Full test matrix automation; golden GL snapshots.
