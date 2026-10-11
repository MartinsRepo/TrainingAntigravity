"""Unit tests for TaskManager operations and error signaling."""

from pathlib import Path
import sys
import tempfile
import unittest

# Ensure parent package directory is in sys.path
PACKAGE_DIR = Path(__file__).resolve().parent.parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from models import Task
from storage import MarkdownStorage, TaskNotFoundError
from manager import TaskManager


class TestTaskManager(unittest.TestCase):
    """Test task operations, state transitions, and error signaling."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.md_file = Path(self.temp_dir.name) / "TASKS.md"
        self.storage = MarkdownStorage(self.md_file)
        self.manager = TaskManager(self.storage)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_and_list_tasks(self) -> None:
        t1 = self.manager.add_task("First task")
        t2 = self.manager.add_task("Second task")

        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "First task")
        self.assertEqual(tasks[1].title, "Second task")

    def test_toggle_task(self) -> None:
        t1 = self.manager.add_task("Toggle me")
        self.assertFalse(t1.completed)

        t1_updated = self.manager.toggle_task(1)
        self.assertTrue(t1_updated.completed)

        # Toggle back
        t1_reverted = self.manager.toggle_task(1)
        self.assertFalse(t1_reverted.completed)

    def test_task_not_found_error(self) -> None:
        """Verify TaskNotFoundError is raised when target task is missing."""
        self.manager.add_task("Existing task")

        with self.assertRaises(TaskNotFoundError) as ctx:
            self.manager.toggle_task(999)
        self.assertIn("Task with ID [999] does not exist", str(ctx.exception))

        with self.assertRaises(TaskNotFoundError) as ctx:
            self.manager.delete_task(999)
        self.assertIn("Task with ID [999] does not exist", str(ctx.exception))

    def test_delete_and_clear_completed(self) -> None:
        self.manager.add_task("Keep me")
        self.manager.add_task("Complete and remove me")
        self.manager.toggle_task(2)

        removed_count = self.manager.clear_completed()
        self.assertEqual(removed_count, 1)

        remaining = self.manager.list_tasks()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].title, "Keep me")


if __name__ == "__main__":
    unittest.main()
