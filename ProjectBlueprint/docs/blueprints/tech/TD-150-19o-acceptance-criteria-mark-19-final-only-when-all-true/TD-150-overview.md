---
id: TD-150
title: "**1.9.O Acceptance criteria (mark §1.9 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-150-19o-acceptance-criteria-mark-19-final-only-when-all-true\TD-150-overview.md"
parent_id: 
anchor: "TD-150"
checksum: "sha256:01578b0243eb68d4f8402113dc1b0ee63258e2340609ae6f7c0ba2587235f413"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-150"></a>
## **1.9.O Acceptance criteria (mark §1.9 FINAL only when ALL true)**

858. Platform fees computed per leg; fee taxes quoted; shown on receipts; earned on completion.
859. Wallet credits/debits behave atomically; cannot overdraft; idempotent reversals on failure paths.
860. GL entries capture capture/earn/payout/refund/dispute correctly; exports work; daily recon green 5/5 days.
861. MoR toggle correctly routes **service tax** to Seller Payable vs Tax Payable; platform fee tax always stays in Tax Payable.
862. Statements (buyer/seller) accurate and downloadable; platform exports ready for accounting.
863. Telemetry complete; SLOs met; costs within budget alarms.

# **§1.9 — Payments & Wallet**

*(Platform fees · Taxes on fees · Separate “ads” credits vs. buyer wallet · Statements · Accounting & revenue recognition · GL & recon · APIs · Admin · Telemetry · Tests · Cost)*

**Purpose.** Define the *financial core* that separates marketplace **GMV** from **platform fee revenue**, treats **taxes correctly**, keeps “ads credits” separate from “buyer wallet,” and drives statements, accounting, and reconciliation. This section makes our booking money flows audit‑grade and implementation‑ready across **data model, fee math, GL entries, APIs, admin tools, telemetry, SLOs, and tests**. It aligns with §§1.3 (Checkout), 1.4 (Messaging/Project Panel), and 1.7 (Promotions).

We will not advance to §1.10 until §1.9 satisfies your 99.9% bar.
