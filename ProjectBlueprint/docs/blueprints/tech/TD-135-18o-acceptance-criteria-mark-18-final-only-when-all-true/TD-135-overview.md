---
id: TD-135
title: "**1.8.O Acceptance criteria (mark §1.8 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-135-18o-acceptance-criteria-mark-18-final-only-when-all-true\TD-135-overview.md"
parent_id: 
anchor: "TD-135"
checksum: "sha256:ce061333be1fa104b76c4c7b33ded1faa6fa8a30cebebb752ddbcab6f7407f1e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-135"></a>
## **1.8.O Acceptance criteria (mark §1.8 FINAL only when ALL true)**

794. Only eligible buyers can review; one per leg; edit window enforced; content scanned.
795. Aggregates computed with decay and sample guards; fraud-flagged reviews excluded pending review.
796. Surfacing correct on SP/Studio pages, search cards, booking/thread headers; “New” chip behavior correct.
797. Moderation & appeals operate with immutable audits; bulk actions for rings.
798. Notifications for reminders/public replies sent; rate limits enforced; policy respected.
799. Telemetry complete; dashboards reflect health and abuse trends.
800. Performance & cost within targets; caches invalidate correctly on updates.

# **§1.9 — Payments & Wallet**

*(Platform fees · Taxes on fees · Separate “ads” credits vs. buyer wallet · Statements · Accounting & revenue recognition · GL & recon · APIs · Admin · Telemetry · Tests · Cost)*

**Purpose.** Define the *financial core* that separates marketplace **GMV** from **platform fee revenue**, treats **taxes correctly**, keeps “ads credits” separate from “buyer wallet,” and drives statements, accounting, and reconciliation. This section makes our booking money flows audit‑grade and implementation‑ready across **data model, fee math, GL entries, APIs, admin tools, telemetry, SLOs, and tests**. It aligns with §§1.3 (Checkout), 1.4 (Messaging/Project Panel), and 1.7 (Promotions).

We will not advance to §1.10 until §1.9 satisfies your 99.9% bar.
