---
id: TD-580
title: "**1.4.13 Acceptance criteria (Part 1)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-580-1413-acceptance-criteria-part-1\TD-580-overview.md"
parent_id: 
anchor: "TD-580"
checksum: "sha256:b3aacf609492138d74316817fa839c552b6eedb5dce16a469f28ec80fe5373c0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-580"></a>
## **1.4.13 Acceptance criteria (Part 1)**

- Message Requests fully gate new contacts with **Accept/Decline/Block** and rate limits.
- Core Action Cards function and update bookings; audit trails present.
- Inbox folders and search behave per spec; notifications and digests render correctly; ICS attaches to confirmations.
- Safety (block/report, Safe‑Mode previews, nudges) enforced; costs & lifecycles configured.

# **§1.4 — Messaging, Inbox & Collaboration — Full Technical Spec (Parts 2–Final)**

**Blueprint basis.** The non‑technical plan defines the role‑aware, booking‑aware **Unified Inbox**, **Message Requests** gating, structured **Action Cards** (reschedule, extras, proofs/approvals, expense, mark‑complete, dispute, safety flag), folders/filters, search, credits, contact filters, read/delivered receipts, typing indicators, and strong anti‑circumvention + safety posture. The specs below translate that into exact payloads, indexes, templates, thresholds, and testable rules.

NonTechBlueprint
