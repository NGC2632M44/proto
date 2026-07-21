#!/usr/bin/env python3
"""Collect a raw trace into the proto inbox. No LLM, no deps.

A trace is the cheap, always-on half of auto-capture (see
references/auto-capture.md). Distillation into a protocol happens later,
on demand, via `$proto extract`.

Usage:
    python scripts/collect_trace.py "git push" --exit 1 --stderr-file err.txt
    echo "schannel: server closed abruptly" | python scripts/collect_trace.py - --exit 1

Env:
    PROTO_STORE   canonical store dir (default: ~/.protocols)
    PROTO_RUNTIME runtime name for the trace header (default: $PROTO_RUNTIME or "unknown")
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

KNOWN_SIGNALS = [
    r"InputValidationError",
    r"UnicodeDecodeError|codec can''t decode|gbk|GBK",
    r"schannel|port 443",
    r"403|422",
    r"timed out|timeout",
    r"fatal:|not a git repository",
    r"Unable to add remote",
]

SLUG_RE = re.compile(r"[^a-z0-9]+")
MAX_SNIPPET_LINES = 8
MAX_LINE = 2000


def store_root() -> Path:
    root = os.environ.get("PROTO_STORE")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".protocols"


def slugify(text: str) -> str:
    s = SLUG_RE.sub("-", text.strip().lower()).strip("-")
    return (s or "trace")[:40]


def read_snippet(path: "Path | None") -> str:
    if not path or not path.is_file():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    for line in lines:
        if len(line) > MAX_LINE:
            line = line[:MAX_LINE] + "..."
        out.append(line)
        if len(out) >= MAX_SNIPPET_LINES:
            break
    return "\n".join(out)


def classify(text: str) -> list:
    hits = []
    for pat in KNOWN_SIGNALS:
        if re.search(pat, text, re.IGNORECASE):
            hits.append(pat.split("|")[0])
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect a raw trace into the proto inbox.")
    ap.add_argument("operation", nargs="?", default="-", help="Operation text. ''-'' reads stdin.")
    ap.add_argument("--exit", type=int, default=None, help="Exit code of the operation.")
    ap.add_argument("--stderr-file", type=Path, default=None, help="File containing stderr to snippet.")
    ap.add_argument("--cwd", default=os.getcwd(), help="Working dir of the operation.")
    ap.add_argument("--runtime", default=os.environ.get("PROTO_RUNTIME", "unknown"), help="Runtime name.")
    ap.add_argument("--note", default="", help="Optional one-line note.")
    args = ap.parse_args()

    op = sys.stdin.read() if args.operation == "-" else args.operation
    if not op.strip():
        print("collect_trace: empty operation, nothing to collect", file=sys.stderr)
        return 0

    inbox = store_root() / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    snippet = read_snippet(args.stderr_file)
    body = op.strip()
    signals = classify("\n".join([body, snippet]))

    fname = f"{ts}-{slugify(body)}.trace"
    path = inbox / fname

    lines = [
        f"# trace {ts}",
        f"runtime: {args.runtime}",
        f"cwd: {args.cwd}",
    ]
    if args.exit is not None:
        lines.append(f"exit: {args.exit}")
    if signals:
        lines.append(f"signals: {'', ''.join(signals)}")
    if args.note:
        lines.append(f"note: {args.note}")
    lines.append("")
    lines.append("## operation")
    lines.append(body)
    if snippet:
        lines.append("")
        lines.append("## stderr snippet")
        lines.append(snippet)
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"collected: {path}")
    if signals:
        print("suggest: run `$proto extract` when convenient to distill this trace.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
