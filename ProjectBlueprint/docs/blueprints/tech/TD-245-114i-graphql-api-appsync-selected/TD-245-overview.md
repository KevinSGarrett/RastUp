---
id: TD-245
title: "**1.14.I GraphQL API (AppSync) — selected**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-245-114i-graphql-api-appsync-selected\TD-245-overview.md"
parent_id: 
anchor: "TD-245"
checksum: "sha256:31e0dbb96a1bf949cb855d56638074eb98f00639b60b6df24471db44ad7f79fa"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-245"></a>
## **1.14.I GraphQL API (AppSync) — selected**

*type FansubCreator {*  
*creatorId: ID!, handle: String!, displayName: String!,*  
*priceMonthCents: Int!, currency: String!, isPublished: Boolean!,*  
*nsfwOk: Boolean!, idvRequiredOk: Boolean!*  
*}*  
  
*type SubscriptionStatus { status: String!, currentPeriodEnd: AWSDateTime!, renews: Boolean! }*  
  
*type PPVPost {*  
*ppvId: ID!, title: String!, caption: String, priceCents: Int!,*  
*previewMedia: \[Attachment!\]!, nsfwBand: Int!, isPublished: Boolean!*  
*}*  
  
*type Query {*  
*fansubCreator(handle: String!): FansubCreator!*  
*fansubPPV(creatorHandle: String!, cursor: String, limit: Int=12): PPVPage!*  
*mySubscription(creatorId: ID!): SubscriptionStatus*  
*myPPVAccess(ppvId: ID!): Boolean!*  
*}*  
  
*type Mutation {*  
*publishFansubCreator(input: FansubCreatorInput!): FansubCreator!*  
*subscribe(creatorId: ID!): SubscriptionStatus! \# kicks off Stripe flow*  
*cancelSubscription(subId: ID!): Boolean!*  
  
*tip(creatorId: ID!, amountCents: Int!): Boolean!*  
*buyPPV(ppvId: ID!): Boolean!*  
  
*requestQuote(creatorId: ID!, title: String!, brief: String!, priceCents: Int!): ID!*  
*acceptQuote(requestId: ID!): Boolean!*  
*deliverRequest(requestId: ID!, manifestRef: ID!, note: String): Boolean!*  
*approveRequest(requestId: ID!): Boolean!*  
*requestRevision(requestId: ID!, note: String!): Boolean!*  
*}*  

**Server guards**

- All mutations check **IDV age gate** from §1.6.
- Entitlement gating for PPV & subscriber‑only posts.
- Rate limits on tips/requests to prevent abuse.
- Pricing floors/ceilings from AppConfig to avoid outliers.
