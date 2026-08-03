#!/usr/bin/env node
// proto-collect.js — 采集原始 trace 到 proto inbox(无 LLM, 零依赖)
// dockercc 版: Node.js 替代 Python collect_trace.py
// 由 Stop hook / agent 在命令失败时自动调用

const fs = require("fs");
const path = require("path");
const os = require("os");

const PROTO_STORE = process.env.PROTO_STORE || path.join(os.homedir(), ".claude", "protocols");
const INBOX = path.join(PROTO_STORE, "inbox");
const MAX_SNIPPET_LINES = 8;

const KNOWN_SIGNALS = [
  /InputValidationError/i,
  /UnicodeDecodeError|codec can't decode|gbk|GBK/i,
  /schannel|port 443/i,
  /403|422/i,
  /timed out|timeout/i,
  /fatal:|not a git repository/i,
  /Unable to add remote/i,
  /EACCES|permission denied/i,
  /ENOENT|no such file/i,
  /ECONNREFUSED|connection refused/i,
];

function slugify(text) {
  const s = text.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  return (s || "trace").slice(0, 60);
}

function classify(text) {
  const hits = [];
  for (const re of KNOWN_SIGNALS) {
    if (re.test(text)) hits.push(re.source.split("|")[0]);
  }
  return hits;
}

function collect(opts = {}) {
  const { operation = "", exitCode = null, stderr = "", cwd = process.cwd(), note = "" } = opts;
  if (!operation.trim()) return null;

  const inboxDir = path.resolve(INBOX);
  fs.mkdirSync(inboxDir, { recursive: true });

  const now = new Date();
  const ts = now.toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const fname = `${ts}-${slugify(operation)}.trace`;
  const fp = path.join(inboxDir, fname);

  const snippet = stderr.split("\n").slice(0, MAX_SNIPPET_LINES).join("\n");
  const signals = classify(operation + "\n" + stderr);

  const lines = [
    `# trace ${ts}`,
    `runtime: dockercc-node`,
    `cwd: ${cwd}`,
  ];
  if (exitCode !== null) lines.push(`exit: ${exitCode}`);
  if (signals.length > 0) lines.push(`signals: ${signals.join(", ")}`);
  if (note) lines.push(`note: ${note}`);
  lines.push("");
  lines.push("## operation");
  lines.push(operation.trim());
  if (snippet) {
    lines.push("");
    lines.push("## stderr snippet");
    lines.push(snippet);
  }
  lines.push("");

  fs.writeFileSync(fp, lines.join("\n"), "utf8");
  return { path: fp, signals, inboxCount: fs.readdirSync(inboxDir).filter(f => f.endsWith(".trace")).length };
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  let operation = "", exitCode = null, stderr = "", note = "";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--exit" && args[i + 1]) { exitCode = parseInt(args[++i], 10); }
    else if (args[i] === "--stderr" && args[i + 1]) { try { stderr = fs.readFileSync(args[++i], "utf8"); } catch {} }
    else if (args[i] === "--note" && args[i + 1]) { note = args[++i]; }
    else if (!operation) { operation = args[i]; }
  }

  if (!operation) {
    // 尝试从 stdin 读取
    const chunks = [];
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", c => chunks.push(c));
    process.stdin.on("end", () => {
      operation = chunks.join("").trim();
      if (!operation) { console.error("collect: empty operation"); process.exit(0); }
      const result = collect({ operation, exitCode, stderr, note });
      if (result) console.log(JSON.stringify(result));
      process.exit(0);
    });
  } else {
    const result = collect({ operation, exitCode, stderr, note });
    if (result) console.log(JSON.stringify(result));
    process.exit(0);
  }
}

module.exports = { collect, classify };
