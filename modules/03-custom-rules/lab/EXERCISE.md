# Module 03 Lab: Authoring Rules & Guardrails

In this lab, you will author custom rules and watch how the agent automatically detects and enforces them without explicit prompting.

---

## 🔬 Lab Exercises

### Exercise 3.1: Create Project Rules (`.agents/rules/standards.md`)
We will create a rule in `.agents/rules/standards.md` that dictates our repository conventions:
1. All Python code must include docstrings and type annotations.
2. All functions must avoid mutable default arguments (`def fn(x=[])`).
3. Whenever a new feature is written, a test must accompany it.

### Exercise 3.2: Verification Challenge
Ask the agent to generate a utility function (e.g. a string sanitizer or JSON parser) without mentioning the rules:
> **Prompt to test in chat:**
> *"Write a utility function in `lab/utils.py` that strips HTML tags and normalizes whitespace."*

**What to observe:**
- The agent automatically includes type hints, Google-style docstrings, and accompanying unit tests because it loaded `.agents/rules/standards.md` from the workspace context.

---

## 💡 Best Practices for Rules

1. **Be specific and actionable:** Say *"Use `Path` from `pathlib` instead of `os.path`"* rather than *"Write clean path code"*.
2. **Don't overload context:** Keep rules focused. Use `trigger: model_decision` for specialized frameworks (e.g. Docker, GraphQL, Kubernetes) that aren't needed in every prompt.
3. **Keep rules in VCS:** Commit rules into `.agents/rules/` so all team members and agents follow the exact same standards.
