---
name: proto
description: Proto as a Codex plugin. Collect failed-command traces, run preflight before risky ops, lint protocols, manage packs, and gather retrospect material -- all via the bundled MCP server. Use when a user wants to operationalize lived experience into reusable protocols without an interactive shell.
metadata:
  short-description: Forge reusable protocols into skills (Codex plugin)
---

# Proto (Codex Plugin)

This is the Codex-plugin packaging of proto. The engine is exposed as MCP tools (see `.mcp.json`); this skill is the entry surface that tells the agent when and how to use them.

> Trigger with `$proto`. North star: never step in the same pit twice.

## When to use the MCP tools

- **Before any known-risky operation** (git push/force, gh repo create, linting a new dir, rewriting history, anything over a proxy or involving Windows paths): call `preflight` with the operation text; read the matched `P-*.md`; apply its steps and respect its `Avoid` list.
- **Any command you run that exits nonzero OR matches a known error regex** (InputValidationError, GBK/UnicodeDecodeError, schannel, gh 403/422, timeout): call `collect_trace` before moving on. AFK by design -- the agent self-collects.
- **Before deciding to distill**: call `inbox_status`. When it says "READY to distill" (>= 10 traces) or at session end, call `retrospect` to gather cheap material, then draft `P-*.md` files (the LLM synthesis is your job, not the tool's).
- **To share**: `pack_export` a set of protocols; consumers `pack_import` them (use `dry_run` first on untrusted packs).
- **To validate**: `lint_protocols` on the store; a distilled protocol must replay-match -- run `preflight` on the trace that birthed it and confirm it routes back.

See the sibling skill files (`SKILL.md`, `references/`, `scripts/` at the repo root) for the full engine. This plugin's `.mcp.json` launches `scripts/mcp_proto.py` as a stdio child process -- on-demand, not a daemon.