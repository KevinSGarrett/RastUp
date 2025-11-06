---
id: TD-196
title: "**1.12.F Data stores & retention**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-196-112f-data-stores-retention\TD-196-overview.md"
parent_id: 
anchor: "TD-196"
checksum: "sha256:2345179d702ec20b5248cf5eb5878f3e16de90f01622280f71924ea9a4a9d4af"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-196"></a>
## **1.12.F Data stores & retention**

**Aurora (PostgreSQL Serverless v2)**

- **Schemas:** *core* (users, profiles, bookings), *finance*, *docs*, *promo*, *trust*, *studios*, *comms*.
- **Backups:** PITR enabled; snapshots retained 7–30 days in dev/stage, 35–90 days in prod.
- **Migrations:** Sqitch/Prisma/Migrate (choose one; locked in CI).

**DynamoDB**

- Tables: *threads*, *presence*, *comms_tokens*, *comms_dedupe*, *promo_active_by_city*, *trust_cache*.
- **TTL**: presence/typing; dedupe caches; in‑app archivals after 90 days.

**S3**

- Buckets: *public-assets*, *user-previews*, *docs-rendered*, *logs-raw*.
- **Lifecycle:** move to Intelligent‑Tiering after 30 days; cold/archive after 90/180 days where safe.
- **Block public access** by default; use CF OAI/ORI for public access.

**Search**

- **Typesense** single small node (or managed) at launch; replica optional.
- Adapter layer ready to switch to **OpenSearch Serverless** if scale demands; **OCU** cap alarms.
