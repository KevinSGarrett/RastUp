---
id: TD-274
title: "**1.15.C Refund & dispute policy (deterministic kernels)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-274-115c-refund-dispute-policy-deterministic-kernels\TD-274-overview.md"
parent_id: 
anchor: "TD-274"
checksum: "sha256:65cfedb442bc3bea219ca8c6401c198d259acdcb8aaa1d93c9d4c53ccee280f7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-274"></a>
## **1.15.C Refund & dispute policy (deterministic kernels)**

**Bookings (people/studios) — base rules**

- If **buyer cancels** within policy bands (from §1.3 / *studio_policy*): refund = band % of subtotal + service tax; platform fees treated per §1.9 (usually refundable before completion, non‑refundable after; configurable).
- If **seller cancels/no‑show**: full refund; optional credit bonus.
- **Partial completion** (time & materials): proration by time delivered or milestone completion when docs reflect acceptance.
- **Damages (studio)**: deposit capture rules in §1.3.N; evidence required (photos, timestamps, invoices).

**Fan‑Sub (subscriptions, PPV, requests, tips)**

- **Subscriptions**: no retro refunds after period starts unless (a) *involuntary churn* reversal, or (b) service outage; dunning handled via Stripe.
- **PPV**: refundable if content not delivered/unavailable within X days; once **finals accessed**, refund eligibility drops unless quality dispute validated.
- **Requests**: if delivered and **buyer approved**, refund only via goodwill; if *revision loop* exhausted with unresolved defects, partial refund per tariff.
- **Tips**: non‑refundable except fraud.

**Escalation ladder**

1626. Auto‑decision (rules).
1627. Support agent decision with macros + reason codes.
1628. Supervisor dual‑approval when money impact \> threshold.
1629. Legal/T&S in DMCA or policy severe cases.
