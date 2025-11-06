---
id: TD-308
title: "**1.16‑C. GraphQL SDL — Saved Search, Feed, Referrals**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-308-116c-graphql-sdl-saved-search-feed-referrals\TD-308-overview.md"
parent_id: 
anchor: "TD-308"
checksum: "sha256:c8a3a11abe4c4b2f988dbbb96f19d425fa2cd5c242a78faa0e29c8928175a281"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-308"></a>
## **1.16‑C. GraphQL SDL — Saved Search, Feed, Referrals**

**Recommended filename/path:** *api/schema/growth.graphql*

*\# growth.graphql*  
  
*scalar AWSJSON*  
*scalar AWSDate*  
*scalar AWSDateTime*  
  
*type SavedSearch {*  
*searchId: ID!*  
*scope: String!*  
*city: String!*  
*queryJson: AWSJSON!*  
*pausedUntil: AWSDate*  
*lastAlertDt: AWSDate*  
*createdAt: AWSDateTime!*  
*updatedAt: AWSDateTime!*  
*}*  
  
*type SavedSearchAlert {*  
*alertId: ID!*  
*searchId: ID!*  
*alertDt: AWSDate!*  
*matchCount: Int!*  
*emailSent: Boolean!*  
*inappCreated: Boolean!*  
*createdAt: AWSDateTime!*  
*}*  
  
*type FeedCard {*  
*feedId: ID!*  
*authorId: ID!*  
*roleTags: \[String!\]!*  
*kind: String!*  
*title: String!*  
*bodyMd: String*  
*mediaPreview: AWSJSON!*  
*city: String*  
*verifiedChip: Boolean!*  
*createdAt: AWSDateTime!*  
*}*  
  
*type FeedPage { items: \[FeedCard!\]!, cursor: String }*  
  
*type ReferralInvite { inviteId: ID!, programId: ID!, inviterUserId: ID!, acceptedAt: AWSDateTime }*  
*type CreditLedger { entryId: ID!, userId: ID!, kind: String!, amountCents: Int!, reason: String!, createdAt: AWSDateTime! }*  
  
*input SavedSearchInput { scope: String!, city: String!, queryJson: AWSJSON! }*  
  
*type Query {*  
*mySavedSearches: \[SavedSearch!\]!*  
*myFeed(cursor: String, limit: Int = 25, tab: String): FeedPage!*  
*myCredits: \[CreditLedger!\]!*  
*}*  
  
*type Mutation {*  
*createSavedSearch(input: SavedSearchInput!): SavedSearch!*  
*pauseSavedSearch(searchId: ID!, days: Int!): SavedSearch!*  
*deleteSavedSearch(searchId: ID!): Boolean!*  
  
*follow(targetId: ID!, targetKind: String!): Boolean!*  
*unfollow(targetId: ID!, targetKind: String!): Boolean!*  
  
*sendReferral(programId: ID!, inviteeEmail: String!): Boolean!*  
*redeemCredit(entryId: ID!, amountCents: Int!): Boolean!*  
*}*
