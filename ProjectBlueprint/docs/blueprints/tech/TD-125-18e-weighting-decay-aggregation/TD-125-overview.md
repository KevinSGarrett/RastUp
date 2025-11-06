---
id: TD-125
title: "**1.8.E Weighting, decay & aggregation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-125-18e-weighting-decay-aggregation\TD-125-overview.md"
parent_id: 
anchor: "TD-125"
checksum: "sha256:09f85f9f3daf6195a45ad112d2f3a20ee0a9e209a5e99247d005c7339c611b74"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-125"></a>
## **1.8.E Weighting, decay & aggregation**

**Base average:** simple mean over *published* reviews only.  
**Recent-weighted average:** apply exponential decay with half-life *H* (e.g., 180 days) to emphasize recent performance:  
*weighted_score = Σ (rating \* e^{-Δt/H}) / Σ e^{-Δt/H}*.

**Minimum sample guard:**

- If *rating_count \< K* (e.g., 5), show **“New — limited reviews”**; still display stars but deemphasize in ranking.
- For search ranking, combine *rating_recent_avg* with count via a Wilson interval or Laplace smoothing.

**Facet aggregation:**

- Per facet mean and count; show as radar or bar chips; used in filters later.

**Fraud signal:**

- Score 0–1 from heuristics (see 1.8.F). If \> threshold, suppress the review from aggregates pending T&S review.

**Update cadence:**

- On every write/mod decision, recompute aggregates; also nightly full recompute for consistency.
