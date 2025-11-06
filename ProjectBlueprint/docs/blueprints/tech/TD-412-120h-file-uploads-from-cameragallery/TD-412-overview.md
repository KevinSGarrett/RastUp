---
id: TD-412
title: "**1.20.H File uploads from camera/gallery**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-412-120h-file-uploads-from-cameragallery\TD-412-overview.md"
parent_id: 
anchor: "TD-412"
checksum: "sha256:da4d35bde879ca747abbcee1d00a5f8dd32106ffbc7683a227b4e84202dd64a7"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-412"></a>
## **1.20.H File uploads from camera/gallery**

- **Direct‑to‑S3 presigned PUT** (see §1.18.G) with client‑side resize (e.g., target ≤ 2048px longest).
- **EXIF strip** by default; user can opt‑in to keep GPS/time for studio evidence flows.
- **Progress & background**: show %; resume after app pause.
- **Virus/NSFW scan** on ingest (already defined in §1.14 and §1.10).

**Recommended path:** *apps/mobile/upload.ts*

*export async function uploadImage(fileUri: string, mime: string) {*  
*const { url, fields, key } = await gql.mutate('getPresignedUrl', { mime, purpose: 'preview' });*  
*const body = await buildMultipart(fileUri, fields); // RN: fetch blob/file*  
*const res = await fetch(url, { method: 'POST', body });*  
*if (!res.ok) throw new Error('UPLOAD_FAILED');*  
*return { key };*  
*}*
