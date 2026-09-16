#!/usr/bin/env python3
"""Dispatch a single LLM call to the writer engines (global, credential-free).

Engines
  astra : gpt-6-astra via the local vendor-specific Codex relay copy
          (`codex exec -` reads the prompt on stdin; CODEX_HOME comes from
          $WRITER_CODEX_HOME, default ${WRITER_CODEX_HOME:-~/.codex-writer})
  fable : claude-fable-5 via any OpenAI-compatible endpoint
          (credentials file $WRITER_CREDENTIALS, default
          ~/paperlab-keys/credentials.json, entry "fable"; loaded at runtime,
          never printed or written anywhere)

No credential lives in this file, in the skill docs, or in the usage log.

Usage
  call_model.py --engine fable [--system FILE] --prompt FILE|-- - --out OUT.md
      [--task tag] [--model NAME] [--max-tokens N] [--temperature 0.3]
      [--timeout 900] [--log PATH]

--system / --prompt accept a file path or `-` (stdin). The response is written
to --out and echoed on stdout; a status line goes to stderr.

Every call appends one JSONL line to the usage log -- default
~/.verdent/logs/writer-engines.jsonl, or --log PATH for a project-local
AI-disclosure log (paper projects pass --log <project>/data/paper/ai_usage_log.jsonl).
The log records engine/model/task/sizes only -- never credentials.
"""
import argparse
import contextlib
import datetime
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

LOG_DEFAULT = Path.home() / ".verdent" / "logs" / "writer-engines.jsonl"
CRED_FILE = Path(os.environ.get(
    "WRITER_CREDENTIALS",
    str(Path.home() / "paperlab-keys/credentials.json")))

DEFAULTS = {"astra": "gpt-6-astra", "fable": "claude-fable-5"}


def _read_src(spec: str) -> str:
    if spec == "-":
        return sys.stdin.read()
    return Path(spec).read_text()


def call_astra(prompt: str, *, model: str, timeout: float) -> str:
    home = os.path.expanduser(os.environ.get("WRITER_CODEX_HOME", "${WRITER_CODEX_HOME:-~/.codex-writer}"))
    fd, out_path = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    try:
        cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "read-only",
               "-m", model, "--output-last-message", out_path, "-"]
        proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True,
                              timeout=timeout, env={**os.environ, "CODEX_HOME": home})
        out = Path(out_path)
        last = out.read_text().strip() if out.exists() else ""
        if proc.returncode != 0 or not last:
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-2:]
            raise RuntimeError(f"codex exec rc={proc.returncode}: {' | '.join(tail)}")
        return last
    finally:
        with contextlib.suppress(OSError):
            os.unlink(out_path)


def call_fable(prompt: str, *, model: str, system: str, max_tokens,
               temperature: float, timeout: float) -> str:
    key_doc = json.loads(CRED_FILE.read_text())
    cred = key_doc["fable"]
    messages = ([{"role": "system", "content": system}] if system else [])
    messages.append({"role": "user", "content": prompt})
    body = {"model": model, "messages": messages, "temperature": temperature}
    if max_tokens is not None:  # default: no cap (agent-calling convention)
        body["max_tokens"] = max_tokens
    req = urllib.request.Request(
        cred["base_url"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + cred["api_key"],
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        r = json.load(resp)
    choice = r["choices"][0]
    content = choice["message"]["content"] or ""
    if choice.get("finish_reason") == "length":
        content += "\n\n<!-- TRUNCATED finish_reason=length; raise --max-tokens -->"
    return content


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--engine", required=True, choices=sorted(DEFAULTS))
    ap.add_argument("--model", default=None, help="override the engine's default model name")
    ap.add_argument("--system", default=None, help="system prompt file or '-' (fable only)")
    ap.add_argument("--prompt", required=True, help="user prompt file or '-' (stdin)")
    ap.add_argument("--out", required=True, help="path to write the response to")
    ap.add_argument("--task", default="unspecified", help="short tag for the usage log")
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="do NOT set by default: an explicit cap truncates reasoning "
                         "models mid-thought (finish_reason=length).")
    ap.add_argument("--temperature", type=float, default=0.3)
    ap.add_argument("--timeout", type=float, default=900.0)
    ap.add_argument("--log", default=str(LOG_DEFAULT),
                    help="JSONL usage log path (project-local disclosure logs welcome)")
    args = ap.parse_args()

    model = args.model or DEFAULTS[args.engine]
    prompt = _read_src(args.prompt)
    system = _read_src(args.system).strip() if args.system else ""
    t0 = datetime.datetime.now(datetime.timezone.utc)
    ok, err = True, None
    try:
        if args.engine == "astra":
            if system:
                prompt = system + "\n\n=====\n\n" + prompt  # codex exec has no system slot
            text = call_astra(prompt, model=model, timeout=args.timeout)
        else:
            text = call_fable(prompt, model=model, system=system,
                              max_tokens=args.max_tokens,
                              temperature=args.temperature, timeout=args.timeout)
    except Exception as e:  # noqa: BLE001 - report and log any failure
        ok, err, text = False, repr(e), ""
    dt = (datetime.datetime.now(datetime.timezone.utc) - t0).total_seconds()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    log = Path(args.log).expanduser()
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as f:
        f.write(json.dumps({
            "ts": t0.isoformat(timespec="seconds"), "engine": args.engine,
            "model": model, "task": args.task, "ok": ok, "error": err,
            "prompt_chars": len(prompt), "out_chars": len(text),
            "seconds": round(dt, 1), "out": str(args.out),
        }) + "\n")

    if ok:
        print(f"[writer-engines] {args.engine}:{model} -> {out} ({len(text)} chars, {dt:.0f}s)",
              file=sys.stderr)
        print(text)
        return 0
    print(f"[writer-engines] FAILED {args.engine}:{model}: {err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
