---
id: TD-377
title: "**1.18.G Pre‑Signed Uploads (size/type guard)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-377-118g-presigned-uploads-sizetype-guard\TD-377-overview.md"
parent_id: 
anchor: "TD-377"
checksum: "sha256:558441cd0337a09d5978104fd1eb4976c179f8490d3174de54754ff8eb5a2766"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-377"></a>
## **1.18.G Pre‑Signed Uploads (size/type guard)**

**Recommended path:** *security/s3/presign.ts*

*export function presignPreviewUpload({ userId, mime, bytes }) {*  
*if (!/^image\\(jpe?g\|png\|webp)\$/.test(mime)) throw new Error('UNSUPPORTED_TYPE');*  
*if (bytes \> 10 \* 1024 \* 1024) throw new Error('FILE_TOO_LARGE');*  
*// key scoped to user prefix, random suffix*  
*const key = \`previews/\${userId}/\${Date.now()}\_\${Math.random().toString(36).slice(2)}.webp\`;*  
*return s3.getSignedUrl('putObject', { Bucket: 'fansub-previews', Key: key, ContentType: mime, Expires: 300 });*  
*}*
