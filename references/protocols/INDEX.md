# Protocol Index

Living index of extracted protocols. Each entry is one atomic, reusable unit following [`protocol-schema.md`](../protocol-schema.md).

## tool-contract
- [P-gh-repo-create-remote](./P-gh-repo-create-remote.md) — `gh repo create --remote=origin` reports "Unable to add remote" when origin already exists; the repo is still created. Cosmetic failure.

## environment
- [P-win-git-push-retry](./P-win-git-push-retry.md) — Transient `port 443` / `schannel` push failures on a proxied Windows host; retry in a loop, verify via the host API.

## implementation-path
- [P-git-history-squash](./P-git-history-squash.md) — Erase authoring/rename traces before a public push via an orphan branch + force-push; one clean "Initial commit".
- [P-cross-platform-skill-install](./P-cross-platform-skill-install.md) — One SKILL.md frontmatter (union of `description` + Codex `metadata`) serves both Claude Code and Codex; install into both skill roots.

## anti-pattern
- [P-protocol-lint-scope](./P-protocol-lint-scope.md) — Gate the protocol linter on the `P-*.md` filename convention, not just the `.md` extension; schema/prose/README are not protocols.

---

Maintenance rules:
- Add a new protocol here when you create its file.
- When a protocol is promoted into `SKILL.md` or a script, mark its `Confidence: promoted` and keep the index entry pointing at the file as the rationale.
- Merge entries when two protocols share trigger, context, fix, and validation.
