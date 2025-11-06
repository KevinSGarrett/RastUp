---
id: TD-417
title: "**1.20.M CI/CD & releases (PWA + RN shells)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-417-120m-cicd-releases-pwa-rn-shells\TD-417-overview.md"
parent_id: 
anchor: "TD-417"
checksum: "sha256:18d2a11ac4ca28a2579c5d6c1a5ee0f12dc2a64582ab85331c00d061022d056f"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-417"></a>
## **1.20.M CI/CD & releases (PWA + RN shells)**

- **PWA**: GitHub Actions build → deploy to Amplify Hosting/CloudFront; invalidation of changed paths; Lighthouse CI budget gate.
- **RN shells** *(optional)*: Expo EAS build & submit; internal test tracks (Play) and TestFlight; codepush‑style OTA (for JS only, not for policy‑sensitive features).
- **Signing & secrets** in GitHub OIDC + Secrets Manager; no long‑lived signing keys in repo (§1.18).
