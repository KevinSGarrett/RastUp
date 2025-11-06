---
id: TD-567
title: "**1.3.17 Acceptance criteria — mark §1.3 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-567-1317-acceptance-criteria-mark-13-final-only-when-all-true\TD-567-overview.md"
parent_id: 
anchor: "TD-567"
checksum: "sha256:fb719222bf5335c9bd9d94ba6b2e361c57c25325ebaaee8f6b1fa0915647f195"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-567"></a>
## **1.3.17 Acceptance criteria — mark §1.3 FINAL only when ALL true**

2772. IB, RTB, and Smart Invite flows work end‑to‑end with calendar blocks and chat threads.

NonTechBlueprint

2773. Checkout attaches and signs the correct **contract pack**; documents are retained with the order.

NonTechBlueprint

2774. Funds are charged and held on platform balance; **release/payout** logic respects completion + review windows; tipping supported.

NonTechBlueprint

2775. Cancellation & reschedule policies compute correct refunds/penalties; provider cancellations penalize reputation and (if repeated) fees.
2776. Disputes route to Admin casework with evidence; outcomes apply refunds/payouts; Stripe chargebacks are tracked.
2777. Webhooks are idempotent; retries safe; audit trails complete.
2778. Costs remain within launch posture (single PSP; serverless infra; no third‑party workflow SaaS).

# **§1.4 — Messaging, Inbox & Collaboration — Full Technical Spec (Part 1)**

**Purpose.** Deliver a **Unified Inbox** that powers safe, auditable collaboration across **People** and **Studios** with **Message Requests gating**, **Action Cards** (reschedule, extras, approvals, proofs, expense, mark‑complete, dispute, safety flag), **Quiet Hours/Do‑Not‑Disturb**, **push/email notifications & digests**, and **anti‑circumvention nudges**—exactly mirroring your non‑technical blueprint. This section will be delivered in multiple parts; I won’t exit §1.4 until it is ≥99.9% complete.
