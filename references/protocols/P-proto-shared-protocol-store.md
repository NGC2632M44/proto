# P-proto-shared-protocol-store - One canonical store across runtimes
> Type: implementation-path
> Scope: tool:proto
> Confidence: observed
> Source: protocol-forge cross-runtime design session

## Symptom
A protocol learned in Claude Code (`~/.claude/skills/`) is invisible to Codex (`~/.codex/skills/`) and vice versa; maintaining two libraries guarantees divergence and copy rot.

## Context
Multiple coding runtimes on one machine, each with its own skill discovery root. proto''s fuel (protocols) should transfer; its engine (SKILL.md/scripts) is small and stable.

## Diagnosis
The fuel and the engine have different churn rates. Share the high-churn fuel via a single canonical store mounted into each runtime; keep the low-churn engine installed per-runtime.

## Protocol
1. Keep one canonical store at `$PROTO_STORE` (default `~/.protocols`): `protocols/` (P-*.md + INDEX) and `inbox/`.
2. Mount `$PROTO_STORE/protocols` into each runtime''s proto skill `references/protocols` via junction (Windows) or symlink (POSIX); or set `PROTO_STORE` so `preflight.py` routes there without a link.
3. Run `scripts/sync_store.ps1` / `sync_store.sh` to (re)establish mounts; optionally `git pull`/`push` the store for cross-machine and community sync.
4. Writes from any runtime land in the one store; INDEX and preflight are shared.

## Validation
A trigger-keyword learned in Codex protects the next Claude Code session: preflight in cc reads the same INDEX. No duplicate protocol folders exist.

## Avoid
Don''t symlink the whole skill folder 鈥?only `references/protocols/` (and `inbox/`). Don''t store runtime-specific absolute paths in protocol files. Don''t keep a per-runtime protocols copy "just in case" 鈥?that recreates the divergence.

## Promotion
Encoded in `references/cross-runtime.md` and `scripts/sync_store.*`. This file is the rationale reference.
