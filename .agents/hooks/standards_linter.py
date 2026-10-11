"""Lifecycle hook validator: Enforces AST syntax, type hints, and mutable default checks."""

import ast
from pathlib import Path
import sys
from typing import List, Tuple


class StandardsVisitor(ast.NodeVisitor):
    """AST Visitor that validates coding standards on Python function definitions."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.violations: List[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Inspects function definitions for mutable defaults and type annotations.

        Args:
            node: The AST FunctionDef node to inspect.
        """
        # Check 1: Mutable default arguments (e.g. def f(x=[]))
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.violations.append(
                    f"{self.file_path}:{node.lineno} in '{node.name}': "
                    f"Forbidden mutable default argument detected ({type(default).__name__})."
                )

        # Check 2: Missing return type annotation on public functions
        if not node.name.startswith("_") and node.returns is None:
            self.violations.append(
                f"{self.file_path}:{node.lineno} in '{node.name}': "
                f"Missing return type annotation."
            )

        self.generic_visit(node)


def lint_file(file_path: Path) -> List[str]:
    """Parses and audits a single Python source file.

    Args:
        file_path: Path to the Python file to inspect.

    Returns:
        A list of violation description strings.
    """
    if not file_path.suffix == ".py":
        return []

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        return [f"{file_path}:{e.lineno} Syntax Error: {e.msg}"]

    visitor = StandardsVisitor(file_path)
    visitor.visit(tree)
    return visitor.violations


def main() -> int:
    """Entry point for post-tool-execution hook.

    Returns:
        Exit code 0 if all audited files pass, otherwise 1.
    """
    repo_root = Path(__file__).resolve().parent.parent.parent

    target_files: List[Path] = []
    if len(sys.argv) > 1:
        target_files = [Path(p) for p in sys.argv[1:]]
    else:
        # Default: audit all python files in modules/ and .agents/
        for pattern in ["modules/**/*.py", ".agents/**/*.py"]:
            target_files.extend(repo_root.glob(pattern))

    total_violations: List[str] = []
    for py_file in target_files:
        if py_file.is_file():
            violations = lint_file(py_file)
            total_violations.extend(violations)

    print("==================================================")
    print("   🪝  POST-TOOL EXECUTION STANDARDS HOOK         ")
    print("==================================================")
    print(f"Audited {len(target_files)} Python source file(s).")

    if total_violations:
        print(f"✗ Found {len(total_violations)} violation(s):")
        for v in total_violations:
            print(f"  - {v}")
        print("==================================================")
        return 1

    print("✓ All inspected files strictly comply with repository standards.")
    print("==================================================")
    return 0


if __name__ == "__main__":
    sys.exit(main())
