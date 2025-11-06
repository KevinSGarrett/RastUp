---
id: TD-458
title: "**1.23.6 Action Cards (Structured Forms in Chat)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-458-1236-action-cards-structured-forms-in-chat\TD-458-overview.md"
parent_id: 
anchor: "TD-458"
checksum: "sha256:fd7f05b88c9d6f608ca2ddd4108e76e78b6d4418b4a06078ad1c67fedccb383a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-458"></a>
## **1.23.6 Action Cards (Structured Forms in Chat)**

Implements the non‑tech Action Cards list and ensures cards trigger the right domain workflows (booking update, add‑on, dispute, etc.).

NonTechBlueprint

- **ProposeTime/Reschedule:** writes a pending booking change request; recipient can **Accept/Counter/Decline** → updates booking schedule.
- **AddExtras/Overtime:** creates draft **order adjustments** (subtotal delta) and posts a summary; acceptance updates the order and, if needed, collects additional payment (ties to §1.22).
- **UploadProofs/RequestApproval:** uploads to S3 proofs bucket; approval marks deliverables accepted; denial loops with comments.
- **ExpenseReceipt:** attaches expense and moves to project finance view.
- **MarkCompleted:** flips booking state and triggers transfer scheduling (per §1.22).
- **OpenDispute:** creates a **DISPUTE** thread subtype and generates a finance hold.
- **ShareLocation:** ephemeral card visible until *until* timestamp.
- **SafetyFlag:** routes to T&S queue with policy tags.

**Validation:** JSON Schemas per card under *messaging/action-cards/\*.schema.json*.
