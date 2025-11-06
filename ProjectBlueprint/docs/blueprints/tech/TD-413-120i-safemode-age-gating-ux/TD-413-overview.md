---
id: TD-413
title: "**1.20.I Safe‑Mode & age gating UX**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-413-120i-safemode-age-gating-ux\TD-413-overview.md"
parent_id: 
anchor: "TD-413"
checksum: "sha256:450c36dc2fda0ff90fa58c05f446c9c828925bf3a9f71a3804d6103655e66f5d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-413"></a>
## **1.20.I Safe‑Mode & age gating UX**

- **First‑run:** Safe‑Mode ON; explain what it does; clear toggle path in **Settings**.
- **Age verification** (when required): IDV web flow in secure webview; store only verdict and event id, not raw images (§1.18 data minimization).
- **Surface rules:** No push/email with 18+ previews; PWA and RN show SFW placeholders until Safe‑Mode OFF + verified.
