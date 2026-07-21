# P-git-history-squash - Erase authoring/rename traces before public push
> Type: implementation-path
> Scope: global
> Confidence: validated
> Source: protocol-forge public release session

## Symptom
A local repo has multiple commits that reveal the work's evolution (e.g. "Initial commit: <old name>" followed by "Rename skill to X and prepare for public release"). For a published skill repo, these traces read as noise and leak the project's history of renaming and editing.

## Context
A skill repo about to be pushed to a public GitHub remote, where the audience is users of the skill, not readers of its commit history. The working tree is already in its final desired state. A second clean commit (or any non-trivial history) is not required by the content.

## Diagnosis
Commit history is content the audience did not ask for. `git rebase -i` is unavailable in non-interactive environments, and `git commit --amend` only rewrites the tip. The durable, scriptable way to produce a single clean "Initial commit" is to build a fresh rootless branch that contains only the current tree, then force-push it over the remote branch.

## Protocol
1. Ensure the working tree is the final state and nothing is uncommitted: `git status` must be clean (or stage everything first).
2. Confirm the desired author identity: `git config user.name` / `user.email` (use the platform noreply email for public skill repos).
3. Create a rootless branch with the current files: `git checkout --orphan tmp-clean`.
4. Commit once: `git commit -m "Initial commit"`.
5. Replace the published branch: `git branch -D main` then `git branch -m tmp-clean main`.
6. Overwrite the remote: `git push --force origin main`.
7. Verify on the host API: `gh api repos/<owner>/<repo>/commits --jq 'length'` returns 1.

## Validation
The remote shows exactly one commit with message "Initial commit", author email is the noreply address, and `gh api .../git/trees/main` lists the full final file set.

## Avoid
Do not use interactive `git rebase -i` in a non-interactive harness; the command will block or error. Do not amend the tip and call it clean — the old root commit still remains in history. Do not force-push without first confirming the tree is the intended final state; a force-push cannot be undone from the working tree.

## Promotion
Keep as a reference protocol. The seven-step sequence is too long for a SKILL.md rule and too conditional to harden into a script (it touches history, which must stay a human decision).
