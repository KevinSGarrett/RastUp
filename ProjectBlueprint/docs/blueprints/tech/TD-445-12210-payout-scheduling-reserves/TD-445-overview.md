---
id: TD-445
title: "**1.22.10 Payout scheduling & reserves**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-445-12210-payout-scheduling-reserves\TD-445-overview.md"
parent_id: 
anchor: "TD-445"
checksum: "sha256:6a8d04c6ae167b098a47eddcbfafd8a1588b198d4bccea3cb5fbad3c9d913916"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-445"></a>
## **1.22.10 Payout scheduling & reserves**

- Default **T+1** transfer after completion; **T+7** for new providers until reaching a reputation threshold.
- **Rolling reserve** (e.g., 10% for 30 days) for high‑risk providers (dispute/cancellation rates).
- Manual **hold/release** flags for risk (see §1.22.12); all changes are audited.

**Artifact — payout policy**  
**Recommended path:** *payments/policy/payout-schedule.md*

*- New providers (\<5 completed bookings): T+7*  
*- Verified/Trusted Pro: T+1*  
*- Reserve triggers: dispute rate \>1%, abnormal cancellations, risk flags*
