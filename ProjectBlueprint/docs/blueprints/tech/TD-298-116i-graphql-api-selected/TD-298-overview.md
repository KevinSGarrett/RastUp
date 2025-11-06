---
id: TD-298
title: "**1.16.I GraphQL API (selected)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-298-116i-graphql-api-selected\TD-298-overview.md"
parent_id: 
anchor: "TD-298"
checksum: "sha256:9d90e5a1643510fa882d9849ac49e0ddbb0c401ccced65cf1bc1a65a6e8d854f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-298"></a>
## **1.16.I GraphQL API (selected)**

*\# Saved search & alerts*  
*type SavedSearch { searchId: ID!, scope: String!, city: String!, queryJson: AWSJSON!, pausedUntil: AWSDate }*  
*type SavedSearchAlert { alertId: ID!, alertDt: AWSDate!, matchCount: Int!, emailSent: Boolean!, inappCreated: Boolean! }*  
  
*type Query {*  
*mySavedSearches: \[SavedSearch!\]!*  
*myFeed(cursor: String, limit: Int = 25, tab: String): FeedPage!*  
*}*  
  
*input SavedSearchInput { scope: String!, city: String!, queryJson: AWSJSON! }*  
  
*type Mutation {*  
*createSavedSearch(input: SavedSearchInput!): SavedSearch!*  
*pauseSavedSearch(searchId: ID!, days: Int!): SavedSearch! \# 30 days typical*  
*deleteSavedSearch(searchId: ID!): Boolean!*  
  
*follow(targetId: ID!, targetKind: String!): Boolean!*  
*unfollow(targetId: ID!, targetKind: String!): Boolean!*  
  
*sendReferral(programId: ID!, inviteeEmail: String!): Boolean!*  
*redeemCredit(entryId: ID!, amountCents: Int!): Boolean! \# buyer fee only scope validated server-side*  
*}*  

**Server guards**: Safe‑Mode checks in feed; per‑search daily dedupe; per‑user referral caps; ID/age gate for credit redemption where required.
