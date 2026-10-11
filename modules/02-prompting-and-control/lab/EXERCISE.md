# Module 02 Lab: Mastering Slash Commands & Steering

In this lab, you will experience how slash commands fundamentally alter agent behavior compared to open-ended chatting.

---

## 🔬 Lab Exercises

### Exercise 2.1: The Interactive Interview (`/grill-me`)
When you want to design a feature but want to explore trade-offs first, use `/grill-me`.
> **Prompt to test in chat:**
> *"/grill-me I want to build a simple Markdown-based task management CLI in this repo. Interview me to define the data format, command syntax, and error handling."*

**What to observe:**
- The agent does not immediately spit out code.
- Instead, it asks targeted, probing questions (data persistence, file storage format, CLI flags, conflict resolution).

---

### Exercise 2.2: Phased Planning (`/plan`)
Once requirements are clear, use `/plan` to establish a rock-solid step-by-step roadmap.
> **Prompt to test in chat:**
> *"/plan Create an architectural plan to implement the task manager CLI with TypeScript or Python, including unit tests and documentation."*

**What to observe:**
- The agent breaks the task down into discrete phases (Setup -> Data Model -> Commands -> Tests -> Docs).
- It highlights potential pitfalls and requests your confirmation before touching the filesystem.

---

### Exercise 2.3: Persisting Learned Lessons (`/learn`)
When you find a specific preference or rule you want the agent to remember across conversations, invoke `/learn`.
> **Prompt to test in chat:**
> *"/learn In this repository, always ensure test scripts include verbose output and all CLI tools print helpful `--help` messages by default."*

**What to observe:**
- The agent records this guideline into project context or memory so future responses respect it automatically.

---

## 💡 Steering Pro-Tips

1. **Use Slash Commands early:** Don't wait until code is written to realize assumptions were misaligned. Run `/grill-me` or `/plan` at the beginning.
2. **Short, directive corrections:** If the agent strays, give short feedback: *"Stop using CommonJS, switch to ESM imports."*
3. **Commit frequently:** Make small Git commits after each milestone so you can revert anytime.
