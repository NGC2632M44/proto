#!/usr/bin/env node
// proto-retrospect.js — 会话结束自动采集，写入 protocol store
// 与 notify-send.js 并行运行于 Stop hook
// 读取 transcript JSONL → 提取关键信号 → 写入 inbox trace

const fs = require("fs");
const path = require("path");
const os = require("os");

const PROTO_STORE = process.env.PROTO_STORE || path.join(os.homedir(), ".claude", "protocols");
const INBOX = path.join(PROTO_STORE, "inbox");
const DEBUG = process.env.HOOK_DEBUG_LOG || "";

function dbg(s) { if (DEBUG) try { fs.appendFileSync(DEBUG, "proto-retrospect " + s + "\n"); } catch {} }

// ── 信号检测 ──────────────────────────────────────────────────────
const ERROR_SIGNALS = [
  { re: /(?:Error|Exception|failed|error)[:\s].*/gi, tag: "error" },
  { re: /(?:EACCES|permission denied|PermissionError)/gi, tag: "permission" },
  { re: /(?:ENOENT|no such file|not found|404)/gi, tag: "not-found" },
  { re: /(?:ECONNREFUSED|connection refused|ECONNRESET|timeout|timed out)/gi, tag: "network" },
  { re: /(?:UnicodeDecodeError|GBK|encoding|codec|charset)/gi, tag: "encoding" },
  { re: /(?:schannel|SSL|TLS|certificate|443)/gi, tag: "ssl" },
  { re: /(?:git.*(?:fail|error|fatal)|merge.conflict|detached.HEAD)/gi, tag: "git" },
  { re: /(?:npm.ERR|install.fail|package.not.found)/gi, tag: "npm" },
  { re: /(?:SyntaxError|Unexpected token|parse.error)/gi, tag: "parse" },
];

const DECISION_SIGNALS = [
  { re: /(?:改为|切换|改用|放弃|不采用|决定|选择|最终方案)/g, tag: "decision" },
  { re: /(?:架构|重构|迁移|升级|降级|替代|替换)/g, tag: "architecture" },
  { re: /(?:踩坑|坑|注意|警告|小心|不要|避免|避坑)/g, tag: "pitfall" },
  { re: /(?:workaround|hack|trick|绕过|绕过方案)/gi, tag: "workaround" },
  { re: /(?:经验|教训|下次|以后|记住|总结)/g, tag: "lesson" },
];

// ── 从 transcript 提取信号 ─────────────────────────────────────────
function analyzeTranscript(jsonlPath) {
  if (!jsonlPath || !fs.existsSync(jsonlPath)) return null;

  const lines = fs.readFileSync(jsonlPath, "utf8").split("\n").filter(Boolean);
  const signals = [];
  const stats = { assistantMsgs: 0, toolCalls: 0, errors: 0, decisions: 0 };
  let lastLongAssistant = "";

  for (const line of lines) {
    try {
      const m = JSON.parse(line);

      // 统计 assistant 消息
      if (m.type === "assistant" && m.message?.content) {
        stats.assistantMsgs++;
        const texts = (Array.isArray(m.message.content) ? m.message.content : [m.message.content])
          .filter(c => c.type === "text").map(c => c.text).join(" ");

        if (texts.length >= 100) lastLongAssistant = texts;

        // 检测决策信号
        for (const { re, tag } of DECISION_SIGNALS) {
          if (re.test(texts)) { stats.decisions++; signals.push(tag); break; }
        }
      }

      // 统计工具调用
      if (m.type === "assistant" && m.message?.tool_use) {
        stats.toolCalls++;
      }

      // 检测错误信号(从工具结果)
      if (m.type === "user" && m.message?.content) {
        const texts = Array.isArray(m.message.content) ? m.message.content : [m.message.content];
        for (const c of texts) {
          const txt = typeof c === "string" ? c : c.text || "";
          for (const { re, tag } of ERROR_SIGNALS) {
            if (re.test(txt)) { stats.errors++; signals.push(tag); break; }
          }
        }
      }
    } catch {}
  }

  return {
    stats,
    signals: [...new Set(signals)],
    lastLongAssistant: lastLongAssistant.slice(0, 500),
    lineCount: lines.length,
  };
}

// ── 写入 trace ─────────────────────────────────────────────────────
function writeRetrospectTrace(analysis, transcriptPath) {
  if (!analysis || analysis.stats.errors + analysis.stats.decisions === 0) {
    dbg("no signals, skip trace");
    return null;
  }

  fs.mkdirSync(INBOX, { recursive: true });
  const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const fname = `retrospect-${ts}.trace`;
  const fp = path.join(INBOX, fname);

  const lines = [
    `# retrospect ${ts}`,
    `runtime: dockercc`,
    `source: ${transcriptPath || "unknown"}`,
    `signals: ${analysis.signals.join(", ") || "none"}`,
    `stats: ${analysis.stats.assistantMsgs} msgs, ${analysis.stats.toolCalls} tools, ${analysis.stats.errors} errs, ${analysis.stats.decisions} decisions`,
    "",
    "## 会话摘要 (供 proto extract 蒸馏)",
    analysis.lastLongAssistant || "(无长文本)",
    "",
  ];

  fs.writeFileSync(fp, lines.join("\n"), "utf8");

  // 统计 inbox
  const count = fs.readdirSync(INBOX).filter(f => f.endsWith(".trace")).length;
  dbg(`trace saved: ${fp} (inbox: ${count})`);
  return { path: fp, inboxCount: count };
}

// ── 主流程 ─────────────────────────────────────────────────────────
function main() {
  let input = "";
  let timedOut = false;
  const timer = setTimeout(() => { timedOut = true; processInput(input); }, 8000);

  process.stdin.setEncoding("utf8");
  process.stdin.on("data", c => { input += c; });
  process.stdin.on("end", () => {
    if (!timedOut) { clearTimeout(timer); processInput(input); }
  });

  function processInput(raw) {
    dbg("stdin-len=" + raw.length);
    let tp = "";
    try { tp = JSON.parse(raw).transcript_path || ""; } catch {}

    if (!tp) { dbg("no transcript_path"); process.exit(0); }

    const analysis = analyzeTranscript(tp);
    if (!analysis) { dbg("analysis failed"); process.exit(0); }

    const result = writeRetrospectTrace(analysis, tp);
    if (result) {
      dbg(`done: ${result.path} inbox=${result.inboxCount}`);
      // 若 inbox >= 10, 输出建议
      if (result.inboxCount >= 10) {
        dbg("SUGGEST: inbox has " + result.inboxCount + " traces — run proto extract");
      }
    }
    process.exit(0);
  }
}

if (require.main === module) {
  main();
}

module.exports = { analyzeTranscript, writeRetrospectTrace };
