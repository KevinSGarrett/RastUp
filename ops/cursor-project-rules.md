# Cursor Project Rules — RastUp

These rules govern how **all AI agents (Cursor, ChatGPT, Anthropic)** and humans operate in this repo.

They are derived from `/docs/blueprints/autopilot-orchestration-spec.md`.  
When there is a conflict, follow the Autopilot spec and the blueprint documents.

---

## 1. Blueprint‑First & Traceability (HARD)

- Non‑technical blueprint path: **[NON_TECH_BLUEPRINT_PATH]**
- Technical blueprint path: **[TECH_BLUEPRINT_PATH]**
- Autopilot spec: `/docs/blueprints/autopilot-orchestration-spec.md`

Rules:

1. Every change to code, infra, CI, or docs MUST be traceable to:
   - At least one **NT ID** (e.g. `NT-4.1`)
   - At least one **TD ID** (e.g. `TD-3.2`)
   - At least one **WBS task** (e.g. `WBS-4.1`)

2. Commits MUST include trailers in the footer:
   - `NT: NT-x.y`
   - `TD: TD-a.b`
   - `WBS: WBS-p.q`

3. The **blueprint crosswalk** lives at:
   - `/docs/blueprints/nt-index.json`
   - `/docs/blueprints/td-index.json`
   - `/docs/blueprints/crosswalk.json`

4. CI job `/ci/concordance-check.yml` MUST fail if:
   - Changed code paths are missing NT/TD/WBS mappings
   - NT items for the relevant phase are uncovered
   - TD items are not justified by an NT (unless Two‑Key override)

---

## 2. Non‑Interference & Locks (HARD)

- Lock files live under `/ops/locks/agent-<name>.lock`.

Lock file JSON schema:

```json
{
  "task_id": "WBS-<phase>.<task>",
  "owner": "AGENT-<N>",
  "scope_paths": [
    "**/apps/backend/**",
    "**/infra/**"
  ],
  "start_time": "YYYY-MM-DDTHH:MM:SSZ",
  "blueprint_refs": ["NT-x.y", "TD-a.b"]
}
