# Auto-Capture: Collect Cheaply, Distill on Demand

Problem: `$proto extract` is manual and expensive (LLM, time, tokens). If capture only happens on explicit invocation, most high-signal pitfalls leak away. But always-on LLM summarization is a token sink and the "right moment" is unknowable.

Solution: **split collect (cheap, always-on, no LLM) from distill (LLM, on-demand, batched).**

## Collect (deterministic, ~free)

Collect a raw *trace* 鈥?not a protocol 鈥?whenever a cheap signal fires. A trace is just: operation text, exit code, an stderr snippet (鈮?8 lines), cwd, runtime, timestamp. No LLM.

Capture triggers, cheapest first:

1. **No-match-then-fail.** Preflight returned `NO_MATCH` and the operation failed (nonzero exit). Highest signal: a pitfall with no existing protocol.
2. **Recurrence.** Preflight fired a protocol and the pitfall still bit. The protocol is defective 鈥?capture the trace so `extract` can strengthen it.
3. **Error-signature watch.** Nonzero exit, or stderr matching a known-signal regex: `InputValidationError`, `UnicodeDecodeError`/`GBK`, `schannel`, `403`/`422` from `gh`, `timed out`/`port 443`, `Unable to add remote`. The agent (or a shell trap) appends one trace file per hit.

Collector: `scripts/collect_trace.py` writes `$PROTO_STORE/inbox/<ts>-<slug>.trace`. Dependency-free; safe to call from any runtime's tooling or a shell `trap`.

## Distill (LLM, on-demand)

Run `$proto extract` on the inbox only when:

- the user explicitly asks, **or**
- `inbox/` exceeds a threshold (e.g. 10 traces) 鈥?a cheap `ls | wc` gate, no LLM, **or**
- session-end `retrospect` with a bounded token budget.

Distillation batches the inbox: cluster by trigger, draft one `P-*.md` per cluster, then **clear or archive** the consumed traces. Drafts start at `Confidence: draft`.

## Validity gate (the closed loop)

A distilled protocol is only "effective" if it survives three checks 鈥?writing it is not enough:

1. `protocol_lint.py` passes (schema + required sections).
2. The "future agent can apply it without the original chat" test (Intake rule).
3. **Replay match:** `preflight.py` run on the captured trace text routes to the protocol that distilled it. The trace that birthed a protocol must be able to find it again 鈥?otherwise its trigger-keywords are wrong and it will never fire.

If check 3 fails, the fix is in the protocol's trigger-keywords / INDEX entry, not the trace. This is what makes the library *effective* rather than merely written.

## Why this works

- Collect costs near-zero: a filesystem append, no model call. It can be always-on without taxing the session.
- Distill is rare and batched, so the LLM cost is amortized across many traces.
- The closed loop (trace -> protocol -> preflight must re-match that trace) is the validity guarantee, not the author's good intentions.
