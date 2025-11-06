---
id: TD-411
title: "**1.20.G Push notifications (APNs/FCM via Pinpoint/SNS)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-411-120g-push-notifications-apnsfcm-via-pinpointsns\TD-411-overview.md"
parent_id: 
anchor: "TD-411"
checksum: "sha256:e8982349b337b06f607462f471538f84cc667e271597062b15142f66ac7d3d77"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-411"></a>
## **1.20.G Push notifications (APNs/FCM via Pinpoint/SNS)**

**Token registration**  
**Recommended path:** *apps/mobile/push/register.ts*

*export async function registerPushToken(userId: string, token: string, platform: 'ios'\|'android'\|'web') {*  
*await gql.mutate('savePushToken', { userId, token, platform, tz: Intl.DateTimeFormat().resolvedOptions().timeZone });*  
*}*  

**Server routing**

- Use Pinpoint/SNS topics per **city** and per **user** for rate‑efficient broadcasts and 1:1 messages.
- **Quiet hours** enforce local‑time windows; **daily caps** per category (alerts/digests vs direct messages).
- Templates mirror §1.16 MJML text (title/body only; no 18+ previews).
