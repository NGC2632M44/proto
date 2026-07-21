# P-win-ps-setcontent-utf8-bom - Windows PowerShell Set-Content writes a UTF-8 BOM
> Type: harness-error
> Scope: tool:powershell
> Confidence: validated
> Source: protocol-forge authoring session (2026-07-21)

## Symptom
A Markdown or Python file written with `Set-Content -Encoding utf8` in Windows PowerShell 5.x starts with a `\ufeff` BOM. Downstream readers using `encoding="utf-8"` see the BOM as the first character, so `^#` regexes fail and `protocol_lint.py` reports `title must look like '# Pslug - Title'` on a correctly-titled file.

## Context
Authoring `P-*.md`, `SKILL.md`, or `.py` files on Windows via PowerShell 5.1 (the default `powershell.exe`). Any tool that opens the file with Python's `utf-8` codec (not `utf-8-sig`) inherits the BOM as a literal char. PowerShell 7+ (`pwsh`) does not add a BOM by default.

## Diagnosis
`Set-Content -Encoding utf8` in PS 5.x emits a 3-byte BOM (`EF BB BF`). `Get-Content`/regex matching that go through the same pipeline can also mangle em-dashes. The file looks correct in an editor but the leading `\ufeff` breaks `^`-anchored matching.

## Protocol
1. Prefer `[System.IO.File]::WriteAllText($path, $content)` or `WriteAllLines` -- no BOM, no re-encoding of non-ASCII.
2. In PS 6+, `-Encoding utf8NoBOM` is explicit and safe.
3. If a BOM already exists, strip it: read bytes, drop `EF BB BF` prefix if present, write back with `WriteAllBytes`.
4. When editing files by string replace, read/write via `[IO.File]::ReadAllText`/`WriteAllText` to avoid re-introducing a BOM.

## Validation
`python -c "print(repr(open('file').read()[:3]))"` shows no `'\ufeff'`. `protocol_lint.py` passes on the title. `^#` regex matches.

## Avoid
Do not use `Set-Content -Encoding utf8` on PS 5.x for files consumed by `utf-8` readers. Do not assume "looks right in the editor" means "parses right". Do not fix the symptom by loosening the regex (e.g. `^\ufeff?`) -- strip the BOM at the source.

## Promotion
Keep as a validated protocol. Pair with `P-proto-collect-distill-split` (this is exactly the kind of cheap-signal pitfall auto-capture should collect).