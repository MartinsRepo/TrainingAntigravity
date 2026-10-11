# 📋 Implementation Plan: Python Markdown Task Manager CLI

This plan defines the architectural phases, file structure, test criteria, and deliverables for implementing the task manager CLI derived from our `/grill-me` alignment.

---

## 🎯 Objectives & Constraints

* **Language:** Python 3 (standard library focused: `dataclasses`, `fcntl`, `typing`, `unittest`).
* **Storage:** Markdown format (`TASKS.md`) with `- [ ] [ID] Description`.
* **Concurrency:** POSIX file locking (`fcntl.flock`) to guard against corrupting `TASKS.md` during concurrent writes.
* **Interface:** Interactive terminal menu loop (TUI) with clear feedback signaling.
* **Location:** `TrainingAntigravity/modules/02-prompting-and-control/lab/task_cli/`

---

## 🏗️ Architectural Blueprint & File Layout

```text
modules/02-prompting-and-control/lab/task_cli/
├── __init__.py
├── models.py         # Task dataclass and parsing/formatting logic
├── storage.py        # FileLock context manager and Markdown persistence
├── manager.py        # Business logic (add, toggle, delete, list)
├── tui.py            # Interactive terminal loop & menu interface
├── main.py           # CLI entry point
└── tests/
    ├── __init__.py
    ├── test_storage.py   # Unit tests for parsing and file locking
    └── test_manager.py   # Unit tests for task operations & error handling
```

---

## 🚦 Phased Execution Roadmap

### Phase 1: Models & Markdown Parsing (`models.py`)
- [ ] Define `Task` dataclass (`id: int`, `title: str`, `completed: bool`).
- [ ] Implement `parse_markdown(content: str) -> List[Task]`.
- [ ] Implement `serialize_to_markdown(tasks: List[Task]) -> str`.
- [ ] Support handling manual user edits in `TASKS.md` gracefully without crashing.

### Phase 2: Safe Storage & File Locking (`storage.py`)
- [ ] Implement `FileLock` context manager utilizing `fcntl.flock` (`LOCK_EX` for writing, `LOCK_SH` for reading).
- [ ] Define custom exceptions: `TaskNotFoundError`, `StorageLockError`.
- [ ] Implement atomic write pattern (write to temp file then rename or direct lock flush).

### Phase 3: Core Service & Operations (`manager.py`)
- [ ] Implement `TaskManager` service:
  - `list_tasks() -> List[Task]`
  - `add_task(title: str) -> Task` (assigns monotonic next ID)
  - `toggle_task(task_id: int) -> Task` (raises `TaskNotFoundError` if missing)
  - `delete_task(task_id: int) -> None` (raises `TaskNotFoundError` if missing)

### Phase 4: Interactive TUI Interface (`tui.py`, `main.py`)
- [ ] Create ANSI-styled interactive terminal loop.
- [ ] Menu options: `[1] List Tasks`, `[2] Add Task`, `[3] Toggle Done`, `[4] Delete Task`, `[q] Quit`.
- [ ] Clear status messages (e.g., `✓ Task [1] marked as completed!`, `✗ Error: Task [42] not found`).

### Phase 5: Automated Verification & Unit Tests (`tests/`)
- [ ] Write unit tests for parsing and formatting.
- [ ] Write unit tests for `TaskNotFoundError` signaling.
- [ ] Write concurrency tests verifying file lock integrity.
- [ ] Execute `python3 -m unittest discover` to ensure 100% test pass rate.

### Phase 6: Solution Documentation & Git Commit
- [ ] Run the interactive CLI to verify functionality.
- [ ] Document the `/grill-me` and `/plan` results in `modules/02-prompting-and-control/solution/result.md`.
- [ ] Commit with clean git history.
