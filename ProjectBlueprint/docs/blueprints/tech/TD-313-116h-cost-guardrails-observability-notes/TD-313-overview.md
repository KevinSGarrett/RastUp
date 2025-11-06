---
id: TD-313
title: "**1.16‑H. Cost guardrails (observability notes)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-313-116h-cost-guardrails-observability-notes\TD-313-overview.md"
parent_id: 
anchor: "TD-313"
checksum: "sha256:8bba85049b7d545f36ed2dc2da6e887bcbe151389043daa88c6883be812a1d11"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-313"></a>
## **1.16‑H. Cost guardrails (observability notes)**

**Recommended filename/path:** *observability/budgets/growth-guards.md*

*Metrics & alarms:*  
*- SES sends/day: warn at 80% of daily cap; hard stop at 120% (switch to in-app only).*  
*- Lambda duration: P95 \> 750ms sustained 10m → investigate search query shapes.*  
*- Dynamo RCU/WCU: consume \> 80% for 15m → auto scale + alert.*  
*- Typesense/OpenSearch: QPS spikes \> 3x baseline → enable precomputed match hashes for saved-search batch.*  

# **§1.16 — Artifacts (inline, text-only) — Continuation**

Below are the remaining **copy-pasteable** blocks for the project plan. Each includes a **Recommended filename/path** label so your builders can later lift them into a repo if you choose. These are all text for your single Word doc.
