---
id: TD-113
title: "**1.7.J GraphQL API (seller‑facing & admin)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-113-17j-graphql-api-sellerfacing-admin\TD-113-overview.md"
parent_id: 
anchor: "TD-113"
checksum: "sha256:18d235a21c06fa402d061471a7ad8fd94df870d3fa1ebdb1ea4f7556dde996a0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-113"></a>
## **1.7.J GraphQL API (seller‑facing & admin)**

*\# Seller APIs*  
*type Campaign {*  
*campaignId: ID!*  
*name: String!*  
*status: String!*  
*surface: String!*  
*format: String!*  
*targetEntityId: ID!*  
*cities: \[String!\]!*  
*cpcCents: Int!*  
*dailyBudgetCents: Int!*  
*totalBudgetCents: Int*  
*spendTodayCents: Int!*  
*spendTotalCents: Int!*  
*}*  
  
*type CampaignStats {*  
*campaignId: ID!*  
*date: AWSDate!*  
*impressions: Int!*  
*clicks: Int!*  
*ctr: Float!*  
*avgCpcCents: Int!*  
*invalidClicks: Int!*  
*creditsCents: Int!*  
*}*  
  
*type Query {*  
*myCampaigns: \[Campaign!\]!*  
*campaignStats(campaignId: ID!, from: AWSDate!, to: AWSDate!): \[CampaignStats!\]!*  
*adBalance: Int! \# current prepaid credits*  
*}*  
  
*input CampaignInput {*  
*targetEntityId: ID!*  
*surface: String!*  
*format: String!*  
*cities: \[String!\]!*  
*cpcCents: Int!*  
*dailyBudgetCents: Int!*  
*totalBudgetCents: Int*  
*keywords: \[String!\]*  
*startDate: AWSDate!*  
*endDate: AWSDate*  
*}*  
  
*type Mutation {*  
*createCampaign(input: CampaignInput!): Campaign!*  
*updateCampaign(campaignId: ID!, input: CampaignInput!): Campaign!*  
*pauseCampaign(campaignId: ID!): Campaign!*  
*resumeCampaign(campaignId: ID!): Campaign!*  
*topUpAdCredits(amountCents: Int!): Boolean!*  
*}*  
  
*\# Admin APIs*  
*type Mutation {*  
*setPromoPolicy(surface: String!, role: String, city: String!, cpcFloorCents: Int!, maxDensityTop20: Int!, maxAboveFold: Int!): Boolean!*  
*suspendCampaign(campaignId: ID!, reason: String!): Boolean!*  
*issuePromoCredit(campaignId: ID!, amountCents: Int!, reason: String!): Boolean!*  
*}*  

**Server guards**

- *createCampaign* validates eligibility, floors (*cpc_cents \>= cpc_floor*), and city allowlists; seeds pacing counters.
- *topUpAdCredits* creates a Stripe PaymentIntent and writes a *topup* ledger entry on success.
