---
name: paperlab
description: Master skill for the paperlab two-tier paper-writing environment — pulls the sub-skills on demand. Use when the user mentions paperlab, asks to draft/review/polish a paper with engine models, make publication figures, run the review panel, or says 论文协作 / 引擎 / 审稿面板 / 开工. This is the only skill that needs to be installed; everything else is pulled from the kit on demand.
---

# paperlab — master skill（默认只装这一个）

Two-tier protocol: the author talks to you in Chinese (or their language); the
external engines produce the English prose. You orchestrate, fact-check, and
report. Everything below is pulled on demand — do not preload.

## Pull map (kit layout)

| Need | Pull |
|---|---|
| WHO writes (engine dispatch astra/fable) | `skills/writer-engines/SKILL.md` → then use its `scripts/call_model.py` |
| HOW to write (principles, abstract formula, citation discipline) | `skills/research-skills/SKILL.md` → Orchestra sub-skills under `vendor/AI-Research-SKILLs/` |
| Figures (binding style) | `docs/FIGSTYLE.md` + `scripts/paperlab/figstyle.py` |
| Data figure / mermaid rendering | `scripts/paperlab/make_paper_figs.py`, `scripts/paperlab/render_mermaid.py` |
| Review panel | `scripts/paperlab/review_panel.py` + `scripts/paperlab/prompts/` |

Locate the kit root via `$PAPERLAB_KIT` or ask the user on first use.

## Boot checklist (first use per session)

1. Kit root found; engines configured? (astra: `WRITER_CODEX_HOME`;
   fable: `WRITER_CREDENTIALS` — see `skills/writer-engines/SKILL.md`.
   Either engine alone is enough; if astra quota fails, fall back to fable.)
2. Agree the disclosure-log path: project `data/paper/ai_usage_log.jsonl`
   (`--log`) or default `~/.verdent/logs/writer-engines.jsonl`.
3. Confirm the project's registered results doc for fact-checking.

## Working rules (summary — full versions in the pulled skills)

- English text always via the engines; you never freestyle prose into the paper.
- Every number is checked against the registered results doc; mismatch = stop
  and ask the author. Citations stay `[CITATION NEEDED: topic]` until verified
  via API — no model-generated references.
- Figures follow `docs/FIGSTYLE.md` exactly (family colors/markers are fixed);
  data figures regenerate from data with assertions; diagrams are mermaid
  source rendered to SVG/cropped PDF; no image-gen raster in the paper.
- Report in the author's language; P0 findings first, decisions collected at
  round end; every LLM call lands in the disclosure log.
