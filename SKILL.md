---
name: proto
description: Extract solved errors, harness pitfalls, debugging paths, implementation paths, project invariants, and handoff lessons into minimal reusable protocols, then compose mature protocols into Codex skills. Use when a user asks to summarize project work into protocols, prevent repeated tool or environment errors, create or improve a meta-skill for producing skills, convert retrospectives into reusable workflows, maintain a protocol library, or decide whether experience should become a protocol, reference, script, or skill.
metadata:
  short-description: Forge reusable protocols into skills
---

# Proto

Turn lived work into operational memory.

> Trigger with `$proto` (Codex) or `/proto` (Claude Code).
> North star: never step in the same pit twice. A protocol that fails to prevent a recurrence is itself defective — fix the protocol, not just the problem.

The skill is the **engine** (its modes do meta-work: extract, distill, promote, compose, retrospect). A protocol is **fuel** — a stored unit that does nothing until Preflight routes the right one into the current operation. `references/protocols/INDEX.md` is the lookup table; matching is by trigger-keyword and intent, not exact text.

## Preflight — Load Before You Leap

The point of a protocol is to prevent a recurrence, not to document it. Before any known-risky operation, spend one cheap read to preload the matching protocol instead of rediscovering the pitfall. This is where tokens are saved and success rates rise.

Known-risky operations (extend as protocols accumulate): `git push` / `git push --force`, `gh repo create`, linting a new directory, installing a skill into a runtime, rewriting git history, anything over a proxy or involving Windows paths.

1. Read `references/protocols/INDEX.md` (small file).
2. Match on **trigger-keywords and operation intent**, not exact text. An entry tagged `[push, force-push, 443, schannel, proxy]` matches any push on a proxied host.
3. Read only the matching `P-*.md` file(s) — one or two, not the whole folder.
4. Apply its `Protocol` steps; respect its `Avoid` list before acting.
5. No match? Proceed — then capture the new pitfall afterward via `extract`.

If you hit a symptom a protocol already describes, that protocol failed to prevent a recurrence. Strengthen its trigger-keywords or promote it to a `SKILL.md` rule; do not just re-solve the problem. Full procedure in `references/routing.md`.

## Operating Modes

Choose one mode before writing:

- `extract`: Convert logs, chat summaries, diffs, tests, or handoff notes into protocol files.
- `distill`: Merge, split, or grade existing protocols for clarity and reuse.
- `promote`: Decide which protocols belong in `SKILL.md`, `references/`, or `scripts/`.
- `compose`: Build or update a skill from a set of related protocols — or auto-propose one when ≥3 validated protocols share a trigger (see Auto-Compose).
- `retrospect`: End a work session by capturing repeated errors, decisions, validation, and next-agent handoff.

`preflight` is not a mode — it is a rule that runs before any known-risky operation, regardless of mode.

For protocol files, read `references/protocol-schema.md` before drafting or editing. For mechanical checks, run `scripts/protocol_lint.py` on the protocol files or folder after edits.

## Intake Rules

Collect high-signal traces only:

- Prefer summaries, error snippets, command outputs, diffs, tests, PR comments, and existing protocol folders.
- Sample large projects by directory shape, touched files, tests, and handoff docs. Read source only when a protocol depends on source-level invariants.
- Keep raw logs out of protocol files. Quote only the short error text needed for future recognition.
- Preserve uncertainty. Mark weak evidence as `draft` or `observed` instead of promoting it.

## Extraction Workflow

1. **Preflight first.** Before extracting, check INDEX for an existing protocol on the same trigger — extend it instead of creating a duplicate.
2. Cluster by trigger. Group incidents by visible symptom, user request, command failure, module boundary, or validation need.
3. Split to atomic units. One protocol = one trigger + one reusable action path. Split if the fix contains independent rules.
4. Assign type and confidence per `references/protocol-schema.md`.
5. Write terse. Symptom, context, diagnosis, steps, validation, avoid, promotion — 1-3 lines each. See Output Rules.
6. Check reuse. Could a future agent apply it without the original conversation? If not, add context or downgrade confidence.
7. Update INDEX with a one-line entry plus trigger-keyword tags.
8. Promote deliberately. Only trigger-critical rules go in `SKILL.md`; conditional detail in `references/`; scripts only for repeated deterministic checks.

## Promotion Ladder

Use the lightest durable form that solves the recurrence:

| Evidence | Form |
|---|---|
| One unresolved or uncertain incident | Draft protocol |
| One solved incident with clear context | Observed protocol |
| Repeated issue or reproduced fix | Validated protocol |
| Conditional knowledge useful only sometimes | Reference file |
| High-frequency rule needed before acting | `SKILL.md` rule |
| Fragile repeated operation with exact checks | Script |
| Related protocols with stable triggers | New or updated skill |

Promote a protocol into a skill when at least one is true:

- Three or more validated protocols share a user trigger or tool context.
- A project has invariants future agents must preserve across sessions.
- The work repeatedly wastes time because the agent must rediscover the same decision tree.
- A deterministic script plus short routing instructions would save more context than prose.

Do not promote when the evidence is anecdotal, the workaround is likely temporary, or the protocol is only a preference with no repeatable failure mode.

## Composition Rules

Keep the skill entrance small:

- `SKILL.md`: triggers, routing, core workflow, and highest-priority rules.
- `references/`: protocol libraries, examples, matrices, project invariants, and long explanations.
- `scripts/`: deterministic validators, converters, collectors, or migration helpers.
- `assets/`: templates or files copied into outputs, only when needed.

When protocols conflict, keep both only if each has a distinct context. Otherwise prefer the newer validated protocol and record why the older rule is superseded.

**Auto-Compose.** When ≥3 validated protocols share a trigger or tool context, run `compose` to draft a candidate skill: distill their `Protocol` sections into the new `SKILL.md` routing rules; keep the `P-*.md` files as its `references/`; reuse any shared script. Propose as a **draft** for human review — never auto-publish a skill, since skills are public-facing and must be deliberate. Full procedure in `references/routing.md`.

**Demote on feedback.** When a `SKILL.md` rule or script proves wrong or incomplete in practice, demote it back to a draft protocol for re-grading rather than silently editing it. Promotion is reversible; the evidence ladder is the source of truth.

When creating a shareable skill, remove project secrets, local absolute paths, personal tokens, raw conversation history, and environment-specific assumptions unless they are the point of the skill.

## Session-End Capture

At the end of substantial work, capture:

1. Top repeated errors or time sinks.
2. Implementation decisions future agents must preserve.
3. Environment and harness constraints.
4. Tests, builds, screenshots, or commands that validated the work.
5. Protocols to draft, merge, promote, or discard — and any recurrence where a protocol should have fired but didn't.

Prefer a short protocol index plus focused protocol files over one long memoir.

## Output Rules

When asked for protocols, produce concise Markdown following `references/protocol-schema.md`.

When asked for a skill, create or update a valid skill folder with only necessary files. Include `agents/openai.yaml` for discoverable Codex skills. Do not add README, changelog, installation guide, or process notes inside the skill folder.

**Terse by default.** A protocol file is ≤ ~20 lines: 1-3 lines per section, quote only the short error text needed for recognition, no narrative. Compression is a feature — a long protocol costs tokens every time it is preloaded. An `extract` run should produce each protocol in a single pass with no re-reads of source or schema.
