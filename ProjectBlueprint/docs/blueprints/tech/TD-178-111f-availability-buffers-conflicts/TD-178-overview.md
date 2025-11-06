---
id: TD-178
title: "**1.11.F Availability, buffers & conflicts**"
source_doc: "TechDevBlueprint.docx"
source_path: "docs\blueprints\tech\TD-178-111f-availability-buffers-conflicts\TD-178-overview.md"
parent_id: 
anchor: "TD-178"
checksum: "sha256:8bda53a59a30e5c32ba4e59dd4cf9bdff421eb9ed351f4b9fd3bcd15f0b04c5d"
last_modified: "2025-11-06T20:40:46Z"
doc_kind: "TD"
h_level: 2
---
<a id="TD-178"></a>
## **1.11.F Availability, buffers & conflicts**

**Authoritative blocks** are **accepted/confirmed** booking legs + **blackouts**. *availability_json* is a hint for search only.

- On **propose/confirm**, we check for **overlaps + buffers** (before/after + cleaning).
- On **amend/reschedule**, re‑check conflict rules; if conflict, fail with *STUDIO_CONFLICT_BUFFER* or *STUDIO_BLACKOUT*.

**Calendar feeds**

- Generate **read‑only ICS** for owners (includes upcoming bookings + buffers), redacted buyer names.
- Optionally import a Google Calendar read‑only feed for soft conflicts (advisory). Hard conflicts are our DB.
