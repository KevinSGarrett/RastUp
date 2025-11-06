---
id: TD-9
title: "**1.2.I Caching, rate limits, and SLOs**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-09-12i-caching-rate-limits-and-slos\TD-9-overview.md"
parent_id: 
anchor: "TD-9"
checksum: "sha256:2cfd7e31494bebda45b95171e85d6a610e423e66ba3ce43687c90d8489a8eab4"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-9"></a>
## **1.2.I Caching, rate limits, and SLOs**

**Result caching**

- Key: hash of normalized *SearchInput* (without page) + city + role + safeMode + version.
- TTL 60–120s (config), **stale‑while‑revalidate** to keep p95 low.
- Pagination cursors cached separately for short time (120s).

**Rate limits**

- Per IP and per account; stricter for anonymous traffic; separate limits for suggest vs full search.

**SLOs (MVP)**

- p95 latency: **≤350ms** for cached hits, **≤600ms** for cold queries at launch city scale.
- Error rate (5xx) \< 0.5%; availability ≥99.9% monthly for the API.
