# P-sci-paper-intro-no-header - Nature 系论文引言无 "Introduction" 标题,正则提取必 0 字
> Type: anti-pattern
> Scope: tool:figexplain / pdf-parsing
> Confidence: validated
> Source: figexplain 优化会话 (2026-08-01,Hrovatin 2023 Nat Metab)

## Symptom
从论文 PDF 提取 "Introduction" 得 0 字;`\n\s*introduction\b` 正则不匹配,但文章确实有引言(在摘要后直接开始)。

## Context
Nature 系期刊(Nat Metab、Nat Commun 等)正文排版:摘要无 "Abstract" 标题、引言无 "Introduction" 标题——标题/作者后第一段即摘要,随后引言段落直接衔接,第一个显式 section 标题是 "Results"/"Methods"。figexplain 的 `abstract_and_intro` 只支持显式 header,无 header 时返回空(之前靠 prompt 兜底"从全文自行定位")。

## Diagnosis
`pdf 首页文本` 检查:页面头是 "Article"+ 标题 + 作者 + 正文段落,无 Introduction 字样;第一个大标题是 Results。

## Protocol
无 header 时 fallback:在**折叠空白后的全文**(与 abstract 同一坐标系)上,取「摘要尾部 80 字符定位点 → 第一个 Results/Methods 标题」之间的文本为引言,上限 4000 字。摘要尾部定位比头部稳(尾部文本独特、跨行折叠一致)。

## Validation
Hrovatin 2023(Nat Metab):引言 0 → 4000 字,内容正确("...δ-cells... Type 1 diabetes...")。

## Avoid
不要只在原文上做 `find(摘要尾部)`(换行折叠不一致找不到)。不要依赖 prompt 兜底当主路径——引言是 Stage 3 摘要/引言对比的关键输入。

## Promotion
保持 `validated`。同族：`P-sci-fig-caption-unicode-space`。若该「无 Introduction 标题」模式在第三本期刊复现，考虑升为 `references/` 里的解析器 invariant 章节。
