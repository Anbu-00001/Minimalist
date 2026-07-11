# Math verification adversarial sweep

Continuation of an earlier stress test (prior batch data lost — scratchpad wipe +
session limit). Rebuilt from scratch 2026-07-11.

Deadline: today 16:00 UTC (21:30 IST). Target: finished partial report by ~14:00 IST.

Scope:
1. Unit-level adversarial suite against `agent/verifiers.py`'s math-verification
   primitives (`extract_final_number`, `extract_expression`, `run_expression`,
   `numbers_agree`), called directly, no docker.
2. Container-level: every `mathematical_reasoning` task in `data/dev_tasks/merged.json`
   run through `ghcr.io/anbu-00001/amda-agent:latest` LOCAL-ONLY (no `FIREWORKS_API_KEY`),
   graded against current golds.
3. Patch ranking (report only — **no agent code edited** per instructions).

Image under test: `ghcr.io/anbu-00001/amda-agent:latest` (digest starting `1c3d756b`,
local docker daemon). Verifier code under test: `agent/verifiers.py` as of commit
`2102e09` (percent/fraction equivalence hardening, already in the image).

Artifacts (batch inputs/outputs, container logs) live under
`eval/tmp_math_sweep/` — not `/tmp` (session-scoped, gets wiped).

---

## Stage 0 — environment check

- `.venv/bin/python3` (3.12.3) has `python-constraint2==2.6.0` installed, importable
  as `constraint`. `agent.verifiers` and `agent.router` import cleanly with
  `sys.path` pointed at repo root — no stubbing/workaround needed after all (the
  earlier concern about `constraint` not being on host doesn't apply inside the
  project's own venv).
- `data/dev_tasks/merged.json`: 228 tasks total, **36 `mathematical_reasoning`** tasks.
  Container batches: batch1 = first 20, batch2 = remaining 16 (both ≤20/run limit).
- Grounding check: dumped all 36 real math prompts+golds
  (`eval/tmp_math_sweep/math_tasks_dump.txt`) to calibrate "realistic shape" judgments
  below against what this task family actually produces, not hypotheticals. Observed
  real gold shapes: plain integers/decimals, `$X.XX` (USD only), `X%`, `X hours`/`X
  minutes` (never combined), a bare ratio `10:9` (1 task), a bare fraction `13/15` (1
  task), `X square meters`. No £/€/₹, no scientific notation, no mixed fractions, no
  ranges, no Indian separators, no multi-quantity answers, no clock times anywhere in
  the current 36 — but a "refreshed" prompt set from the same generators (ChatGPT/Grok/
  synth word-problem templates) plausibly reuses the same *style*, so risk judgments
  below weight the ratio/fraction/time-phrase shapes higher (they already occur) and
  currency-symbol/scientific-notation/Indian-separator shapes lower (never occur, and
  wouldn't fit this word-problem style).

---

## Stage 1 — unit-level adversarial sweep (`agent/verifiers.py`)

Method: called `extract_final_number`, `extract_expression`, `run_expression`,
`numbers_agree` directly (no docker, no live LLM — the translator call in
`_math_program_check` is mocked by hand-supplying the expression a *correct*
translation would plausibly emit, to see whether the extraction bug alone would
cause the end-to-end check to falsely disagree). Scripts:
`eval/tmp_math_sweep/unit_sweep.py`, `eval/tmp_math_sweep/unit_sweep2_expr.py`.

**Headline result: every bug found is fail-safe, not fail-open.** `extract_final_number`
mis-tokenizes several ANSWER shapes, but in every case the mis-extraction makes a
*correct* stated value look like it disagrees with the independently-computed program
value — never the reverse. Simulated end-to-end runs (feeding `_math_program_check` a
hand-verified-correct expression) confirm this: mixed fractions, unit-suffixed
fractions, hour+minute phrases, scientific notation, and multi-quantity answers all
come back `False -- DISAGREE` even when the model's stated answer was actually right.
Effect is **token cost** (unnecessary escalation to remote) and **potential false
negatives on the leaderboard's accuracy metric IF the escalated remote answer is ALSO
scored strictly against the same gold string** — never a wrong answer getting blessed.
This reframes the SAFE/RISKY axis for math: nearly every fix here is unambiguously SAFE
because it can only *reduce* spurious disagreement, not manufacture agreement with a
wrong value from nothing.

### extract_final_number — per-shape results

| Shape | Example | Extracted | Correct? | Real-risk | Verdict |
|---|---|---:|---|---|---|
| £/€/₹ currency | `£45`, `€12.50`, `₹1,200` | 45.0, 12.5, 1200.0 | **Correct** — `$` is optional in `_NUM_RE`, other symbols are simply outside the match and ignored | Low (never seen in corpus; USD-only prompts) | No patch needed |
| Negative | `-5`, `-3.5` | -5.0, -3.5 | Correct | Low-medium (subtraction results, temperature-style problems are plausible) | No patch needed |
| "approximately X" / `~X` / `≈X` | `approximately 3.14` | 3.14 | Correct (regex ignores prose/symbol prefix) | Medium | No patch needed |
| **Mixed fraction** | `1 1/2` | **2.0** | **Wrong** (should be 1.5) — the bare-fraction `fullmatch` only fires when the *entire* ANSWER remainder is `N/D`; `"1 1/2"` fails that fullmatch, falls through to `nums()`, which independently matches `1`, `1`, `2` and keeps the last (`2`) | Medium — cooking/rate word problems ("1 1/2 hours") are a natural template for this generator family even though absent from the current 36 | **SAFE patch available** |
| **Fraction + unit** | `3/4 cup` | **4.0** | **Wrong** (should be 0.75) — same fullmatch-fails-on-trailing-text cause; degenerates to "last number in the string," which for `N/D suffix` is always the denominator | **High** — the corpus already has a bare-fraction gold (`13/15`, no unit); a unit-suffixed variant is one prompt-phrasing tweak away, and the existing Jul-11 hardening (commit 2102e09) was written for exactly this family but didn't generalize past the exact-fullmatch case | **SAFE patch available** — highest-value fix in this suite |
| Fraction, no unit (baseline) | `3/4`, `13/15` | 0.75, 0.867 | Correct (this is the commit-2102e09 fix, confirmed still working) | — | Already fixed |
| Range ("between") | `between 40 and 50` | 50.0 | Ambiguous-by-design (verifier can't know intended value) but PROMPT_HINTS explicitly asks for one committed value, so a range answer is a prompt-compliance failure upstream, not a verifier bug | Low (hint discourages this shape) | No patch — not a verifier problem |
| Range (dash) | `40-50` | **-50.0** | Wrong for range-intent, but also **structurally ambiguous with subtraction** (`_NUM_RE`'s optional leading `-` eats the dash) | Low-medium | RISKY to "fix" — any dash-as-range heuristic will misread genuine negative numbers or subtraction expressions typed as the final answer; not attempted |
| Range ("to") | `40 to 50` | 50.0 | Same as "between" case | Low | No patch — prompt-compliance issue |
| **Multi-number answer** | `12 apples and 8 oranges` | 8.0 (last wins) | Ambiguous by construction — task expects one committed number; two-quantity answers usually mean the model answered a sub-question, not the final one | Low-medium | No patch — again a prompt-compliance signal, arguably the *right* place to fail (escalate) |
| **Scientific notation** | `3e8` | **8.0** | **Wrong**, badly so (300,000,000 vs 8) — `e`/`E` split the mantissa and exponent into two separate `_NUM_RE` matches, keeping the last | Low (no physics-scale problems in this word-problem generator family; but catastrophic if it ever occurs) | **SAFE patch available**, cheap to add, but lowest priority (least realistic) |
| Scientific ("3 x 10^8") | prose form | 8.0 | Wrong, same failure shape | Low | Same as above |
| **Time, hour+minute** | `2 hours 30 minutes` | **30.0** | Wrong — loses the hour component entirely, keeps only minutes | **Medium-high** — the corpus already has both an hours-only gold (`6 hours`) and a minutes-only gold (`109 minutes`) from the *same* generator template family; a combined-unit phrasing is a plausible next variant | **SAFE patch available** (convert to a single unit, e.g. total minutes, when both appear) — moderate implementation risk of choosing the "right" combination rule, see patch notes |
| Time, clock format | `2:30 PM` | 30.0 | Wrong for the same colon/last-number reason | Low (final numeric answers as clock times don't fit this task family) | Not worth the complexity given low realism |
| Time, single unit (baseline) | `6 hours`, `109 minutes` | 6.0, 109.0 | Correct | — | No patch needed |
| **Ratio (colon)** | `3:2`, `10:9` | **2.0, 9.0** (second term only) | **Wrong in spirit** — collapses a two-part committed value to one number, discarding the first term entirely | **High** — `10:9` is a *verbatim real gold answer* in the corpus (`grok_mathematical_reasoning_hard_7`); the whole ANSWER-line + program-check pipeline is structurally unable to verify ratio-shaped answers, since the translator call is prompted for "ONE Python arithmetic expression" that "computes the final numeric answer" — a ratio has no single numeric answer to compute | **RISKY to patch cheaply** — see dedicated note below; this is an architectural gap, not a tokenizer bug |
| Indian separators | `1,20,000`, `1,20,00,000` | 120000.0, 12000000.0 | Correct — `_NUM_RE`'s `[\d,]*` has no positional grouping validation, so any comma-grouping style round-trips correctly through `.replace(",","")` | Low (all prompts are in a US-style generator corpus) | No patch needed |
| Unit-suffixed number | `45 km/h`, `45%`, `40 square meters` | 45.0, 45.0, 40.0 | Correct in all three | — | No patch needed |

### extract_expression / run_expression (the independent-translation side of the check)

- Scientific notation is a **non-issue on this side**: `3e8`, `1.5e-3`, and `3 * 10**8`
  all pass `_EXPR_OK` and evaluate correctly via `run_expression` (300000000.0, 0.0015,
  300000000.0) — Python's own float-literal grammar handles it natively. Only the
  *stated-answer* extraction side mangles scientific notation; the *program* side is
  fine. This confirms the asymmetry: a model that both answers *and* explains its
  math in scientific notation would get a real, correctly-computed program value
  compared against a badly mis-extracted stated value → false disagreement → escalate.
  Cost, not correctness, and further evidence the fix belongs on the extraction side only.
- Prose-style exponents (`3 x 10^8`) are rejected outright by `_EXPR_OK` (no `^` or `x`
  multiplication in the whitelist) — `extract_expression` returns `None`, which is the
  documented tri-state "no check possible," never a wrong verdict.
- `numbers_agree`'s 0.5%-relative / 2-cent-absolute tolerance was not stressed by any
  adversarial case above — it's downstream of extraction, so the bugs found are all
  upstream of it.

---

## Stage 1 patch ranking (report only — nothing below was applied)

1. **[SAFE] Fraction + trailing unit** (`3/4 cup` → 0.75, not 4.0). Highest-value fix:
   corpus already has a bare-fraction gold in this exact family, and the current
   fullmatch-only regex is one word away from breaking on it. Minimal patch: try the
   fraction match against the first whitespace-delimited token of the ANSWER remainder
   (or `re.match` anchored at the start instead of `re.fullmatch` on the whole
   remainder) rather than requiring the entire remainder to be just the fraction.
   Pure robustness — cannot manufacture a false agreement, only prevents a correct
   `3/4`-shaped answer from being needlessly discarded.

2. **[SAFE] Mixed fractions** (`1 1/2` → 1.5, not 2.0). Same family as #1; needs a
   distinct `N N2/D` pattern (whole number + space + fraction) checked *before* the
   bare-fraction pattern, since `nums()`'s fallback currently shreds it into three
   independent numbers. Same fail-safe argument applies.

3. **[SAFE] Hour+minute phrase** (`2 hours 30 minutes`). Lower priority than #1/#2 —
   requires picking a normalization target (decimal hours vs. total minutes) that
   matches what the independent program-check translation is likely to produce, or the
   fix just trades one false-disagreement shape for another. Recommend: only apply if
   time allows; the current behavior already fails safe (escalates), so the cost is
   token spend, not correctness. If patched, extract *both* numbers and expose them
   (e.g. as decimal-hours = hours + minutes/60) rather than guessing which unit the
   task wants — let `numbers_agree`'s tolerance-based comparison against the program
   value pick the right one, similar to the existing percent×100 fallback pattern.

4. **[SAFE, low priority] Scientific notation** (`3e8` → 300000000.0, not 8.0). Cheap
   to add (recognize `\d+\.?\d*[eE][+-]?\d+` as one token before falling back to the
   plain-digit scan) but lowest realism in this task family — no physics-scale prompts
   observed in 36 real tasks or their generator style. Do if time remains after #1-#3.

5. **[RISKY / architectural — do not attempt as a quick patch] Ratio-shaped answers**
   (`10:9`). This is not a tokenizer bug like the others — it's a structural mismatch
   between the verification architecture (one committed number, checked against one
   independently-computed expression) and a task shape that has no single "final
   numeric answer" to compute. Two bad options: (a) parse `10:9` as `10/9 = 1.111` and
   hope the translator also reduces the ratio problem to a single quotient — fragile,
   since a ratio problem's "obvious" arithmetic expression is ambiguous (part-to-part
   vs. part-to-whole, which term is numerator); a wrong guess here on either side of
   the comparison is a genuine RISKY change, because unlike the shapes above, a
   coincidental agreement between two independently-wrong single-number reductions of
   a ratio *could* bless a wrong ratio answer. (b) Special-case ratio detection to
   always route to `unknown` → self-consistency check instead of the program check —
   safer, but self-consistency is the suite's weakest signal (57% strict per
   `agent/router.py`'s own comment) and this is a 1-of-36-task shape, so the expected-
   value case for spending effort here is weak. Recommend: leave as-is; flag as a known
   gap for future task-generator refreshes rather than patching under deadline
   pressure. **Verified against the real container run below** (see batch grading) —
   the exact `grok_mathematical_reasoning_hard_7` ratio task is checked end-to-end.

6. **[Not a verifier bug] Ranges and multi-number answers.** `40-50`, `between 40 and
   50`, `12 apples and 8 oranges` all resolve to "last number wins," which is
   ambiguous by construction. These are prompt-compliance failures (the PROMPT_HINTS
   explicitly demand one committed value on the ANSWER line) rather than extraction
   bugs — "fixing" the verifier to guess at multi-value intent would be RISKY (inventing
   semantics for a shape the task design already tries to prevent) for no realistic
   payoff (never observed in 36 real prompts). No patch recommended.

---

## Stage 1b — addendum found DURING Stage 2 grading (new unit-level finding)

**The 2102e09 bare-fraction fix is scoped to the ANSWER-line branch only.** The
last-digit-bearing-lines fallback path in `extract_final_number` still collapses any
bare fraction to its **denominator**:

```
extract_final_number("ANSWER: 13/15")            -> 0.8667   (fixed branch)
extract_final_number("13/15")                    -> 15.0     (unfixed fallback branch)
extract_final_number("The tank is 13/15 full.")  -> 15.0     (unfixed fallback branch)
extract_final_number("3/4")                      -> 4.0
```

Why this matters more than the Stage 1 shapes:
1. **It's evidenced by a real dev task**, not a hypothetical: the container run below
   produced `7/15` for `grok_mathematical_reasoning_hard_3` (gold `13/15`), and my own
   first-pass auto-grader **marked it correct** — gold `13/15` → last number 15.0,
   answer `7/15` → last number 15.0, "agree." Any two different fractions over the same
   denominator falsely agree on this path. Caught only on manual review.
2. **The remote-audit path (VERDICTS V16) runs through this branch.** Local answers
   carry `ANSWER:` because PROMPT_HINTS demands it, but remote answers don't —
   `REMOTE_SUFFIX` says only "Answer directly and concisely." A remote math answer
   like "The tank is 13/15 full." gets its *denominator* extracted as the stated
   value, and the audit comparison runs against garbage. Direction of failure in the
   agent (stated-vs-program-value) is still fail-safe (spurious disagreement →
   fallback model gets a shot), but it's a *live* mis-extraction on the actual paid
   path, unlike the Stage 1 shapes which mostly need a hypothetical answer style.
3. **Fail-OPEN in judge contexts.** `eval/judge.py::_judge_math`'s regex fallback has
   the same collapse (gold `13/15` → `_numbers` gives `[13,15]` → picks last → 15.0),
   so a wrong `7/15` answer *passes* against a `13/15` gold — agreement-by-artifact,
   the one genuinely fail-open instance found in this sweep. Mitigated in practice:
   `math_verify` IS installed in the dev venv and takes priority (`verify(parse('13/15'),
   parse('7/15'))` correctly returns False); the regex fallback only bites where
   math_verify is missing. Worth knowing before trusting historic dev numbers computed
   on hosts without math_verify.

---

## Stage 2 — container run: all 36 mathematical_reasoning tasks, LOCAL-ONLY

Setup: `ghcr.io/anbu-00001/amda-agent:latest` (id `1c3d756b2439`), two runs of
`docker run --rm --memory=4g --memory-swap=4g --cpus=2 -e TOTAL_BUDGET_S=540`, tasks
mounted at `/input/tasks.json`, no `FIREWORKS_API_KEY` (escalation dead-ends → the
"Unable to answer." marker = escalation-needed). Batch1 = 20 tasks (518.9s, exit 0),
batch2 = 16 tasks (513.2s, exit 0). Artifacts: `eval/tmp_math_sweep/{batch1,batch2}/
tasks.json`, `{out1,out2}/results.json`, `batch*_container.log`, `grading_output.txt`.

**Timing caveat (per instructions, correctness only is judged):** two other agent
containers ran concurrently on this host during the sweep (4 × ~2-CPU containers on a
12-core box, 3.5 GB swap in use, <200 MB free RAM at times). The stderr summaries show
`local: 0 | remote: 0 | scored tokens: 0` — **every single answer shipped via the
`fallback` route** (router's last-resort "Give ONLY the final numeric answer" retry,
max_tokens=32) or as "Unable to answer." The full local pipeline (step-by-step answer →
`_math_program_check` translator call → verified ship) never once completed inside the
25 s/request timeout under this contention. So this run measures the **fallback floor**,
not the verified pipeline — contrast with the uncontended 2026-07-09 full-228 benchmark
(VERDICTS V24) where math scored 83% and `local+program` went 28 pass / 0 fail.

**Contract check: passed.** Valid JSON both batches, all 36 task_ids present, exit 0,
both under the 540 s budget.

### Headline counts (manual grade, trusting current corrected golds)

| Verdict | Count | / 36 |
|---|---:|---:|
| Correct | **10** | 28% |
| Wrong | **20** | 56% |
| Unable ("Unable to answer." = would-escalate marker) | **6** | 17% |
| Missing | 0 | — |

Auto-grader said 11 correct; manual review demoted `grok_hard_3` (`7/15` vs gold
`13/15` — the Stage 1b false-agree artifact). All 19 other flagged answers confirmed
genuinely wrong by independent recomputation.

In a keyed (real) run, all 26 non-correct tasks would have escalated to remote instead
of shipping a fallback guess — the 28% is the floor when *both* verification and remote
are unavailable, not the pipeline's accuracy.

### Correct (10)

`chatgpt_easy_1` (75), `chatgpt_easy_2` ($40), `chatgpt_med_2` (240000),
`chatgpt_hard_1` (1060.90), `grok_easy_1` ($30), `grok_easy_2` (40),
`grok_hard_1` (11576), `grok_easy_1_dup2` (30), `grok_med_2_dup2` (6 hours),
`grok_hard_1_dup2` (1158). Pattern: every 1-2-step task passed, plus the three
textbook-classic compound-interest values (1060.90 / 11576 / 1158) that a 4B most
plausibly knows as memorized worked examples — the only "hard" tasks it survived
without chain-of-thought.

### Wrong (20) — one-line root cause each

All 20 shipped via the 32-token, no-steps fallback retry; the dominant root cause is
uniform — **a 4B doing multi-step arithmetic in one shot with chain-of-thought
explicitly forbidden by the retry prompt** — with per-task detail:

| Task | Agent | Gold | Root cause |
|---|---|---|---|
| chatgpt_med_1 | "…Total distance: 1" | 60 mph | 32-token cap truncated mid-derivation (model ignored "no steps", got cut; it had already written "= 60 mph" twice but never committed) |
| grok_med_2 | $42 | 63 | two-step percentage chain error (40% then 30%-of-remainder) |
| grok_med_1_dup2 | $144 | 132 | discount-then-tax chain error |
| grok_hard_1_dup3 | 7324 | 5372 | 3-stage compound growth + emigration; no CoT |
| grok_hard_2 | 6 | 5.33 | work-rate two-phase; answered a rounded/garbled total |
| grok_hard_3 | 7/15 | 13/15 | pipe fill/drain fraction error (also the false-agree grader trap, Stage 1b) |
| grok_hard_7 | 1.5:1 | 10:9 | ratio task — wrong ratio AND non-normalized shape; the one task the program-check architecture couldn't have verified anyway (Stage 1 #5) |
| grok_hard_8 | 1/2 | 1 | incoherent-premise task (gold degenerately 1 per 2026-07-09 note); model guessed a fraction |
| grok_hard_9 | 600 | 500 | mixture-dilution equation error |
| grok_hard_10 | 2 | 6 | catch-up problem; likely reported head-start hours, not catch-up time |
| synth_hard_1 | 412.80 | $360.91 | 3-step percent chain (raise/discount/tax) error |
| synth_hard_2 | 576.72 | $617.03 | same template, same failure |
| synth_hard_4 | 292.48 | $302.94 | same template, same failure |
| synth_hard_6 | 60 | 141 min | combined work-rate → minutes; wildly off |
| synth_hard_7 | 120 | 122 min | rounded 2.034 h to 2 h *then* converted — precision loss without CoT |
| synth_hard_8 | 120 | 104 min | work-rate error, same template |
| synth_hard_9 | 10896 | 8596 | compound-growth delta error |
| synth_hard_10 | 10788 | 6686 | same template, same failure |
| synth_hard_11 | 10393 | 5626 | same template, same failure |
| synth_hard_12 | 14883 | 15220 | same template; close (2% off — outside every tolerance) |

### Unable (6) — escalation-needed markers

`grok_med_1`, `grok_hard_4`, `grok_hard_5`, `grok_hard_6` (batch1 — the last three are
the batch tail, where the 540 s deadline check `deadline - now > REQUEST_TIMEOUT_S + 5`
stopped even the fallback retry), `synth_hard_3`, `synth_hard_5` (batch2 — mid-batch
retry returned empty). In a keyed run all 6 route to remote.

### What Stage 2 establishes

1. **No fail-open at system level.** Under the worst conditions this sweep could
   produce (contention-starved local inference, no remote), the agent never shipped a
   *falsely verified* answer — 0 tasks routed `local+program`; every degraded answer
   is honestly a last-resort guess or an explicit marker. The fail-safe direction
   claimed in Stage 1 holds end-to-end.
2. **The fallback floor is 28%** on this dev set — relevant only to the doomsday
   scenario (no key AND starved CPU). The verified-pipeline number of record remains
   V24's 83% (uncontended host).
3. **The ratio task (`hard_7`) confirms the Stage 1 architectural gap in vivo**: the
   answer produced (`1.5:1`) is exactly the shape `extract_final_number` reads as
   `1.0` — even a *correct* `10:9` here could not have been program-verified.
4. **Contention sensitivity is real but was self-inflicted here** (4 concurrent
   containers). The judging VM runs one container; the 2026-07-08 constrained-Docker
   test and V24 bench show the pipeline completing normally at 2 vCPU uncontended.
   Still, the 25 s request timeout is the single point through which ALL verified-path
   value disappears — worth knowing, not necessarily worth changing.

---

## Final consolidated patch ranking (SAFE/RISKY, report only — no code edited)

1. **[SAFE — do first] Fraction collapse-to-denominator on the non-ANSWER-line path**
   (Stage 1b). Evidence: real dev task + live remote-audit path + fail-open judge
   fallback. Minimal patch, two independent halves:
   a. In `extract_final_number`'s last-lines loop, apply the same bare-fraction
      `fullmatch` to each *line* (or to the line minus a short trailing word) before
      the `nums()` last-number fallback. Conservative: only a line that IS a fraction
      is converted — derivation lines like `180/3 = 60` don't fullmatch and are
      untouched.
   b. In `eval/judge.py::_judge_math`'s regex fallback, same guard for gold and answer
      (or simply require math_verify at judge time). This is the only fail-open fix in
      the list; it corrects the *grader*, not the agent.
   Additionally (zero-code alternative for the agent half): append "End with
   `ANSWER: <value>`" to the math remote suffix so remote answers route through the
   already-hardened ANSWER-line branch — costs a handful of scored input tokens.

2. **[SAFE] Fraction + trailing unit on the ANSWER line** (`ANSWER: 3/4 cup` → 0.75,
   not 4.0). Anchor the fraction regex with `re.match` instead of `re.fullmatch` (or
   match the first whitespace token). Same family as #1a — arguably the same patch.

3. **[SAFE] Mixed fractions** (`ANSWER: 1 1/2` → 1.5, not 2.0). Add an
   `N N/D` pattern checked before the bare-fraction pattern.

4. **[SAFE] Hour+minute phrase** (`2 hours 30 minutes` → 30.0 today). Extract as
   decimal hours (h + m/60) and let `numbers_agree` tolerance handle unit choice,
   mirroring the percent×100 fallback pattern. Only if time allows — current behavior
   fails safe.

5. **[SAFE, lowest priority] Scientific notation on the extraction side** (`3e8` →
   8.0 today; the expression/eval side already handles it correctly). One regex token.
   Least realistic shape for this task family.

6. **[RISKY — do not patch] Ratio-shaped answers** (`10:9`). Architectural gap, not a
   tokenizer bug; any cheap single-number reduction risks coincidental false agreement
   (the one place a patch could bless a wrong answer). Confirmed in vivo by `hard_7`.
   Leave as known limitation.

7. **[Not a bug — do not patch] Ranges / multi-number answers.** Prompt-compliance
   failures by construction; escalation is the correct response.

**Cross-cutting observation:** every SAFE patch above shares one root cause — the
`nums()`-last-number fallback treats `/`, `:`, `e`, and unit words as number
*separators* when they are actually part of one committed value. A single "recognize
composite numeric tokens (fraction, mixed fraction, scientific) before splitting"
pre-pass in `extract_final_number` fixes #1a, #2, #3, and #5 together in ~10 lines,
all fail-safe by the Stage 1 argument (mis-extraction today only manufactures
*disagreement*, so any fix can only recover verifications that are currently lost —
except in the judge fallback, #1b, which is the one fail-open case and should be
fixed or explicitly gated on math_verify).

*Report completed 2026-07-11 ~10:30 IST, well ahead of the 16:00 UTC deadline. Prior
lost batch data was never recovered (confirmed absent from git history and scratch
dirs); everything above was re-derived fresh.*
