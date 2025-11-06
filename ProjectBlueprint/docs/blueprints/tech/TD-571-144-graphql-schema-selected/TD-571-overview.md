---
id: TD-571
title: "**1.4.4 GraphQL schema (selected)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-571-144-graphql-schema-selected\TD-571-overview.md"
parent_id: 
anchor: "TD-571"
checksum: "sha256:26b610262311f2cbf75ad302f55e48ee8e07077069b7161b46e445dc79c8dffd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-571"></a>
## **1.4.4 GraphQL schema (selected)**

**Recommended path:** *api/schema/messaging.graphql*

*enum ThreadKind { INQUIRY BOOKING STUDIO INVITE SUPPORT }*  
*enum MessageKind { TEXT IMAGE FILE CARD }*  
*enum RequestStatus { PENDING ACCEPTED DECLINED BLOCKED EXPIRED }*  
  
*type Thread {*  
*id: ID!, kind: ThreadKind!, subject: String, orderId: ID,*  
*participants: \[Participant!\]!, lastMessageAt: AWSDateTime, unreadCount: Int*  
*}*  
  
*type Participant { userId: ID!, role: String, status: String, lastReadAt: AWSDateTime, mutedUntil: AWSDateTime }*  
  
*type Message {*  
*id: ID!, kind: MessageKind!, bodyText: String, cardType: String, cardPayload: AWSJSON,*  
*attachment: AWSJSON, senderUser: ID!, createdAt: AWSDateTime!, editedAt: AWSDateTime*  
*}*  
  
*type MessageRequestGate { id: ID!, threadId: ID!, targetUser: ID!, status: RequestStatus!, expiresAt: AWSDateTime, reason: String }*  
  
*input SendTextInput { threadId: ID!, bodyText: String! }*  
*input SendFileInput { threadId: ID!, fileName: String!, contentType: String! } \# returns presigned URL*  
*input CreateThreadInput { kind: ThreadKind!, subject: String, toUserId: ID, orderId: ID }*  
*input AcceptGateInput { gateId: ID! }*  
*input DeclineGateInput { gateId: ID!, reason: String }*  
*input BlockUserInput { userId: ID!, reason: String }*  
*input CardInput { threadId: ID!, type: String!, payload: AWSJSON! } \# reschedule, extras, proofs, expense, complete, dispute, safety*  
  
*type Query {*  
*inbox(folder: String, page: Int = 1): \[Thread!\]!*  
*thread(threadId: ID!): Thread!*  
*messages(threadId: ID!, page: Int = 1): \[Message!\]!*  
*requestGate(threadId: ID!, forUserId: ID!): MessageRequestGate*  
*}*  
  
*type Mutation {*  
*createThread(input: CreateThreadInput!): ID!*  
*sendText(input: SendTextInput!): ID!*  
*getFileUploadUrl(input: SendFileInput!): AWSJSON!*  
*sendCard(input: CardInput!): ID!*  
  
*acceptMessageRequest(input: AcceptGateInput!): Boolean!*  
*declineMessageRequest(input: DeclineGateInput!): Boolean!*  
*blockUser(input: BlockUserInput!): Boolean!*  
  
*markRead(threadId: ID!): Boolean!*  
*moveToFolder(threadId: ID!, folder: String!): Boolean!*  
*setMuted(threadId: ID!, until: AWSDateTime): Boolean!*  
*}*  

**Notes**

- **Message Request** flow: a new thread *does not* notify or display fully until the recipient **accepts**; preview shows limited profile/card. **Decline** closes the gate and moves the thread to *Spam*. **Block** creates *user_block* and hides future attempts.
- **Action Cards** are first‑class messages with *cardType* and structured *cardPayload* (see §1.4.6).
