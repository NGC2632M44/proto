# VIBECODE — protocol-forge

> 生成于 2026-10-07（VibeCode Phase 4）。本文件是 agent 进项目的第一入口。

## 这是什么
PROTO 引擎：把工作经验蒸馏成最小可复用单元（protocol），再组合成 skill。

## 技术栈
Python（零依赖脚本）+ Node 兼容脚本 + PowerShell/Bash

## 入口文件
- SKILL.md
- agents/openai.yaml
- scripts/preflight.py
- scripts/collect_trace.py
- scripts/protocol_lint.py
- scripts/mcp_proto.py

## 端口
- `—` — 无常驻端口；mcp_proto.py 是 stdio MCP，按需启动

## 怎么跑
- 一键安装：scripts/install_skill.ps1 -Both
- 建库：scripts/init_store.ps1 -Both
- 自动采集钩子：scripts/auto_capture_hook.ps1
- 校验：python scripts/protocol_lint.py references/protocols/

## 边界与禁止事项
- canonical 经验库：~/.protocols（engine 与 fuel 分离）
- engine 按运行时安装：~/.claude/skills/proto、~/.codex/skills/proto
- 本仓库是 engine 的唯一源；镜像副本视为冗余

## 产物 / 大目录
- references/protocols/（P-*.md + INDEX.md）
- graphify-out/
- .firecrawl/
- scripts/__pycache__/

## 当前状态
active（核心源项目）

## 待办
- 把 ~/.protocols 纳入 VibeCode 备份清单
- 统一 .claude / .codex / .cc-switch 下的 proto 镜像为链接或由脚本生成
- 注册 proto MCP 到 Codex（当前 config.toml 未注册）

## 配套文档
- `docs/STATE.md` — 当前进度与下一步（compact 前更新）
- `docs/DECISIONS.md` — 重要决策记录
- `docs/OPERATIONS.md` — 启停 / 恢复 / 备份
