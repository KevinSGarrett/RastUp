---
id: TD-573
title: "**1.4.6 Action Cards (structured flows inside chat)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-573-146-action-cards-structured-flows-inside-chat\TD-573-overview.md"
parent_id: 
anchor: "TD-573"
checksum: "sha256:1958eef564ff8541979597123d802a8d73225fe0e3f6c429c2921e143091948a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-573"></a>
## **1.4.6 Action Cards (structured flows inside chat)**

All cards are **messages** with a typed *cardType* and *cardPayload*. Cards support **Accept / Decline / Counter** where appropriate and drive order updates (cross‑refs to §1.3/§1.24).

2804. Propose/Reschedule

      392. Payload: *oldStart*, *oldEnd*, *newStart*, *newEnd*, *reason*.
      393. Accept → updates the order/line item; conflicts trigger an error card.
      394. Decline → thread note only.

2805. Extras / Overtime

      395. Payload: *items\[\]* (title, qty, unitCents), *why*.
      396. Accept → creates **adjustment** line items and either charges immediately (if captured) or at payout reconciliation.
      397. Studio overtime can consume **deposit** before new charge (per policy).

2806. Proofs / Approvals

      398. Payload: *gallery\[\]* (s3KeyWeb, thumb, count), *expiresAt*.
      399. Buyer can **Approve** or **Request Changes** (with notes/markers).
      400. On approve, triggers **milestone complete** (for deliverable‑based jobs).

2807. Expense / Receipt

      401. Payload: *receipt{amountCents, image, merchant, date}*
      402. Accept → adds to payouts or new charge (if buyer‑payable).
      403. Good for travel, props, studio cleaning receipts.

2808. Mark Complete / Deliver

      404. Payload: *what* (*time_based* \| *milestone_id*), *notes*.
      405. Starts buyer’s **review window**; on lapse, auto‑release payout.

2809. Dispute

      406. Payload: *reason*, *details*, optional *evidence\[\]*.
      407. Creates **dispute_case** and pauses affected payout; opens Admin case (T&S) with SLA.

2810. Safety Flag / Report

      408. Payload: *reason*, *notes*.
      409. Soft‑blocks thread, restricts new messages pending review; Admin case created.

**Card security**: all server‑validated (no client‑side totals). Card execution writes **immutable audit** entries.
