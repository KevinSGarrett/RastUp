---
id: TD-432
title: "**1.21.J Telemetry, evaluation & experimentation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-432-121j-telemetry-evaluation-experimentation\TD-432-overview.md"
parent_id: 
anchor: "TD-432"
checksum: "sha256:e81171e1d45d85f45638895771772142c215f9f4fe9c0e2b95ea102266425c74"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-432"></a>
## **1.21.J Telemetry, evaluation & experimentation**

- **Events:** *search.query\|results\|click\|zero_results*, *search.autocomplete.select*, *search.suggest.click*.
- **Quality:** CTR@k, save rate@k, message‑start/booking start&complete@k, zero‑results rate.
- **Offline eval:** compute **NDCG@10** weekly from interaction labels; compare weight variants; guardrails for result diversity.

**NDCG SQL (simplified):** *search/eval/ndcg.sql*.
