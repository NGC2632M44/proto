# DECISIONS — protocol-forge

> 只记「为什么这么做」。每条：日期 / 决策 / 原因 / 影响。

## 2026-10-07
- **决策**：为 protocol-forge 建立 VibeCode 持久化文档（VIBECODE.md + docs/）。
  - 原因：长会话 compact 会丢失项目状态，改为落盘持久化，compact 后按文档恢复。
  - 影响：以后进本项目先读 `VIBECODE.md` 与 `docs/STATE.md`，不再依赖会话记忆。
