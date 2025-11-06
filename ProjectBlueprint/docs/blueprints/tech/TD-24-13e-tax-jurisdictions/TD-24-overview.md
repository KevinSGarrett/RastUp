---
id: TD-24
title: "**1.3.E Tax & jurisdictions**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-24-13e-tax-jurisdictions\TD-24-overview.md"
parent_id: 
anchor: "TD-24"
checksum: "sha256:01305748a79a10406d67f5a19071c7bb5852207ea021d45b466641749ea3f0db"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-24"></a>
## **1.3.E Tax & jurisdictions**

- Use **TaxJar/Avalara** (adapter) or **Stripe Tax** if we decide to keep vendors lean for MVP; either way, **quote is per leg** and stored in *tax_txn* with jurisdiction granularity.
- **Commit** tax on confirmation; **amend** on change orders; **refund** tax appropriately on cancellations/refunds per provider rules.

**Edge cases**

- Cross‑city bookings: compute tax based on **service location** (studio’s city or talent’s service location if no studio).
- Tax‑exempt flags (rare) require admin approval and audit.
