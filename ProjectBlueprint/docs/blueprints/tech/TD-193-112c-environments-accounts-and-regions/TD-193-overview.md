---
id: TD-193
title: "**1.12.C Environments, accounts, and regions**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-193-112c-environments-accounts-and-regions\TD-193-overview.md"
parent_id: 
anchor: "TD-193"
checksum: "sha256:91fcbb56d15419d02c0dc5f518e1c1f50ff2a528aed81c9898bd8fd39b52d524"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-193"></a>
## **1.12.C Environments, accounts, and regions**

- **Accounts:** *rastup-dev*, *rastup-stage*, *rastup-prod*.

- **Region:** default **us-east-1** (broadest service coverage, SES deliverability), with room to add read replicas or S3 CRR later.

- DNS:

  - App: *app.dev.rastup.com*, *app.stage.rastup.com*, *app.rastup.com*.
  - Email: *notify.rastup.com* (SES—see §1.10).

- **Secrets & config:** AWS Secrets Manager for secrets; AWS AppConfig for feature flags and city gates.

**Branch mapping (Amplify Hosting):**

- *feature/\** → ephemeral previews (cost-capped; auto‑destroy 48h after last update).
- *main* → **stage**; *release/\** → **prod** via approved promotion.
- *develop* → **dev**.
