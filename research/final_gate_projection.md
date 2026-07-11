# Final gate-pass projection — 2026-07-11 evening

Verdict up front: **STOP — ship the current image.** Point-estimate P(≥16/19)
= **93.6%**, expected score **17.3/19**. The two weak categories
(logical_reasoning and sentiment_classification, both 5/7) have **no
verified surgical fix**: the "raise the logic token cap / add a hint" idea
was tested live against the remote model and **disproven** (details in the
probe section), and the sentiment misses are consistent 4B trap-shape errors
that no one-line change reaches. The only mechanically-plausible remaining
fix is a solver-audit of remote logic answers — a routing-code change with
unproven efficacy that would need a rebuild plus a full validation cycle;
per the bias-to-STOP rule it is documented below but **not recommended**.

## What ran

- Image: `ghcr.io/anbu-00001/amda-agent:latest`, digest `fb43f519` (built
  2026-07-11 18:27 from HEAD `f4d5353`; contains remote-first
  factual/NER/summarisation, sentiment closed-label guard, NER honorific
  hints, math extraction hardening, remote transient retry). Working tree
  clean — what was measured is exactly what ships.
- Sample: **56 tasks = 7 per category × 8 categories** from
  `data/dev_tasks/merged.json`, mixed difficulty (hard/medium/easy
  round-robin), **preferring `_dup`/`_dup2`/`_dup3` variants** (39 of 56 are
  dups — the closest thing we have to prompts not used in prior tuning,
  mirroring the refreshed-prompt final).
- Exclusions: all 11 broken `grok_logical_reasoning` tasks per
  `research/logic_code_shape_sweep.md` (8 placeholder/underspecified golds +
  provably-wrong golds `hard_2`, `hard_5`, `hard_1_dup3`). None sampled.
- Run: 4 sequential docker batches of 14 (never parallel), `--memory=4g
  --memory-swap=4g --cpus=2`, `TOTAL_BUDGET_S=540`, `REMOTE_RPM_LIMIT=5`
  (rate-limited stand-in key). All 4 exited 0, valid JSON, all 56 task_ids
  answered, every batch well under budget (386.3s / 238.8s / 286.4s /
  148.7s).
- Grading: `eval/judge.py` logic verbatim (`eval/tmp_final_gate/grade_all.py`),
  then **every fail and every unsure manually verified** — code answers
  executed against acceptance examples (Python and JS), logic golds
  brute-forced by exhaustive permutation, FK/summarisation paraphrases read
  against acceptance criteria. Corrected verdicts with per-task reasons:
  `eval/tmp_final_gate/graded_corrected.json`.

## Per-category results

| category | judge strict | artifact-corrected | what the correction was |
|---|---|---|---|
| code_debugging | 0/7 (6 unsure, 1 fail) | **7/7** | all 6 unsure verified by execution; the 1 "fail" is a broken-gold task (prompt code provably correct; agent's "no bug" matches the gold's own "actually correct") |
| code_generation | 0/7 (7 unsure) | **7/7** | all executed correct vs examples (incl. both JS tasks) |
| factual_knowledge | 3/7 | **7/7** | 4 unsure = correct paraphrases under-credited by keyword overlap (the known artifact) |
| logical_reasoning | 6/7 | **5/7** | judge wrong in BOTH directions: 1 false fail (answer exactly matches gold, 0% overlap because "D" ≠ "Book D") and **2 false passes** (fail-open at 82%/62% overlap on genuinely wrong answers — confirmed by brute-forcing the unique solutions) |
| mathematical_reasoning | 7/7 | **7/7** | clean; incl. the 3-stage population task (5372) that failed in the no-key sweep |
| named_entity_recognition | 6/7 | **6/7** | the miss: gold truncated in dataset, graded vs intact acceptance — answer covered 4/5 required items, tagged "Geneva Conference" ORG instead of emitting Geneva LOCATION (conservative fail) |
| sentiment_classification | 5/7 | **5/7** | both fails genuine and local-shipped: litotes ("I don't hate this movie" → said "Neutral to slightly positive", gold Positive) and neutral-factual ("went to the park and read" → said Positive, gold Neutral) |
| text_summarisation | 6/7 | **7/7** | 1 unsure = correct one-sentence summary at 38% overlap; all format constraints (exact sentence counts, word limits, mandated tokens "1.8"/"600"/"dynamics") satisfied |
| **TOTAL** | 33/56 = 59% | **51/56 = 91.1%** | |

Judge-artifact taxonomy for the record: the deterministic judge under-credits
correct answers in code (no semantic check), FK/summarisation (paraphrase),
and exact-but-differently-worded logic — and **over-credits wrong logic**
via keyword overlap (both real logic fails scored as "pass"). Strict dev
scores for logical_reasoning are inflated, not deflated. An LLM-intent judge
(what the hidden eval uses) lands near the corrected column.

## Gate projection

Model: hidden eval = 19 tasks, every category contributes 2, three unknown
categories contribute a 3rd; exact enumeration over all C(8,3)=56
assignments; tasks Bernoulli at the category's corrected rate
(`eval/tmp_final_gate/project_gate.py`).

| scenario | P(≥16/19) | expected score |
|---|---|---|
| **Point estimate** (corrected rates as measured) | **93.6%** (worst-assignment 85.9%, best 97.1%) | 17.3/19 |
| Pessimistic (broken-gold code_debugging task + both borderline calls counted against us) | 80.2% | 16.6/19 |
| Ultra-conservative (Laplace +1 smoothing on every category, ignores all prior evidence) | 54.1% | 15.6/19 |

The Laplace row overstates risk — it shrinks even categories with strong
independent evidence (math 100% here on top of 83% over 36 dev tasks with
program-check; NER 77% over all 26; FK 100%-ceiling over all 28 in
`remote_path_validation.md`). Honest range: **~80-94% gate probability,
point estimate low-90s.** For reference, the 2026-07-10 leaderboard image
scored 15/19; this sample puts the current image ~2 tasks stronger in
expectation.

Token economics (side check): 5,017 scored input + 2,946 scored output
tokens for 56 tasks ≈ 142/task → a 19-task run lands ≈ 2.7k scored tokens.
Rank cost of the accuracy tilt remains small.

## Weakest category: logical_reasoning (5/7) — tied by sentiment, but structural

**One-line diagnosis: under 2-vCPU judging constraints the local
solver-verified path almost never fires (6 of 7 solver-eligible puzzles
escalated; batch route summary `local: 1, remote: 13`), and the remote
model deterministically fails ~1/3 of 5-variable CSPs — the strong verifier
we built exists but sits on the path the router no longer reaches.**

Sentiment (also 5/7) is different in kind: the 4B mislabels classic trap
shapes (litotes, neutral-factual) *consistently*, so the second
constrained-read agreement check confirms the error instead of catching it —
same blind spot as the JS "consistent hallucination" cases in
`logic_code_shape_sweep.md`. No cheap check can catch a consistently wrong
classifier; that is a model-capability ceiling, not a routing bug.

## The probe that killed the easy fix (do not re-litigate this)

Both failed logic tasks were re-run directly against the remote model
(`gemma-4-31b` stand-in, temp 0, exact router prompt + suffix) at the
shipped 192-token cap AND at a raised 320-token cap
(`eval/tmp_final_gate/logic_probe.json`):

- `gemini_logical_reasoning_hard_1`: at 320 tokens it *still* churns through
  wrong assignments ("Wait, checking constraint 7... Let me re-evaluate")
  and truncates again; its last complete attempt **violates constraint 4
  while claiming it passes**. Truncation is a symptom; the model cannot
  solve the puzzle at any cap.
- `gemini_logical_reasoning_med_1_dup2`: byte-identical wrong answer at both
  caps (violates "Casey did not finish last"). Deterministic capability
  failure.

So `REMOTE_MAX_TOKENS` raise and/or a `REMOTE_HINTS["logical_reasoning"]`
nudge — the only one-line candidates — are **measured non-fixes**. Ditto
sentiment: there is no prompt line that makes a 4B stop reading "went to the
park and read a book" as positive *consistently*.

## STOP/GO: **STOP**

- No reproducible failure with a **verified** one-line fix exists. The one
  candidate that looked like it (logic token cap) was tested and disproven
  before it could burn the lead.
- The only mechanically-sound remaining idea — run `_logic_solver_check` on
  the *remote* logic answer and ship the solver override, mirroring the
  math remote-audit (~6 lines in `agent/router.py::solve`) — has **unproven
  efficacy**: it depends on the local 4B producing a decisive translation
  under the same 2-vCPU pressure that made these tasks escalate in the
  first place. It needs a rebuild + a full 26-task logic validation run.
  Even in the extended window (Jul 12 22:00 UTC), that is an
  unforced-error risk against a ~94% point-estimate gate: expected gain
  ≈ +3-5pts of gate probability, worst case a botched routing change in
  our second-strongest verifier's category. **Not recommended.** If the
  team overrides, the non-negotiable protocol is: implement, rebuild, run
  ALL 26 clean logic dev tasks + one 14-task mixed-category smoke batch,
  and revert unless logic ≥6/7 with zero regressions elsewhere.
- Explicitly rejected: tilting sentiment to REMOTE_FIRST (unmeasured
  remote-vs-local A/B on this category = the exact class of same-night
  unverified change V25 warns about), and any judge-time change (the eval's
  judge is not ours to fix).

The image is at its practical ceiling for safe changes. Ship it.

## Artifacts

- Inputs/outputs/logs: `eval/tmp_final_gate/batch{1..4}/`,
  `eval/tmp_final_gate/batch{1..4}_container.log`
- Judge verdicts: `eval/tmp_final_gate/graded_all.json`; manually corrected
  verdicts with per-task reasons: `eval/tmp_final_gate/graded_corrected.json`
- Sample + golds: `eval/tmp_final_gate/sample_golds.json`
- Projection: `eval/tmp_final_gate/project_gate.py`; remote probe:
  `eval/tmp_final_gate/logic_probe.json`
