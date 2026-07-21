# Protocol Index

Living index of extracted protocols. Each entry is one atomic, reusable unit following [`protocol-schema.md`](../protocol-schema.md). Routing is by the bracketed trigger-keywords — Preflight matches on intent, not exact text. See [`routing.md`](../routing.md).

## tool-contract
- [P-gh-repo-create-remote](./P-gh-repo-create-remote.md) — [gh, gh-repo-create, remote, origin, Unable-to-add-remote] `gh repo create --remote=origin` reports "Unable to add remote" when origin already exists; the repo is still created. Cosmetic failure.

## environment
- [P-win-git-push-retry](./P-win-git-push-retry.md) — [git-push, force-push, 443, schannel, proxy, Windows, timeout] Transient `port 443` / `schannel` push failures on a proxied Windows host; retry in a loop, verify via the host API.

## implementation-path
- [P-git-history-squash](./P-git-history-squash.md) — [git-history, squash, force-push, orphan, Initial-commit, public-push] Erase authoring/rename traces before a public push via an orphan branch + force-push; one clean "Initial commit".
- [P-cross-platform-skill-install](./P-cross-platform-skill-install.md) — [skill, SKILL.md, frontmatter, metadata, Claude-Code, Codex, install] One SKILL.md frontmatter (union of `description` + Codex `metadata`) serves both Claude Code and Codex; install into both skill roots.

## anti-pattern
- [P-protocol-lint-scope](./P-protocol-lint-scope.md) — [protocol_lint, lint, false-positive, P-prefix, scope] Gate the protocol linter on the `P-*.md` filename convention, not just the `.md` extension; schema/prose/README are not protocols.
- [P-proto-collect-distill-split](./P-proto-collect-distill-split.md) — [proto, auto-capture, collect, distill, inbox, trace, token-cost] Split always-on cheap trace collection from on-demand LLM distillation; closed-loop replay match validates a distilled protocol.
- [P-proto-shared-protocol-store](./P-proto-shared-protocol-store.md) — [proto, cross-runtime, PROTO_STORE, junction, symlink, cc, codex, sync] One canonical protocol store mounted into each runtime's skill; engine per-runtime, fuel shared.

---

Maintenance rules:
- Add a new protocol here when you create its file, with a 3-6 keyword tag set.
- When a protocol is promoted into `SKILL.md` or a script, mark its `Confidence: promoted` and keep the index entry pointing at the file as the rationale.
- Merge entries when two protocols share trigger, context, fix, and validation.
- If a pitfall recurs, first check whether a protocol should have fired — if so, fix its keywords/INDEX entry (routing failure) or its content, do not just re-solve.
