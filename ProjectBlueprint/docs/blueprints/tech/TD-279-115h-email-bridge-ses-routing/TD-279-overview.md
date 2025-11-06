---
id: TD-279
title: "**1.15.H Email bridge (SES) & routing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-279-115h-email-bridge-ses-routing\TD-279-overview.md"
parent_id: 
anchor: "TD-279"
checksum: "sha256:4cf18bacbd1f4d1594f777bfbdfcd29d6b9e849ce5efeff27bfd413b5b81b443"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-279"></a>
## **1.15.H Email bridge (SES) & routing**

- **Inbound**: [*case+{case_id}@support.rastup.com*](mailto:case+%7bcase_id%7d@support.rastup.com) → SES inbound rule → Lambda → *support_message* append (author detection via DKIM/DMARC + token).
- **Outbound**: replies include *Message‑ID*/*In‑Reply‑To*; List‑Unsubscribe for marketing categories unaffected.
- **Auto‑ack**: immediate “we received your request” message with case id and SLA.
