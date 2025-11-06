---
id: TD-167
title: "**1.10.U Experiments & localization**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-167-110u-experiments-localization\TD-167-overview.md"
parent_id: 
anchor: "TD-167"
checksum: "sha256:f0a49e9874aa4b0d0a78793f5af595d670095b89b505bb2c7cbd12f364e88597"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-167"></a>
## **1.10.U Experiments & localization**

**U.1 Experiments**

- **Bucketing**: sticky, per user (UUID‑v4 salted hash).
- Testable assets: email subject/preview text, CTA wording, send‑time (outside quiet hours), digest cadence.
- Metrics: delivery→open→click→conversion, unsubscribe delta; guardrails (bounce/complaint ceilings).
- Rollouts: feature flag controls + staged %; automatic rollback on guardrail breach.

**U.2 Localization**

- Locale resolution order: user setting → browser *Accept-Language* → city default → *en-US*.
- Templates per locale (name/version stable). Fallback to *en-US* when missing.
- Pluralization rules (CLDR), local date/time formatting using recipient’s **timezone** (from quiet hours setting).
- Right‑to‑Left support in MJML (dir attribute), font fallback stacks.
