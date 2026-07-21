# P-codex-sandbox-readonly-git - Git writes fail in the Codex workspace-write sandbox
> Type: environment
> Scope: tool:codex
> Confidence: validated
> Source: protocol-forge sync session (2026-07-21)

## Symptom
In the Codex CLI `workspace-write` sandbox, `git checkout -- <file>`, `git add`, `git commit`, `git reset` fail with `fatal: Unable to create '.git/index.lock': Permission denied`. `git fetch`/`git push` fail with `Failed to connect to github.com port 443`. Read commands (`git log`, `git show`, `git status`, `git diff`) work.

## Context
Codex sandbox mounts `.git` read-only and blocks network. Working tree files are writable. This hits any task that wants to commit, rebase, or push.

## Diagnosis
Two independent gates: `.git` is read-only (blocks index/ref writes), and the network is restricted (blocks fetch/push/clone). Read-only git commands succeed because they never touch `.git` mutably.

## Protocol
1. For read-only inspection, use `git show HEAD:<path>`, `git log`, `git diff` -- they work and need no escalation.
2. To restore a working-tree file without the index, pipe `git show HEAD:<path>` to a temp file and `Move-Item` it over the target (writable tree, no `.git` write).
3. For real writes (`add`/`commit`/`pull --rebase`/`push`), request escalation once with `sandbox_permissions: require_escalated` and a `prefix_rule` of `["git"]`. Do not retry the same escalated command more than 2-3 times against a 503 reviewer -- hand off to the user.
4. On `! [rejected] main -> main (fetch first)`, run `git fetch && git pull --rebase origin main && git push` -- never `--force` over a remote that has work you don't have.

## Validation
`git status` shows a clean tree after commit. `git ls-remote origin main` matches local `git rev-parse HEAD`. No `index.lock` errors.

## Avoid
Do not `git push --force` to bypass a "fetch first" rejection -- it erases remote-only commits. Do not attempt to `git checkout` inside the sandbox without escalation. Do not loop escalated retries against a persistent 503 -- it is a platform outage, not a policy denial.

## Promotion
Keep as a validated protocol. Related: `P-win-ps-setcontent-utf8-bom` (authoring side of the same session), `P-proto-collect-distill-split` (cheap-signal capture).