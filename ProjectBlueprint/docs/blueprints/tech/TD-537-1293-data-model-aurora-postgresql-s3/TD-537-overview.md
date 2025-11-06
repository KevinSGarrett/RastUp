---
id: TD-537
title: "**1.29.3 Data model (Aurora PostgreSQL + S3)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-537-1293-data-model-aurora-postgresql-s3\TD-537-overview.md"
parent_id: 
anchor: "TD-537"
checksum: "sha256:6b512e0f559bdbb8598d61cd70b8c38e3fd5e5295068fae2d1342353e104a7d6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-537"></a>
## **1.29.3 Data model (Aurora PostgreSQL + S3)**

**Tables (schema** ***portfolio*****)**

- portfolio_item

  - *item_id pk*, *owner_user_id*, *role_profile_id*, *title*, *slug*, *city*, *shoot_date*, *genres text\[\]*,  
    *cover_media_id*, *sfw_band smallint*, *status enum('draft','pending','published','archived','blocked')*,  
    *verified_booking_order_id nullable*, *studio_id nullable*, *created_at*, *updated_at*.
  - Notes: *sfw_band* drives Safe‑Mode visibility; *verified_booking_order_id* shows a “Verified booking” badge when present. **All public media must be SFW.**

NonTechBlueprint

- portfolio_media

  - *media_id pk*, *item_id fk*, *kind enum('image','video')*, *s3_key_original*, *s3_key_web*, *width*, *height*, *duration_sec nullable*, *ordinal*, *alt_text*.

- *portfolio_case_study* (optional, attached to *item_id*)

  - *client_type*, *summary*, *deliverables text\[\]*, *results text*, *budget_range_low_cents*, *budget_range_high_cents*.

- portfolio_collab_tag

  - *item_id fk*, *collaborator_user_id*, *role_code*, *status enum('pending','approved','declined')*, *note*, *evidence_order_id nullable*, *created_at*.
  - Drives **tagging & approvals**; only **approved** collaborators render as chips that **open profiles**.

NonTechBlueprint

- board

  - *board_id pk*, *owner_user_id*, *title*, *visibility enum('private','unlisted','public')*, *city nullable*, *created_at*.

- board_item

  - *board_id fk*, *entity_type enum('person','studio','portfolio_item')*, *entity_id*, *note nullable*, *ordinal*.

**S3 prefixes**

- *portfolio/{ownerUserId}/{itemId}/media/\** (original & web)
- *boards/{ownerUserId}/{boardId}/share/\** (share images, optional)
