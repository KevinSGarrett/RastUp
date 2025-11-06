---
id: TD-108
title: "**1.7.E Targeting & matching**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-108-17e-targeting-matching\TD-108-overview.md"
parent_id: 
anchor: "TD-108"
checksum: "sha256:7d499f264e8c2d19e5f653ab3b23e9792a3513f590eeee1e666e9a64a1edecbb"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-108"></a>
## **1.7.E Targeting & matching**

**Mandatory:** *surface*, *city*, and (for people) *role*.  
**Optional:** keywords (prefix/synonyms), price bands, availability day hints.

**Matching algorithm (MVP):**

658. Start with campaigns active in *surface* + *city* (+ *role* if people).
659. Filter out those failing **eligibility** (trust, policy, completeness, Safe‑Mode).
660. Filter by **query filters** (price range, availability day if required, etc.).
661. Apply **budget availability** (daily balance left) & **pacing** (even distribution: remaining_budget / remaining_slots).
662. Produce a ranked **candidate set** ordered by: compliance → campaign freshness → spend vs target pacing (under‑pacing gets slight priority) → random tiebreaker for fairness.
663. Blend into organic results per §1.7.F.
