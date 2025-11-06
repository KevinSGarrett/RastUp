---
id: TD-13
title: "**1.2.M Error model (API)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-13-12m-error-model-api\TD-13-overview.md"
parent_id: 
anchor: "TD-13"
checksum: "sha256:c614d483d52f03c890a4c3947bb110309ee06e109166590b50b40ee57763aaf7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-13"></a>
## **1.2.M Error model (API)**

- *SEARCH_INVALID_LOCATION* — unresolvable or mismatched city vs lat/lon.
- *SEARCH_UNDERAGE_SAFEMODE* — attempted explicit toggle without age verification.
- *SEARCH_ROLE_FILTER_CONFLICT* — role‑specific filter provided for wrong role.
- *SEARCH_CITY_GATED* — surface disabled for this city.
- *SEARCH_TOO_MANY_PARAMS* — exceeded allowed number of facets.
- *SEARCH_ENGINE_ERROR* — upstream engine error (masked; logged with corrId).

All error payloads include *code*, *message*, *hint*, and a correlation id.
