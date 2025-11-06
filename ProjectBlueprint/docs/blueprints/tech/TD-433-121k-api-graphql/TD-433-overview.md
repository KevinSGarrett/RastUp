---
id: TD-433
title: "**1.21.K API (GraphQL)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-433-121k-api-graphql\TD-433-overview.md"
parent_id: 
anchor: "TD-433"
checksum: "sha256:ed1ffecdfbc7a403cc483935c9f141dcfc87e05b5095602125a7b9d6f3e46bfd"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-433"></a>
## **1.21.K API (GraphQL)**

**Recommended path:** *api/schema/search.graphql*

*type SearchResult {*  
*id: ID!*  
*kind: String!*  
*score: Float!*  
*distanceKm: Float*  
*priceFromCents: Int*  
*priceToCents: Int*  
*city: String!*  
*displayName: String*  
*name: String*  
*verified: Boolean!*  
*trusted: Boolean*  
*preview: AWSJSON*  
*}*  
  
*type SearchPage { items: \[SearchResult!\]!, total: Int!, nextCursor: String }*  
  
*input SearchFilter {*  
*scope: String!, city: String!,*  
*any: AWSJSON, all: AWSJSON,*  
*safeMode: Boolean = true,*  
*originLat: Float, originLon: Float,*  
*sort: String = "best", pageSize: Int = 24, cursor: String*  
*}*  
  
*type Query {*  
*search(input: SearchFilter!): SearchPage!*  
*autocomplete(q: String!, scope: String!, city: String!): \[String!\]!*  
*}*
