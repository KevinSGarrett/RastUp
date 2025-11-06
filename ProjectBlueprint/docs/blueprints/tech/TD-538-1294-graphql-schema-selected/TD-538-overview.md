---
id: TD-538
title: "**1.29.4 GraphQL schema (selected)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-538-1294-graphql-schema-selected\TD-538-overview.md"
parent_id: 
anchor: "TD-538"
checksum: "sha256:5cfc31d1f5379fec50255a8fd831ba715efea939aa38ea496767a77b274f76ee"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-538"></a>
## **1.29.4 GraphQL schema (selected)**

*(file: api/schema/portfolio.graphql)*

*type PortfolioItem {*  
*id: ID!, title: String!, slug: String!, ownerUserId: ID!, roleProfileId: ID!,*  
*city: String, shootDate: AWSDate, genres: \[String!\]!,*  
*cover: Media!, media: \[Media!\]!, caseStudy: CaseStudy,*  
*studioUsedId: ID, verifiedBooking: Boolean!, sfwBand: Int!, status: String!,*  
*collaborators: \[CollabTag!\]!*  
*}*  
  
*type Media { id: ID!, kind: String!, url: AWSURL!, width: Int, height: Int, durationSec: Int, altText: String }*  
*type CaseStudy { clientType: String, summary: String, deliverables: \[String!\], results: String, budgetLowCents: Int, budgetHighCents: Int }*  
*type CollabTag { userId: ID!, roleCode: String!, status: String!, note: String }*  
  
*type Board { id: ID!, title: String!, visibility: String!, items: \[BoardItem!\]! }*  
*type BoardItem { entityType: String!, entityId: ID!, note: String, ordinal: Int }*  
  
*input PortfolioDraftInput { title: String!, roleProfileId: ID!, city: String, shootDate: AWSDate, genres: \[String!\]! }*  
*input PortfolioPublishInput { id: ID!, caseStudy: AWSJSON, studioUsedId: ID, coverMediaId: ID! }*  
*input CollabRequestInput { itemId: ID!, collaboratorUserId: ID!, roleCode: String!, note: String }*  
*input CollabRespondInput { itemId: ID!, status: String!, note: String }*  
*input BoardCreateInput { title: String!, visibility: String! }*  
*input BoardAddInput { boardId: ID!, entityType: String!, entityId: ID!, note: String }*  
  
*type Query {*  
*portfolioItem(slug: String!): PortfolioItem*  
*profilePortfolio(roleProfileId: ID!, page: Int = 1): \[PortfolioItem!\]!*  
*boards(ownerUserId: ID!): \[Board!\]!*  
*}*  
  
*type Mutation {*  
*createPortfolioDraft(input: PortfolioDraftInput!): ID!*  
*uploadPortfolioMedia(itemId: ID!, mediaKind: String!, fileName: String!): AWSJSON! \# presigned URL*  
*requestCollaboratorTag(input: CollabRequestInput!): Boolean!*  
*respondToCollaboratorTag(input: CollabRespondInput!): Boolean! \# approve/decline*  
*publishPortfolio(input: PortfolioPublishInput!): Boolean!*  
*archivePortfolioItem(id: ID!): Boolean!*  
  
*createBoard(input: BoardCreateInput!): ID!*  
*addToBoard(input: BoardAddInput!): Boolean!*  
*removeFromBoard(boardId: ID!, entityType: String!, entityId: ID!): Boolean!*  
*reorderBoardItem(boardId: ID!, entityType: String!, entityId: ID!, ordinal: Int!): Boolean!*  
  
*dmcaReport(entityType: String!, entityId: ID!, reason: String!, evidence: AWSJSON): ID! \# routes to Admin/T&S*  
*}*
