---
id: TD-204
title: "**1.12.N Disaster recovery**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-204-112n-disaster-recovery\TD-204-overview.md"
parent_id: 
anchor: "TD-204"
checksum: "sha256:147eba085f89042350b925f5ed2111e771c56295f7ea3cdea31f2bc269bf2264"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-204"></a>
## **1.12.N Disaster recovery**

- **RPO**: ≤ 15 minutes for Aurora (PITR).
- **RTO**: ≤ 4 hours (restore + DNS flip) for critical path.
- **Runbook**: documented steps; quarterly drills (stage env); alarms that trigger the runbook.
