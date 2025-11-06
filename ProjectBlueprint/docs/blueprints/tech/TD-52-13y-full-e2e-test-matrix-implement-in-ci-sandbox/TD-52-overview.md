---
id: TD-52
title: "**1.3.Y Full E2E Test Matrix (implement in CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-52-13y-full-e2e-test-matrix-implement-in-ci-sandbox\TD-52-overview.md"
parent_id: 
anchor: "TD-52"
checksum: "sha256:05a2548c9b1178b4f780127d2d7157e78b23c6e2ad03d96214d2b164c6f93350"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-52"></a>
## **1.3.Y Full E2E Test Matrix (implement in CI + sandbox)**

**Booking & Payment**

368. Single-leg, card.
369. LBG, card + studio deposit auth.
370. Single-leg, ACH (settlement wait).
371. 3DS challenge.
372. Atomic failure → no charge.
373. Retry with different method.

**Docs & Receipts**  
7. Doc pack gating; signatures required; hashes on receipts.  
8. PDF receipts (leg + group), immutable & downloadable.

**Amendments**  
9. Change order pre-session → delta math & tax.  
10. Overtime during session → incremental capture/new PI, receipts updated.

**Cancellations/Refunds**  
11. Provider cancel → full refund to buyer.  
12. Buyer cancel across 72h/48h/12h bands.  
13. Partial LBG cancel (one leg only).

**Acceptance & Payouts**  
14. Buyer accept → payouts queued; reserve applied.  
15. Auto-accept → payouts queued.  
16. Instant payout allowed vs denied (risk).  
17. Payout webhook sync to *paid*.

**Disputes**  
18. Dispute open → evidence build → submit → won.  
19. Dispute lost → clawback; receipts/Gold reflect.

**Recon & Close**  
20. Daily close green.  
21. Inject small variance → payouts paused → adjustment → green.  
22. Webhook duplication → idempotent handling.

**Performance**  
23. Checkout p95 \< 2s with tax/3DS mix.  
24. Payout queue drain \< 15 min on completion spikes.

**Cost**  
25. Renderer throttling; OpenSearch/Typesense calls within budget; Stripe/Tax cost alarms quiet.
