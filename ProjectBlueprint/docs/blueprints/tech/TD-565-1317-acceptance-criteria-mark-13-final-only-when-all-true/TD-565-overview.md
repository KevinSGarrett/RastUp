---
id: TD-565
title: "**1.3.17 Acceptance criteria — mark §1.3 FINAL only when ALL true**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-565-1317-acceptance-criteria-mark-13-final-only-when-all-true\TD-565-overview.md"
parent_id: 
anchor: "TD-565"
checksum: "sha256:1995e9514387158bc22ae22a2e9dd96218b9cc77ebf4ce4216e604e861447272"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-565"></a>
## **1.3.17 Acceptance criteria — mark §1.3 FINAL only when ALL true**

2707. IB, RTB, and Smart Invite flows work end‑to‑end with calendar blocks and chat threads.

NonTechBlueprint

2708. Checkout attaches and signs the correct **contract pack**; documents are retained with the order.

NonTechBlueprint

2709. Funds are charged and held on platform balance; **release/payout** logic respects completion + review windows; tipping supported.

NonTechBlueprint

2710. Cancellation & reschedule policies compute correct refunds/penalties; provider cancellations penalize reputation and (if repeated) fees.
2711. Disputes route to Admin casework with evidence; outcomes apply refunds/payouts; Stripe chargebacks are tracked.
2712. Webhooks are idempotent; retries safe; audit trails complete.
2713. Costs remain within launch posture (single PSP; serverless infra; no third‑party workflow SaaS).

# **§1.3 — Booking, Payments & Disputes — Full Technical Spec**

**Purpose.** Implement fast, trustworthy booking with Instant Book (IB) and Request‑to‑Book (RTB), private **Smart Invite** to multiple profiles, escrowed payments, transparent cancellation, and a fair, auditable dispute process. This section translates your non‑technical scope (Service Profile, Packages, Extras, Usage License, IB/Smart Invite, checkout contracts, escrow, payout timing, and disputes) into build‑ready detail.

NonTechBlueprint
