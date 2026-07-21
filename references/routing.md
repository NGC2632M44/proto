# Routing: How Protocols Fire, Promote, and Compose

This reference answers the three operational questions about proto:
1. How does a protocol actually get used (and how is it different from invoking the skill)?
2. How do protocols and the skill upgrade each other?
3. When do accumulated protocols auto-generate a new skill?

## Protocol vs. Skill Invocation

- **Invoking the skill** (`/proto` or `$proto`) runs the *engine*: meta-work — extract, distill, promote, compose, retrospect. You do this when you want to *produce or maintain* protocols/skills. It is expensive and should be rare.
- **A protocol firing** is a *fuel burn*: one stored rule applied to a live operation to prevent a known pitfall. It happens silently during normal work, before the risky action. No skill invocation needed.

The two are decoupled on purpose. You don't call `/proto` to avoid a git-push pitfall; you read one `P-*.md` during preflight. You call `/proto` only to create, merge, or compose protocols.

## How Preflight Matches

Matching is by **trigger-keywords and operation intent**, never by exact text:

1. Read `references/protocols/INDEX.md`. Each entry carries a bracketed keyword set, e.g.:
   `- [P-win-git-push-retry](./P-win-git-push-retry.md) — [push, force-push, 443, schannel, proxy] transient ...`
2. If the current operation touches any keyword (`git push`, a proxy, a 443/schannel error), open that one file.
3. Apply its `Protocol` steps; obey its `Avoid` list.
4. Multiple keyword overlaps → read 1-2 most-specific files only, not the whole folder.
5. No keyword overlap → skip preflight for this operation; proceed, then `extract` if a new pitfall appears.

INDEX is the cheap routing table. Reading the full schema or all protocols every time defeats the purpose. Keep INDEX small and keyword-tagged; the linter does not enforce INDEX format, so maintain it as a discipline.

## Skill ↔ Protocol Upgrade Loop

They reinforce each other in a closed loop:

```
   live work
       │  hits a pitfall
       ▼
   preflight fires (or fails to fire) a P-*.md
       │
       ├── prevented a recurrence → confidence holds/strengthened
       │       │  repeated 3+ times around same trigger
       │       ▼
       │   promote → SKILL.md rule / script / new skill (compose)
       │
       └── pitfall recurred despite protocol → protocol is defective
               │
               ▼
           strengthen trigger-keywords, or demote to draft, or rewrite
```

- **Up**: a validated protocol that keeps preventing recurrences graduates into a `SKILL.md` rule (rule needed before acting) or a `script` (fragile repeated operation with exact checks). Three validated protocols sharing a trigger auto-propose a new skill via `compose`.
- **Down**: when a promoted rule proves wrong or incomplete in live work, demote it back to a draft protocol for re-grading — do not silently patch a skill rule in place. Promotion is reversible; the evidence ladder is the source of truth.

This is how protocols and the skill upgrade each other: protocols feed the skill (promotion), and the skill's rules get pressure-tested by live work (demotion feedback). The loop converges because every recurrence either strengthens a protocol or exposes it as defective.

## When Protocols Auto-Generate a New Skill (Auto-Compose)

Threshold: **≥3 validated protocols sharing a trigger or tool context.**

When the threshold is crossed, run `compose` to draft a candidate skill:

1. Collect the ≥3 validated `P-*.md` files sharing the trigger.
2. Distill each `Protocol` section into the new skill's `SKILL.md` routing rules (terse, trigger-first).
3. Copy the `P-*.md` files into the new skill's `references/` as the long-form rationale.
4. Reuse any shared script; only write a new script if a deterministic check spans ≥2 of the protocols.
5. Add `agents/openai.yaml` (display_name, short_description, default_prompt `$<new-name>`).
6. Output as a **draft** for human review — never auto-publish. Skills are public-facing; composition is a proposal, not a release.
7. Mark the source protocols `Confidence: promoted` and keep INDEX pointing at them as rationale.

Auto-compose is a proposal gate, not an autonomous publish. The human decides whether the draft skill earns a name, a folder, and a push.

## Preflight Discipline (Token Economics)

- Always read INDEX before a known-risky operation. INDEX is one small file; the protocols it routes to are the savings.
- Never read the whole protocols folder or the schema during preflight — only the 1-2 matched files.
- If preflight keeps missing a recurrence, the defect is in the protocol's trigger-keywords or in INDEX, not in the user. Fix the routing, then the protocol.

## Recurrence Accountability

The north star is "never step in the same pit twice." Enforce it:

- When a pitfall recurs, ask first: *did a protocol exist for this?*
- If yes and it didn't fire → fix its trigger-keywords / INDEX entry (routing failure).
- If yes and it fired but the fix didn't work → rewrite the protocol's `Protocol`/`Avoid` (content failure).
- If no protocol existed → `extract` a new one.

A protocol that fails to prevent its own recurrence is itself the bug.
