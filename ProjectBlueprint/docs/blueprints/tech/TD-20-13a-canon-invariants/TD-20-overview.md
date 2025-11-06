---
id: TD-20
title: "**1.3.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-20-13a-canon-invariants\TD-20-overview.md"
parent_id: 
anchor: "TD-20"
checksum: "sha256:5b21e328958803d78d1f2055da76307d61cb6d31a3f04422cd58c2d875ade566"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-20"></a>
## **1.3.A Canon & invariants**

- **Two distinct ledgers:** Talent leg and Studio leg are independent commercial contracts (prices, taxes, refunds, payouts, disputes). **LBG** is a *container* that synchronizes timing and UX but **never** merges their policies or reviews.
- **Docs‑before‑pay:** Required packs (SOW, Model Releases, Studio House Rules) must be assembled and signed **before** any charge is authorized or captured.
- **Escrow‑like handling:** Buyer is charged at confirmation; payouts are **withheld** until completion or acceptance window close (escrow mimic), with deposits handled separately for Studios.
- **Atomicity:** LBG confirmation succeeds **only if both legs validate and fund**; otherwise nothing commits.
- **Money correctness:** Sum of lines = totals; taxes computed per leg; cents (integer); idempotency on all external I/O.
- **Attach‑in‑flow Studio:** During Talent checkout, the buyer can add a Studio leg that matches time/location rules; both legs confirm together if valid.
