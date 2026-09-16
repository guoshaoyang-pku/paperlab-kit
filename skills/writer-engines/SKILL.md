---
name: writer-engines
description: Credential-free dispatcher for the external writer engines — astra (gpt-6-astra via a local Codex relay copy) and fable (claude-fable-5 via any user-supplied OpenAI-compatible endpoint). Use when the user asks to draft, polish, or review English text using astra or fable, to use codex relay copy or eval-key models as sub-writers, or says 用astra / 用fable / 下层模型 / 引擎调用. This skill is the WHO-writes layer; the research-skills router is the HOW-to-write layer. No credentials are stored here.
---

# writer-engines — global engine dispatcher

The bottom layer of the two-tier writing protocol: the current agent orchestrates,
fact-checks, and reports to the user (Chinese when they speak Chinese); the engines
below produce the English prose. Guidance on WHAT good prose looks like comes from
the `research-skills` router (Orchestra library) — put relevant guidance excerpts
into the engine brief instead of letting engines freestyle.

## Engines

| Engine | Default model | Channel | Best for |
|---|---|---|---|
| astra | gpt-6-astra | `codex exec -` with CODEX_HOME `${WRITER_CODEX_HOME:-~/.codex-writer}` (local relay) | bulk drafting, long sections |
| fable | claude-fable-5 | any OpenAI-compatible endpoint (credentials file, below) | polish, critique, review panels |

If astra returns an empty stream or quota errors (the relay's upstream credentials
rate-limited), fall back to fable for that call.

## Dispatch

    python3 ~/.verdent/skills/writer-engines/scripts/call_model.py \
        --engine astra --prompt brief.md --out draft.md --task draft:intro

- `--prompt -` reads the brief on stdin (large prompts safe).
- `--system FILE` (fable only) sets a system prompt.
- `--model` overrides the default model name; `--max-tokens` is unset by default
  (an explicit cap truncates reasoning models mid-thought).
- Every call appends one JSONL line to the usage log: default
  `~/.verdent/logs/writer-engines.jsonl`, or `--log PATH` for a project-local
  AI-disclosure log (paper projects use `data/paper/ai_usage_log.jsonl`).

## Credential policy (binding)

- No key, token, or credential may ever be written into a skill file, a repo,
  chat output, or the usage log.
- astra: credentials live inside `${WRITER_CODEX_HOME:-~/.codex-writer}/` and are consumed by `codex`
  itself; the script never reads them. Override the home with `WRITER_CODEX_HOME`.
- fable: credentials are read at runtime from the JSON file named by
  `$WRITER_CREDENTIALS` (any path and filename you choose; template
  `keys/credentials.example.json`, entry `fable`) and never echoed.
- The usage log records engine/model/task/sizes/timing only.

## Two-tier protocol (any project)

1. Turn the user's intent into an English brief: message of the section, the exact
   numbers with their source doc, constraints, what NOT to say, plus any Orchestra
   guidance excerpts pulled via `research-skills`.
2. Dispatch with the command above; independent sections can run as parallel calls.
3. Fact-check the output yourself before showing the user: every number must match
   the project's results docs; citations stay `[CITATION NEEDED: topic]` until a
   real reference is verified — engines never invent references.
4. Report in the user's language; collect decisions that need the author.

In a paper project, a thin project-level skill (like the bundled `paperlab`
master) orchestrates this dispatcher with repo-specific rules — results-doc
fact-checking, house style, disclosure log path.
