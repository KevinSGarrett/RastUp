---
id: TD-602
title: "**1.6.6 Support Widget (guided flows & deflection)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-602-166-support-widget-guided-flows-deflection\TD-602-overview.md"
parent_id: 
anchor: "TD-602"
checksum: "sha256:ce00293a79862d80b09486538ed06ee7479d103d50e83178cbd5a2ef358e923c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-602"></a>
## **1.6.6 Support Widget (guided flows & deflection)**

**UX**

- Step 1: **Suggest articles** (live search over *kb_index* with role/city context).
- Step 2: **Guided flow** per category (dynamic form with 3–6 fields, e.g., booking ID, city, dates, screenshots).
- Step 3: If unresolved, **“Contact Support”** → we create a **ticket prefilled** with: user ID, session, platform, last 3 article IDs **viewed**, booking/studio IDs, environment, and screenshots. *(Your plan expressly requires attaching “read article IDs” to the ticket when a user still contacts support after deflection.)*

NonTechBlueprint

**GraphQL (*****api/schema/support.graphql*****)**

*type KBArticle { id: ID!, slug: String!, title: String!, summary: String!, bodyMd: String!, category: String!, updatedAt: AWSDateTime! }*  
*type KBSearchResult { id: ID!, slug: String!, title: String!, summary: String!, category: String! }*  
  
*input GuidedFlowContext { category: String!, bookingId: ID, orderId: ID, studioId: ID, city: String, dates: \[AWSDate!\], screenshots: \[AWSURL\] }*  
  
*type TicketResult { ticketId: ID!, externalId: String!, url: AWSURL! }*  
  
*type Query {*  
*kbSearch(q: String!, role: String, category: String): \[KBSearchResult!\]!*  
*kbArticle(slug: String!): KBArticle!*  
*}*  
  
*type Mutation {*  
*recordKBView(articleId: ID!): Boolean!*  
*createSupportTicket(flow: GuidedFlowContext!, readArticleIds: \[ID!\]!): TicketResult!*  
*}*  

**Adapter layer (*****/adapters/helpdesk/\******)**

- **Zendesk**: create ticket (brand, requester, custom fields), attach screenshots, set **priority** & **group** via rules, add internal note with KB reads.
- **Zammad**: same shape via REST; field mapping parity.
