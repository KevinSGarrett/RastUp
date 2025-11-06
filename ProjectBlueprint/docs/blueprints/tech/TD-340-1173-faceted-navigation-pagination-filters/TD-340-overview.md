---
id: TD-340
title: "**1.17.3 Faceted Navigation, Pagination & Filters**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-340-1173-faceted-navigation-pagination-filters\TD-340-overview.md"
parent_id: 
anchor: "TD-340"
checksum: "sha256:64ed6b1c3d191b721b83ce842622882948b498b05812e22ddf1ac33d19443fca"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-340"></a>
## **1.17.3 Faceted Navigation, Pagination & Filters**

**Objective:** Let users filter richly **without** creating an indexation explosion.

**Approach**

- **Indexable landing** per role/city **without filters** (e.g., */models?city=houston*).
- **Non‑indexable** filter combinations (e.g., price/amenities) → keep crawlable links but serve *noindex, follow* and **self‑canonical** to the landing variant.
- Pagination: *?page=2* allowed but **noindex**; canonical to page 1 landing. Avoid *rel=prev/next* (deprecated); use strong internal links instead.

**Artifact — filter allowlist**  
*Recommended path:* *search/spec/filter-allowlist.md*

*Indexable: (role + city) only*  
*Non-indexable: any additional filters (price, amenity, availability, verification, rating, etc.) =\> meta robots noindex, self-canonical to landing*  
*Pagination: ?page=N =\> meta robots noindex, canonical to page=1*
