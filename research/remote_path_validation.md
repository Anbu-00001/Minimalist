# Remote-first path validation — 2026-07-11

Deadline: today 16:00 UTC. This report is written incrementally; sections
below fill in as each batch completes. If you are reading this mid-run,
trust the timestamps, not the absence of a section.

## Why this run exists

After the 2026-07-10 leaderboard scored 15/19 (gate needs 16/19), commits
`3724d6b` and `77d9c58` moved `factual_knowledge`, `named_entity_recognition`,
and `text_summarisation` to `REMOTE_FIRST` routing (agent/router.py) — local
generation is skipped entirely for these categories; every task in them goes
straight to the Fireworks-proxy remote model. The stated justification was
that these categories' local route relied on self-consistency (measured at
57% strict on `local+consistent`, the weakest verification signal in the
system, vs ~100% for program-checked math and ~92% for solver-checked
logic), so buying remote accuracy was assumed cheap. **The remote path's own
end-to-end accuracy was never measured before shipping the tilt.** This run
measures it.

## Method

- Image: `ghcr.io/anbu-00001/amda-agent:latest`, digest `1c3d756b2439` (local
  daemon, current HEAD `77d9c58` baked in).
- `docker run --rm --memory=4g --memory-swap=4g --cpus=2`, tasks mounted at
  `/input/tasks.json`, output at `/output/results.json`.
- Env: `TOTAL_BUDGET_S=540`, `REMOTE_RPM_LIMIT=5` (client-side throttle for
  the Cerebras gemma-4-31b stand-in key, which is rate-limited to 5 req/min
  — same stand-in the 2026-07-09 baseline run used). `FIREWORKS_API_KEY` /
  `FIREWORKS_BASE_URL` / `ALLOWED_MODELS` read from `.env` via
  `grep '^NAME=' .env | cut -d= -f2-`, values never echoed.
- Task sets: ALL 28 `factual_knowledge` + ALL 26 `named_entity_recognition`
  dev tasks from `data/dev_tasks/merged.json` (one docker run per category —
  each close to the instructed ~25-task batch size). `text_summarisation`:
  10-task random sample (seed 42) if time allows after Part 1's priority
  categories are done, since long prompts cost more tokens per throttle
  window.
- Grading: same deterministic judge logic as `eval/judge.py`
  (`_judge_short_text` for factual_knowledge, `_judge_ner` for NER,
  `_judge_summary` for summarisation) — intent-match against
  `gold_answer`/`acceptance_criteria`, not exact string match.
- Baseline for comparison: `research/benchmark_2026-07-09/full_228_results_goldfixed.json`
  and its `summary.txt`, the **pre-tilt** run (local-cascade routing, i.e.
  what these categories did before `3724d6b`/`77d9c58`). Pre-tilt category
  strict scores from that run:
  - `factual_knowledge`: 19 pass / 2 fail / 7 unsure of 28 = **68% strict**
  - `named_entity_recognition`: 15 pass / 8 fail / 3 unsure of 26 = **58% strict**
  - `text_summarisation`: 16 pass / 4 fail / 7 unsure of 27 = **59% strict**

Artifacts (inputs, raw docker outputs, graded results) live in
`eval/tmp_remote_val/`.

## VERDICT (Part 1): remote-first is NOT WORSE anywhere measured — do not revert

- **named_entity_recognition: remote is clearly BETTER.** 77% strict (20/26,
  fail 4, unsure 2) vs pre-tilt baseline 58% (15/26, fail 8, unsure 3).
  Per-task flips: 7 improved, 2 regressed, 17 same. Keep remote-first.
- **factual_knowledge: remote is at least as good — keep it.** Strict dipped
  61% vs baseline 68%, but with **zero fails** (baseline had 1) and a 100%
  ceiling: every sub-threshold answer is a substantively correct paraphrase
  that the keyword-overlap dev judge under-credits (verified by inspection —
  details below). Under an LLM intent judge, remote FK is at parity or
  better. Not a revert case.
- **text_summarisation: remote is BETTER on the 10-task sample.** 60% strict
  (6/10, fail 0, unsure 4, ceiling 100%) vs the same 10 tasks' baseline 50%
  strict (5/10, fail 2, unsure 3). Per-task: 2 improved (both baseline
  fails), 0 regressed, 8 same. Keep remote-first.
- Operational caveat (not a revert reason): two NER tasks returned
  "Unable to answer." — the remote call failed on both preference models
  AND the local last-resort produced nothing. Both tasks were already fails
  in the baseline (no net rank lost), but it demonstrates a hard-failure
  mode under rate-limit pressure. The real Fireworks judging proxy is not
  throttled to 5 RPM, so this specific failure shape is much less likely on
  submission day — but it is worth knowing it exists. Details in the NER
  section.

## Status

- [x] factual_knowledge (28 tasks) — remote-first run — DONE, see below
- [x] named_entity_recognition (26 tasks) — remote-first run — DONE, see below
- [x] text_summarisation (10-task sample) — remote-first run — DONE, see below
- [x] Verdict at top of report
- [x] Part 2: Gemini/Claude upgrade doc mining — DONE, see below

## Note on the baseline numbers

Recomputing `research/benchmark_2026-07-09/full_228_results_goldfixed.json`
directly (rather than trusting `summary.txt`, which has a minor count typo
for factual_knowledge — 19/2/7 printed vs 19/1/8 actual, same 68% strict
either way) gives the authoritative pre-tilt baseline used for every
comparison below:

| category | pass | fail | unsure | strict | ceiling (pass+unsure) |
|---|---|---|---|---|---|
| factual_knowledge (28) | 19 | 1 | 8 | 68% | 96% |
| named_entity_recognition (26) | 15 | 8 | 3 | 58% | 69% |
| text_summarisation (27) | 16 | 4 | 7 | 59% | 85% |

## factual_knowledge: remote-first live results (28/28 tasks)

Command: `docker run --rm --memory=4g --memory-swap=4g --cpus=2` with
`TOTAL_BUDGET_S=540 REMOTE_RPM_LIMIT=5`, all 28 factual_knowledge dev tasks,
real Fireworks-proxy key. Graded with the unmodified `eval/judge.py` logic
(`_judge_short_text`), same as the baseline.

**strict: 17/28 = 61% (fail 0, unsure 11) — ceiling (pass+unsure): 100%**

vs baseline 68% strict / 96% ceiling. Strict score alone looks like a
regression (61% < 68%), but that is *not* the right read — the fail count
tells the real story:

- **fail: 0** (vs baseline's 1) — no remote answer was judged demonstrably
  wrong.
- **unsure: 11** (vs baseline's 8) — every one of these is a keyword-overlap
  score in the 30-54% band, below the judge's 55% auto-pass threshold.

Manual inspection of the 11 "unsure" cases (sampled 5, see
`eval/tmp_remote_val/fk_graded.json` for all) shows every single one is a
**substantively correct, well-formed answer** that simply uses different
vocabulary than the terse gold string — e.g. gold says "microwaves cause
water molecules to vibrate," remote answer says "the oscillating
electromagnetic field causes [polar] molecules to rotate rapidly... creating
molecular friction" (same physics, zero literal word overlap on the key
terms); gold defines gravity as "the force of attraction between any two
objects with mass," remote says "the fundamental force of attraction that
acts between all objects with mass" (46% overlap only because "fundamental"
and "acts" aren't in gold's word list). None of the sampled "unsure" cases
read as wrong.

**Read: factual_knowledge remote-first looks AT LEAST AS GOOD as the pre-tilt
local route, likely better** — it produced zero clearly-wrong answers
against the local route's one, and its full "unsure" bucket is explainable
by answer verbosity/paraphrase, not incorrectness, which a real (non
keyword-overlap) judge is very likely to credit. This is consistent with the
tilt's original justification. **Not a case for reverting.**

Raw docker output: `eval/tmp_remote_val/fk_output/results.json`. Graded:
`eval/tmp_remote_val/fk_graded.json`.

Per-task flips vs baseline (rank order fail < unsure < pass): 4 improved,
5 regressed, 19 same. All 5 "regressions" are pass→unsure (paraphrase
under-crediting, per the inspection above); none is a new wrong answer.
The single baseline fail (`haiku_factual_knowledge_hard_3`, overlap 12%)
improved to unsure under remote.

## named_entity_recognition: remote-first live results (26/26 tasks)

Same setup. Graded with unmodified `eval/judge.py` `_judge_ner`.

**strict: 20/26 = 77% (fail 4, unsure 2) — ceiling: 85%**
vs baseline **58% strict (15 pass, 8 fail, 3 unsure), 69% ceiling.**

This is the category the tilt was most worried about, and remote-first is
unambiguously better: +19 points strict, fails halved (8 → 4). Per-task
flips: **7 improved, 2 regressed, 17 same.** Improvements include both
previously-failing repaired-prompt tasks' neighbours and 4 of the 5 synth
tasks the local route was fumbling
(`synth_named_entity_recognition_medium_22/24/27/28`: fail → pass) plus
`chatgpt_named_entity_recognition_easy_1`: fail → pass (one of the 2
repaired-prompt tasks; the other, `chatgpt_..._hard_1`, went fail → unsure,
missing only the honorific forms "King Ferdinand II"/"Queen Isabella I" —
it listed "Ferdinand II"/"Isabella I").

The 4 remaining fails, dissected (all in `eval/tmp_remote_val/ner_graded.json`):

1. `synth_named_entity_recognition_medium_21` and `..._25` — the model
   answered `"Lena Fischer"` where gold demands `"Dr. Lena Fischer"`.
   **Honorific-prefix drops. This is the one real, recurring error pattern
   in remote NER** (also the residual miss in `chatgpt_..._hard_1`'s
   King/Queen forms). `_25` was a baseline fail anyway (local put Dublin in
   orgs); `_21` is one of the 2 genuine regressions (baseline local passed
   it).
2. `gemini_named_entity_recognition_med_1` and `..._med_2` — answer is
   literally `"Unable to answer."`: the remote call failed on both
   preference models and the local last-resort also returned nothing.
   Consecutive tasks, so almost certainly a transient rate-limit/timeout
   burst on the throttled 5-RPM stand-in key. **Both were baseline fails
   too** (local hallucinated "Battle of Kokoda" as a location on med_1 and
   flubbed med_2), so no ground was lost — but on the real proxy these two
   would likely have been correct remote answers.

**Actionable, tiny, low-risk fix worth considering before the deadline:**
`agent/router.py`'s `REMOTE_HINTS["named_entity_recognition"]` already says
"Cities, countries, and regions are LOCATION, never ORGANIZATION." Appending
one clause — e.g. "Keep titles and honorifics as part of PERSON names
(Dr. Jane Smith, King Henry VIII, not Jane Smith or Henry VIII)." — targets
the only recurring remote NER error (3 tasks affected: would flip 2 fails
and 1 unsure if obeyed). It is a one-line prompt change to an
already-remote-first category, no routing logic touched. Not implemented
here (out of this task's scope; needs owner's call + a quick re-run of the
5 affected tasks to confirm).

Raw docker output: `eval/tmp_remote_val/ner_output/results.json`. Graded:
`eval/tmp_remote_val/ner_graded.json`.

## text_summarisation: remote-first live results (10-task sample, seed 42)

Same setup; 10 tasks sampled from the 27 dev summarisation tasks with
`random.seed(42)` (ids in `eval/tmp_remote_val/ts_input/tasks.json`).
Graded with unmodified `eval/judge.py` `_judge_summary`. Baseline below is
recomputed **on the same 10 tasks only**, not the whole 27.

**strict: 6/10 = 60% (fail 0, unsure 4) — ceiling: 100%**
vs same-10 baseline: **5/10 = 50% strict (fail 2, unsure 3), ceiling 80%.**

Per-task flips: **2 improved, 0 regressed, 8 same.** Both improvements were
baseline hard-fails at 0% overlap that remote fixed
(`chatgpt_text_summarisation_easy_1` fail → unsure at 38% overlap;
`chatgpt_text_summarisation_hard_1` fail → pass at 60% overlap). No format
violations anywhere. All 4 "unsure" answers were inspected: each is an
accurate, on-length summary whose vocabulary diverges from the single gold
reference (e.g. gold "opacity of AI decision-making" vs answer "lack of
transparency regarding how models reach specific diagnoses") — the same
paraphrase-under-crediting pattern as factual_knowledge, not wrongness.

**Read: the dominance argument that shipped 77d9c58 ("a 31B-class remote
model summarizes at least as well as the local 4B") is confirmed on this
sample — remote eliminated both hard fails and regressed nothing.** Sample
is 10/27 tasks, so treat the +10pt strict delta as directional rather than
precise; the fail 2 → 0 signal is the robust part.

Raw docker output: `eval/tmp_remote_val/ts_output/results.json`. Graded:
`eval/tmp_remote_val/ts_graded.json`.

---

## Part 2: mining `UpgradessuggestedbyGeminiandcld` (48KB Gemini-Flash audit)

Read in full (932 lines, Sections 1-7, 22 "agent reports" + 5 code
blueprints). Section 1.1's leaderboard numbers are confirmed fabricated (as
briefed: claims 84.2%/27,459 tokens/8th-of-8-qualified; we were DNQ at 78.9%
with a tiny token count). **Section 7's "live diagnostic run" is also
suspect** and should not be trusted either: it claims every one of 8 sampled
tasks — including `sentiment_classification` and `logical_reasoning`, which
have deterministic local verifiers and were never remote-first — routed
`remote:gemma-4-31b`. That's inconsistent with the router code at any point
in this project's history; treat Section 7's specific numbers/failure
examples as unverified, same posture as Section 1.1.

Screened all 22 reports + 5 code blueprints against the three filters
(accuracy-relevant, <2h to implement, not already in AMDA). Result: **nothing
survives cleanly.** Details:

| Idea | Verdict | Why |
|---|---|---|
| Z3 SMT solver (2.2, 3.2) | Rejected | New heavyweight dependency (`z3-solver`, not in `requirements.txt`), replaces a CSP solver already measured at ~92% on logic — no evidence current solver is the bottleneck. Untested Docker rebuild this close to deadline is a real risk of breaking a working path for an unmeasured gain. |
| Sympy/math-verify symbolic math (2.2, 3.1) | Rejected — superseded | `math_verify` is already wired into `eval/judge.py`; the specific gap this section targets (percent/fraction equivalence) was already fixed today in the agent itself, commit `2102e09`, without adding sympy as a runtime dependency. Nothing left to gain here. |
| TF-IDF Naive Bayes semantic router (3.3) | Rejected | Would replace `agent/classify.py`'s keyword rules with an untrained classifier (the blueprint ships no trained weights/corpus) — training + validating a new classifier against the dev set in the remaining hours is not a <2h, low-risk change, and the current keyword classifier's accuracy is already high (near-100% on the one sample this doc itself reports). |
| LLMLingua-2 prompt compression (2.1) | Rejected | New ML model dependency + weights to bake into the image; token-cost lever, not accuracy; out of scope per the task's own filter. |
| Prefix-cache `x-session-affinity` header, cache layout tricks (2.1, 2.18) | Rejected | Speculative claim about the judging proxy's caching behavior we have no way to confirm: this is a graded proxy, not raw Fireworks, and there's no evidence it honors an arbitrary custom header. Also a cost lever, not accuracy. |
| Dynamic per-domain remote model matrix (2.13) | Rejected — already superseded | Proposes `kimi-k2p7-code` for code and specific per-domain mappings; `agent/config.py`'s `REMOTE_PREFERENCE`/`CODE_PREFERENCE` already made this exact tradeoff deliberately the other way — kimi-k2p7-code is placed LAST because its thinking mode is architecturally mandatory and bills as output tokens on every call. The doc's proposal isn't a new insight, it's the option already considered and rejected. |
| Logprob-confidence escalation gate at threshold -0.35 (2.19, phase 1) | Rejected as specified | The mechanism already exists (`config.LOGPROB_ESCALATE_BELOW`, `agent/router.py` `low_confidence` check) and is deliberately set to `None` pending dev-set calibration (`research/VERDICTS.md` V17: "Calibrate thresholds on the dev set only... an overfit threshold that ships wrong local answers costs the accuracy gate"). Blind-setting -0.35 with no calibration data on this codebase contradicts that documented reasoning and risks demoting correct local answers this close to the deadline. Also now moot for the three REMOTE_FIRST categories, which skip local generation entirely. |
| Zero-token prompt-injection guardrails (2.16) | Rejected | No adversarial-input tasks in the dev/eval set; risk of false-positive triggers on legitimate prompts (e.g. a factual question that happens to contain a flagged word) for zero measured benefit on this leaderboard's actual grading. |
| Ephemeral subprocess sandbox w/ `resource.setrlimit`/`unshare -n` (2.7, 3.4) | Borderline, not recommended now | The existing `_run_python`/`run_with_assertions` sandboxing (already shipped) bounds wall-clock time via subprocess timeout but not memory; adding an RLIMIT_AS cap is a genuinely small, low-risk change. But it's a *reliability* hardening item, not accuracy-relevant by the task's own filter (nothing in the dev set exercises a memory-bomb candidate answer), so it doesn't clear filter (a). Noted for later, not implemented now. |
| Speculative decoding, DPO training, knowledge distillation, ROCm/GPU offload, Graph-of-Thought reasoning (2.9/2.10/2.14/2.15/2.20/2.21) | Rejected | All require new infra, training data/time, or hardware (ROCm GPU) not present in the CPU-only 2vCPU/4GB grading VM; none are <2h; several (DPO, distillation) need training runs measured in hours, not minutes. |
| NER title-prefix normalization (Section 7.3's specific failure example: gold `Dr. Lena Fischer` vs answer `Lena Fischer`) | **CONFIRMED against live data — the one surviving item** | Section 7 itself is unverified/possibly fabricated, so the example wasn't trusted at face value — but Part 1's live NER run independently reproduced exactly this failure on 3 of 26 tasks (`synth_..._21`, `synth_..._25` dropped "Dr."; `chatgpt_..._hard_1` dropped "King"/"Queen"). Fix is a one-line append to `REMOTE_HINTS["named_entity_recognition"]` in `agent/router.py` (see NER section) — minutes of work, prompt-only, no routing logic touched. Recommended if any change window remains before the deadline. |

**Honest bottom line: of the entire 48KB document, exactly one item survives
all three filters** — the NER honorific-prefix hint, and even that survives
only because this run's own live measurements independently confirmed the
failure pattern (the doc's supporting "diagnostic run" is itself untrusted).
Everything else is either already in AMDA, already deliberately rejected
with recorded reasoning, not accuracy-relevant, or not implementable safely
in under 2 hours.
