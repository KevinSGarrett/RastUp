---
id: TD-53
title: "**1.3.Z Acceptance Criteria — mark §1.3 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-53-13z-acceptance-criteria-mark-13-final-only-when-all-true\TD-53-overview.md"
parent_id: 
anchor: "TD-53"
checksum: "sha256:144bbc8386777a71ae90004dc7728bda1e0911a92e17f9d024f83d730e1a6b0c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-53"></a>
## **1.3.Z Acceptance Criteria — mark §1.3 FINAL only when ALL true**

374. **Atomic LBG**, **Docs-before-Pay**, **Deposits**, **Amendments**, **Refunds**, **Disputes**, **Payouts/Reserves**, **Acceptance Window** all function as specified.
375. Receipts (leg + group) include line items, taxes, doc hashes, amendments, refunds, payouts.
376. Scheduler/Step Functions drive end-to-end state reliably; retries are idempotent.
377. Finance **daily close** runs green for 5 consecutive days; variances gate payouts correctly.
378. Admin consoles (Finance/Support/Trust/City Ops) provide the actions above with immutable audits and dual approvals where required.
379. Telemetry is complete (events listed across 1.3); observability dashboards green.
380. p95 **Checkout ≤ 2s**, payout drain ≤ 15m, and costs stay within budget alarms.
381. The **full E2E test matrix** passes in CI and sandbox (card/ACH/3DS/atomic/cancel/dispute/recon).

# **§1.4 — Messaging & Project Panel (threads, action cards, deliverables, approvals)**

**Goal.** Implement a role‑aware, booking‑aware messaging system with a **Project Panel** embedded in the conversation: briefs, moodboard, shot list, files (previews + external manifests), docs & e‑sign status, expenses/amendments, and one‑click **action cards** (reschedule, extras, overtime, deliverable approvals, deposit claims, dispute/report). This section gives the **full technical spec**—data models, APIs, realtime behavior, file pipeline, moderation/safety rules, notifications, admin tooling, telemetry, SLOs, tests, and cost levers.

We will not move to §1.5 until §1.4 hits your **99.9% coverage** bar.
