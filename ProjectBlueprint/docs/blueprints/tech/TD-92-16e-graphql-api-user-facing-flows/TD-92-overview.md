---
id: TD-92
title: "**1.6.E GraphQL API (user-facing flows)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-92-16e-graphql-api-user-facing-flows\TD-92-overview.md"
parent_id: 
anchor: "TD-92"
checksum: "sha256:001d9f0ed25e7e4535b8b7765253a63a62b93b1e34fbba7fb438d3028f0aece1"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-92"></a>
## **1.6.E GraphQL API (user-facing flows)**

*type IdvSession { provider: String!, url: String, clientToken: String }*  
*type BgInvitation { provider: String!, url: String }*  
  
*type TrustStatus {*  
*idVerified: Boolean!*  
*ageVerified: Boolean!*  
*trustedPro: Boolean!*  
*socialVerified: Boolean!*  
*riskScore: Int!*  
*lastIdvAt: AWSDateTime*  
*lastBgAt: AWSDateTime*  
*}*  
  
*type Query {*  
*trustStatus: TrustStatus!*  
*socialConnections: \[SocialConnection!\]!*  
*}*  
  
*type Mutation {*  
*startIdv: IdvSession! \# create new provider session*  
*refreshIdvStatus: TrustStatus! \# polling fallback*  
*startBackgroundCheck: BgInvitation! \# sends FCRA consent flow*  
*disconnectSocial(platform: SocialPlatform!): Boolean!*  
*connectSocial(platform: SocialPlatform!): SocialConnection! \# returns OAuth URL*  
*}*  

**Server rules**

- *startBackgroundCheck* prompts user with **FCRA consents** and a clear explanation; check is optional; badge used as a positive signal only.
- *startIdv* requires logged-in user; if an active IDV *pending*, returns that session to avoid duplicates.
