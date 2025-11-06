---
id: TD-62
title: "**1.4.I File pipeline & limits**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-62-14i-file-pipeline-limits\TD-62-overview.md"
parent_id: 
anchor: "TD-62"
checksum: "sha256:884f47c527cf8faea6f2931c27494e7180175749dc62634a812d16c8420c2e00"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-62"></a>
## **1.4.I File pipeline & limits**

- **Uploads**: signed S3 URLs; client streams **previews** only; large files rejected; user pointed to “attach external link.”
- **Scanning**: Lambda antivirus + vision safety; quarantine bucket for suspects; admin override with audit.
- **Preview transforms**: Lambda@Edge resizes images on demand; video previews transcoded to HLS snippets with caps.
- **Limits (launch)**: preview ≤ 20 MB; images ≤ 12k px max dimension; videos ≤ 60s preview.
