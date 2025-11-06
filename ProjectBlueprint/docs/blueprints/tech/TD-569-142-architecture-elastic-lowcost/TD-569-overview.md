---
id: TD-569
title: "**1.4.2 Architecture (elastic & low‑cost)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-569-142-architecture-elastic-lowcost\TD-569-overview.md"
parent_id: 
anchor: "TD-569"
checksum: "sha256:9436bc943dfdc27cb9856e93ef98eb82de34234bbd0f9730a19d4c5e2f695127"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-569"></a>
## **1.4.2 Architecture (elastic & low‑cost)**

- **Frontend**: Next.js (web) + React Native (mobile). Inbox = virtualized lists; thread = sticky composer + cards.

- **API**: AppSync GraphQL with Lambda resolvers.

- **Storage**:

  - **Aurora Postgres** for threads, participants, message metadata, cards, and inbox indexes.
  - **S3** for attachments (images, proofs, receipts) with short‑TTL pre‑signed URLs.
  - **DynamoDB** for ephemeral **typing/presence**, **rate limits**, **idempotency**, and **Message Request** pending gates.

- **Events**: Kinesis/SNS bus (*msg.sent*, *card.accepted*, *request.accepted*, etc.) feeds notifications, analytics, and Admin.

- **Search**: Typesense collection *inbox_index* for fast participant/keyword search (sanitized; no sensitive PII).
