---
name: research-skills
description: Router into the vendored Orchestra AI-Research-SKILLs library (12.7k stars, MIT, v1.7.2). Pulls and routes the right sub-skill on demand for ML paper writing (NeurIPS/ICML/ICLR/ACL), academic plotting, conference talks, and research ideation. Use when the user asks to draft/revise/structure a paper, write an abstract or related work, make publication figures, prepare a talk or poster, brainstorm research ideas, or says 写论文 / 润色 / 摘要 / 画图 / 投稿 / talk / ICLR / NeurIPS. Do not preload sub-skills; pull only what the task needs.
---

# research-skills — Orchestra library router

Single entry point into the vendored Orchestra AI-Research-SKILLs repo. The user
curates aggressively: modern models do not need 87 skills registered, so this
router exposes a small Tier-1 set and pulls sub-skill content only on demand.

- Vendored at: `~/.verdent/vendor/AI-Research-SKILLs` (12,723 stars, MIT,
  HEAD 773a529 = v1.7.2, 2026-06-15)
- Update policy: before heavy use, if HEAD is older than ~30 days run
  `git -C ~/.verdent/vendor/AI-Research-SKILLs pull --ff-only` and re-check
  `git log -1`. Trust ONLY this upstream; before vendoring any other skill
  source, verify stars (very high), recency, and license first (user rule).

## Pull protocol (never preload)

1. Match the task to ONE route below.
2. Read that sub-skill's `SKILL.md` (and only the specific `references/*.md`
   file it points to for the task at hand).
3. Execute the task following that sub-skill's workflow.

## Tier-1 routes (curated)

| Task | Pull from (under `20-ml-paper-writing/`) | Notes |
|---|---|---|
| Draft / revise / structure an ML paper; abstract; intro; related work; checklists; camera-ready | `ml-paper-writing/SKILL.md` | Writing philosophy (Nanda narrative, Farquhar 5-sentence abstract, Gopen & Swan); venue checklists; LaTeX templates in `ml-paper-writing/templates/` (incl. `iclr2026`) |
| Citations / BibTeX / literature lookup | `ml-paper-writing/references/citation-workflow.md` | Absolute rule: never generate BibTeX from memory — verify via API, else mark `[CITATION NEEDED: topic]` |
| Publication figures / plots | `academic-plotting/SKILL.md` | matplotlib/seaborn venue styling, diagram workflows |
| Conference talk / poster / slides | `presenting-conference-talks/SKILL.md` | Use after acceptance or for practice talks |
| Systems-venue paper (OSDI/NSDI/ASPLOS/SOSP) | `systems-paper-writing/SKILL.md` | Not for ICLR-track work |
| Research idea brainstorming (post-deadline) | `21-research-ideation/<sub-skill>/SKILL.md` | Not during a submission sprint |

Everything else in the vendored repo (categories 01-19, 22) is Tier-2: browse
by listing the repo root ONLY when a task clearly maps to a category; do not
register or read them speculatively.

## Engine routing (project context)

When working inside `ca-worldmodels`, this router supplies the WRITING GUIDANCE;
prose production still goes through the project's two-layer protocol: dispatch
to astra/fable via `scripts/paperlab/call_model.py`, fact-check every number
against `docs/RESULTS.md`, and report to the author in Chinese (see project
skills `paper-en` / `paper-review`). Outside that project, follow the sub-skill
directly with your own capabilities.
