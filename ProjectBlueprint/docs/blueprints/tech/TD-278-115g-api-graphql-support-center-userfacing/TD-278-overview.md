---
id: TD-278
title: "**1.15.G API (GraphQL) & Support Center (user‑facing)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-278-115g-api-graphql-support-center-userfacing\TD-278-overview.md"
parent_id: 
anchor: "TD-278"
checksum: "sha256:e38d853b15846ec1624e9f3e17419bf29e6f44e4024dc42ed40560b5e89c9607"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-278"></a>
## **1.15.G API (GraphQL) & Support Center (user‑facing)**

*type SupportCase {*  
*caseId: ID!, type: String!, subtype: String, status: String!, severity: String!,*  
*createdAt: AWSDateTime!, updatedAt: AWSDateTime!,*  
*lbgId: ID, legId: ID, orderId: ID, studioId: ID, creatorId: ID,*  
*reasonCode: String, ownerUserId: ID, slaDueAt: AWSDateTime*  
*}*  
*type SupportMessage {*  
*msgId: ID!, authorRole: String!, bodyMd: String!, createdAt: AWSDateTime!*  
*attachments: \[Attachment!\]!*  
*}*  
*type SupportRefund { refundId: ID!, amountCents: Int!, status: String!, createdAt: AWSDateTime! }*  
  
*type Query {*  
*mySupportCases(cursor:String, limit:Int=20): \[SupportCase!\]!*  
*supportCase(caseId: ID!): SupportCase!*  
*supportMessages(caseId: ID!, cursor:String, limit:Int=50): \[SupportMessage!\]!*  
*}*  
  
*input OpenCaseInput {*  
*type: String!, subtype: String, severity: String = "normal",*  
*lbgId: ID, legId: ID, orderId: ID, studioId: ID, creatorId: ID,*  
*reasonCode: String, bodyMd: String!, attachments:\[AttachmentInput!\]*  
*}*  
  
*type Mutation {*  
*openCase(input: OpenCaseInput!): SupportCase!*  
*postSupportMessage(caseId: ID!, bodyMd: String!, attachments:\[AttachmentInput!\]): SupportMessage!*  
*closeCase(caseId: ID!): Boolean!*  
*}*  

**Guards**

- Role‑scoped visibility: buyer sees their cases; seller/creator sees cases naming them; agents see all.
- Attachments scanned (NSFW/AV) as in §1.14.4.
- Rate‑limits on open‑case attempts.

**Support Center UI**

- “Report a problem” flows pre‑filled from booking/order context.
- Case list, case detail with timeline, message composer, attachment upload, status chips.
