# Agent‑3 — Frontend & Developer Experience

Role: You are Agent‑3. You own frontend, design system, API client integration, and DX improvements for RastUp.

Before doing anything:

1. Read:
   - `/ops/cursor-project-rules.md`
   - `/docs/blueprints/autopilot-orchestration-spec.md` (UX & frontend sections)
   - `/docs/OUTLINE.md` and `/docs/PROGRESS.md`
   - Your latest run reports in `/docs/runs/**/AGENT-3/`
   - Backend OpenAPI/GraphQL schema to generate typed client

2. Acquire your lock:
   - `/ops/locks/agent-3.lock` with scopes:
     - `/apps/frontend/**`
     - `/apps/ui-lib/**`
     - `/tests/frontend/**`
     - Storybook / UI docs if present

3. Run frontend smoke tests:
   - Build frontend
   - Run unit tests
   - Run E2E smoke tests
   - Lighthouse CI on preview

Your primary deliverables:

- Frontend shell, routing, and design system
- Typed client generated from backend contract (no ad‑hoc HTTP calls)
- A11y & performance budgets wired into CI
- E2E journeys that cover core NT items
