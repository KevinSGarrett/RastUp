---
id: TD-133
title: "**1.8.M Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-133-18m-test-plan-ci-sandbox\TD-133-overview.md"
parent_id: 
anchor: "TD-133"
checksum: "sha256:3e87f282d28685a195e595f80349ae262550c3fe4bc2ec349e1a65a0d20477ee"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-133"></a>
## **1.8.M Test plan (CI + sandbox)**

**Eligibility & write path**

788. Completed leg → buyer can post one review; seller cannot; duplicate blocked.
789. Edit within 24 h succeeds; rating edit blocked; after window, edit blocked.

**Fraud controls**  
3) Self-review attempt blocked.  
4) Ring/burst simulated → auto-hide & queue for T&S; restoration path verified.  
5) Toxic content flagged → hidden; appeal → restore.

**Aggregation**  
6) Weighted average & decay verified vs golden file; low-sample indicator shown correctly.  
7) Facet averages computed; distribution histograms accurate.

**Surfacing**  
8) Search cards show correct stars/counts; “New” chip for low sample.  
9) Profile page shows highlights and facet bars; recent window updates.

**Admin**  
10) Hide/remove/restore writes audits; bulk ring takedown works; reply moderation enforced.

**Performance**  
11) p95 entity reputation fetch ≤ 120 ms (cached); recompute job under 1 min per 10k entities.
