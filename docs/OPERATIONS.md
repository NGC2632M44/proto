# OPERATIONS — protocol-forge

> 启停 / 恢复 / 备份。只写可执行的命令。

## 启动
- 一键安装：scripts/install_skill.ps1 -Both
- 建库：scripts/init_store.ps1 -Both
- 自动采集钩子：scripts/auto_capture_hook.ps1
- 校验：python scripts/protocol_lint.py references/protocols/

## 停止
- （待补：停止命令或进程名）

## 端口
- `—` — 无常驻端口；mcp_proto.py 是 stdio MCP，按需启动

## 备份
- 源码：Git（见 `git status`）
- 大目录 / 数据：- references/protocols/（P-*.md + INDEX.md）
- graphify-out/
- .firecrawl/
- scripts/__pycache__/
- VibeCode 侧统一清单：`C:\Users\29346\VibeCode\registries\projects.json`

## 恢复
1. 读 `VIBECODE.md` 与 `docs/STATE.md`
2. 按上面「启动」执行
3. 复现问题前先看 `docs/DECISIONS.md`，避免重复决策

## 已知坑
- （待补）
