---
id: TD-190
title: "**1.11.R Acceptance criteria (mark §1.11 FINAL only when ALL true)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-190-111r-acceptance-criteria-mark-111-final-only-when-all-true\TD-190-overview.md"
parent_id: 
anchor: "TD-190"
checksum: "sha256:8ff397bb114fb17d9ecdf8d93160c467088044a50d45979ad66a9b2bbef5e9f0"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-190"></a>
## **1.11.R Acceptance criteria (mark §1.11 FINAL only when ALL true)**

1135. Studio onboarding, publish, and verification operate end‑to‑end with audits.
1136. Quote engine computes hourly/slot/day correctly; buffers/blackouts enforced; taxes and deposit surfaced correctly.
1137. Attach‑in‑flow Studio works with **atomic** LBG confirm; deposit auth is separate and captured only on approved claim.
1138. Search facets (amenities, verified, deposit, capacity, price) function; Safe‑Mode rules hold.
1139. Media pipeline scans/blocks unsafe previews; ordering and thumbnails correct; S3 lifecycle active.
1140. Admin tools (verification, policy editor, taxonomy) function with immutable audits.
1141. Telemetry complete; p95 perf within targets; costs within budget alarms through 48h synthetic run.

# **§1.12 — Platform & Infrastructure (Amplify Gen 2 Foundation, Environments, Security, Cost)**

*(code‑first Amplify, infra topology, CI/CD, auth, data stores, observability, budgets, DR, and developer workflow)*

**Purpose.** Establish a cost‑conscious, elastic, and auditable foundation that can carry us from **build → launch → growth** without re‑platforming. This section guarantees we’re on **Amplify Gen 2 (code‑first/CDK)**—**not** Classic—while wiring AppSync, Cognito, S3/CloudFront, Aurora, DynamoDB, Step Functions, SQS, EventBridge, WAF, and our optional engines (Typesense/OpenSearch). It includes IaC, environments, secrets, runtime limits, budgets, SLOs, admin access controls, and a full test plan.

We will not advance to the next subsection until §1.12 meets your 99.9% bar.
