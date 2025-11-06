---
id: TD-182
title: "**1.11.J Checkout & deposits (tie‑in to §1.3)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-182-111j-checkout-deposits-tiein-to-13\TD-182-overview.md"
parent_id: 
anchor: "TD-182"
checksum: "sha256:c98a706fec63f5045e13edb8bc9372ca71e1f049bff481b66e05d2c1d9472336"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-182"></a>
## **1.11.J Checkout & deposits (tie‑in to §1.3)**

- Studio leg participates in **atomic LBG confirm**.
- **Deposit auth** handled via **SetupIntent** (separate from GMV).
- **Overtime** & **extras** use the amendment flow (§1.3.K).
- **Deposit claims** handled post‑session with evidence (§1.3.N).
- Cancellation policy bands live in *studio_policy.cancellation_policy*.
