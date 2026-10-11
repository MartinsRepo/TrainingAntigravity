# Module 05 Lab: Advanced Tools & Automation

In this lab, you will experience how Antigravity manages background processes, timers, and living artifacts.

---

## 🔬 Lab Exercises

### Exercise 5.1: Living Artifact Generation
Ask the agent to generate a rich architecture artifact:
> **Prompt to test in chat:**
> *"Generate a comprehensive architecture artifact for an async event processing pipeline, using a Mermaid sequence diagram, GitHub alert boxes, and a data schema table."*

---

### Exercise 5.2: Background Process Management
Ask the agent to launch a background process (e.g. a simple Python HTTP dev server) and inspect its status:
> **Prompt to test in chat:**
> *"Start a background HTTP server on port 8000 using Python, check its process status with `manage_task`, test it, and then terminate it cleanly."*

---

### Exercise 5.3: Autonomous Scheduling
Ask the agent to set a timer using the scheduler tool:
> **Prompt to test in chat:**
> *"Set a 30-second notification timer to remind us to review the test suite status."*

---

## 💡 Best Practices for Advanced Tools

1. **Clean up background processes:** Always terminate background servers when testing completes.
2. **Never poll in loops:** Rely on Antigravity's Reactive Wakeup rather than writing `while sleep 1;` bash loops.
3. **Use artifacts for architecture:** When discussing system design, ask for artifacts so you retain a durable reference.
