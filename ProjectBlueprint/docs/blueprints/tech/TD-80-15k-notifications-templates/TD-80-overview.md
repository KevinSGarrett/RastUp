---
id: TD-80
title: "**1.5.K Notifications & templates**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-80-15k-notifications-templates\TD-80-overview.md"
parent_id: 
anchor: "TD-80"
checksum: "sha256:6cddd7201075222241d72f67f70242e25c267111893eb484ac3ca3f8354f4298"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-80"></a>
## **1.5.K Notifications & templates**

- Triggers: envelope sent, signer reminder (24h cadence), nearing expiry, completed.
- Channels: email (primary), push (secondary), SMS (reminders only, no links to PII).
- Templates parameterized by *{role}*, *{doc_name}*, *{deadline}*, *{thread_url}*; live in the Comms adapter.
