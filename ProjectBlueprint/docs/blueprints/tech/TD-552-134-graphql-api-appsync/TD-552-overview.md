---
id: TD-552
title: "**1.3.4 GraphQL API (AppSync)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-552-134-graphql-api-appsync\TD-552-overview.md"
parent_id: 
anchor: "TD-552"
checksum: "sha256:c6ec731c9b4f755caf559307ee2355354b0e296052417cba5b2a8953a4946640"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-552"></a>
## **1.3.4 GraphQL API (AppSync)**

**Recommended path:** *api/schema/booking.graphql*

*enum BookingMode { IB RTB INVITE }*  
*enum BookingStatus {*  
*INITIATED PENDING_ACCEPT COUNTERED ACCEPTED DECLINED*  
*CONFIRMED IN_PROGRESS DELIVERED COMPLETED*  
*CANCELLED_BUYER CANCELLED_PROVIDER DISPUTED RESOLVED*  
*}*  
  
*type LineItem { id: ID!, kind: String!, title: String!, qty: Float!, unitCents: Int!, totalCents: Int! }*  
*type Milestone { id: ID!, title: String!, dueTs: AWSDateTime, amountCents: Int!, status: String! }*  
  
*type Order {*  
*id: ID!, buyerId: ID!, providerId: ID!, serviceProfileId: ID!,*  
*mode: BookingMode!, status: BookingStatus!,*  
*startTs: AWSDateTime!, endTs: AWSDateTime!,*  
*locationKind: String!, city: String,*  
*licenseTier: String, subtotalCents: Int!, platformFeeCents: Int!, taxCents: Int!, tipCents: Int!, totalCents: Int!,*  
*lineItems: \[LineItem!\]!, milestones: \[Milestone!\]!,*  
*chatThreadId: ID*  
*}*  
  
*input StartOrderInput {*  
*serviceProfileId: ID!, mode: BookingMode!, packageId: ID,*  
*startTs: AWSDateTime!, endTs: AWSDateTime!, city: String, locationKind: String!,*  
*extras: \[ID!\], licenseTier: String, travelMiles: Float*  
*}*  
*input CounterOfferInput { orderId: ID!, newStartTs: AWSDateTime, newEndTs: AWSDateTime, lineItemChanges: AWSJSON }*  
*input AcceptInput { requestId: ID! }*  
*input DeclineInput { requestId: ID!, reason: String }*  
*input ConfirmIBInput { orderId: ID! } \# IB fast path*  
*input CreateInviteInput { brief: String!, recipients: \[ID!\]!, startTs: AWSDateTime!, endTs: AWSDateTime!, packageId: ID, budgetCents: Int }*  
*input AwardInviteInput { inviteId: ID!, recipientId: ID! }*  
*input CompleteInput { orderId: ID!, milestoneId: ID } \# time- or deliverable-based*  
*input DisputeInput { orderId: ID!, reason: String!, description: String }*  
  
*type Query {*  
*order(id: ID!): Order*  
*myOrders(page: Int = 1): \[Order!\]!*  
*myRequests(page: Int = 1): \[AWSJSON!\]!*  
*}*  
  
*type Mutation {*  
*startOrder(input: StartOrderInput!): ID! @auth(role: "user")*  
*sendRequest(orderId: ID!, message: String): ID! @auth(role: "user")*  
*confirmInstantBook(input: ConfirmIBInput!): Boolean! @auth(role: "user")*  
*counterOffer(input: CounterOfferInput!): Boolean! @auth(role: "user")*  
*acceptRequest(input: AcceptInput!): Boolean! @auth(role: "user")*  
*declineRequest(input: DeclineInput!): Boolean! @auth(role: "user")*  
  
*createInvite(input: CreateInviteInput!): ID! @auth(role: "user")*  
*awardInvite(input: AwardInviteInput!): Boolean! @auth(role: "user")*  
  
*completeWork(input: CompleteInput!): Boolean! @auth(role: "user")*  
*openDispute(input: DisputeInput!): ID! @auth(role: "user")*  
*}*
