# Local benchmark run — 2026-07-07/08, full 228-task dev set

Raw data + observations from the first full local+Cerebras-escalation run against
the entire dev set. Written for a Fable analysis pass, same pattern as the earlier
research/*.md -> VERDICTS.md pipeline. Minimal interpretation below; the numbers
and the two flagged bugs are the substance.

## Run setup

- Machine: user's laptop (Dell Inspiron 16 5640, Intel Core 7 150U, 12 threads,
  16GB RAM), Ubuntu 24.04.
- Local model: Qwen3-4B-Instruct-2507 Q4_K_M via llama-server, capped at 6/12
  threads (deliberate headroom, not a hardware limit).
- Remote stand-in: Cerebras free tier, model id `gemma-4-31b` (closest free-tier
  match to the real submission target `gemma-4-31b-it` — see research/VERDICTS.md
  V8). Real API key, real network round-trips, not simulated.
- `TOTAL_BUDGET_S` overridden to 6300s for this run (the shipped default, 540s,
  is sized for the 10-minute judging VM window and would have forced remote-only
  routing on every task past the 9-minute mark of a 90-minute local run — a
  measurement artifact, not agent behavior, so it was raised for this run only).
- Command: `TOTAL_BUDGET_S=6300 timeout 6600 eval/run_local.py` (no N = full set).

## Headline numbers

- **228/228 tasks completed, 0 errors, exit 0.**
- Wall clock: 4968.5s = **82.8 minutes** (21.8s/task average).
- Thermal: CPU package temp 53°C idle -> 66°C peak sustained -> 59°C within a
  minute of stopping the server. Load average settled around 5-7 of 12 threads
  throughout. No throttling, no instability.
- Routing distribution:
  | route | count |
  |---|---|
  | local | 48 |
  | local+consistent | 68 |
  | local+program | 5 |
  | remote:gemma-4-31b | 105 |
  | fallback | 2 |

  46% of tasks never left the machine (local + local+consistent + local+program =
  121/228); 46% escalated to the Cerebras stand-in; 2 tasks hit the last-resort
  fallback path (remote returned nothing usable, e.g. rate-limit or empty
  response, and the local retry answer shipped instead).
- Scored tokens (remote calls only, local is free): **10,854 input + 4,277
  output across 105 calls** — ~137 tokens/call combined. Cerebras' 5 RPM free-tier
  cap (research/free_apis_opensource_tools.md A6) was never visibly hit; the
  sequential single-process pace naturally stayed under it.

## Judge results (eval/judge.py, deterministic local judge — NOT the real
## AMD LLM-judge; treat as a lower-bound / sanity signal only)

- **Strict: 89/228 = 39%** (fail 79, unsure 60)
- **Ceiling (pass+unsure): 65%**

| category | pass | fail | unsure | strict |
|---|---|---|---|---|
| code_debugging | 0 | 8 | 19 | 0% |
| code_generation | 0 | 6 | 17 | 0% |
| factual_knowledge | 17 | 1 | 10 | 61% |
| logical_reasoning | 9 | 23 | 5 | 24% |
| mathematical_reasoning | 16 | 20 | 0 | 44% |
| named_entity_recognition | 14 | 9 | 3 | 54% |
| sentiment_classification | 16 | 8 | 0 | 67% |
| text_summarisation | 17 | 4 | 6 | 63% |

| route | pass | fail | unsure |
|---|---|---|---|
| fallback | 0 | 2 | 0 |
| local | 14 | 5 | 29 |
| local+consistent | 40 | 20 | 8 |
| local+program | 5 | 0 | 0 |
| remote:gemma-4-31b | 30 | 52 | 23 |

Notable: `local+program` (the math program-aided check) is 5/5 pass — small
sample, but 100% agreement between the program-check and the deterministic
judge on the cases it fired for.

`remote:gemma-4-31b` has more raw fails (52) than passes (30) by count, but
this is the category that escalated *because* local verification failed —
i.e. these are disproportionately the hardest tasks in the set, not a signal
that the remote model itself is weak. Needs category-conditioning to interpret
properly (a hard math/logic task escalated and still marked "fail" by our
judge isn't necessarily wrong — see the code-judge bug below for how much the
local judge's own limitations can distort this table).

## Bug #1 (fixed this session): classify.py "ner" substring false-positive

`agent/classify.py` had a bare `"ner"` keyword for `named_entity_recognition`
that matched inside ordinary words ("ru**ner**", "cor**ner**", "ban**ner**").
Zero legitimate word-boundary hits in the whole 228-task set, 8 false
positives. Removed. Classifier accuracy on the full set: 87% (199/228) with
the fix in place for this run (was 84.6% pre-fix on the same data).

## Bug #2 (fixed this session): parse_batches.py task_id collisions

`eval/parse_batches.py` namespaces task_id as `f"{source}_{task_id}"`, but
each source has multiple batch files that each restart their own numbering
(`easy_1`, `med_1`, ...). 45/228 tasks had colliding IDs before the fix —
different prompts sharing one ID, silently corrupting `judge.py`'s
`{task_id: prompt}` dict lookup (last-write-wins). Fixed by disambiguating
collisions at merge time (`_dup2`, `_dup3` suffixes); `merged.json`
regenerated, 0 duplicates, same 228 tasks.

## Bug #3 (FIXED 2026-07-08 — see research/VERDICTS.md V11 for the fix,
## measured effect: code fails 14→2, ceiling 65%→71%)

`_extract_code()` exists in two places — `eval/judge.py` (dev judge, line
~102) and `agent/verifiers.py` (**live runtime verifier**, nearly identical
code). Both have the same flaw in the no-fenced-code-block fallback: if any
line in the text matches `^\s*(def |class |import |...)` (MULTILINE search,
i.e. anywhere in the text, not just the start), the function returns the
**entire input text, prose included**, as "code" to `compile()`. Any prose
sentence before the code (a nearly universal LLM habit: "Bug: ... Corrected
code:\n\ndef foo():...") guarantees a `SyntaxError`.

Measured impact:
- **33 of 50 code-category gold answers (66%) are unfenced** prose+code, i.e.
  hit this path.
- This is *why* code_debugging and code_generation show 0% strict pass above
  — the judge's own gold-answer extraction fails to compile in most cases, so
  the stdout-comparison "pass" path can essentially never fire. The 0% is a
  **judge-methodology artifact**, not a measured agent failure — the real
  code quality is unknown from this run, buried under "unsure."
- The same bug in `agent/verifiers.py` is a live, scored-token cost: if our
  local model (or a remote model) answers a code task with any lead-in prose
  before an unfenced fix, `verify()` force-fails a possibly-correct local
  answer and escalates to remote unnecessarily.
- Confirmed by direct inspection, not inferred: e.g.
  `chatgpt_code_debugging_easy_1`'s gold answer is
  `"Bug: The loop for i in range(n) only sums up to n-1. ... Corrected code:\n\ndef sum_to_n(n):\n..."`
  — `_extract_code` returns this whole string, `compile()` raises on the
  `"Bug: ..."` line, gold "runs" with rc=1 and empty stdout.
- Some gold answers in this same unfenced style are JavaScript, not Python
  (`chatgpt_code_debugging_med_1`: `function findMax(arr) {...}`) — those
  correctly return `None` from `_extract_code` (no def/class/import match)
  and fall through to "unsure," which is arguably correct behavior already
  for a Python-only local judge.

## Bug #4 (FIXED 2026-07-08 — see research/VERDICTS.md V12,
## measured: 87.3%→96.5%, math misroutes eliminated)

29 total classifier misses on this run (87% accuracy). Breakdown by
true-category -> guessed-category:

| true category | guessed | count |
|---|---|---|
| logical_reasoning | factual_knowledge | 12 |
| mathematical_reasoning | factual_knowledge | 6 |
| factual_knowledge | text_summarisation | 3 |
| named_entity_recognition | factual_knowledge | 2 |
| code_generation | factual_knowledge | 2 |
| logical_reasoning | named_entity_recognition | 1 |
| sentiment_classification | code_debugging | 1 |
| code_debugging | code_generation | 1 |
| text_summarisation | sentiment_classification | 1 |

23 of 29 misses (79%) land on `factual_knowledge` — this is `classify.py`'s
explicit default (`return best if scores[best] > 0 else "factual_knowledge"`)
firing because the prompt matched zero keywords in any category's list. The
dominant failure mode isn't confusion between two categories, it's the
keyword list being too sparse for logic-puzzle and math-word-problem phrasing
that doesn't happen to contain "puzzle," "constraint," "calculate," etc.
Misclassification degrades the router only indirectly — wrong PROMPT_HINTS
template and wrong verifier get applied — but it's a real, sizeable, and now
quantified gap.

## Raw artifacts

- `eval/results_dev.json` — all 228 answers, routes, categories (regenerate-
  able, gitignored).
- This file — everything needed to pick up analysis without re-running
  anything.
