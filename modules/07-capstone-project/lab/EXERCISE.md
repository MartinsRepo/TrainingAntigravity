# Module 07 Lab: The Capstone Project Workflow

This lab guides you through steering the agent through the complete lifecycle of your Capstone Project.

---

## 🔬 Lab Workflow

### Step 1: Pitch the Idea & Trigger `/grill-me`
Select a Capstone project idea (or propose your own) and kick off the alignment interview:
> **Prompt example:**
> *"/grill-me I want to build `doc-guard`, a CLI tool that scans Markdown files for broken links, missing headings, and dead anchors. Interview me to define the scope and architecture."*

---

### Step 2: Request the Phased Plan (`/plan`)
Once requirements are clarified, request the implementation roadmap:
> **Prompt example:**
> *"/plan Create a phased implementation roadmap for `doc-guard` including dataclass models, regex link parser, validator service, CLI, and unittest suite."*

---

### Step 3: Oversee Execution & Test-Driven Verification
Review the generated plan artifact and approve execution. The agent builds the project adhering to our repository rules:
- Strict type hints on every function.
- Google-style docstrings.
- 100% test pass rate with `unittest`.
- Validated by the `.agents/hooks/standards_linter.py` lifecycle hook.

---

### Step 4: Run the Final Repository Audit (`repo-health`)
Execute the final health check across the entire workspace:
> **Prompt:**
> *"Run a repository health check on our training project."*

---

### Step 5: Graduate!
Commit all files and document the solution in `modules/07-capstone-project/solution/result.md`.
