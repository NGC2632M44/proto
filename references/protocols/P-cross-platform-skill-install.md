# P-cross-platform-skill-install - One SKILL.md for both Claude Code and Codex
> Type: implementation-path
> Scope: tool:skill
> Confidence: promoted
> Source: protocol-forge cross-platform installation session

## Symptom
A skill works in one runtime but is invisible/malformed in the other (cc: not in available list; codex: missing short description in picker). Or the skill is maintained as two divergent copies.

## Context
Skill folder with `SKILL.md` (frontmatter + body), `agents/openai.yaml`, `references/`, `scripts/`. Two runtimes discover from different roots: `~/.claude/skills/<name>/` and `~/.codex/skills/<name>/`.

## Diagnosis
cc reads frontmatter `name`+`description`. Codex also wants `metadata: short-description` and surfaces via `agents/openai.yaml`. A frontmatter with only `name`/`description` installs in cc but renders incomplete in codex; codex-only `metadata` without `name`/`description` breaks cc routing. The union frontmatter satisfies both; `agents/openai.yaml` is needed by codex and harmless to cc.

## Protocol
1. Frontmatter carries the union:
   ```yaml
   ---
   name: <slug>
   description: <one-paragraph trigger description>
   metadata:
     short-description: <one-line picker label>
   ---
   ```
2. Keep `agents/openai.yaml` with `display_name`, `short_description`, `default_prompt` (`$<name>`).
3. Add a one-line trigger hint at body top: `Trigger with $<name> (Codex) or /<name> (Claude Code)`.
4. Install into both roots by copying the skill folder (minus `.git`, LICENSE, README, .gitignore):
   - `~/.claude/skills/<name>/`
   - `~/.codex/skills/<name>/`
5. Verify each runtime lists the skill.

## Validation
cc: skill in available-skills reminder, `/name` routes. codex: skill in picker with short-description, `$name` routes. `agents/openai.yaml` present in both copies. Two copies byte-identical in skill files.

## Avoid
Don't maintain two frontmatter variants — union is valid for both, divergence rots. Don't copy repo root files (LICENSE/README/.gitignore/.git) into skill dirs — they are repo metadata, and `.git` inside a skills root confuses discovery. Don't omit `agents/openai.yaml` even for cc-only — costs nothing, keeps the skill portable.

## Promotion
Already encoded in proto's own SKILL.md and install procedure. This file is the rationale reference.
