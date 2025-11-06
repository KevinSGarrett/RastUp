---
id: TD-457
title: "**1.23.5 Message Requests, Credits & Contact Filters**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-457-1235-message-requests-credits-contact-filters\TD-457-overview.md"
parent_id: 
anchor: "TD-457"
checksum: "sha256:18265e6c7a8411bc68a8a02cf0be45885f40d84dad7669a3443dc248d38b5e16"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-457"></a>
## **1.23.5 Message Requests, Credits & Contact Filters**

- **Requests:** First‑time contacts to a user route to *REQUESTS* until accepted; the inbox shows a separate **Requests** folder. Accept moves to normal inbox; Decline keeps a passive block entry.

NonTechBlueprint

- Credits:

  - Ledger *message_credit_ledger* grants **monthly “new conversation” credits** (amount configurable). Spending 1 credit allows *startConversation*. **Replies** do not consume credits; **booking threads** are exempt (unlimited).

NonTechBlueprint

- **Contact filters:** Enforce per recipient settings: **ID‑verified only**, **budget disclosed**, **date provided**. If unmet, present an **Action Card** form to collect missing fields before allowing send.

NonTechBlueprint
