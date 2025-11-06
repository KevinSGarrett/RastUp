---
id: TD-10
title: "**1.2.J Ingestion & update pipeline**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-10-12j-ingestion-update-pipeline\TD-10-overview.md"
parent_id: 
anchor: "TD-10"
checksum: "sha256:7782be0f1ed3136c05bd01baaea726684f876af4a8b32cc4a9b3efac16d13e57"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-10"></a>
## **1.2.J Ingestion & update pipeline**

**Write sources**

- SP publish/update, rating updates, verification/badge changes, availability updates, policy signals, studio verification toggles.

**Mechanics**

- **Outbox** on mutations → SQS → Indexer Lambda → engine upsert.
- **Nightly backfill** per city to guarantee convergence.
- **On booking accept**: emit event to add date to *availabilityBuckets* for the participant SP and studio (if applicable).
- **On cancellation**: remove bucket(s) if time still in future.
- **On policy change** (Safe‑Mode, city gate, eligibility): bulk partial update.

**Consistency**

- If index write fails, retry with exponential backoff; stale card renders are guarded by server query filters.
