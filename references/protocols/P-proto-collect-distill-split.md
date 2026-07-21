# P-proto-collect-distill-split - Separate cheap capture from LLM distillation
> Type: implementation-path
> Scope: tool:proto
> Confidence: validated
> Source: protocol-forge auto-capture design session

## Symptom
proto only fires on manual `$proto extract`, so most high-signal pitfalls leak away; always-on LLM summarization to fix this is a token sink and the right moment is unknowable.

## Context
Any coding runtime (Codex/cc). proto''s value depends on lived pitfalls, but capture must not tax the session.

## Diagnosis
Conflating "collect" and "distill" is the bug. Collection is deterministic and near-free; distillation needs the LLM. Split them: collect always-on into an inbox, distill on demand in batches.

## Protocol
1. Collect a raw trace (command, exit, 鈮?8 stderr lines, cwd, runtime, ts) on any cheap signal: nonzero exit, known error regex (InputValidationError, GBK/UnicodeDecodeError, schannel, gh 403/422, timeout), or preflight NO_MATCH-then-fail / recurrence.
2. Write to `$PROTO_STORE/inbox/<ts>-<slug>.trace` via `scripts/collect_trace.py` 鈥?no model call.
3. Distill only on: explicit `$proto extract`, inbox 鈮?N traces (cheap `ls` gate), or session-end `retrospect` with a bounded budget.
4. Drafts start at `Confidence: draft`; must pass `protocol_lint.py` and replay-match (see below); then clear/archive consumed traces.

## Validation
A replayed trace routes to the protocol that distilled it (`preflight.py` matches it). Lint passes. A future agent applies it without the original chat.

## Avoid
Don''t run the LLM on every error 鈥?that is the token sink this protocol prevents. Don''t collect without an inbox cap 鈥?unbounded traces rot. Don''t promote a draft to validated without the closed-loop replay check.

## Promotion
Encoded in `references/auto-capture.md` and `scripts/collect_trace.py`. This file is the rationale reference.
