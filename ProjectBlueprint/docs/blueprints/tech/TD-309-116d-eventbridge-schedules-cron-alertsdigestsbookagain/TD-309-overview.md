---
id: TD-309
title: "**1.16‑D. EventBridge schedules (cron) — Alerts/Digests/Book‑Again**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-309-116d-eventbridge-schedules-cron-alertsdigestsbookagain\TD-309-overview.md"
parent_id: 
anchor: "TD-309"
checksum: "sha256:8ac433767dcba1950a5e9827c44a4f8a86023eb911f2b0122377b4403e586f05"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-309"></a>
## **1.16‑D. EventBridge schedules (cron) — Alerts/Digests/Book‑Again**

**Recommended filename/path:** *infra/schedules/growth-schedules.yml*

*\# growth-schedules.yml (declarative intent; implemented via CDK/Amplify Gen 2)*  
*schedules:*  
* - name: saved-search-alerts-daily*  
*cron: "cron(5 13 \* \* ? \*)" \# 13:05 UTC daily*  
*targetLambda: growthSavedSearchAlerts*  
* - name: weekly-city-digest*  
*cron: "cron(15 14 ? \* MON \*)" \# Mondays 14:15 UTC*  
*targetLambda: growthWeeklyDigest*  
* - name: book-again-7d*  
*cron: "cron(0 12 \* \* ? \*)"*  
*targetLambda: growthBookAgain7*  
* - name: book-again-30d*  
*cron: "cron(5 12 \* \* ? \*)"*  
*targetLambda: growthBookAgain30*  
* - name: book-again-90d*  
*cron: "cron(10 12 \* \* ? \*)"*  
*targetLambda: growthBookAgain90*
