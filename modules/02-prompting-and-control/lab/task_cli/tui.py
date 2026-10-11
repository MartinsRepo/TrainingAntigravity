"""Interactive Terminal UI (TUI) menu interface."""

import os
import sys
from typing import Optional

try:
    from .manager import TaskManager
    from .storage import TaskError, TaskNotFoundError
except ImportError:
    from manager import TaskManager
    from storage import TaskError, TaskNotFoundError


# ANSI Color codes for clean terminal styling
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
GRAY = "\033[90m"
RESET = "\033[0m"


class TaskTUI:
    """Terminal user interface menu loop."""

    def __init__(self, manager: TaskManager):
        self.manager = manager
        self.status_message: Optional[str] = None
        self.is_error: bool = False

    def set_status(self, message: str, is_error: bool = False) -> None:
        self.status_message = message
        self.is_error = is_error

    def print_header(self) -> None:
        print(f"\n{BOLD}{CYAN}=================================================={RESET}")
        print(f"{BOLD}{CYAN}   📋  MARKDOWN TASK MANAGER (Antigravity Lab)    {RESET}")
        print(f"{BOLD}{CYAN}=================================================={RESET}")
        if self.status_message:
            color = RED if self.is_error else GREEN
            symbol = "✗" if self.is_error else "✓"
            print(f"{color}{BOLD} {symbol} {self.status_message}{RESET}")
            print(f"{GRAY}--------------------------------------------------{RESET}")
            self.status_message = None
            self.is_error = False

    def display_tasks(self) -> None:
        tasks = self.manager.list_tasks()
        if not tasks:
            print(f"{GRAY}  (No tasks found. Select [1] to add your first task){RESET}\n")
            return

        for t in tasks:
            if t.completed:
                check = f"{GREEN}[x]{RESET}"
                title = f"{GRAY}\033[9m{t.title}\033[29m{RESET}"
            else:
                check = f"{YELLOW}[ ]{RESET}"
                title = f"{BOLD}{t.title}{RESET}"
            print(f"  {check} {BOLD}[{t.id:02d}]{RESET} {title}")
        print()

    def print_menu(self) -> None:
        print(f"{BOLD}Actions:{RESET}")
        print(f"  {CYAN}[1]{RESET} Add Task")
        print(f"  {CYAN}[2]{RESET} Toggle Done / Undone")
        print(f"  {CYAN}[3]{RESET} Delete Task")
        print(f"  {CYAN}[4]{RESET} Clear Completed Tasks")
        print(f"  {CYAN}[q]{RESET} Quit")

    def run_add(self) -> None:
        try:
            title = input(f"{BOLD}Enter task description: {RESET}").strip()
            if title:
                task = self.manager.add_task(title)
                self.set_status(f"Added task [{task.id}]: '{task.title}'")
            else:
                self.set_status("Task description cannot be empty.", is_error=True)
        except Exception as e:
            self.set_status(str(e), is_error=True)

    def run_toggle(self) -> None:
        try:
            id_str = input(f"{BOLD}Enter task ID to toggle: {RESET}").strip()
            task_id = int(id_str)
            task = self.manager.toggle_task(task_id)
            state = "completed" if task.completed else "active"
            self.set_status(f"Task [{task.id}] marked as {state}.")
        except ValueError:
            self.set_status("Invalid input: Please enter a numeric ID.", is_error=True)
        except TaskNotFoundError as e:
            self.set_status(str(e), is_error=True)
        except TaskError as e:
            self.set_status(str(e), is_error=True)

    def run_delete(self) -> None:
        try:
            id_str = input(f"{BOLD}Enter task ID to delete: {RESET}").strip()
            task_id = int(id_str)
            self.manager.delete_task(task_id)
            self.set_status(f"Task [{task_id}] permanently deleted.")
        except ValueError:
            self.set_status("Invalid input: Please enter a numeric ID.", is_error=True)
        except TaskNotFoundError as e:
            self.set_status(str(e), is_error=True)
        except TaskError as e:
            self.set_status(str(e), is_error=True)

    def run_clear_completed(self) -> None:
        try:
            removed = self.manager.clear_completed()
            self.set_status(f"Removed {removed} completed task(s).")
        except TaskError as e:
            self.set_status(str(e), is_error=True)

    def loop(self) -> None:
        """Main interaction loop."""
        while True:
            self.print_header()
            self.display_tasks()
            self.print_menu()
            try:
                choice = input(f"\n{BOLD}Select option: {RESET}").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{CYAN}Goodbye!{RESET}")
                break

            if choice in ("q", "quit", "exit"):
                print(f"{CYAN}Goodbye!{RESET}")
                break
            elif choice == "1":
                self.run_add()
            elif choice == "2":
                self.run_toggle()
            elif choice == "3":
                self.run_delete()
            elif choice == "4":
                self.run_clear_completed()
            else:
                self.set_status("Invalid option. Choose 1, 2, 3, 4 or q.", is_error=True)
