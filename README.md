# PROTO

**[English](./README.en.md)** · 中文


> **吃一堑,长一智。把工作经验沉淀成最小可复用单元,少造重复的轮子。**

Every engineering session leaks value: the same error is diagnosed three times by three different agents; the same decision tree is rebuilt because nothing recorded *why* a route worked. **PROTO** compresses lived work into the **protocol** — the smallest repeatable unit a future agent can execute without re-reading the original conversation — and only escalates a unit's visibility when its recurrence earns it.

The result is **operational memory**: forward-looking, scoped, validated — not backward-looking narrative. It saves tokens, it saves time, and it lets experience transfer between agents, machines, and people.

---

## 初心

- **少造重复的轮子** — 同一个坑不该被踩第二次,同一个决策树不该被重搭。
- **吃一堑,长一智** — 失败是最高信号;proto 把它固化成下次能自动加载的规则。
- **节省 token 与时间** — 一次廉价的 preflight 读取,胜过反复重新诊断。
- **珍惜工作经验** — 把"为什么这条路走通了"沉淀下来,而不是随会话消散。
- **以最小单元交流分享** — protocol 是最小单位,组合成 skill,或打包成 pack 在社区流通。

## 这是什么

PROTO 是一套**把工作蒸馏成可复用记忆的引擎**,不是一个固定工具库:

- **protocol** — 最小单元。一个 trigger + 一条可复用行动路径。`P-*.md` 文件,≤~20 行。
- **skill** — 组合多个 co-triggered protocol 的执行接口(`SKILL.md` + `references/` + `scripts/`)。
- **pack** — 分享单元。一组 `P-*.md` + provenance,可发布成 git repo 供他人导入。

关键机制:**engine 与 fuel 分离**。引擎(`SKILL.md`/scripts)小而稳,按运行时安装;燃料(`P-*.md` protocols)是真正的经验,跨运行时共享一份。

## 核心机制

| 机制 | 作用 |
|---|---|
| **Preflight** | 已知风险操作前,花一次廉价读取预载匹配的 protocol,而不是重新踩坑。 |
| **Collect → Distill** | 采集永远无 LLM、always-on(命令失败即记录 trace);蒸馏按需批量。 |
| **Closed-loop validation** | 蒸馏出的 protocol 必须能被产生它的 trace 经 preflight 路由回——否则 trigger-keywords 是错的。 |
| **Promotion ladder** | 证据越足,形式越硬:draft → observed → validated → `SKILL.md` rule → script → new skill。 |
| **Cross-runtime store** | 一个 canonical store(`~/.protocols`),cc 和 codex 共享同一份燃料。 |
| **Pack** | protocol 打包成可分享的单元,碰撞时自动重键关键词。 |

## 安装

PROTO 是一个可移植的 skill 文件夹。

**Codex / Claude Code 一键安装(推荐)**

```powershell
git clone https://github.com/NGC2632M44/proto.git
cd proto
powershell scripts\install_skill.ps1 -Both      # 同步到 cc + codex 两个 skill 根
powershell scripts\init_store.ps1 -Both         # 建 ~/.protocols 并链接两个 runtime 到它
powershell scripts\auto_capture_hook.ps1        # 装 PowerShell 失败命令自动采集钩子
```

**仅 lint(无运行时)**

```bash
git clone https://github.com/NGC2632M44/proto.git
python proto/scripts/protocol_lint.py --self-test
```

要求:Markdown 编辑器 + Python 3.7+。无其他依赖。

## 快速开始

```text
你: 用 $proto 从本次工作会话提取 protocol,并判断哪些应该成为 skill。
```

五个操作模式:

| Mode | Action |
|---|---|
| `extract` | 把日志、对话摘要、diff、测试、handoff 笔记转成 protocol 文件。 |
| `distill` | 合并、拆分、分级现有 protocol。 |
| `promote` | 决定哪些 protocol 进 `SKILL.md`/`references/`/`scripts/`。 |
| `compose` | 从一组相关 protocol 构建或更新 skill。 |
| `retrospect` | 会话结束时捕获重复错误、决策、验证与 handoff。 |

protocol 文件起草前读 [`references/protocol-schema.md`](./references/protocol-schema.md);编辑后跑 [`scripts/protocol_lint.py`](./scripts/protocol_lint.py)。

## 仓库布局

```
proto/
├── SKILL.md                       # 触发器、路由、核心流程、最高优先级规则
├── agents/openai.yaml             # Codex 发现接口
├── references/
│   ├── protocol-schema.md         # 每个 protocol 必须遵守的语法
│   ├── routing.md                 # preflight 匹配、promote、auto-compose 规则
│   ├── auto-capture.md            # collect/distill 拆分与闭环校验
│   ├── cross-runtime.md           # 共享 store 设计与避坑
│   └── protocols/                 # protocol 库 + INDEX.md 路由表
└── scripts/
    ├── preflight.py               # 路由器:操作文本 → 该读哪些 protocol
    ├── protocol_lint.py           # 零依赖 protocol 校验器 + self-test
    ├── collect_trace.py           # 无 LLM 的裸 trace 采集器
    ├── pack.py                    # protocol pack 导出/导入(分享单元)
    ├── install_skill.ps1          # 同步 skill 到运行时
    ├── init_store.ps1             # 一键建 store + 链接 runtime
    ├── link_store.ps1             # junction 各 runtime 到共享 store
    ├── auto_capture_hook.ps1      # PowerShell 自动采集钩子(装/卸)
    ├── sync_store.ps1 / .sh       # 跨机器 store 同步
    └── publish.ps1                # 一键:同步 skill + commit + rebase + push
```

skill 文件夹内部**不含** README/changelog/安装指南——那些在仓库根,skill 文件夹只是产物。

## 一键工作流(不依赖任何审批通道)

```powershell
# 改完代码后同步已装 skill 并推 GitHub
powershell scripts\publish.ps1 -Both -Message "your message"

# 新机器一键配置
powershell scripts\init_store.ps1 -Both
powershell scripts\auto_capture_hook.ps1
```

## 校验与 Lint

`scripts/protocol_lint.py` 零依赖,强制 schema:标题形态、`Type`/`Confidence` 枚举、`Scope`/`Source` 必填、七个必填段非空、拒绝内联代码里的裸 Windows 反斜杠路径。

```bash
python scripts/protocol_lint.py references/protocols/   # 校验整个文件夹
python scripts/protocol_lint.py --self-test             # 内置自测
```

一个 protocol 在 lint 干净 **且** 脱离原对话可用之前,不算就绪。

## 理念与愿景

### 个性化自迭代

本仓库只交付**引擎**与少量示例 protocol。真正有价值的 protocol 是你在自己工作里踩出来的——它跟着你迭代,越用越懂你的环境、你的栈、你的偏好。所以**协议库不必同步回上游**:它是你私人的端智能,自己喂自己。proto 的设计就是让"采集—蒸馏—复用"这条闭环足够便宜,能始终在后台跑。

### 社区化与市场化

protocol 是最小单元,pack 是流通货币。设想:

- **protocol packs** 像 npm 包一样发布——"我的 Windows + 代理 + gh 踩坑集"、"我的 React 性能调优路径集"。
- 消费者 `pack.py import` 一行导入,碰撞时自动重键关键词,不打架。
- **skill 是个性化组合**:同一组 pack,不同用户按自己的工作流 compose 出不同 skill。
- 成熟 protocol 组可以沉淀成**面向某领域/某工具的 skill**对外发布,而底层的 pack 仍可被他人重组。

这样,经验不再锁在某个人的脑子里或某次会话里:吃一堑的是一个人,长一智的是整个社区。少造重复的轮子,把节省的 token 和时间还给真正的创造。

## 隐私与规范

- **无 secrets。** 发布前移除项目密钥、本地绝对路径、个人 token、原始对话历史。示例 protocol 用占位名;`protocol_lint.py` 拒绝内联代码里的裸 `C:\` 路径。
- **无环境假设**,除非它是 protocol 的核心。
- **作者身份用 GitHub-noreply**,保持可链接而不暴露个人邮箱。
- **不确定性是一等公民。** `draft`/`observed` 是合法的公开状态;过早 promote 才是缺陷。

Fork 或改编本 skill 时,发布前请跑同样的隐私检查。

## 贡献

欢迎**新增或加强 protocol**(以 pack 形式)、修复脚本、改进 schema。PR 前:

1. 按 [`references/protocol-schema.md`](./references/protocol-schema.md) 起草。
2. `python scripts/protocol_lint.py <你的文件或文件夹>` 干净退出。
3. 确认 protocol 脱离原对话可用——否则补 context 或降级 confidence。
4. 移除本地路径、token、环境特定假设。

protocol 冲突时,仅当各自 context 不同才保留两者;否则优先更新的 validated protocol 并记录旧规则被取代的理由。

## License

MIT © [NGC2632M44](https://github.com/NGC2632M44). See [`LICENSE`](./LICENSE).

---

*吃一堑,长一智。少造一个重复的轮子,就是给所有人省下一段重复的时间。*