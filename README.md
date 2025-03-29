# Obsidian MCP

This is a MCP for interacting with my Obsidian vaults from LLMs.

It has basic functionality for:

- Listing files in a vault
- Reading file contents in a vault
- And updating file contents in a vault

I have also included some prompts for common tasks I do for adding new vaults (namely importing recipes into my vault).

## Usage

Test locally with:

```
uv run mcp dev server.py
```

Install with Claude Desktop:

```
uv run mcp install server.py
```

NOTE: I manually updated the config it generated to ensure dependencies are installed. Below is my config:

```
{
  "mcpServers": {
    "obsidian": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/calebvandyke/code/personal-mcps/obsidian",
        "run",
        "mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```
