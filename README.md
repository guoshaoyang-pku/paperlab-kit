# paperlab-kit — 论文协作工作包（handover 2026-09-16)

ICLR 2027 论文协作用的两层写作/绘图/评审工作环境，交给合作者。

## 这是什么

```
vendor/AI-Research-SKILLs/   Orchestra 研究技能库（12.7k★, MIT, v1.7.2）— 只按需拉取
skills/paperlab/             主 skill（默认只装这一个，其余由它按需拉起）
skills/research-skills/      子技能：写作指导层（怎么写）
skills/writer-engines/       子技能：引擎调度层（谁来写），credential-free
scripts/paperlab/            figstyle 统一绘图风格 + 出图/渲染/评审脚本
docs/FIGSTYLE.md             统一绘图风格规范（所有图必须遵守）
docs/figs/mermaid_template/  信息流图 mermaid 源码模板（源码 = 唯一事实来源）
keys/credentials.example.json 引擎凭证文件格式模板（文件名和路径由你自定）
HANDOFF.md                   给合作者 agent 的 handoff prompt（直接粘贴使用）
```

分层：**人 ↔ 主 agent（中文）↔ 引擎（英文产出）**。Orchestra 提供写作原则，
主 agent 负责编排、数字核对、中文汇报；引擎只写英文。

## 安装（合作者）

1. 把主 skill `skills/paperlab` 复制（或软链）到你的 agent 技能目录
   （Verdent: `~/.verdent/skills/`；Claude Code/codex 同理）——**默认只装这一个**，
   它会在需要时按需拉起 `research-skills` / `writer-engines` 和脚本。
2. `vendor/AI-Research-SKILLs` 放在 `~/.verdent/vendor/`（或改主 skill 里的路径，
   或设 `PAPERLAB_KIT` 指向 kit 根目录）。
3. 准备你自己的引擎凭证（包内零密钥，见下）。
4. 依赖：python3 + matplotlib + numpy；`npx @mermaid-js/mermaid-cli`；TeX Live 的
   `pdfcrop`（渲染 mermaid PDF 用）。

## 凭证（包内零密钥，机制通用）

- 引擎凭证统一走一个 JSON 文件：内容格式见 `keys/credentials.example.json`，
  **文件放哪、叫什么完全由你决定**，用环境变量 `WRITER_CREDENTIALS` 指向它即可。
  fable（claude-fable-5，润色/评审）读其中 `fable` 条目（任意 OpenAI 兼容端点）。
- 凭证永不进 skill、repo、日志。
- astra（gpt-6-astra，批量起草）：指向你自己的 codex 副本（`WRITER_CODEX_HOME`）。
- 两者都可只用其一：调度器按 `--engine` 选择；astra 配额不可用时回落 fable。
- 用量日志默认 `~/.verdent/logs/writer-engines.jsonl`；论文项目用
  `--log <project>/data/paper/ai_usage_log.jsonl` 汇总成 AI 使用披露。

## 快速验证安装

```bash
echo "Reply with exactly: KIT_OK" | python3 skills/writer-engines/scripts/call_model.py \
  --engine fable --prompt - --out /tmp/kit_smoke.md --task smoke
```

## 绘图（统一风格，强制）

所有论文数据图 import `scripts/paperlab/figstyle.py`；流程图写 mermaid 源码并
用 `scripts/paperlab/render_mermaid.py` 渲染成裁切好的 SVG+PDF。规范全文见
`docs/FIGSTYLE.md`。禁止 image-gen 栅格图进论文。
