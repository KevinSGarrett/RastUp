---
id: TD-319
title: "**1.16-N. Lambda Skeleton — Weekly Digest**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-319-116-n-lambda-skeleton-weekly-digest\TD-319-overview.md"
parent_id: 
anchor: "TD-319"
checksum: "sha256:4b3fe88bcc41dd5cd376f31833e566a17cb7a08b011938ba7bd44aa3d9b932f5"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-319"></a>
## **1.16-N. Lambda Skeleton — Weekly Digest**

**Recommended filename/path:** *apps/functions/growthWeeklyDigest.ts*

*// growthWeeklyDigest.ts*  
*import { pickDigestBlocks } from '../lib/digestBlocks';*  
*import { sendEmail } from '../lib/ses';*  
*import { createInApp } from '../lib/inapp';*  
*import { getOptedInUsersByCity } from '../lib/digestRepo';*  
  
*export const handler = async () =\> {*  
*const cities = await getDigestCities();*  
*for (const city of cities) {*  
*const users = await getOptedInUsersByCity(city);*  
*const blocks = await pickDigestBlocks(city); // { caseStudies, studios, rising }*  
*for (const u of users) {*  
*await createInApp(u.userId, 'weekly_digest', { city, blocks });*  
*await sendEmail({*  
*toUserId: u.userId,*  
*template: 'weekly_city_digest',*  
*vars: { city, ...blocks }*  
*});*  
*}*  
*}*  
*};*
