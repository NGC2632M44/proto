# P-proto-codex-integration - Three shapes for Codex (skill / plugin / MCP)
> Type: implementation-path
> Scope: tool:proto
> Confidence: validated
> Source: protocol-forge Codex integration design session (2026-07-21)

## Symptom
Users want proto to "just work" in Codex like other skills (agent calls it anytime, no manual shell), and to link with Codex's left-side session-summary strip; the skill-only install feels too manual and there is no obvious integration point.

## Context
Codex supports plugins (`.codex-plugin/plugin.json` with skills/mcpServers/apps), MCP servers (stdio child, on-demand, not daemon), and automations (scheduled/thread-wakeup). The left-side summary strip is Codex-owned UI state with no public extension feed (no API/manifest/file/MCP contract). No documented `SESSION-END` event exists.

## Diagnosis
Split integration into three shapes sharing one engine. The skill is the entry surface; the MCP server is the execution core (on-demand stdio, no daemon); the plugin wraps both for discovery + composer prompts. Do NOT target the summary strip -- produce the right summary content instead. Drive session-end retrospect via the agent rule (already in SKILL.md) plus optional automations, since there is no native SESSION-END event.

## Protocol
1. Skill-only: `install_skill.ps1 -Both` (engine + scripts, no packaging).
2. Plugin: scaffold with plugin-creator, validate with `validate_plugin.py`; manifest points skills + .mcp.json.
3. MCP: `scripts/mcp_proto.py` (stdio JSON-RPC 2.0); tools: collect_trace, preflight, lint_protocols, inbox_status, retrospect, pack_export/import. Launch on-demand; never daemonize.
4. Summary strip: do not inject; let `retrospect` produce standard Markdown the agent surfaces.
5. Session-end: agent self-proposes retrospect (SKILL.md rule) + optional Codex automation polling `inbox_status`.

## Validation
`validate_plugin.py proto-plugin` passes. MCP server responds correctly to initialize/tools/list/tools/call (inbox_status, preflight, lint_protocols verified). All shapes read the same `$PROTO_STORE`.

## Avoid
Don't try to feed Codex's summary strip -- it is private UI state, no extension feed. Don't make the MCP server a persistent daemon -- it breaks proto's no-resident-process design. Don't duplicate the engine per shape -- one engine, three wrappers.

## Promotion
Encoded in `references/codex-integration.md`, `scripts/mcp_proto.py`, `proto-plugin/`. This file is the rationale reference.