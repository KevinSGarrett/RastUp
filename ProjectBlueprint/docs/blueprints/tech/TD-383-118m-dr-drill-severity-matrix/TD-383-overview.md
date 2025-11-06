---
id: TD-383
title: "**1.18.M DR Drill & Severity Matrix**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-383-118m-dr-drill-severity-matrix\TD-383-overview.md"
parent_id: 
anchor: "TD-383"
checksum: "sha256:0c0a3a58804764fafa9c8b6ea92ba4589e7a6e1901397e354d88df348922bc58"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-383"></a>
## **1.18.M DR Drill & Severity Matrix**

**Recommended path:** *security/ir/severity-matrix.md*

*Severities*  
*- P0: data exfiltration confirmed; payments outage \> 30 min*  
*- P1: partial outage; suspected credential leak*  
*- P2: localized bug with security impact; WAF false positive spike*  
  
*DR Drill (quarterly)*  
*- Restore Aurora snapshot to stage clone; switch read traffic for an hour; verify parity.*  
*- Simulate region impairment: serve static from CF + cached ISR; payments degraded mode on.*  
*- Outcome recorded; gaps turned into CAPA tickets.*
