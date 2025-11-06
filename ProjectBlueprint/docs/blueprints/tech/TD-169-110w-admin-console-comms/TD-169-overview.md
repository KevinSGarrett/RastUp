---
id: TD-169
title: "**1.10.W Admin console (Comms)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-169-110w-admin-console-comms\TD-169-overview.md"
parent_id: 
anchor: "TD-169"
checksum: "sha256:c617581627a22b04c178b9e10ab97e0d966a45bbef60cc7dd368a67aa2bb2399"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-169"></a>
## **1.10.W Admin console (Comms)**

- **Template Manager**: search, diff, preview (with sample variables), MJML validation, multi‑locale versions, **dual approval** for security/legal templates; staged rollout with kill‑switch.
- **Test send**: to whitelisted addresses only; record as *status='sent'* with *cause_event='admin.test'*.
- **Suppression Viewer**: search by hashed email/phone; show reasons; **re‑permission** only on explicit user opt‑in.
- **Campaigns/Digests**: configure digest cadence, review experiment assignments; simulate send volumes with cost estimates.
- **Audit log**: all admin actions immutable with actor, reason, diffs.
