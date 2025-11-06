---
id: TD-315
title: "**1.16-J. MJML — “Book Again” (7/30/90 variants)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-315-116-j-mjml-book-again-73090-variants\TD-315-overview.md"
parent_id: 
anchor: "TD-315"
checksum: "sha256:c2dbbf895d1fadcb4837465e0ec9c916871dd18ad4ee0fa340b213b609802f6b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-315"></a>
## **1.16-J. MJML — “Book Again” (7/30/90 variants)**

**Recommended filename/path:** *comms/templates/book_again_7d.mjml* (copy & tweak for *30d*/*90d*)

*\<mjml\>*  
*\<mj-head\>*  
*\<mj-title\>Ready to book {{spName}} again?\</mj-title\>*  
*\<mj-attributes\>*  
*\<mj-text font-size="14px" line-height="20px" /\>*  
*\</mj-attributes\>*  
*\</mj-head\>*  
*\<mj-body\>*  
*\<mj-section padding="16px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="20px" font-weight="600"\>Re-book {{spName}}\</mj-text\>*  
*\<mj-text\>We pre-filled your last package and scope. Pick a date, and you’re done.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*\<mj-section padding="0 24px 12px"\>*  
*\<mj-column\>*  
*\<mj-image src="{{previewUrl}}" alt="{{spName}} — SFW preview" /\>*  
*\<mj-text\>\<strong\>Last package:\</strong\> {{packageName}} — {{packagePrice}}\</mj-text\>*  
*\<mj-button href="{{draftCheckoutLink}}"\>Open draft checkout\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*\<mj-section padding="16px 24px"\>*  
*\<mj-column\>*  
*\<mj-text font-size="12px" color="#667085"\>*  
*To stop these reminders for this provider, \<a href="{{stopLink}}"\>click here\</a\>.*  
*\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*\</mj-body\>*  
*\</mjml\>*
