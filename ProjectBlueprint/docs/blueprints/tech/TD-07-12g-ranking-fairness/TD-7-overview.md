---
id: TD-7
title: "**1.2.G Ranking & fairness**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-07-12g-ranking-fairness\TD-7-overview.md"
parent_id: 
anchor: "TD-7"
checksum: "sha256:76eddeb6e94175626e02450637603b563907c2e77e98e9a0bad49a97ae3d373a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-7"></a>
## **1.2.G Ranking & fairness**

**Base score**  
*score = w_text\*textMatch + w_geo\*geoScore + w_rep\*repScore + w_verify\*verifyBoost + w_price\*priceFit + w_avail\*availBoost + w_recency\*recency*

- *textMatch*: keyword/synonym features (if query text present).
- *geoScore*: distance‑decay (radius Gaussian; 0 beyond radius).
- *repScore*: f(ratingAvg, ratingCount) with Laplace smoothing to avoid low‑sample overweighting.
- *verifyBoost*: +X if ID Verified, +Y if Trusted Pro (BG passed).
- *priceFit*: penalty for large deviation from user budget (if set).
- *availBoost*: +Z if the requested date is in *availabilityBuckets*.
- *recency*: mild boost for recently updated profiles (helps cold start).

**Fairness & diversity constraints**

- **Provider diversity**: impose a max of K results per owner within the top N (avoid multi‑role flooding).
- **New‑seller floor**: ensure a minimum presence (M slots in top N reserved for low‑history but complete/verified profiles).
- **Studio diversity**: different studio owners in top M.
- **Policy penalties**: suppress results if *policySignals* exceed thresholds (dispute, late delivery). Thresholds configured via Admin.

**Promotions blending (when enabled)**

- **Featured**: eligible results can occupy fixed slots (e.g., 1–2 positions in top 20) but **never break filters**.
- **Boost**: cost‑per‑click uplift—insert additional slots every X organic results after position P.
- Both obey density caps: e.g., ≤2 Featured in top 20; ≤1 above the fold.
