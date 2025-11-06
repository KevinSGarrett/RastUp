---
id: TD-75
title: "**1.5.F Variable binding (examples)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-75-15f-variable-binding-examples\TD-75-overview.md"
parent_id: 
anchor: "TD-75"
checksum: "sha256:d25b3943485fe63fcced90f8f2a274636fdf1d50100a7372d977b1c8bd716b2c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-75"></a>
## **1.5.F Variable binding (examples)**

|  |  |
|----|----|
| **Variable** | **Source** |
| *service_date*, *start_time*, *end_time* | *booking_leg.start_at/end_at* (UTC → local tz of city gate) |
| *location_address* | *studio.address_json* if studio leg, else buyer‑provided shoot location |
| *buyer_legal_name*, *buyer_email* | Account profile / checkout identity |
| *seller_legal_name* | Talent SP owner legal name |
| *deliverables_summary* | From Brief/Shot list (if provided) + chosen packages |
| *total_price*, *taxes* | From leg price snapshot (*total_cents*, *tax_cents*) |
| *cancellation_policy_summary* | Derived from *policy_json* bands |
| *deposit_amount* | *deposit_policy.auth_cents* (studio leg) |
| *usage_scope*, *territory*, *duration* | Defaults from template, can be narrowed by seller; never wider than template allows |
| *model_dob* | From IDV provider (age 18+ required for Model Release at MVP) |

Validation runs both in the **API** and during **render**. Any failure returns explicit error codes.
