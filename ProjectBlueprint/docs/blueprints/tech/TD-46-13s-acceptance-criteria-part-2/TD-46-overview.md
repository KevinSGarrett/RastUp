---
id: TD-46
title: "**1.3.S Acceptance Criteria (Part 2)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-46-13s-acceptance-criteria-part-2\TD-46-overview.md"
parent_id: 
anchor: "TD-46"
checksum: "sha256:ba790a96673a25c308a84a9faf95f0b79932a27328a57596a46940e9fb2931e0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-46"></a>
## **1.3.S Acceptance Criteria (Part 2)**

We will mark **§1.3 (Part 2) COMPLETE** only when **all** are true:

- Change orders & overtime create amendment lines, collect payments properly, and re‑quote tax.
- Cancellation engine returns accurate band outcomes and executes refunds; partial LBG cancellation handled with clear UX and math.
- Acceptance window logic gates payouts correctly; auto‑accept on deadline.
- Deposit claim flow (auth → claim → capture/void) functions with audits and caps.
- Receipts (leg + group) render deterministically with tax and doc hashes.
- Webhook mappings produce normalized events idempotently.
- Part‑2 test suite green in CI and under sandbox smoke.
- No unexpected cost spikes (incremental captures vs new PIs measured; renderer concurrency capped).

# **§1.3 — Booking & Checkout**

**Part 3/3: Payouts & Reserves · Disputes & Evidence · Daily Close & Recon · Admin Consoles · Full E2E Test Matrix & SLOs**

This completes §1.3. We won’t move forward to §1.4 until you’re satisfied this sub-section is covered to your 99.9% bar.
