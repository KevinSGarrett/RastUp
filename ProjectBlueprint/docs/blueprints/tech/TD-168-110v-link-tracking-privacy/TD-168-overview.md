---
id: TD-168
title: "**1.10.V Link tracking & privacy**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-168-110v-link-tracking-privacy\TD-168-overview.md"
parent_id: 
anchor: "TD-168"
checksum: "sha256:0451e73b9b49a996055182e34e835eee680b790e65f277816210247f8b6c0be6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-168"></a>
## **1.10.V Link tracking & privacy**

- **Link wrapper**: */l/{token}* where *token = HMAC(user_id\|template_name\|msg_id\|url)*; logs *click* then 302 to *url*.
- **No tracking** for security/legal emails (privacy first) and unsubscribe links.
- **Open pixel** optional; respect **DNT** and suppress tracking for sensitive categories.
- **UTM** parameters for non‑critical emails only; strip PII.
- **Data minimization**: SMS never includes full names + full addresses + amounts in combination; use in‑app deep links.
