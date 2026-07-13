# AMDA — Local-Dominant Verified Routing Agent (AMD Developer Hackathon Act II, Track 1)

**Every token is a rank.** Track 1 ranks accuracy-gate survivors by total
Fireworks-metered tokens, and locally-generated tokens are scored at zero —
so the winning agent is the one that holds the accuracy gate while paying
nothing at all. AMDA answers **all eight categories on a local model** and
the shipped configuration spends **zero scored tokens**: for every category
it has either a zero-token way to *compute* the answer (math by program
execution, logic by CSP solver), or a measured, dev-validated local answer
format sized to finish on 2 vCPUs. A full Fireworks escalation path exists
in the code — verification-gated, proxy-only, output-capped — and is how
earlier revisions of this agent qualified; it is disabled by default
(`LOCAL_ONLY_ESCALATE=""`) because on this leaderboard a single remote call
costs more rank than a wrong answer does accuracy.

## Architecture

```
/input/tasks.json
      │
      ▼
 classify (keyword rules, no LLM, no tokens)          agent/classify.py
      │
      ├── mathematical_reasoning ── PAL program path: the local model emits
      │        a ~20-token arithmetic EXPRESSION; we execute it, honor any
      │        rounding instruction, ship the exact number + the expression
      │        as shown work. No long derivation is ever decoded. (0 tokens)
      │
      ├── factual / NER / summarisation / sentiment / logic
      │        │
      │        ▼
      │   local model (llama.cpp, Qwen3-4B Q4, 2 vCPU)
      │   per-category decode caps + answer-shape hints
      │   (caps sized so every generation FINISHES in budget)
      │        │
      │        ▼
      │   free improvers still run: logic answers are checked against a
      │   CSP solver over an extracted constraint translation — a unique
      │   solver solution OVERRIDES the free-form answer   (0 tokens)
      │
      └── code_generation / code_debugging
               │
               ▼
          local model (cap 128 tokens, fence-parity truncation guard)
               │
               ▼
          deterministic verification         agent/verifiers.py
            parser-oracle extraction → execute the candidate
               │
               ├── verified ──► ship local answer            (0 tokens)
               └── fails ─────► ship best local answer anyway (0 tokens)
                                [escalation to Fireworks exists behind
                                 LOCAL_ONLY_ESCALATE — verification-gated,
                                 FIREWORKS_BASE_URL only, ALLOWED_MODELS
                                 only, output-capped — but is OFF in the
                                 shipped image: one call = many ranks]
               │
               ▼
      /output/results.json   (written atomically after EVERY task —
                              a hard kill at any moment leaves a valid,
                              complete file; tasks are solved
                              cheapest-category-first so a deadline
                              never lands on four code tasks)
```

### Why local-dominant is safe here (the part that took a week to earn)

A 4B on 2 vCPU fails in exactly two ways, and both are *engineering*
failures, not capability walls — we measured, then fixed each:

1. **Decode-time starvation.** At ~2.5 tok/s, any generation past ~55 tokens
   used to hit the request timeout, return empty, and silently fall through
   to a paid remote call (or a truncated retry). Fix: a longer local-only
   timeout (the <30s/request rule governs *proxy* calls, not our own
   in-container server) plus per-category decode caps and terse answer-shape
   hints so every generation **finishes** — short-complete, not truncated
   (`agent/config.py::LOCAL_GEN_CAP`).
2. **Long-form reasoning it cannot afford.** Math needs a 150-250-token
   derivation the box can't decode in time — so AMDA never decodes one. The
   PAL-style program path (emit expression → execute → format) scored **7/7
   on dev math at zero tokens**, strictly better than the derivations it
   replaced (`agent/router.py::_math_local_program`).

Categories with no deterministic verifier (factual, NER, summarisation)
were remote-first in an earlier revision of this agent — that image
qualified the accuracy gate at 89.5% but paid **8,282 tokens**. The local
replacements were each re-validated on dev before this revision shipped:
factual/summarisation via terse-complete hints, NER via a completeness
hint that fixed the one real local failure mode (dropped entities — the
terse wording, not the token budget, caused it).

## The escalation path (and why Gemma leads it)

`agent/config.py::REMOTE_PREFERENCE` puts `gemma-4-31b-it` first, ahead of
`minimax-m3` and `kimi-k2p7-code` — a measured choice: the competition
scores *total* tokens, so a reasoning model that narrates its thinking is a
liability (`kimi-k2p7-code` has thinking **architecturally mandatory** per
its own model card; every call bills the trace as scored output). Gemma-4
ships thinking off by default and stayed well under every per-category cap
in our traced runs (e.g. NER: mean 19.6 output tokens against a 256 cap —
`research/token_thrift_audit.md`). This Gemma-first escalation path is how
earlier revisions of AMDA qualified on the real leaderboard (89.5% at 8,282
tokens; later 84.2% at 7,460 on a re-score). The shipped configuration
disables it (`LOCAL_ONLY_ESCALATE=""`) because the endgame leaderboard
showed a 0-token top tier — but the path is one env var away, fully
verification-gated, and everything about it (preference order, caps,
per-model behavior) is measurement-backed in `research/`.

## Measured results (shipped pure-zero configuration, 2026-07-13)

| Metric | Value | Source |
|---|---|---|
| **Scored tokens** | **0** — zero remote calls across a full 56-task stratified run (7 × 8 categories) AND a 19-task hidden-set-shaped dress rehearsal, all under `--cpus=2 --memory=4g` | `eval/tmp_cap7/`, `eval/tmp_dress/` |
| Dress rehearsal (19 tasks, hidden-set mix) | **19/19 answered in 395.9s** (~160s inside the 555s internal budget); strict-judge ceiling 18/19 | `eval/tmp_dress/run1/` |
| 56-task run, strict deterministic judge | 32 pass / 14 unsure / 10 fail (ceiling 82%) — most "unsure" are correct paraphrases the keyword judge under-credits (see caveat) | `eval/tmp_cap7/` |
| Earlier remote-first revision, real leaderboard | qualified at 89.5% / **8,282 tokens** (re-scored later at 84.2% / 7,460) — the baseline this configuration exists to beat | git history, `research/endgame_leaderboard_state.md` |

Per-category mechanism and 56-task strict-judge line (pass/fail/unsure):

| Category | Mechanism (all local, 0 tokens) | 56-task strict |
|---|---|---|
| mathematical_reasoning | expression emitted → executed → rounding honored (`_math_local_program`) | **7/7 pass** |
| logical_reasoning | capped local answer + CSP-solver check/override (`solve_logic_csp`) | **7/7 pass** |
| named_entity_recognition | completeness hint + JSON grammar when requested | 6 pass, 1 unsure |
| text_summarisation | task-limit-first hint, cap 88 | 5 pass, 2 unsure |
| sentiment_classification | label-first hint, cap 48 | 5 pass, 2 fail |
| factual_knowledge | terse-complete hint, cap 56 | 2 pass, 5 unsure (paraphrases) |
| code_generation / code_debugging | cap 128, fence-parity truncation guard, execution-verified | mostly "runs clean" unsure (see note) |

**Caveats, stated plainly for anyone auditing**: the strict judge is a
deterministic keyword/number/execution checker that under-credits correct
paraphrases ("unsure" ≠ wrong — hand-verification of earlier identical runs
found most factual/summarisation unsures to be correct, complete answers).
The code rows' 56-task numbers come from an artificially all-code 14-task
batch that deliberately over-stresses the time budget; the realistic-mix
dress rehearsal is the representative measurement. The one dress-rehearsal
hard fail was a genuine model reasoning miss on a hard-tier sequencing
puzzle (complete answer, first two elements swapped) — a measured capability
ceiling, not a routing bug.

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
