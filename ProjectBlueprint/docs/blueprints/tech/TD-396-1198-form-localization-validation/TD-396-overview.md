---
id: TD-396
title: "**1.19.8 Form localization & validation**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-396-1198-form-localization-validation\TD-396-overview.md"
parent_id: 
anchor: "TD-396"
checksum: "sha256:9029a5d87d80f64730deedad9af6d86334b3291a8b8603da4f50fc177e56aeb3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-396"></a>
## **1.19.8 Form localization & validation**

- **Names:** do not force first/last in all locales; offer single “full name” with optional structured fields.
- **Addresses:** use country‑specific layouts (state/province, postal code).
- **Phones:** use libphonenumber server‑side and client hints; store E.164 format.
- **Error messages:** localized, short, plain language; associate with fields via *aria-describedby*.
- **Date pickers:** local week start; localized month/day names; keyboard accessible.

**Validation messages catalog**  
**Recommended path:** *i18n/validation/en-US.json*

*{*  
*"required": "This field is required.",*  
*"email": "Enter a valid email address.",*  
*"minLength": "Use at least {min} characters.",*  
*"invalidPhone": "Enter a valid phone number."*  
*}*
