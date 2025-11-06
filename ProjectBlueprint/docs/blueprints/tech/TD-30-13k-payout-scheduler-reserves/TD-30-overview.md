---
id: TD-30
title: "**1.3.K Payout scheduler & reserves**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-30-13k-payout-scheduler-reserves\TD-30-overview.md"
parent_id: 
anchor: "TD-30"
checksum: "sha256:c7c6f9907621e24e9cf5d60af3674e4d754b649ecce4502f4f4a84a8774dcf60"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-30"></a>
## **1.3.K Payout scheduler & reserves**

- Default payout policy: queue **on completion** (or acceptance window end).
- **Reserves** (first‑payout or risk‑flagged sellers): hold for *N* days configurable per seller; Admin can override.
- Stripe transfers created with idempotency and reconciled via webhooks.
