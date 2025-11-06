---
id: TD-104
title: "**1.7.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-104-17a-canon-invariants\TD-104-overview.md"
parent_id: 
anchor: "TD-104"
checksum: "sha256:bb7f86477a25fa8b3f337e133e1e0f844e6fd95f4820f4d4f997cfe64a64f07c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-104"></a>
## **1.7.A Canon & invariants**

640. **No filter bypass.** Promoted results must **match the user’s filters** (role, city, price bands, availability, Safe‑Mode) and respect city gates.
641. **Transparency by design.** Promoted units are marked (“Promoted”/“Featured”) and visually distinct.
642. **Density caps.** Fixed, configurable caps (e.g., ≤2 promoted in top‑20; ≤1 above the fold).
643. **Eligibility gates.** Sellers must be **ID Verified**, have minimum **completeness score**, and be policy‑clean. Studios must be verified to advertise.
644. **Pay only for valid clicks.** Deduplicate & filter suspicious clicks; issue automatic make‑good credits.
645. **Budget safety.** Daily & total budgets; pacing to avoid early day burn; automatic pause when funds low or policy violated.
646. **Auditable.** Every impression/click/charge/credit is traceable, immutable, and reconcilable to Stripe.
