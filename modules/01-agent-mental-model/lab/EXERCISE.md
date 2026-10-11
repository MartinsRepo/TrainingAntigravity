# Module 01 Lab: Observing the Agent in Action

In this hands-on lab, we will directly observe how Antigravity interacts with your system.

---

## 🔬 Lab Steps

### Step 1: Tool Inspection Test
When you instruct an agent to find information, watch the tool calls displayed in the IDE interface:
- Look for tool names such as `run_command`, `list_dir`, `grep_search`, or `view_file`.
- Notice how the agent executes a tool, waits for the result, and synthesizes its findings.

### Step 2: Artifact Creation
Artifacts are special markdown documents generated under the agent's brain directory (`~/.gemini/antigravity-ide/brain/<conversation-id>/`). They are rendered in the auxiliary side panel in the Antigravity IDE / Antigravity 2.0 interface.
- Artifacts allow complex documents, tables, plans, and Mermaid diagrams to stay visible while conversation rolls forward.

### Step 3: Git Baseline
Every good agentic workflow uses Git as the checkpointing mechanism. If an agent performs an experiment that you don't like, Git allows instant rollback.

---

## 💡 Quick Tips for Working with Agents

1. **Be specific with intent, flexible with implementation**: State your objective clearly and let the agent research the best technical path.
2. **Review tool calls**: Check what commands or file edits the agent performs.
3. **Keep changes atomic**: Commit frequently so you can branch or revert easily.
