<div align="center">

# PROTO

### *The First Glue* — distilling high-entropy engineering context into deterministic, on-device automation.

[![License: MIT](https://img.shields.io/badge/License-MIT-2d2d2d?style=flat-square)](./LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-161616?style=flat-square)](./agents/openai.yaml)
[![Protocols](https://img.shields.io/badge/Schema-protocol--v1-3a3a3a?style=flat-square)](./references/protocol-schema.md)
[![Python](https://img.shields.io/badge/Linter-py3.11-3674A5?style=flat-square)](./scripts/protocol_lint.py)
[![Status](https://img.shields.io/badge/Status-stable-1f6f3b?style=flat-square)]()

</div>

---

> **prōtokollon** *(πρωτόκολλον)* — *prōtos* (first) + *kolla* (glue).
> The flyleaf pasted onto the front of a papyrus scroll: not the body of the text, but the certificate of authenticity, the summary, and the parsing contract for everything that follows.

**PROTO** is not a tool. It is the **grammar and infrastructure** by which chaotic, high-entropy engineering context — logs, chat, diffs, handoff notes, harness failures — is distilled, parsed, and sealed into **low-entropy, on-device automation units**. Each unit is a *protocol*: the smallest repeatable unit of operational memory. Mature protocols compose into *skills*: the execution interface that routes, selects, and applies them without reloading their history.

This repository is the canonical skill package: a single self-contained folder you can drop into a Codex skills directory, an agent workspace, or a CI checklist — and immediately start turning lived work into durable, reusable procedure.

---

## Table of Contents

- [1. Motivation](#1-motivation)
- [2. Etymology & System Mapping](#2-etymology--system-mapping)
- [3. Architecture](#3-architecture)
- [4. The Protocol as an Atomic Unit](#4-the-protocol-as-an-atomic-unit)
- [5. Installation](#5-installation)
- [6. Quick Start](#6-quick-start)
- [7. Lifecycle: Intake → Extract → Distill → Promote → Compose](#7-lifecycle-intake--extract--distill--promote--compose)
- [8. Validation & Linting](#8-validation--linting)
- [9. Repository Layout](#9-repository-layout)
- [10. Conventions & Privacy](#10-conventions--privacy)
- [11. Contributing](#11-contributing)
- [12. License](#12-license)

---

## 1. Motivation

Every engineering session leaks value. The same error is diagnosed three times by three different agents. The same decision tree is rebuilt because nothing recorded *why* a route worked. The same fragile shell command is re-derived from memory, then subtly mis-transcribed, then breaks in production.

The conventional answer is *more documentation*. PROTO rejects that. A retrospective is prose about the past; prose cannot be routed, selected, or applied. PROTO instead compresses experience into **the smallest repeatable unit that a future agent can execute without reading the original conversation** — and only escalates a unit's visibility when its recurrence earns it.

The result is **operational memory**: forward-looking, scoped, and validated, not backward-looking narrative.

## 2. Etymology & System Mapping

> *In classical antiquity, prōtokollon denoted the flyleaf pasted onto the front of a papyrus scroll. This page carried no body text. It provided the official certificate of authenticity, a content summary, and the parsing contract for the scroll. It was the system's first drop of glue: without it, everything that followed lost its legitimacy and its reading baseline.*

PROTO occupies the identical role in the engineering stack. It executes no business logic — no "body text," no Skill. It is the **a priori contract** by which the system distills, parses, and seals high-entropy context into low-entropy, on-device automation.

| Classical *prōtokollon* | PROTO engineering role |
|---|---|
| The flyleaf, pasted first | The skill's entry surface (`SKILL.md`) |
| Certificate of authenticity | The **Validation** field — how success is confirmed |
| Content summary | Trigger, scope, and promotion ladder |
| Parsing contract | The **protocol-schema** — the grammar every unit obeys |
| The first drop of glue | The binding between chaotic context and deterministic action |

PROTO is named to make explicit that this project establishes the **underlying grammar and infrastructure** of on-device intelligent automation. Every subsequently derived Skill instance and SOP orchestration is founded upon this contract.

## 3. Architecture

```
                        ┌─────────────────────────────────────┐
   high-entropy         │           INTAKE                    │
   context (logs,      │  sample by shape; keep traces only │  →  protocol drafts
   chat, diffs,        └─────────────────────────────────────┘
   handoff)                              │
                                         ▼
                        ┌─────────────────────────────────────┐
                        │          EXTRACT                    │
                        │  cluster → split → type → write     │  →  atomic protocols
                        └─────────────────────────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                   ┌──────────────────┐  ┌──────────────────────┐
                   │   DISTILL         │  │   PROMOTE             │
                   │ merge / split /  │  │ draft → observed →    │
                   │ grade for clarity│  │ validated → promoted  │
                   └──────────────────┘  └──────────────────────┘
                                         │
                                         ▼
                        ┌─────────────────────────────────────┐
                        │          COMPOSE                    │
                        │  route, select, apply without        │  →  skill package
                        │  reloading history                   │
                        └─────────────────────────────────────┘
```

The package is deliberately **small and self-contained**: one `SKILL.md`, a `references/` library, and a `scripts/` validator. No build step. No runtime dependencies. The skill's entrance is the only thing that must stay small — everything else is promoted *out* of it on demand.

## 4. The Protocol as an Atomic Unit

A protocol is the smallest repeatable unit: **one error pattern, one diagnosis path, one implementation route, one validation rule, one invariant, or one handoff recipe.** It carries its own trigger, scope, diagnosis, action path, validation check, and avoid-list — enough for a future agent to apply it without the original conversation.

The full grammar lives in [`references/protocol-schema.md`](./references/protocol-schema.md). The shape, in brief:

```markdown
# P{slug} - {title}
> Type: harness-error | tool-contract | environment | debugging-path
>      | implementation-path | validation | handoff | project-invariant | anti-pattern
> Scope: global | tool:{name} | project:{name} | repo:{path}
> Confidence: draft | observed | validated | promoted
> Source: {conversation, log, file, project, PR, test run}

## Symptom       What the user or agent sees.
## Context       When this applies — OS, shell, tool, version, repo.
## Diagnosis     Why the issue happened, or why this route worked.
## Protocol      Repeatable steps or rules. Imperative.
## Validation    How to confirm success next time.
## Avoid         False fixes and conditions where this does not apply.
## Promotion     Keep as draft | reference | SKILL.md | script | merge.
```

## 5. Installation

PROTO ships as a portable skill folder. Drop it into your skills directory.

**Codex / agent workspaces**
```bash
# from your skills root
cp -r proto/ "$SKILLS_DIR/proto/"
```

**Standalone (lint any protocol folder)**
```bash
git clone https://github.com/NGC2632M44/proto.git
python proto/scripts/protocol_lint.py --self-test
```

Requirements: a Markdown editor and Python 3.7+ for the linter. Nothing else.

## 6. Quick Start

```text
You: Use $proto to extract protocols from this work session and decide what should become a skill.
```

PROTO selects one of five operating modes before writing:

| Mode | Action |
|---|---|
| `extract` | Convert logs, chat summaries, diffs, tests, or handoff notes into protocol files. |
| `distill` | Merge, split, or grade existing protocols for clarity and reuse. |
| `promote` | Decide which protocols belong in `SKILL.md`, `references/`, or `scripts/`. |
| `compose` | Build or update a skill from a set of related protocols. |
| `retrospect` | End a work session by capturing repeated errors, decisions, validation, and handoff. |

For protocol files, read [`references/protocol-schema.md`](./references/protocol-schema.md) before drafting. For mechanical checks, run [`scripts/protocol_lint.py`](./scripts/protocol_lint.py) after edits.

## 7. Lifecycle: Intake → Extract → Distill → Promote → Compose

**Intake** collects high-signal traces only: summaries, error snippets, command outputs, diffs, tests, PR comments. Raw logs stay out of protocol files — quote only the short error text needed for future recognition. Uncertainty is preserved: weak evidence is marked `draft` or `observed`, never promoted on faith.

**Extract** clusters by trigger, splits to atomic units (one trigger, one reusable action path), assigns type and confidence, then writes the protocol and asks the reuse question: *could a future agent apply this without reading the original conversation?* If not, add context or downgrade confidence.

**Distill** merges protocols that share trigger, context, fix, and validation; splits those that bundle multiple triggers; and downgrades confidence when evidence depends on memory or one-off local state.

**Promote** uses the lightest durable form that solves the recurrence:

| Evidence | Form |
|---|---|
| One unresolved or uncertain incident | Draft protocol |
| One solved incident with clear context | Observed protocol |
| Repeated issue or reproduced fix | Validated protocol |
| Conditional knowledge useful only sometimes | Reference file |
| High-frequency rule needed before acting | `SKILL.md` rule |
| Fragile repeated operation with exact checks | Script |
| Related protocols with stable triggers | New or updated skill |

**Compose** keeps the skill entrance small: trigger-critical rules in `SKILL.md`, conditional detail in `references/`, deterministic checks in `scripts/`, templates in `assets/` only when needed.

## 8. Validation & Linting

`scripts/protocol_lint.py` is a zero-dependency validator. It enforces the schema: title shape, `Type`/`Confidence` enums, presence of `Scope` and `Source`, all seven required sections non-empty, and a guard against raw Windows backslash paths in inline code.

```bash
# validate one file or a whole folder
python scripts/protocol_lint.py references/protocols/

# built-in self-test
python scripts/protocol_lint.py --self-test
```

A protocol is *not* ready until the linter is clean **and** a future agent could apply it without the original conversation.

## 9. Repository Layout

```
proto/
├── SKILL.md                       # triggers, routing, core workflow, top-priority rules
├── LICENSE                        # MIT
├── README.md                      # this document
├── .gitignore
├── agents/
│   └── openai.yaml                # Codex discovery interface
├── references/
│   ├── protocol-schema.md         # the grammar every protocol obeys
│   └── rename.md                  # etymology note (Proto — The First Glue)
└── scripts/
    └── protocol_lint.py           # zero-dependency protocol validator + self-test
```

The skill folder intentionally contains **no** README, changelog, installation guide, or process notes inside itself — those live here at the repository root, per the skill-package convention. The skill folder is the artifact; the repository is its documentation.

## 10. Conventions & Privacy

- **No secrets.** The skill is authored to remove project secrets, local absolute paths, personal tokens, and raw conversation history before sharing. Example protocols use placeholder names; `protocol_lint.py` rejects raw `C:\` paths in inline code.
- **No environment assumptions** unless they are the point of the protocol.
- **Author identity is GitHub-noreply** to keep commits linkable without exposing a personal email.
- **Uncertainty is a first-class field.** `draft` and `observed` are legitimate, published states — promoting them prematurely is the defect, not the hesitation.

If you fork or adapt this skill, run the same privacy pass before publishing your own version.

## 11. Contributing

Contributions that **add or harden protocols** are welcome. Before opening a PR:

1. Draft or edit under [`references/protocol-schema.md`](./references/protocol-schema.md).
2. `python scripts/protocol_lint.py <your-file-or-folder>` must exit clean.
3. Confirm the protocol is applicable without the original conversation — add context or downgrade confidence if not.
4. Remove any local paths, tokens, or environment-specific assumptions.

When protocols conflict, keep both only if each has a distinct context; otherwise prefer the newer validated protocol and record why the older rule is superseded.

## 12. License

MIT © [NGC2632M44](https://github.com/NGC2632M44). See [`LICENSE`](./LICENSE).

---

<div align="center">

*PROTO is the first drop of glue between chaotic context and deterministic action.*

</div>
