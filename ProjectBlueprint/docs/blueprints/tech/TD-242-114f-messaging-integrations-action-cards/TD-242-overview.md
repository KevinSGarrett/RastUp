---
id: TD-242
title: "**1.14.F Messaging integrations (action cards)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-242-114f-messaging-integrations-action-cards\TD-242-overview.md"
parent_id: 
anchor: "TD-242"
checksum: "sha256:5810b20f478d9bf9a8ce66315877fbca7f59d69dfc04c1717eb713478c211a70"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-242"></a>
## **1.14.F Messaging integrations (action cards)**

- **Request Quote** → **Pay** → **Deliver** → **Approve/Revise** loops occur in the **thread** using **action cards** defined in §1.4.E (reused with *ACTION_TYPE = FS_REQUEST\_\**).
- **Tip receipt** and **PPV unlocked** post system messages into the thread (optional; user‑toggle).
- **Nudges** (comms §1.10) for unsigned docs if the creator uses any release forms (off by default for Fan‑Sub).
