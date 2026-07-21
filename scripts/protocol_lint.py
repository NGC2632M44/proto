#!/usr/bin/env python3
"""Validate protocol Markdown files without external dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "Symptom",
    "Context",
    "Diagnosis",
    "Protocol",
    "Validation",
    "Avoid",
    "Promotion",
]

VALID_TYPES = {
    "harness-error",
    "tool-contract",
    "environment",
    "debugging-path",
    "implementation-path",
    "validation",
    "handoff",
    "project-invariant",
    "anti-pattern",
}

VALID_CONFIDENCE = {"draft", "observed", "validated", "promoted"}


def is_protocol_file(name: str) -> bool:
    """A protocol file's name begins with the 'P-' marker, e.g. P-slug.md."""
    upper = name.upper()
    if upper in {"SKILL.md", "README.md"} or name.startswith("."):
        return False
    return bool(re.match(r"^P-[\w.-]+\.md$", name, re.IGNORECASE))


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(item for item in path.rglob("*.md") if is_protocol_file(item.name))
        elif path.suffix.lower() == ".md" and is_protocol_file(path.name):
            files.append(path)
    return sorted(set(files))


def first_meta(text: str, name: str) -> str | None:
    match = re.search(rf"^>\s*{re.escape(name)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def section_body(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def lint_text(text: str, label: str) -> list[str]:
    errors: list[str] = []
    if not re.search(r"^#\s+P[\w.-]+\s+-\s+\S", text, re.MULTILINE):
        errors.append(f"{label}: title must look like '# Pslug - Title'")

    protocol_type = first_meta(text, "Type")
    if protocol_type not in VALID_TYPES:
        errors.append(f"{label}: Type must be one of {', '.join(sorted(VALID_TYPES))}")

    scope = first_meta(text, "Scope")
    if not scope:
        errors.append(f"{label}: missing Scope metadata")

    confidence = first_meta(text, "Confidence")
    if confidence not in VALID_CONFIDENCE:
        errors.append(
            f"{label}: Confidence must be one of {', '.join(sorted(VALID_CONFIDENCE))}"
        )

    source = first_meta(text, "Source")
    if not source:
        errors.append(f"{label}: missing Source metadata")

    for heading in REQUIRED_HEADINGS:
        body = section_body(text, heading)
        if not body:
            errors.append(f"{label}: missing or empty section '{heading}'")

    if "`C:\\" in text:
        errors.append(f"{label}: raw Windows backslash path appears in inline code")

    return errors


def run_self_test() -> int:
    sample = """# P-demo - Demo protocol
> Type: harness-error
> Scope: global
> Confidence: validated
> Source: self-test

## Symptom
Example failure.

## Context
Example context.

## Diagnosis
Example diagnosis.

## Protocol
Do the repeatable thing.

## Validation
Confirm the result.

## Avoid
Avoid the false fix.

## Promotion
Keep as draft.
"""
    errors = lint_text(sample, "<self-test>")
    if errors:
        print("\n".join(errors))
        return 1
    print("protocol_lint self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint protocol Markdown files.")
    parser.add_argument("paths", nargs="*", type=Path, help="Protocol files or folders")
    parser.add_argument("--self-test", action="store_true", help="Run built-in self-test")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.paths:
        parser.error("provide at least one protocol file or folder")

    files = iter_markdown(args.paths)
    if not files:
        print("No protocol files found (looking for P-*.md)")
        return 0

    all_errors: list[str] = []
    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        all_errors.extend(lint_text(text, str(file_path)))

    if all_errors:
        print("\n".join(all_errors))
        return 1

    print(f"Checked {len(files)} protocol file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
