---
id: TD-72
title: "**1.5.C Clause library & variables**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-72-15c-clause-library-variables\TD-72-overview.md"
parent_id: 
anchor: "TD-72"
checksum: "sha256:2dd68381bdc82006fd86061dfece488cea8bc127093b72f65f73477a2de20c6a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-72"></a>
## **1.5.C Clause library & variables**

**Clause authoring**

- Authored in **Markdown** with limited components: headings, lists, clause refs, and **variable placeholders** in *{{snake_case}}*.
- Variables must be declared in *variables_json* with type, description, and example. Supported types: *string*, *int*, *money_cents*, *datetime*, *date*, *duration*, *enum{…}*, *address*.

**Examples**

- SOW “Base Terms” requires: *{{service_date}}*, *{{start_time}}*, *{{end_time}}*, *{{location_address}}*, *{{deliverables_summary}}*, *{{total_price}}*, *{{taxes}}*, *{{cancellation_policy_summary}}*.
- Model Release (Adult) requires: *{{model_legal_name}}*, *{{model_dob}}* (age verification gate), *{{usage_scope}}*, *{{territory}}*, *{{duration}}*, *{{compensation_summary}}*.
- Studio Rules requires: *{{studio_name}}*, *{{safety_rules}}*, *{{deposit_amount}}*, *{{damage_policy}}*.

**City & role gates**

- Clauses and templates can be constrained by **city** (local rules) and **role** (e.g., Model Releases apply only to Talent legs). City gates align to your feature‑flag model.

**Versioning**

- Clauses are immutable once published; edits create a **new version**. Templates reference clause **name + version** explicitly to guarantee reproducible renders.
