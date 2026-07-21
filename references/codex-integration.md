# Codex Integration: Plugin + MCP

Proto ships three integration shapes for Codex (and any MCP client). They share one engine; pick by how much ceremony you want.

## 1. Skill-only (already installed)

`~/.codex/skills/proto` and `~/.claude/skills/proto`. The agent reads `SKILL.md` and runs `scripts/*.py` directly. Zero packaging. This is what `install_skill.ps1` sets up. Use this if you only want the engine and are happy invoking scripts by path.

## 2. Codex plugin (`proto-plugin/`)

A discoverable Codex plugin that wraps the skill and adds a UI entry (displayName, defaultPrompt, brandColor). Built with the `plugin-creator` skill; validated by `validate_plugin.py`.

```
proto-plugin/
  .codex-plugin/plugin.json   # manifest: skills + mcpServers + interface
  .mcp.json                   # launches the MCP server (see #3)
  skills/proto/SKILL.md       # thin entry surface: when to call which tool
  assets/
```

Install via the personal marketplace (`.agents/plugins/marketplace.json`) or `codex plugin marketplace add <repo>`. The plugin's value is discovery + the composer starter prompts; execution still flows through the MCP server.

## 3. MCP server (`scripts/mcp_proto.py`)

The execution core. A stdio JSON-RPC 2.0 server launched **on demand** as a child process by the MCP client -- not a daemon, not persistent. Any MCP-capable client (Codex, Claude Code, others) gets the same tools:

| Tool | Role |
|---|---|
| `collect_trace` | record a failed operation into the inbox (no LLM) |
| `preflight` | route an operation text to the protocol(s) to read |
| `lint_protocols` | validate protocol files against the schema |
| `inbox_status` | cheap count + cluster hint; the distill gate |
| `retrospect` | gather cheap material for a session retrospect (LLM synthesis stays in the agent) |
| `pack_export` / `pack_import` | share protocols as a pack |

Configure in `.mcp.json`:
```json
{
  "mcpServers": {
    "proto": {
      "type": "local",
      "command": "python",
      "args": ["${workspaceFolder}/scripts/mcp_proto.py"],
      "env": { "PROTO_STORE": "${env:HOME}/.protocols" }
    }
  }
}
```

## What about Codex's left-side summary strip?

Researched via the official Codex manual: that strip is **Codex-owned UI state with no public extension feed** (no API, manifest field, file contract, or MCP mechanism to populate it). So proto does not try to inject into it. Instead, proto's `retrospect` produces a standard Markdown summary that the agent can surface in chat; the user or Codex can treat it as the session summary. "Linking with the strip" = producing the right summary content, not hijacking the UI.

## Session-end triggering

Codex has **no documented `SESSION-END` event**. Two ways proto still self-drives:
- **Agent rule** (in `SKILL.md`, already added): the agent proposes `retrospect` when the inbox hits the gate or at a substantial session boundary.
- **Codex automations** (scheduled/thread-wakeup): optionally register a recurring check that calls `inbox_status` and proposes distillation when the gate is crossed.

## Which shape to use

- **Just want it to work, minimal**: skill-only (`install_skill.ps1 -Both`).
- **Want Codex discovery + composer prompts**: install the plugin (it pulls in the MCP server).
- **Non-Codex client or want raw tool access**: point your MCP client at `scripts/mcp_proto.py` directly.

All three read the same `$PROTO_STORE`; the protocol library is the single source of truth regardless of integration shape.