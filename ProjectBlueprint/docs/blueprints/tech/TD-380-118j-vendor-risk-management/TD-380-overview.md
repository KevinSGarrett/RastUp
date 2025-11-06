---
id: TD-380
title: "**1.18.J Vendor Risk Management**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-380-118j-vendor-risk-management\TD-380-overview.md"
parent_id: 
anchor: "TD-380"
checksum: "sha256:5e82f8f0438bbcb164202e877b37d5c2939d8248bc2a3e83794e0c481bafa30d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-380"></a>
## **1.18.J Vendor Risk Management**

**Recommended path:** *security/vendors/register.md*

*- Stripe (Processor): DPA, SOC1/2 bridge, data location (US), breach SLA in vendor contract.*  
*- IDV provider: ID docs storage duration & encryption; data deletion API tested quarterly.*  
*- E-sign: signature evidence retention; tamper-evident hashes.*  
*- Email (SES): region & sending limits; bounce/complaint handling verified.*  
*- CDN/DNS: CloudFront/Route53; no third-party DNS at launch.*  
*- Annually review DPAs and security reports; track in vendor register with risk scores.*
