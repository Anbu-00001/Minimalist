# AMDA — Verify-Local-First Routing Agent (AMD Developer Hackathon Act II, Track 1)

**Verify Before You Pay.** Track 1 ranks accuracy-gate survivors by total
Fireworks-metered tokens, and locally-generated tokens are scored at zero.
AMDA's only real idea: don't ask "can a bigger model answer this?" — ask
"can I *prove* my free answer is already right?" A quantized local model
answers every task first; deterministic verifiers (code execution, program
re-derivation, a CSP solver, grammar-constrained re-reads) decide whether
that free answer is provably good enough to ship. Only what fails — or, for
three categories with no cheap verifier, everything — pays for a Fireworks
call.

## Architecture

```
/input/tasks.json
      │
      ▼
 classify (keyword rules, no LLM, no tokens)         agent/classify.py
      │
      ├── factual_knowledge, NER, summarisation ──────────────────────┐
      │   (REMOTE_FIRST — no deterministic verifier exists;           │
      │    dev-measured 57% strict on the self-consistency route,     │
      │    see "Why remote-first" below)                              │
      │                                                                │
      └── math, logic, code_debug/gen, sentiment                      │
              │                                                        │
              ▼                                                        │
        local model (llama.cpp, Qwen3-4B Q4, zero token cost)          │
              │                                                        │
              ▼                                                        │
        deterministic verification          agent/verifiers.py         │
          code      → parser-oracle extract + assertion execution      │
          math      → independent program re-derivation                │
          logic     → CSP solver over an extracted translation          │
          sentiment → grammar-constrained second read                   │
              │                                                        │
              ├── pass ─────► keep local answer (0 tokens)             │
              ├── unknown ──► solver/program check, else self-consist. │
              └── fail ─────────────────────────────────────┐         │
                                                              ▼         ▼
                                                    escalate to Fireworks
                                                    (REMOTE_PREFERENCE order,
                                                     via FIREWORKS_BASE_URL only,
                                                     ALLOWED_MODELS only)
                                                              │
                                                              ▼
                                                    /output/results.json
```

Escalated math answers are re-checked by the same free local program
re-derivation before being trusted; a grounded disagreement buys one shot at
the fallback model (`agent/router.py::solve`). Remote prompts carry no local
prompt scaffolding — only the raw task plus one short format line, because
input tokens are scored too.

### Why remote-first for factual/NER/summarisation

The first real leaderboard run scored 15/19 (78.9%, one task under the
16/19 gate). Forensics (`research/leaderboard_gate_forensics.md`,
`research/VERDICTS.md` V25) pinned the miss to exactly the categories with
no deterministic verifier: a self-consistent 4B is still a 4B on world
knowledge and entity typing (57% strict on dev). Their prompts are short —
low scored-input cost — so buying a 31B-class remote answer is cheap; a long
summarisation passage is not, but the accuracy-gate is binary and worth
more than the token-rank cost (`agent/router.py` — see the `REMOTE_FIRST`
comment block for the full accounting). This is a real behavioral fork in
the code, not a diagram simplification: `category not in REMOTE_FIRST` is
the literal gate in `agent/router.py::solve`.

## Why Gemma (Track 1 side prize: "Best Use of Gemma via Fireworks — $1,000")

`agent/config.py::REMOTE_PREFERENCE` puts `gemma-4-31b-it` first, ahead of
`minimax-m3` and `kimi-k2p7-code` — and it's the reasoned choice, not the
default one. The competition scores *total* tokens, so a "smart" reasoning
model that narrates its thinking is a liability: `kimi-k2p7-code` has
thinking **architecturally mandatory** (its own model card), meaning every
call bills an unavoidable reasoning trace as scored output. Gemma-4 ships
**thinking off by default**, and the one quantitative verbosity datapoint we
found puts it at "rarely generates more than 20k tokens" against a
comparable model's 100k+ (`research/models_fireworks.md` §3, Kaitchup
benchmark) — while still leading on the benchmarks that matter for this
agent (MMLU 85.2, LiveCodeBench v6 80.0). We measured, not assumed, that
this holds under our own prompts: `research/token_thrift_audit.md` traced
real remote-call token counts and found Gemma staying well under every
per-category cap (e.g. NER: mean 19.6 output tokens against a 256 cap).
Choosing the non-reasoning model isn't a side-quest for the prize — on a
token-ranked leaderboard it's the same decision as choosing to win
(`research/VERDICTS.md` V1, V3).

## Measured results

| Metric | Value | Source |
|---|---|---|
| Accuracy, artifact-corrected | **91.1%** (51/56) on a 56-task stratified sample (7 tasks × 8 categories) | `research/final_gate_projection.md` |
| Gate probability, P(≥16/19) | **93.6%** point estimate (range 80–94% across sensitivity scenarios) | `research/final_gate_projection.md` |
| Token cost, projected 19-task run | **≈2,702 scored tokens** (142 tok/task measured on the 56-task sample) | `research/final_gate_projection.md` §"Token economics" |
| Wall-clock, projected 19-task run | **≈360s** (extrapolated from four 14-task batches: 386.3s / 238.8s / 286.4s / 148.7s under `--cpus=2 --memory=4g`), well inside the 540s/10-min budget | `research/final_gate_projection.md` |
| First real leaderboard score (pre-tilt image) | 15/19 = 78.9%, one task short of the 16/19 gate | `research/VERDICTS.md` V25, `research/leaderboard_gate_forensics.md` |

Per-category verification mechanism and the corrected score behind it:

| Category | Verifier | Corrected (56-task sample) |
|---|---|---|
| code_debugging / code_generation | parser-oracle extraction + executed assertions against the candidate's own function (`agent/verifiers.py::run_with_assertions`) | 7/7, 7/7 |
| mathematical_reasoning | independent program re-derivation, executed and compared with tolerance (`_math_program_check`) | 7/7 |
| logical_reasoning | CSP solver over an extracted declarative translation; a unique solution both verifies and can supply the answer (`solve_logic_csp`) | 5/7 (weakest category — see caveat below) |
| sentiment_classification | grammar-constrained second read must agree on the label (`_sentiment_label_agrees`) | 5/7 |
| named_entity_recognition | JSON-grammar-constrained generation + remote-first | 6/7 |
| factual_knowledge, text_summarisation | remote-first (no cheap deterministic check exists for open-ended text) | 7/7, 7/7 |

**Caveat, stated plainly for anyone auditing these numbers**: "artifact-corrected"
means every judge `fail`/`unsure` verdict was manually re-verified (code
executed, logic golds brute-forced, paraphrases read against acceptance
criteria) — the raw deterministic-judge strict score on the same sample is
33/56 = 59%, because the judge under-credits correct paraphrases and
differently-worded-but-correct logic answers. The full methodology,
per-task reasoning, and raw judge output are in
`research/final_gate_projection.md` and `eval/tmp_final_gate/`. The weakest
category (logical_reasoning) is a measured model-capability ceiling, not a
routing bug — see that file's "Weakest category" section for the probe that
ruled out a one-line fix.

## Build & run

The submitted artifact is built from this repository's `Dockerfile`, exactly:

```bash
docker buildx build --platform linux/amd64 -t ghcr.io/anbu-00001/amda-agent:latest .

docker run --rm \
  -v "$PWD/input:/input:ro" -v "$PWD/output:/output" \
  -e FIREWORKS_API_KEY -e FIREWORKS_BASE_URL -e ALLOWED_MODELS \
  ghcr.io/anbu-00001/amda-agent:latest
```

Contract: reads `/input/tasks.json` (`[{"task_id", "prompt"}]`), writes
`/output/results.json` (`[{"task_id", "answer"}]`), exits 0. All
configuration comes from the environment — nothing is hardcoded and no
secrets are baked into the image (see COMPLIANCE.md for the auditor-facing
version of this claim, with file:line references and a grep an auditor can
run themselves).

| Env var | Meaning |
|---|---|
| `FIREWORKS_API_KEY` | injected by the judging harness |
| `FIREWORKS_BASE_URL` | judging proxy — **all** remote calls route through it |
| `ALLOWED_MODELS` | comma-separated permitted model IDs, read at runtime |

**Building from source requires two large directories this repo does not
ship in git** (`.gitignore`d for size, not hidden for any other reason):
`tools/llama-b9888/` (a portable llama.cpp CPU build — the binary naming
matches the official `llama.cpp` release artifacts at
`github.com/ggml-org/llama.cpp/releases`, tag `b9888`) and `models/*.gguf`
(the local model, `Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, sourced from
`huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF`, per
`eval/gpu_bootstrap.sh`'s pinned download URL). Populate both directories
before running `docker buildx build`; without them the local-inference path
is simply absent from the image and the router falls back to remote-only
(the container is designed to degrade gracefully in exactly this case —
see `docker/entrypoint.sh`).

## Local development

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt json-repair
# optional: put FIREWORKS_API_KEY=... etc. in .env (gitignored, never shipped)

.venv/bin/python eval/parse_batches.py    # rebuild data/dev_tasks/merged.json (228 tasks)
.venv/bin/python eval/run_local.py 60     # run the agent on a 60-task subsample
.venv/bin/python eval/judge.py            # deterministic scoring of the results
```

`eval/` also contains `bench_matrix.sh` / `gpu_bootstrap.sh` for benchmarking
candidate local models on a GPU box, and `synth_tasks.py`, which generates
eval tasks with *computed* gold answers (no LLM, no wrong labels).

## Compliance summary

Full auditor dossier: **[COMPLIANCE.md](COMPLIANCE.md)**. The short version:

- Every remote call is constructed in exactly one place —
  `agent/remote.py::_get_client()` (lines 27–36) — using `base_url=
  config.FIREWORKS_BASE_URL`, which is itself read only from the
  `FIREWORKS_BASE_URL` environment variable (`agent/config.py:6`, default
  is the real `https://api.fireworks.ai/inference/v1`, never a
  hardcoded third-party endpoint). There is no second HTTP client, no
  hardcoded URL, and no code path that calls anything other than this one
  client or the loopback local model server.
- Every remote model name is filtered through `ALLOWED_MODELS`
  (`agent/router.py::pick_models`, `agent/config.py:7`) before it can be
  used — a model outside that env-supplied list is never called.
- Verify it yourself:
  ```bash
  grep -rn "http" agent/
  ```
  This returns exactly four lines: the `FIREWORKS_BASE_URL` env read (with
  its Fireworks-default fallback), the loopback-only `LOCAL_BASE_URL`
  (`http://127.0.0.1:8080/v1`, the in-container llama.cpp server — not an
  external network call), the `httpx` import, and the one `httpx.get(...)`
  call that uses it — solely to health-check that loopback server. No other
  network egress exists in `agent/`.

## Repository layout

```
agent/        the shipped agent (router, verifiers, classifier, clients)
docker/       container entrypoint
eval/         dev-set tooling: parser, judge, benchmark runners (not shipped)
data/         raw dev-task batches from multiple generators (not shipped)
research/     dated research/decision log — every routing threshold in
              agent/ traces back to a measurement recorded here
submission/   lablab.ai submission copy (description, video/slide outlines)
```

`tools/` (llama.cpp binaries) and `models/` (GGUF weights) are real
directories used by the `Dockerfile` but excluded from git via
`.gitignore` for size — see "Build & run" above for how to populate them.

## License

MIT — see [LICENSE](LICENSE).
