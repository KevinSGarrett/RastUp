---
id: TD-405
title: "**1.20.A Canon & invariants**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-405-120a-canon-invariants\TD-405-overview.md"
parent_id: 
anchor: "TD-405"
checksum: "sha256:c242ee647af4f5aa2260a049d8fda7118c7f398b7e4da28ebb3a76477189a87e"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-405"></a>
## **1.20.A Canon & invariants**

2045. **PWA‑first**: one codebase (Next.js) with service worker, install prompt, offline for core routes, and background sync for drafts/uploads.
2046. **Optional native shells** (React Native + Expo) wrap the web for store distribution and system‑level push; both shells and PWA use the same AppSync APIs.
2047. **Safe‑Mode on mobile**: defaults ON for guests/new installs; SFW previews only; 18+ features gated behind age verification and explicit user choice, never emailed or pushed with previews.
2048. **Cost‑conscious:** APNs/FCM via Amazon **Pinpoint/SNS**, no extra third‑party SDK bloat; media uploads are direct‑to‑S3 presigned, resized on device.
2049. **Accessibility**: WCAG mobile patterns, large tap targets, VoiceOver/TalkBack tested, motion‑safe animations.
2050. **Privacy**: no background location; images EXIF stripped on upload (unless user opts in for studio proofs).
