---
id: TD-101
title: "**1.6.N Test plan (CI + sandbox)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-101-16n-test-plan-ci-sandbox\TD-101-overview.md"
parent_id: 
anchor: "TD-101"
checksum: "sha256:c691dd7637a938e1fe92b0a1a72b2450bf3feb5114ec7d5627bb3610df871c67"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-101"></a>
## **1.6.N Test plan (CI + sandbox)**

619. **IDV pass** → badge issued, *age_verified=true*, Instant Book enabled; search boost visible.
620. **IDV fail/expired** → badge removed; IB disabled; 18+ surfaces gated.
621. **BG clear** → Trusted Pro badge issued; search boost; promotions eligibility allowed.
622. **BG consider** → no badge; Admin adverse-action flow required; user notified with correct template.
623. **Social verified** → badge appears; snapshot in index; revoke removes badge.
624. **Risk score thresholds** → throttles engage correctly; admin override works with dual approval.
625. **Privacy** → no PII in our storage; access logs for Admin views; legal hold respected.
626. **Webhooks idempotent** → duplicate events do not double-apply.
627. **SLO monitors** → IDV funnel and BG turnaround within targets on synthetic load.
