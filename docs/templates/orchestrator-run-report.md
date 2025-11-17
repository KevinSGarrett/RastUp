# Orchestrator Run Report

- **Run ID:** {{ run_id }}
- **Started:** {{ started_at }}
- **Finished:** {{ finished_at }}
- **Environment:** {{ env }}
- **Mode:** {{ mode }} <!-- autopilot | manual -->

## 1. Queue Snapshot

- Total tasks: {{ queue_total }}
- todo: {{ queue_todo_count }}
- doing: {{ queue_doing_count }}
- review: {{ queue_review_count }}
- done: {{ queue_done_count }}

## 2. Agent Activity

{{ agent_activity }}

## 3. Locks & Recovery

{{ locks_and_recovery }}

## 4. Errors / Alerts

{{ errors }}

## 5. Notes

{{ notes }}
