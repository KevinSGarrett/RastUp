---
id: TD-16
title: "**1.2.P Cost controls**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-16-12p-cost-controls\TD-16-overview.md"
parent_id: 
anchor: "TD-16"
checksum: "sha256:86a4c28b5469ba999c050175652e0121562c242cf8785d4bc8967976308ec1b6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-16"></a>
## **1.2.P Cost controls**

- **Typesense**: single small node (or managed starter), vertical scale when QPS rises; replica optional for HA.
- **OpenSearch Serverless** (if chosen): **OCU cap** per region; alarms on sustained OCU \> 80%.
- Cache TTLs keep engine calls low; nightly reindex batched to off‑peak hours.
