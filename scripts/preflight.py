#!/usr/bin/env python3
"""Preflight router: print which protocol file(s) to read for an operation.

Given the operation text (free-form, e.g. a command or error message), scan
references/protocols/INDEX.md for bracketed keyword sets and print the matching
P-*.md file(s). Cheaper than loading the whole protocols folder or the schema.

Usage:
    python scripts/preflight.py "git push --force origin main"
    python scripts/preflight.py "schannel: server closed abruptly"
    echo "gh repo create --remote=origin" | python scripts/preflight.py -
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


INDEX_RE = re.compile(
    r"^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*[-\u2014\u2013]\s*\[([^\]]*)\](.*)$"
)

# Generic words that appear in many operations and must NOT trigger a match
# on their own. A keyword that is only these (or a single short generic word)
# is "weak"; a match requires at least one "strong" keyword.
STOPWORDS = {
    "origin", "install", "remote", "push", "pull", "skill", "main", "commit",
    "file", "metadata", "frontmatter", "claude", "codex", "windows", "public",
    "initial", "repo", "branch", "config", "run", "build", "test", "lint",
    "force", "git", "gh", "error", "fail", "failure", "timeout", "proxy",
}

_SEP_RE = re.compile(r"[-_\s]+")


def normalize(s: str) -> str:
    """Collapse hyphens/underspaces/whitespace to a single space, lowercase."""
    return _SEP_RE.sub(" ", s).strip().lower()


def is_strong_keyword(kw: str) -> bool:
    """A keyword is 'strong' (eligible to trigger) if it is multi-token after
    normalization, contains a digit, or is >=6 chars and not a generic stopword.
    Single short generic words (origin, install, remote, push, skill) are weak
    and only count as tiebreakers, never as the sole trigger."""
    k = kw.lower()
    if " " in normalize(k):
        return True
    if any(ch.isdigit() for ch in k):
        return True
    if len(k) >= 6 and k not in STOPWORDS:
        return True
    return False


def load_index(index_path: Path) -> list[dict]:
    """Parse INDEX.md into [{name, file, keywords[], blurb}]."""
    if not index_path.is_file():
        return []
    entries: list[dict] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m = INDEX_RE.match(line)
        if not m:
            continue
        name, file, kws, blurb = m.groups()
        keywords = [k.strip().lower() for k in kws.split(",") if k.strip()]
        entries.append(
            {
                "name": name.strip(),
                "file": file.strip(),
                "keywords": keywords,
                "blurb": blurb.strip(),
            }
        )
    return entries


def match(op_text: str, entries: list[dict]) -> list[dict]:
    """Return entries with at least one STRONG keyword matching the operation.
    Matching normalizes hyphens/space/underscore so 'gh-repo-create' matches
    'gh repo create'. Weak/generic keywords never trigger a match alone."""
    hay = normalize(op_text)
    hits = []
    for e in entries:
        matched = False
        for kw in e["keywords"]:
            if not kw:
                continue
            if not is_strong_keyword(kw):
                continue
            if normalize(kw) in hay:
                matched = True
                break
        if matched:
            hits.append(e)
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preflight router: print protocol file(s) to read for an operation."
    )
    parser.add_argument(
        "operation",
        nargs="?",
        default="-",
        help="Operation text (a command, error, or intent). '-' reads stdin.",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=None,
        help="Path to INDEX.md (default: <script>/../references/protocols/INDEX.md).",
    )
    parser.add_argument(
        "--self-test", action="store_true", help="Run built-in self-test."
    )
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if args.operation == "-":
        op_text = sys.stdin.read()
    else:
        op_text = args.operation

    if not op_text.strip():
        print("preflight: empty operation, nothing to route", file=sys.stderr)
        return 0

    if args.index is not None:
        index_path = args.index
    elif os.environ.get("PROTO_STORE"):
        index_path = Path(os.environ["PROTO_STORE"]) / "protocols" / "INDEX.md"
    else:
        index_path = (
            Path(__file__).resolve().parent.parent
            / "references"
            / "protocols"
            / "INDEX.md"
        )

    entries = load_index(index_path)
    if not entries:
        print(f"preflight: no protocols indexed at {index_path}", file=sys.stderr)
        return 0

    hits = match(op_text, entries)
    if not hits:
        print("NO_MATCH: no protocol keywords matched; proceed, then extract if a new pitfall appears.")
        return 0

    print(f"MATCHED {len(hits)} protocol(s) to preflight:")
    for h in hits:
        print(f"  - {index_path.parent / h['file']}")
        print(f"    keywords: {', '.join(h['keywords'])}")
        print(f"    {h['blurb']}")
    return 0


def run_self_test() -> int:
    sample_index = """# Index

## environment
- [P-win-git-push-retry](./P-win-git-push-retry.md) - [git-push, force-push, 443, schannel, proxy] transient push failures.
- [P-gh-repo-create-remote](./P-gh-repo-create-remote.md) - [gh, gh-repo-create, remote, origin] cosmetic remote failure.
"""
    tmp = Path(__file__).resolve().parent / "_selftest_INDEX.md"
    tmp.write_text(sample_index, encoding="utf-8")
    try:
        entries = load_index(tmp)
        assert len(entries) == 2, f"expected 2 entries, got {len(entries)}"
        assert entries[0]["name"] == "P-win-git-push-retry"
        assert "schannel" in entries[0]["keywords"]

        hits = match("git push --force origin main schannel closed", entries)
        assert len(hits) == 1 and hits[0]["name"] == "P-win-git-push-retry", hits

        hits = match("gh repo create --remote=origin", entries)
        assert len(hits) == 1 and hits[0]["name"] == "P-gh-repo-create-remote", hits

        hits = match("npm install left-pad", entries)
        assert hits == [], hits
    finally:
        tmp.unlink(missing_ok=True)

    print("preflight self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
