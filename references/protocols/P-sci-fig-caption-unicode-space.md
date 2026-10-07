# P-sci-fig-caption-unicode-space - PDF 提取正则必须含 Unicode 空格,否则 "Fig.\xa01A" 全漏
> Type: debugging-path
> Scope: tool:figexplain / pdf-parsing
> Confidence: validated
> Source: figexplain 训练集验证 (2026-08-01,PNAS 2025 文章)

## Symptom
`extract_figures` 对某篇 PNAS 文章返回 0 张图;正文里明明有大量 "Fig. 1A" 引用和完整图注。`CAPTION_HEAD_RE` 匹配不到任何 "Fig. N"。

## Context
PNAS(及部分 Nature 系)排版把 `Fig.` 与编号之间的空格编码为 **\xa0(不换行空格)**、窄空格( )或窄不换行空格( )。原正则空白类 `[ \t\r\n\f]+` 不含这些 Unicode 空格 → "Fig.\xa01A" 整体漏匹配 → caption 头找不到 → 图=0。正文引用同样用 \xa0,连 `\b` 边界都断。

## Diagnosis
`repr(文本片段)` 显示 `'Fig.\\xa01A'`;`re.search(r"Fig[.]?\s*1", t)` 无匹配。

## Protocol
1. 空白类正则统一加 Unicode 空格:`_WS_P = r"[ \t\r\n\f\xa0  ]*"`。
2. 涉及 PDF 文本匹配的空白类(`\s+` 也要注意——`\s` 不含 \xa0?Python `\s` 匹配 `[ \t\n\r\f\v]` 加 Unicode 空白包括 \xa0!\xNN 注意:Python re 的 `\s` 在 Unicode 模式下**包含** \xa0)优先用字符类显式列出。
3. 修复后对原失败文章重验(图 0→N)。

## Validation
PNAS 2025(DDFVPLQW):图 0→4(Fig 1-4);Sci Rep/FASEB/CellRM 无回归。

## Avoid
不要只修单篇(caption 正则的 Unicode 空格是通用问题,各期刊混用)。不要用 `\s` 替代显式字符类而不验证(不同 Python/re 版本行为不同)。

## Promotion
保持 `validated`。同族：`P-sci-paper-intro-no-header`（同为 PDF 解析漏读）。再遇同类漏匹配时，优先扩大字符类（`\s` 覆盖 Unicode 空白）而不是继续堆正则分支。
