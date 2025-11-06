---
id: TD-183
title: "**1.11.K GraphQL API (AppSync) — Studio management & browse**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-183-111k-graphql-api-appsync-studio-management-browse\TD-183-overview.md"
parent_id: 
anchor: "TD-183"
checksum: "sha256:f87c093800a2607ce78b1953826b9451c68342427355a57babfb20693ba5f2b2"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-183"></a>
## **1.11.K GraphQL API (AppSync) — Studio management & browse**

*\# Types*  
*type Studio {*  
*studioId: ID!*  
*title: String!*  
*slug: String!*  
*description: String!*  
*city: String! region: String! country: String!*  
*geo: Geo!*  
*capacityPeople: Int!*  
*sizeSqft: Int*  
*amenities: \[String!\]!*  
*verifiedStudio: Boolean!*  
*depositRequired: Boolean!*  
*depositAuthCents: Int!*  
*houseRules: \[String!\]!*  
*insuranceConfirmed: Boolean!*  
*priceFromCents: Int!*  
*ratingAvg: Float!*  
*ratingCount: Int!*  
*media: \[Media!\]!*  
*isPublished: Boolean!*  
*}*  
  
*type StudioRate {*  
*rateId: ID!*  
*kind: String!*  
*name: String!*  
*dow: \[Int!\]!*  
*startLocal: String!*  
*endLocal: String!*  
*slotMinutes: Int*  
*priceCents: Int!*  
*overtimeCentsPer30m: Int!*  
*minBookingMinutes: Int!*  
*maxBookingMinutes: Int*  
*taxInclusive: Boolean!*  
*active: Boolean!*  
*}*  
  
*\# Queries*  
*type Query {*  
*studio(slug: String!): Studio!*  
*myStudios: \[Studio!\]!*  
*studioRates(studioId: ID!): \[StudioRate!\]!*  
*studioAvailability(studioId: ID!, from: AWSDateTime!, to: AWSDateTime!): \[DateTimeRange!\]!*  
*}*  
  
*\# Mutations*  
*input StudioInput {*  
*title: String!, description: String!, city: String!, region: String!, country: String!,*  
*lat: Float!, lon: Float!, address: AddressInput!,*  
*amenities: \[String!\]!, capacityPeople: Int!, sizeSqft: Int,*  
*depositRequired: Boolean!, depositAuthCents: Int!, houseRules: \[String!\]!,*  
*insuranceConfirmed: Boolean!*  
*}*  
  
*type Mutation {*  
*createStudio(input: StudioInput!): Studio!*  
*updateStudio(studioId: ID!, input: StudioInput!): Studio!*  
*publishStudio(studioId: ID!): Studio!*  
*unpublishStudio(studioId: ID!): Studio!*  
  
*addStudioRate(studioId: ID!, rate: StudioRateInput!): StudioRate!*  
*updateStudioRate(rateId: ID!, rate: StudioRateInput!): StudioRate!*  
*deleteStudioRate(rateId: ID!): Boolean!*  
  
*addStudioMedia(studioId: ID!, media: MediaInput!): Media!*  
*reorderStudioMedia(studioId: ID!, order: \[ID!\]!): Boolean!*  
*deleteStudioMedia(mediaId: ID!): Boolean!*  
  
*addStudioBlackout(studioId: ID!, range: DateTimeRange!, reason: String): Boolean!*  
*deleteStudioBlackout(blackoutId: ID!): Boolean!*  
  
*submitStudioVerification(studioId: ID!, docs: \[Upload!\]!): Boolean!*  
*}*  

**Guards & rules**

- Publish gate: required fields, minimum media, house rules present.
- Verification submission requires owner IDV passed (from §1.6).
- Media upload uses signed S3 URLs; scans run async; blocked images don’t appear in public.
