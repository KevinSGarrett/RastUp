---
id: TD-398
title: "**1.19.10 Emails & notifications localization (MJML)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-398-11910-emails-notifications-localization-mjml\TD-398-overview.md"
parent_id: 
anchor: "TD-398"
checksum: "sha256:53c3d1d431155f693e69fba73857592f1d08058d59fa852d7ecbf7b6b40b4cc6"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-398"></a>
## **1.19.10 Emails & notifications localization (MJML)**

**Template with locale switch**  
**Recommended path:** *comms/templates/\_partials/strings.json*

*{*  
*"en-US": { "cta.viewProfile": "View profile", "digest.header": "This week in {city}" },*  
*"es-ES": { "cta.viewProfile": "Ver perfil", "digest.header": "Esta semana en {city}" }*  
*}*  

**Sender policy:** *From* name localized; subject lines localized; quiet hours per **recipient timezone**.
