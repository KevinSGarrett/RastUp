---
id: TD-28
title: "**1.3.I GraphQL API (checkout & lifecycle) — key operations**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-28-13i-graphql-api-checkout-lifecycle-key-operations\TD-28-overview.md"
parent_id: 
anchor: "TD-28"
checksum: "sha256:b76748fd3d2df40158b33c5432d312b6c8b680b901661055bde63cd2882a30d9"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-28"></a>
## **1.3.I GraphQL API (checkout & lifecycle) — key operations**

*type Mutation { startCheckout(leg: StartLegInput!, when: DateTimeRange!, city: String!): CheckoutDraft! attachStudioInFlow(draftId: ID!, studioId: ID!): CheckoutDraft! \# validates time/conflicts createDocPack(draftId: ID!): DocPack! \# returns envelope links markDocSigned(draftId: ID!, packId: ID!, envelopeId: ID!): DocPack! \# Payment createPaymentIntent(draftId: ID!, method: PaymentMethodInput!): PaymentIntentClientSecret! confirmPayment(draftId: ID!): CheckoutConfirmation! \# triggers atomic confirm \# Amendments addChangeOrder(lbgId: ID!, legId: ID!, change: ChangeOrderInput!): Amendment! addOvertime(lbgId: ID!, legId: ID!, minutes: Int!): Amendment! \# Post-session markCompleted(lbgId: ID!): CompletionReceipt! \# or auto after acceptance window fileDepositClaim(legId: ID!, amountCents: Int!, reason: String!): DepositClaimResult!} type Subscription { checkoutStatus(lbgId: ID!): CheckoutEvent!}*

**Guards**

- *attachStudioInFlow* checks studio availability, deposit policy, and buyer acceptance of additional terms.
- *createDocPack* enforces pack content per leg type and role; blocks payment steps until **both** legs have signed docs recorded.
- *confirmPayment* fails atomically if **any** leg fails validation or funding.
