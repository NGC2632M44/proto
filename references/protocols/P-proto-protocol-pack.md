# P-proto-protocol-pack - Protocol packs as the sharing/marketplace primitive
> Type: implementation-path
> Scope: tool:proto
> Confidence: observed
> Source: protocol-forge sharing direction (2026-07-21)

## Symptom
Protocols are valuable only inside the author's store; there is no portable unit to publish, share, or import across users, so everyone re-derives the same pitfalls.

## Context
A mature library has validated P-*.md files with trigger-keywords in INDEX. Multiple users/machines; want community sharing without copying whole skills.

## Diagnosis
A skill is too coarse to be the sharing unit (engine varies per user). The protocol is too fine to ship alone (needs its keywords). The right unit is a *pack*: a few related P-*.md + their INDEX keyword snippet + provenance.

## Protocol
1. Export: `python scripts/pack.py export <name> P-a.md P-b.md` -> a folder of the protocols + `PACK.md` (provenance) + `INDEX.md` (keyword snippet read from the store INDEX).
2. Publish: `git init` the pack folder and push to a repo (the pack is the marketplace currency).
3. Import: `python scripts/pack.py import <pack-dir> [--dry-run]` merges the P-*.md into `$PROTO_STORE/protocols/`; on a name collision it re-keys trigger-keywords by prefixing the pack name so both can coexist.
4. Validate after import: `protocol_lint.py` on the store, then `preflight.py` replay-match against a representative trace.

## Validation
Lint passes on imported protocols. preflight routes a trace to an imported protocol. No duplicate INDEX entries (collisions are re-keyed, not duplicated).

## Avoid
Don't ship whole skills as the sharing unit -- engine diverges per user. Don't import without `--dry-run` first on an untrusted pack. Don't drop provenance (PACK.md) -- it is how consumers grade confidence.

## Promotion
Encoded in `scripts/pack.py`. This file is the rationale reference and the marketplace-direction spec.