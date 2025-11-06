---
id: TD-366
title: "**1.18.L Monitoring & detection**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-366-118l-monitoring-detection\TD-366-overview.md"
parent_id: 
anchor: "TD-366"
checksum: "sha256:707ab23cdfec266032a7cedb9275ff99058c1a1039e46b82c5107b48fda68ffc"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-366"></a>
## **1.18.L Monitoring & detection**

- **GuardDuty**: enabled in all accounts; alerts → Security account SNS.

- **Security Hub**: aggregates findings; CIS benchmark checks.

- **Access Analyzer**: detect public/broad‑trust resources.

- **CloudWatch/SNS** alerts:

  - WAF blocks spike, 4xx/5xx spikes, AppSync throttles, Lambda DLQ growth, KMS key errors, Secrets rotation failure.

- **SIEM (lightweight)**: centralize key logs in S3 + Athena queries; optional OpenSearch later.
