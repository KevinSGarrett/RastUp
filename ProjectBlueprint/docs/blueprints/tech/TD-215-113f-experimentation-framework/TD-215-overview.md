---
id: TD-215
title: "**1.13.F Experimentation framework**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-215-113f-experimentation-framework\TD-215-overview.md"
parent_id: 
anchor: "TD-215"
checksum: "sha256:a74f4389c81c67c46c59ba87a01a13accc6251bbf19dd4d652b05230d584a45d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-215"></a>
## **1.13.F Experimentation framework**

**Assignment**

- Sticky bucket per *user_id* (or *anon_id* pre‑login) via salted hash (e.g., *hash(user_id + exp_key) % 100*).
- Variants defined in AppConfig (feature flags). Exposure logged as *exp.exposed* at first checkpoint.

**Metrics & guardrails**

- Primary metrics per experiment pre‑declared; guardrails include: refund rate, complaint rate, SLO latency, bounce for comms.
- **CUPED** or stratified analyses supported by exporting **per‑user aggregates** (pre‑period covariates).
- **Sequential** or fixed horizon; maintain cookbook for analysts.

**Data**

- *dim_exposure* table links *user_id*/*anon_id* to *exp_key*, *variant*, *exposed_at*.
- Gold layer produces per‑variant metric tables with p‑values/CI (analyst notebooks).
