# P-win-python-requests-proxy-hijack - Claude Code 注入的代理 env 劫持 Python requests,境外 API 断连
> Type: harness-error
> Scope: tool:bash / runtime:python-requests
> Confidence: validated
> Source: figexplain 优化会话 (2026-08-01)

## Symptom
Python `requests.post` 到境外 LLM 端点(如 api.babelark.ai)报 `RemoteDisconnected('Remote end closed connection without response')`,连续多图全失败;而同一端点 Python 直连(清除代理 env)返回 200。

## Context
Claude Code `settings.json` 的 `env` 块注入 `HTTP_PROXY/HTTPS_PROXY=http://127.0.0.1:21882`(privoxy)。Bash/子进程继承后,Python `requests` 默认尊重环境代理 → 所有外网请求走 privoxy。privoxy 转发部分境外 API(尤其 TLS 长连接/大响应)会掐断连接。`NO_PROXY` 只保护了配置内域名,境外 LLM 端点不在其中。本机 curl 另有沙箱拦截,不能用 curl 诊断外网(清代理也 000 立即失败);用 Python/Node 验证。

## Diagnosis
`env | grep -i proxy` 显示注入的代理变量;`python -c "urllib.request.urlopen(...)"`(无 env)200 vs 带 env 断连。区分:curl 000 不代表网络不通(沙箱),以 Python/Node 实测为准。

## Protocol
1. LLM/境外 API 调用在每次 `requests.post(..., proxies={"http": None, "https": None})` 显式禁代理(直连)。
2. 或启动时从环境剔除:`os.environ.pop("HTTP_PROXY"); os.environ.pop("HTTPS_PROXY")`(注意别影响本应走代理的 WebFetch 类请求)。
3. 需要走代理的请求保持默认;本地/境内直连域名加入 `NO_PROXY`。
4. 不要用 Session keep-alive(见 P-win-requests-port-exhaustion-10048 的两难与最终方案)。

## Validation
同端点直连返回 200;`figexplain` 10 图流水线零断连。

## Avoid
不要用 curl 判断外网连通性(本机沙箱外网全 000)。不要为绕过断连而把超时无限拉长。不要用 Session 复用连接(被掐)。

## Promotion
保持 `validated`。关联 `P-win-requests-port-exhaustion-10048`（同一次 figexplain 会话的相邻故障）。若第三方工具再次注入代理 env，考虑升为 skill 级 preflight 规则。
