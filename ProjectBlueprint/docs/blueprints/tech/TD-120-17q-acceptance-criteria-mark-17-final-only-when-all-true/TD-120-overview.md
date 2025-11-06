---
id: TD-120
title: "**1.7.Q Acceptance criteria (mark §1.7 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-120-17q-acceptance-criteria-mark-17-final-only-when-all-true\TD-120-overview.md"
parent_id: 
anchor: "TD-120"
checksum: "sha256:dcac5e2ab7658130a98242772f0d06141258bc63be26c69a9dfab9f26f09325f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-120"></a>
## **1.7.Q Acceptance criteria (mark §1.7 FINAL only when ALL true)**

722. Promoted units **never** bypass filters or city gates and are transparently labeled.
723. Density caps and diversity rules hold; blending preserves organic integrity and fairness.
724. Eligibility gates (IDV/completeness/safety) enforced; auto‑pause on breaches.
725. Budgets, pacing, pauses/resumes work; spend never exceeds budget caps.
726. Click validation rejects duplicates/bad traffic; make‑good credits issued; fraud dashboard active.
727. Billing (prepaid) works with Stripe; ledger equals Σ(valid_clicks × CPC); recon green.
728. Admin policy edits versioned with dual approval; suspensions & credits audited.
729. p95 selection latency within target; infra/costs within budget alarms for 48h synthetic load.

# **§1.8 — Reviews & Reputation**

*(per-entity scopes · write rules · fraud controls · weighting & decay · surfacing · moderation & appeals · admin · telemetry · tests · cost)*

**Purpose.** Implement a trustworthy reputation system that reflects real, recent performance, scoped correctly to *people* (Service Profiles) and *places* (Studios). Prevent abuse (self-reviews, review rings), handle disputes and takedowns, and surface aggregate reputation into search, booking, messaging, and promotions eligibility—without leaking ratings across scopes.

We will not advance to §1.9 until §1.8 satisfies your 99.9% bar.
