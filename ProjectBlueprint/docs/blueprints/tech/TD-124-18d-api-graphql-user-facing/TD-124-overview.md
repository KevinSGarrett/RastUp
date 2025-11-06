---
id: TD-124
title: "**1.8.D API (GraphQL) — user-facing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-124-18d-api-graphql-user-facing\TD-124-overview.md"
parent_id: 
anchor: "TD-124"
checksum: "sha256:97f8bbb5c3ec7cb706d86e057ea85c219c5ec7d08c0c892c7ff20eb2700d7155"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-124"></a>
## **1.8.D API (GraphQL) — user-facing**

*type Review {*  
*reviewId: ID!*  
*targetType: String!*  
*targetId: ID!*  
*rating: Int!*  
*title: String*  
*body: String*  
*facets: AWSJSON*  
*photos: \[Attachment!\]!*  
*status: String!*  
*createdAt: AWSDateTime!*  
*}*  
  
*type Reputation {*  
*ratingAvg: Float!*  
*ratingCount: Int!*  
*ratingRecentAvg: Float!*  
*facetAvgs: AWSJSON*  
*lastReviewAt: AWSDateTime*  
*}*  
  
*input CreateReviewInput {*  
*legId: ID!*  
*targetType: String! \# 'service_profile' or 'studio'*  
*targetId: ID!*  
*rating: Int!*  
*title: String*  
*body: String*  
*facets: AWSJSON*  
*photos: \[AttachmentInput!\]*  
*}*  
  
*type Query {*  
*reviews(targetType: String!, targetId: ID!, cursor: String, limit: Int = 10): ReviewPage!*  
*reputation(targetType: String!, targetId: ID!): Reputation!*  
*myEligibleToReview: \[LegRef!\]! \# legs completed but not yet reviewed*  
*}*  
  
*type Mutation {*  
*createReview(input: CreateReviewInput!): Review!*  
*editReview(reviewId: ID!, title: String, body: String, facets: AWSJSON): Review! \# within window*  
*reportReview(reviewId: ID!, reason: String!, details: String): Boolean!*  
*}*  

**Server guards**

- Verify target matches the leg’s counterparty (SP for talent leg; Studio for studio leg).
- Deny self-review (*author_user_id == seller_user_id*), deny cross-scope attempts.
- Rate-limit review write attempts per user.
