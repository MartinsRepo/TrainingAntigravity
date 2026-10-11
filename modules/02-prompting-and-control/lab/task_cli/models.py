"""Task data models and Markdown parsing/serialization."""

from dataclasses import dataclass
import re
from typing import List, Tuple

# Regex to match Markdown checkboxes with optional integer ID prefix:
# Matches:
# - [ ] [1] Task title
# - [x] [2] Finished task
# - [ ] Unnumbered task
TASK_REGEX = re.compile(
    r"^\s*-\s*\[([ xX])\]\s*(?:\[(\d+)\])?\s*(.*?)\s*$"
)


@dataclass
class Task:
    """Represents a single task item."""
    id: int
    title: str
    completed: bool = False

    def to_markdown_line(self) -> str:
        """Format the task as a Markdown checkbox line."""
        check = "x" if self.completed else " "
        return f"- [{check}] [{self.id}] {self.title}"


def parse_markdown(content: str) -> List[Task]:
    """Parse Markdown content into a list of Task objects.
    
    Extracts all checkbox lines. If an ID is missing, automatically generates
    an ID higher than any existing ID.
    """
    tasks: List[Task] = []
    highest_id = 0
    unassigned_entries: List[Tuple[bool, str]] = []

    for line in content.splitlines():
        match = TASK_REGEX.match(line)
        if match:
            check_char, id_str, title = match.groups()
            is_done = check_char.lower() == "x"
            clean_title = title.strip()
            if not clean_title:
                continue

            if id_str is not None:
                task_id = int(id_str)
                highest_id = max(highest_id, task_id)
                tasks.append(Task(id=task_id, title=clean_title, completed=is_done))
            else:
                unassigned_entries.append((is_done, clean_title))

    # Assign IDs to unnumbered tasks
    for is_done, title in unassigned_entries:
        highest_id += 1
        tasks.append(Task(id=highest_id, title=title, completed=is_done))

    # Keep tasks ordered by ID
    tasks.sort(key=lambda t: t.id)
    return tasks


def serialize_to_markdown(tasks: List[Task], title_header: str = "# Task List\n\n") -> str:
    """Serialize a list of Task objects into a clean Markdown document."""
    lines = [title_header.rstrip()]
    lines.append("")
    if not tasks:
        lines.append("_No tasks currently registered._")
    else:
        for task in sorted(tasks, key=lambda t: t.id):
            lines.append(task.to_markdown_line())
    lines.append("")  # Trailing newline
    return "\n".join(lines)
