---
id: TD-455
title: "**1.23.3 GraphQL Schema (AppSync)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-455-1233-graphql-schema-appsync\TD-455-overview.md"
parent_id: 
anchor: "TD-455"
checksum: "sha256:2056e043ec2f6978837086a4dd1e44aaa32ae02b89c33314c8ae8a2efba8544d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-455"></a>
## **1.23.3 GraphQL Schema (AppSync)**

**Recommended path:** *api/schema/messaging.graphql*

*enum ThreadType { INQUIRY INVITE BOOKING DISPUTE SYSTEM }*  
*enum ThreadStatus { OPEN AWAITING_REPLY PENDING_DECISION CONFIRMED COMPLETED DISPUTED ARCHIVED }*  
*enum MessageKind { TEXT ATTACHMENT ACTION SYSTEM STATE }*  
  
*type Thread {*  
*threadId: ID!*  
*type: ThreadType!*  
*roleContext: String!*  
*participants: \[ID!\]!*  
*bookingId: ID*  
*status: ThreadStatus!*  
*lastMessageAt: AWSDateTime!*  
*unreadCount: Int!*  
*project: ProjectPanel*  
*requestState: String*  
*}*  
  
*type Message {*  
*messageId: ID!*  
*threadId: ID!*  
*senderId: ID!*  
*ts: AWSDateTime!*  
*kind: MessageKind!*  
*text: String*  
*attachments: \[Attachment!\]*  
*action: ActionCard*  
*}*  
  
*type Attachment { key: String!, mime: String!, bytes: Int!, thumbKey: String }*  
*type ProjectPanel {*  
*packageId: ID*  
*schedule: AWSJSON*  
*location: AWSJSON*  
*callSheet: AWSJSON*  
*contracts: \[ID!\]*  
*deliverables: AWSJSON*  
*payments: AWSJSON*  
*}*  
  
*union ActionCard = ProposeTime \| Reschedule \| AddExtras \| Overtime \| UploadProofs \| RequestApproval \| ExpenseReceipt \| MarkCompleted \| OpenDispute \| ShareLocation \| SafetyFlag*  
*type ProposeTime { start: AWSDateTime!, end: AWSDateTime!, timezone: String! }*  
*type Reschedule { reason: String!, options: \[ProposeTime!\]! }*  
*type AddExtras { items: \[ExtraInput!\]! }*  
*input ExtraInput { sku: ID!, qty: Int! }*  
*type Overtime { minutes: Int!, rateCents: Int! }*  
*type UploadProofs { files: \[Attachment!\]! }*  
*type RequestApproval { assetIds: \[ID!\]!, due: AWSDateTime }*  
*type ExpenseReceipt { amountCents: Int!, memo: String!, attachment: Attachment }*  
*type MarkCompleted { note: String }*  
*type OpenDispute { reason: String!, detail: String }*  
*type ShareLocation { lat: Float!, lon: Float!, until: AWSDateTime }*  
*type SafetyFlag { category: String!, note: String }*  
  
*type Query {*  
*inbox(folder: String, after: String, limit: Int = 30): \[Thread!\]!*  
*thread(threadId: ID!): Thread!*  
*messages(threadId: ID!, after: String, limit: Int = 50): \[Message!\]!*  
*}*  
  
*type Mutation {*  
*startConversation(toUserId: ID!, roleContext: String!, bookingId: ID, firstMessage: String!): Thread!*  
*sendMessage(threadId: ID!, kind: MessageKind!, text: String, attachments: \[AttachmentInput!\], action: AWSJSON): Message!*  
*setTyping(threadId: ID!, on: Boolean!): Boolean!*  
*markRead(threadId: ID!, upToTs: AWSDateTime!): Boolean!*  
*acceptRequest(threadId: ID!): Boolean!*  
*declineRequest(threadId: ID!, reason: String): Boolean!*  
*blockUser(userId: ID!, reason: String): Boolean!*  
*reportMessage(messageId: ID!, reason: String!, detail: String): Boolean!*  
*}*  
  
*input AttachmentInput { key: String!, mime: String!, bytes: Int!, thumbKey: String }*  
*type Subscription {*  
*onThreadEvent(threadId: ID!): Message! @aws_subscribe(mutations: \["sendMessage"\])*  
*}*  

**Mapping:** Types, statuses, and action cards mirror the non‑tech definitions and project panel contents.

NonTechBlueprint
