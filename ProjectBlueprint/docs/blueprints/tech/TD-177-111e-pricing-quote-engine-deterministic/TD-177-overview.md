---
id: TD-177
title: "**1.11.E Pricing & quote engine (deterministic)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-177-111e-pricing-quote-engine-deterministic\TD-177-overview.md"
parent_id: 
anchor: "TD-177"
checksum: "sha256:2adb22d93f3a05aba550be28d666ed6f18768e7506d159fcef75d91b5ae64149"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-177"></a>
## **1.11.E Pricing & quote engine (deterministic)**

**Inputs**: date/time, duration, studio_id, rate schedule, buffers/cleaning, deposit policy.  
**Steps**

1075. **Resolve rate** by DOW and local time window:

      145. *Hourly*: within a rate window; price = ceil(duration / 60) \* hourly rate.
      146. *Slot*: duration must equal *slot_minutes*; price = slot price.
      147. *Day*: flat day price.

1076. **Apply minimums/maximums**.

1077. **Compute buffers**: ensure surrounding time is free (*buffer_before_min*, *buffer_after_min*, *cleaning_min*).

1078. **Overtime** (if requested or if stop late): price per 30m bucket from *overtime_cents_per_30m*.

1079. **Taxes**: quote service tax by city via adapter (see §1.3.E).

1080. **Deposit**: show **auth amount** (not part of GMV).

1081. **Total** per leg: *subtotal + service tax + platform fee + fee tax* (platform portions from §1.9).

**Edge cases**

- Split windows (e.g., crossing two hourly windows): either disallow or pro‑rate (MVP: disallow).
- Overlapping slot/day with hourly: pick the best matching schedule deterministically.
