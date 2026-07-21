# Codex / MCP Integration

Proto integrates with Codex (and any MCP client) as **one shape**: an on-demand stdio **MCP server**. No separate plugin scaffold, no per-platform packaging. The community standard for agent-memory / experience-capture tools (memorizer, agent-memory-mcp, linksee-memory, ...) is uniformly "an MCP server" -- proto follows that precedent rather than maintaining three parallel shapes.

## The one shape: MCP server (`scripts/mcp_proto.py`)

A stdio JSON-RPC 2.0 server, launched **on demand** as a child process by the MCP client. Not a daemon, not persistent, zero dependencies.

| Tool | Role |
|---|---|
| `collect_trace` | record a failed operation into the inbox (no LLM) |
| `preflight` | route an operation text to the protocol(s) to read |
| `lint_protocols` | validate protocol files against the schema |
| `inbox_status` | cheap count + cluster hint; the distill gate |
| `retrospect` | gather cheap material for a session retrospect (LLM synthesis stays in the agent) |
| `pack_export` / `pack_import` | share protocols as a pack |

Configure it in your client's MCP config (Codex `~/.codex/config.toml` or `.mcp.json`; Claude Code `~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "proto": {
      "type": "local",
      "command": "python",
      "args": ["/absolute/path/to/protocol-forge/scripts/mcp_proto.py"],
      "env": { "PROTO_STORE": "~/.protocols" }
    }
  }
}
```

## What about the skill's `SKILL.md`?

The MCP server is the **execution core**; it does not know *when* to call itself. The `SKILL.md` (installed at `~/.codex/skills/proto` / `~/.claude/skills/proto`) is the **behavior layer**: it tells the agent to call `preflight` before risky ops, `collect_trace` on any failure, `retrospect` at session end, and to honest-grade confidence. So the integration is "SKILL.md rules + MCP tools", not "skill OR MCP". The skill-only install (`install_skill.ps1`) already deploys the SKILL.md; adding the MCP server config is the one extra line for clients that want tool-call access.

## What about Codex's left-side summary strip?

Researched via the official Codex manual: that strip is **Codex-owned UI state with no public extension feed** (no API, manifest field, file contract, or MCP mechanism to populate it). So proto does not inject into it. `retrospect` produces a standard Markdown summary the agent surfaces in chat; the user/Codex treats it as the session summary. "Linking with the strip" = producing the right content, not hijacking the UI.

## Session-end triggering

Codex has **no documented `SESSION-END` event**. Proto self-drives two ways:
- **Agent rule** (in `SKILL.md`): the agent proposes `retrospect` when `inbox_status` crosses the gate (>= 10) or at a substantial session boundary.
- **Optional Codex automation**: a scheduled/thread-wakeup check that calls `inbox_status` and proposes distillation when the gate is crossed.

## Why not also ship a plugin?

Researched and rejected: the plugin scaffold (`.codex-plugin/plugin.json` + marketplace entry) is Codex-private, adds maintenance, and buys only discovery + composer prompts -- which a one-line MCP config already covers. The community ships experience-capture as MCP, not as platform plugins. One shape is easier to maintain and works across clients.