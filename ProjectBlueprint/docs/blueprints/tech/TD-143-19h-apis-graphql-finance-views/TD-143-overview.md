---
id: TD-143
title: "**1.9.H APIs (GraphQL) — finance views**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-143-19h-apis-graphql-finance-views\TD-143-overview.md"
parent_id: 
anchor: "TD-143"
checksum: "sha256:0e50a8c55f2acb7de5f46859ee1c59ee33865044c96e4218de753013e8ee8f1e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-143"></a>
## **1.9.H APIs (GraphQL) — finance views**

*type ChargeSummary { lbgId: ID!, amountCents: Int!, capturedAt: AWSDateTime!, method: String! }*  
*type PayoutSummary { legId: ID!, amountCents: Int!, status: String!, scheduledFor: AWSDateTime }*  
*type StatementLink { url: AWSURL!, kind: String!, period: String! }*  
  
*type Query {*  
*myCharges(from: AWSDate!, to: AWSDate!): \[ChargeSummary!\]!*  
*myPayouts(from: AWSDate!, to: AWSDate!): \[PayoutSummary!\]!*  
*myStatements(period: String): \[StatementLink!\]! \# '2025-11'*  
*}*  

Server enforces least‑privilege (buyer sees their charges; seller sees their payouts; admins see all).
