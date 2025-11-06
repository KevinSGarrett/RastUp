---
id: TD-173
title: "**1.11.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-173-111a-canon-invariants\TD-173-overview.md"
parent_id: 
anchor: "TD-173"
checksum: "sha256:571710b4c708a64da2bcbf1e1c42f9aa8d8d04d47c53969bb0aca0f2098ee246"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-173"></a>
## **1.11.A Canon & invariants**

1050. **Studios are places**, not people. Ratings, verification, search facets, and policies are **separate** from Service Profiles (SPs).
1051. **Independent leg math**: a Studio leg has its own price, taxes, deposit policy, refunds, receipts, payout, and dispute/deposit-claim flows (see §1.3).
1052. **Attach‑in‑flow**: a Studio can be added during Talent checkout. Confirmation is **atomic** across legs (all‑or‑nothing).
1053. **Verification before boost**: only **verified studios** are eligible for “Verified Studio” badge and advertising (see §1.7).
1054. **Safe content**: public thumbnails are SFW; NSFW scanning rules apply to any images.
1055. **Cost‑conscious**: asset storage minimal (previews only), intelligent S3 tiering, lean search indices, and throttled scans.
