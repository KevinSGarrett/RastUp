---
id: TD-6
title: "**1.2.F Query grammar & API contracts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-06-12f-query-grammar-api-contracts\TD-6-overview.md"
parent_id: 
anchor: "TD-6"
checksum: "sha256:83e3344f250ad4ad514b368ac0e9f25804f770d1c2028f19f0511600d0901bfb"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-6"></a>
## **1.2.F Query grammar & API contracts**

**GraphQL (AppSync)**

*input SearchInput { surface: SearchSurface! \# PEOPLE or STUDIOS role: RoleType \# required when surface=PEOPLE city: String! lat: Float lon: Float radiusKm: Int = 50 date: AWSDate \# single day dateRange: DateRangeInput \# optional alternative budgetMinCents: Int budgetMaxCents: Int ratingMin: Float verifiedOnly: Boolean instantBookOnly: Boolean safeMode: Boolean = true \# Role-specific filters: model: ModelFiltersInput photographer: PhotographerFiltersInput videographer: VideographerFiltersInput creator: CreatorFiltersInput studios: StudiosFiltersInput sort: SearchSort = DEFAULT page: String \# opaque cursor pageSize: Int = 20} type SearchResult { items: \[SearchCard!\]! facets: \[Facet!\]! page: String \# next cursor} type Query { search(input: SearchInput!): SearchResult! searchSuggest(query: String!, surface: SearchSurface!, role: RoleType, city: String!): \[SuggestItem!\]! savedSearches: \[SavedSearch!\]!} type Mutation { saveSearch(name: String!, input: SearchInput!): SavedSearch! deleteSavedSearch(id: ID!): Boolean!}*

**Cursor‑based pagination**

- Results return opaque *page* tokens (do not leak engine details).
- We cache the last N cursors per user/session (server‑side) to enable back/forward replay.

**Query normalization**

- City is canonicalized to a region/city id; if *lat/lon* present, we compute city from reverse geocoding and warn on mismatches.
- Role‑specific filters are ignored unless *role* matches the relevant type.
