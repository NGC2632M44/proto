# Protocol Schema

Use this file when drafting, reviewing, or normalizing protocol files.

## Required Template

```markdown
# P{number-or-slug} - {title}
> Type: harness-error | tool-contract | environment | debugging-path | implementation-path | validation | handoff | project-invariant | anti-pattern
> Scope: global | tool:{name} | project:{name} | repo:{path}
> Confidence: draft | observed | validated | promoted
> Source: {conversation, log, file, project, PR, test run}

## Symptom
What the user or agent sees. Include short recognizable errors.

## Context
When this applies. Include OS, shell, tool, API, framework, module, version, or repo when relevant.

## Diagnosis
Why the issue happened, or why this route worked.

## Protocol
Repeatable steps or rules. Use imperative instructions.

## Validation
How to confirm success next time.

## Avoid
False fixes, tempting wrong moves, and conditions where this protocol does not apply.

## Promotion
Keep as draft | add to reference | add to SKILL.md | turn into script | merge with {protocol}
```

## Field Guidance

`Type` selects the reuse shape:

- `harness-error`: Tool invocation, sandbox, shell, encoding, JSON, or connector failure.
- `tool-contract`: API or CLI semantics such as flags, payloads, pagination, or auth behavior.
- `environment`: OS, shell, path, dependency, locale, process, or network condition.
- `debugging-path`: Ordered diagnosis that avoids chasing the wrong subsystem.
- `implementation-path`: Repeatable project build route or architectural move.
- `validation`: Test, build, smoke check, or artifact verification pattern.
- `handoff`: Minimum state transfer for the next agent or session.
- `project-invariant`: Rule that must stay true for project compatibility.
- `anti-pattern`: A known bad fix or strategy to avoid.

`Confidence` controls promotion:

- `draft`: Plausible but not proven.
- `observed`: Solved once with clear context.
- `validated`: Reproduced, tested, or seen repeatedly.
- `promoted`: Already encoded in `SKILL.md`, a reference, or a script.

## Quality Bar

A protocol is ready when a future agent can apply it without reading the original chat.

It must have:

- A visible trigger.
- A scoped context.
- A causal diagnosis or decision rationale.
- A concrete action path.
- A validation check.
- An avoid list when the failure came from a tempting mistake.

## Compression Rules

Split when one note has multiple triggers, tools, or validation paths.

Merge when protocols share the same trigger, context, fix, and validation.

Downgrade confidence when the protocol depends on memory, missing logs, or a one-off local state.

Promote only the rule, not the story. Keep narrative evidence in references or source notes.

## Naming

Use stable names:

- `P-win-json-path.md`
- `P-gh-api-contents-upload.md`
- `P-memex-search-latency.md`
- `P-project-handoff-minimum.md`

Use numbers only when the user already has an ordered protocol series.

## Example: Harness Error

```markdown
# P-win-json-path - Windows paths break JSON tool params
> Type: harness-error
> Scope: global
> Confidence: validated
> Source: repeated tool failures

## Symptom
Tool calls fail with `InputValidationError` when a Windows path appears in a JSON argument.

## Context
Windows paths inside tool parameters, especially `C:/Users/...` (use forward slashes everywhere).

## Diagnosis
Single backslashes are parsed as JSON escapes such as `\U`.

## Protocol
Use forward slashes in all tool parameters: `C:/Users/name/project`. If native backslashes are required inside code, construct them inside the script with `chr(92)` or escape them as `\\`.

## Validation
The same tool call parses and reaches the shell or file operation.

## Avoid
Do not paste raw backslash-prefixed paths into JSON strings.

## Promotion
Add the short rule to `SKILL.md`; keep details in `references/windows-harness.md`.
```

## Example: Project Implementation Path

```markdown
# P-search-latency - Reduce retrieval latency
> Type: implementation-path
> Scope: project:MEMEX2.0
> Confidence: validated
> Source: protocol notes and tests

## Symptom
Search feels slow and vector database queries are suspected.

## Context
Retrieval pipeline with intent classification, vector lookup, reranking, and expansion.

## Diagnosis
Profile by stage before optimizing. In the observed project, latency was mostly in LLM intent classification and reranking, not vector lookup.

## Protocol
Replace query-time LLM intent classification with a fast rule-based classifier plus cache. Limit collection search by target domain. Parallelize independent collection queries. Truncate reranker inputs and cap candidates before reranking.

## Validation
Record per-stage timings before and after. Keep retrieval behavior tests green.

## Avoid
Do not rewrite the vector store first without timing evidence.

## Promotion
Keep in a project implementation reference; promote only if future projects reuse the same retrieval architecture.
```
