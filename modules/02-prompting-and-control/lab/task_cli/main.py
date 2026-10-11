"""CLI entry point for the Task Manager."""

import argparse
from pathlib import Path
import sys

try:
    from .storage import MarkdownStorage
    from .manager import TaskManager
    from .tui import TaskTUI
except ImportError:
    from storage import MarkdownStorage
    from manager import TaskManager
    from tui import TaskTUI


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Markdown-based Interactive Task Manager CLI with File Locking."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        default=Path("TASKS.md"),
        help="Path to the Markdown tasks file (default: TASKS.md in current directory)",
    )
    args = parser.parse_args()

    storage = MarkdownStorage(args.file.resolve())
    manager = TaskManager(storage)
    tui = TaskTUI(manager)

    try:
        tui.loop()
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
