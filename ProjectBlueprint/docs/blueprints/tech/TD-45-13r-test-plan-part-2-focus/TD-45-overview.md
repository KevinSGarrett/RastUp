---
id: TD-45
title: "**1.3.R Test Plan (Part 2 focus)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-45-13r-test-plan-part-2-focus\TD-45-overview.md"
parent_id: 
anchor: "TD-45"
checksum: "sha256:7fb6c880294f6b42dbc6111c6152178d6c58ceefb4499a11f0be671aa3ff376a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-45"></a>
## **1.3.R Test Plan (Part 2 focus)**

301. **Change Order** (pre‑session): positive delta → taxes re‑quoted → payment collected → amendment row saved → receipts updated.
302. **Overtime** (in‑session): card incremental capture; fall back to second PI if incremental capture not allowed; ACH always second PI.
303. **Cancellation bands**: simulate 96h/48h/12h cases; verify buyer refund and seller retention match policy; tax refunds correct.
304. **Partial LBG cancel**: cancel studio leg; talent leg remains; group receipt shows correct summary; buyer warned.
305. **Acceptance window**: buyer accepts vs auto‑accept; payouts queued accordingly (Part 3 will verify payouts).
306. **Deposit claim**: studio files claim; approve partial capture; receipts updated and buyer notified.
307. **Receipts**: verify line math and PDF rendering; hashes stored; email links valid.
308. **Webhooks mapping**: Stripe refund, dispute created, e‑sign completed → normalized events created once (idempotency).
