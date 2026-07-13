# COMPLIANCE.md — auditor dossier

One page. Every claim below points at a file:line an auditor can open, or a
command an auditor can run against this exact repository.

## 1. Endpoint inventory

There are exactly two HTTP clients in `agent/`, and no other network code.

| Client | Constructed at | Target | Source of the target |
|---|---|---|---|
| Fireworks (remote) | `agent/remote.py:27-36`, `_get_client()` | `config.FIREWORKS_BASE_URL` | `agent/config.py:6` — `os.environ.get("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")`. Env var wins if set; the fallback is the real Fireworks endpoint, never a third party. |
| Local (llama.cpp, in-container) | `agent/local_llm.py:25-34`, `_get_client()` | `config.LOCAL_BASE_URL` | `agent/config.py:40` — `os.environ.get("LOCAL_BASE_URL", "http://127.0.0.1:8080/v1")`. Loopback only; the server it talks to is started by `docker/entrypoint.sh` inside the same container. Not external egress. |

Both clients are the OpenAI Python SDK pointed at different `base_url`
values — this is the standard way to speak to an OpenAI-compatible server
(which both Fireworks and llama.cpp's server expose) and is not a second
provider integration.

**Model allow-list**: `agent/router.py::pick_models` (line 62) intersects
the category's preference order with `config.ALLOWED_MODELS`
(`agent/config.py:7` — parsed from the `ALLOWED_MODELS` env var) before any
model name reaches `remote.complete()`. If none of the preferred models are
in the allow-list, it falls back to whatever *is* allowed, never to an
unlisted model. A model name outside `ALLOWED_MODELS` is structurally
unreachable.

**Reproduce this section yourself:**

```bash
grep -rn "http" agent/
```

Expected output (verified against this repo's current `agent/` tree):

```
agent/config.py:6:FIREWORKS_BASE_URL = os.environ.get("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")
agent/config.py:40:LOCAL_BASE_URL = os.environ.get("LOCAL_BASE_URL", "http://127.0.0.1:8080/v1")
agent/local_llm.py:5:import httpx
agent/local_llm.py:18:            httpx.get(config.LOCAL_BASE_URL.replace("/v1", "/health"), timeout=2.0)
```

Four lines, all accounted for above. No `requests`, `urllib`, `socket`, or
`aiohttp` import anywhere in `agent/` (`grep -rn "import requests\|urllib\|socket\.\|aiohttp" agent/` returns nothing).

## 2. Token spend by category, and why

All remote calls carry a fixed overhead (`SYSTEM` message + `REMOTE_SUFFIX`,
~25 tokens) plus a per-category cap (`agent/config.py::REMOTE_MAX_TOKENS`);
measured real generations never approach the cap (`research/token_thrift_audit.md`
§3: factual_knowledge 63% of cap, NER 17%, summarisation 44%, at most).

| Category | Routing | Why |
|---|---|---|
| mathematical_reasoning | local program path, never remote (`agent/router.py::_math_local_program`) | The local model emits a short arithmetic expression; we execute it and ship the exact value (rounding instructions honored). 7/7 on dev at zero tokens — the answer is computed, not generated. |
| factual_knowledge, named_entity_recognition, text_summarisation, sentiment_classification, logical_reasoning | local, ships local (`LOCAL_ONLY=1`, baked into the image) | Per-category decode caps + answer-shape hints make the local answer short-COMPLETE (`agent/config.py::LOCAL_GEN_CAP`); logic answers are additionally checked against a CSP solver whose unique solution can override them. Each local replacement was re-validated on dev against the earlier remote-first configuration before shipping (see git history: that configuration held the gate at 89.5% but paid 8,282 tokens). |
| code_generation, code_debugging | local-first, escalate ONLY on verification failure (`LOCAL_ONLY_ESCALATE`) | Executed extraction + model-written assertions + a fence-parity truncation guard decide; only a demonstrably failed code answer pays for one Fireworks call (single model, output hard-capped at `CODE_CAP`). This is the only code path in the agent that can spend scored tokens. |

Measured cost (56-task graded dev sample, 4 batches under judging-VM
constraints `--cpus=2 --memory=4g`): **every category except code at 0
scored tokens**; the entire dev bill was the code-escalation calls. The
worst-case hidden-eval projection is a small number of code escalations
(~230 measured tokens per call on dev); zero escalations — a genuinely
free run — is the expected mode when local code answers verify.

## 3. Dev-time remote stand-in — what it is, and why it isn't in the image

During development, remote-path testing used a Cerebras-hosted OpenAI-compatible
endpoint as a rate-limited stand-in for the real Fireworks judging proxy
(`research/VERDICTS.md` V8) — cheaper to iterate against, same request
shape. Its credentials live in a single local file, `.env`, in this format:

```
FIREWORKS_API_KEY=<dev key>
FIREWORKS_BASE_URL=https://api.cerebras.ai/v1
ALLOWED_MODELS=gemma-4-31b
```

**This file is never read by the shipped image.** The `Dockerfile` does not
`COPY` it, `.dockerignore` excludes it, and `agent/config.py` only ever
reads these three names from the process environment at container runtime —
whatever the judging harness injects (real `FIREWORKS_API_KEY` /
`FIREWORKS_BASE_URL` / `ALLOWED_MODELS`) is what the agent uses. `.env` is a
convenience for `.venv/bin/python eval/run_local.py`-style local runs only.

**Verification performed for this dossier:**

- `.env` is listed in `.gitignore` (`# environments & secrets` section) and
  `git ls-files | grep -i '\.env'` returns nothing — it has never been
  tracked.
- `git log -p -- .env` returns empty output — no commit in this repository's
  history has ever touched a file at that path, tracked or otherwise.
- A full-history scan (`git rev-list --all` piped through `git grep` for the
  dev key's literal prefix, and separately for generic
  `api_key=`/`secret=`/`token=`-shaped assignments across every blob in
  every commit) found **no occurrence of the dev Fireworks/Cerebras key
  anywhere in git history.** (Key value itself intentionally not reproduced
  in this document.)

**One unrelated finding from the same history scan, flagged here because
the scan surfaced it:** `research/top5_forensics.md`, introduced in commit
`2102e09` ("Support math percent/fraction equivalence and add competitor
research") and unchanged in every commit since (present verbatim in
`77d9c58`, `f4d5353`, and current `HEAD` `97c6c23`), quotes — verbatim and
in full, at line 119 — a live-looking Google Gemini API key (`AIzaSy...`,
39 chars) that a **different team** hardcoded in their own public GitHub
repo. It's reproduced there as evidence for that team's
non-Fireworks-routing DQ pattern (direct, undisclosed calls to
`generativelanguage.googleapis.com`, overwriting the Fireworks answer). It
is **not AMDA's key** and does not enable any call this agent makes. It is
still a live plaintext credential sitting in this soon-to-be-public repo,
republished from someone else's leak — worth redacting to a truncated form
before the repo goes public, both as good practice and so a skimming
auditor cannot mistake it for AMDA's own credential. Recommend redacting
`research/top5_forensics.md:119` to something like `AIzaSy...REDACTED`
before publishing; the forensic point (that the key is hardcoded and live)
survives the redaction intact.

## 4. Image provenance

- Built from this repository's `Dockerfile` (linux/amd64, `python:3.12-slim`
  base), tag `ghcr.io/anbu-00001/amda-agent:latest`.
- The measured/graded image (`research/final_gate_projection.md`,
  `research/verify_local_decision.md`) is recorded as local Docker image ID
  `fb43f519`, built from commit `f4d5353`, which is exactly **one** commit
  behind current `HEAD` (`git log --oneline f4d5353..HEAD` shows only
  `97c6c23`). That one commit touches `research/` only —
  `git diff f4d5353 HEAD --stat -- agent/ Dockerfile requirements.txt
  docker/` is empty — so this digest still accurately describes the code
  currently in the image; nothing under `agent/`, the `Dockerfile`, or
  `docker/` has changed since it was built.
- Note on precision: `fb43f519` (like `1c3d756b2439` recorded earlier in
  `research/remote_path_validation.md`) is a **local Docker image ID**
  captured at build/measurement time — the short form `docker images`
  reports — not a registry-pushed `sha256:` manifest digest. GHCR
  publication status (and therefore the registry digest an auditor would
  see from `docker manifest inspect`) is tracked as a submission-time TODO
  in `submission/DESCRIPTIONS.md` ("flip package to PUBLIC before
  submitting"); confirm current publication state there before citing this
  ID as the live registry digest.
- Building the image from a fresh clone requires populating two large,
  git-ignored directories (`tools/llama-b9888/`, `models/*.gguf`) not
  committed to this repo for size — see README.md § "Build & run" for
  exact source URLs. Without them, the image still builds and runs; it
  simply has no local model, so every task escalates to Fireworks
  (`docker/entrypoint.sh`'s documented degrade-gracefully behavior).

## 5. What this document is not

This is a static-analysis dossier: it describes what the code in this repo
does and where. It does not certify runtime network behavior (e.g. via a
packet capture) — an auditor wanting that level of proof should run the
container under `docker run --network` restrictions or a proxy that only
allow-lists `FIREWORKS_BASE_URL`, and confirm no other destination is ever
contacted. The `grep` command in §1 is offered as the fast, reproducible
first check; it is not a substitute for that deeper audit if one is
warranted.
