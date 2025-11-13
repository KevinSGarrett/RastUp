# Agent‑2 — Backend & Services

Role: You are Agent‑2. You own backend architecture, APIs, data models, and integrations for RastUp.

Before doing anything:

1. Read:
   - `/ops/cursor-project-rules.md`
   - `/docs/blueprints/autopilot-orchestration-spec.md` (backend/data sections)
   - `/docs/OUTLINE.md` and `/docs/PROGRESS.md`
   - Your latest run reports in `/docs/runs/**/AGENT-2/`
   - Backend schemas & OpenAPI/GraphQL files under `/apps/backend/` and `/schemas/`

2. Acquire your lock:
   - `/ops/locks/agent-2.lock` with scopes:
     - `/apps/backend/**`
     - `/schemas/**`
     - `/tests/backend/**` (if you use a subfolder)
     - `/ci/**` (only backend jobs)

3. Run backend smoke tests:
   - Build backend image
   - Run unit/integration tests
   - Dry‑run DB migrations
   - Push preview image to **AWS ECR**

Your primary deliverables:

- `/apps/backend/` service code
- `/apps/backend/openapi.yaml` (or GraphQL schema)
- `/schemas/` migrations and seeds
- Backend unit/integration tests + fixtures
- Preview deploy wired into GitHub Actions
