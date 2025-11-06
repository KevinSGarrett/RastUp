---
id: TD-58
title: "**1.4.E Action cards — contract & state machines (examples)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-58-14e-action-cards-contract-state-machines-examples\TD-58-overview.md"
parent_id: 
anchor: "TD-58"
checksum: "sha256:d0e8824ef159a2db21ba62217e20e2191ba659e77a197c29bffe7513d03a1c5a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-58"></a>
## **1.4.E Action cards — contract & state machines (examples)**

**All actions share:** *actionId*, *type*, *payload{}*, *state*, *version*, *createdBy*, timestamps, and **idempotencyKey**.

- Reschedule

  - *payload*: *{ old: DateRange, proposed: DateRange }*
  - *state*: *PENDING → ACCEPTED\|DECLINED\|EXPIRED*
  - Accept transitions booking (§1.3) to new times if conflict‑free.

- Request Extra / Overtime

  - *payload*: *{ name, priceCents }* or *{ minutes }*
  - *state*: *PENDING → PAID\|DECLINED*
  - On approve → calls **Amendments**; on pay fail → *FAILED* with error code.

- Deliverables

  - Proof/Final cards include *manifestRef* to aura row.
  - Buyer: *APPROVE_DELIVERABLE* → *APPROVED*; or *REQUEST_REVISIONS* → *REVISION_REQUESTED* (optional extra cost via change order).

- Cancel/Refund

  - Calls §1.3 policy engine; returns quoted outcome; Support/Admin can override via console (dual‑approval).

- Deposit claim

  - Studio opens claim with amount + evidence; Support approves/denies; on approve → capture deposit hold.

- Dispute

  - Opens processor dispute row; triggers evidence kit builder; timeline pinned in panel.
