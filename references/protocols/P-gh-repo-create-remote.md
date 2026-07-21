# P-gh-repo-create-remote - Avoid the double-add-remote failure
> Type: tool-contract
> Scope: tool:gh
> Confidence: validated
> Source: protocol-forge repo creation session

## Symptom
`gh repo create <owner>/<repo> --public --source=. --remote=origin` prints the repo URL then `X Unable to add remote "origin"`, yet the repo was created and `origin` already points to the right URL.

## Context
Local repo where `origin` was already added manually; `gh` authenticated; user wants `gh` to create repo and wire the remote.

## Diagnosis
`gh repo create --remote=origin` always attempts `git remote add origin`. If origin exists, the add fails — but repo creation happens first, so the repo exists while "Unable to add remote" refers only to the already-correct local remote. Cosmetic, not auth.

## Protocol
1. Check first: `git remote -v`. If origin already points to the intended URL, skip `--remote`.
2. Create without `--remote`: `gh repo create <owner>/<repo> --public --source=. --description "..."`. Add `--remote=origin` only when no origin exists.
3. If you already saw "Unable to add remote origin", don't treat as failure — verify: `gh repo view <owner>/<repo> --json url,visibility`.
4. Confirm no duplicate: `git remote -v` shows exactly one origin fetch + one origin push, both correct URL.

## Validation
`gh repo view` returns intended visibility/description. `git remote -v` lists one origin pair. `git push -u origin main` succeeds (modulo network — see P-win-git-push-retry).

## Avoid
Don't re-run `gh repo create` after the cosmetic failure (name collision error). Don't reflexively `git remote remove origin` + re-run when origin is already correct (wasted motion). Don't read it as auth failure and re-authenticate.

## Promotion
Keep as reference. Trigger is specific to `gh`'s remote flag; a script can't decide whether the user intended a pre-existing origin.
