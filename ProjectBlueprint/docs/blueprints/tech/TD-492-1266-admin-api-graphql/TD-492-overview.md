---
id: TD-492
title: "**1.26.6 Admin API (GraphQL)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-492-1266-admin-api-graphql\TD-492-overview.md"
parent_id: 
anchor: "TD-492"
checksum: "sha256:69b1882861bed96bec65ef52109feee348bee46f813a2691100603c713467457"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-492"></a>
## **1.26.6 Admin API (GraphQL)**

**Recommended path:** *api/schema/admin.graphql*

*enum CaseKind { REPORT DMCA DISPUTE APPEAL FRAUD }*  
*enum CaseStatus { NEW TRIAGE INVESTIGATING AWAITING_USER RESOLVED CLOSED }*  
  
*type AdminCase {*  
*caseId: ID!, kind: CaseKind!, status: CaseStatus!, priority: Int!,*  
*subjectUser: ID, orderId: ID, threadId: ID, listingId: ID,*  
*summary: String!, slaDueAt: AWSDateTime, timeline: \[AdminAction!\]!*  
*}*  
*type AdminAction { actionId: ID!, actorAdmin: ID!, action: String!, payload: AWSJSON, createdAt: AWSDateTime! }*  
  
*type Query {*  
*adminSearchUsers(q: String!, limit: Int = 25): \[AWSJSON!\]! @auth(role: "support")*  
*adminGetCase(caseId: ID!): AdminCase! @auth(role: "trust_safety")*  
*adminListCases(kind: CaseKind, status: CaseStatus, page: Int = 1): \[AdminCase!\]! @auth(role: "trust_safety")*  
*adminRecon(orderId: ID!): AWSJSON! @auth(role: "finance_ops")*  
*}*  
  
*type Mutation {*  
*adminCreateCase(kind: CaseKind!, summary: String!, subjectUser: ID, orderId: ID, threadId: ID, listingId: ID): ID! @auth(role: "trust_safety")*  
*adminAddAction(caseId: ID!, action: String!, payload: AWSJSON): Boolean! @auth(role: "trust_safety")*  
*adminSuspendUser(userId: ID!, reason: String!): Boolean! @auth(role: "trust_safety")*  
*adminReinstateUser(userId: ID!): Boolean! @auth(role: "trust_safety")*  
*adminRefund(orderId: ID!, amountCents: Int!, reason: String!): Boolean! @auth(role: "finance_ops")*  
*adminHoldPayout(orderId: ID!, reason: String!): Boolean! @auth(role: "finance_ops")*  
*adminReleasePayout(orderId: ID!): Boolean! @auth(role: "finance_ops")*  
*adminSearchPin(scope: String!, city: String!, query: String, pinIds: \[ID!\]!, ttlHours: Int): Boolean! @auth(role: "search_curator")*  
*adminSynonymUpsert(id: String!, words: \[String!\]!): Boolean! @auth(role: "search_curator")*  
*adminTemplatePublish(templateId: String!, version: String!, locale: String!): Boolean! @auth(role: "docs_admin")*  
*adminFlagSet(key: String!, value: AWSJSON!): Boolean! @auth(role: "engineering")*  
*}*
