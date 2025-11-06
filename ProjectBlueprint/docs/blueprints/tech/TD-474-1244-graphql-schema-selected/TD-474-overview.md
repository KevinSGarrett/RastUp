---
id: TD-474
title: "**1.24.4 GraphQL Schema (selected)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-474-1244-graphql-schema-selected\TD-474-overview.md"
parent_id: 
anchor: "TD-474"
checksum: "sha256:a107612c3cdac2abff2e5336a80e3a9fadfd36e5bc73cf292b225df6d81b8105"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-474"></a>
## **1.24.4 GraphQL Schema (selected)**

*(file: api/schema/spaces.graphql)*

*type Space {*  
*id: ID!*  
*title: String!*  
*neighborhood: String*  
*quickFacts: QuickFacts!*  
*amenities: \[Amenity!\]!*  
*rules: \[Rule!\]!*  
*pricing: Pricing!*  
*availability: \[AvailabilityWindow!\]!*  
*media: \[Media!\]!*  
*reputation: Reputation*  
*host: HostSummary!*  
*locationPreview: LocationPreview! \# approximate map only*  
*reviews(page: Int = 1): \[SpaceReview!\]!*  
*linkedTalent: \[ID!\] \# people profile ids*  
*instantBookEnabled: Boolean!*  
*}*  
  
*type QuickFacts { sizeSqft: Int, ceilingHeightFt: Float, daylightOrientation: String, powerNotes: String }*  
*type Amenity { code: String!, detail: AWSJSON }*  
*type Rule { code: String!, valueBool: Boolean, valueText: String }*  
*type Pricing { currency: String!, pricePerHourCents: Int!, minHours: Int!, cleaningFeeCents: Int, bufferBeforeMin: Int, bufferAfterMin: Int }*  
*type AvailabilityWindow { weekday: Int!, startMinute: Int!, endMinute: Int!, effectiveFrom: AWSDate, effectiveTo: AWSDate, blocked: Boolean! }*  
*type Media { id: ID!, type: String!, url: AWSURL!, thumbUrl: AWSURL! }*  
*type Reputation { score: Float!, volume: Int!, reliability: Float, responsiveness: Float, verification: Float, recency: Float }*  
*type HostSummary { userId: ID!, avatarUrl: AWSURL, responseStats: AWSJSON, otherListings: Int! }*  
*type LocationPreview { latApprox: Float!, lonApprox: Float! }*  
  
*type SpaceReview { id: ID!, authorUserId: ID!, rating: Int!, body: String!, hasPhotos: Boolean!, createdAt: AWSDateTime!, verifiedBooking: Boolean!, ownerReply: String }*  
  
*input SpaceFilter {*  
*city: String, neighborhood: String, priceMin: Int, priceMax: Int, amenityCodes: \[String!\], minCeilingFt: Float*  
*availableOn: AWSDateTime, durationHours: Int*  
*}*  
  
*type Query {*  
*searchSpaces(filter: SpaceFilter!, page: Int = 1): \[Space!\]!*  
*space(id: ID!): Space!*  
*}*  
  
*input SpaceDraftInput { ... } \# wizard fields (title, media, amenities, rules, pricing, availability)*  
*input BookingWidgetInput { spaceId: ID!, start: AWSDateTime!, durationHours: Int!, crewSize: Int!, acceptDocs: Boolean!, requestInstant: Boolean }*  
  
*type Mutation {*  
*createSpaceDraft(input: SpaceDraftInput!): ID! \# returns spaceId*  
*publishSpace(spaceId: ID!): Boolean!*  
*updateSpace(spaceId: ID!, patch: AWSJSON!): Boolean!*  
*setInstantBook(spaceId: ID!, enabled: Boolean!): Boolean!*  
*makeBookingForSpace(input: BookingWidgetInput!): ID! \# returns bookingId; enforces min hours/buffers and deposit hold*  
*leaveSpaceReview(spaceId: ID!, rating: Int!, body: String!, photos: \[ID!\]): Boolean!*  
*ownerReplyToReview(reviewId: ID!, body: String!): Boolean!*  
*}*  

**Notes:**

- *makeBookingForSpace* creates a **space line item** and injects **Property/Space Release + House Rules** into checkout. Deposit hold metadata is included in the payment intent (Stripe auth‑only).

NonTechBlueprint

- Address secrecy: only *LocationPreview* is public; the exact address and door code are revealed in the **booking detail** after confirmation.

NonTechBlueprint
