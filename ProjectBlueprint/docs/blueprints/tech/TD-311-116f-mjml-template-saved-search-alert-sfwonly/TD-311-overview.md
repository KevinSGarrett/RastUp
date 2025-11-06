---
id: TD-311
title: "**1.16‑F. MJML template — Saved Search Alert (SFW‑only)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-311-116f-mjml-template-saved-search-alert-sfwonly\TD-311-overview.md"
parent_id: 
anchor: "TD-311"
checksum: "sha256:d48e2cb7e6cf39c0a19e32052b8c0bc690c9a20f8c2d86695765228595c92992"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-311"></a>
## **1.16‑F. MJML template — Saved Search Alert (SFW‑only)**

**Recommended filename/path:** *comms/templates/saved_search_alert.mjml*

*\<mjml\>*  
*\<mj-head\>*  
*\<mj-title\>New matches in {{city}}\</mj-title\>*  
*\<mj-attributes\>*  
*\<mj-text font-size="14px" line-height="20px" /\>*  
*\</mj-attributes\>*  
*\</mj-head\>*  
*\<mj-body\>*  
*\<mj-section\>*  
*\<mj-column\>*  
*\<mj-text font-size="18px"\>\<strong\>{{count}}\</strong\> new match{{#plural count}}es{{/plural}} in {{city}}\</mj-text\>*  
*\<mj-text\>We’ve found new profiles that match your saved search. Previews are SFW.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
  
*{{#each cards}}*  
*\<mj-section\>*  
*\<mj-column\>*  
*\<mj-image src="{{this.previewUrl}}" alt="{{this.title}} — SFW preview" /\>*  
*\<mj-text\>\<strong\>{{this.title}}\</strong\>\<br/\>{{this.subtitle}}\</mj-text\>*  
*\<mj-button href="{{this.deepLink}}"\>View profile\</mj-button\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*{{/each}}*  
  
*\<mj-section\>*  
*\<mj-column\>*  
*\<mj-text\>If you’d like to pause alerts for 30 days, \<a href="{{pauseLink}}"\>click here\</a\>.\</mj-text\>*  
*\<mj-text font-size="12px" color="#666"\>No 18+ content is included in this email. To change preferences, visit Settings.\</mj-text\>*  
*\</mj-column\>*  
*\</mj-section\>*  
*\</mj-body\>*  
*\</mjml\>*
