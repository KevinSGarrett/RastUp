---
id: TD-37
title: "**1.3.R Acceptance criteria (mark §1.3 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-37-13r-acceptance-criteria-mark-13-final-only-when-all-true\TD-37-overview.md"
parent_id: 
anchor: "TD-37"
checksum: "sha256:8debedf6c4a6ccb11ef27d9fe480b90f1da827ab0222a62731127a78ebb53c24"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-37"></a>
## **1.3.R Acceptance criteria (mark §1.3 FINAL only when ALL true)**

233. **Atomic LBG**: Both legs confirm together or neither does; receipts & tax per leg; group summary rendered.
234. **Docs‑before‑pay** gating enforced; envelopes signed and hashed on receipts.
235. **Main charge captured** at confirm; **payouts delayed** until completion/acceptance window; studio **deposit** authorized separately and auto‑voided absent approved claim.
236. **Amendments** (extras/overtime) produce correct deltas and taxes; payments succeed for deltas; receipts updated.
237. **Refunds** computed per leg policy; processed; receipts amended; taxes refunded per provider rules.
238. **Disputes** lifecycle fully supported; evidence packs produced; outcomes reflected in ledgers.
239. **Reconciliation** daily close green 5/5 days; SLOs met for checkout and payout queue.
240. **Telemetry** events present end‑to‑end; idempotency verified; error taxonomy used.
241. **Cost** within budget; no always‑on compute; Stripe/Tax usage aligns with traffic.

# **§1.3 — Booking & Checkout**

**(Linked Booking Group, Docs‑before‑Pay, Taxes, Deposits, Refunds, Disputes)**

We will complete §1.3 in multiple parts. **Part 1** (previous reply) delivered: entities, state machines, core Aurora schema, checkout API contracts, “Docs before Pay,” charge/deposit strategy, Stripe/Tax adapters, error taxonomy, and Part‑1 test plan.  
Below is **Part 2/3**, which covers **change orders & overtime, cancellation/refund policy engine, acceptance windows, deposit claims, receipts, and webhook mapping** in full build detail. After Part 2, I’ll continue with **Part 3/3** (payouts, reserves/instant payouts, disputes evidence kits, daily close, admin consoles, full E2E test matrix).
