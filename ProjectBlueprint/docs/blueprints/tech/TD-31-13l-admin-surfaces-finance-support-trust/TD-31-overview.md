---
id: TD-31
title: "**1.3.L Admin surfaces (Finance, Support, Trust)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-31-13l-admin-surfaces-finance-support-trust\TD-31-overview.md"
parent_id: 
anchor: "TD-31"
checksum: "sha256:c194416c24b8bb794f44ee756ef12793e41ddf9465caaf379beed84441ad9285"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-31"></a>
## **1.3.L Admin surfaces (Finance, Support, Trust)**

- **Finance**: payment/refund ledger, payout scheduler, reserve settings, tax commits, deposit claim approvals, reconciliation status, daily close.
- **Support**: cancel/partial refund tools with policy simulator; resend receipts; check‑in/out timeline; evidence export.
- **Trust**: dispute management, evidence pack builder, doc pack audit, chargeback trend analytics.

All actions are audited (actor, reason, before/after) and gated by RBAC + two‑person approvals where money moves.
