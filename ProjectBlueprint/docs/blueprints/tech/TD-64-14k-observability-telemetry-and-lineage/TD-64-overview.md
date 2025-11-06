---
id: TD-64
title: "**1.4.K Observability, telemetry, and lineage**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-64-14k-observability-telemetry-and-lineage\TD-64-overview.md"
parent_id: 
anchor: "TD-64"
checksum: "sha256:73ba8f0d0afcd942895f1b80d21b9d202be8503ad988cd40abda2094dfbac833"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-64"></a>
## **1.4.K Observability, telemetry, and lineage**

**Events (immutable):**  
*thread.create*, *thread.promoted_to_project*,  
*message.send*, *message.asset.attach*, *message.blocked*,  
*presence.typing_on/off*, *presence.online/offline*,  
*panel.brief.update*, *panel.moodboard.pin*, *panel.shotlist.update*, *panel.files.add*,  
*action.create*, *action.state_change*,  
*deliverable.proof.posted*, *deliverable.final.posted*, *deliverable.approved*,  
*cancel.requested*, *refund.requested*,  
*deposit.claim.opened\|approved\|denied*,  
*dispute.opened*,  
*notification.sent*,  
*admin.moderation.\**.

**Lineage:** for every action that touches money/docs/booking, emit correlating IDs (*leg_id*, *lbg_id*, *doc_id*, *amendment_id*) so evidence kits can be assembled reliably (§1.3.U).
