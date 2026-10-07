#!/usr/bin/env node
// proto-lint.js — 校验 protocol Markdown 文件
// dockercc 版: Node.js 替代 Python protocol_lint.py

const fs = require("fs");
const path = require("path");

const REQUIRED_HEADINGS = ["Symptom", "Context", "Diagnosis", "Protocol", "Validation", "Avoid", "Promotion"];
const VALID_TYPES = new Set([
  "harness-error", "tool-contract", "environment", "debugging-path",
  "implementation-path", "validation", "handoff", "project-invariant", "anti-pattern",
]);
const VALID_CONFIDENCE = new Set(["draft", "observed", "validated", "promoted"]);

function isProtocolFile(name) {
  const upper = name.toUpperCase();
  if (upper === "SKILL.md" || upper === "README.md" || name.startsWith(".")) return false;
  return /^P-[\w.-]+\.md$/i.test(name);
}

function iterMarkdown(paths) {
  const files = [];
  for (const p of paths) {
    const stat = fs.statSync(p);
    if (stat.isDirectory()) {
      for (const item of fs.readdirSync(p, { recursive: true })) {
        const full = path.join(p, item);
        if (full.endsWith(".md") && isProtocolFile(path.basename(full)) && fs.statSync(full).isFile()) {
          files.push(full);
        }
      }
    } else if (p.endsWith(".md") && isProtocolFile(path.basename(p))) {
      files.push(p);
    }
  }
  return [...new Set(files)].sort();
}

function firstMeta(text, name) {
  const m = text.match(new RegExp(`^>\\s*${name}:\\s*(.+?)\\s*$`, "m"));
  return m ? m[1].trim() : null;
}

function sectionBody(text, heading) {
  const m = text.match(new RegExp(`^##\\s+${heading}\\s*$([\\s\\S]*?)(?=^##\\s+|\\Z)`, "m"));
  return m ? m[1].trim() : "";
}

function lintText(text, label) {
  const errors = [];
  if (!/^#\s+P[\w.-]+\s+-\s+\S/m.test(text)) {
    errors.push(`${label}: title must look like '# Pslug - Title'`);
  }

  const pType = firstMeta(text, "Type");
  if (!VALID_TYPES.has(pType)) {
    errors.push(`${label}: Type must be one of ${[...VALID_TYPES].sort().join(", ")}`);
  }

  const scope = firstMeta(text, "Scope");
  if (!scope) errors.push(`${label}: missing Scope metadata`);

  const confidence = firstMeta(text, "Confidence");
  if (!VALID_CONFIDENCE.has(confidence)) {
    errors.push(`${label}: Confidence must be one of ${[...VALID_CONFIDENCE].sort().join(", ")}`);
  }

  const source = firstMeta(text, "Source");
  if (!source) errors.push(`${label}: missing Source metadata`);

  for (const heading of REQUIRED_HEADINGS) {
    if (!sectionBody(text, heading)) {
      errors.push(`${label}: missing or empty section '${heading}'`);
    }
  }

  if (/`C:\\/.test(text)) {
    errors.push(`${label}: raw Windows backslash path in inline code`);
  }

  return errors;
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.includes("--self-test")) {
    const sample = `# P-demo - Demo protocol
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
`;
    const errors = lintText(sample, "<self-test>");
    if (errors.length > 0) { console.log(errors.join("\n")); process.exit(1); }
    console.log("proto-lint self-test passed");
    process.exit(0);
  }

  if (args.length === 0) {
    console.error("Usage: node proto-lint.js <path> [...]");
    console.error("       node proto-lint.js --self-test");
    process.exit(1);
  }

  const files = iterMarkdown(args);
  if (files.length === 0) {
    console.log("No protocol files found (looking for P-*.md)");
    process.exit(0);
  }

  const allErrors = [];
  for (const f of files) {
    const text = fs.readFileSync(f, "utf8");
    allErrors.push(...lintText(text, f));
  }

  if (allErrors.length > 0) {
    console.log(allErrors.join("\n"));
    process.exit(1);
  }

  console.log(`Checked ${files.length} protocol file(s)`);
  process.exit(0);
}

module.exports = { lintText, isProtocolFile, iterMarkdown };
