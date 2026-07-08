# AMDA — Token-Efficient Routing Agent (AMD Developer Hackathon Act II, Track 1)

A general-purpose AI agent that answers tasks across 8 capability categories
while spending as few Fireworks tokens as possible. The core idea: **a local
model's tokens are free, so every answer that can be produced and *verified*
locally should never touch the network.**

## How it works

```
/input/tasks.json
      │
      ▼
 classify (keyword rules, no LLM)          agent/classify.py
      │
      ▼
 local model first (llama.cpp, Qwen3-4B Q4, zero token cost)
      │
      ▼
 deterministic verification                agent/verifiers.py
   code        → parser-oracle extract + execute
   math        → independent program re-derivation
   logic       → constraint-solver check (CSP)
   sentiment   → grammar-constrained label re-read
   summaries   → word/sentence limits
   NER         → generated under a JSON grammar
      │
      ├── pass ──────────────► keep local answer (0 tokens)
      ├── unknown ─► program/solver check, else self-consistency
      │              (agreement → keep local, else escalate)
      └── fail ──────────────► escalate to Fireworks
                               (measured preference order,
                                via FIREWORKS_BASE_URL only)
      │
      ▼
/output/results.json
```

Escalation prefers non-reasoning models (a reasoning model's thinking trace
bills as output tokens); escalated math answers are audited by the same free
local re-derivation before being trusted, and a grounded disagreement buys
one shot at the fallback model. All remote calls go through the judging
proxy (`FIREWORKS_BASE_URL`).

## Build & run

```bash
docker buildx build --platform linux/amd64 -t ghcr.io/anbu-00001/amda-agent:latest .

docker run --rm \
  -v "$PWD/input:/input:ro" -v "$PWD/output:/output" \
  -e FIREWORKS_API_KEY -e FIREWORKS_BASE_URL -e ALLOWED_MODELS \
  ghcr.io/anbu-00001/amda-agent:latest
```

Contract: reads `/input/tasks.json` (`[{"task_id", "prompt"}]`), writes
`/output/results.json` (`[{"task_id", "answer"}]`), exits 0. All configuration
comes from the environment — nothing is hardcoded and no secrets are baked
into the image.

| Env var | Meaning |
|---|---|
| `FIREWORKS_API_KEY` | injected by the judging harness |
| `FIREWORKS_BASE_URL` | judging proxy — **all** remote calls route through it |
| `ALLOWED_MODELS` | comma-separated permitted model IDs, read at runtime |

The image bakes in llama.cpp (CPU build) plus quantized local weights under
`/models/`; the entrypoint boots the local server and the router degrades to
remote-only if it is unavailable.

## Local development

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt json-repair
# optional: put FIREWORKS_API_KEY=... etc. in .env (never shipped)

.venv/bin/python eval/parse_batches.py    # rebuild data/dev_tasks/merged.json (228 tasks)
.venv/bin/python eval/run_local.py 60     # run the agent on a 60-task subsample
.venv/bin/python eval/judge.py            # deterministic scoring of the results
```

`eval/` also contains `bench_matrix.sh` / `gpu_bootstrap.sh` for benchmarking
candidate local models on a GPU box, and `synth_tasks.py`, which generates
eval tasks with *computed* gold answers (no LLM, no wrong labels).

## Repository layout

```
agent/        the shipped agent (router, verifiers, classifier, clients)
docker/       container entrypoint
eval/         dev-set tooling: parser, judge, benchmark runners (not shipped)
data/         raw dev-task batches from multiple generators (not shipped)
```

## License

MIT — see [LICENSE](LICENSE).
