---
id: TD-4
title: "**1.2.D Analyzers & normalization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-04-12d-analyzers-normalization\TD-4-overview.md"
parent_id: 
anchor: "TD-4"
checksum: "sha256:1991c5c75fa32251897c3aec57d173e9e94bde35ef6a786d4c502c06980f826c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-4"></a>
## **1.2.D Analyzers & normalization**

**Text fields**

- Lowercase, ASCII‑fold; stopwords minimal; synonyms (see Admin §1.2.N) for common fashion/creator terms: *"glamour" ~ "glam"*, *"bnw" ~ "black and white"*, *"H‑Town" ~ "Houston"*.

**Numeric**

- Height, price, rating stored as numerics for range queries.

**Geo**

- Store *geo* as lat/lon. We support **radius** queries at MVP (polygon later).

**Availability**

- Bucket by ISO calendar days; daily job populates buckets for the next N days (N configurable; default 30).

**NSFW/Safe‑Mode**

- For **public search**, apply a query‐time filter:

  - Safe‑Mode ON → *safeModeBandMax \<= 1* (block band 2 entirely).
  - Safe‑Mode OFF for verified adults → *safeModeBandMax \<= 2* (still no explicit thumbnails if the product policy forbids explicit public imagery).
