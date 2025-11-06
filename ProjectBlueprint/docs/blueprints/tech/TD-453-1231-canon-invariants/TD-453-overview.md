---
id: TD-453
title: "**1.23.1 Canon & Invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-453-1231-canon-invariants\TD-453-overview.md"
parent_id: 
anchor: "TD-453"
checksum: "sha256:45c825ff47d3a5f1a1772803561ffb0b9c7b380cdf25930607b3e38f886ef60d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-453"></a>
## **1.23.1 Canon & Invariants**

- **Role‑aware, Booking‑aware:** Every thread is anchored to a **Role Context** (service profile) and, when applicable, a **Booking**. This mirrors the non‑tech “Roleaware & Bookingaware” principle.

NonTechBlueprint

- **Single source of truth:** Messages + structured **Project Panel** context (package, schedule, call sheet, contracts, deliverables, extras, payments) co‑exist in the thread.

NonTechBlueprint

- **Structured “Action Cards”:** time proposals/reschedules, add‑ons, overtime, proofs/finals, approvals, expense receipts, mark‑completed, open dispute, share location, safety flag—sent as typed, machine‑readable cards.

NonTechBlueprint

- **Message Requests & Credits:** First‑time contacts land in **Requests**; users can **Accept/Decline/Block**. New conversation **credits** throttle cold outreach; replies and booking‑thread messaging remain unlimited. Contact filters (ID‑verified only, budget disclosed, date provided) are enforced before a message can be sent.

NonTechBlueprint

- **Safety & Policy:** Prominent **Report/Block**, rate limits, spam detection, and PII redaction tools for support are required. Messaging must respect Safe‑Mode on previews and use the policy escalation flows.

NonTechBlueprint_Part3

- **Privacy:** No sensitive EXIF by default on uploads; redactable message copies for legal/dispute workflows.
- **Cost posture:** Serverless realtime (AppSync + DynamoDB + S3 + Lambda) with pay‑per‑use; Typesense (shared) for message search snippets.
