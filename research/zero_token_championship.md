# Zero-Token Championship: Research Log — AMDA Track 1

Research question (verbatim from task brief): since a genuine zero-token (fully
local, never escalating) run that clears the accuracy gate would have the best
possible token rank (0, literally unbeatable), how realistic is that as an
actual target, versus accepting some non-zero escalation rate as the pragmatic
ceiling?

Mode: evidence collection + an explicit verdict section at the end (per task
brief, unlike the pure-collection style of `logic_escalation_economics.md`).
Direct quotes are in quotation marks; paraphrases are marked as such. Anything
found only via search-engine synopsis (not confirmed by directly fetching the
primary page) is marked **UNVERIFIED**. Numbers I could not find are reported
as "not found," not guessed.

---

## 1. The accuracy-gate threshold itself

### 1.1 Primary source: the Participant Guide (read directly from the repo)

The file `Participant Guide_ AMD Developer Hackathon (ACT II).pdf` sits in the
repo root and was read directly (not via search) for this research pass.
Verbatim, the entire scoring section for Track 1 reads:

> "Scoring
> 1. Accuracy gate: LLM-Judge evaluates each answer against the expected
> intent. Submissions below the accuracy threshold are excluded from the
> leaderboard.
> 2. Token efficiency: submissions that pass the accuracy gate are ranked
> ascending by total tokens recorded by the judging proxy. Fewer tokens =
> higher rank."

No number, percentage, or pass/fail rubric accompanies this. The guide's own
opening line is explicit about withholding this kind of detail: "Exact
evaluation inputs are intentionally omitted: your agent must be genuinely
capable, not hardcoded to specific answers." The general-rules section adds
constraints (60s container start, 30s/request, 10min total runtime, 10GB
image, English-only responses, no hardcoding/caching) but nothing about
accuracy calibration.

### 1.2 Searched for a leaked/announced number — none found

Searched: `devcommunity.amd.com` official AMD forum thread ("🏃 AMD Developer
Hackathon: ACT II", https://devcommunity.amd.com/t/amd-developer-hackathon-act-ii/596),
lablab.ai Discord (indirectly, via WebSearch only — no direct Discord access
available to this researcher), X/Twitter announcements, and generic "AMD
Developer Hackathon accuracy gate threshold/percentage" queries.

- The AMD forum thread was fetched directly. It references the Participant
  Guide by link but does not restate or add a numeric threshold. Quote (via
  the fetch's own summary, forum thread does not appear to contain a
  differently-worded statement than the guide): "Read the full guide for
  exact I/O formats, environment variables, and scoring details."
- WebSearch of `lablab.ai discord AMD hackathon accuracy gate percentage
  clarify` surfaced only the same public pages already covered in
  `research/hackathon_meta_amd_ecosystem.md` and
  `research/competitors_lablab.md` — no forum/Discord post with an actual
  number.
- WebSearch of `"amd developer hackathon" tie-break token count leaderboard
  rank equal` returned no on-topic result beyond the same event pages.

**Conclusion: the numeric accuracy-gate threshold is not publicly documented
anywhere this researcher could reach.** This should be treated as a genuine
unknown, not estimated or guessed at.

### 1.3 Live leaderboard, refetched this pass — still zero passers, and zero-token submissions are not exempt

Fetched `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
directly (two separate fetch passes, minor count discrepancies between them —
noted below, likely fetch-timing/rendering noise rather than a real change
within minutes).

- Pass 1: 44 Track 1 submissions total. Status breakdown: ACCURACY_GATE_FAILED
  27, PULL_ERROR 10, RUNTIME_ERROR 2, TIMEOUT 2, ZERO_API_CALLS 2 (shown paired
  with ACCURACY_GATE_FAILED — i.e., these two zero-token submissions **also
  failed the accuracy gate**), INVALID_RESULTS_SCHEMA 1, OUTPUT_MISSING 1.
  "No passing submissions are visible on this page segment."
- Pass 2 (immediately after, re-fetched to cross-check): 44 submissions,
  ACCURACY_GATE_FAILED 26, PULL_ERROR 12, RUNTIME_ERROR 2, TIMEOUT 2,
  INVALID_RESULTS_SCHEMA 1, OUTPUT_MISSING 1, ZERO_API_CALLS 2. Quote: "Zero
  submissions appear to have passed evaluation with a token count or ranking
  displayed... No submissions exist outside these error categories." Also
  explicitly: "The page contains no explicit accuracy percentage thresholds,
  specific numerical targets, or tie-breaking rules for equal token counts.
  The only related language states: 'Your agent ran but didn't reach the
  minimum accuracy threshold' (repeated across multiple submissions), but no
  specific percentage is disclosed."
- This updates the 2026-07-08 snapshot already recorded in
  `research/VERDICTS.md` V20 (29 submissions, 16 ACCURACY_GATE_FAILED, zero
  passing). Submission count grew roughly 50%; the accuracy-gate-failure
  count grew proportionally; **the "zero submissions currently pass the
  accuracy gate" finding persists** at this later snapshot.
- **The single most decision-relevant fact found in this whole research
  pass**: at least two teams already tried the "ZERO_API_CALLS" (fully local,
  zero-token) path that the guide explicitly endorses as valid ("flagged:
  ZERO_API_CALLS... is not a failure," per VERDICTS V20's prior reading of the
  guide), and both of those submissions **still failed the accuracy gate**.
  This is direct, current, primary-source evidence that going fully local
  does not, by itself, guarantee clearing the gate — the gate is failing
  local-only and hybrid submissions alike right now.

---

## 2. Realistic accuracy ceiling for small (2-4B) local models, per category

### 2.1 Vendor benchmark numbers for the models named in the brief

All numbers below are from directly-fetched official model cards / technical
reports unless flagged otherwise. **Caveat that applies to the whole table**:
these are full-precision (BF16/FP16) vendor-reported numbers, not our actual
Q4_K_M-quantized runtime numbers, and most are multiple-choice or exact-match
benchmarks, not open-ended LLM-judge grading — both gaps are discussed in
§2.3 and §2.4.

**Qwen3-4B-Instruct-2507** (our currently baked model; HF card fetched
directly, https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507):

| Benchmark | Score | Nearest AMD category |
|---|---|---|
| MMLU-Pro | 69.6 | factual_knowledge (proxy) |
| MMLU-Redux | 84.2 | factual_knowledge (proxy) |
| GPQA | 62.0 | factual_knowledge (proxy, harder tail) |
| ZebraLogic | 80.2 | logical_reasoning (direct match — CSP grid puzzles) |
| IFEval | 83.4 | format-following, cross-cuts summarisation/NER/sentiment |
| LiveCodeBench v6 | 35.1 | code_generation/code_debugging (proxy) |
| MultiPL-E | 76.8 | code_generation (proxy) |
| Aider-Polyglot | 12.9 | code_debugging (proxy, hard end) |
| AIME25 | 47.4 | mathematical_reasoning (proxy, competition-hard) |
| Arena-Hard v2 | 43.4 | general open-ended quality |

The official card does **not** report GSM8K, MATH, or HumanEval for this
specific instruct-2507 checkpoint — searched directly for these (WebSearch +
a discussion thread on the model's own HF page) and confirmed they are simply
absent from the vendor's own published table, not just hard to find.

**Qwen3-4B-Base / Qwen3-1.7B-Base** (Qwen3 Technical Report, arXiv 2505.09388,
Table 7/8, HTML full text fetched directly): these are base pretrain models
(not instruct-2507, not quantized), included only as an approximate capability
ceiling since the official instruct-2507 card omits these specific numbers:

| Model | MMLU | MATH | GSM8K | EvalPlus (HumanEval-family) |
|---|---|---|---|---|
| Qwen3-4B-Base | 72.99 | 54.10 | 87.79 | 63.53 |
| Qwen3-1.7B-Base | 62.63 | 43.50 | 75.44 | 52.70 |

Flagging explicitly: base-model numbers are not directly transferable to the
instruct-tuned, quantized, chat-templated runtime configuration AMDA actually
uses — treat as a rough ceiling reference, not a prediction.

**Llama-3.2-3B-Instruct** (official Meta HF card, fetched directly, BF16):

| Benchmark | Score |
|---|---|
| MMLU (5-shot) | 63.4 |
| GSM8K (8-shot CoT) | 77.7 |
| MATH (0-shot CoT) | 48.0 |
| ARC-C (0-shot) | 78.6 |
| GPQA (0-shot) | 32.8 |
| HellaSwag (0-shot) | 69.8 |
| IFEval | 77.4 |
| BFCL v2 (tool use) | 67.0 |

Card does not report HumanEval, MBPP, or BBH for the 3B variant.

**Phi-4-mini-instruct (3.8B)** (Microsoft HF card, fetched directly):

| Benchmark | Score |
|---|---|
| MMLU (5-shot) | 67.3 |
| MMLU-Pro (0-shot CoT) | 52.8 |
| BigBench Hard (0-shot CoT) | 70.4 |
| GPQA (0-shot CoT) | 25.2 |
| GSM8K (8-shot CoT) | 88.6 |
| MATH (0-shot CoT) | 64.0 |
| Arena-Hard | 32.8 |
| ARC-Challenge (10-shot) | 83.7 |

A WebSearch synopsis (not independently re-verified against the primary card
in this pass) separately characterized IFEval as "Phi-4's weakest benchmark,"
i.e. instruction-following/format-compliance is flagged as a relative
weak point for this model family — relevant to summarisation/NER, which lean
on format compliance, but no specific number was confirmed for this claim.

### 2.2 Where there is genuinely no close published benchmark

Searched specifically for small-model (2-4B), non-benchmark-suite coverage of
three of AMD's eight categories:

- **named_entity_recognition**: searched directly; found only larger-model
  (6B-8B+) biomedical/domain-specific NER studies (e.g., Llama3-8B zero-shot
  F1 40.69%, few-shot F1 61.69% on biomedical NER — not general-domain, not
  2-4B, and not the AMD category's person/org/location/date scope). **No
  published NER benchmark was found for any of the four named 2-4B models on
  general-domain entity extraction.**
- **text_summarisation**: found a relevant academic paper, "Evaluating Small
  Language Models for News Summarization" (ACL Anthology / arXiv 2502.00641),
  which does test small models including Llama-3.2-3B-Instruct and notes
  (paraphrase) that "instruction tuning, not model size, is the key to LLM's
  zero-shot summarization capability" — directionally favorable for a small
  instruct-tuned model, but exact ROUGE/factuality numbers per-model were not
  extracted in this pass (would require a further fetch of the full paper;
  not done here to keep scope bounded).
- **code_debugging** specifically (as distinct from code_generation):
  DebugBench (arXiv 2401.04621) reports open-source LLMs scoring 43.9%-66.6%,
  but per-model breakdown by the 2-4B parameter class was not surfaced in
  this pass's search results — the search tool's own synthesis explicitly
  stated it could not find "specific accuracy data for 3B and 4B parameter
  models specifically" on this benchmark.

**Honest gap**: for NER and code_debugging specifically, there is no
confirmed small-model benchmark ceiling to cite. The best available proxies
remain IFEval (format compliance, relevant to NER's structured-output
requirement) and general code benchmarks (LiveCodeBench/MultiPL-E/EvalPlus)
for code_debugging, both already tabulated above.

### 2.3 Quantization impact (Q4/Q4_K_M) — one strong primary source, one contradicting case study

**Primary source, directly fetched (PDF, read in full)**: "Which
Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on
Llama-3.1-8B-Instruct" (arXiv 2601.14277). This is exactly the right kind of
study — same model, same llama.cpp GGUF quantization stack AMDA uses,
FP16-vs-Q4_K_M head-to-head — but on an 8B model, not a 2-4B one (flagged
below). Table 2, transcribed directly from the fetched PDF:

| Bits | Quant | GSM8K | HellaSwag | IFEval | MMLU | TruthfulQA(mc2) | Avg |
|---|---|---|---|---|---|---|---|
| — | F16 (baseline) | 77.63 | 72.51 | 78.93 | 63.50 | 54.79 | 69.47 |
| 4-bit | Q4_K_S | 77.33 | 72.79 | 80.26 | 62.06 | 53.40 | 69.17 |
| 4-bit | **Q4_K_M** | **77.41** | **72.35** | **79.06** | **62.43** | **54.49** | **69.15** |
| 3-bit | Q3_K_S | 68.31 | 71.87 | 73.89 | 59.31 | 54.08 | 65.49 |

At Q4_K_M specifically (the exact scheme AMDA bakes), the paper's own
findings (quoted): GSM8K "essentially matching baseline" (77.41 vs 77.63, a
-0.22pt change); IFEval *improves slightly* over F16 (79.06 vs 78.93); MMLU
shows the largest (but still modest) drop, -1.07pt. The paper's overall
conclusion (quoted): "mid-bit quantization can preserve capabilities
surprisingly well... 4-bit K-quants typically offer near-maximal compression
at 4-bit while keeping task performance close to the FP16 baseline." Q3-class
(more aggressive than what AMDA uses) is where damage becomes clearly visible
(GSM8K -9.32pt, IFEval -5.04pt at Q3_K_S).

**Caveat on transferability to a 4B model**: this study is on an 8B model.
Smaller models are generally believed to have less parametric redundancy and
may be more sensitive to the same quantization scheme — no primary source
testing Q4_K_M specifically on a 2-4B instruct model across this benchmark
suite was found in this pass. This is a real, unfilled evidence gap.

**Contradicting data point, directly fetched**: "How Small is Enough?
Empirical Evidence of Quantized Small Language Models for Automated Program
Repair" (arXiv 2508.16499v1) reports that naive INT4 quantization (not
llama.cpp's K-quant format — a cruder scheme) on **Qwen2.5-Coder-3B**
collapsed program-repair performance from 38/40 to 0/40 bugs fixed on their
benchmark — a catastrophic failure at a similar parameter scale to our
candidates. This is a small-N (40 total bugs), narrow (code-repair-only)
benchmark, and a different, less sophisticated quantization scheme than
Q4_K_M — so it does not directly contradict the Q4_K_M finding above, but it
is a real, primary-source demonstration that quantization degradation is
scheme- and task-dependent enough to swing from "negligible" to
"catastrophic" depending on exact configuration. **Net finding: no single
number safely describes "the" Q4 accuracy cost; the two best primary sources
found bracket a very wide range (near-zero to total collapse) depending on
scheme and task**, and specifically K-quant-format Q4_K_M (what AMDA uses)
looks close to the negligible end on the one directly relevant study found,
at 8B scale.

### 2.4 AMDA's own dev-run numbers — the single most directly relevant data point, with important caveats

From `research/benchmark_run_2026-07-07.md` and `research/VERDICTS.md`
(V13/V14/V15, already in this repo — not re-derived here, cited for this
research question's purposes): a full 228-task dev run using the actual
baked Qwen3-4B-Instruct-2507 Q4_K_M model plus a Cerebras `gemma-4-31b`
stand-in for remote escalation.

- Routing: 121/228 tasks (53%) never left the machine (local, local+
  consistent, local+program routes combined); 105/228 (46%) escalated; 2
  hit last-resort fallback.
- Within the **local-only-routed** subset specifically: local route 14
  pass/5 fail/29 unsure (48 total); local+consistent 40 pass/20 fail/8
  unsure (68); local+program 5 pass/0 fail/0 unsure (5). Combined: 59 pass /
  25 fail / 37 unsure across 121 tasks = **49% strict pass rate among tasks
  the router judged safe to keep local**.
- **Critical caveat, stated plainly**: this 49% figure is *not* the accuracy
  a forced zero-escalation run would get. It is the accuracy on the
  self-selected subset of tasks that already passed local verification —
  by construction, the harder 46% that failed verification and escalated
  are excluded. A true zero-escalation run would still need to answer those
  105 harder tasks locally (verification would still run, but there would
  be no remote fallback to catch the disagreements) — and those are
  disproportionately the categories flagged as weak below. **No clean
  "local-only accuracy across all 228 tasks with escalation forcibly
  disabled" measurement exists in the research corpus** — this would be a
  useful follow-up experiment (rerun `eval/run_local.py` with
  `ALLOWED_MODELS` empty or remote disabled) but was out of scope for this
  research-only pass.
- Per-category strict pass rates in that same (mixed local+remote) run,
  after the sentiment/NER/code-extraction bug fixes landed
  (`research/VERDICTS.md` V11/V14): logical_reasoning was the clear worst
  category pre-solver-fix at **24% strict (9 pass/23 fail/5 unsure)** — both
  the local model and the remote Cerebras gemma-4-31b stand-in failed these
  hard. mathematical_reasoning: 44% (16/20/0). sentiment_classification
  jumped to 96% pass (23/1) once the extraction-order bug was fixed — the
  true rate had been masked by a judge/verifier bug, not genuine model
  weakness. factual_knowledge: 61% strict (17/1/10) — note the large
  "unsure" bucket (10), which given the DIY judge's own limits (discussed
  next) likely undercounts genuinely-correct-but-hard-to-grade answers.
- The logic CSP solver (V15) and the widened program-check audit (V16) were
  implemented and unit/live-tested *after* this 228-task run — per
  `VERDICTS.md`'s own priority-action checklist, item 14, "full 228-task
  benchmark re-run with V15+V16 in place" is still **unchecked/pending** in
  this repo as of the last commit touching that file. **The most
  category-accurate, most current local-only numbers this repo has do not
  yet reflect the solver fix that specifically targets the weakest
  category** — a rerun would materially change (very likely improve) the
  logical_reasoning figure above, but by how much is not yet measured.
- This dev judge (`eval/judge.py`) is explicitly **not** the real AMD
  LLM-judge — it's a deterministic heuristic sanity check the AMDA team
  built for local iteration. Treat every percentage in this subsection as a
  lower-bound/directional signal, not a prediction of what the real
  grader will say.

### 2.5 A reframe worth flagging: AMD's own category definitions, read closely

Reading the Participant Guide's category table closely (not previously
dissected this way in the existing research corpus) surfaces two points
directly relevant to the accuracy-ceiling question:

- **"Factual knowledge" is defined as "Explaining concepts, definitions, and
  how things work"** — not "answer this trivia question." This is an
  open-ended, expository generation task graded by an LLM-judge on
  intent-match, not a closed-form recall lookup. MMLU/GPQA (multiple-choice,
  cited above) may therefore *overstate* the difficulty gap versus what the
  real task actually demands: a 4B instruct model explaining, say, "how
  photosynthesis works" in its own words is a much easier bar than
  correctly picking one of four GPQA answer options on a graduate-level
  science question. This cuts toward optimism for this category, with the
  usual caveat that we don't know how hard AMD's actual factual prompts get.
- **"Logical / deductive reasoning" is explicitly defined as "Constraint-based
  puzzles where all conditions must be satisfied"** — i.e., AMD's own
  category framing is CSP-shaped by definition, not open-ended search or
  optimization. This is directly favorable evidence for the scope decision
  already made in `research/VERDICTS.md` V15 (the CSP solver is deliberately
  scoped to finite-domain assignment/ordering puzzles and explicitly *skips*
  optimization-style puzzles like river-crossing, escalating those instead).
  If AMD's actual hidden eval set matches its own category description, the
  fraction of logic tasks structurally outside the solver's coverage may be
  smaller than the "seating, zebra/Einstein, knights-and-knaves,
  river-crossing" mix used to build AMDA's dev set (per
  `research/logic_escalation_economics.md`'s framing of that mix) would
  suggest — river-crossing puzzles are optimization/search-shaped, not
  pure CSP, and may simply be over-represented in the dev set relative to
  what AMD's own rubric implies it's testing. This is a hypothesis, not a
  confirmed fact — the guide gives a one-line category description, not a
  task-type manifest.

---

## 3. Tie-breaking at equal (especially zero) token counts

Searched the Participant Guide (read in full, directly — no tie-break section
exists anywhere in its ~8 pages), the AMD official forum thread (fetched
directly, no tie-break content), and multiple WebSearch queries combining
"AMD Developer Hackathon," "tie-break," "leaderboard," "token count," "equal
rank" — no result surfaced a documented tie-breaking rule (submission
timestamp, margin above threshold, or anything else).

**This is genuinely undocumented — stated plainly, not speculated about.**
One contextual observation, not a finding about tie-breaking itself: given
§1.3's live-leaderboard evidence that zero submissions currently pass the
accuracy gate at all, the question of how ties are broken *among gate-passing
zero-token submissions* is, at the moment, entirely theoretical — there is
no evidence yet that multiple teams have even reached the point where a
tie-break would matter.

---

## 4. Verdict

### 4.1 Is a true zero-escalation run realistic as a primary target?

**The honest answer is: this cannot be determined from public information
alone, and betting the whole submission on it is a higher-risk strategy than
it might first appear, for a reason that has nothing to do with model
capability — the pass bar itself is unknown and unverifiable except by
spending a real submission (rate-limited to 10/hour).** That said, the
evidence assembled here is not neutral; it leans toward "escalation should
remain available, tuned to specific categories" rather than "eliminate it
outright," for reasons that are separable into a capability argument and a
risk argument:

**Capability argument** — AMDA's existing verifier arsenal (program-aided
math re-derivation, CSP-solved logic puzzles, grammar-constrained sentiment/
NER re-reads, parser-oracle code extraction) already pushes several
categories close to what looks like a local ceiling:

- sentiment_classification and named_entity_recognition are structurally
  well-suited to zero-escalation: sentiment already measured at 96% strict
  locally-plus-mixed after the V14 fix, NER has a JSON-grammar guarantee of
  well-formed output (removing one whole failure mode for free).
- code_generation/code_debugging: the 0% dev-judge scores in the raw
  228-task run were confirmed to be a judge-methodology artifact (V11), not
  a real capability gap — the real ceiling is unmeasured but the underlying
  model benchmarks (LiveCodeBench v6 35.1, MultiPL-E 76.8 for Qwen3-4B-
  Instruct-2507) suggest real, non-trivial-but-not-strong local coding
  ability, auditable deterministically via `ast.parse`/execution.
- mathematical_reasoning has a working, 5/5-agreement-in-testing
  program-aided check for single-expression arithmetic word problems — the
  category AMD's own guide describes ("multi-step arithmetic, percentages,
  word problems, projections") is a good match for what that check can
  verify.
- logical_reasoning, read against AMD's own "constraint-based puzzles"
  framing (§2.5), may be more solver-coverable than AMDA's own dev-set mix
  implied — but this was the single worst-measured category (24% strict
  pre-solver-fix) and the solver's live-tested override behavior, while
  promising (4/4 unique-solution matches on dev puzzles per VERDICTS V15),
  has not yet been measured across a full re-run.
- factual_knowledge is the one category where no verifier can help: a 4B
  model either knows a fact/concept well enough to explain it or it doesn't,
  and this is a genuine knowledge-breadth ceiling, not a verification
  problem. §2.5's reframe (open-ended explanation, not trivia recall) is
  the best mitigating consideration found, but is a hypothesis about task
  difficulty, not a measured result.

**Risk argument** — the accuracy threshold is undocumented, and §1.3's
freshest evidence (two confirmed ZERO_API_CALLS submissions that *still*
failed the accuracy gate) proves that going fully local does not
automatically clear whatever bar exists. Given zero Track 1 submissions have
passed the gate at all as of this research pass — local, hybrid, or
otherwise — the current bottleneck for *everyone* in this competition is
answer quality/format, not token-routing policy. That is double-edged: it
means a well-verified local-only strategy isn't obviously worse-positioned
than a hybrid one right now (nobody's remote calls are buying a pass either),
but it also means there is no positive proof anywhere that a fully local
strategy *can* pass, either.

### 4.2 Minimum viable escalation rate — an explicit, low-confidence estimate

If forced to give a number: **roughly 10-30% of tasks likely need escalation
to reliably clear an unknown-but-plausible accuracy bar, LOW CONFIDENCE**,
concentrated in:

1. **logical_reasoning** — specifically the sub-shapes outside the CSP
   solver's finite-domain assignment/ordering coverage (optimization/search
   puzzles, if present in AMD's hidden set despite §2.5's more favorable
   reading of AMD's own category description), and CSP puzzles where the
   4B model's clue-to-constraint *translation* itself is unreliable (the
   solver's uniqueness guardrail catches wrong answers but returns "skip" —
   not "correct" — on mistranslation, per VERDICTS V15's own description of
   its "skip" branch).
2. **mathematical_reasoning**, the tail beyond single-closed-form-expression
   word problems (multi-part problems, problems requiring real-world
   judgment/estimation rather than pure arithmetic) that the existing
   program-check cannot verify.
3. **factual_knowledge**, the genuine-knowledge-gap tail — concepts or
   domains a 4B model's pretraining corpus under-covers, which no local
   verification strategy can detect or fix (a wrong-but-confident
   explanation is exactly the failure mode with no local signal to catch
   it).

This range is built from: (a) AMDA's own pre-solver dev numbers (24% strict
locally on logical_reasoning, the single worst-measured category in the
whole corpus); (b) the structural coverage boundary of the CSP solver, which
by design does not attempt every logic sub-shape; (c) the general literature
finding (already collected in `research/logic_escalation_economics.md` §1.6,
the "Inverse Scaling in Test-Time Compute" paper) that "deduction tasks with
constraint tracking" are a category where model behavior is unusually
fragile and hard to predict even for frontier models, not just small local
ones; and (d) the complete absence of any information about the actual
difficulty distribution of AMD's hidden eval set, which could move this
number substantially in either direction. This is exactly the kind of
estimate the task brief warned against stating with false precision — treat
the 10-30% figure as a directional planning input, not a target to hit
exactly.

### 4.3 Concrete recommendation

1. **Do not lock into a zero-escalation-only submission as the primary bet.**
   The threshold is undocumented and unverifiable except by spending a real
   submission slot (10/hour rate limit) — that is a real cost, but a much
   smaller one than losing the accuracy gate entirely on a submission that
   had no fallback.
2. **Use the 8 official practice tasks already in this repo**
   (`test_io/practice_tasks.json`, per VERDICTS V20) to get the one
   empirical signal actually available: run the current stack local-only
   (escalation disabled) against them and see how it grades under
   `eval/judge.py`. This is the only available proxy for "would a
   zero-token run plausibly clear the real gate" that doesn't cost a
   submission.
3. **Keep escalation available, but treat it as a targeted safety valve for
   the three flagged categories** (logical_reasoning's solver-uncovered
   shapes, mathematical_reasoning's tail, factual_knowledge's genuine
   knowledge gaps) rather than a general-purpose fallback — the existing
   verify-then-escalate architecture already does this; the open item is
   re-running the full 228-task dev set with V15 (logic solver) and V16
   (remote-answer audit) in place, per VERDICTS.md's own pending checklist
   item 14, to get a current, solver-informed number for exactly how much
   escalation the current local model actually still needs.
4. **If practice-task testing shows local-only clears whatever threshold
   exists, a zero-escalation submission becomes a legitimate high-value
   bet** — rank 0 is unbeatable by construction, and §1.3's evidence that
   nobody (local or hybrid) is passing the gate right now means there is no
   evidence a hybrid approach has any accuracy advantage over a well-verified
   local-only one at this moment. But this is conditional on evidence this
   research pass could not obtain (the real threshold, the real judge's
   behavior on open-ended explanatory/summarization answers) — it is a
   decision to make after practice-task testing, not before it.

---

## Sources (all URLs fetched or searched this session)

Directly fetched (PDF read or WebFetch full-page pass):
- `Participant Guide_ AMD Developer Hackathon (ACT II).pdf` (repo root, read directly, all 8 pages)
- https://devcommunity.amd.com/t/amd-developer-hackathon-act-ii/596
- https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live (two passes)
- https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507
- https://huggingface.co/Qwen/Qwen3-1.7B
- https://arxiv.org/html/2505.09388v1 (Qwen3 Technical Report, HTML full text)
- https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
- https://huggingface.co/microsoft/Phi-4-mini-instruct
- https://arxiv.org/pdf/2601.14277 ("Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct" — read as PDF, pages 4-10, Table 2 transcribed directly)
- https://arxiv.org/html/2508.16499v1 ("How Small is Enough? Empirical Evidence of Quantized Small Language Models for Automated Program Repair")
- `research/logic_escalation_economics.md`, `research/VERDICTS.md`, `research/hackathon_meta_amd_ecosystem.md`, `research/competitors_lablab.md`, `research/models_fireworks.md`, `research/benchmark_run_2026-07-07.md` (existing repo research, read for context/cross-reference, not re-fetched from source)
- `agent/router.py` (read directly to accurately describe the current verifier arsenal)

WebSearch queries (result links reviewed, not all individually re-fetched):
- "AMD Developer Hackathon" "Act II" accuracy threshold Discord announcement Track 1
- AMD Developer Hackathon Act II Track 1 leaderboard July 2026
- Llama-3.2-3B-Instruct benchmark MMLU GSM8K HumanEval IFEval model card
- Phi-4-mini-instruct benchmark MMLU GSM8K HumanEval IFEval GPQA
- Qwen3-4B-Instruct-2507 GSM8K HumanEval MBPP benchmark score
- small language model 3B 4B ZebraLogic knights and knaves accuracy quantized Q4
- Qwen3 technical report GSM8K accuracy small model 1.7B 4B table
- Q4_K_M quantization accuracy loss GSM8K MMLU benchmark degradation percentage points
- "amd developer hackathon" tie-break token count leaderboard rank equal
- lablab.ai discord AMD hackathon accuracy gate percentage clarify
- small LLM 3B 4B NER named entity recognition benchmark accuracy few-shot
- small language model summarization benchmark 3B 4B ROUGE factuality
- code debugging benchmark small language model DebugBench 3B 4B accuracy

Not fetched / out of scope for this pass (noted as follow-ups, not done):
- Full text of "Evaluating Small Language Models for News Summarization" (arXiv 2502.00641) for per-model ROUGE/factuality numbers
- DebugBench (arXiv 2401.04621) per-model-size breakdown table
- A forced zero-escalation rerun of `eval/run_local.py` against the 228-task dev set (would directly answer §2.4's flagged gap — this is a code/experiment task, out of scope for a research-only pass)
