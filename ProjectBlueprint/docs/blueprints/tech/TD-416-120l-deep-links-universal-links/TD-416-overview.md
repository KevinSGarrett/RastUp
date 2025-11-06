---
id: TD-416
title: "**1.20.L Deep links & universal links**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-416-120l-deep-links-universal-links\TD-416-overview.md"
parent_id: 
anchor: "TD-416"
checksum: "sha256:2ccaacb445193c2d588256bceb9c5b3f12ac55da6320e0fdc4864fc357d5ce15"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-416"></a>
## **1.20.L Deep links & universal links**

- **iOS** *apple‑app‑site‑association* and **Android** Asset Links hosted under */.well-known/*.
- Universal link handling maps to Profile/Studio/Checkout/Message screens; unknown routes open in in‑app webview.

**Recommended path:** *web/public/.well-known/apple-app-site-association*

*{"applinks":{"apps":\[\],"details":\[{"appID":"TEAMID.com.rastup.app","paths":\["/p/\*","/s/\*","/checkout/\*","/messages\*"\]}\]}}*
