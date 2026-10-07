# Protocol Index

Living index of extracted protocols. Each entry is one atomic, reusable unit following [`protocol-schema.md`](../protocol-schema.md). Routing is by the bracketed trigger-keywords — Preflight matches on intent, not exact text. See [`routing.md`](../routing.md).

## tool-contract
- [P-gh-repo-create-remote](./P-gh-repo-create-remote.md) — [gh, gh-repo-create, remote, origin, Unable-to-add-remote] `gh repo create --remote=origin` reports "Unable to add remote" when origin already exists; the repo is still created. Cosmetic failure.

## harness-error
- [P-win-ps-setcontent-utf8-bom](./P-win-ps-setcontent-utf8-bom.md) — [powershell, Set-Content, utf8, BOM, ufeff, index.lock, lint, title] Set-Content -Encoding utf8 on PS 5.x writes a BOM that breaks ^# regex/lint; use [IO.File]::WriteAllText.
## harness-error
- [P-win-python-requests-proxy-hijack](./P-win-python-requests-proxy-hijack.md) — [requests, proxy, HTTP_PROXY, privoxy, RemoteDisconnected, babelark, 21882] Claude Code 注入的代理 env 劫持 Python requests → 境外 LLM API 断连;Session 显式禁代理;curl 外网诊断不可信(沙箱)。
- [P-win-requests-port-exhaustion-10048](./P-win-requests-port-exhaustion-10048.md) — [requests, 10048, port-exhaustion, TIME_WAIT, session, keep-alive, Windows] 每次裸 requests.post 大响应 → Windows 端口耗尽 WinError 10048;用全局 Session 连接池。

## environment
- [P-win-git-push-retry](./P-win-git-push-retry.md) — [git-push, force-push, 443, schannel, proxy, Windows, timeout] Transient `port 443` / `schannel` push failures on a proxied Windows host; retry in a loop, verify via the host API.
- [P-codex-sandbox-readonly-git](./P-codex-sandbox-readonly-git.md) — [git, index.lock, Permission-denied, sandbox, fetch-first, 443, codex, escalated] Git writes fail in Codex workspace-write sandbox (.git read-only, network blocked); restore via git show, escalate for add/commit/push, rebase not force.

## implementation-path
- [P-git-history-squash](./P-git-history-squash.md) — [git-history, squash, force-push, orphan, Initial-commit, public-push] Erase authoring/rename traces before a public push via an orphan branch + force-push; one clean "Initial commit".
- [P-cross-platform-skill-install](./P-cross-platform-skill-install.md) — [skill, SKILL.md, frontmatter, metadata, Claude-Code, Codex, install] One SKILL.md frontmatter (union of `description` + Codex `metadata`) serves both Claude Code and Codex; install into both skill roots.

## domain-knowledge
- [P-sci-paper-intro-no-header](./P-sci-paper-intro-no-header.md) — [pdf, Introduction, abstract_and_intro, Nature, figexplain, 引言, 0字] Nature 系论文引言无 Introduction 标题;折叠空白全文上取「摘要尾部→Results」区间为引言。
- [P-sci-fig-caption-unicode-space](./P-sci-fig-caption-unicode-space.md) — [pdf, caption, \xa0, unicode-space, PNAS, figexplain, 图0] PDF 文本匹配的空白类必须含 Unicode 空格(\xa0 等),否则 "Fig.\xa01A" 全漏匹配、图=0。

## anti-pattern
- [P-protocol-lint-scope](./P-protocol-lint-scope.md) — [protocol_lint, lint, false-positive, P-prefix, scope] Gate the protocol linter on the `P-*.md` filename convention, not just the `.md` extension; schema/prose/README are not protocols.
- [P-proto-collect-distill-split](./P-proto-collect-distill-split.md) — [proto, auto-capture, collect, distill, inbox, trace, token-cost] Split always-on cheap trace collection from on-demand LLM distillation; closed-loop replay match validates a distilled protocol.
- [P-proto-shared-protocol-store](./P-proto-shared-protocol-store.md) — [proto, cross-runtime, PROTO_STORE, junction, symlink, cc, codex, sync] One canonical protocol store mounted into each runtime's skill; engine per-runtime, fuel shared.

## sharing
- [P-proto-protocol-pack](./P-proto-protocol-pack.md) — [pack, export, import, marketplace, share, collision, re-key, PACK.md] Protocol packs (P-*.md + INDEX snippet + PACK.md provenance) are the sharing unit; pack.py exports/imports, re-keying on collision.
- [P-proto-codex-integration](./P-proto-codex-integration.md) — [codex, plugin, mcp, mcp-server, stdio, summary-strip, session-end, automation, retrospect] Three integration shapes (skill/plugin/MCP) sharing one engine; MCP is on-demand stdio not daemon; do not target Codex's private summary strip.
---

Maintenance rules:
- Add a new protocol here when you create its file, with a 3-6 keyword tag set.
- When a protocol is promoted into `SKILL.md` or a script, mark its `Confidence: promoted` and keep the index entry pointing at the file as the rationale.
- Merge entries when two protocols share trigger, context, fix, and validation.
- If a pitfall recurs, first check whether a protocol should have fired — if so, fix its keywords/INDEX entry (routing failure) or its content, do not just re-solve.
