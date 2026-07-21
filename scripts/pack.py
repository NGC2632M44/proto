#!/usr/bin/env python3
"""Export/import protocol packs for sharing (the marketplace primitive).

A pack = a folder of P-*.md + a PACK.md manifest (provenance) + an INDEX.md
snippet. Publish the folder as a git repo; consumers import it into their
$PROTO_STORE/protocols/, re-keying trigger-keywords on collision.

Commands:
    python scripts/pack.py export <pack-name> P-foo.md P-bar.md [--desc "..."]
        -> writes <pack-name>/ with the protocols, a PACK.md manifest, and
           an INDEX.md snippet ready to publish.

    python scripts/pack.py import <pack-dir> [--dry-run]
        -> merges the pack's P-*.md into $PROTO_STORE/protocols/ and appends
           their INDEX entries (prefixed with the pack name to avoid keyword
           collisions). --dry-run shows what would change without writing.

Env:
    PROTO_STORE   canonical store (default: ~/.protocols)
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

INDEX_LINE_RE = re.compile(r"^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*[-\u2014\u2013]\s*\[([^\]]*)\](.*)$")


def store_root() -> Path:
    root = os.environ.get("PROTO_STORE")
    if root:
        return Path(root).expanduser()
    return Path.home() / ".protocols"


def parse_index_entry(text: str, name_hint: str | None = None) -> dict | None:
    for line in text.splitlines():
        m = INDEX_LINE_RE.match(line)
        if m:
            fname, file, kws, blurb = m.groups()
            if name_hint and fname.strip() != name_hint:
                continue
            return {
                "name": fname.strip(),
                "file": file.strip(),
                "keywords": [k.strip() for k in kws.split(",") if k.strip()],
                "blurb": blurb.strip(),
                "raw": line,
            }
    return None


def load_store_index() -> dict:
    """Return {name: entry_dict} parsed from the store/INDEX.md (or repo INDEX)."""
    idx = store_root() / "protocols" / "INDEX.md"
    if not idx.is_file():
        idx = Path("references/protocols/INDEX.md")
    if not idx.is_file():
        return {}
    out = {}
    for line in idx.read_text(encoding="utf-8").splitlines():
        m = INDEX_LINE_RE.match(line)
        if m:
            out[m.group(1).strip()] = {"name": m.group(1).strip(), "file": m.group(2).strip(),
                                       "keywords": [k.strip() for k in m.group(3).split(",") if k.strip()],
                                       "blurb": m.group(4).strip(), "raw": line}
    return out

def cmd_export(args) -> int:
    store_idx = load_store_index()
    files: list[Path] = []
    for spec in args.protocols:
        p = Path(spec)
        # resolve against the store protocols dir if not found locally
        if not p.is_file():
            cand = spec if spec.endswith(".md") else spec + ".md"
            p = store_root() / "protocols" / cand
            if not p.is_file():
                p = Path("references/protocols") / cand
        if not p.is_file():
            print(f"not found: {spec}", file=sys.stderr)
            return 1
        files.append(p)
    if not files:
        print("no protocols given", file=sys.stderr)
        return 1

    out = Path(args.out_dir) if args.out_dir else Path(args.name)
    out.mkdir(parents=True, exist_ok=True)
    entries = []
    for src in files:
        dst = out / src.name
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        e = store_idx.get(src.stem) or parse_index_entry(src.read_text(encoding="utf-8"), name_hint=src.stem)
        entries.append(e or {"name": src.stem, "file": src.name, "keywords": [], "blurb": "", "raw": ""})

    # PACK.md manifest (provenance)
    manifest = out / "PACK.md"
    lines = [
        f"# pack: {args.name}",
        f"> exported: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"> source: proto pack",
        f"> count: {len(files)}",
        "",
        "## protocols",
    ]
    for e in entries:
        lines.append(f"- {e['name']} - {e['blurb']}")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # INDEX.md snippet
    idx = out / "INDEX.md"
    ilines = [f"# {args.name} pack -- INDEX snippet", ""]
    for e in entries:
        if e["raw"]:
            ilines.append(e["raw"])
        else:
            kws = ",".join(e["keywords"]) if e["keywords"] else "uncategorized"
            ilines.append(f"- [{e['name']}]({e['file']}) - [{kws}] {e['blurb']}")
    idx.write_text("\n".join(ilines) + "\n", encoding="utf-8")

    print(f"exported pack '{args.name}' -> {out} ({len(files)} protocols)")
    print(f"publish it:  cd {out} && git init && git add -A && git commit -m 'pack: {args.name}' && git push")
    return 0


def cmd_import(args) -> int:
    pack = Path(args.pack_dir)
    if not pack.is_dir():
        print(f"not a directory: {pack}", file=sys.stderr)
        return 1
    pack_index = pack / "INDEX.md"
    pack_name = (pack / "PACK.md").read_text(encoding="utf-8").splitlines()[0].replace("# pack: ", "").strip() if (pack / "PACK.md").is_file() else pack.name

    proto_dir = store_root() / "protocols"
    if not proto_dir.is_dir():
        print(f"store protocols dir missing: {proto_dir} (run init_store first)", file=sys.stderr)
        return 1
    store_index = proto_dir / "INDEX.md"

    # gather protocol files in the pack
    pack_protos = sorted([p for p in pack.glob("P-*.md") if p.is_file()])
    if not pack_protos:
        print(f"no P-*.md files in pack {pack}", file=sys.stderr)
        return 1

    # existing protocol names in the store (for collision re-keying)
    existing = set()
    if store_index.is_file():
        for line in store_index.read_text(encoding="utf-8").splitlines():
            m = INDEX_LINE_RE.match(line)
            if m:
                existing.add(m.group(1).strip())

    plan = []
    for src in pack_protos:
        dst = proto_dir / src.name
        e = parse_index_entry(src.read_text(encoding="utf-8"), name_hint=src.stem)
        action = "add"
        if e and e["name"] in existing:
            # collision: re-key by prefixing pack name into keywords
            new_kws = [pack_name] + e["keywords"]
            action = f"replace (re-key: +{pack_name})"
            e["keywords"] = new_kws
        plan.append((src, dst, e, action))

    if args.dry_run:
        print(f"[dry-run] would import {len(plan)} protocols from pack '{pack_name}':")
        for src, dst, e, action in plan:
            print(f"  {action:30s} {src.name}")
        return 0

    new_index_lines = []
    for src, dst, e, action in plan:
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        if e and e["raw"]:
            # rebuild the INDEX line with possibly re-keyed keywords
            kws = ",".join(e["keywords"])
            new_index_lines.append(f"- [{e['name']}]({e['file']}) \u2014 [{kws}] {e['blurb']}")
    if new_index_lines and store_index.is_file():
        with store_index.open("a", encoding="utf-8") as fh:
            fh.write("\n## imported: " + pack_name + "\n")
            for ln in new_index_lines:
                fh.write(ln + "\n")
    print(f"imported pack '{pack_name}': {len(plan)} protocols into {proto_dir}")
    print("re-run lint + preflight closed-loop to validate:")
    print(f"  python scripts/protocol_lint.py {proto_dir}")
    print(f"  python scripts/preflight.py '<a trace>'")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Export/import protocol packs (sharing primitive).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("export", help="bundle protocols into a publishable pack folder")
    ex.add_argument("name", help="pack name (becomes output dir if --out-dir omitted)")
    ex.add_argument("protocols", nargs="+", help="P-*.md files or bare names from the store")
    ex.add_argument("--out-dir", default=None, help="output directory (default: ./<name>)")
    ex.add_argument("--desc", default="proto pack", help="pack description for PACK.md")
    ex.set_defaults(func=cmd_export)
    im = sub.add_parser("import", help="merge a pack into the shared store")
    im.add_argument("pack_dir", help="directory containing P-*.md + INDEX.md")
    im.add_argument("--dry-run", action="store_true", help="show what would change without writing")
    im.set_defaults(func=cmd_import)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
