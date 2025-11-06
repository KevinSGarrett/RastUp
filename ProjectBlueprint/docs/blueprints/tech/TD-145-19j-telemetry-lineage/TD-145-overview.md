---
id: TD-145
title: "**1.9.J Telemetry & lineage**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-145-19j-telemetry-lineage\TD-145-overview.md"
parent_id: 
anchor: "TD-145"
checksum: "sha256:63bf4eb1a6810fb2a9f979d6409fb6688d5f2d21c2ddd0c37b54a7a48fd6caf8"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-145"></a>
## **1.9.J Telemetry & lineage**

- *fee.compute*, *fee.deferred.recorded*, *fee.earned.recorded*,
- *wallet.credit\|debit\|reversal*,
- *gl.entry.write*, *gl.export*,
- *recon.daily.start\|succeeded\|failed*, *recon.variance.notice*.  
  Every event includes *lbg_id/leg_id*, amounts, and relevant external refs (PI id, refund id, transfer id, balance txn id).
