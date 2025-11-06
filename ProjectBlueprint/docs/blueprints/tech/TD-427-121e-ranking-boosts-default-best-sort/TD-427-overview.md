---
id: TD-427
title: "**1.21.E Ranking & boosts (default “best” sort)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-427-121e-ranking-boosts-default-best-sort\TD-427-overview.md"
parent_id: 
anchor: "TD-427"
checksum: "sha256:af37936c510812072269fd283c9ea07ea207211a4598bb7b2e1ec4ec9c92716a"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-427"></a>
## **1.21.E Ranking & boosts (default “best” sort)**

**People**

*score = 0.25\*rep + 0.20\*recency + 0.15\*engagement + 0.15\*availability*  
* + 0.10\*verifiedBoost + 0.05\*trustedBoost + 0.05\*priceFitness*  
* - 0.10\*distancePenalty*  

**Studios**

*score = 0.30\*booking + 0.20\*recency + 0.15\*engagement*  
* + 0.15\*verifiedBoost + 0.10\*amenityFitness*  
* - 0.10\*distancePenalty*  

Signals are normalized to \[0,1\]. Boosts are **bounded** to avoid overwhelming organic signals; tie‑breakers: recency, id.

**Spec:** *search/signals/compute.md* (sigmoid/exp‑decay/gaussian/Jaccard formulas).
