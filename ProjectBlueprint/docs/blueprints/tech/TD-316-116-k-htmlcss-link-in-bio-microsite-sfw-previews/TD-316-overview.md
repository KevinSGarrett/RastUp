---
id: TD-316
title: "**1.16-K. HTML/CSS — Link-in-Bio microsite (SFW previews)**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-316-116-k-htmlcss-link-in-bio-microsite-sfw-previews\TD-316-overview.md"
parent_id: 
anchor: "TD-316"
checksum: "sha256:7546ff388ec9617225f9a91c0e355429059748a5b02800bb7eff92ece4ef3a3b"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-316"></a>
## **1.16-K. HTML/CSS — Link-in-Bio microsite (SFW previews)**

**Recommended filename/path:** *web/linkinbio/template.html*

*\<!doctype html\>*  
*\<html lang="en"\>*  
*\<head\>*  
*\<meta charset="utf-8" /\>*  
*\<meta name="viewport" content="width=device-width, initial-scale=1" /\>*  
*\<title\>{{handle}} — Link-in-Bio\</title\>*  
*\<style\>*  
*:root{ --bg:#0e1116; --card:#151a21; --text:#e7edf5; --muted:#9aa6b2; --brand:#ECC540; }*  
*body{ margin:0; background:var(--bg); color:var(--text); font: 16px/1.5 Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }*  
*.wrap{ max-width:780px; margin:0 auto; padding:28px 16px; }*  
*.profile{ display:flex; gap:16px; align-items:center; }*  
*.avatar{ width:72px; height:72px; border-radius:999px; object-fit:cover; border:2px solid var(--brand); }*  
*.handle{ font-size:20px; font-weight:600; }*  
*.chip{ display:inline-block; background:#212833; border:1px solid \#2a3442; padding:4px 10px; border-radius:999px; font-size:12px; margin-right:6px; }*  
*.grid{ display:grid; gap:12px; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); margin-top:16px; }*  
*.card{ background:var(--card); border:1px solid \#222b36; border-radius:16px; padding:12px; }*  
*.card img{ width:100%; height:160px; object-fit:cover; border-radius:12px; }*  
*.btn{ display:inline-block; background:var(--brand); color:#111; padding:10px 14px; border-radius:12px; font-weight:600; text-decoration:none; }*  
*.muted{ color:var(--muted); font-size:13px; }*  
*\</style\>*  
*\</head\>*  
*\<body\>*  
*\<main class="wrap"\>*  
*\<section class="profile"\>*  
*\<img class="avatar" src="{{avatarUrl}}" alt="{{handle}}" /\>*  
*\<div\>*  
*\<div class="handle"\>@{{handle}}\</div\>*  
*\<div class="muted"\>{{city}}\</div\>*  
*{{#if verified}}\<span class="chip"\>Verified\</span\>{{/if}}*  
*{{#each roles}}\<span class="chip"\>{{this}}\</span\>{{/each}}*  
*\</div\>*  
*\</section\>*  
  
*\<section class="grid"\>*  
*\<!-- Packages --\>*  
*{{#each packages}}*  
*\<div class="card"\>*  
*\<img src="{{this.previewUrl}}" alt="SFW preview for {{this.name}}"\>*  
*\<h4\>{{this.name}}\</h4\>*  
*\<p class="muted"\>{{this.description}}\</p\>*  
*\<a class="btn" href="{{this.checkoutLink}}?utm_source=lib&utm_medium=link&utm_campaign=pkg"\>Book {{this.price}}\</a\>*  
*\</div\>*  
*{{/each}}*  
  
*\<!-- Availability --\>*  
*{{#each availability}}*  
*\<div class="card"\>*  
*\<h4\>Availability: {{this.date}}\</h4\>*  
*\<p class="muted"\>{{this.window}}\</p\>*  
*\<a class="btn" href="{{this.bookLink}}?utm_source=lib&utm_medium=link&utm_campaign=avail"\>Request\</a\>*  
*\</div\>*  
*{{/each}}*  
*\</section\>*  
  
*\<p class="muted" style="margin-top:16px"\>*  
*Previews are SFW. For 18+ material, Safe-Mode must be OFF and age-verified in app.*  
*\</p\>*  
*\</main\>*  
*\</body\>*  
*\</html\>*
