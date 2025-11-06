---
id: TD-111
title: "**1.7.H Budgets, pacing & pausing**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-111-17h-budgets-pacing-pausing\TD-111-overview.md"
parent_id: 
anchor: "TD-111"
checksum: "sha256:ffdbef2d6e9d4d02108bf623808abd361793e199a0313674eb2c2b1b15699f13"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-111"></a>
## **1.7.H Budgets, pacing & pausing**

- **Budgets**: *daily_budget_cents* and optional *total_budget_cents*.

- **Pacing**:

  - *Even*: estimate eligible query volume and drip impressions/clicks over the day; slow or pause when spend exceeds expected pace.
  - *Accelerated*: allow faster delivery while respecting caps and eligibility.

- **Auto‑pause** when: daily budget exhausted, total budget reached, policy violation, or Trust score drops below threshold.

- **Resume rules**: manual or next day reset; spending resumes when budget refills or policy clears.
