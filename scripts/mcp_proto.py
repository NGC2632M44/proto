#!/usr/bin/env python3
"""Proto MCP server (stdio, on-demand, non-daemon).

Exposes proto's engine as MCP tools so any MCP client (Codex, Claude Code, ...)
can collect traces, run preflight, lint, manage packs, and draft a retrospect
without an interactive shell. The server is launched as a child process by the
MCP client; it is NOT a persistent daemon.

Tools:
    collect_trace    - record a failed operation as a trace in the inbox
    preflight        - route an operation text to the protocol(s) to read
    lint_protocols   - validate protocol files against the schema
    pack_export      - bundle protocols into a publishable pack folder
    pack_import      - merge a pack into the shared store (dry-run supported)
    retrospect       - summarize the inbox into a draft retrospect (counts +
                       clusters; the LLM side stays in the agent, this only
                       gathers the cheap material)
    inbox_status     - report inbox trace count + a one-line cluster hint

Env:
    PROTO_STORE   canonical store (default: ~/.protocols)

The server speaks JSON-RPC 2.0 over stdio (MCP). It implements the minimal
subset: initialize, tools/list, tools/call. No external deps beyond stdlib.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"


def store_root() -> Path:
    root = os.environ.get("PROTO_STORE")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".protocols"


def _run_py(script: str, args: list, env: dict | None = None) -> dict:
    """Run a proto script and capture stdout/stderr/exit."""
    cmd = [sys.executable, str(SCRIPTS / script), *args]
    r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, **(env or {})})
    return {"exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr}


TOOLS = [
    {
        "name": "collect_trace",
        "description": "Record a failed operation as a raw trace in the proto inbox (no LLM). Call this whenever a command exits nonzero or a known error regex matches.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "description": "The command or operation text that failed."},
                "exit_code": {"type": "integer", "description": "Exit code of the operation."},
                "runtime": {"type": "string", "default": "codex", "description": "Runtime name (codex/cc/powershell)."},
                "note": {"type": "string", "description": "Optional one-line note."},
            },
            "required": ["operation"],
        },
    },
    {
        "name": "preflight",
        "description": "Route an operation text to the protocol file(s) to read before acting. Returns the matched P-*.md list.",
        "inputSchema": {
            "type": "object",
            "properties": {"operation": {"type": "string"}},
            "required": ["operation"],
        },
    },
    {
        "name": "lint_protocols",
        "description": "Validate protocol files against the schema. Defaults to the shared store's protocols/.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Folder or file to lint. Default: store protocols/."}},
        },
    },
    {
        "name": "inbox_status",
        "description": "Report the inbox trace count and a one-line cluster hint. Cheap; call before deciding to distill.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "retrospect",
        "description": "Gather cheap material for a session retrospect: inbox status + preflight hits on the latest traces + a draft outline. The LLM synthesis stays in the calling agent.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "pack_export",
        "description": "Bundle protocols into a publishable pack folder (P-*.md + PACK.md + INDEX snippet).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "protocols": {"type": "array", "items": {"type": "string"}},
                "out_dir": {"type": "string"},
            },
            "required": ["name", "protocols"],
        },
    },
    {
        "name": "pack_import",
        "description": "Merge a pack into the shared store, re-keying trigger-keywords on collision. Use dry_run first on untrusted packs.",
        "inputSchema": {
            "type": "object",
            "properties": {"pack_dir": {"type": "string"}, "dry_run": {"type": "boolean", "default": True}},
            "required": ["pack_dir"],
        },
    },
]


def handle_call(name: str, args: dict) -> dict:
    env = {"PROTO_STORE": str(store_root())}
    if name == "collect_trace":
        r = _run_py("collect_trace.py", [args["operation"], "--exit", str(args.get("exit_code", 1)),
                                         "--runtime", args.get("runtime", "codex")], env=env)
        if args.get("note"):
            r2 = _run_py("collect_trace.py", [args["operation"], "--exit", str(args.get("exit_code", 1)),
                                              "--runtime", args.get("runtime", "codex"), "--note", args["note"]], env=env)
            r = r2
        return {"content": [{"type": "text", "text": r["stdout"] or r["stderr"] or "collected"}]}
    if name == "preflight":
        r = _run_py("preflight.py", [args["operation"]], env=env)
        return {"content": [{"type": "text", "text": r["stdout"] or r["stderr"] or "no match"}]}
    if name == "lint_protocols":
        path = args.get("path") or str(store_root() / "protocols")
        r = _run_py("protocol_lint.py", [path])
        return {"content": [{"type": "text", "text": r["stdout"] or r["stderr"]}]}
    if name == "inbox_status":
        inbox = store_root() / "inbox"
        traces = sorted(inbox.glob("*.trace")) if inbox.is_dir() else []
        n = len(traces)
        # cheap cluster hint: most common leading token in operation lines
        from collections import Counter
        heads = Counter()
        for t in traces[:50]:
            for line in t.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("## operation"):
                    idx = traces[:50].index(t)
                    try:
                        nxt = t.read_text(encoding="utf-8", errors="replace").splitlines()
                        op = nxt[nxt.index(line) + 1] if line in nxt else ""
                        heads[op.split()[0]] += 1 if op.split() else 0
                    except Exception:
                        pass
                    break
        hint = ", ".join(f"{k}({v})" for k, v in heads.most_common(3)) or "n/a"
        gate = "READY to distill" if n >= 10 else "accumulate"
        return {"content": [{"type": "text", "text": f"inbox: {n} traces ({gate}). clusters: {hint}"}]}
    if name == "retrospect":
        inbox = store_root() / "inbox"
        traces = sorted(inbox.glob("*.trace")) if inbox.is_dir() else []
        lines = [f"# Retrospect material (gathered by MCP, {len(traces)} traces)", "",
                 "## inbox traces", f"count: {len(traces)}", "READY to distill" if len(traces) >= 10 else "accumulate", ""]
        for t in traces[:20]:
            txt = t.read_text(encoding="utf-8", errors="replace")
            op = ""
            for i, ln in enumerate(txt.splitlines()):
                if ln.startswith("## operation"):
                    op = txt.splitlines()[i + 1] if i + 1 < len(txt.splitlines()) else ""
                    break
            lines.append(f"- {t.name}: {op}")
        lines += ["", "## suggested steps for the agent",
                  "1. cluster the above traces by trigger",
                  "2. for each cluster draft a P-*.md (<=20 lines) per protocol-schema",
                  "3. lint + replay-match each draft against its trace via preflight",
                  "4. downgrade any draft not hit by preflight"]
        return {"content": [{"type": "text", "text": "\n".join(lines)}]}
    if name == "pack_export":
        out = ["export", args["name"], *args["protocols"]]
        if args.get("out_dir"):
            out += ["--out-dir", args["out_dir"]]
        r = _run_py("pack.py", out, env=env)
        return {"content": [{"type": "text", "text": r["stdout"] or r["stderr"]}]}
    if name == "pack_import":
        out = ["import", args["pack_dir"]]
        if args.get("dry_run", True):
            out += ["--dry-run"]
        r = _run_py("pack.py", out, env=env)
        return {"content": [{"type": "text", "text": r["stdout"] or r["stderr"]}]}
    return {"content": [{"type": "text", "text": f"unknown tool: {name}"}]}


def main() -> int:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method")
        mid = msg.get("id")
        if method == "initialize":
            resp = {"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "proto", "version": "0.1.0"},
                    "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
        elif method == "tools/call":
            result = handle_call(msg["params"]["name"], msg["params"].get("arguments", {}))
            resp = {"jsonrpc": "2.0", "id": mid, "result": result}
        elif method == "notifications/initialized":
            continue
        else:
            resp = {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())