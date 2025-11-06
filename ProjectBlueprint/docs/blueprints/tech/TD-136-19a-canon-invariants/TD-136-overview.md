---
id: TD-136
title: "**1.9.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-136-19a-canon-invariants\TD-136-overview.md"
parent_id: 
anchor: "TD-136"
checksum: "sha256:5464a2dc2bf59bf8a4149d30d6f619146ef937fcccb4b74e4eb6c7ff6cf13e03"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-136"></a>
## **1.9.A Canon & invariants**

801. Money in integer cents (UTC timestamps).

802. **One buyer charge per LBG** (already in §1.3), with **per‑leg allocations** and **escrow‑like holds** (payouts only on completion/acceptance window).

803. **Platform fee ≠ GMV.** Fees are **not** the seller’s price; fees are separate lines and recognized as **revenue** for the platform only when *earned*.

804. **Taxes split correctly**: (a) **service taxes** on the seller’s service (pass‑through liability to seller or to tax authority depending on “merchant‑of‑record” (MoR) configuration), and (b) **platform fee taxes** (platform’s own tax obligation) — never recognized as revenue.

805. **Two distinct credits**:

     92. **Ads credits**: for §1.7 promotions (advertiser side).
     93. **Buyer wallet**: marketplace credits for buyers (refund residuals, goodwill, referrals). **These must not mingle.**

806. **Accounting gates**: daily close/reconciliation must be green to release payouts (ties to §1.3.V).

807. **Idempotency & lineage everywhere** (PI ids, transfer ids, refund ids, ledger ids; stable joins for recon).
