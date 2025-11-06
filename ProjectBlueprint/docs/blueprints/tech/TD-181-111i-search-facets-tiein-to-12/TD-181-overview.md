---
id: TD-181
title: "**1.11.I Search facets (tie‑in to §1.2)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-181-111i-search-facets-tiein-to-12\TD-181-overview.md"
parent_id: 
anchor: "TD-181"
checksum: "sha256:9967c4df02c8e671dc383c3c117857feb2e5ffb8f8665199081798b09d55fecf"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-181"></a>
## **1.11.I Search facets (tie‑in to §1.2)**

- **Collection**: *studios_v1* (already defined).
- **Facets**: city, amenities\[\], verifiedStudio (bool), depositRequired (bool), capacity buckets, priceFromCents, ratingAvg, availability day buckets.
- **Sort**: default → text match → verified → rating → price distance from user budget → recency.
- **Safe‑Mode**: block nsfw_band=2 from thumbnails.
