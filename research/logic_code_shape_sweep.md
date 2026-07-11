# Logic/code shape-coverage sweep

Continuation of a sweep whose batch data was lost (scratchpad wipe + prior
agent session limit). Deadline: 2026-07-11 16:00 UTC (21:30 IST). This file
is written incrementally — each stage appended as it completes.

Context: `logical_reasoning` uses a CSP-solver check
(`agent/router.py:_logic_solver_check` + `agent/verifiers.py:solve_logic_csp`)
that only fires on assignment/ordering puzzles (people+positions+alldiff
constraints). Everything else in the category returns `skip` from the solver
and ships on self-consistency (57% strict on dev — the weakest signal in the
router). Code tasks get a real executed-Python check
(`_run_python`/`_code_assertion_check`); non-Python code answers can't be
executed, so `verify()` returns `unknown` and those also fall through to
self-consistency. Image under test: `ghcr.io/anbu-00001/amda-agent:latest`
(local daemon, digest `1c3d756b2439`). Working files: `eval/tmp_logic_sweep/`.

---

## Stage 1 — Inventory (data/dev_tasks/merged.json, 228 tasks total)

Category counts: code_debugging 27, code_generation 23, factual_knowledge 28,
logical_reasoning 37, mathematical_reasoning 36, named_entity_recognition 26,
sentiment_classification 24, text_summarisation 27.

### logical_reasoning (37 tasks) by shape

| Shape | Clean (gradable) | Broken/placeholder gold or truncated prompt | Total |
|---|---|---|---|
| (a) solver-eligible assignment/ordering | 22 | 5 | 27 |
| (b) yes/no deductive (syllogism, "does it follow") | 1 | 0 | 1 |
| (c) truth-teller/liar (Knight/Knave/Normal) | 3 | 2 | 5 |
| (d) other (river-crossing, height-comparison, boxes-labeling, circular seating) | 3 | 1 | 4 |
| **Total** | **29** | **8** | **37** |

**(a) solver-eligible, clean (22):** all 5 chatgpt_logical_reasoning_*, all 8
gemini_logical_reasoning_* (incl. `_dup2` variants), all 8
synth_logical_reasoning_hard_13..20, plus `grok_logical_reasoning_hard_3`
(task scheduling with a fully-determined unique order, gold "S, P, Q, R, T").
These are exactly what `_logic_solver_check` already targets — not part of
this sweep's measurement (already covered by the solver, ~92% per the router
comments).

**(a) solver-shaped but broken (5, all grok):** `grok_logical_reasoning_hard_1`
(Einstein riddle with clues elided — prompt literally says "[Include full
Einstein riddle clues here but shortened for brevity]"), `hard_1_dup2` (gold
is the literal excluded placeholder "Specific arrangement satisfying all
constraints."), `hard_4` ("Deduce positions using full classic-like
constraints" — clues not actually given, gold "Specific unique assignment of
colors and nationalities."), `hard_6` (references "7 rules" never stated,
gold "The unique order satisfying all 7 constraints."),
`grok_logical_reasoning_med_2_dup2` (constraints under-specified, gold
itself says "Multiple valid orders like D C A B E etc." — not a unique
answer). None of these are gradable against their own gold; excluded from
accuracy measurement in Stage 2, same policy as the mission's example
exclusion.

**(b) yes/no deductive, clean (1):** `grok_logical_reasoning_easy_1_dup2`
("If all cats are animals and some animals are dogs, does it follow that
some cats are dogs?" gold: No).

**(c) truth-teller/liar, clean (3):** `gemini_logical_reasoning_easy_2`
(classic Knight/Knave, 2 people), `grok_logical_reasoning_hard_2` (3
statements, Knight/Knave/Random, gold "A is random, B is liar, C is
truth-teller"), `grok_logical_reasoning_hard_5` (3 people Knight/Knave/
Normal, gold "A Knave, B Normal, C Knight").

**(c) truth-teller/liar, broken (2):** `grok_logical_reasoning_med_2` (gold
admits the puzzle is underspecified: "Need specific statements... to fix:
Alice says..."), `grok_logical_reasoning_med_1_dup2` (gold is a vague
placeholder: "Detailed deduction leads to consistent assignment satisfying
constraints.").

**(d) other, clean (3):** `grok_logical_reasoning_med_1` (river-crossing
optimization, gold "17 minutes" + full sequence), `grok_logical_reasoning_easy_2`
(simple transitive height comparison, gold "A"), `grok_logical_reasoning_hard_1_dup3`
(circular seating, gold explicitly accepts rotations/reflections — gradable
with fuzzy/LLM-judge-style matching, not exact string match).

**(d) other, broken (1):** `grok_logical_reasoning_easy_1` (three-boxes
label puzzle; gold text itself is a confused, self-interrupting draft:
"...actually has only apples or only oranges? Wait, standard: ... classic
puzzle sol[ution cut off]" — not usable as ground truth).

**Net for Stage 2 measurement (non-solver, clean only): 1 (b) + 3 (c) + 3 (d)
= 7 tasks.** Small n — results here are directional, not statistical power.
Will note this caveat again in Stage 4.

### code_debugging / code_generation (50 tasks) by language

| Language | code_debugging | code_generation | Total |
|---|---|---|---|
| Python | 20 | 17 | 37 |
| JavaScript | 7 | 6 | 13 |
| Other/unspecified | 0 | 0 | 0 |

No non-JS/non-Python languages present (no C++/Java/Go/etc.). A handful of
`code_generation` prompts (5, all `grok`) don't literally say "Python" or
"JavaScript" but are unambiguous by syntax (`def foo(...)` vs
`function foo(...)`) — folded into the Python/JS counts above, not a
separate bucket.

**Why this matters:** `verify()` in `agent/verifiers.py` only executes
Python. A JS answer to a JS-language task can never be run
(`extract_python_code` fails to parse it), so `verify()` returns `unknown`
(non-python code detected via `` ```/function/const/let ``) rather than
`fail`, and the task falls through to self-consistency — same weak-signal
path as the non-solver logic shapes. **13/50 (26%) of code tasks are on
this path.**

JS task IDs: `chatgpt_code_debugging_easy_2`, `chatgpt_code_debugging_med_1`,
`gemini_code_debugging_med_2`, `gemini_code_debugging_med_2_dup2`,
`grok_code_debugging_easy_2`, `grok_code_debugging_med_2`,
`grok_code_debugging_med_2_dup2`, `chatgpt_code_generation_easy_2`,
`chatgpt_code_generation_med_2`, `gemini_code_generation_easy_2`,
`gemini_code_generation_med_2_dup2`, `grok_code_generation_easy_2`,
`grok_code_generation_med_1_dup2`.

**Next:** Stage 2 measures local-only accuracy on the 7 clean non-solver
logic tasks (shapes b/c/d) and, per Stage 3, spot-checks the 13 JS code
tasks.

---
## Stage 2 — Pipeline behavior on non-solver logic shapes (local-only docker)

Run: `ghcr.io/anbu-00001/amda-agent:latest`, `--network none` (no
FIREWORKS_API_KEY → every remote call fails → "Unable to answer." =
**escalation-needed** in production), `--memory=4g --memory-swap=4g
--cpus=2`, `TOTAL_BUDGET_S=540`. One batch of all 15 non-solver logic tasks
(7 clean + 8 broken). Finished in 520.2s; stderr route summary:
`local: 1, remote: 0`. Artifacts:
`eval/tmp_logic_sweep/{input/batch_logic_nonsolver.json,output/logic_nonsolver/results.json}`.

Caveat: 3 other AMDA containers (another agent's math sweep) ran
concurrently on the host for part of the run; per instruction, timing is
ignored, only answer content graded. Contention *can* inflate the
escalation count (the no-key fallback retry at 192 tokens can exceed the
25s request timeout on starved CPUs, turning a would-be weak local answer
into "Unable to answer."), so escalation counts below are an upper bound;
correctness of shipped answers is unaffected.

### Results per task (clean tasks, LLM-judge-style grading vs gold/criteria)

| Task | Shape | Outcome | Graded |
|---|---|---|---|
| grok_logical_reasoning_easy_1_dup2 | (b) yes/no deductive | shipped local: "No." | CORRECT (gold "No") |
| gemini_logical_reasoning_easy_2 | (c) truth-teller | escalated | — |
| grok_logical_reasoning_hard_2 | (c) truth-teller | escalated | — |
| grok_logical_reasoning_hard_5 | (c) truth-teller | escalated | — |
| grok_logical_reasoning_med_1 | (d) other (bridge crossing) | escalated | — |
| grok_logical_reasoning_easy_2 | (d) other (transitive height) | shipped local: "A is the tallest" | CORRECT (gold "A") |
| grok_logical_reasoning_hard_1_dup3 | (d) other (circular seating) | escalated | — |

All 8 broken/placeholder-gold tasks also escalated (8/8) — consistent with
self-consistency failing on underspecified puzzles, as it should.

### Stage 2 headline

- **The current pipeline already escalates most non-solver logic.** On the 7
  clean tasks: 2 shipped locally (both trivial-easy, both CORRECT), 5
  escalated (71% escalation rate). Every truth-teller/liar task escalated
  (3/3); the two shipped were the one-line syllogism and the one-line
  transitive comparison.
- **What ships locally on these shapes is accurate so far (2/2)** — but the
  sample is tiny and skewed easy. The open question for the "keep local"
  case is raw local accuracy on the tasks that currently escalate — measured
  next via a direct probe of the same model/weights/params outside the
  router (Stage 2b below).

## Stage 3 — Non-Python (JavaScript) code tasks, local-only docker

Same container settings; all 13 JS tasks in one batch. Finished in 435.8s;
stderr: `local: 9, remote: 0`. Artifacts:
`eval/tmp_logic_sweep/{input/batch_js_code.json,output/js_code/results.json}`.
Recall the mechanics: JS answers can't be executed by `verify()`
(`extract_python_code` can't parse them → "unknown"), so all 13 rode the
self-consistency probe; 9 passed it and shipped, 4 failed it and escalated.

### Shipped answers graded (9)

| Task | Graded | Note |
|---|---|---|
| chatgpt_code_debugging_easy_2 | CORRECT | `=` vs `===` found, corrected code matches gold |
| chatgpt_code_debugging_med_1 | CORRECT | `max = arr[0]` fix, matches gold exactly |
| grok_code_debugging_easy_2 | CORRECT | missing argument identified, fixed call shown |
| grok_code_debugging_med_2 | **WRONG** | gold: "code is correct, outputs 120, no bug" — model invented a negative-input bug |
| grok_code_debugging_med_2_dup2 | **WRONG** | gold: "code is correct, outputs true" — model invented a case-sensitivity bug |
| chatgpt_code_generation_easy_2 | CORRECT | celsiusToFahrenheit matches gold |
| chatgpt_code_generation_med_2 | CORRECT | factorial matches gold semantics |
| grok_code_generation_easy_2 | CORRECT | isEven matches gold |
| grok_code_generation_med_1_dup2 | CORRECT | maxOfArray with empty-array null, matches gold |

**Shipped-local JS accuracy: 7/9 (78%).** Both misses are the same failure
mode: "no bug present" trick debugging tasks where the 4B hallucinates a
plausible-sounding bug — and hallucinates it *consistently*, so the
self-consistency probe confirms rather than catches it. This is the exact
blind spot the V21 assertion check closes for Python and cannot for JS.

### Escalated (4) — all gemini, the longest/hardest prompts

`gemini_code_debugging_med_2` (var/let closure scoping),
`gemini_code_debugging_med_2_dup2` (chunk indexing off-by-one),
`gemini_code_generation_easy_2` (convertTemperature with rounding spec),
`gemini_code_generation_med_2_dup2` (email dedup rules). In a keyed run
these 4 go remote — appropriate: their acceptance criteria are the
strictest of the JS set.

## Stage 2b — Gold-answer audit: 3 of the 7 "clean" non-solver tasks have provably wrong golds

Before grading the raw-local probe, each truth-teller/liar and seating gold
was brute-forced (script inline in the sweep transcript; all-permutation
enumeration, no LLM involved):

- **grok_logical_reasoning_hard_2** — unique consistent assignment is
  **A truth-teller, B liar, C random**. Gold says "A random, B liar,
  C truth-teller", which is internally impossible: if C were the
  truth-teller, B (the liar) saying "C is the truth-teller" would be telling
  the truth. **Gold wrong.**
- **grok_logical_reasoning_hard_5** — unique consistent assignment is
  **A Knight, B Normal, C Knave**. Gold says "A Knave, B Normal, C Knight"
  (the mirror image): if A were a Knave, his claim "B is Normal" would have
  to be false, but the gold itself makes B Normal. **Gold wrong.**
- **grok_logical_reasoning_hard_1_dup3** — the constraint set (Alice not
  adjacent to Bob, Bob opposite Charlie, Dana adjacent to Alice, Charlie
  clockwise-adjacent to Dana, square table) is **unsatisfiable** under
  either reading of "left of"; the gold's own "Clockwise: Alice, Dana, Bob,
  Charlie" places Bob adjacent to Charlie, violating its own constraint 2.
  **Task broken.**

Revised truly-gradable non-solver inventory: **(b) 1 task, (c) 1 task,
(d) 2 tasks = 4 of 37.** Combined with Stage 1's 8 placeholder/underspecified
golds, **11 of the 15 non-solver logical_reasoning dev tasks are broken or
provably mis-golded** (all 10 grok tasks + 1 more grok dup). The non-solver
dev-set signal for this category is mostly noise, and any accuracy
percentage over it (including the 57% self-consistency strict figure, to the
extent it drew on these tasks) understates or misstates real capability.
Scoring consequence: on tasks like these, being *right* loses to the gold —
neither local nor remote routing can recover points from a wrong gold, which
caps the value of escalating this shape on dev-like data.

