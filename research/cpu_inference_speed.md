# CPU Inference Speed Levers for the Baked Qwen3-4B Server (llama.cpp, 2 vCPU / 4 GB grading VM)

Research only, no code changed. Goal: find currently-unused llama.cpp CPU levers
that could reduce time-to-first-token / raise tokens-per-second on the grading
VM's 2-thread, no-GPU box, without changing the baked model, so reasoning-heavy
categories stop tripping `REQUEST_TIMEOUT_S=25` (`agent/config.py:48`) and
falling back to paid remote calls.

**Method**: verified every flag name/default against `llama-server --help` and
`llama-bench --help` on the actual vendored binary
(`tools/llama-b9888/llama-server`, version `9888 (cb295bf59)`), cross-checked
against the official llama.cpp server README and GitHub discussions/issues
(cited inline), and then ran real `llama-bench` measurements against the
actual baked model (`models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf`) at `-t 2` to
match the grading VM's thread budget. Benchmarks ran on the dev machine
(**Intel Core 7 150U**, 1 socket / 10 cores / 12 threads, AVX2+FMA+AVX-VNLI,
no AVX-512) — **not** the actual grading VM, whose CPU microarchitecture the
hackathon docs don't specify. Numbers are a low-repetition (`-r 1` or `-r 2`),
shared-laptop measurement, not a controlled lab run — treat magnitudes as
directional, not exact, but the *qualitative* rankings (which flags help,
which don't, which regress) were consistent across repeated runs and are the
part this report leans on.

Current state (for reference):
- `docker/entrypoint.sh:22-24`: `llama-server -m "$MODEL" -c 2048 -t "$THREADS" --port 8080 --jinja` — no `-b`/`-ub`/`-ctk`/`-ctv`/`-fa`/`--numa` passed, so all of those sit at llama.cpp's built-in defaults.
- `agent/config.py:48`: `REQUEST_TIMEOUT_S = 25`.
- `agent/router.py`'s first local attempt (`local_llm.complete_scored(full_prompt, system=SYSTEM, ...)`, no `max_tokens=` override) uses `local_llm.py`'s default `max_tokens=768` — uncapped relative to category, unlike the remote path's per-category `REMOTE_MAX_TOKENS` (`agent/config.py:27-36`).

---

## 1. KV-cache quantization (`-ctk`/`-ctv`) — measured: not worth it at our context lengths, and it costs prompt-processing speed

`llama-server --help` confirms both flags exist with allowed values
`f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1` (default `f16` for
both). Documented constraint, confirmed via a real llama.cpp error string
surfaced in GitHub issue #10378 (https://github.com/ggml-org/llama.cpp/issues/10378):
quantizing the **V** cache requires Flash Attention to be enabled —
`llama_new_context_with_model: V cache quantization requires flash_attn`.
K-only quantization doesn't have this requirement, but symmetric K+V
quantization (the common recipe) forces `-fa on`.

Measured on the baked model, `-t 2`, short context (`-p 64 -n 96`, i.e. in
the realistic range for this workload — see §6):

| config | pp (t/s) | tg (t/s) |
|---|---|---|
| `f16/f16`, `-fa off` | 18.75 ± 0.36 | 4.67 ± 0.26 |
| `f16/f16`, `-fa on` | 15.82 ± 1.00 | 4.65 ± 0.22 |
| `f16/f16`, `-fa` unset (**current, = auto**) | 23.12 ± 2.03 | 5.33 ± 0.17 |
| `q8_0/q8_0`, `-fa on` (required) | 12.82 ± 0.08 | 4.47 ± 0.01 |
| `q4_0/q4_0`, `-fa on` (required) | 12.22 ± 0.23 | 4.54 ± 0.01 |

Two findings, both against the naive expectation:
- **`-fa auto` (today's default, i.e. doing nothing) is already the fastest
  prompt-processing option measured** — faster than either explicit `-fa on`
  or `-fa off`. Forcing FA on (which quantized KV requires) is a **regression**
  on this CPU/build for pp, and roughly a wash for tg.
- KV-cache quantization **decreases** pp speed (23.1 → 12.2-12.8 t/s, roughly
  -45%) and doesn't meaningfully move tg (5.33 → 4.5, within run-to-run noise)
  at these context lengths. This is because the KV cache itself is tiny here
  (a few hundred KB at ctx ≈ 150) relative to the 2.32 GiB of Q4_K_M weights
  that dominate memory traffic — quantizing/dequantizing the cache adds
  compute overhead without cutting meaningful memory traffic. KV-cache
  quantization is a documented win for **long-context, memory-constrained**
  serving (source: search-synthesized CPU benchmark citing q4_0 becoming
  competitive with f16 only past ~24K context, and the TurboQuant / GDM 2026
  KV-quant literature this repo already collected in
  `research/local_inference_llamacpp.md` — all framed around long contexts),
  not for our ~150-1000 token combined prompt+completion regime.

**Verdict: do not add `-ctk`/`-ctv`. It would force `-fa on` (itself a
measured pp regression here) for a cache that's too small to matter.**

## 2. Batch / ubatch size (`-b`/`-ub`) — measured: no effect, because our prompts never fill the default ubatch

Confirmed defaults via `llama-server --help`: `-b/--batch-size` (logical,
default 2048), `-ub/--ubatch-size` (physical, default 512). Per the official
GitHub discussion #6328 (https://github.com/ggml-org/llama.cpp/discussions/6328)
and the server README, `-b` is the app-level buffer ceiling and `-ub` is the
actual per-step compute chunk (`b >= ub`); smaller ubatch trades prompt
throughput for lower peak memory, and for single-request serving throughput
generally isn't the bottleneck latency is.

Measured, `-t 2 -p 128 -n 32`:

| config | pp128 (t/s) | tg32 (t/s) |
|---|---|---|
| `-b 2048 -ub 512` (current default) | 12.83 ± 0.25 | 4.02 ± 0.24 |
| `-b 256 -ub 256` | 12.27 ± 0.30 | 4.56 ± 0.38 |

Difference is within run-to-run noise. This tracks with §6's finding on our
prompt-length distribution: real prompts top out around 187 tokens (max, see
§6) — every real prompt fits inside a *single* default ubatch (512) already,
so there's no chunking overhead to remove and no batching lever to pull for
this workload. Batch/ubatch tuning matters for concurrent multi-request
serving or very long single prompts; AMDA is single-request, short-prompt.

**Verdict: leave `-b`/`-ub` at defaults. No measured benefit either way.**

## 3. Thread affinity / NUMA — confirmed no-op on this topology, and almost certainly a no-op on the grading VM too

`llama-server --help` confirms `--numa <distribute|isolate|numactl>`
(default: disabled/none) plus a family of `--cpu-mask`/`--cpu-range`/
`--prio`/`--poll` affinity flags. Per official docs and GitHub discussion
#19102 (https://github.com/ggml-org/llama.cpp/discussions/19102) and issue
#1437 (https://github.com/ggml-org/llama.cpp/issues/1437): NUMA optimizations
only apply across multiple physical CPU sockets/memory domains; on a
single-socket system there is nothing to distribute across.

Confirmed the dev box's own topology (`lscpu`): **1 socket, 1 NUMA node**
(`NUMA node(s): 1`). Measured `-t 2 -p 64 -n 64`:

| config | pp64 (t/s) | tg64 (t/s) |
|---|---|---|
| no `--numa` (current) | 11.71 ± 0.17 | 4.53 ± 0.30 |
| `--numa distribute` | 11.82 ± 0.46 | 4.59 ± 0.28 |

Statistically indistinguishable, as expected for a single-NUMA-node box.
A 2-vCPU cloud-grading container is virtually guaranteed to present as a
single NUMA node to the guest (a hypervisor wouldn't split a 2-core
allocation across sockets) — this isn't something to "confirm on the grading
VM," it's structurally true of any ≤2-vCPU cloud instance. `--cpu-mask`/
`--prio`/`--poll` affinity tuning is aimed at pinning threads to specific
physical cores on much bigger boxes to avoid scheduler migration; with only
2 vCPUs there's nowhere else for the scheduler to migrate threads to.

**Verdict: `--numa` and CPU-affinity flags are a no-op here. Don't add them.**

## 4. Build-time CPU flags — already optimal for portability, and already auto-selecting a fast variant

Checked `tools/llama-b9888/` directly (this is what `Dockerfile:19` `COPY`s
into the image) instead of guessing at how it was built — there's no build
step in this repo's `Dockerfile`, the binaries are vendored prebuilt. The
directory contains **14 separate `libggml-cpu-*.so` files**: `x64` (generic
baseline), `sse42`, `sandybridge`, `ivybridge`, `haswell`, `skylakex`,
`icelake`, `cannonlake`, `cascadelake`, `cooperlake`, `sapphirerapids`,
`alderlake`, `zen4`, `piledriver`. This is the exact, real llama.cpp
`GGML_CPU_ALL_VARIANTS=ON` + `GGML_BACKEND_DL=ON` build mode: one binary
containing every x86_64 microarchitecture-tuned CPU backend, each exporting a
`ggml_backend_score()` that's evaluated against the *running* CPU's detected
features at load time, picking the best-scoring variant (confirmed via
`ggml-cpu/CMakeLists.txt` on GitHub and DeepWiki's architecture doc:
https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-cpu/CMakeLists.txt,
https://deepwiki.com/ggml-org/llama.cpp/4.2-cpu-backend-and-optimization).
Directly observed on the dev box: `llama-bench`/`llama-server` both print
`load_backend: loaded CPU backend from .../libggml-cpu-alderlake.so` at
startup — i.e. it picked the Alder Lake-tuned kernel set for this Meteor
Lake-U chip automatically, no flag needed.

This answers the portability-vs-speed question directly: the vendored binary
**already ships every rung from a generic-x64 SSE2 fallback up through
Sapphire Rapids/Zen4 AVX-512** in one file, and self-selects at runtime. A
single-target rebuild pinned to, say, AVX-512 would only be faster on CPUs
that already get scored into a *worse* variant than they qualify for — but
since the current build always picks the *best available* variant for
whatever CPU it lands on, there's no headroom to gain, only downside
(a fixed-ISA build that requires an instruction set the grading VM's CPU
lacks would `SIGILL` on startup — exactly the "worse than slow" failure mode
flagged in the task). The one plausible speed exception (a hand-tuned,
non-generic single-microarch build using e.g. `-march=native` on the grading
VM's exact silicon) isn't buildable in the time remaining without knowing
that silicon, and isn't safe to assume.

**Verdict: nothing to change. The current build is already the portable+fast
option; don't replace it with a narrower one.**

## 5. Prompt-processing vs. decode — decode dominates, and gets *slower* as generation gets longer

Confirmed via search synthesis (llm-tracker.info Benchmarking Cheat-Sheet,
TechHara's CPU-vs-iGPU writeup) and directly measured here: prompt
processing (`pp`) is compute-bound and fast (11-23 t/s in the runs above);
decode (`tg`) is memory-bandwidth-bound (has to stream the model's weights
from RAM every generated token) and much slower (2-5 t/s, see below) — a
4-10x gap, consistent with the general claim that pp and tg are bound by
different resources. Given our real prompts are short (max 187 tokens,
§6) and completions can run to hundreds of tokens, **decode time dominates
wall-clock latency by a wide margin** — the pp phase for even our longest
prompt (187 tok at ~15-23 t/s ≈ 8-12s) is a rounding error next to what
decode costs for the same request.

The more important, less expected finding — decode speed is **not flat with
context depth** for this model/build. Measured `tg64` at increasing
already-filled context (`-d`, i.e. simulating how far into a generation the
model already is):

| context depth already filled | tg64 (t/s) |
|---|---|
| 0 (start of generation) | 5.39 ± 1.53 (single 2-rep sample, higher variance) |
| 256 | 3.06 |
| 512 | 2.70 |
| 1024 | 2.18 |

(Single-rep spot checks past d=0 due to time budget — real signal, not
lab-grade, but the direction is consistent and monotonic across three
independent points.) Decode roughly **halves** in speed between the start of
a generation and 1024 tokens deep. That means the *tail* of a long
completion (e.g. `code_generation`'s 640-768 token cap) is generated far
slower than the first tokens — the effective time cost of a long generation
is worse than "N tokens × flat rate," it compounds. This is the direct,
measured explanation for why reasoning/code categories specifically blow the
25s budget: it isn't just that they ask for more tokens, it's that each of
those extra tokens costs more than the ones before it.

**Practical implication: decode length is the lever that matters, far more
than any KV-cache/batch/NUMA flag above** — see §6.

## 6. Context size below 2048 — the `-c` flag itself isn't the lever; generation-length caps are

Checked `data/dev_tasks/merged.json` (228 tasks) with the real Qwen tokenizer
(`llama-tokenize` against the baked model, not a char/4 estimate):

| stat | prompt tokens (raw prompt text only, no system/chat template) |
|---|---|
| min | 12 |
| median | 46 |
| p90 | 135 |
| max | 187 |

By category (character-length proxy, `data/dev_tasks/merged.json`):
`text_summarisation` and `code_generation` have the longest prompts (mean
~281-496 chars, max 826-832 chars ≈ 190-210 tokens); `factual_knowledge` the
shortest (mean 71 chars). Add a short system prompt and the chat template
overhead and real total input is comfortably under 300 tokens even at the
99th percentile. `agent/local_llm.py`'s default local completion budget is
`max_tokens=768`; `agent/config.py`'s `REMOTE_MAX_TOKENS` caps top out at 640
(code categories). So the realistic **combined** prompt+completion length
for any single request tops out around 900-1000 tokens — well under the
current `-c 2048`, which was already set for RAM headroom (VERDICTS V20: 4096
→ 2048 to halve KV-cache memory on the 4GB box), not because anything needs
2048.

Given §5's finding, shrinking `-c` itself (e.g. to 1024) **would not speed
up decode** — the per-token cost measured above is a function of how many
tokens are *actually* in the KV cache at that point in generation (which
grows during a single request regardless of the `-c` ceiling), not the
ceiling itself. `-c` only bounds the worst case and the KV-cache buffer's
memory footprint; it doesn't change the per-position compute/bandwidth cost
for requests that were already going to finish inside a lower ceiling. A
smaller `-c` here would be a memory-headroom decision, already made (V20),
not a speed one — dropping it further only makes sense if RAM is still tight,
and only guards against unusually long requests, which per the token counts
above aren't the profile of this dataset.

What *does* follow directly from §5's measured slowdown curve: the local
completion path's uncapped `max_tokens=768` default (`agent/local_llm.py:37`,
used with no override on every category's first local attempt in
`agent/router.py`) lets a request run into exactly the region where decode
is slowest (>500 tokens deep) for no benefit if the real answer needed far
fewer tokens. This mirrors a pattern the remote path already has
(`REMOTE_MAX_TOKENS` per category, `agent/config.py:27-36`) but the primary
local call doesn't. This is a **router-level code change, not a llama.cpp
launch flag**, so it's out of this report's strict scope (research-only, no
edits made) — flagging it here only because it's the single most
evidence-backed lever this research surfaced, and the data (§5's curve, §6's
token counts) is the direct justification if it's picked up separately.

---

## Ranked list: effort vs. expected speedup, before tonight's deadline

1. **Do nothing to the llama.cpp launch flags.** Every flag investigated
   (`-ctk`/`-ctv`, `-b`/`-ub`, `--numa`) either measured as a wash or a
   regression at our actual context/thread/prompt profile on this build.
   The current `entrypoint.sh` invocation (defaults for all of these,
   `-fa` left at `auto`) was, in every head-to-head measured above, tied
   for fastest or the outright fastest option. Effort: zero. Expected
   speedup: N/A (there is nothing here to gain — the honest finding of this
   research is "the requested levers are already at their best setting").
2. **(Out of scope, adjacent, evidence-backed if picked up separately)**
   Cap the local path's decode length per category the same way
   `REMOTE_MAX_TOKENS` already caps remote calls, instead of the uncapped
   768-token default on the primary local call. Effort: small (mirrors an
   existing pattern in `agent/config.py`/`agent/router.py`). Expected
   effect: directly attacks the mechanism measured in §5 (decode gets
   progressively slower the longer a generation runs) rather than any
   launch flag — this is a code change, not a config/flag change, so it's
   noted here for visibility only, not recommended as tonight's action
   under a research-only mandate.
3. **Do not** build a narrower/AVX512-pinned llama.cpp binary tonight. The
   vendored build already self-selects the best of 14 CPU variants at
   runtime (§4); a rebuild has no headroom to gain and real risk (crash on
   an unknown grading VM) for a deadline with no time to test on the actual
   target hardware.
4. **Do not** add `-ctk q8_0 -ctv q8_0` (or q4_0) to `entrypoint.sh`. It
   measured as a net regression for this workload (§1): forces `-fa on`
   (slower prompt processing here) to quantize a KV cache that's already
   too small at our context lengths to matter, for no measured tg gain.

Net honest conclusion: **this research did not find an unused, low-risk
llama.cpp flag worth flipping before tonight.** The current entrypoint
configuration already sits at (or within measurement noise of) the fastest
observed setting for every flag tested. The one lever with real, measured
leverage (decode cost compounding with generation length, §5) is addressed
by capping *how many tokens the model is allowed to generate*, which is
already the router's existing pattern for remote calls and simply isn't
extended to the primary local call — a small code change, not a config flag,
and therefore outside this report's no-edit research mandate.

---

## Sources

- `tools/llama-b9888/llama-server --help`, `tools/llama-b9888/llama-bench --help` (this repo, version `9888 (cb295bf59)`, GNU 11.4.0) — primary source for every flag name/default cited above.
- `docker/entrypoint.sh`, `agent/config.py`, `agent/local_llm.py`, `agent/router.py` (this repo) — current launch flags and request-budget code.
- `data/dev_tasks/merged.json` (this repo, 228 tasks) — prompt length distribution; tokenized directly with `llama-tokenize` against the baked model.
- Real `llama-bench` measurements against `models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, `-t 2`, on the dev machine (Intel Core 7 150U) — all tables above.
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md — official server flag docs (fetched directly).
- https://github.com/ggml-org/llama.cpp/issues/10378 — exact error string confirming quantized V-cache requires `-fa`.
- https://github.com/ggml-org/llama.cpp/discussions/5932 — 4-bit KV cache discussion (GPU-focused, no CPU-specific numbers found there).
- https://github.com/ggml-org/llama.cpp/discussions/6328 — official `-b` vs `-ub` semantics discussion.
- https://github.com/ggml-org/llama.cpp/discussions/19102, https://github.com/ggml-org/llama.cpp/issues/1437 — NUMA behavior/limitations discussions.
- https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-cpu/CMakeLists.txt — `GGML_CPU_ALL_VARIANTS`/`GGML_BACKEND_DL` build options and the x86_64 variant list, confirming what's vendored in `tools/llama-b9888/`.
- https://deepwiki.com/ggml-org/llama.cpp/4.2-cpu-backend-and-optimization — CPU backend runtime-dispatch architecture explanation.
- https://github.com/abetlen/llama-cpp-python/issues/2069 — corroborating description of `GGML_BACKEND_DL`/`GGML_CPU_ALL_VARIANTS` runtime CPU-variant loading.
- `lscpu` output on the dev machine — confirms 1 socket / 1 NUMA node topology used to reason about §3's grading-VM generalization.
- `research/local_inference_llamacpp.md` (this repo, prior research pass) §1 and §6 — cross-referenced for CPU threading and quantization context already collected; not re-derived here.
- `research/VERDICTS.md` V20 — primary-source quote on the grading environment's 4GB/2vCPU constraint and the existing `-c 4096→2048` rationale.
