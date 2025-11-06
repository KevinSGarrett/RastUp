---
id: TD-5
title: "**1.2.E Filters & UI chips**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-05-12e-filters-ui-chips\TD-5-overview.md"
parent_id: 
anchor: "TD-5"
checksum: "sha256:d45fe6e5009044ba4866a9763f16b8afa8ce86338e1ab0fc33ef64afbf1e601c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-5"></a>
## **1.2.E Filters & UI chips**

**Global filters (people)**

- Role (tab), Location (city/radius), Date (single or range), Budget (min/max), Verification (ID Verified badge), Instant Book toggle, Rating (≥ threshold), Safe‑Mode on/off (if signed‑in and age‑verified), Availability (specific day), Sort (Default, Top Rated, Price Low→High, New).

**Role‑specific filters**

- **Models**: Height (cm/in ranges), Genres (allowlist), Experience (years), Travel ready (bool).
- **Photographers**: Specialties, Studio Access (has studio link), Turnaround (days), Insurance (bool).
- **Videographers**: Specialties, Audio capability (bool), Deliverable format (enum).
- **Creators**: Platforms (IG/TT/YT/X), Category, Verified social (bool), Min followers (range).
- **Studios**: Amenities (multi‑select), Deposit required (bool), Size/Capacity buckets, Natural light (bool), Parking (bool).

**Promotion chips (when feature flag on)**

- “Featured” label (above the fold) or “Boosted” (below); both must be visually distinct and disclose paid placement.
