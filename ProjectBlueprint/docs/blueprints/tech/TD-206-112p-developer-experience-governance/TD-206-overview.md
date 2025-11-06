---
id: TD-206
title: "**1.12.P Developer experience & governance**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-206-112p-developer-experience-governance\TD-206-overview.md"
parent_id: 
anchor: "TD-206"
checksum: "sha256:87538f8393cb8a6321b1f98b496f5e950c7513f452de77aeb1eb511db0f95dd3"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-206"></a>
## **1.12.P Developer experience & governance**

- **Monorepo** with pnpm, turbo, strict TS, ESLint, Prettier.
- **Conventional commits**; PR templates with checklists (security, cost, migrations).
- **CODEOWNERS** for critical paths (finance, trust, infra).
- **Schema/codegen** for GraphQL; shared types for events; golden files for ranking & fee math.
- **ADR** (Architecture Decision Records) in repo for choices like Typesense vs OpenSearch.
