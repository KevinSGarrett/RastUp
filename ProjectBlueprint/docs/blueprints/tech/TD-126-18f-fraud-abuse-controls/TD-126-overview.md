---
id: TD-126
title: "**1.8.F Fraud & abuse controls**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-126-18f-fraud-abuse-controls\TD-126-overview.md"
parent_id: 
anchor: "TD-126"
checksum: "sha256:880dbbd8269e20a077d0056749fdcd1a9cfe764571307de1a2cd1bf0364bcf2b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-126"></a>
## **1.8.F Fraud & abuse controls**

**Heuristics (near-real-time):**

- **Self-review**: author matches seller or same household (IP/device cluster) → block.
- **Ring behavior**: small set of accounts reviewing each other frequently across short intervals.
- **Burst anomalies**: many 5-star or 1-star reviews in a short window relative to baseline.
- **Retaliation pattern**: reciprocal low star after a dispute outcome.
- **Content policy**: toxicity/hate/off-platform coercion detected by classifier → auto-hide and queue for T&S.

**Signals collected:** author age of account, spend history, dispute/refund context, message sentiment trend, IP/UA/device fingerprints, city mismatch.

**Actions:**

- Auto-hide with *status='hidden'*, set *policy_flags.fraud_score*, enqueue moderation; notify author about review under review (no details that reveal heuristics).
- If confirmed, *removed* with reason; if cleared, *restore*.

**Rate limits:**

- Per account: N reviews/day, with backoff.
