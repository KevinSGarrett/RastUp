---
id: TD-3
title: "**1.2.C Index schema (canonical)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-03-12c-index-schema-canonical\TD-3-overview.md"
parent_id: 
anchor: "TD-3"
checksum: "sha256:6e4dc4ec55fa38b9289e530def361f823b1fa499293140411c09e15aea4d6cc7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-3"></a>
## **1.2.C Index schema (canonical)**

***people_v1*** **(Service Profiles)**

*{ "id": "srv_mdl_01h...", "userId": "usr_01h...", "role": "model \| photographer \| videographer \| creator \| fansub", "handle": "kevin", "slug": "model", // for /u/{handle}/{role} "isPublished": true, "completenessScore": 82, "createdAt": "2025-10-30T19:00:00Z", "updatedAt": "2025-11-05T14:12:00Z", "city": "Houston", "region": "TX", "geo": { "lat": 29.7604, "lon": -95.3698 }, "radiusKm": 80, // willing-to-travel hint "safeModeBandMax": 1, // 0 allow, 1 blur OK, 2 block on public "verification": { "id": true, "bg": false, "socialVerified": true }, "instantBook": true, "ratingAvg": 4.92, "ratingCount": 27, "priceFromCents": 15000, // min package price "priceMedianCents": 25000, // optional "currency": "USD", "availabilityBuckets": \["2025-11-10","2025-11-11","2025-11-14"\], "roleFields": { "model": { "height_cm": 175, "genres": \["fashion","editorial"\] }, "photographer": { "specialties": \["portrait"\], "studio_access": false }, "videographer": { "specialties": \["music"\] }, "creator": { "platforms": \["instagram","tiktok"\] } }, "social": { "igFollowers": 182000, "igEngagementRate": 0.028, "ttFollowers": 530000, "ttAvgViews": 120000 }, "policySignals": { "disputeRate30d": 0.0, "cancelRate90d": 0.02, "lateDeliveryRate90d": 0.01 }, "boosts": { "trustedPro": 0, // +1 if BG passed "newSellerFloor": 1, // protect cold start "studioLinked": 0 // +1 if linked studio (has chip) }}*

***studios_v1*** **(Studio Listings)**

*{ "id": "std_01h...", "ownerUserId": "usr_01h...", "title": "East End Loft", "slug": "east-end-loft", "city": "Houston", "region": "TX", "geo": {"lat": 29.75, "lon": -95.35}, "isPublished": true, "verifiedStudio": true, "amenities": \["natural light","backdrops","makeup area","parking"\], "depositRequired": true, "ratingAvg": 4.85, "ratingCount": 41, "priceFromCents": 3500, // per-hour or base slot price (normalized) "availabilityBuckets": \["2025-11-10","2025-11-12"\]}*
