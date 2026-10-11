"""Unit tests for models and safe Markdown storage with file locking."""

from pathlib import Path
import sys
import tempfile
import unittest

# Ensure parent package directory is in sys.path
PACKAGE_DIR = Path(__file__).resolve().parent.parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from models import Task, parse_markdown, serialize_to_markdown
from storage import MarkdownStorage, FileLock, StorageLockError


class TestMarkdownParsing(unittest.TestCase):
    """Test parsing and serialization of Markdown task items."""

    def test_parse_with_and_without_ids(self):
        raw_markdown = """# Project Tasks
- [ ] [1] First existing task
- [x] [2] Completed task
- [ ] Unnumbered task without brackets
- [X] [5] Uppercase completed task
"""
        tasks = parse_markdown(raw_markdown)
        self.assertEqual(len(tasks), 4)

        # Check existing IDs
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "First existing task")
        self.assertFalse(tasks[0].completed)

        self.assertEqual(tasks[1].id, 2)
        self.assertTrue(tasks[1].completed)

        # Check that unnumbered task received ID 6 (highest was 5)
        self.assertEqual(tasks[3].id, 6)
        self.assertEqual(tasks[3].title, "Unnumbered task without brackets")
        self.assertFalse(tasks[3].completed)

    def test_serialization_roundtrip(self):
        tasks = [
            Task(id=1, title="Review PR", completed=False),
            Task(id=2, title="Deploy to prod", completed=True),
        ]
        serialized = serialize_to_markdown(tasks)
        self.assertIn("- [ ] [1] Review PR", serialized)
        self.assertIn("- [x] [2] Deploy to prod", serialized)

        reparsed = parse_markdown(serialized)
        self.assertEqual(len(reparsed), 2)
        self.assertEqual(reparsed[0].title, "Review PR")
        self.assertEqual(reparsed[1].completed, True)


class TestFileLocking(unittest.TestCase):
    """Test POSIX file lock contention."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.lock_file = Path(self.temp_dir.name) / "test.lock"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_lock_exclusivity(self):
        # Acquire lock in first context
        with FileLock(self.lock_file, timeout=0.5):
            # Attempting to acquire lock with short timeout must fail
            with self.assertRaises(StorageLockError):
                with FileLock(self.lock_file, timeout=0.1):
                    pass

    def test_lock_release(self):
        # Verify lock can be re-acquired sequentially
        with FileLock(self.lock_file, timeout=0.5):
            pass

        with FileLock(self.lock_file, timeout=0.5):
            pass  # Successfully acquired after previous release


if __name__ == "__main__":
    unittest.main()
