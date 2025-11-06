---
id: TD-603
title: "**1.6.7 Ticketing: priorities, routing, SLAs, macros, QA**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-603-167-ticketing-priorities-routing-slas-macros-qa\TD-603-overview.md"
parent_id: 
anchor: "TD-603"
checksum: "sha256:8e004d5eb2d4aa0cd8d80b449ae07367cb436d29403b7c15f0e0aff6976e2fd7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-603"></a>
## **1.6.7 Ticketing: priorities, routing, SLAs, macros, QA**

**Priorities & SLAs**

- **P0**: payments failing platform‑wide, data loss → page on‑call; **FRT ≤ 30m**.
- **P1**: payout issue, booking within 24–48h → **FRT ≤ 4h**.
- **P2**: general billing/account → **FRT ≤ 1 day**. Targets match your metrics section.

NonTechBlueprint

**Auto‑routing**

- **BILLING/PAYOUT** → Finance queue; **SAFETY** → T&S queue; **TECHNICAL** → Support Eng; rules set by **category + guided flow answers**.

NonTechBlueprint

**Macros (examples)**

- *Refund – partial (Quality ladder step 1)*: template pulls **package spec** + **evidence list** and posts a structured decision; applies ticket tags for later analytics.

NonTechBlueprint

- *Disable Instant Book (pending safety)*: pauses IB via Admin API and posts user‑visible explanation.

NonTechBlueprint

- *Request more info (deliverables)*: asks for missing proof within **24–48h cure** window.

NonTechBlueprint

**QA sampling:** randomly sample **5%** of closed tickets to review **macro adherence, empathy, correctness**.

NonTechBlueprint

**Breach alerts:** SLA timers drive **CloudWatch alarms** → pager for P0; views for P1/P2 backlog.
