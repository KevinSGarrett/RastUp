---
id: TD-280
title: "**1.15.I Automations, macros, and rules**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-280-115i-automations-macros-and-rules\TD-280-overview.md"
parent_id: 
anchor: "TD-280"
checksum: "sha256:356b842ca633691b57242195924fbeea590c7a4df46687cabc32939c4b465eaf"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-280"></a>
## **1.15.I Automations, macros, and rules**

- **Macros** (agent shortcuts):

  - Booking no‑show (buyer): checklist + refund logic + canned message + case close.
  - Duplicate charge: verify Stripe balance txns → auto refund/dismiss.
  - Fan‑Sub PPV unavailable: verify manifest access logs → auto refund if within window.

- **Rules engine**:

  - SLA breaches → escalate severity + notify supervisor.
  - Too many simultaneous severe cases for a seller → **auto payout hold** to limit exposure.
  - Policy keywords/NSFW escalation → T&S queue.
