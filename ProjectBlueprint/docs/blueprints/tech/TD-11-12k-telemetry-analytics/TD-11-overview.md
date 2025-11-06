---
id: TD-11
title: "**1.2.K Telemetry & analytics**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-11-12k-telemetry-analytics\TD-11-overview.md"
parent_id: 
anchor: "TD-11"
checksum: "sha256:1f06c3ce739a080378012a35ca83bb180544a84c904fa88b74058abf72a4d3ee"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-11"></a>
## **1.2.K Telemetry & analytics**

**Events**

- *search.open*, *search.filters.apply*, *search.query.execute*, *search.results.render*, *search.result.impression*, *search.result.click*, *search.result.save*, *search.error*, *search.latency*.
- Promotions: *promo.slot.impression*, *promo.slot.click*, *promo.invalid_click.flag*, *promo.credit.issued*.
- Integrity: *search.integrity.invalid_request*, *search.abuse.robot_detected*.

**Metrics**

- CTR by role/facet; budget fit distribution; verified share; availability hit rate; density cap compliance; diversity indices.
