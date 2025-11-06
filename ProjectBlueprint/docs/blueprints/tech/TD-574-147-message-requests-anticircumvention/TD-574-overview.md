---
id: TD-574
title: "**1.4.7 Message Requests & Anti‑circumvention**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-574-147-message-requests-anticircumvention\TD-574-overview.md"
parent_id: 
anchor: "TD-574"
checksum: "sha256:5de9b9fb24e30cae7e30735ae03920225aada2ba2cb7fce6350e6dda211c2bd7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-574"></a>
## **1.4.7 Message Requests & Anti‑circumvention**

- **Gated start**: new contact → *message_request_gate* created for the recipient. Inbox shows a preview card with **Accept / Decline / Block**.
- **Heuristics**: gates more aggressively for brand‑new senders (age, verification, prior accept ratio, text entropy).
- **Anti‑circumvention nudges**: detect phrases like off‑platform payment requests; show banner: “Keep payment on RastUp for protection.” Repeated attempts → **throttle** or **soft block**.
- **Credit / contact filters** (from non‑technical spec): large‑blast attempts or template spam are slowed; per‑hour caps applied via Dynamo *msg_rate*.
