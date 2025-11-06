---
id: TD-310
title: "**1.16‑E. Lambda handler skeleton — Saved Search Alerts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-310-116e-lambda-handler-skeleton-saved-search-alerts\TD-310-overview.md"
parent_id: 
anchor: "TD-310"
checksum: "sha256:ba5f443f464888cd7ff091585d983b2922738a4cc6e179c146fd7ea9c204a57c"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-310"></a>
## **1.16‑E. Lambda handler skeleton — Saved Search Alerts**

**Recommended filename/path:** *apps/functions/growthSavedSearchAlerts.ts*

*// growthSavedSearchAlerts.ts*  
*// Pseudocode: load eligible searches, query index, dedupe (Dynamo), send in-app + email via SES.*  
  
*import { queryPeople, queryStudios } from '../lib/search';*  
*import { getEligibleSavedSearches, markAlertSent } from '../lib/savedSearchRepo';*  
*import { dynamoDedupeHit } from '../lib/dedupe';*  
*import { sendEmail } from '../lib/ses';*  
*import { createInAppDigest } from '../lib/inapp';*  
  
*export const handler = async () =\> {*  
*const searches = await getEligibleSavedSearches();*  
*for (const s of searches) {*  
*const alreadySent = await dynamoDedupeHit(s.searchId);*  
*if (alreadySent) continue;*  
  
*const matches = s.scope === 'people'*  
*? await queryPeople(s.query_json, s.city)*  
*: await queryStudios(s.query_json, s.city);*  
  
*if (matches.length === 0) continue;*  
  
*await createInAppDigest(s.user_id, s.search_id, matches.slice(0, 20));*  
*await sendEmail({*  
*toUserId: s.user_id,*  
*template: 'saved_search_alert',*  
*vars: { city: s.city, count: matches.length, cards: matches.slice(0, 20) }*  
*});*  
  
*await markAlertSent(s.search_id, matches.length);*  
*}*  
*};*
