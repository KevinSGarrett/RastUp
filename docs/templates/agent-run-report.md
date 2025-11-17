# Agent Run Report – {{ agent_id }}

- **Run ID:** {{ run_id }}
- **Agent:** {{ agent_id }} – {{ agent_name }}
- **Started:** {{ started_at }}
- **Finished:** {{ finished_at }}
- **Environment:** {{ env }}
- **Tasks handled:** {{ task_ids | join:", " }}
- **Status:** {{ status }}  <!-- success | partial | failed -->

## 1. Objectives

{{ objectives }}

## 2. Actions Taken

{{ actions }}

## 3. Artifacts Produced

{{ artifacts }}

## 4. Notes & Follow-ups

{{ follow_ups }}
