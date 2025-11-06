---
id: TD-395
title: "**1.19.7 Accessible components (WCAG 2.2 AA)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-395-1197-accessible-components-wcag-22-aa\TD-395-overview.md"
parent_id: 
anchor: "TD-395"
checksum: "sha256:9a6a6e1ff9eaf2b1d501d9aa6e58f91674f01a454e811a3c4f415bc0f0942d15"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-395"></a>
## **1.19.7 Accessible components (WCAG 2.2 AA)**

**Skip link & landmarks**  
**Recommended path:** *web/components/SkipLink.tsx*

*export const SkipLink = () =\> (*  
*\<a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 bg-yellow-300 p-2 rounded"\>*  
*{t("a11y.skip")}*  
*\</a\>*  
*);*  

**Accessible modal (focus trap, aria)**  
**Recommended path:** *web/components/Modal.tsx*

*export function Modal({ open, titleId, children, onClose }) {*  
*// trap focus, ESC to close, role="dialog" aria-modal="true" aria-labelledby={titleId}*  
*/\* ...focus management code... \*/*  
*}*  

**Combobox (search) ARIA**  
**Recommended path:** *web/components/Combobox.tsx*

*/\* role="combobox" aria-expanded aria-controls listbox; options role="option"; keyboard arrows, Enter, Esc; announces via aria-live \*/*  

**Color/contrast:** enforce ≥ 4.5:1; expose *high_contrast* toggle that upgrades token set.

**Reduced motion:** respect *prefers-reduced-motion* and user pref; disable parallax/animated transitions.
