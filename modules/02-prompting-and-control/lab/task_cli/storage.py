"""Safe storage engine for tasks with POSIX file locking."""

import fcntl
import os
from pathlib import Path
import time
from typing import List

try:
    from .models import Task, parse_markdown, serialize_to_markdown
except ImportError:
    from models import Task, parse_markdown, serialize_to_markdown


class TaskError(Exception):
    """Base exception for Task Manager CLI."""
    pass


class TaskNotFoundError(TaskError):
    """Raised when an operation targets a non-existent task ID."""
    def __init__(self, task_id: int):
        super().__init__(f"Task with ID [{task_id}] does not exist.")
        self.task_id = task_id


class StorageLockError(TaskError):
    """Raised when unable to acquire file lock."""
    pass


class FileLock:
    """Context manager for acquiring POSIX file locks via fcntl."""
    def __init__(self, lock_path: Path, timeout: float = 3.0):
        self.lock_path = lock_path
        self.timeout = timeout
        self.fd = None

    def __enter__(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(self.lock_path), os.O_CREAT | os.O_RDWR, 0o666)
        
        start_time = time.time()
        while True:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except (BlockingIOError, IOError):
                if time.time() - start_time >= self.timeout:
                    os.close(self.fd)
                    self.fd = None
                    raise StorageLockError(
                        f"Could not acquire lock on {self.lock_path} within {self.timeout}s."
                    )
                time.sleep(0.05)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd is not None:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
            finally:
                os.close(self.fd)
                self.fd = None


class MarkdownStorage:
    """Handles persistent reading and writing of tasks to a Markdown file."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.lock_path = file_path.with_suffix(file_path.suffix + ".lock")

    def read_tasks(self) -> List[Task]:
        """Read all tasks from Markdown file under lock protection."""
        if not self.file_path.exists():
            return []

        with FileLock(self.lock_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return parse_markdown(content)

    def write_tasks(self, tasks: List[Task]) -> None:
        """Write all tasks to Markdown file under lock protection."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_text = serialize_to_markdown(tasks)

        with FileLock(self.lock_path):
            # Atomic temp write + replace
            temp_path = self.file_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(markdown_text)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, self.file_path)
