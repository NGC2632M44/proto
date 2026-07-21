# P-protocol-lint-scope - Lint only protocol files, not schema or prose
> Type: anti-pattern
> Scope: tool:protocol_lint
> Confidence: validated
> Source: protocol-forge linter false-positive session

## Symptom
A protocol linter that validates files against the protocol schema (title shape, `Type`/`Confidence` enums, seven required sections) flags the schema file itself, the rename/etymology note, and the README as malformed protocols:
```
references/protocol-schema.md: Type must be one of ...
references/rename.md: missing or empty section 'Symptom'
references/rename.md: title must look like '# Pslug - Title'
```
The linter exits 1 even though no actual protocol file is broken — it is linting documentation and reference prose as if they were protocols.

## Context
A skill folder where `references/` contains the protocol schema (a template document, not a protocol), prose notes (etymology, explanations), and the actual protocol files (`P-*.md`). The linter walks `*.md` under the target directory.

## Diagnosis
The linter selected files by extension (`.md`) and a coarse "not SKILL.md, not dotfile" filter. That filter admits the schema document, the etymology note, and any README — none of which obey the protocol template, because they are not protocols. The linter then reports their absence of `Type:`/`Symptom`/etc. as defects. The fix is to narrow selection to files whose *name* marks them as protocols, not to relax the schema checks.

## Protocol
1. Gate file selection on the protocol filename convention, not just the extension: a protocol file's name begins with `P-` (e.g. `P-slug.md`). Implement as a regex `^P-[\w.-]+\.md$` (case-insensitive).
2. Explicitly exclude known non-protocol markdown: `SKILL.md`, `README.md`, dotfiles.
3. When no protocol files are found, exit 0 with a clear "No protocol files found (looking for P-*.md)" message — absence of protocols is a valid state, not a lint failure.
4. Keep the per-file schema checks strict. Only the selection scope changes.
5. Preserve the `--self-test` path: it must still pass a synthetic valid protocol and still catch a malformed one.

## Validation
Running the linter over a `references/` folder that contains the schema, prose notes, and README produces "No protocol files found" and exits 0. Dropping a valid `P-*.md` in a `references/protocols/` subfolder and linting that folder reports "Checked N protocol file(s)" and exits 0. A deliberately broken `P-*.md` still reports the specific defect.

## Avoid
Do not fix the false positives by relaxing the schema (e.g. making `Type` optional, dropping section requirements) — that hides real breakage in genuine protocols. Do not hard-code-exclude individual filenames one by one as they appear; name-based selection by the `P-` convention generalises. Do not exit nonzero on "no protocols found"; that turns a clean empty library into a CI red.

## Promotion
Already encoded in `scripts/protocol_lint.py` (`is_protocol_file` + the exit-0-on-empty branch). Keep this protocol as the rationale reference for that decision.
