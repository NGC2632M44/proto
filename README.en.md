<div align="center">

# PROTO

### *Learn from every stumble. Turn lived work into the smallest reusable unit — and stop reinventing the wheel.*

[![License: MIT](https://img.shields.io/badge/License-MIT-2d2d2d?style=flat-square)](./LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-161616?style=flat-square)](./agents/openai.yaml)
[![Protocols](https://img.shields.io/badge/Schema-protocol--v1-3a3a3a?style=flat-square)](./references/protocol-schema.md)
[![Python](https://img.shields.io/badge/Linter-py3.7+-3674A5?style=flat-square)](./scripts/protocol_lint.py)
[![Status](https://img.shields.io/badge/Status-stable-1f6f3b?style=flat-square)]()

**English** · [中文](./README.md)

</div>

---

> **Every engineering session leaks value.** The same error is diagnosed three times by three different agents. The same decision tree is rebuilt because nothing recorded *why* a route worked. **PROTO** compresses lived work into the **protocol** — the smallest repeatable unit a future agent can execute without re-reading the original conversation — and only escalates a unit's visibility when its recurrence earns it.

The result is **operational memory**: forward-looking, scoped, validated — not backward-looking narrative. It saves tokens, saves time, and lets experience transfer between agents, machines, and people.

## ✨ The Intent

- **Stop reinventing the wheel** — no pitfall should be stepped in twice; no decision tree should be rebuilt.
- **Learn from every stumble** — failure is the highest-signal event; PROTO turns it into a rule that auto-loads next time.
- **Save tokens & time** — one cheap preflight read beats rediscovering the trap.
- **Value experience** — capture *why* a route worked, so it does not evaporate with the session.
- **Share at the smallest unit** — the protocol is the atom; compose it into skills, or ship it as a pack for the community.

## 🧩 What This Is

PROTO is an **engine that distills work into reusable memory** — not a fixed tool library.

| Unit | Role |
|---|---|
| **protocol** | The smallest unit. One trigger + one reusable action path. A `P-*.md` file, ≤~20 lines. |
| **skill** | An execution interface composing multiple *co-triggered* protocols (`SKILL.md` + `references/` + `scripts/`). |
| **pack** | The sharing unit. A set of `P-*.md` + provenance, publishable as a git repo. |

Key principle: **engine and fuel are separate.** The engine (`SKILL.md` / scripts) is small and stable, installed per runtime; the fuel (`P-*.md` protocols) is the real experience, shared as one library across runtimes.

## ⚙️ Core Mechanisms

| Mechanism | What it does |
|---|---|
| **Preflight** | Before any known-risky operation, spend one cheap read to preload the matching protocol — instead of rediscovering the pitfall. |
| **Collect → Distill** | Collection is always-on and LLM-free (a failed command appends a trace); distillation runs on demand, in batches. |
| **Closed-loop validation** | A distilled protocol must be routable back from the trace that birthed it via preflight — otherwise its trigger-keywords are wrong. |
| **Promotion ladder** | The more evidence, the harder the form: draft → observed → validated → `SKILL.md` rule → script → new skill. |
| **Cross-runtime store** | One canonical store (`~/.protocols`); Claude Code and Codex read the same fuel. |
| **Pack** | Protocols bundle into a portable, publishable unit; keyword collisions are auto-re-keyed on import. |

## 📦 Installation

PROTO ships as a portable skill folder.

**One-command install (recommended, Windows PowerShell)**

```powershell
git clone https://github.com/NGC2632M44/proto.git
cd proto
powershell scripts\install_skill.ps1 -Both      # sync into cc + codex skill roots
powershell scripts\init_store.ps1 -Both         # create ~/.protocols and link both runtimes
powershell scripts\auto_capture_hook.ps1        # install the failed-command auto-capture hook
```

**Lint only (no runtime)**

```bash
git clone https://github.com/NGC2632M44/proto.git
python proto/scripts/protocol_lint.py --self-test
```

Requirements: a Markdown editor and Python 3.7+. Nothing else.

## 🚀 Quick Start

```text
You: Use $proto to extract protocols from this work session and decide what should become a skill.
```

Five operating modes:

| Mode | Action |
|---|---|
| `extract` | Turn logs, chat summaries, diffs, tests, or handoff notes into protocol files. |
| `distill` | Merge, split, or grade existing protocols. |
| `promote` | Decide which protocols belong in `SKILL.md`, `references/`, or `scripts/`. |
| `compose` | Build or update a skill from a set of related protocols. |
| `retrospect` | End a session by capturing repeated errors, decisions, validation, and handoff. |

Read [`references/protocol-schema.md`](./references/protocol-schema.md) before drafting a protocol; run [`scripts/protocol_lint.py`](./scripts/protocol_lint.py) after editing.

## 🗂️ Repository Layout

```
proto/
├── SKILL.md                       # triggers, routing, core workflow, top-priority rules
├── agents/openai.yaml             # Codex discovery interface
├── references/
│   ├── protocol-schema.md         # the grammar every protocol obeys
│   ├── routing.md                 # preflight matching, promotion, auto-compose
│   ├── auto-capture.md            # collect/distill split + closed-loop validation
│   ├── cross-runtime.md           # shared store design and pitfalls
│   └── protocols/                 # the protocol library + INDEX.md routing table
└── scripts/
    ├── preflight.py               # router: operation text → which protocols to read
    ├── protocol_lint.py           # zero-dependency validator + self-test
    ├── collect_trace.py           # LLM-free raw trace collector
    ├── pack.py                    # protocol pack export/import (sharing unit)
    ├── install_skill.ps1          # sync the skill into runtimes
    ├── init_store.ps1             # one-command: build store + link runtimes
    ├── link_store.ps1             # junction each runtime onto the shared store
    ├── auto_capture_hook.ps1      # PowerShell auto-capture hook (install/uninstall)
    ├── sync_store.ps1 / .sh       # cross-machine store sync
    └── publish.ps1                # one-command: sync skill + commit + rebase + push
```

The skill folder contains **no** README, changelog, or install guide — those live at the repo root. The skill folder is the artifact; the repository is its documentation.

## 🔁 One-Command Workflow

No approval channel, no ceremony.

```powershell
# after a change: sync installed skills + push to GitHub
powershell scripts\publish.ps1 -Both -Message "your message"

# on a new machine
powershell scripts\init_store.ps1 -Both
powershell scripts\auto_capture_hook.ps1
```

## ✅ Validation & Lint

`scripts/protocol_lint.py` is zero-dependency and enforces the schema: title shape, `Type`/`Confidence` enums, required `Scope`/`Source`, all seven required sections non-empty, and a guard against raw Windows backslash paths in inline code.

```bash
python scripts/protocol_lint.py references/protocols/   # validate a folder
python scripts/protocol_lint.py --self-test             # built-in self-test
```

A protocol is not ready until the linter is clean **and** a future agent could apply it without the original conversation.

## 🌱 Vision

### Personalized self-iteration

This repository ships only the **engine** and a handful of example protocols. The protocols that actually matter are the ones you stub your toe on in your own work — they iterate with you, learning your environment, your stack, your preferences. So **the protocol library is not synced upstream**: it is your private on-device intelligence, feeding itself. PROTO is designed so the collect → distill → reuse loop is cheap enough to run in the background forever.

### Community & marketplace

The protocol is the atom; the pack is the currency. Imagine:

- **Protocol packs** published like npm packages — "my Windows + proxy + gh pitfall set", "my React performance-tuning path set".
- Consumers import with one `pack.py import`; keyword collisions are auto-re-keyed, never clashing.
- **Skills are personalized compositions**: the same pack set composes into different skills for different workflows.
- Mature protocol groups can solidify into **domain- or tool-specific skills** for public release, while the underlying packs stay re-composable by others.

That way, experience is no longer locked in one head or one session: one person stumbles, the whole community learns. Fewer reinvented wheels; more tokens and time returned to real creation.

## 🔒 Privacy & Conventions

- **No secrets.** Remove project secrets, local absolute paths, personal tokens, and raw conversation history before sharing. Example protocols use placeholders; `protocol_lint.py` rejects raw `C:\` paths in inline code.
- **No environment assumptions** unless they are the point of the protocol.
- **Author identity is GitHub-noreply** to keep commits linkable without exposing a personal email.
- **Uncertainty is first-class.** `draft` / `observed` are legitimate published states; promoting prematurely is the defect, not the hesitation.

If you fork or adapt this skill, run the same privacy pass before publishing.

## 🤝 Contributing

Contributions that **add or harden protocols** (as packs), fix scripts, or improve the schema are welcome. Before a PR:

1. Draft per [`references/protocol-schema.md`](./references/protocol-schema.md).
2. `python scripts/protocol_lint.py <your-file-or-folder>` exits clean.
3. Confirm the protocol is applicable without the original conversation — add context or downgrade confidence if not.
4. Remove local paths, tokens, and environment-specific assumptions.

When protocols conflict, keep both only if each has a distinct context; otherwise prefer the newer validated protocol and record why the older rule is superseded.

## 📄 License

MIT © [NGC2632M44](https://github.com/NGC2632M44). See [`LICENSE`](./LICENSE).

---

<div align="center">

*Learn from every stumble. Every wheel you stop reinventing is time returned to everyone.*

</div>