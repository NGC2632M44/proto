# P-win-requests-port-exhaustion-10048 - requests 连接策略:keep-alive 被掐 vs 端口耗尽(两难)
> Type: harness-error
> Scope: runtime:python-requests / platform:windows
> Confidence: validated
> Source: figexplain 优化会话 (2026-08-01)

## Symptom
连续多次 `requests.post`(每次新建连接、大响应体,如图 base64)后报 `NewConnectionError: [WinError 10048] 通常每个套接字地址(协议/网络地址/端口)只允许使用一次`,前几张图成功、后续全失败。反之用 `requests.Session()` 复用连接(keep-alive)时,第二次起必报 `RemoteDisconnected`(远端掐断复用连接)。

## Context
两个独立约束构成两难:
- 部分境外 API(babelark 实测)掐断 keep-alive 复用连接——Session 复用的第二次请求必断
- 每请求新建连接(Connection: close)→ Windows 上连接主动关闭后进 TIME_WAIT(120s 级),大响应连接堆积 → 本地端口耗尽(10048)

## Diagnosis
对比矩阵(文本/图 × Session/逐请求):Session 必 RemoteDisconnected(0s 级),逐请求必连通。10048 出现在逐请求模式连续多图之后,重启进程前几张正常、随后复发。

## Protocol
1. 用裸 `requests.post` + `proxies={"http": None, "https": None}`(禁代理,见 P-win-python-requests-proxy-hijack)+ 头 `"Connection": "close"`。
2. 重试次数 ≥4,backoff 用长间隔(20/40/60s):10048 需等 TIME_WAIT 释放(120s 级),短 backoff 必然全部重试失败。
3. 降低单请求载荷(图压缩)可减小连接驻留与端口占用。

## Validation
同流水线 10 图连续调用零断连零 10048;单图 3 连发全 OK(27-31s)。

## Avoid
不要用 Session keep-alive 复用(babelark 等掐复用连接)。不要短 backoff 重试 10048(等不到端口释放)。不要在每个请求里新建 Session(等同不复用,10048 照旧)。

## Promotion
保持 `validated`。关联 `P-win-python-requests-proxy-hijack`。若在其它 Windows 项目复现，考虑升为 `scripts/` 里的 requests 连接池检查脚本。
