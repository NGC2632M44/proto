# P-cross-platform-skill-install - One SKILL.md for both Claude Code and Codex
> Type: implementation-path
> Scope: tool:skill
> Confidence: validated
> Source: protocol-forge cross-platform installation session

## Symptom
A skill works in one runtime but is invisible or malformed in the other. In Claude Code the skill does not appear in the available-skills list; in Codex it lacks the short description shown in the picker. Or: the same skill is maintained as two divergent copies, one per runtime.

## Context
A skill folder with `SKILL.md` (frontmatter + body), `agents/openai.yaml`, `references/`, `scripts/`. The two runtimes discover skills from different roots:
- Claude Code: `~/.claude/skills/<name>/SKILL.md`
- Codex: `~/.codex/skills/<name>/SKILL.md`

## Diagnosis
The two runtimes share the `SKILL.md` frontmatter `name` + `description` (Claude Code reads these) but Codex also expects a `metadata: short-description` field and surfaces skills via `agents/openai.yaml`. A SKILL.md with only `name`/`description` installs fine in Claude Code but renders incompletely in Codex; a Codex-only `metadata` block without `name`/`description` breaks Claude Code routing. The fix is one frontmatter that carries both, plus the shared `agents/openai.yaml` for Codex discoverability. No runtime requires the other's exclusive files.

## Protocol
1. Frontmatter carries the union, not a subset:
   ```yaml
   ---
   name: <slug>
   description: <one-paragraph trigger description>
   metadata:
     short-description: <one-line picker label>
   ---
   ```
2. Keep `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt` (the `$<name>` trigger) — Codex needs it; Claude Code ignores it harmlessly.
3. Add a one-line trigger hint at the top of the body so users know the invocation token differs by runtime: `Trigger with $<name> (Codex) or /<name> (Claude Code)`.
4. Install into both roots by copying the skill folder (minus `.git`, LICENSE, README, .gitignore) into each:
   - `~/.claude/skills/<name>/`
   - `~/.codex/skills/<name>/`
5. Verify in each runtime that the skill appears in its available-skills list / picker.

## Validation
In Claude Code, the skill name appears in the available-skills system reminder and `/name` routes to it. In Codex, the skill appears in the picker with the short-description label and `$name` routes to it. `agents/openai.yaml` is present in both install copies. The two install copies are byte-identical in their skill files.

## Avoid
Do not maintain two frontmatter variants; the union is valid for both runtimes and divergence will rot. Do not copy the repo root files (LICENSE, README, .gitignore, .git) into the skill install dirs — they are repo metadata, not skill content, and a `.git` folder inside a skills root confuses discovery. Do not omit `agents/openai.yaml` even when targeting only Claude Code; it costs nothing and keeps the skill portable.

## Promotion
Already encoded in the proto skill's own SKILL.md and install procedure. Keep as the reference rationale for the cross-platform frontmatter shape and the install-copy rule.
