# P-proto-codex-integration - One MCP shape, not three (skill+plugin+MCP was over-engineering)
> Type: implementation-path
> Scope: tool:proto
> Confidence: validated
> Source: protocol-forge Codex integration session + community survey (2026-07-21)

## Symptom
Tempting to ship three integration shapes (skill-only + Codex plugin + MCP server) for "flexibility". Maintaining all three is over-engineering and diverges from community precedent.

## Context
Surveyed GitHub agent-memory / experience-capture projects (memorizer 178*, agent-memory-mcp, linksee-memory, ...): they ship as a single MCP server, no platform-plugin parallel. Codex plugin scaffold is Codex-private (no cross-client value). Codex's summary strip is private UI (no extension feed). No native SESSION-END event.

## Diagnosis
The MCP server is the execution core; SKILL.md is the behavior layer that says when to call it. That pair already covers everything. A plugin scaffold only adds Codex discovery (covered by a one-line MCP config) at the cost of platform lock-in + maintenance. Three shapes is over-engineering; one (MCP + SKILL.md) is the community-aligned answer.

## Protocol
1. Ship one MCP server (`scripts/mcp_proto.py`, stdio, on-demand, zero-dep) with 7 tools.
2. Keep SKILL.md as the behavior layer (when to preflight / collect / retrospect / honest-grade); it is NOT an alternative to MCP -- it drives the MCP tools.
3. Configure via the client's MCP config (one line); do not ship a plugin scaffold or marketplace entry.
4. `retrospect` produces standard Markdown (do not target Codex's private summary strip).
5. Session-end: agent self-proposes (SKILL.md rule) + optional automation polling inbox_status.

## Validation
MCP server responds to initialize/tools/list/tools/call (inbox_status, preflight, lint verified). All clients reading the same $PROTO_STORE. No plugin scaffold to maintain.

## Avoid
Don't ship a Codex plugin parallel to the MCP server -- it is platform-private, redundant with a one-line MCP config, and not what the community does. Don't make the MCP server a daemon. Don't try to feed Codex's summary strip.

## Promotion
Encoded in `references/codex-integration.md` and `scripts/mcp_proto.py`. This file is the rationale and the anti-over-engineering record.