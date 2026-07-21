# P-win-git-push-retry - Retry force-push on transient network failures
> Type: environment
> Scope: global
> Confidence: validated
> Source: protocol-forge force-push session on a proxied Windows host

## Symptom
`git push` (and especially `git push --force`) fails with one of:
- `Failed to connect to github.com port 443 after ~21000ms: Could not connect to server`
- `schannel: server closed abruptly (missing close_notify)`

The same command, run again seconds later, succeeds. There is no change to credentials, remote URL, or branch between failures.

## Context
A Windows host behind a local HTTP proxy (e.g. `http.proxy = http://127.0.0.1:7890` in git config), pushing to GitHub over HTTPS. Connectivity to the proxy and to github.com is intermittent — the proxy port is not always reachable and TLS handshakes are occasionally cut short.

## Diagnosis
These are transient transport-layer failures, not auth or ref failures. The proxy or upstream link drops mid-handshake; a single attempt times out or is reset. Git treats it as fatal, but the operation is idempotent for a clean push and safe-to-retry for a force-push (the target ref is the same and the source commit is unchanged), so retrying is correct and eventually succeeds.

## Protocol
1. Identify the failure as transport, not auth: the message names `port 443`, `Could not connect`, or `schannel`. If the message is `Authentication failed` or `refusing to allow`, do NOT retry — treat it as a different protocol.
2. Retry the same push command in a short loop with a small sleep, capturing each attempt's output:
   ```bash
   for i in 1 2 3 4 5; do
     OUT=$(git push origin main 2>&1)
     echo "$OUT" | tail -2
     echo "$OUT" | grep -qE "main|up to date" && { echo "PUSHED on attempt $i"; break; }
     sleep 4
   done
   ```
3. For force-push specifically, confirm success via the host API rather than trusting the local ref: `gh api repos/<owner>/<repo>/commits --jq '.[].sha[0:7]'`.
4. If all attempts fail with the *same* transport error, the proxy is down — pause and resume rather than hammering.

## Validation
A retry loop returns "PUSHED on attempt N" and the host API lists the expected commit SHA. The pushed SHA matches `git rev-parse HEAD`.

## Avoid
Do not retry an authentication or permission failure — it will not self-heal and burns rate-limit. Do not assume success from the push command exiting 0 alone; a `tee`/pipe can mask a nonzero exit. Do not shorten the sleep below ~3s; back-to-back retries against a flaky proxy make the flakiness worse.

## Promotion
Keep as a reference protocol. The retry shape is generic enough to live here; a script would have to encode the "transport vs auth" discriminator and the force-push-vs-push distinction, which is better judged per-incident.
