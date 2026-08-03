#!/usr/bin/env node
// proto-preflight.js — 路由器: 操作文本 → 匹配的 protocol 文件
// dockercc 版: Node.js 替代 Python preflight.py

const fs = require("fs");
const path = require("path");
const os = require("os");

const PROTO_STORE = process.env.PROTO_STORE || path.join(os.homedir(), ".claude", "protocols");

const STOPWORDS = new Set([
  "origin", "install", "remote", "push", "pull", "skill", "main", "commit",
  "file", "metadata", "frontmatter", "claude", "codex", "windows", "public",
  "initial", "repo", "branch", "config", "run", "build", "test", "lint",
  "force", "git", "gh", "error", "fail", "failure", "timeout", "proxy",
]);

function normalize(s) {
  return s.replace(/[-_\s]+/g, " ").trim().toLowerCase();
}

function isStrongKeyword(kw) {
  const k = kw.toLowerCase();
  if (normalize(k).includes(" ")) return true;
  if (/\d/.test(k)) return true;
  if (k.length >= 6 && !STOPWORDS.has(k)) return true;
  return false;
}

// 解析 INDEX.md 行: - [P-name](./P-name.md) — [kw1, kw2] description
const INDEX_RE = /^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*[-—–]\s*\[([^\]]*)\](.*)$/;

function loadIndex(indexPath) {
  if (!fs.existsSync(indexPath)) return [];
  const entries = [];
  const lines = fs.readFileSync(indexPath, "utf8").replace(/\r/g, "").split("\n");
  for (const line of lines) {
    const m = line.match(INDEX_RE);
    if (!m) continue;
    const [, name, file, kws, blurb] = m;
    const keywords = kws.split(",").map(k => k.trim().toLowerCase()).filter(Boolean);
    entries.push({ name: name.trim(), file: file.trim(), keywords, blurb: blurb.trim() });
  }
  return entries;
}

function match(opText, entries) {
  const hay = normalize(opText);
  return entries.filter(e => e.keywords.some(kw => isStrongKeyword(kw) && normalize(kw) === hay || hay.includes(normalize(kw))));
}

function preflight(opText, indexPath) {
  if (!opText || !opText.trim()) return { matches: [], noMatch: true, reason: "empty operation" };

  const idxPath = indexPath || path.join(PROTO_STORE, "protocols", "INDEX.md");
  const entries = loadIndex(idxPath);
  if (entries.length === 0) return { matches: [], noMatch: true, reason: "no index at " + idxPath };

  const hits = match(opText, entries);
  if (hits.length === 0) return { matches: [], noMatch: true, reason: "NO_MATCH" };

  return {
    matches: hits.map(h => ({
      name: h.name,
      path: path.join(path.dirname(idxPath), h.file),
      keywords: h.keywords,
      blurb: h.blurb,
    })),
    noMatch: false,
    count: hits.length,
  };
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  let opText = "", indexPath = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--index" && args[i + 1]) { indexPath = args[++i]; }
    else if (!opText) { opText = args[i]; }
  }

  if (!opText) {
    const chunks = [];
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", c => chunks.push(c));
    process.stdin.on("end", () => {
      const result = preflight(chunks.join(""), indexPath);
      console.log(JSON.stringify(result, null, 2));
      process.exit(0);
    });
  } else {
    const result = preflight(opText, indexPath);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }
}

module.exports = { preflight, loadIndex, match };
