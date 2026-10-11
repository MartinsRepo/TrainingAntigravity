"""Helper script to execute automated repository health checks."""

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
from typing import Dict, List, Optional


@dataclass
class TestResult:
    """Stores test execution metrics."""
    suite_name: str
    passed: bool
    details: str


def run_command_safe(command: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    """Executes a subprocess command safely with captured output.

    Args:
        command: List of command arguments to execute.
        cwd: Optional working directory for command execution.

    Returns:
        The CompletedProcess instance containing stdout, stderr, and returncode.

    Raises:
        FileNotFoundError: If the binary is not found in the environment.
    """
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
    )


def check_git_status(repo_root: Path) -> Dict[str, str]:
    """Inspects the git status of the repository.

    Args:
        repo_root: The root path of the repository.

    Returns:
        A dictionary with branch name, status summary, and clean flag ('true'/'false').
    """
    res = run_command_safe(["git", "status", "--porcelain"], cwd=repo_root)
    branch_res = run_command_safe(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root)

    is_clean = len(res.stdout.strip()) == 0
    branch_name = branch_res.stdout.strip() or "unknown"
    return {
        "branch": branch_name,
        "is_clean": "true" if is_clean else "false",
        "details": "Clean working tree" if is_clean else f"{len(res.stdout.splitlines())} modified/untracked files",
    }


def run_test_suite(module_path: str, repo_root: Path) -> TestResult:
    """Executes a unittest command and parses the pass/fail outcome.

    Args:
        module_path: The unittest module or discovery path.
        repo_root: The root path of the repository.

    Returns:
        A TestResult instance describing the outcome.
    """
    cmd = ["python3", "-m", "unittest", module_path]
    res = run_command_safe(cmd, cwd=repo_root)
    passed = res.returncode == 0
    first_line = res.stderr.splitlines()[-1] if res.stderr.splitlines() else "Unknown"
    return TestResult(
        suite_name=module_path,
        passed=passed,
        details=first_line.strip(),
    )


def main() -> int:
    """Main execution entry point for repo health audit.

    Returns:
        Exit code 0 if all checks pass, otherwise 1.
    """
    repo_root = Path(__file__).resolve().parent.parent.parent.parent

    print("==================================================")
    print("   🏥  RUNNING REPOSITORY HEALTH AUDIT            ")
    print("==================================================")

    git_info = check_git_status(repo_root)
    print(f"Git Branch: {git_info['branch']}")
    print(f"Git Status: {git_info['details']}")
    print("--------------------------------------------------")

    test_targets = [
        "modules/02-prompting-and-control/lab/task_cli/tests/test_storage.py",
        "modules/02-prompting-and-control/lab/task_cli/tests/test_manager.py",
        "modules/03-custom-rules/lab/test_text_utils.py",
    ]

    all_tests_passed = True
    for target in test_targets:
        result = run_test_suite(target, repo_root)
        status_symbol = "✓ PASS" if result.passed else "✗ FAIL"
        print(f"[{status_symbol}] {result.suite_name} -> {result.details}")
        if not result.passed:
            all_tests_passed = False

    print("==================================================")
    if all_tests_passed and git_info["is_clean"] == "true":
        print("OVERALL HEALTH: 🟢 EXCELLENT (All checks passing)")
        return 0
    elif all_tests_passed:
        print("OVERALL HEALTH: 🟡 GOOD (Tests pass, uncommitted changes present)")
        return 0
    else:
        print("OVERALL HEALTH: 🔴 ISSUES DETECTED (Tests failing)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
