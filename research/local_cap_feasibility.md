# Local Decode-Cap Feasibility — factual_knowledge / named_entity_recognition on the 2-vCPU Grading Box

Research only, no code changed. Question: can a capped LOCAL Qwen3-4B-Instruct-2507
Q4_K_M generation for `factual_knowledge`/`named_entity_recognition` reliably finish
inside `REQUEST_TIMEOUT_S=25` (`agent/config.py:48`) on the 2-vCPU/4GB grading box,
instead of the current pattern (uncapped local call times out to empty, escalates to
paid remote) — and are the just-added caps (`LOCAL_GEN_CAP`: factual=80, NER=112,
`agent/config.py:89-92`) the right numbers.

**Method**: read the three named prior-research files first (not duplicated below).
Then two kinds of new evidence: (1) **primary/live** — started the actual vendored
`tools/llama-b9888/llama-server` (same binary/version `9888 (cb295bf59)` as
`docker/entrypoint.sh`) against the real baked model
(`models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf`) with the *same* flags as production
(`-c 2048 -t 2 --jinja`), and drove it directly over HTTP with streaming
chat-completions requests, instrumenting per-chunk arrival time — this measures the
real code path (chat template, JSON/SSE framing, detokenization) that `llama-bench`
does not exercise, at the cost of running on a **shared dev laptop with other
processes active**, so treat absolute numbers as noisier than `cpu_inference_speed.md`'s
controlled `llama-bench` runs, not cleaner. Also read `llama-server --help` directly
(the actual vendored binary) and the server's own startup log. (2) Web search/fetch:
llama.cpp GitHub issues/discussions, the server README, Qwen3 model card, and
independent token-budget-vs-accuracy measurements. UNVERIFIED = not from a primary
source (repo code/binary, or a directly-fetched official doc).

---

## 1. Realistic tok/s for a 4B Q4_K_M model on 2 x86 vCPUs (decode) — cross-checked, and the safe worst-case to budget against

`cpu_inference_speed.md` §5 (this repo's own controlled `llama-bench` runs, Intel
Core 7 150U, 2 threads, AVX2+FMA+AVX-VNNI, **no AVX-512**) already found decode is
**not flat with depth**: `tg64` at increasing already-filled context —
d=0: 5.39±1.53 t/s, d=256: 3.06, d=512: 2.70, d=1024: 2.18 t/s. That report's own
conclusion was that decode roughly halves from start to 1024 tokens deep.

New evidence gathered here, running the **real HTTP server** (not the bare
`llama-bench` loop) with the production launch flags, on the same machine:

| request | max_tokens | prefill (1st tok) | decode time | tokens | decode rate |
|---|---|---|---|---|---|
| factual, default system, natural ~108-tok answer | 112 | 5.24s | 28.35s | 108 | 3.81 t/s |
| factual cap=80, default system (truncated) | 80 | 3.50s | 32.63s | 80 | 2.45 t/s |
| factual cap=80, terse system (complete) | 80 | 8.44s | 18.90s | 53 | 2.80 t/s |
| NER cap=64, default system (truncated) | 64 | 0.82s | 25.09s | 64 | 2.55 t/s |
| NER cap=64, terse system (complete) | 64 | 14.70s | 19.02s | 44 | 2.31 t/s |
| NER cap=48, terse system (complete) | 48 | 0.48s | 18.03s | 44 | 2.44 t/s |

(Full transcripts not reproduced here; each request used the real
`/v1/chat/completions` endpoint via `httpx.stream`, `temperature=0.0`.)

Decode rate through the real server clusters **2.3-2.8 t/s** — meaningfully slower
than `cpu_inference_speed.md`'s bare-loop `tg64` at comparable depth (3.06-5.39 t/s).
Prefill is the noisiest number observed (0.48s to 14.70s for near-identical short
prompts) — almost certainly contention from other processes sharing this dev
machine during the test, not a property of the model/flags; **do not treat the
prefill spread as representative of a quiet grading VM**, but do treat it as a
warning that prefill is not a fixed quantity you can subtract cleanly from the 25s
budget.

**Cross-check verdict: our ~4 tok/s figure was optimistic for the code path that
actually matters.** ~4 tok/s (or the bare-loop's 5.3 t/s at d=0) describes
`llama-bench`'s internal generation loop; the real HTTP server, doing the same
work, measured 2.3-2.8 t/s in these runs. Both numbers are from the same box/binary/
thread count — the gap is real serving overhead (chat template render, per-token
SSE/JSON framing, detokenization), not a different machine.

**Does grading-VM microarchitecture (AVX2 vs AVX-512) plausibly swing this 2-3x?**
Web research (`research/local_inference_llamacpp.md` §"CPU threading behavior",
corroborated by a fresh search) is consistent on this point: *"the most important
factor for performance is memory bandwidth, and for CPU inference especially, the
bandwidth of consumer RAM is much lower compared to the bandwidth of GPU VRAM so the
actual CPU doesn't matter much"* — i.e. **decode (tg) is memory-bandwidth-bound, not
compute-bound**, so ISA width (AVX2 vs AVX-512) mainly accelerates the compute-bound
prompt-processing (pp) phase, not decode. `cpu_inference_speed.md` §4 already
confirmed the vendored binary self-selects the best of 14 CPU-tuned variants at
runtime regardless of the grading VM's actual silicon (`GGML_CPU_ALL_VARIANTS`), so
ISA mismatch risk is already handled. **The bigger unknown is absolute memory
bandwidth**, not ISA: a cheap/burstable 2-vCPU cloud tier (the AWS t3.medium /
Azure B2s / GCP e2-medium class this grading VM almost certainly resembles) can have
throttled or oversubscribed memory bandwidth for reasons unrelated to instruction
set — this is a real, UNVERIFIED-for-this-specific-VM risk, and it points the same
direction as the AVX argument: budget pessimistically, don't assume AVX-512 headroom
that may not exist, but also don't assume a 2-3x ISA-driven swing specifically.

**Safe worst-case to budget against: ~2.5 tok/s sustained decode.** This is not the
bare-loop's best-case 5.3 t/s, and not a hypothetical "could be 3x worse" guess — it
is the low end of what this repo's own two independent measurement methods
(`cpu_inference_speed.md`'s depth-degraded bare loop, and this report's real-HTTP-serving
runs) both actually produced on the *same known-good* hardware. An unknown,
possibly-weaker/oversubscribed grading VM is reasonably assumed to sit at or below
this, not above it.

## 2. What max_tokens cap reliably finishes within budget — the current caps are too high, confirmed empirically

Budget arithmetic: 25s total, reserve for prefill+HTTP/template overhead. Prefill
for our real prompt range (max 187 tokens, `cpu_inference_speed.md` §6) at the
bare-loop's measured pp rate (11.7-23 t/s) is normally a few seconds, but the noisy
0.48-14.70s spread measured here means a contended grading VM could plausibly eat
8-10s of the 25s just on prefill+overhead before a single output token streams.
That leaves a **decode budget of roughly 15-17s in a bad case**. At the ~2.5 t/s
safe-worst-case rate from §1, that supports **~37-42 output tokens**, not 80 or 112.

Directly measured confirmation that today's caps are too generous:

- **factual=80, default prompt**: the model's natural, un-truncated answer to a
  "list three inventions and their years" question ran to ~108 tokens; capped at 80
  it truncated mid-sentence ("...Power Loom – 1785 (invented by") and still took
  **36.12s total** — 44% over budget, and the shipped text is a broken sentence, not
  a usable partial answer.
- **NER=112, default prompt**: an 8-entity extraction naturally wants ~74-108 tokens
  of output (list + a trailing "Note:" aside); at cap=112 it ran **40.12s total** —
  60% over budget.
- Even a **tighter cap=64 with the current default (non-terse) prompt** still hit
  25.91s — right at the edge, truncated the trailing "Note:" filler mid-word.

**factual=80 and NER=112 are both too risky, confirmed on the same box that produced
the ~4 tok/s estimate they were sized against** — the estimate itself, not just the
depth-decay curve, needs revising per §1. NER=112 is the more dangerous of the two
(it was sized closer to a "let it finish including its filler" length rather than a
tight cap), but factual=80 is not safe either once the natural answer needs more than
one sentence (any "list N things" / "name three X" style factual prompt, which is a
real slice of the factual_knowledge category, not an edge case).

**Recommended caps, evidence-based**: factual **48-56**, NER **56-64** — both roughly
half the current values, sized to the §1 safe-worst-case decode budget rather than
the optimistic bare-loop number the current 80/112 were set against. Paired with the
prompt tweak in §5 below (which is necessary, not optional — see why in §4/§5), a
44-53 token *complete* answer was repeatedly achieved live in these tests, which a
48-64 cap accommodates without truncating.

## 3. Partial-on-timeout: no server flag does this; it is achievable client-side via streaming, with a real primary-source caveat

Checked `llama-server --help` directly (the vendored binary) for every
timeout/predict/cancel-shaped flag: `-n/--n-predict` (generation length cap, not a
timeout), `-to/--timeout` (default 3600s — an HTTP **socket** read/write idle
timeout, not a generation-length deadline; at the default it is far larger than our
25s budget and not the limiting factor here). **There is no launch flag that makes a
timed-out generation return partial output instead of nothing** — this was
force-checked against the real `--help` text, not inferred.

However, **partial-on-timeout is achievable, and was directly demonstrated live**,
via a client-side architecture change, not a server flag:

- Non-streaming behavior (what `agent/local_llm.py:47-79`'s `complete_scored()` does
  today via the `openai` SDK, `stream` not set): the server does not send any bytes
  back to the client until the *entire* JSON body is ready — i.e. until generation is
  completely finished. The OpenAI SDK's `timeout=` (currently
  `REQUEST_TIMEOUT_S=25`, `local_llm.py:31`) becomes an httpx `read` timeout, which
  measures time-since-last-byte; since **zero** bytes arrive during non-streaming
  generation, a generation that runs long enough eventually hits that gap and raises
  — caught by `local_llm.py`'s bare `except Exception: return None, None` — this is
  the exact, now-confirmed mechanism behind the "5/7 factual local generations
  returned len 0" this repo already measured (`config.py:77` comment).
- **Streaming** (`stream=True`) changes this structurally: tokens arrive
  incrementally as SSE chunks. Directly measured live: chunks arrived roughly every
  0.2-0.5s throughout a 25-40s generation — i.e. continuous data flow, which means
  the same read-timeout clock keeps resetting on each chunk and **will not fire from
  mere slowness** the way the non-streaming path does. A live test simulating a
  client that reads chunks and gives up at a fixed 20s wall-clock cutoff (independent
  of the httpx-level timeout) produced a genuine, non-empty partial answer where the
  non-streaming path would have produced nothing:
  `'Named Entities:\n\n- Barack Obama (Person)  \n- Germany (Location)  \n- France (Location)  \n- Japan ('`
  — partial, but real content, vs the current empty string.

**Important caveat this test also surfaced (confirmed against a real, closed GitHub
issue, not assumed)**: https://github.com/ggml-org/llama.cpp/issues/24496
(opened 2026-06-11, **closed as "not planned"**) — *"When a client disconnects,
`llama-server` continues generating tokens indefinitely... The `is_connection_closed()`
function is never called anywhere in the generation loop"* — and explicitly, this
*"affects both `stream=true` and `stream=false` modes."* So client-side abandonment
(closing the connection early after your own deadline) does **not** free server-side
compute — the orphaned generation keeps running until it hits its own `max_tokens`
cap or EOS, same as if the client had never disconnected. This is llama.cpp upstream
behavior on the exact server version this repo vendors, with no fix landing.

**Whether this matters for AMDA's serial task loop was checked directly, not
assumed**: started the real server with production's exact flags and read its own
startup log — `load_model: initializing, n_slots = 4, n_ctx_slot = 2048,
kv_unified = 'true'`. **`-np`/`--parallel` defaults to 4 concurrent slots on this
build**, not 1. An abandoned generation from a timed-out task occupies one slot,
bounded to its own `max_tokens` cap (never truly "indefinite" for AMDA specifically,
since every call already passes a `max_tokens`) — with 3 other slots free, the next
task's request is not blocked behind it. This meaningfully de-risks the "orphan
blocks the next task" failure mode, though it was not load-tested under real
concurrent AMDA traffic (UNVERIFIED whether `kv_unified` slot-sharing under real
memory pressure on a 4GB box behaves identically to this idle dev-box test).

**Implementation note for whoever picks this up**: setting `stream=True` alone is
not sufficient — the httpx-level timeout must be set generously (larger than the
worst case you're willing to wait, not `REQUEST_TIMEOUT_S`), and the *application*
must enforce the real deadline itself inside the chunk-read loop (check
`time.monotonic()` each iteration, `break` and use accumulated text once the budget
is spent) — httpx does not impose a "total elapsed" cap on its own, only
connect/read/write/pool timeouts, confirmed against the OpenAI Python SDK's own
default (`Timeout(connect=5, read=600, write=600, pool=600)`). Also: NER's
grammar-constrained JSON path (`grammars.JSON_GBNF`, used when `"json" in
prompt.lower()`, `router.py:216-218`) would need a fallback for a cut-off-mid-object
partial string, since a truncated JSON payload won't parse — this affects only the
subset of NER prompts that explicitly ask for JSON, not the category as a whole; not
solved here, flagged as a follow-up gap.

**This is a genuinely bigger lever than the cap number itself**: even a well-tuned
cap (§2) only reduces the *probability* of a timeout; streaming + client-side partial
capture changes what happens *when* one occurs anyway (contention, an unusually
verbose question, a slower-than-expected grading VM) from "guaranteed zero-credit
empty string" to "usually-complete, worst-case partial-but-real-content" — directly
answering the failure mode named in the task ("our current failure mode is
empty-on-timeout").

## 4. Accuracy tradeoff: truncation genuinely hurts open-ended answers, confirmed by both literature and this repo's own live tests

A token-budget study (Qwen2.5-3B-Instruct, 40 open-ended factual-QA questions,
exact-match scoring, chain-of-thought forced) found a **stark, non-linear
relationship**: 8 tokens -> ~0% accuracy (100% of outputs truncated), 32 -> ~10%,
64 -> ~20%, 128 -> ~40%, plateauing at ~70% by 256-512 tokens (~10% still clipped
even at 256). The author's framing is exactly our failure mode: *"the 70-point
accuracy swing... reflected model knowledge remaining constant — only the token
budget changed."* Caveat: different model (Qwen2.5-3B not our Qwen3-4B) and a
CoT-forcing setup that puts the answer at the *end* of the generation (worst case
for truncation) — the specific percentages don't transfer directly, but the
*shape* (truncation silently converts "knew the answer" into "scored wrong," and the
effect is large, not marginal) is the load-bearing finding, and it matches this
report's own live NER/factual tests directly: a truncated multi-item answer isn't
merely imperfect, it structurally cuts off content (missing "Washington D.C.,"
"March," "United Nations," "next year" at a 20s cutoff in the live NER test — half
the entity list gone).

Separately, general NER/extraction literature search corroborates the specific
failure shape for entity lists: *"for tables with many entities, the output of the
model exceeds the size limit... the completion of the prompt is stopped abruptly"*
and *"models frequently fail to capture all entities in the input text, particularly
in cases of... enumerated lists."* This is precisely what a hard token cap risks for
NER specifically — an incomplete entity list reads as a *wrong* answer under
exact/overlap-style grading, not a partially-correct one, since NER grading is
typically "did you list every entity."

**Multiple-choice / short-label tasks are structurally different and safer to cap
hard**: the same token-budget research area found truncation "doesn't matter at all"
for calibration on multiple-choice-shaped tasks — only open-ended generation loses
content under a tight cap. `sentiment_classification` (already capped at `max_tokens=8`
via grammar, `router.py:92`) is the safe end of this spectrum; factual/NER open-answer
prompts are the risky end, which is exactly why they need the prompt discipline in §5,
not just a smaller number.

## 5. Prompt technique for short-complete (not truncated-long) answers — directly measured to work

Web search on Qwen-family prompting practice surfaced generic advice ("set explicit
length constraints," "numbered/concrete rules over vague ones") but the concrete,
falsifiable version of this was tested live against the real model, not taken on
faith:

- **NER**, cap=64, current-style prompt (format hint only, no "stop after the list"
  instruction): natural output = "Named Entities:\n\n" + 8-item list +
  "\n\nNote: \"next year\" is a relative date, not a specific date." — the preamble
  and trailing aside are pure waste, and at cap=64 the trailing note gets truncated
  mid-sentence.
- **NER**, cap=64, `system="List only the entities with their type, one per line. No
  headings, no notes, no explanations."`: natural output = the 8-item list, nothing
  else, **44 tokens, complete, well inside the 64-token cap** — the model stopped on
  its own, it did not need truncating.
- Same instruction reproduced identically at cap=48 (44 tokens used, i.e. the cap
  wasn't even the constraint) — **total wall time 18.51s**, comfortably inside the
  25s budget.
- **factual**, cap=80, current-style prompt ("Answer concisely."): natural output ran
  to ~108 tokens across a "list three things" question, truncating at 80.
- **factual**, cap=80, `system="Answer in one short sentence or a brief list. No
  extra notes or caveats."`: natural output dropped to **53 tokens, complete**
  (three items with years, no extra framing).

**This is not a marginal effect — it's roughly a 30-45% reduction in tokens needed
for the *same* informational content**, and it is the difference between "truncated
mid-sentence" and "the model chose to stop." Concretely actionable against the real
code: `PROMPT_HINTS["named_entity_recognition"]` (`router.py:28`) already states
format rules but never tells the model to omit trailing commentary — appending
something like *"Output the list only — no headings, no notes, no explanations."*
is a one-line change directly justified by the measurement above.
`PROMPT_HINTS` currently has **no entry at all for `factual_knowledge`** locally
(only `REMOTE_HINTS`/`REMOTE_SUFFIX` apply on the remote path) — adding one
("Answer in one short sentence. If asked for a list, give only the list, no extra
explanation.") is the direct, evidence-backed fix suggested by the factual test
above. (Both are prompt-only changes; not applied here per the research-only scope
of this file — flagged for whoever implements it.)

---

## Recommended caps and GO/NO-GO

**Safe worst-case decode rate to design against: ~2.5 tok/s** (§1 — both this repo's
own bare-loop depth curve and fresh real-HTTP-serving measurements on the same known
hardware converge here; an unknown, possibly-weaker grading VM should not be assumed
faster).

**Recommended `LOCAL_GEN_CAP`**: `factual_knowledge: 56` (down from 80),
`named_entity_recognition: 64` (down from 112) — sized to the §2 decode-budget
arithmetic (~37-42 safe tokens plus headroom, since the §5 prompt tweak below makes
the model *want* to stop around 44-53 tokens rather than fill the cap). **Caps alone
are not enough** — ship them together with:

1. The terse "no notes/no preamble, list/answer only" prompt hint (§5) for both
   categories — this is what converts "80-112 tokens of rambling that gets chopped"
   into "44-53 tokens of a complete answer," and is necessary, not optional, for the
   lower caps in the previous paragraph to actually land inside budget rather than
   just truncating a shorter ramble.
2. Streaming + a client-side wall-clock cutoff that ships whatever partial text has
   arrived instead of raising on read-timeout (§3) — this is the backstop for the
   residual cases (contention, an unusually verbose question, a grading VM slower
   than this dev box) that caps and prompting reduce in probability but cannot fully
   eliminate. This is the single highest-leverage change available: it doesn't just
   shrink the failure rate, it changes the failure's *shape* from zero-credit empty
   string to a real partial answer. `llama.cpp` itself provides no server-side flag
   for this (§3, checked directly against `--help`); it must be built into
   `agent/local_llm.py`'s client.

**GO, conditionally.** Capped local generation for factual_knowledge/NER *can*
reliably fit inside 25s on 2 vCPU **if** the cap is lowered per §2 **and** paired
with the prompt tweak in §5 — both were directly demonstrated together to produce
complete, in-budget answers on the real server (NER: 18.51s total; factual-style:
27.34s total, which was still slightly over due to a noisy 8.44s prefill spike in
that one run — see the prefill-variance warning in §1). Caps and prompting alone
get you *probably* fine, not *guaranteed* fine, on an unknown grading VM — which is
exactly why item 2 above (streaming partial-capture) is the recommended companion,
not a nice-to-have: it is the only lever in this report that removes the
zero-credit-empty-string outcome altogether rather than just making it less likely.
If the 2-hour window only allows shipping one change tonight, ship the lower
caps + prompt tweak first (cheap, config/prompt-only, no client-code risk) and treat
streaming partial-capture as the next follow-up, not a blocker for tonight — but do
not consider the timeout risk fully closed without it.

**One adjacent finding worth flagging even though it's outside this report's literal
scope**: `research/VERDICTS.md` V25 (2026-07-10) moved factual_knowledge and
named_entity_recognition to `REMOTE_FIRST` specifically because dev-set accuracy on
the local+self-consistency route measured only ~57% strict for these two categories,
against ~100%/92% for the program-checked/solver-checked categories. This report
only answers whether a capped local generation *finishes in time* — it says nothing
about whether the resulting answer is *correct* often enough to be worth shipping
locally instead of paying for the accuracy V25 bought. That is a separate, real
tension (`config.py`'s own comment: "winning needs local dominance" for token rank,
vs V25's accuracy-driven remote-first) that whoever flips `LOCAL_ONLY` for these two
categories should weigh explicitly, not resolve by default.

---

## Sources

- `research/cpu_inference_speed.md` (this repo) — §5 depth-degradation curve
  (tg64 at d=0/256/512/1024), §6 prompt-length distribution, §4 CPU-variant
  auto-selection. Read in full per task instructions, not duplicated above except
  where directly cross-checked.
- `research/local_inference_llamacpp.md` (this repo) — §"CPU threading behavior"
  memory-bandwidth-bound claim; §6 tok/s throughput collection (no direct
  CPU-only Qwen3-4B number was found there either — confirmed still true in this
  pass's fresh search).
- `research/VERDICTS.md` V17 (logprob confidence, not directly load-bearing here),
  V20 (4GB/2vCPU grading environment, primary-source organizer guide quote), V25
  (factual/NER moved REMOTE_FIRST for accuracy — the adjacent tension noted above).
- `agent/config.py`, `agent/local_llm.py`, `agent/router.py` (this repo, read
  directly) — current `LOCAL_GEN_CAP`, `complete_scored()`'s non-streaming
  implementation and bare `except Exception` empty-return, `PROMPT_HINTS`/
  `REMOTE_HINTS` current content.
- `research/chaos_proxy_test.md` (this repo, untracked/in-progress) — cross-checked
  for the sibling `remote.py` `httpx.Timeout(REQUEST_TIMEOUT_S, connect=5.0)`
  pattern (remote path only; local path still uses a single scalar timeout).
- `tools/llama-b9888/llama-server --help` (this repo's actual vendored binary,
  version `9888 (cb295bf59)`) — checked directly for every timeout/predict/cancel
  flag; confirmed no partial-on-timeout flag exists.
- Live measurements against `tools/llama-b9888/llama-server -m
  models/Qwen3-4B-Instruct-2507-Q4_K_M.gguf -c 2048 -t 2 --port 8099 --jinja` (this
  session, same binary/model/flags as `docker/entrypoint.sh` modulo port) — startup
  log (`n_slots = 4`), streaming chunk-timing tests for factual/NER at multiple
  caps and system prompts (tables in §1-§5 above).
- https://github.com/ggml-org/llama.cpp/issues/24496 — client-disconnect does not
  cancel generation, closed as not planned; fetched directly, quoted verbatim above.
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md —
  fetched directly; `n_predict`, `stream`, `stop`, `-to/--timeout`, `/slots` erase
  action confirmed, no generation-timeout-returns-partial mechanism found.
- https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 — fetched directly; official
  recommended sampling (temperature 0.7, top_p 0.8, top_k 20, min_p 0) differs from
  AMDA's `temperature=0.0` greedy decoding (noted, not evaluated further — out of
  this report's scope).
- https://medium.com/@gsagar/my-model-knew-the-answer-but-wasnt-allowed-to-finish-717af0354501
  — fetched directly; Qwen2.5-3B-Instruct token-budget-vs-accuracy S-curve, quoted
  in §4 with the model/setup caveat stated inline.
- Search-synthesized, not individually deep-fetched (titles/claims cross-checked
  against ≥1 other source where flagged): OpenAI Python SDK default timeout
  `Timeout(connect=5, read=600, write=600, pool=600)` and read-timeout-resets-per-chunk
  streaming behavior (§3); general NER truncation/incomplete-entity-list literature
  (§4); AWS/Azure/GCP AVX2-vs-AVX-512 availability by VM tier (§1, informs but does
  not resolve the "which does the grading VM have" UNVERIFIED question).
