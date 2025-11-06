---
id: TD-448
title: "**1.22.13 Admin finance console**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-448-12213-admin-finance-console\TD-448-overview.md"
parent_id: 
anchor: "TD-448"
checksum: "sha256:639de9dcab699252df6d7f30c82ea1483a41796e456487fb6aef9e1da3e51673"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-448"></a>
## **1.22.13 Admin finance console**

- Search orders by id/email; view PI/charge; see transfers; issue refunds; apply holds/releases; apply credits; upload dispute evidence.
- **Audit trail** for every action (immutable table; see §1.18.H).
- **Access:** OIDC Admin role only; irreversible actions require two‑step confirmation.

**Artifact — admin GraphQL**  
**Recommended path:** *api/schema/payments.admin.graphql*

*type PaymentAdmin {*  
*orderId: ID!, stripePi: String, amountCents: Int!, currency: String!,*  
*status: String!, providerAccount: String, transfers: \[Transfer!\]!, refunds: \[Refund!\]!*  
*}*  
*type Transfer { xferId: ID!, stripeTransfer: String, amountCents: Int!, status: String! }*  
*type Refund { refundId: ID!, stripeRefund: String, amountCents: Int!, reason: String! }*  
  
*extend type Query {*  
*adminGetOrder(orderId: ID!): PaymentAdmin! @auth(role: "admin")*  
*}*  
*extend type Mutation {*  
*adminRefund(orderId: ID!, amountCents: Int!, reason: String!): Boolean! @auth(role: "admin")*  
*adminHoldPayout(orderId: ID!, reason: String!): Boolean! @auth(role: "admin")*  
*adminReleasePayout(orderId: ID!): Boolean! @auth(role: "admin")*  
*}*
