---
id: TD-67
title: "**1.4.N Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-67-14n-test-plan-ci-sandbox\TD-67-overview.md"
parent_id: 
anchor: "TD-67"
checksum: "sha256:42f30e9ca8fdbc8a537f97059fd37de18503f9cad08ccb765056756857868365"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-67"></a>
## **1.4.N Test plan (CI + sandbox)**

**Threads & inbox**

450. Create inquiry; promote to project on checkout success.
451. Inbox lists threads with unread counts; mute suppresses notifications.

**Messages & presence**  
3) Send text + preview; Safe‑Mode blur/blocked behavior verified; read receipts correct.  
4) Presence/typing TTLs work; offline after TTL.

**Project Panel**  
5) Brief edit versioning and merge conflict.  
6) Moodboard pin/ordering & NSFW rules.  
7) Shot list CRUD + completion stats.  
8) Files: preview upload → scanned; finals via manifest; blocked file path.

**Action cards**  
9) Reschedule propose/accept/decline; booking reflects new time.  
10) Request Extra → amendment created & paid (card/ACH flows).  
11) Overtime start/stop → billed and appended to receipts.  
12) Deliverable proofs/finals → approve/revise loop; receipts unaffected unless change orders occur.  
13) Cancel/Refund → policy engine invoked; math aligns with §1.3.  
14) Deposit claim → approval path; partial capture; receipts reflect.  
15) Dispute open → evidence kit seeded; timeline shows deadlines.

**Moderation**  
16) Anticircumvention: first nudge, then soft block on repeat.  
17) Report/Block actions; muted user can’t DM; audit written.

**Notifications**  
18) Dedup window coalesces bursts; quiet hours batching.

**Performance/cost**  
19) p95: open thread ≤ 300 ms (cached) / ≤ 600 ms (cold) at city scale; subscriptions stable.  
20) S3/CF egress stable; DDB RCU/WCU within budget.
