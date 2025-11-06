---
id: TD-265
title: "**1.14.12 GraphQL SDL — extended (selected)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-265-11412-graphql-sdl-extended-selected\TD-265-overview.md"
parent_id: 
anchor: "TD-265"
checksum: "sha256:882f2ed19bc01563f215d017e0af8d4fdf3731a78eba2cd3e7e5ea0c9467ec29"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-265"></a>
## **1.14.12 GraphQL SDL — extended (selected)**

*enum FansubOrderKind { TIP PPV REQUEST }*  
*enum FansubRequestStatus { QUOTED ACCEPTED PAID DELIVERED APPROVED REVISION_REQUESTED REFUNDED DISPUTED CLOSED }*  
*enum FansubNSFWBand { SAFE BLUR BLOCK }*  
  
*type FansubOrder {*  
*orderId: ID! kind: FansubOrderKind!*  
*amountCents: Int! feeCents: Int! taxCents: Int! currency: String!*  
*status: String! createdAt: AWSDateTime!*  
*}*  
  
*type PPVAccess { ppvId: ID!, purchasedAt: AWSDateTime! }*  
  
*type Mutation {*  
*\# Admin-ish helpers for creators:*  
*setFansubPrices(priceMonthCents: Int!): FansubCreator!*  
*publishPPV(input: PPVInput!): PPVPost!*  
*unpublishPPV(ppvId: ID!): Boolean!*  
  
*\# Purchases:*  
*buyPPV(ppvId: ID!): FansubOrder! \# returns order + client secret if needed*  
*tip(creatorId: ID!, amountCents: Int!): FansubOrder!*  
*subscribe(creatorId: ID!): SubscriptionStatus!*  
  
*\# Requests flow:*  
*requestQuote(creatorId: ID!, title: String!, brief: String!, priceCents: Int!): ID!*  
*acceptQuote(requestId: ID!): FansubOrder!*  
*deliverRequest(requestId: ID!, proofManifest: ManifestInput!): Boolean!*  
*approveRequest(requestId: ID!, finalManifest: ManifestInput!): Boolean!*  
*requestRevision(requestId: ID!, note: String!): Boolean!*  
*}*  

Server injects idempotency keys; returns PaymentIntent client secrets where applicable.
