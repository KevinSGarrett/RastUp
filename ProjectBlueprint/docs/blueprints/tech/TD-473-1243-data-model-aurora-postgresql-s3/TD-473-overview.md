---
id: TD-473
title: "**1.24.3 Data Model (Aurora PostgreSQL + S3)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-473-1243-data-model-aurora-postgresql-s3\TD-473-overview.md"
parent_id: 
anchor: "TD-473"
checksum: "sha256:ab8e5c8ad92fe55a605e9cac6c6a4253a47b27f99f65ae421420d9c0955b07dd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-473"></a>
## **1.24.3 Data Model (Aurora PostgreSQL + S3)**

**Tables (schema** ***spaces*****)**

- *space* (pk *space_id*, owned by *host_user_id*): *title*, *neighborhood*, *lat_approx*, *lon_approx*, *capacity*, *size_sqft*, *ceiling_height_ft*, *daylight_orientation*, *power_notes*, *status*, *published_at*. **Quick Facts** fields mirror the non‑tech spec.

NonTechBlueprint

- *space_media* (*space_id*, *media_id*, *type*, *s3_key*, *ordinal*) — **min 6** with recommended shots list (exterior, cyc, makeup/dressing, load‑in path, restrooms).

NonTechBlueprint

- *space_amenity* (*space_id*, *amenity_code*, *detail_json*) — amenity chips + details (e.g., cyc dimensions).

NonTechBlueprint

- *space_rule* (*space_id*, *rule_code*, *value_bool*, *value_text*) — noise, shoes, pets, food, **surveillance disclosure (required)**, crew limits, hazard toggles (strobe/haze/open flame/ladder).

NonTechBlueprint

- *space_pricing* (*space_id*, *currency*, *price_per_hour_cents*, *min_hours*, *cleaning_fee_cents*, *buffer_before_min*, *buffer_after_min*) — widget computes example totals; buffers enforced.

NonTechBlueprint

- *space_availability_slot* (*space_id*, *weekday*, *start_minute*, *end_minute*, *effective_from*, *effective_to*, *is_blocked*) — **hourly slots** with min hours and buffers.

NonTechBlueprint

- *space_deposit_policy* (*space_id*, *hold_cents*, *hold_currency*) — “authorization only” label in widget.

NonTechBlueprint

- *space_verification_lite* (*space_id*, *status*, *evidence_doc_s3*, *ocr_json*, *place_match_score*, *badge_visible*) — **Studio Lite** verification; on pass, badge available and can gate IB if policy requires.

NonTechBlueprint

- *space_review* (*review_id pk*, *space_id*, *author_user_id*, *rating_int*, *body*, *has_photos*, *created_at*, *is_verified_booking*) — verified booking reviews labeled; owner **one reply** allowed.

NonTechBlueprint

- *space_reputation* (*space_id*, *score_float*, *volume*, *reliability*, *responsiveness*, *verification*, *recency*) — breakdown as described.

NonTechBlueprint

- *space_listing_link* (*space_id*, *linked_people_profile_id*) — supports “**Pair with Talent**” deep‑linking.

NonTechBlueprint

- *space_booking_policy* (*space_id*, *instant_book_enabled_bool*, *ib_guardrail_reason*) — IB guardrails per city/feature flags as needed (ties to §3.9 ops).

NonTechBlueprint

**S3 prefixes**

- *spaces/{spaceId}/media/…* (images/video), *spaces/{spaceId}/docs/…* (rules PDF snapshot, verification docs), *spaces/{spaceId}/doorcode.txt* (encrypted at rest, shared only post‑booking).

**Typesense collection** *spaces_public*  
Fields: *title*, *city*, *neighborhood*, amenity facets, price/hour (ranges), rating, **availability summaries** for a look‑ahead window.
