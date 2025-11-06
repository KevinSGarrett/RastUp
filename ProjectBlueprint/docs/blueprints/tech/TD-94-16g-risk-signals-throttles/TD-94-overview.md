---
id: TD-94
title: "**1.6.G Risk signals & throttles**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-94-16g-risk-signals-throttles\TD-94-overview.md"
parent_id: 
anchor: "TD-94"
checksum: "sha256:8615e8778d7db976ffc799c3363d0bd6f4192cfc8ce051304d3e1cb81ffb62ed"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-94"></a>
## **1.6.G Risk signals & throttles**

**Signals (rolled up daily/weekly):**

- Disputes opened, refunds requested, cancellations late, late delivery ratio, payment failures, invalid-click attributions (as buyer/seller), moderation flags.

**Score (0–100):**  
Weighted sum with decay—recent events weigh more. Thresholds:

- **Watch (≤60)** → warnings; **limit** high-risk features (promotions, instant payouts).
- **Action (≤40)** → suspend **Instant Book** and **Promotions**; manual review.
- **Critical (≤25)** → pause payouts pending review; city-gated exposure reduced.

**Throttles:**

- Limit number of open proposals, outgoing messages per minute, or daily instant payout requests when below thresholds.
