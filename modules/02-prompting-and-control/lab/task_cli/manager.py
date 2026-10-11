"""Core task management service."""

from typing import List, Optional

try:
    from .models import Task
    from .storage import MarkdownStorage, TaskNotFoundError
except ImportError:
    from models import Task
    from storage import MarkdownStorage, TaskNotFoundError


class TaskManager:
    """Manages high-level CRUD operations on tasks."""

    def __init__(self, storage: MarkdownStorage):
        self.storage = storage

    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return all tasks, optionally filtering completed ones."""
        tasks = self.storage.read_tasks()
        if not include_completed:
            return [t for t in tasks if not t.completed]
        return tasks

    def get_task(self, task_id: int) -> Task:
        """Find a single task by ID or raise TaskNotFoundError."""
        tasks = self.storage.read_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)

    def add_task(self, title: str) -> Task:
        """Add a new task with an automatically incremented ID."""
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")

        tasks = self.storage.read_tasks()
        next_id = max((t.id for t in tasks), default=0) + 1
        new_task = Task(id=next_id, title=title, completed=False)
        tasks.append(new_task)
        self.storage.write_tasks(tasks)
        return new_task

    def toggle_task(self, task_id: int) -> Task:
        """Toggle the completion status of a task by ID."""
        tasks = self.storage.read_tasks()
        target: Optional[Task] = None
        for task in tasks:
            if task.id == task_id:
                task.completed = not task.completed
                target = task
                break

        if target is None:
            raise TaskNotFoundError(task_id)

        self.storage.write_tasks(tasks)
        return target

    def delete_task(self, task_id: int) -> None:
        """Remove a task by ID or raise TaskNotFoundError."""
        tasks = self.storage.read_tasks()
        initial_len = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]

        if len(tasks) == initial_len:
            raise TaskNotFoundError(task_id)

        self.storage.write_tasks(tasks)

    def clear_completed(self) -> int:
        """Delete all completed tasks and return the count removed."""
        tasks = self.storage.read_tasks()
        active = [t for t in tasks if not t.completed]
        removed_count = len(tasks) - len(active)
        if removed_count > 0:
            self.storage.write_tasks(active)
        return removed_count
