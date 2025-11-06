---
id: TD-594
title: "**1.4.N Test plan — additional cases to reach 99.9%**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-594-14n-test-plan-additional-cases-to-reach-999\TD-594-overview.md"
parent_id: 
anchor: "TD-594"
checksum: "sha256:6e4375877240a7ccb0217deb86bc0b227ace1f3cddc4588e0880136b5d9d646e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-594"></a>
## **1.4.N Test plan — additional cases to reach 99.9%**

2895. **Search tokens**: *card:proofs from:@buyer has:file date:2025-11* returns correct thread set.
2896. **Typing presence**: multi‑device typing shows once; TTL expiry clears state.
2897. **Delivery/read receipts**: ✓✓ hollow → ✓✓ filled when recipient opens; last_read_ts advances.
2898. **Email templates**: render variables; ICS attached on confirmed/rescheduled; quiet hours suppress push.
2899. **Digest**: timezone‑aware batching; de‑dup logic; opt‑out honored.
2900. **Anti‑circumvention**: nudge → throttle → soft‑block flow on repeated attempts; thread banner shows reason.

NonTechBlueprint

2901. **Case‑bound Admin**: JIT token allows only case threads; audit shows reads/actions with reason codes.
2902. **Attachment AV**: quarantined file cannot be downloaded; “clean” flips state and link appears.
