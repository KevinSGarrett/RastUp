---
id: TD-19
title: "**1.2.S Acceptance criteria (mark §1.2 FINAL only when ALL are true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-19-12s-acceptance-criteria-mark-12-final-only-when-all-are-true\TD-19-overview.md"
parent_id: 
anchor: "TD-19"
checksum: "sha256:27c0a4d5a73325c2f968ba25a051d447968b4cd852ca69daab565f81e0b94c48"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-19"></a>
## **1.2.S Acceptance criteria (mark §1.2 FINAL only when ALL are true)**

152. **Correctness**: Role‑true discovery and studio separation verified; safe‑mode & age‑gate enforced; city gate honored.
153. **Filters**: All global and role‑specific filters work; social metrics shown only when verified.
154. **Ranking**: Diversity caps & new‑seller floor active; verify boosts and price fit working.
155. **Promotions** (if flag on): featured/boost slots respect density caps; no filter bypass; invalid clicks removed from billing.
156. **Performance**: p95 within SLO; cache hit rate ≥60% under synthetic load.
157. **Resilience**: Indexer DLQ empty after backfill; backfill parity within ±1% of DB records.
158. **Telemetry**: Events emitted; dashboards show CTR, filter usage, fairness metrics, index lag.
159. **Cost**: Engine within budget; cache prevents \>40% of engine calls; alarms quiet for 48h.

# 

# 

# **§1.3 — Booking & Checkout (Linked Booking Group, Escrow, Deposits, Docs‑Before‑Pay, Tax, Refunds, Disputes)**

**Purpose.** Specify the end‑to‑end technical design and guarantees for creating, validating, paying for, amending, and settling bookings—both single‑leg and **Linked Booking Groups (LBG)** where a *Talent leg* and a *Studio leg* are confirmed together but keep independent policies, receipts, and payouts. This section includes domain models, state machines, APIs, ledgers, taxes, deposits, refunds, disputes, attach‑in‑flow studios, admin tools, telemetry, SLOs, and a full test plan. We will stay in §1.3 until it is complete to your 99.9% bar.
