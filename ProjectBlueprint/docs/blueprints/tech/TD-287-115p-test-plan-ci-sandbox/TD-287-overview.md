---
id: TD-287
title: "**1.15.P Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-287-115p-test-plan-ci-sandbox\TD-287-overview.md"
parent_id: 
anchor: "TD-287"
checksum: "sha256:55ed9506fbf5f4d8a707a7ec5e883d4c31ee3f29f6457048c51b2c0095847261"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-287"></a>
## **1.15.P Test plan (CI + sandbox)**

**Core flows**

1678. Open case from booking/order context; timeline auto‑stitches evidence.
1679. Deterministic refund outcomes by cancellation bands; manual override requires dual approval.
1680. Payout hold applied & released; finance views update.

**Chargebacks**  
4) Chargeback intake; evidence pack creation; representment submitted; outcome handling (GL + risk).

**DMCA & policy**  
5) DMCA hides content; counter‑notice restores; audits present.  
6) Policy violation escalations; appeals path.

**Email bridge**  
7) Inbound email creates/appends case; spoofing rejected; attachments scanned.  
8) Outbound reply threading correct.

**SLA & automations**  
9) SLA timers escalate; macros apply consistent decisions; rules trigger holds on thresholds.

**Analytics**  
10) Case events land in Bronze → Silver → Gold (§1.13); dashboards show backlog and win rates.

**Performance & cost**  
11) p95 case list fetch ≤ 120 ms; evidence download streams; S3 lifecycle verified.
