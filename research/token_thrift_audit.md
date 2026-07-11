# Token thrift audit — remote prompt overhead, 2026-07-11

Scope: `agent/router.py`, `agent/remote.py`, `agent/config.py`. Goal: find
token savings with **zero accuracy risk** ahead of the 19:45 IST deadline.
No code changed by this audit (per instructions) — findings only.

Tokenizer note: no `tiktoken` in `.venv` (checked, not installed). All
counts below use the requested `words * 1.3` heuristic, computed with a real
Python word split on the literal strings in `agent/router.py`, not
hand-counted. This is an approximation of the actual Gemma/proxy tokenizer,
but consistent across every row so the *relative* comparisons hold even if
the absolute numbers are off by some constant factor.

## 1. Overhead inventory — every non-task-content token we add to a remote call

| Piece | Literal | Words | Est. tokens | Sent when | Sent to |
|---|---|--:|--:|---|---|
| `SYSTEM` | "You are a precise assistant. Answer correctly and concisely. No preamble." | 11 | 14.3 | **every** remote call (`solve()` always passes `system=SYSTEM` to `remote.complete`, router.py:278) | all 8 categories |
| `REMOTE_SUFFIX` | "\n\nAnswer directly and concisely. Do not show reasoning." | 8 | 10.4 | **every** remote call (router.py:267, unconditional) | all 8 categories |
| `REMOTE_HINTS["named_entity_recognition"]` | "List every entity, including dates and times. Keep titles and honorifics as part of PERSON names. Cities, countries, and regions are LOCATION, never ORGANIZATION." | 24 | 31.2 | NER remote calls only | NER only |
| `REMOTE_HINTS["mathematical_reasoning"]` | "End with ANSWER: <value>." | 4 | 5.2 | math remote calls only (rare — math is not `REMOTE_FIRST`, only escalates on local fail) | math only |
| `REMOTE_HINTS` — all other categories | *(no entry)* | 0 | 0 | — | factual, summarisation, sentiment, logic, code_debugging, code_generation |
| Local `PROMPT_HINTS` (per-category nudges, e.g. "Work step by step...") | — | — | — | **never sent remote** — confirmed by code: `remote_prompt` (router.py:267) is built from raw `prompt`, not `full_prompt` (which has `PROMPT_HINTS` appended, used only for local calls, line 206/217). Already optimal. | — |
| `LOGIC_TRANSLATE_SUFFIX` | — | — | — | **local only** (`_logic_solver_check` → `local_llm.complete`, free) | — |

**Per-call fixed overhead by category** (SYSTEM + SUFFIX + any hint):

| Category | Overhead tokens/call | Mean raw prompt tokens (dev set, n shown) | Overhead as % of prompt |
|---|--:|--:|--:|
| factual_knowledge | 24.7 | 14.8 (n=28) | **167%** — overhead bigger than the task text |
| named_entity_recognition | 55.9 | 53.2 (n=26) | **105%** — overhead ≈ doubles input |
| text_summarisation | 24.7 | 92.3 (n=27, prompt text only) | 27% |
| mathematical_reasoning (escalation only) | 29.9 | 37.0 (n=36) | 81% |
| logical_reasoning, sentiment, code_* (escalation only) | 24.7 | 32–61 | 40–75% |

Overhead is a *large relative* share for factual/NER precisely because
those prompts are short — but the *absolute* number is small (25–56
tokens) in every case.

## 2. Load-bearing vs speculative

| Item | Classification | Evidence |
|---|---|---|
| `REMOTE_SUFFIX` | **LOAD-BEARING** | `research/VERDICTS.md` V3: cites measured Gemma-4 verbosity-by-default ("it has no instruction by default, so it falls back to its training prior, which is verbose") — this line is the fix. Also directly implicated in V25's NER investigation (its "concisely" wording caused a real observed entity-omission bug, which is why the NER hint below exists) — proof it has a real, measurable effect on generation shape, not a no-op. |
| `REMOTE_HINTS["named_entity_recognition"]` (dates/times + LOCATION clause) | **LOAD-BEARING** | `research/VERDICTS.md` V25: live smoke test caught the remote answer dropping a DATE entity under `REMOTE_SUFFIX`'s "concisely" pull; hint added, re-tested, "returned all 4 entities at 83in/19out tokens." |
| `REMOTE_HINTS["named_entity_recognition"]` (honorifics clause, added commit `f4d5353`) | **LOAD-BEARING** | `research/remote_path_validation.md`: live 26/26-task remote NER run found honorific-prefix drops ("Lena Fischer" for gold "Dr. Lena Fischer") as **the one recurring remote NER error**, 3 of 26 tasks affected (2 fails + 1 unsure would flip). Fix implemented same day, matches the report's explicit recommendation. |
| `REMOTE_HINTS["mathematical_reasoning"]` ("End with ANSWER: <value>.") | **LOAD-BEARING** | `research/math_adversarial_sweep.md` Stage 1b: found a *real* dev-task failure (`grok_mathematical_reasoning_hard_3`) where a remote-shaped answer without an `ANSWER:` line fed a bare fraction ("13/15") into `extract_final_number`'s fallback branch, which collapses to the **denominator** (15.0) — corrupting both the internal program-audit and, per the same doc, the leaderboard-judge's own regex fallback path. This hint routes remote math answers through the already-hardened `ANSWER:`-prefixed branch (commit `2102e09`). Direct code comment confirms intent (router.py:56-57). |
| `SYSTEM` message on remote calls | **SPECULATIVE (small)** | No evidence isolates its contribution *separately* from `REMOTE_SUFFIX` — every live-graded run in `eval/tmp_remote_val/` used the current SYSTEM+SUFFIX combination together, so we cannot attribute credit between them from that data. V3 recommends "single short line, or none" for the remote system prompt — the current 11-word line satisfies "single short line" as-is, so this isn't a violation, just untested in isolation. |
| `REMOTE_MAX_TOKENS` caps | **N/A — not a token-overhead item** | See §3: caps are non-binding in every category we have data for; lowering them saves nothing because generation never reaches the cap. |

**Speculative-item savings estimate** (`SYSTEM` message only, the sole
candidate): 14.3 tokens × expected remote-call count on 19 tasks.
- Low scenario (7 calls, `REMOTE_FIRST` categories only, no escalations): **~100 tokens**
- High scenario (15 calls, smoke-scaled): **~215 tokens**

That is the entire theoretical upside in this codebase — everything else
with a nonzero token cost has recorded evidence tying it to a measured
accuracy or completeness fix.

## 3. Output caps vs actual generations — confirmed non-binding

Measured directly from `eval/tmp_remote_val/{fk,ner,ts}_output/results.json`
(real Fireworks-proxy generations, not a cap or an estimate):

| Category | Cap (`REMOTE_MAX_TOKENS`) | n | Observed min / mean / max (tok≈words×1.3) | Max as % of cap |
|---|--:|--:|---|--:|
| factual_knowledge | 256 | 28 | 1.3 / 59.7 / 162.5 | 63% |
| named_entity_recognition | 256 | 26 | 3.9 / 19.6 / 42.9 | 17% |
| text_summarisation | 256 | 10 | 22.1 / 58.2 / 113.1 | 44% |

**No output in any measured category came close to its cap.** Billing is by
actual generated tokens, not the cap value — a cap that's never hit costs
nothing to leave alone, and there is no real-generation data on disk for
sentiment/logic/math/code (they aren't `REMOTE_FIRST`, so no dedicated
remote sweep exists for them; they escalate only occasionally). **Do not
touch any `REMOTE_MAX_TOKENS` value** — there is nothing to gain (the
measured categories are 37-83% of headroom under cap already) and no data
to safely justify moving the unmeasured ones either up or down this close
to the deadline.

## 4. Summarisation prompt — no redundant instruction text

`REMOTE_HINTS.get("text_summarisation", "")` returns `""` (no entry in the
dict). The remote summarisation prompt is exactly:

```
<full passage> + "" + "\n\nAnswer directly and concisely. Do not show reasoning."
```

Confirmed by direct code inspection (router.py:44, 54-59, 267) — one
instruction line only, no duplicated or extra hint text. The unavoidable
cost here is the passage itself (mean ~92 tokens on dev, `text_summarisation`
row in §1's prompt-length table), which cannot be reduced without touching
task content.

## 5. Hidden token leaks in `remote.complete`

- **Router-level retry**: `pick_models()` returns at most 2 models
  (`allowed[:2]`, config.py `REMOTE_PREFERENCE`/`CODE_PREFERENCE`). For
  `REMOTE_FIRST` categories only, router.py:270-275 appends one more try of
  the primary model (`models = models + models[:1]`) — so **up to 3 router-level
  attempts** for factual/NER/summarisation, **up to 2** for everything else.
  This part matches the task brief's own framing.
- **SDK-level retry, not previously counted**: `remote.py:34` constructs the
  `OpenAI` client with `max_retries=1`. Verified in
  `.venv/lib/python3.12/site-packages/openai/_base_client.py` (installed
  `openai==2.44.0`): on `httpx.TimeoutException` (exactly what fires when a
  call exceeds `REQUEST_TIMEOUT_S=25`) or a 5xx/429/408/409 status, the SDK
  **resends the identical request one more time internally**, invisible to
  `agent/router.py` and to the local `usage` counter (which only increments
  on a `resp.usage` that comes back from a call our code sees as
  successful). This means **each router-level "attempt" can itself be 2
  real HTTP requests** to the proxy.
- **Combined worst case for ONE task** (not 3 calls as roughly guessed in
  the brief — actually **up to 6**):
  `REMOTE_FIRST` category, everything transient-failing: 3 router attempts
  × 2 SDK-level sends = 6 real requests, each carrying the full
  `remote_prompt`. For a NER task at mean prompt 53.2 + overhead 55.9 =
  109.1 input tokens/request: **6 × 109.1 ≈ 655 input tokens for a single
  degraded task**, vs. ~109 tokens in the normal one-shot case — a 6×
  blowup. Non-`REMOTE_FIRST` worst case: 2 × 2 = 4 requests.
  This is a genuine tail risk, but it is exactly the failure mode commit
  `f4d5353`'s retry-fallback and `research/remote_path_validation.md`'s
  live run (2 NER "Unable to answer." results under rate-limit pressure)
  were guarding against — **whether this billing actually happens depends
  on whether Fireworks bills a request that times out client-side before
  the response returns**, which is unverified and not verifiable before
  the deadline. Flagging only; not a recommended change (see below — cutting
  `max_retries` trades away exactly the resilience the retry-fallback logic
  was added for).
- **Temperature/top_p**: `remote.complete` always sends `temperature=0`
  (remote.py:53), no `top_p` override (provider default). This is already
  the lowest-variance setting available and isn't a token-cost lever — flat
  `temperature=0` minimizes (does not eliminate, MoE routing can still
  vary) answer-shape variance that would otherwise trigger more
  verify()-driven fallback-model calls. No leak here.

## 6. Worst-case token projection, 19 tasks

Using the category-proportional call estimate from dev-set distribution
(§1) and the two "expected" scenarios already used in §2:

| Scenario | Remote calls | Overhead-only tokens | Notes |
|---|--:|--:|---|
| Low (REMOTE_FIRST only, no escalations) | ~7 | ~235 | 2-3 factual + 2 NER + 2 summarisation |
| High (smoke-scaled, matches brief's "6 calls/8 tasks") | ~15 | ~469 | adds ~6 escalations from math/logic/sentiment/code |
| Retry-storm tail (one degraded `REMOTE_FIRST` task) | up to 6 requests for that task alone | up to ~655 input tokens for that one task | SDK max_retries=1 stacked on router retry; not the expected case |

Overhead (SYSTEM + SUFFIX + hints) is ~13-20% of the brief's own 1.2-1.8k
total-token projection in the expected case — real but secondary to the
prompt/passage text and output tokens, which dominate the budget.

## 7. Recommendation: ship as-is

No change in this codebase clears the bar of **provably zero-accuracy-risk
AND verifiable in under 20 minutes**:

- `REMOTE_SUFFIX` and both `REMOTE_HINTS` entries are directly evidenced as
  fixing measured failures (V25, `remote_path_validation.md`,
  `math_adversarial_sweep.md`) — removing or shrinking any of them risks
  reintroducing a documented, already-fixed failure mode for a few tokens
  of savings.
- The only speculative piece (`SYSTEM` message, ~14.3 tok/call, ~100-215
  tokens total on 19 tasks) cannot be safely verified: every real
  remote-graded measurement on disk used SYSTEM+SUFFIX together, so there
  is no isolated evidence for what removing SYSTEM alone does — and the
  only way to get that evidence is a fresh live-graded run against the
  real submission path, which isn't possible before 19:45 IST.
  `research/models_fireworks.md` also records Gemma-4 behaving
  counter-intuitively to verbosity instructions in at least one documented
  case (telling it "taciturn" made it *more* verbose) — reason for extra
  caution around touching prompt wording this close to the gate, for a
  <1% change to the total token budget.
- `REMOTE_MAX_TOKENS` caps are confirmed non-binding on every category with
  real generation data (§3) — nothing to gain, so leave them.
- The SDK-level `max_retries=1` (§5) is a real but *uncertain-magnitude*
  tail risk, and the obvious "fix" (drop to 0) trades away resilience that
  was deliberately added the same day for a documented transient-failure
  mode. Not a safe touch under deadline pressure.
- `text_summarisation`'s remote prompt already carries no redundant
  instruction text (§4) — nothing to cut there either.

**Ship as-is.** Every remaining token in the remote path either has
recorded evidence it fixes a real measured failure, or is too small
(~1% of budget) and too unverifiable in the remaining time to touch safely
on a submission that is not yet confirmed past the accuracy gate.
