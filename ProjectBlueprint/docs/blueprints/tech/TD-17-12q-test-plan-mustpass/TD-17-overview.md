---
id: TD-17
title: "**1.2.Q Test plan (must‑pass)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-17-12q-test-plan-mustpass\TD-17-overview.md"
parent_id: 
anchor: "TD-17"
checksum: "sha256:0123ccc0cb80a09b764abc4b2ff87548576db17782de05c6b29a3f037f5b57e8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-17"></a>
## **1.2.Q Test plan (must‑pass)**

**Unit & contract**

- Filter parsing/normalization; role‑filter gating; city & safe‑mode checks; error codes.

**Search correctness**

- Role true: a multi‑role user queried in “Model” must link to */u/{handle}/model*; ratings don’t leak across roles.
- Studios separated: amenities filters never affect people surface.

**Ranking & fairness**

- Diversity: same owner appears ≤K times in top N.
- New‑seller floor: at least M cold‑start profiles surface in top N given enough eligible docs.
- Verify boosts: ID Verified outranks equal unverified, all else equal.

**Promotions**

- Density caps obeyed; placements never bypass filters; invalid clicks removed from billable stream.

**Performance**

- p95 latency within SLO for cached and uncached queries under synthetic city load.

**Resilience**

- Indexer retry & DLQ; search fallback message (non‑blocking) if engine unreachable.
