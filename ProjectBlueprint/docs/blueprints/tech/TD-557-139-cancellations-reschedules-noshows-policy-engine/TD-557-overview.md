---
id: TD-557
title: "**1.3.9 Cancellations, reschedules & no‑shows (policy engine)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-557-139-cancellations-reschedules-noshows-policy-engine\TD-557-overview.md"
parent_id: 
anchor: "TD-557"
checksum: "sha256:75dcc3186a8a3211a28068e170039ba55943b120a1e9685e5a2f93f1723e4a59"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-557"></a>
## **1.3.9 Cancellations, reschedules & no‑shows (policy engine)**

**Policy matrix (configurable in Admin; defaults below):**

- **Flexible**:

  - Buyer cancels ≥72h: full refund minus platform fee.
  - 72–24h: 50% of subtotal (provider) + platform fee not refunded.
  - \<24h: no refund (provider keeps subtotal) unless provider rebooks slot.

- **Standard**: 7d/48h/24h thresholds with 100%/50%/0% similar to above.

- **Strict**: 14d/7d/48h thresholds with 75%/50%/0%.

**Reschedule**: buyer can request reschedule ≥48h without fees; provider must accept; otherwise treat as cancellation.  
**Provider cancel**: automatic buyer refund; provider reputation hit; optional monetary penalty after repeated cancels (Admin configurable).  
**No‑show**: treat per policy; talent no‑show → refund; buyer no‑show → no refund.

Studio‑specific overtime/cleaning/deposit rules live in §1.24.
