---
id: TD-378
title: "**1.18.H Break‑Glass & JIT Admin Access**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-378-118h-breakglass-jit-admin-access\TD-378-overview.md"
parent_id: 
anchor: "TD-378"
checksum: "sha256:696757cf28d7e078621c95ec5fa1a2f94b91fa99fcb4f7d7dd095d1738cedd33"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-378"></a>
## **1.18.H Break‑Glass & JIT Admin Access**

**Recommended path:** *security/admin/break-glass.md*

*- No standing Admin in prod. Use Identity Center JIT with 1-hour session TTL.*  
*- Break-glass triggers:*  
*\* Widespread outage, data corruption, compromised credentials.*  
*- Procedure:*  
* 1) PagerDuty page; open IR ticket.*  
*2) Two-person approval; one requests JIT role; one approves.*  
*3) All actions in console shell are screen-recorded; correlation ID must be attached to commands.*  
*4) Revoke access at TTL; post-mortem includes access diff from CloudTrail.*
