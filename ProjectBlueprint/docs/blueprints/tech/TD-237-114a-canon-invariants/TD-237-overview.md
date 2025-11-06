---
id: TD-237
title: "**1.14.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-237-114a-canon-invariants\TD-237-overview.md"
parent_id: 
anchor: "TD-237"
checksum: "sha256:20eedc1135fbd38c838bc3beb5bb5a89842e9e59ac17b49f256b095627dca575"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-237"></a>
## **1.14.A Canon & invariants**

1430. **Age gate & IDV required:** Creators **and** paying fans must be 18+ (verified via §1.6). Creators need **ID Verified** to publish Fan‑Sub.
1431. **Safe‑Mode everywhere:** Public thumbnails are SFW; NSFW bands apply to previews and in‑thread uploads.
1432. **Previews vs finals:** Only **previews** (small images/clips) are stored in our S3. **Final media** is external (Drive/Dropbox/S3 owner) and referenced via **immutable manifests** (checksums), like deliverables in §1.4/§1.3.
1433. **No filter bypass:** Fan‑Sub surfaces honor city gates, age gates, Safe‑Mode, and user preferences.
1434. **Money clarity:** Separate **Marketplace GMV** (requests/PPV) and **Subscription revenue** streams; platform fees & **taxes on fees** follow §1.9.
1435. **Privacy:** No PII in media watermarks; no emails/phones exchanged off‑platform (anticircumvention).
1436. **Auditability:** All paid actions produce immutable records (orders, receipts, approvals), with lineage to users and threads.
