---
name: proto
description: Extract solved errors, harness pitfalls, debugging paths, implementation paths, project invariants, and handoff lessons into minimal reusable protocols, then compose mature protocols into Codex skills. Use when a user asks to summarize project work into protocols, prevent repeated tool or environment errors, create or improve a meta-skill for producing skills, convert retrospectives into reusable workflows, maintain a protocol library, or decide whether experience should become a protocol, reference, script, or skill.
---

# Proto

Turn lived work into operational memory.

A protocol is the smallest repeatable unit: one error pattern, diagnosis path, implementation route, validation rule, invariant, or handoff recipe. A skill is the execution interface that routes, selects, and applies mature protocols without loading every detail.

## Operating Modes

Choose one mode before writing:

- `extract`: Convert logs, chat summaries, diffs, tests, or handoff notes into protocol files.
- `distill`: Merge, split, or grade existing protocols for clarity and reuse.
- `promote`: Decide which protocols belong in `SKILL.md`, `references/`, or `scripts/`.
- `compose`: Build or update a skill from a set of related protocols.
- `retrospect`: End a work session by capturing repeated errors, decisions, validation, and next-agent handoff.

For protocol files, read `references/protocol-schema.md` before drafting or editing. For mechanical checks, run `scripts/protocol_lint.py` on the protocol files or folder after edits.

## Intake Rules

Collect high-signal traces only:

- Prefer summaries, error snippets, command outputs, diffs, tests, PR comments, and existing protocol folders.
- Sample large projects by directory shape, touched files, tests, and handoff docs. Read source only when a protocol depends on source-level invariants.
- Keep raw logs out of protocol files. Quote only the short error text needed for future recognition.
- Preserve uncertainty. Mark weak evidence as `draft` or `observed` instead of promoting it.

## Extraction Workflow

1. Cluster by trigger.
   Group incidents by visible symptom, user request, command failure, module boundary, or validation need.

2. Split to atomic units.
   One protocol should have one trigger and one reusable action path. If the fix contains independent rules, split it.

3. Assign type and confidence.
   Use the schema types and confidence ladder from `references/protocol-schema.md`.

4. Write the protocol.
   Include symptom, context, diagnosis, steps, validation, avoid list, and promotion decision.

5. Check reuse.
   Ask whether a future agent could apply the protocol without reading the original conversation. Add missing context or downgrade confidence if not.

6. Promote deliberately.
   Put only trigger-critical rules in `SKILL.md`. Put conditional detail in `references/`. Add scripts only for repeated deterministic checks or transformations.

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

When creating a shareable skill, remove project secrets, local absolute paths, personal tokens, raw conversation history, and environment-specific assumptions unless they are the point of the skill.

## Session-End Capture

At the end of substantial work, capture:

1. Top repeated errors or time sinks.
2. Implementation decisions future agents must preserve.
3. Environment and harness constraints.
4. Tests, builds, screenshots, or commands that validated the work.
5. Protocols to draft, merge, promote, or discard.

Prefer a short protocol index plus focused protocol files over one long memoir.

## Output Rules

When asked for protocols, produce concise Markdown following `references/protocol-schema.md`.

When asked for a skill, create or update a valid skill folder with only necessary files. Include `agents/openai.yaml` for discoverable Codex skills. Do not add README, changelog, installation guide, or process notes inside the skill folder.
