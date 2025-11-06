---
id: TD-151
title: "**1.9.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-151-19a-canon-invariants\TD-151-overview.md"
parent_id: 
anchor: "TD-151"
checksum: "sha256:01ae79bafb0071dad76ecff5079fe6b5a415b8e54ba06acce237e7cd3bd60bc5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-151"></a>
## **1.9.A Canon & invariants**

864. Money in integer cents (UTC timestamps).

865. **One buyer charge per LBG** (already in §1.3), with **per‑leg allocations** and **escrow‑like holds** (payouts only on completion/acceptance window).

866. **Platform fee ≠ GMV.** Fees are **not** the seller’s price; fees are separate lines and recognized as **revenue** for the platform only when *earned*.

867. **Taxes split correctly**: (a) **service taxes** on the seller’s service (pass‑through liability to seller or to tax authority depending on “merchant‑of‑record” (MoR) configuration), and (b) **platform fee taxes** (platform’s own tax obligation) — never recognized as revenue.

868. **Two distinct credits**:

     118. **Ads credits**: for §1.7 promotions (advertiser side).
     119. **Buyer wallet**: marketplace credits for buyers (refund residuals, goodwill, referrals). **These must not mingle.**

869. **Accounting gates**: daily close/reconciliation must be green to release payouts (ties to §1.3.V).

870. **Idempotency & lineage everywhere** (PI ids, transfer ids, refund ids, ledger ids; stable joins for recon).
