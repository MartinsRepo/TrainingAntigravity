# Module 06 Lab: Configuring MCP & Lifecycle Hooks

In this lab, you will author an MCP server configuration and configure a lifecycle hook.

---

## 🔬 Lab Exercises

### Exercise 6.1: Authoring an MCP Server Configuration (`.agents/mcp_config.json`)
We will configure an MCP server configuration template showing how external tool servers are attached:
```json
{
  "mcpServers": {
    "git-tools": {
      "command": "python3",
      "args": ["-m", "mcp_git_server"],
      "env": {
        "GIT_PYTHON_REFRESH": "quiet"
      }
    }
  }
}
```

---

### Exercise 6.2: Creating a Lifecycle Hook (`.agents/hooks.json`)
We will create a lifecycle hook that executes a validator before or after tool actions:
```json
{
  "hooks": {
    "post_tool_execution": [
      {
        "matcher": "write_to_file|replace_file_content",
        "command": "python3 .agents/hooks/format_checker.py"
      }
    ]
  }
}
```

---

## 💡 Best Practices for MCP & Hooks

1. **Keep MCP servers lightweight:** Avoid servers with massive startup latency to keep the agent responsive.
2. **Deterministic hooks:** Ensure hooks fail fast and return clean exit codes (0 for success).
3. **Commit team integrations:** Keep `.agents/mcp_config.json` and `.agents/hooks.json` in version control so everyone on the team has access to the same tools.
