---
id: TD-253
title: "**1.14.Q Acceptance criteria (mark §1.14 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-253-114q-acceptance-criteria-mark-114-final-only-when-all-true\TD-253-overview.md"
parent_id: 
anchor: "TD-253"
checksum: "sha256:d31a2c70c4bf5c786376f532e612a47bcc64058a1cca2754752ea626caeaa82a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-253"></a>
## **1.14.Q Acceptance criteria (mark §1.14 FINAL only when ALL true)**

1508. Age‑gated eligibility enforced; creators with IDV can publish; fans 18+ can pay.
1509. Subscriptions, tips, PPV, and requests work end‑to‑end with receipts, taxes, and payouts.
1510. Media pipeline (previews vs finals) functions with watermarking, safety scans, and access tokens; no finals stored internally.
1511. Messaging action cards cover the entire request lifecycle; approvals & revisions audited.
1512. Moderation & DMCA tooling live; anticircumvention active; violations audited.
1513. Dashboards & NRT views show earnings/churn/backlog; experiments and guardrails instrumented.
1514. Cost posture holds (previews only, limited HLS, caching); p95 performance targets met.

# **§1.14 — Fan‑Sub (Paid Content, Requests, Tips & PPV) — Expanded Spec**

This augments the earlier §1.14 with **implementation‑grade detail**: exact Stripe object mappings, state machines, watermarking/preview specs, entitlement tokens, manifest contracts, moderation & DMCA flows, tax/fee math, GL entries, comms templates, errors, and runbooks.
