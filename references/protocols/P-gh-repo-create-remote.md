# P-gh-repo-create-remote - Avoid the double-add-remote failure
> Type: tool-contract
> Scope: tool:gh
> Confidence: validated
> Source: protocol-forge repo creation session

## Symptom
Running `gh repo create <owner>/<repo> --public --source=. --remote=origin` prints the new repo URL but then a line `X Unable to add remote "origin"`, even though the repo was created successfully. A subsequent inspection shows `origin` already exists and points to the right URL, so the message looks contradictory.

## Context
A local git repo that already has a remote named `origin` configured (e.g. it was added manually with `git remote add origin <url>` moments before), on a host where `gh` is authenticated. The user wants `gh` to both create the GitHub repo and wire up the remote.

## Diagnosis
`gh repo create --remote=origin` unconditionally attempts `git remote add origin <url>`. If `origin` already exists, the add fails — but `gh` creates the repo first, then attempts the remote add, so the repo exists on the host while the "Unable to add remote" line refers only to the (already-correct) local remote. The failure is cosmetic: the remote is already what `gh` wanted it to be. It is not an auth or permissions error.

## Protocol
1. Check the remote first: `git remote -v`. If `origin` already points to the intended GitHub URL, skip the `--remote` flag.
2. Create the repo without `--remote`: `gh repo create <owner>/<repo> --public --source=. --description "..."`. Add `--remote=origin` only when no origin exists yet.
3. If you already ran `gh repo create ... --remote=origin` and saw "Unable to add remote origin", do not treat it as a failure of repo creation — verify the repo exists: `gh repo view <owner>/<repo> --json url,visibility`.
4. Verify the remote is correct and not a duplicate: `git remote -v` should show exactly one `origin` fetch and one `origin` push, both to the right URL.

## Validation
`gh repo view <owner>/<repo>` returns the repo with the intended visibility and description. `git remote -v` lists exactly one origin pair. `git push -u origin main` succeeds (modulo network, see P-win-git-push-retry).

## Avoid
Do not re-run `gh repo create` after the "Unable to add remote" line — the repo already exists and a second call will error on the name collision. Do not `git remote remove origin` then re-run `gh repo create --remote=origin` reflexively; that is wasted motion when the existing remote is already correct. Do not read the cosmetic failure as an auth failure and start re-authenticating.

## Promotion
Keep as a reference protocol. The trigger is specific to `gh`'s remote-handling flag; a script cannot decide whether the user *intended* a pre-existing origin, so the judgement stays here.
