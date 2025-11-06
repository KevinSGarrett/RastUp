---
id: TD-159
title: "**1.10.F Preferences & quiet hours (user‑facing)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-159-110f-preferences-quiet-hours-userfacing\TD-159-overview.md"
parent_id: 
anchor: "TD-159"
checksum: "sha256:75994fc93fc6541b48d0183e8728c35528ac662903d212e0eca5f2ee75dd5096"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-159"></a>
## **1.10.F Preferences & quiet hours (user‑facing)**

**Categories (initial)**

- *security* (critical), *legal* (critical), *booking*, *messages*, *reviews*, *promotions* (marketing), *finance* (receipts/statements).

**Defaults**

- Email: opt‑in for all except *promotions* (opt‑out default ON).
- Push: opt‑in for *booking*, *messages*, *reviews* only after device grants permission.
- SMS: **opt‑out by default**; explicit opt‑in per category where used (*booking* status or *security*).
- In‑app: always on; controlled by red dot/unread.

**Quiet hours**

- Store *tz*, *start_local*, *end_local*.
- Router schedules non‑critical notifications inside allowed windows (e.g., 8 am–9 pm local).
- Per‑category overrides (e.g., allow *booking* during quiet hours).

**GraphQL API (user settings)**

*type CommsPreference {*  
*channel: String!*  
*categoryKey: String!*  
*optedIn: Boolean!*  
*updatedAt: AWSDateTime!*  
*}*  
  
*type QuietHours { tz: String!, startLocal: String!, endLocal: String! }*  
  
*type Query {*  
*commsPreferences: \[CommsPreference!\]!*  
*quietHours: QuietHours*  
*}*  
  
*type Mutation {*  
*setCommsPreference(channel: String!, categoryKey: String!, optedIn: Boolean!): \[CommsPreference!\]!*  
*setQuietHours(tz: String!, startLocal: String!, endLocal: String!): QuietHours!*  
*unsubscribeAllEmail(): Boolean! \# sets all email categories to optedIn=false except critical*  
*}*  

**List‑Unsubscribe**

- Email headers include *List-Unsubscribe* mailto + HTTPS link to a **one‑click** suppression endpoint (sets *comms_pref* to opted‑out for marketing categories and records *comms_suppression* if required by provider).
