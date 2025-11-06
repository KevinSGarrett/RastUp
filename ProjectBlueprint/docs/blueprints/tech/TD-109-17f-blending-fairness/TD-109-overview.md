---
id: TD-109
title: "**1.7.F Blending & fairness**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-109-17f-blending-fairness\TD-109-overview.md"
parent_id: 
anchor: "TD-109"
checksum: "sha256:26f5c6b86e3fa7b2c59b36ade74fe3bf61a1ee8751ac1b7a228c7dd67e8f4be9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-109"></a>
## **1.7.F Blending & fairness**

**Density rules (configurable via** ***promo_policy*****):**

- At most *max_density_top20* promoted results in top‑20.
- At most *max_above_fold* promoted slots within the first screen.
- Never two promoted results back‑to‑back unless inventory is extremely low (flag‑gated).

**Featured slots**: reserve fixed positions (e.g., \#2, \#8). If fewer eligible than slots, leave slot organic.

**Boosted slots**: insert after every *N* organic results starting after position *P* (e.g., start at \#6, then every 5 cards). Skip if no eligible candidates.

**Diversity & rotation:**

- Per owner: at most one promoted result **from the same owner** in the top‑N to avoid crowd‑out.
- Rotation window ensures that if a campaign lost a slot in this query earlier, it gets priority next time (pacing).
- City‑wide fairness health metric monitors share of voice (% impressions) by owner.
