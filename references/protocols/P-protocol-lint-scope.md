# P-protocol-lint-scope - Lint only protocol files, not schema or prose
> Type: anti-pattern
> Scope: tool:protocol_lint
> Confidence: promoted
> Source: protocol-forge linter false-positive session

## Symptom
A protocol linter validating against the schema flags the schema file, prose notes, and README as malformed protocols (`Type must be one of ...`, `missing section 'Symptom'`, `title must look like '# Pslug - Title'`). Exits 1 though no real protocol is broken.

## Context
Skill folder where `references/` holds the schema (a template, not a protocol), prose notes, and real `P-*.md` files. Linter walks `*.md` under the target dir.

## Diagnosis
Selection was by extension + a coarse "not SKILL.md, not dotfile" filter, which admits the schema, etymology note, and README — none obey the protocol template. The fix is to narrow selection to files whose *name* marks them as protocols, not to relax the schema checks.

## Protocol
1. Gate selection on the `P-` filename convention: regex `^P-[\w.-]+\.md$` (case-insensitive).
2. Explicitly exclude non-protocol markdown: `SKILL.md`, `README.md`, dotfiles.
3. No protocols found → exit 0 with "No protocol files found (looking for P-*.md)". Absence is valid, not failure.
4. Keep per-file schema checks strict; only scope changes.
5. `--self-test` must still pass a valid synthetic protocol and catch a malformed one.

## Validation
Linting a `references/` with schema/prose/README → "No protocol files found", exit 0. Dropping a valid `P-*.md` into `references/protocols/` → "Checked N protocol file(s)", exit 0. A broken `P-*.md` still reports the specific defect.

## Avoid
Don't relax the schema (optional `Type`, dropped sections) — hides real breakage. Don't exclude filenames one-by-one as they appear — `P-` convention generalizes. Don't exit nonzero on "no protocols found" — turns a clean empty library into CI red.

## Promotion
Already encoded in `scripts/protocol_lint.py` (`is_protocol_file` + exit-0-on-empty). This file is the rationale reference.
