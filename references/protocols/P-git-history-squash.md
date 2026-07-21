# P-git-history-squash - Erase authoring/rename traces before public push
> Type: implementation-path
> Scope: global
> Confidence: validated
> Source: protocol-forge public release session

## Symptom
Multiple commits reveal the work's evolution (e.g. "Initial commit: <old name>" then "Rename skill to X"). For a public skill repo this is noise.

## Context
Skill repo about to be pushed publicly; working tree already final; non-interactive harness (no `git rebase -i`).

## Diagnosis
History is content the audience didn't ask for. `rebase -i` is unavailable; `--amend` only rewrites the tip. A single clean root requires a rootless branch holding only the current tree, force-pushed.

## Protocol
1. Confirm tree is final and clean: `git status`.
2. Confirm author identity (`user.name`/`user.email`, noreply for public skill repos).
3. `git checkout --orphan tmp-clean`.
4. `git commit -m "Initial commit"`.
5. `git branch -D main && git branch -m tmp-clean main`.
6. `git push --force origin main` (retry on transient failure — see P-win-git-push-retry).
7. Verify: `gh api repos/<owner>/<repo>/commits --jq 'length'` returns 1.

## Validation
Remote shows exactly one "Initial commit", noreply author, full file tree via `gh api .../git/trees/main`.

## Avoid
No interactive `git rebase -i` in a non-interactive harness (blocks/errors). No amend-and-call-it-clean (old root remains). No force-push before confirming the tree is final (irreversible from working tree).

## Promotion
Keep as reference. The 7-step sequence is too long for SKILL.md and too conditional for a script (rewrites history — must stay a human decision).
