# paperlab-kit — 论文协作工作包（handover 2026-09-16)

ICLR 2027 论文协作用的两层写作/绘图/评审工作环境，交给合作者。

## 这是什么

```
vendor/AI-Research-SKILLs/   Orchestra 研究技能库（12.7k★, MIT, v1.7.2）— 只按需拉取
skills/research-skills/      路由器：写作指导层（怎么写），入口只此一个
skills/writer-engines/       引擎调度层（谁来写）：astra / fable，credential-free
scripts/paperlab/            figstyle 统一绘图风格 + 出图/渲染/评审脚本
docs/FIGSTYLE.md             统一绘图风格规范（所有图必须遵守）
docs/figs/mermaid_template/  信息流图 mermaid 源码模板（源码 = 唯一事实来源）
keys/eval_keys.example.json  你的引擎密钥文件格式模板
HANDOFF.md                   给合作者 agent 的 handoff prompt（直接粘贴使用）
```

分层：**人 ↔ 主 agent（中文）↔ 引擎（英文产出）**。Orchestra 提供写作原则，
主 agent 负责编排、数字核对、中文汇报；引擎只写英文。

## 安装（合作者）

1. 把 `skills/research-skills` 和 `skills/writer-engines` 复制（或软链）到你的
   agent 技能目录（Verdent: `~/.verdent/skills/`；Claude Code/codex 同理）。
2. `vendor/AI-Research-SKILLs` 放在 `~/.verdent/vendor/`（或改 router 里的路径）。
3. 准备你自己的引擎凭证（包内不含任何密钥，见下）。
4. 依赖：python3 + matplotlib + numpy；`npx @mermaid-js/mermaid-cli`；TeX Live 的
   `pdfcrop`（渲染 mermaid PDF 用）。

## 凭证（重要：包内零密钥）

- **fable**（claude-fable-5，润色/评审）：把你的 OpenAI 兼容端点 key 写入
  `keys/eval_keys.json`（格式见 `keys/eval_keys.example.json`），并设环境变量
  `WRITER_EVAL_KEYS` 指向它。key 永不进 skill、repo、日志。
- **astra**（gpt-6-astra，批量起草）：需要你自己的 codex 副本（如
  `~/.codex-<vendor>`），设 `WRITER_CODEX_HOME` 指向它。
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
