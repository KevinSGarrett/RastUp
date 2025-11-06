---
id: TD-221
title: "**1.13.L Error taxonomy (data platform)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-221-113l-error-taxonomy-data-platform\TD-221-overview.md"
parent_id: 
anchor: "TD-221"
checksum: "sha256:ba021ced8db62c3d14e703e2c506fc3d8acc523a39fadcf288686a0ef980207e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-221"></a>
## **1.13.L Error taxonomy (data platform)**

- *EVENT_SCHEMA_INVALID* — payload fails JSON Schema.
- *EVENT_REJECTED_RATE_LIMIT* — client flooding; sample/delay.
- *PIPELINE_LAG_EXCEEDED* — Bronze→Silver lag \> SLO.
- *QUALITY_CHECK_FAILED* — Great Expectations failed (which check & partition).
- *DSAR_CONFLICT* — deletion collides with legal hold.
- *BI_REFRESH_FAILED* — SPICE refresh failed.
