# FIGSTYLE — 论文图统一风格规范（强制）

出处：`scripts/paperlab/figstyle.py`（ICLR profile）。所有进入论文/报告的图
必须符合本规范；数据图一律由脚本从数据再生，**禁止手改任何产物**。

## 总原则

1. **矢量优先**：LaTeX 引用 PDF（矢量），PNG 仅作 300dpi 预览。
2. **禁 image-gen**：Gemini/DALL-E 类生成的栅格示意图不进论文（文字易错、
   不可微调、不可复现）。流程/架构图写 mermaid 源码 → `render_mermaid.py`
   渲染成 SVG + 裁切 PDF；需要 AI 时让引擎写/改 mermaid 代码，不生成像素。
3. **可复现**：每张数据图有生成脚本；图上每个数字可溯源到 run artifact 或
   登记文档，脚本内做断言（数据与注册值不一致即失败）。
4. **自解释**：caption 之外，图内标签完整（量名+单位）；图例不遮挡数据。

## 尺寸与字体（ICLR 单栏）

- 全宽 5.5 in（`figstyle.ICLR_WIDTH`），半宽 2.65 in；最高 9 in。
- 字体 Helvetica/Arial（无则 DejaVu Sans）；正文 8pt，轴标 8.5pt，
  刻度 7.5pt，图例 7pt。
- `pdf.fonttype = 42`（TrueType，PDF 内文字可编辑）。

## 颜色与 marker（家族固定，全论文一致）

Okabe-Ito 色盲安全调色板，家族 → 颜色/marker 由 `figstyle.FAMILY` /
`FAMILY_MARKER` 固定：

| 家族 | 颜色 | marker |
|---|---|---|
| scaffolded ART | 黑 `#000000` | ● 圆 |
| scaffolded CNN | 绿 `#009E73` | ■ 方 |
| generic transformer | 蓝 `#0072B2` | ● 圆（多规模连线） |
| generic CNN | 橙 `#E69F00` | ▲ 三角 |
| generic diffusion | 朱红 `#D55E00` | ◆ 菱形 |

新增家族先扩 `figstyle.py` 再用图，不得在单图内私定颜色。
多种子：均值 + min/max 误差棒（`capsize=2.5`）；参考线灰虚线 `0.75, (4,3)`。

## 图面纪律

- 只留左/下 spine（`axes.spines.top/right: False`）；默认无网格。
- 线宽 1.3，marker 4.5pt；对数轴用 `10^n` 刻度。
- 图例放图下（`bbox_to_anchor`），双列，`frameon=False`。
- 注释（annotate）字号 7pt，引线 0.7pt，不与数据点/图例重叠。
- 每图导出前问一句：黑白打印还能分清五个家族吗？（marker 形状差异保证）

## 流程图（mermaid）

- 源码 `.mmd` 是唯一事实来源，与渲染产物一起进版本库。
- 统一 config：base 主题、Arial 15px、`htmlLabels:false`、`curve:linear`。
- 语义配色四类：数据来源蓝 `#2563EB` / 机构绿 `#059669` /
  中间帧橙 `#EA580C` / 评测紫 `#7C3AED`，底色用各 50 号浅色。
- 渲染：`render_mermaid.py --src-dir <dir>`（mermaid-cli → SVG 透明底 +
  PDF 白底 → `pdfcrop --margins 12` 裁切）。
