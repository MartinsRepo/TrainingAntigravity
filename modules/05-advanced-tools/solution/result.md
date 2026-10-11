# Module 05: Lab Results & Output Documentation

This document records the exercises executed during **Module 05: Advanced Tools & Automation**, demonstrating persistent living artifacts, background task lifecycle management, and clean process control.

---

## 📌 Exercise 5.1: Living Architecture Artifact

### Generated Artifact
* **Artifact Path:** `event_pipeline_architecture.md`
* **Artifact URL:** [event_pipeline_architecture.md](file:///home/martin/.gemini/antigravity-ide/brain/d9c20d7c-6f4c-4ef3-84e3-dfa112c1d209/event_pipeline_architecture.md)

### Artifact Highlights
* **Mermaid Sequence Diagram:** Modeled asynchronous pub/sub event pipeline from HTTP API Gateway through Redis queue to background worker daemons and telemetry monitors.
* **Mermaid State Machine:** Modeled the lifecycle states of an event (`Ingested` -> `Queued` -> `Processing` -> `Succeeded` / `DeadLetter`).
* **GitHub Callout Alerts:** Incorporated `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, and `[!WARNING]` blocks defining idempotency guarantees, exponential backoff with jitter, and graceful `SIGTERM` shutdown policies.

---

## 📌 Exercise 5.2: Background Process Management

### 1. Created Mock Service: `server.py`
* Endpoints:
  * `GET /health` -> Returns `{"status": "healthy", "service": "event-pipeline-mock", "uptime_seconds": ...}`
  * `GET /metrics` -> Returns `{"events_processed": 128, "active_workers": 4, "error_rate": 0.0}`

### 2. Background Task Launch
Executed:
```bash
python3 modules/05-advanced-tools/lab/server.py 8888 (IsDaemon=true)
```
Output:
```text
Tool is running as a background task with task id: d9c20d7c-6f4c-4ef3-84e3-dfa112c1d209/task-267
```

### 3. Inspection via `manage_task`
Action `list` output:
```json
{
  "taskId": "d9c20d7c-6f4c-4ef3-84e3-dfa112c1d209/task-267",
  "toolName": "run_command",
  "description": "python3 modules/05-advanced-tools/lab/server.py 8888",
  "isDaemon": true
}
```

### 4. HTTP Endpoint Verification
Executed:
```bash
curl -s http://127.0.0.1:8888/health && curl -s http://127.0.0.1:8888/metrics
```
Output:
```json
{"status": "healthy", "service": "event-pipeline-mock", "uptime_seconds": 11.32}
{"events_processed": 128, "active_workers": 4, "error_rate": 0.0}
```

### 5. Clean Process Termination
Action `kill` on `task-267`:
```text
Task "d9c20d7c-6f4c-4ef3-84e3-dfa112c1d209/task-267" cancelled.
Verification: "No background tasks are currently running."
```

### 6. Automated Unit Tests (`test_server.py`)
```text
test_health_endpoint ... ok
test_metrics_endpoint ... ok
test_not_found ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.104s — OK (100% Pass Rate)
```

---

## 🧠 Key Takeaways from Module 05

1. **Non-Blocking Execution:** Background tasks allow the agent to start servers, watchers, or compilers without stalling the conversation.
2. **Deterministic Lifecycle:** `manage_task` provides complete control over long-running processes (status checks, input streaming, and guaranteed cleanup).
3. **Living Artifacts Persist:** Diagrams and structural specifications live in dedicated IDE panes rather than vanishing in ephemeral chat history.
