---
id: TD-103
title: "**1.6.P Acceptance criteria (mark §1.6 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-103-16p-acceptance-criteria-mark-16-final-only-when-all-true\TD-103-overview.md"
parent_id: 
anchor: "TD-103"
checksum: "sha256:dbb50b2a7f5053d389ebbf6180b339758ee4e7b132f0a27e707923e8f9a9e044"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-103"></a>
## **1.6.P Acceptance criteria (mark §1.6 FINAL only when ALL true)**

632. IDV flow works end-to-end; badge & age gate applied; Instant Book correctly gated.
633. BG flow (optional) works with FCRA consents, statuses, adverse-action templates, and audit trails; Trusted Pro badge granted on **clear**.
634. Social verification connects/revokes; nightly snapshot reflected in search and badges.
635. Risk score updates from domain events and enforces throttles at thresholds; overrides require dual approval.
636. Admin consoles cover review, overrides, exports, and adverse-action steps with immutable audits.
637. Privacy posture holds (no raw PII stored; access logs); retention policies configured.
638. Telemetry/SLO dashboards for funnels and turnaround; all targets met under synthetic load.
639. Costs remain within budget; batch refreshes and cohort recerts smoothed.

# **§1.7 — Promotions & Advertising**

*(eligibility · placements · targeting · blending & fairness · budgets & pacing · click validation · billing & credits · admin tools · telemetry · error taxonomy · tests · cost controls)*

**Purpose.** Provide a complete, auditable ad system that allows eligible sellers to promote their **Service Profiles** (people) and, later, **Studios** (places) within search/browse—**without** breaking filters or user trust. Promotions must be transparent (“Promoted”), capped in density, city‑gated, safe‑mode compliant, verifiable against fraud, and cost‑controlled.

We will not move to §1.8 until §1.7 satisfies your 99.9% bar.
