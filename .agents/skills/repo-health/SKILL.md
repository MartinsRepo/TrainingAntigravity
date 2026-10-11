---
name: repo-health
description: Audits repository health, validates git status, executes all unit test suites, verifies coding standards compliance, and outputs a formatted health scorecard. Activate when the user asks for a health check, repository audit, or project status validation.
---

# Repository Health Audit Procedure

When this skill is activated, execute the following standardized audit procedure to verify repository integrity and generate a Health Scorecard.

---

## Step 1: Git Repository & Working Tree Audit
1. Run `git status` to check for uncommitted changes, staged files, or untracked artifacts.
2. Run `git log -n 5 --oneline` to review the latest commit history.
3. Verify that temporary files (`*.lock`, `*.tmp`, `__pycache__`) are properly excluded by `.gitignore`.

---

## Step 2: Automated Test Suite Execution
Discover and execute all test suites across the repository using `unittest`:
```bash
python3 -m unittest discover -s modules/02-prompting-and-control/lab/task_cli/tests -v
python3 -m unittest modules/03-custom-rules/lab/test_text_utils.py -v
```
Record:
* Total number of tests executed.
* Number of passing tests vs. failures/errors.
* Execution duration.

---

## Step 3: Rule & Standards Conformance Check
Verify compliance with `.agents/rules/standards.md`:
* **Type Annotations**: Verify that newly authored modules include explicit type annotations.
* **Docstrings**: Verify that public functions include Google-style docstrings (`Args:`, `Returns:`, `Raises:`).
* **Test Accompanying**: Confirm that every business logic/utility module has a corresponding test file.

---

## Step 4: Generate Health Scorecard Report
Format and deliver a markdown scorecard to the user:

```markdown
### 🏥 Repository Health Scorecard

| Check Category | Component | Status | Details |
| :--- | :--- | :---: | :--- |
| **Git Tree** | Working directory | 🟢 / 🟡 | Clean tree / X uncommitted files |
| **Test Suites** | Task Manager CLI | 🟢 / 🔴 | 8/8 tests passed |
| **Test Suites** | Text Utilities | 🟢 / 🔴 | 11/11 tests passed |
| **Standards** | Type hints & Docstrings | 🟢 / 🔴 | 100% compliant |
| **Rules Config** | .agents/rules/standards.md | 🟢 / 🔴 | Present and active |

**Overall Health:** 🟢 EXCELLENT (All checks passing)
```
