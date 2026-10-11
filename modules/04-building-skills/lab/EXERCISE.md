# Module 04 Lab: Authoring and Triggering Skills

In this lab, you will author your first Antigravity skill and experience how progressive disclosure triggers specialized runbooks on demand.

---

## 🔬 Lab Exercises

### Exercise 4.1: Create a Skill (`.agents/skills/repo-health/SKILL.md`)
We will create a custom skill named `repo-health`:
- **Name:** `repo-health`
- **Description:** Run a health check on the repository, validating git status, linting, and running unit tests across all modules.
- **Workflow:**
  1. Inspect Git status and report uncommitted changes.
  2. Discover and execute all unit tests.
  3. Verify that all modules conform to repository rules.
  4. Generate a health report.

### Exercise 4.2: Trigger the Skill
Ask the agent:
> *"Run a repository health check on our training project."*

**What to observe:**
- The agent recognizes the task matches the description of `repo-health`.
- It activates the skill, reads `SKILL.md`, and methodically follows the procedure step by step.

---

## 💡 Best Practices for Skills

1. **Specific descriptions:** The agent decides whether to activate a skill based on its YAML `description`. Be clear about the trigger conditions (e.g. *"Use when the user asks to..."*).
2. **Deterministic steps:** Write numbered steps so the agent executes them systematically.
3. **Provide examples or helper scripts:** Place helper scripts in `scripts/` or reference files in `references/` if the skill involves multi-step automation.
