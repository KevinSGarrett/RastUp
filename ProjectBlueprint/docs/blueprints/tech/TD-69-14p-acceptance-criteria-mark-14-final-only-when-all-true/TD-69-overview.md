---
id: TD-69
title: "**1.4.P Acceptance criteria (mark §1.4 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-69-14p-acceptance-criteria-mark-14-final-only-when-all-true\TD-69-overview.md"
parent_id: 
anchor: "TD-69"
checksum: "sha256:8201bd14513a99fcfcc883546567742186a9c2b93fb0ff79510bf6fb65cdf787"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-69"></a>
## **1.4.P Acceptance criteria (mark §1.4 FINAL only when ALL true)**

456. Inquiry → Project promotion path live; project thread bound to leg or LBG.
457. Messaging works with presence, read receipts, Safe‑Mode previews, and NSFW scanning.
458. Project Panel tabs (brief, moodboard, shot list, files, docs, expenses, actions) are fully functional; finals handled by external manifests.
459. Action cards trigger §1.3 domain flows correctly and idempotently; states visible and auditable in thread.
460. Moderation, report/block, and anticircumvention nudges operate with audits; policy cannot be bypassed by guests.
461. Notifications (email/push/SMS) are batched, deduped, and respect quiet hours.
462. Telemetry covers lifecycle, panel, actions, moderation, and notifications; dashboards show health & lag \< threshold.
463. p95 performance meets targets; DDB/AppSync/S3 costs within budget alarms for 48h of synthetic load.

# **§1.5 — Smart Docs & E‑Sign CMS**

*(Clause library · variables · pack assembly · e‑signature · PDF hashing · retention · rollbacks · comms templates · admin & audits)*

**Purpose.** Create a versioned, auditable **Smart Docs CMS** that generates legal‑quality documents for bookings and linked booking groups (LBG): SOW (Statement of Work), Model Release(s), and Studio House Rules. These are assembled into **Doc Packs** that must be **fully signed before payment** (Docs‑Before‑Pay), with immutable storage (hashing), retention, re‑issue rules, and end‑to‑end lineage for disputes and finance.

We won’t move to §1.6 until §1.5 meets your 99.9% bar.
