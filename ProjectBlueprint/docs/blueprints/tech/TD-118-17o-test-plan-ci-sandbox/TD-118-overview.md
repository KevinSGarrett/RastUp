---
id: TD-118
title: "**1.7.O Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-118-17o-test-plan-ci-sandbox\TD-118-overview.md"
parent_id: 
anchor: "TD-118"
checksum: "sha256:9ab03f2f19fc0b10963914ad9d3dce8d28f917c67f62f9b13179c496a836cd9d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-118"></a>
## **1.7.O Test plan (CI + sandbox)**

**Correctness**

715. Eligible campaign appears only when it **matches filters** and city; ineligible campaigns never show.
716. Density caps respected with mixed inventory; no back‑to‑back promoted cards unless flag forces.
717. Featured slot reserved; if empty, organic card fills.

**Budget & pacing**  
4) Daily budget drains gradually in **even** mode under stable traffic; accelerated spends faster.  
5) Budget exhausted → campaign paused; resumes next day or after top‑up.

**Fraud & billing**  
6) Duplicate clicks within window deduped; bot UA/ip patterns flagged; only valid clicks billed.  
7) Post‑hoc invalidation issues **make‑good credits**.  
8) Ledger totals == Σ(valid_clicks × CPC); recon green vs Stripe top‑ups.

**Admin**  
9) Floor & cap updates take effect with versioning; rollback works; two‑person approval enforced.  
10) Campaign suspension/restore applies immediately; audit logged.

**Performance**  
11) p95 selection ≤ 30 ms after cache warm; ≤ 120 ms cold; overall search p95 still meets §1.2 SLOs.

**UX**  
12) “Promoted” chip visible; disclosure link opens policy page; analytics counts impressions/clicks.
