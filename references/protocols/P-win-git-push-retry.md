# P-win-git-push-retry - Retry force-push on transient network failures
> Type: environment
> Scope: global
> Confidence: validated
> Source: protocol-forge force-push session on a proxied Windows host

## Symptom
`git push` / `git push --force` fails with `Failed to connect to github.com port 443 after ~21000ms` or `schannel: server closed abruptly (missing close_notify)`. Same command succeeds seconds later. No credential/URL/branch change.

## Context
Windows host behind a local HTTP proxy (e.g. `http.proxy = http://127.0.0.1:7890`), pushing to GitHub over HTTPS; proxy/upstream intermittently drops the TLS handshake.

## Diagnosis
Transient transport-layer failure, not auth. Operation is idempotent (clean push) or safe-to-retry (force-push to same ref, unchanged source commit), so retrying is correct and eventually succeeds.

## Protocol
1. Identify as transport, not auth: message names `port 443` / `Could not connect` / `schannel`. If `Authentication failed` or `refusing to allow`, STOP — different problem.
2. Retry in a short loop with ~4s sleep:
   ```bash
   for i in 1 2 3 4 5; do OUT=$(git push origin main 2>&1); echo "$OUT"|tail -2; echo "$OUT"|grep -qE "main|up to date" && { echo "PUSHED on attempt $i"; break; }; sleep 4; done
   ```
3. For force-push, confirm via host API not local ref: `gh api repos/<owner>/<repo>/commits --jq '.[].sha[0:7]'`.
4. All attempts fail identically → proxy is down; pause, don't hammer.

## Validation
Loop prints "PUSHED on attempt N"; host API lists expected SHA; SHA matches `git rev-parse HEAD`.

## Avoid
Don't retry auth/permission failures (won't self-heal, burns rate-limit). Don't trust push exit 0 alone (pipe can mask nonzero). Don't sleep <3s (back-to-back retries worsen flaky proxy).

## Promotion
Keep as reference. Generic retry shape; a script can't encode the transport-vs-auth discriminator + force-push-vs-push distinction — judge per-incident.
