---
id: TD-461
title: "**1.23.9 Spam Controls, Rate Limits & Safety**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-461-1239-spam-controls-rate-limits-safety\TD-461-overview.md"
parent_id: 
anchor: "TD-461"
checksum: "sha256:41b148e2ce522a3d518bbe390e2abe69c28c48e1f809c36e9be7c476a356d68e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-461"></a>
## **1.23.9 Spam Controls, Rate Limits & Safety**

- **Rate limits:** per‑user token bucket: new‑conversation starts (credits + per‑hour cap), per‑thread send QPS, attachment size caps; Requests folder protected by stricter per‑sender gates.
- **Spam detection:** rules + lightweight ML: rapid multi‑thread outreach, repeated phrases/links, reputation signals.
- **Report/Block:** one‑tap from thread header; **block** stops delivery both ways; **report** files a T&S case with evidence bundles and policy tags (harassment, doxxing, illegal).

NonTechBlueprint_Part3

- **PII redaction (support‑side tool):** hide phone/email/addresses from public copies when necessary.

NonTechBlueprint_Part3

- **Enforcement:** auto‑muting, temporary holds, escalation to T&S lead for severe harms with legal hand‑off.

NonTechBlueprint_Part3
