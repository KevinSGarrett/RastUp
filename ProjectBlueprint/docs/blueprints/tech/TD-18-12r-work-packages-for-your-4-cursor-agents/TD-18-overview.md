---
id: TD-18
title: "**1.2.R Work packages (for your 4 Cursor agents)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-18-12r-work-packages-for-your-4-cursor-agents\TD-18-overview.md"
parent_id: 
anchor: "TD-18"
checksum: "sha256:c7fa3da262be26ea39384afba136e7a1458ccc760a0c4f5940b2ea8517ab4361"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-18"></a>
## **1.2.R Work packages (for your 4 Cursor agents)**

**Agent C — Search/Index**

- WP‑SRCH‑01: Define Typesense collections; create indexer Lambda; implement upsert paths from outbox.
- WP‑SRCH‑02: Build query layer with normalization (city, radius) and safe‑mode enforcement; cursor pagination.
- WP‑SRCH‑03: Implement ranking features and fairness constraints; write unit tests.

**Agent A — API/BFF**

- WP‑API‑SRCH‑01: Implement GraphQL *search*, *searchSuggest*, *saveSearch* with auth & rate limits; error model and correlation ids.
- WP‑API‑SRCH‑02: Result caching (SWR) + per‑user cursor cache.

**Agent B — Web**

- WP‑WEB‑SRCH‑01: Search UI (role tabs, chips, facets, sort); result cards; disclosure for paid slots.
- WP‑WEB‑SRCH‑02: Saved searches & alerts (optional flag).

**Agent D — Admin & QA**

- WP‑ADM‑SRCH‑01: Console pages (reindex, synonyms, density caps, invalid‑clicks).
- WP‑QA‑SRCH‑01: E2E tests for correctness, fairness, promotions, and SLOs; synthetic dataset & golden files.
