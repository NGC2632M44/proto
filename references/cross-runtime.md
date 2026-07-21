# Cross-Runtime Protocol Store

Problem: Claude Code discovers skills in `~/.claude/skills/`; Codex in `~/.codex/skills/`. A protocol learned in one runtime is invisible to the other, so lived experience does not transfer 鈥?the exact pitfall re-bites in the other agent.

Solution: **one canonical store, many runtime mounts.** The protocol library is the single source of truth; each runtime's proto skill points its preflight at the same store.

## Layout

Canonical store (default `~/.protocols`, override with `PROTO_STORE`):

```
~/.protocols/
  protocols/   # shared P-*.md library + INDEX.md
  inbox/       # raw traces awaiting distillation (see auto-capture.md)
```

If you `git init` the store and set a remote, it doubles as the cross-machine and community sync point.

## Mounting into each runtime

Each runtime's installed proto skill should resolve `references/protocols/` from the shared store, not a per-runtime copy. Two interchangeable options:

- **Junction/symlink (preferred, zero duplication).** Link `<runtime-skill>/references/protocols` -> `$PROTO_STORE/protocols`. On Windows use a junction (`New-Item -ItemType Junction`) 鈥?no admin rights, no symlink privilege. On POSIX use `ln -sfn`.
- **Env override (fallback).** `scripts/preflight.py` honors `PROTO_STORE`: when set, it routes to `$PROTO_STORE/protocols/INDEX.md` instead of the bundled folder. The runtime keeps its own skill files but shares the protocol data.

## Sync script

`scripts/sync_store.ps1` (Windows) and `scripts/sync_store.sh` (POSIX):

1. Ensure `$PROTO_STORE` exists; create `protocols/` and `inbox/`.
2. For each detected runtime (`~/.claude/skills/proto`, `~/.codex/skills/proto`), junction/symlink its `references/protocols` to the store (replacing an existing link, never a real folder).
3. Optional `git pull` on entry / `git push` on exit so multiple machines share one library.

## Why this works

- Writes from either runtime land in one store 鈥?no divergence, no copy rot.
- INDEX and the preflight router are shared, so a trigger-keyword learned in Codex immediately protects the next Claude Code session.
- The skill *engine* (SKILL.md / scripts) stays versioned with the skill (small, stable); only the *fuel* (protocols) is shared. This matches the engine/fuel split in SKILL.md.

## Avoid

- Don't maintain two protocol folders 鈥?that re-creates the exact divergence this store exists to prevent.
- Don't store runtime-specific absolute paths in protocol files; the store is cross-machine.
- Don't symlink the entire skill folder 鈥?only `references/protocols/` (and optionally `inbox/`). The engine should version with the skill, not the store.
