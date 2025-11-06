---
id: TD-217
title: "**1.13.H Privacy, governance & retention**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-217-113h-privacy-governance-retention\TD-217-overview.md"
parent_id: 
anchor: "TD-217"
checksum: "sha256:35171a61cf0d95bdcc19d9ef4c70148d475192ee646f832126214452e027e753"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-217"></a>
## **1.13.H Privacy, governance & retention**

- **Lake Formation** for table/column permissions; analysts get **row‑level filtering** by environment and city if required.

- **Hashing**: *email_sha256*, *phone_sha256* kept only in **Silver private** area (not in Gold); never in events.

- **DSAR/Deletion**: user deletion writes a **tombstone event**; nightly job purges Silver/Gold joins that carry the user’s PII hash; Bronze (raw, immutable) is handled by maintaining a mapping table of redactions and excluding on read.

- **Retention**:

  - Bronze events: 18 months (partition delete after).
  - Silver facts: 24–36 months depending on table.
  - Gold marts: rolling 24 months.

- **Legal holds**: tag partitions; purge blocked until hold cleared.
