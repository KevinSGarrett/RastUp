---
id: TD-361
title: "**1.18.G Data classification & handling**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-361-118g-data-classification-handling\TD-361-overview.md"
parent_id: 
anchor: "TD-361"
checksum: "sha256:3ae68a6af1cb5d2a591c2dec5c35c184de563db4d2f0f26ed478d827f6d8bac3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-361"></a>
## **1.18.G Data classification & handling**

**Recommended path:** *security/policies/data-classification.md*

- **Public**: marketing copy, SFW previews.
- **Internal**: ops dashboards, aggregate metrics.
- **Confidential PII**: names, emails, phone (minimize; never in logs).
- **Highly Sensitive**: government IDs, IDV artifacts, payment tokens (never store raw PAN).  
  **Rules**
- PII only in **Aurora/Dynamo “private”** schemas; analytics **events are PII‑free** (link via surrogate keys).
- **DSAR** tombstone events (see §1.13) applied to Silver/Gold; Bronze excluded on read.
- **Retention**: per §1.13 — Bronze 18 mo, Silver 24–36 mo, Gold 24 mo; finance facts 7 years.
