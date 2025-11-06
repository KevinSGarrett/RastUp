---
id: TD-320
title: "**1.16-O. Lambda Skeleton — Book Again (7/30/90)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-320-116-o-lambda-skeleton-book-again-73090\TD-320-overview.md"
parent_id: 
anchor: "TD-320"
checksum: "sha256:b08fdafe5cfa842e69e310b48f8f157c4ba5ff6157ea32542e0c0ba076d043bc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-320"></a>
## **1.16-O. Lambda Skeleton — Book Again (7/30/90)**

**Recommended filename/path:** *apps/functions/growthBookAgain7.ts* (copy for 30/90)

*// growthBookAgain7.ts*  
*import { findEligibleRebooks } from '../lib/rebookRepo';*  
*import { sendEmail } from '../lib/ses';*  
  
*export const handler = async () =\> {*  
*const reb = await findEligibleRebooks({ daysAgo: 7 });*  
*for (const r of reb) {*  
*await sendEmail({*  
*toUserId: r.buyerId,*  
*template: 'book_again_7d',*  
*vars: {*  
*spName: r.spName,*  
*packageName: r.packageName,*  
*packagePrice: r.packagePriceFmt,*  
*previewUrl: r.previewUrl,*  
*draftCheckoutLink: r.draftCheckoutLink,*  
*stopLink: r.stopLink*  
*}*  
*});*  
*}*  
*};*
