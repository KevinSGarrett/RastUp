---
id: TD-199
title: "**1.12.I CI/CD and migrations**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-199-112i-cicd-and-migrations\TD-199-overview.md"
parent_id: 
anchor: "TD-199"
checksum: "sha256:09132df7f0f9d52d57b6173f2eb74a1941cde0f4fcdff082154ad8f1c9a3b5e7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-199"></a>
## **1.12.I CI/CD and migrations**

- **CI (per PR):** typecheck, lint, unit tests, contract tests for GraphQL, build Next.js, synth CDK, **cost‑diff** (cdk‑nag + infracost if configured).

- **DB migrations**: gated step; runs against dev and stage; prod migrations require approval & safe mode (online migrations, lock‑timeout, backfills through batch jobs).

- Deploy:

  - *develop* → dev, auto.
  - *main* → stage, auto with smoke tests.
  - *release/\** → prod, requires approvals; feature flags off by default, enabled progressively.

**Feature flags** via AppConfig: search promotions, LBG, deposits, Fan‑sub, OpenSearch switch, instant payouts, etc.
