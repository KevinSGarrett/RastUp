---
id: TD-87
title: "**1.5.R Acceptance criteria — mark §1.5 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-87-15r-acceptance-criteria-mark-15-final-only-when-all-true\TD-87-overview.md"
parent_id: 
anchor: "TD-87"
checksum: "sha256:04ae73b1ca3a9904261b46058aefd41d4e91702c3b799a5f0f41160efaf3b0ca"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-87"></a>
## **1.5.R Acceptance criteria — mark §1.5 FINAL only when ALL true**

550. Clause & Template library supports versioning, city/role gates, previews, and dual approvals for publish.
551. Pack assembly resolves variables, renders PDFs, creates envelopes, and enforces Docs‑Before‑Pay across both legs in an LBG.
552. Completed envelopes change pack status to *signed*; payment capture proceeds; receipts reference doc IDs and **post‑sign hashes**.
553. Re‑issue logic invalidates packs when scope/time/location/party/deposit changes; prior PDFs retained and auditable.
554. Hashing verified; S3 storage and retention policies active; legal hold works.
555. Messaging displays doc status and action prompts; Admin can search/void/resend with full audits.
556. Telemetry complete; evidence export works; error taxonomy produced for all failure modes.
557. Costs within budget; renderer concurrency capped; e‑sign envelopes within allowance.

# **§1.6 — Trust, Verification & Background Checks**

*(ID Verification · Age Gate (18+) · Trusted Pro (BG) · Social Verification · Risk Signals · Badges & Gating · Admin & Audits · Privacy)*

**Purpose.** Design and implement the full trust layer: identity verification (IDV) for 18+ and Instant Book eligibility; optional FCRA-compliant background checks for the **Trusted Pro** badge; verified-social signals; risk scoring & throttles; and the badges/gates that flow into search, booking, messaging, and payouts. This section includes data models, adapters, APIs, admin tools, privacy and retention, telemetry, error taxonomy, tests, SLOs, and cost controls. We will not move on until §1.6 meets your 99.9% bar.
