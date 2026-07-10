# VERDICTS — analysis of the 7-file research corpus (2026-07-07)

Decisions for AMDA Track 1, each grounded in the collected evidence
(see research/*.md for sources). Ordered by scoring impact.

---

## V1. Escalation model policy: Gemma-first, Kimi last, MiniMax conditional

**Decision:** default escalation order for ALL categories becomes
`gemma-4-31b-it → gemma-4-31b-it-nvfp4 → gemma-4-26b-a4b-it → minimax-m3 → kimi-k2p7-code`.
The code-specialist-first policy (kimi first for code) is **reversed**.

Evidence:
- kimi-k2p7-code: thinking is architecturally **mandatory** — "Kimi-K2.7-Code
  forces thinking and preserve_thinking as True" (HF model card, verbatim).
  Every call bills unavoidable reasoning tokens as output. HN practitioners:
  "you'll spend many more tokens" vs alternatives. On a leaderboard ranked by
  ascending tokens, this is disqualifying as a first choice.
- gemma-4-31b-it: thinking **off by default** ("Thinking mode is not enabled
  by default", HF card) — enabled only via `<|think|>` token. Strong scores
  (MMLU 85.2, AIME'26 89.2, LiveCodeBench v6 80.0) and the only quantitative
  verbosity datapoint favors it: "rarely generates more than 20k tokens" vs
  Qwen3.5's 100k+ (Kaitchup). Code score (LCB 80.0) beats any verified number
  for kimi, whose public-suite results are vendor-only.
- **Side prize**: Track 1 carries "Best Use of Gemma via Fireworks — $1,000"
  (event page, verbatim). Gemma-primary makes us eligible at zero cost.
- minimax-m3: Fireworks confirms "toggling thinking on or off at request
  time"; a real integration found the API accepts `"thinking": {"type":
  "disabled"}` (rejects "enabled", accepts "adaptive"/"disabled" — kilocode
  issue). BUT reasoning has been observed inline in normal output, and M3
  measured 64% more tokens than a peer on identical tasks (thinkwright).
  → conditional: test `thinking: disabled` through the proxy on key day-1;
  promote above 26b-a4b only if reasoning demonstrably absent.
- gemma-4-31b-it-nvfp4: quality ≈ base (0.25% GPQA loss; "no meaningful
  accuracy difference" — Kaitchup), and "quantization has little impact on
  token efficiency." Faster infra → use as latency fallback (see V2).

## V2. The 30s/request rule is a live risk on Fireworks — keep timeout + fast fallback

Telnyx benchmark: Fireworks minimax-m3 p95 latency **54.06s, max 111.51s** —
far over the 30s/request cap. Our 25s client timeout is correct; add: on
timeout, retry once against the nvfp4 variant (faster) with a hard cap,
else fall back to the local answer. Never let one slow call sink a task.

## V3. Token micro-economics on remote calls

Proxy records **total tokens** — input and output both cost rank.
- Remote system prompt: single short line, or none. Never send local
  PROMPT_HINTS verbatim to remote; send the raw task + one format line max.
- Per-category `max_tokens` caps on remote calls (sentiment ~48, NER ~256,
  factual ~160, summary ~256, logic ~192, math ~320, code ~640).
- Append "Answer directly. Do not show reasoning." to remote prompts —
  Gemma-4's verbosity is prior-driven and this measurably reduces narration
  (openllmbridge: "it has no instruction by default, so it falls back to its
  training prior, which is verbose").
- Verify remote answers with the same verifiers; at most ONE retry.

## V4. Judge-gate posture: local answers polished, remote answers lean

LLM judges "prefer longer, authoritative-looking, and well-formatted
responses" (2411.16594) — and **local tokens are free**. So: local answers
should be complete, clean, well-formatted sentences (costless judge appeal);
remote answers concise but complete (they're metered). Never ship
"Unable to answer." when any local draft exists — a guaranteed judge fail
beats nothing, but a mediocre local answer beats both. Do not attempt
judge-gaming (master-key phrases) — high risk, likely countered.

## V5. Constrained decoding: use for classification/extraction, never for reasoning

- llama.cpp ships GBNF (`grammars/json.gbnf`, `-j` schema conversion);
  llama-server accepts grammars per request. Grammar-constrain LOCAL
  sentiment (label-choice grammar) and NER (JSON-schema grammar) —
  practitioner data: 100% well-formed output, ~25% accuracy gain, "guardrails
  in bowling" (imaurer.com).
- Do NOT constrain math/logic/code/summarisation: "significant decline in
  LLMs reasoning abilities under format restrictions"; GSM8K-style tasks show
  10-30% degradation (Let Me Speak Freely, 2408.02442; JSONSchemaBench).
- Two-pass pattern where format matters after reasoning ("Thinking Before
  Constraining"): free-form reason → constrained extract. Local passes cost
  only time, and we have time budget per task on GPU-class judging VMs.

## V6. Math verification upgrade — program-aided checking (biggest accuracy lever)

Local math is our worst verified category (17% strict on laptop bench).
Adopt the eval-framework standard: **math-verify** (HF; sympy+ANTLR4;
`parse()`/`verify()`) — the same library lighteval AND lm-evaluation-harness
use for math scoring.
- In eval/judge.py: replace regex-number matching with math-verify.
- In agent/verifiers.py: program-aided self-check — after the local model
  answers, ask it (locally, free) to emit the computation as a bare Python
  expression; execute; compare to its stated answer with math-verify
  tolerance. Agree → trust local; disagree → escalate. Deterministic, free.
- Keep 2-sample self-consistency for logic/factual only; evidence says
  returns diminish on capable models ("Self-Consistency Is Losing Its Edge")
  so never exceed 2 samples.

## V7. Cascade literature confirms the architecture; quality-estimation is the whole game

"Good quality estimators" are THE critical factor (cascade-routing, ETH) and
naive cascades fail through "poor estimation of the quality of the affordable
LLM's outputs" (BARGAIN). Our deterministic verifiers ARE the quality
estimator — every verifier improvement converts directly to rank. No
framework adoption needed (RouteLLM etc. solve preference-routing, not
verify-then-escalate); our bespoke design is the right shape. Steal ideas,
not dependencies.

## V8. Dev stand-ins before the Fireworks key (test escalation TODAY)

Name-matching free hosts found for our exact locked targets:
- **Cerebras free tier hosts `gemma-4-31b`** (5 RPM, 1M tokens/day, no card)
  — closest stand-in for our PRIMARY escalation model.
- **Cloudflare Workers AI hosts `@cf/google/gemma-4-26b-a4b-it`** (10K
  neurons/day free).
- HF Inference Providers router (`https://router.huggingface.co/v1`, OpenAI-
  compatible) reaches gemma-4-31b-it / Kimi-K2.7-Code / MiniMax-M3 via
  Novita/Together/DeepInfra — pay-per-token, ~$0.10 free credit (tiny).
- Google AI Studio free tier (Gemini Flash ~1.5k req/day) — use as the
  dev **LLM judge** for the 228-task set's "unsure" bucket, not as a stand-in.
Config needs zero code changes: point FIREWORKS_BASE_URL / ALLOWED_MODELS /
FIREWORKS_API_KEY at the stand-in in `.env`. User action: create Cerebras
(and optionally Cloudflare) account.

## V9. Local model matrix (for the next GPU window) — revised candidates

Benchmark in this order, one model per session, judged by eval/judge.py:
1. Qwen3-4B-Instruct-2507 Q4_K_M (baseline; IFEval 83.4 = best format-follower)
2. Phi-4-mini-instruct Q4 (GSM8K 88.6 / HumanEval 74.4 — targets our two
   weakest categories)
3. Granite 4.1 8B instruct Q4 (HumanEval 87.2 / GSM8K 92.49, if GGUF exists)
4. Qwen3.5-4B (thinking off) — newer family, toggleable
Two-model bake (4B generalist + math/code specialist, both fit in 10GB) is
on the table if category-routed local wins the numbers.
Also: use `-ngl 99` on GPU box; CPU worst case threads = physical cores.

## V10. Competitive posture: submit early, iterate on the leaderboard

At the Jul-7 snapshot the entire Track 1 had **5 submissions** out of 4,327
teams. Rate limit is 10/hour. The leaderboard is a feedback oracle — first
submission should go up the moment the key arrives and the remote path is
smoke-tested, then iterate. No verified competitor is doing verify-local-
first (two name-alikes unverified/404). No Act-I precedent exists — nobody
has meta-game experience on this track type.

## V11. Code extraction: parser-oracle, not prose patterns (IMPLEMENTED 2026-07-08)

The `_extract_code` prose-prefix bug (research/benchmark_run_2026-07-07.md
Bug #3) was fixed by adopting EvalPlus's approach: a **longest-valid-segment
search** where `ast.parse` is the oracle — iterate line ranges, keep the
longest contiguous segment that parses as substantive Python. No prose
regexes, no fence parsing, no language lists: prose, fence markers, and
language tags exclude themselves by failing to parse. (Source:
github.com/evalplus/evalplus `sanitize.py` `code_extract()` — "the longest
valid Python code by non-empty line count"; corroborated by the two-stage
fence-then-recovery convention in code-eval literature, arXiv 2403.17214.)
One guard added on top: a winning segment must define something
(def/class/import) or span ≥3 non-empty lines, because stray single lines of
JavaScript (`max = arr[i];`) parse as Python. A fence explicitly tagged
`python` whose content never parses still fails (declared-broken code).
Installed in BOTH agent/verifiers.py (runtime) and eval/judge.py (kept as an
independent copy — the measuring instrument must not import agent bugs).
Measured on the same 228-task results: code-category fails 14 → 2 (12 were
judge artifacts), judge ceiling 65% → 71%, local+consistent route fails
20 → 10. Runtime effect: prose-prefixed local code answers no longer
false-fail into paid escalations.

## V12. Classifier: intent-first tie-breaks + generic markers (IMPLEMENTED 2026-07-08)

Bug #4 fix, two changes to agent/classify.py, both category-generic:
(1) rule order now puts explicit-intent categories (sentiment, NER,
summarisation) before incidental-vocabulary ones (code, math, logic) —
`max()` keeps the first maximum, so ties break toward intent ("a tweet about
buggy software is still a sentiment task"); (2) keyword coverage extended
with canonical task-phrasing markers: "clue"/"sitting"/"does it follow"
(logic puzzles), "average speed"/" km"/"fraction"/"per hour" (rate-and-work
word problems), "extract"/"organization" (NER), "a function"/"javascript"
(code), plus `function name(` / `=>` in the code-block regex. Deliberately
NOT added: bare "speed" or "how long" — they'd steal factual questions like
"what is the speed of light". Measured: 87.3% → **96.5%** (220/228), math
misroutes eliminated (36/36 — the costliest class: a math→factual misroute
lost the ANSWER hint, the program check, and half the token cap). No
category regressed. The 8 residual misses are factual↔summarisation-class
confusions with ~zero runtime cost (identical verify() behavior).

## V13. First full-run economics: 66 scored tokens/task; logic is the accuracy hole

Full 228-task run (local + Cerebras gemma-4-31b stand-in, 2026-07-07): 46%
of tasks never left the machine; 105 remote calls spent 15,131 tokens total
= **66 scored tokens/task average** — the leaderboard number to beat.
Program-aided math check went 5/5 against the deterministic judge. Verified
accuracy holes after removing judge artifacts: logical_reasoning (9 pass /
23 fail — BOTH local and the gemma stand-in fail hard constraint puzzles)
and mathematical_reasoning (16 pass / 20 fail). Next research scope:
(a) whether logic escalation should route to a thinking-enabled model
despite token cost — the accuracy gate precedes token ranking, so failed
logic tasks may cost more than thinking tokens do; (b) widening the
program-check's firing conditions (currently needs verdict=unknown + number
present + time headroom; it could also audit remote math answers for free);
(c) sentiment's 8 residual fails (label-agreement active — check whether
gold "mixed" cases are genuinely ambiguous).

## V14. Sentiment "mixed" fails were a judge/verifier extraction bug, not
## ambiguous gold (IMPLEMENTED 2026-07-08)

Investigated per user request: "check whether gold-mixed cases are
genuinely ambiguous before engineering anything." They were not. Root
cause: `SENTIMENT_LABELS = ("positive", "negative", "neutral", "mixed")` —
the fallback extraction scanned this tuple in **fixed order**, not by where
the label actually occurs in the text. A "mixed" verdict is almost always
justified with prose containing both "positive" and "negative" ("...positive
aspects...negative aspects..."), so the scan found "positive" first and
returned it — even when "Mixed" was the literal first word of the answer.
Compounding it: gold-answer extraction never even tried the anchored
`label:\s*X` regex the answer side already had; gold always went straight to
the broken fallback. Same bug independently present in `agent/router.py`'s
`_sentiment_label_agrees` (the runtime label-agreement check), so it was
also causing live false-fail escalations, not just a dev-judge miscount.
Fix: `_sentiment_label()` (both files) now tries an anchored
`(?:label|sentiment|overall)\s*[:=]?\s*X` regex first, and falls back to
whichever label word occurs **earliest in the text** — not tuple-priority
order. Measured on the same 228-task results: sentiment pass 16 → **23**,
fail 8 → **1** — true accuracy was 96%, not 67%. Overall strict score
39% → **43%**, ceiling 65% → **74%**. The one real residual
(`chatgpt_sentiment_classification_hard_1`) is a genuine nuanced
double-negative case ("don't hate" → model hedged "neutral to slightly
positive" vs gold "positive") — not worth engineering around.

This is the third extraction-order bug found in one session (classify.py's
"ner", the code prose-prefix, now this) — same root shape every time: code
that decides among fixed categories by checking a **hardcoded priority
order** or **unanchored substring**, rather than by what the text actually
says or where. Worth a standing rule for future verifier/judge code: prefer
an anchored "the label IS X" pattern first, and if scanning for bare
keywords, rank by position-in-text, never by an arbitrary tuple order.

---

# Round-2 verdicts (2026-07-08) — analysis of the 8-file second research
# corpus: logic_escalation_economics, logic_solver_tooling,
# program_aided_verification_patterns, rust_math_tooling, go_graph_tooling,
# opensource_quality_tools_round2, cpp_mojo_zig_potential,
# academic_literature_survey

## V15. Logic: solve with a constraint solver, do NOT escalate to thinking mode

**Decision:** the logical_reasoning fix is a program-aided **solver check**
(mirror of the V6 math check): local model translates the puzzle's clues
into constraints, a deterministic CSP solver solves them, and the solver's
verdict gates (and can supply) the answer. Thinking-mode escalation is
rejected as the primary lever.

Against thinking-mode escalation (research/logic_escalation_economics.md):
- ZebraLogic's own abstract: accuracy decline with complexity "persists even
  with larger models and increased inference-time computation."
- "Inverse Scaling in Test-Time Compute" (2507.14417) names "deduction tasks
  with constraint tracking" — exactly our puzzle class — as a category where
  LONGER reasoning makes accuracy WORSE across frontier families.
- "Do Thinking Tokens Help or Trap?" (2506.23840): "Incorrect responses
  contain twice as many thinking tokens as correct ones."
- BBEH Table 2 (single-fetch, cell-level UNVERIFIED): DeepSeek R1 scored
  8.0% on Zebra Puzzles vs non-reasoning Gemma2-27B's 23.0% — reasoning
  advantage is task-dependent, not uniform.
- No public logic-puzzle numbers exist at all for gemma-4-31b or minimax-m3
  (thinking on OR off) — escalating to them on thinking for logic would be
  flying blind at 3-30x token multipliers (blog-range, no consensus).

For the solver path (logic_solver_tooling.md + go_graph_tooling.md,
independently convergent):
- **Logic.py: 24.9% → 91.4% on ZebraLogicBench** (Llama-3.1-70B alone vs
  LLM-formalizes-solver-solves; arXiv 2502.15776, directly fetched).
- Logic-LM (EMNLP 2023): +39.2% over standard prompting across five logic
  datasets including LogicalDeduction (our seating/ordering class); includes
  self-refinement on solver error messages.
- SatLM (NeurIPS 2023): declarative-spec-then-solve beats program-aided
  imperative code precisely on "constraint solving problems that require
  more sophisticated planning and search"; "the declarative specification
  is closer to the problem description than the reasoning steps are, so the
  LLM can parse it out of the description more accurately" — i.e.
  translation is extraction-shaped, which per V5 is exactly what our
  grammar-constrained decoding is FOR.
- Tooling verified on PyPI: **python-constraint2** (2-4MB, BSD, active,
  `from constraint import *`, string constraints auto-parsed) and
  **z3-solver** (13-47MB wheel, MIT, self-contained; working zebra +
  knights-and-knaves code captured verbatim in the research file).
  OR-Tools (~30MB + numpy/pandas deps) is third choice.

**Implementation shape** (next build item): `_logic_solver_check` in the
router — classify logic sub-shape (assignment/ordering = finite-domain CSP;
skip optimization puzzles like bridge-crossing, which fall through to
escalation as today); ask the local model (free) to emit variables/domains/
constraints in python-constraint's simple string form; `getSolutions()`;
if exactly one solution and it matches the local answer → pass; if exactly
one solution and it contradicts the local answer → ship the solver-derived
assignment (formatted in prose); zero or multiple solutions → translation
failed, escalate as today. Start with python-constraint2 (simplest emission
target for a 4B model — fewer translation errors); move to Z3 only if
expressiveness runs out.

## V16. Widen program-aided checking to audit REMOTE answers (CRITIC pattern)

**Decision:** run the existing `_math_program_check` (and V15's solver
check, once built) against remote answers too — a free local audit of a
paid answer, deciding between remote answer, second remote model, or
solver-derived value.

Evidence (program_aided_verification_patterns.md):
- CRITIC (ICLR 2024, PDF read directly): verify-then-correct on an
  *already-produced* answer via code interpreter is a published, named
  pattern (+2 to +16 points across GSM8k/SVAMP/TabMWP).
- CRITIC's ablation is the sharp edge: **ungrounded self-critique made
  results worse than no verification at all** (text-davinci-003: 70.1 →
  68.3 "w/o Tool") — "Without execution feedback from the interpreter, the
  ability of LLMs to correct programs becomes limited and unstable." Never
  add an LLM-critiques-LLM step without execution grounding.
- Known literature gap (explicitly searched, not found): no study measures
  how often an independent translation-to-code shares the SAME
  misunderstanding as the answer it checks. Consequence for us: treat
  program-agreement as a positive signal, never as an override that
  silently replaces a disagreeing answer without a fallback path.
- Notable for the submission writeup: lm-evaluation-harness and lighteval
  only execute symbolic *equivalence grading against a known gold*
  (math-verify); neither re-derives answers from the problem text. AMDA's
  from-scratch re-derivation check is genuinely ahead of the reference
  eval frameworks here.

## V17. Add a free logprob confidence signal for the "unknown" categories

**Decision:** request `n_probs`/logprobs on local completions and use
mean/min token logprob as a third routing signal for factual_knowledge and
logical_reasoning (the categories where verify() returns "unknown" and we
currently lean only on 2-sample self-consistency).

Evidence:
- llama-server `/completion` exposes per-token `logprob` via `n_probs` —
  directly confirmed from tools/server/README.md; zero new dependencies
  (opensource_quality_tools_round2.md §5.1). `llama-perplexity` confirmed
  NOT usable for single answers.
- Academic backing (academic_literature_survey.md): Semantic Entropy Probes
  (2406.15927) — cheap single-pass uncertainty from hidden states; CISC
  (2502.06233) — confidence-weighted self-consistency cuts sampled paths
  >40%, "LLMs can effectively judge the correctness of their own outputs";
  LLM Performance Predictors (2601.07006) — escalation meta-models built
  exactly from logprob/entropy features.
- Calibrate thresholds on the dev set only; a logprob gate that saves one
  remote call per few tasks is pure rank profit, but an overfit threshold
  that ships wrong local answers costs the accuracy gate. Conservative
  rollout: use LOW confidence only to short-circuit self-consistency and
  escalate faster (saves local time, never ships more risk).
- Deferred, noted: HHEM-2.1-Open (~100M, Apache-2.0) / TinyLettuce (17M)
  are real premise-vs-hypothesis groundedness checkers usable for
  summarisation verification (context = source passage), but add a
  transformers dependency + weights to the image for a category currently
  at 63% strict. Revisit only if the leaderboard shows summarisation
  failing.

## V18. Languages (Rust/Go/C++/Mojo/Zig): no adoptions — evidence-closed

Per-language, from the four collect-files (all honest-negative where
negative):
- **Rust:** `py-evalexpr` (~0.5MB manylinux+musllinux wheels, pip-only,
  wraps evalexpr) is real and would harden the math sandbox by
  construction — but evalexpr's own README says "not built with untrusted
  input in mind"; our `_EXPR_OK` whitelist + subprocess + timeout already
  constrains the same surface. Optional hardening, not adopted. No viable
  Rust CAS (symbolica is source-available/non-standard license —
  disqualifying), no derivation-path tooling ("nothing notable found" —
  the one match is a 39-star hobby project).
- **Go:** explicit negative finding — no Go knights-and-knaves or seating
  solvers exist; Go's one CSP library (centipede, 76 stars) is 4 years
  stale and self-described "work in progress." Every published LLM+solver
  logic result uses Python-reachable solvers. Go graph tooling closed.
- **C++ (llama-cpp-python):** prebuilt CPU wheel (22.1MB, directly
  measured) with the same GBNF dialect exists — but zero benchmark evidence
  it beats llama-server over loopback (the one primary source is a
  qualitative overhead discussion; a search-synthesis suggests the C++
  server WINS on TTFT for short single requests). Switching would risk a
  proven pipeline for an unproven gain. Closed.
- **Mojo:** MAX-full Docker image directly measured at **11.9GB
  compressed — over our entire 10GB cap by itself**; compiler
  closed-source until Fall 2026; Modular's own 1.0 scope is GPU-kernel
  authoring, not glue code. Closed.
- **Zig:** llama.cpp removed Zig build support in May 2024 (merged PR
  7471, maintainer: "I don't think the Zig build system adds much value").
  Dead avenue. Closed.

## V19. Academic framing: AMDA sits in the exact regime where cascades win

For the submission narrative (README/slides/video) and posture:
- **FrugalGPT (2305.05176)** is the seminal citation for our architecture:
  "match the performance of the best individual LLM (e.g. GPT-4) with up
  to 98% cost reduction" via LLM cascade.
- **"Is Escalation Worth It?" (2605.06350)** finds cascades are limited by
  "structural cost, since cascades pay the cheap model before any
  escalation decision" — and AMDA's cheap model costs ZERO scored tokens.
  The strongest published critique of cascades is structurally neutralized
  by this competition's scoring rules; that argument belongs in the
  submission description verbatim.
- **"Dynamic Model Routing and Cascading for Efficient LLM Inference: A
  Survey" (2603.04445)** is the field map — cite it once as the anchor.
- Judge posture (V4) reconfirmed and sharpened by the new bias literature:
  CALM's 12-bias taxonomy (2410.02736) and "Reliability without Validity"
  (2606.19544). Keep answers clean, complete, well-formatted; no gaming.
- xRouter (2510.08439) critiques "static escalation rules" like ours — the
  defense is V7's: our rules are deterministic quality estimators with
  zero-cost first stage, which learned routers exist to approximate.

---

## Priority actions (code)
1. [x] config.py: flip preferences to Gemma-first, kimi last (V1)
2. [x] router/remote: per-category remote max_tokens + "answer directly" +
       lean remote prompts (V3), remote-verify + single retry (V3), timeout
       fallback order (V2)
3. [x] verifiers.py + router.py + grammars.py: program-aided math check (V6),
       JSON grammar for NER, constrained label-agreement for sentiment (V5)
       — functionally tested against llama-server 2026-07-07, all paths pass
4. [x] eval/judge.py: math-verify integration (V6) — dev-venv only dependency
5. [x] .env stand-in test with Cerebras gemma-4-31b (V8) — full 228-task run
       2026-07-07, escalation path proven live (V13)
6. [x] parser-oracle code extraction in verifiers.py + judge.py (V11)
7. [x] classifier intent-first ordering + generic markers, 96.5% (V12)
8. [x] sentiment label extraction fixed in judge.py + router.py (V14) —
       true sentiment accuracy 96%, strict score 39%→43%, ceiling 65%→74%
9. [x] **logic solver check (V15)** — implemented 2026-07-08:
       python-constraint2 in requirements + image; verifiers.py gained
       parse_logic_translation (strict PEOPLE/POSITIONS/C: format,
       whitelist: declared-identifiers-only, no **/dots/brackets/quotes,
       empty __builtins__), solve_logic_csp (AllDifferent always, ≤7 vars
       ≤10 domain, 2-pull uniqueness test), assignment_matches_answer
       (clause-scoped nearest-number, ordinal-aware — window-based matching
       was proven wrong on dense listings and replaced), format_assignment.
       Live-tested against llama-server on real dev puzzles: 4/4 unique
       solutions matched gold exactly (incl. 3 overrides of wrong local
       answers — the base-rate failure case the solver exists to fix);
       1 mistranslation (ages puzzle, contradictory constraints) correctly
       yielded 'none' → skip, no wrong answer shipped. Uniqueness guardrail
       validated in the wild on its first encounter.
10. [x] program-check audit of remote math answers (V16) — implemented
        2026-07-08: _math_program_check is tri-state (None = couldn't
        check, never treated as disagreement); escalation loop holds a
        doubted-but-verified answer, gives the fallback model one shot,
        ships the held answer if the fallback also fails/doubts (never
        discards over our own doubt; both-doubted ties break to the
        higher-preference model). All branches proven live via Cerebras:
        audit disagreed with a wrong remote answer (363.30 vs computed
        360.91 — the audit's value matched gold), fallback call fired
        (calls 1→2), held answer shipped on exhaustion.
11. [x] logprob confidence plumbing (V17) — implemented 2026-07-08:
        `local_llm.complete_scored()` returns (answer, mean token logprob);
        OpenAI-style `logprobs=True` verified working on our llama-server
        b9888; router gate wired behind `config.LOGPROB_ESCALATE_BELOW`.
        **Gate DISABLED (None)**: 26-task calibration showed pass/fail
        mean-logprob distributions overlap (passes span -0.000..-0.118, a
        fail sits at -0.101 inside that range; only 2 fails observed) — no
        defensible threshold. Recalibrate after the local-model choice
        settles (threshold is model-specific); the plumbing costs nothing.
12. [ ] GPU window: model matrix per V9 — REFRAMED by V20: candidates are
        now 2-3B models, not 4B+
13. [x] language adoptions evaluated and closed — none adopted (V18)
14. [ ] full 228-task benchmark re-run with V15+V16 in place (route mix
        and logic strict-score are the numbers to watch)

---

## V20. Grading environment is 4 GB RAM / 2 vCPU — model size and threading
## are now first-order constraints (organizer announcement + guide v2, 2026-07-08)

Verified from the updated Participant Guide (downloaded, primary source):
- "Grading environment: 4 GB RAM, 2 vCPU. If bundling a local model, size it
  to fit within these limits (2B–3B 4-bit quantized models are safe; 7B
  4-bit fills the full RAM budget...)" — our baked Qwen3-4B Q4_K_M (~2.5GB
  weights + KV cache) sits in the untested middle; needs an empirical
  constrained-Docker test (--memory=4g --cpus=2) before trusting it.
- "flagged: ZERO_API_CALLS... is not a failure. It just means your
  submission made zero calls through the Fireworks proxy" — a fully-local
  run is OFFICIALLY safe. The theoretical ceiling is a zero-token
  accuracy-gate pass: unbeatable rank.
- New failure status OUTPUT_MISSING; full failure table now documented.
- 8 official practice tasks published (extracted to
  test_io/practice_tasks.json) — validate the container without burning a
  submission slot (10/hr limit).
- Live leaderboard (fetched 2026-07-08): **29 submissions, ZERO passing
  the accuracy gate** — 16 ACCURACY_GATE_FAILED, rest infra errors. The
  gate is the real filter; token rank is currently academic. Several
  competitors now explicitly run local-first cascades ("Frugal Router",
  "FireCascade", "Local First, Tokens Last").
- Fix landed: entrypoint threads are now cgroup-v2-aware (nproc reports
  HOST cores under a CPU quota — 12 threads would thrash a 2-vCPU cgroup);
  context reduced 4096→2048 to halve KV-cache memory.
- Consequence for V9: the GPU model matrix pivots from 4B+ candidates to
  2-3B (with the 4B kept only if the constrained-Docker test proves it
  fits both RAM and the 10-minute budget at 2 threads).

## V21. Code verifier only proved "doesn't crash as a script", not "logic is
## correct" — fixed with spec-derived assertions (2026-07-09)

Found by the `certificate_carrying_answers` research agent, independently
confirmed by direct code read + unit test before shipping. `verify()`'s code
branch (`agent/verifiers.py`) extracted the candidate function and ran it via
`_run_python`, which executes the block **as a standalone script**. Almost
every real candidate answer is a bare `def f(...): ...` with no call site —
running that as a script defines the function and exits 0 regardless of
whether the body is correct. Confirmed with the canonical bug
(`def get_max(nums): return nums[0]`, from `test_io/practice_tasks.json`
practice-06's own prompt): the old check returned `True` (pass) for it,
since indexing a non-empty list never raises. A pure "does it crash"
fuzz check (the research's other option, Hypothesis `fuzz()`) would have
missed this exact bug too, for the same reason, on most inputs — crash-only
checking can't see a wrong-but-non-crashing return value.

Fix: `verifiers.run_with_assertions` splices the candidate with a few
example-based `assert` statements and actually executes the call.
`router._code_assertion_check` generates those assertions from the local
model, shown **only the task's natural-language spec, never the candidate
code** (avoids the same misreading leaking into both the answer and its own
check — an open risk the CRITIC-pattern research flagged and had no prior
art ruling in or out, so kept as the cheap mitigation). Wired as a
post-verdict demotion in `router.solve()`, same shape as sentiment's second
constrained read: a `verify()` "pass" only gets demoted to "fail" on a real
assertion disagreement; no usable assertion parses out → `None` → today's
script-only pass stands, so this can only add rigor, never regress below
the current floor. Gated on `time_left > 90` like the other post-verdict
checks. Zero new dependencies (pure `ast`/`subprocess`, no Hypothesis).

Live-verified: old check passes the buggy `get_max`, new check fails it
(`assert get_max([3,1,4,1,5,9,2,6]) == 9`), correct code still passes,
no-usable-assertion case returns `None` not `False`.

**Caveat for the full-228 benchmark started before this fix landed**: that
run's code_generation/code_debugging numbers reflect the old, weaker
script-only check and are likely optimistic for those two categories only —
worth a targeted re-check, not necessarily a full re-run. (Superseded by the
finding below: `eval/judge.py`'s own `_judge_code` returns "unsure, semantics
unchecked" for all parseable code regardless of agent-side verification, so
the dev harness can't actually surface V21's effect numerically — a targeted
re-check wouldn't show a clear before/after signal. V21 stands on its unit
test, not on a benchmark delta.)

## V22. The 228-task benchmark surfaced a bigger, real bug: solver answers
## were graded wrong for label wording, not substance (2026-07-09)

The full run gave `logical_reasoning` a 57% strict score and the `solver`
route (V15's CSP override) only 5 pass / 6 fail / 2 unsure — worse than the
earlier small live tests suggested. Read the actual failing pairs before
accepting that number: **every one of the 8 non-pass "solver" tasks had the
exact correct person/item-to-position assignment** — the CSP solver's
substance was 100% right. The only difference from gold was label
vocabulary: `format_assignment` hardcoded `"Position N: Name"`, but gold
answers use whatever wording the puzzle itself established — day names
("Monday: Sarah"), ordinals ("1st: Drew"), or bare numbers ("1: Yellow").
"Position N" matched **zero** of the 8 gold answers verbatim.

This means V15's real solving accuracy on this dev set is far higher than
57% suggests — the measured number was mostly a formatting artifact, not a
reasoning failure. Given `logical_reasoning` was flagged as the project's
single weakest category as far back as V13, this was likely suppressing our
best-fixed category's real score the whole time.

Fix: `verifiers._position_labels(prompt, n)` detects the puzzle's own
labeling scheme directly from its text — day-of-week names (in the order
they appear, not calendar order), an ordinal pattern (`"1st"` present in the
prompt), or bare numbers as the fallback — and `format_assignment` now takes
`prompt` and uses whichever scheme the puzzle actually established, never a
scheme not evidenced in the prompt itself. Verified against the three real
failing prompts pulled from the benchmark: day-name, ordinal, and bare-number
outputs each now match their gold answer's format exactly (not just
approximately). `router._logic_solver_check` updated to pass `prompt`
through; the bare-number fallback preserves the exact old output for any
prompt where no scheme is detected, so this can only fix cases, never
regress existing passes.

**Round 2 (same day, caught by actually re-running the fix, not just unit
tests)**: a targeted 37-task logical_reasoning-only re-check on the GPU pod
showed the `solver` route still failing 4/13 and unsure 4/13 after V22
"landed" — i.e. the fix was live but the number barely moved. Manual
inspection of the fails found two vocabulary gaps the first pass's evidence
didn't cover: (1) **"seat"** — a prompt saying "sitting in a row of five
seats, numbered 1 to 5" has gold using "Seat 1: Ivy", which the day/ordinal/
bare-number cases didn't anticipate; (2) **day RANGES** — "scheduled from
Monday to Thursday" only names the two endpoint days, not all four
individually, so the original day-detector (which required literal mentions
of every day) undercounted and fell through to the bare-number default.
Fixed: explicit `seat`/`seats` keyword → `"Seat N"` labels; a day-range
regex (`"<day> to/through <day>"`) that fills in the calendar days between
the two named endpoints (still grounded in the puzzle's own two stated
words, not invented). Re-verified against all 5 real cases now on file
(day-list, ordinal, bare-number, seat, day-range) — all 5 produce an exact
match to their gold answer's format.

**Round 3 — a second, independent bug, in the measuring instrument, not the
agent**: the round-2 re-run still scored 57% strict, unchanged, even though
the actual answer text for the "seat"/day-range cases now matched gold
*exactly* (byte-for-byte, verified directly). Traced to `eval/judge.py`'s
`_judge_short_text`: 9 of 37 logical_reasoning gold answers (the
gemini-sourced batch, and only those) append a `"Justification: ..."`
reasoning paragraph the task never asked the agent to reproduce. Left in,
it dilutes `_overlap()`'s denominator (fraction of GOLD's words found in
the answer) — a terse, exactly-correct structured answer scores ~15%
instead of ~100%. Fixed by stripping everything from `"Justification:"`
onward before comparison, a no-op for the other 28 tasks that never contain
that literal marker (confirmed by direct count before shipping the fix, not
assumed). Dev-tool-only change (`eval/judge.py` isn't shipped in the
container), no image rebuild needed.

**Final, trustworthy number**: re-judging the same round-2 answers (no
re-run needed — the answers were already correct, only the scoring was
wrong) gives logical_reasoning **28/37 = 76% strict** (up from the original
57%), and the `solver` route specifically **12 pass / 0 fail / 1 unsure**
(92%), up from 5/13. The 4 remaining fails are a different, real issue:
grok-sourced gold answers that are themselves non-specific placeholders
("Specific arrangement satisfying all constraints.", not an actual named
solution) — a dev-set data quality problem, not an agent or judge bug, and
out of scope to fix under the current deadline.

**Takeaway for how this project should read its own numbers going forward**:
three rounds of "found a bug, fixed it, re-ran, found the real number was
still wrong for a *different* reason" on a single category. The lesson
isn't "logical_reasoning is fixed now" (grok placeholders remain, and other
categories haven't had this level of scrutiny) — it's that a single
benchmark run's raw numbers should not be trusted without reading actual
failing examples, because both the agent AND the measuring instrument can
be wrong independently, and a low score can hide a working mechanism behind
an unrelated formatting/scoring bug.

## V23. Fable audit of the 228-run + this session's fixes (2026-07-09)

Full independent re-read of V21/V22 code, the judged results, and the gold
data. Findings, each verified directly against the files:

1. **V22 latent bug found and fixed**: `_position_labels` ordered day labels
   by FIRST MENTION in the prompt. All 5 on-file cases passed only because
   their day enumerations happen to precede any constraint text; a puzzle
   whose constraints mention a day early ("Kevin cannot present on
   Wednesday. Four colleagues present... Monday, Tuesday, Wednesday,
   Thursday") would scramble the position→day mapping. Positions 1..n
   encode earliest→latest, so calendar order is the only correct order —
   and since `_DAYS` is iterated in calendar order, the fix was DELETING
   the mention-order sort. Verified on all 5 prior cases + the adversarial
   one (6/6 exact match). Also fixes the red-herring-day case (5 days
   mentioned, 4 positions: calendar order keeps Mon–Thu, mention order
   could keep the red herring and drop a real day).
2. **Six dev tasks are corrupted at the data level** — their prompts
   announce a payload that was lost in the original chat-paste
   (chatgpt_text_summarisation easy_1/med_1/med_2/hard_1 end at "...in one
   sentence:"; chatgpt_named_entity_recognition easy_1/hard_1 end at
   "...following sentence:"). The agent's "The passage is not provided."
   is the CORRECT response to these; gold expects a summary of the missing
   passage. This accounts for 3-4 of summarisation's 4 judged fails and 2
   of NER's 8. Corrected real picture: summarisation ≈1 real fail (fine),
   NER's real weakness is 3-6 entity-TYPE confusions (e.g. Geneva/São
   Paulo/Dublin listed under ORGS — a precision error, possibly worth one
   prompt-hint line, nothing more).
3. **factual_knowledge's 2 "fails" are judge-too-narrow, not wrong
   answers**: haiku_medium_2 answered Steam Engine/Spinning Jenny/Power
   Loom with correct dates — a fully valid answer to "list three key
   inventions" — but gold names a different valid triple, and keyword
   overlap can't credit alternatives. Open-list questions structurally
   can't be graded by overlap-vs-one-gold; the real LLM judge may well
   accept these. No agent action available or needed.
4. **mathematical_reasoning's 10 fails are the one REAL capability gap**:
   all are wrong numbers on the grok hard tail (got 132 vs 135, 5372 vs
   5768...) — multi-step problems where local+remote+program-check all
   land wrong or unverifiable. This matches zero_token_championship.md's
   prediction that the hard math tail is a genuine 4B ceiling.
   **[CORRECTED same day — see V24. This claim was wrong: I compared
   got-vs-gold without recomputing the golds. 6-7 of the 10 golds were
   themselves wrong or the task incoherent; only 3 fails were real, and
   all 3 shipped via the fallback route (rate-limited dev stand-in), not
   through failed verification.]**
5. **V21 audit**: sound as shipped (demotion-only, tri-state None, spec-not-
   code independence). One unmeasured risk flagged, deliberately NOT built:
   a wrong generated assertion falsely demotes a correct local pass →
   unnecessary escalation (bounded: costs tokens, not accuracy). Measure
   post-submission if scored tokens look high; a ≥2-asserts-fail demotion
   threshold is the ready mitigation. Not touched now — no data, and no
   new code 2 days before deadline without measurement to justify it.
6. **Throttle/fallback/judge-fix audits**: REMOTE_RPM_LIMIT defaults None
   (unset in grading -- dev-only, correct); last-resort `cap` is always
   defined on every path that reaches it; the "Justification:" strip
   cannot fire on any other category (marker counted across all 228 golds:
   logical_reasoning only). No other category shows the V22-round-3
   dilution shape.

**Corrected best-estimate dev accuracy after removing measurement/data
artifacts**: strict ~52% raw → real ≈65-70%, with the only structural gaps
being the hard-math tail and NER type-precision. Code categories remain
unmeasurable by the deterministic judge (V21 caveat) — they stand on the
practice-task container runs (7/8, 6/8).

## V24. Second-pass audit: the math "capability gap" was mostly wrong golds;
## dev data repaired; V21 hardened per literature (2026-07-09)

Triggered by the user's "fix each bug found in the audit + check for
hardcoding + research risky parts." Every number below was recomputed
independently (fractions/floats in a script, printed before acting), not
eyeballed.

**The V23 math claim was wrong, and the correction flips the conclusion.**
Recomputing all 10 failed math tasks' true answers:
- 3 tasks: **agent RIGHT, gold WRONG** (grok_med_1_dup2: true 132, gold
  said 135; grok_hard_1_dup3: true 5372, gold 5768; grok_hard_4: true
  174.96, gold 178.2). All three shipped via `local+program` — the
  program-aided check *confirmed correct answers* that wrong golds then
  failed. V6/V16 machinery worked flawlessly.
- 3 tasks: **both wrong, gold included** (hard_2 true 16/3≈5.33 vs gold
  4.5; hard_6 true 5956 vs gold 8621; hard_7 true ratio 10:9 vs gold
  17:12), and hard_8 is **mathematically incoherent** (its own rates
  finish the job at 1.25× within the first 3 days, before C "joins";
  gold 47/60 is unreconstructable).
- 3 tasks: real agent fails (hard_9, synth_10, synth_12) — **all shipped
  via `fallback`**, the route that exists only because the Cerebras dev
  stand-in was rate-limited (5 RPM). In grading, these escalate to a real
  remote model instead. Zero real fails passed through verification.

**Dev data repaired** (data/dev_tasks/merged.json):
- 7 grok math golds corrected to independently-recomputed values
  (hard_8's gold set to 1 with an acceptance note explaining the
  incoherence). grok-sourced hard math golds are now a known-unreliable
  batch — 6 of 7 checked were wrong.
- The 6 chat-paste-truncated prompts (V23 finding #2) reconstructed from
  their intact golds + acceptance criteria (the payloads' required content
  is fully determined by what the gold summarises/extracts). These 6 need
  a fresh run to produce meaningful scores; their old recorded answers
  responded to broken prompts.

**Re-judged full-228 with corrected golds + open-list judge fix**
(research/benchmark_2026-07-09/full_228_results_goldfixed.json):
strict 52% → 54%, ceiling 83% → 87%. mathematical_reasoning 72% → **83%**
(30/36), and the `local+program` route is now **28 pass / 0 fail /
0 unsure — a perfect record**. factual_knowledge fails 2 → 1 (open-list
questions now cap at "unsure": overlap-vs-one-gold cannot distinguish a
wrong answer from a correct alternative). logical_reasoning still reads
59% here because these are pre-V22 answers; its validated number is 76%
(V22 round 3).

**V21 hardened, this time with literature grounding** (user asked for
research on risky parts): CodeT (2207.10397) works via dual agreement
across MANY candidate solutions — unavailable with one candidate; newer
measurements find only ~35-51% of LLM-generated tests are valid on some
benchmarks (2602.10522), and treating generated tests as ground truth
"risks degrading valid solutions" (2603.28653). A 4B generator is likely
worse. So demote-on-any-single-assert was too aggressive. Changes:
(a) asserts that don't call the candidate's own function are discarded
up front (a foreign-name assert raises NameError and would false-demote);
(b) `run_with_assertions` now executes each assert independently in a
tally harness — AssertionError counts as a real value mismatch, any other
exception means the ASSERT is broken and is discarded — and returns False
only when failures OUTNUMBER passes; mixed signals return None (no
demotion). All six decision branches unit-tested, including the canonical
practice-06 bug (still caught) and a poisoned batch (no longer demotes).

**Hardcode audit (competition-rule compliance): clean.** All runtime
config is env-read (FIREWORKS_*, ALLOWED_MODELS, paths, budgets); no
task-specific strings, names, or answers anywhere in agent/ (grepped);
no dev/test data COPYd into the image (Dockerfile: requirements, llama
binaries, models/, agent/, entrypoint only); REMOTE_PREFERENCE hardcodes
only the *ordering* of model IDs and every call is still gated by the
env-provided ALLOWED_MODELS list with a fallback to whatever the env
lists (guide requires reading ALLOWED_MODELS at runtime — we do).
`_position_labels`' seat/day/ordinal detection keys on prompt vocabulary,
not on any specific task. Nothing to resolve.

**Standing state after this pass**: image rebuilt with all fixes
(V22-day-order, V21-tally, NER type-precision hint). The GPU pod is gone
(proxy now serves a self-signed cert — instance ended). A fresh full-228
on the laptop (~30-40 min, llama-server local) is the remaining
measurement item; the corrupted-task repairs and gold fixes only pay off
in that re-run. It is NOT a submission blocker — practice-task container
runs remain the shipping gate.

## V25. First real leaderboard score: 15/19 (78.9%) — the gate forensics were
right, and the miss lived exactly where dev data said it would (2026-07-10)

The submitted image (all V21-V24 fixes included) scored ACCURACY_GATE_FAILED
at 78.9% — exactly 15/19 against the 16/19 (84.21%) gate that
leaderboard_gate_forensics.md predicted from k/19 quantization of 79 public
scores. Every qualifying entry visible that night sat at 84.2%, 89.5%, or
100.0% — all k/19 values. Treat the 19-item/16-pass model as confirmed.

**Response shipped the same night (commits 3724d6b, 574892a):**

1. **Remote-first factual_knowledge + named_entity_recognition.** Both
   categories have no deterministic verifier and were shipping on the
   self-consistency probe — dev strict 57% on the local+consistent route,
   vs ~100% (program-checked math) and 92% (solver logic). A consistent
   4B is still a 4B on world knowledge and entity typing. Their prompts
   are short (low scored-input cost) so the remote upgrade is cheap;
   qualifiers spend 1.8k-5.4k tokens, we project ~0.5-1k post-tilt.
2. **NER remote completeness hint.** Caught live in the tilt smoke test:
   the remote answer dropped "last March: DATE" that the local answer had
   included — REMOTE_SUFFIX's "concisely" encouraged omission. One-line
   hint ("List every entity, including dates and times. Cities, countries,
   and regions are LOCATION, never ORGANIZATION.") fixed it: micro-test
   returned all 4 entities at 83in/19out tokens.
3. **factual REMOTE_MAX_TOKENS 160 -> 256.** All factual answers are now
   remote; a truncated "explain/describe" answer judges as wrong, and an
   unused cap costs nothing.
4. **Sentiment offered-label-set guard (verifiers.verify).** A prompt that
   offers a closed label set ("positive, negative, or neutral") makes any
   answer outside that set wrong by construction — our smoke-test "Mixed"
   answer is the exact failure shape. Deterministic, free, escalation-only.
   Unit-tested (6 cases) + container micro-test: closed-set prompt escalated
   and shipped "Neutral" (2 output tokens); open prompt kept local "Mixed".
   stated_sentiment_label moved to verifiers.py (shared with router).

**Organizer clarifications (Discord, 2026-07-10)** that shaped the response:
final rankings re-run on REFRESHED randomized prompts (so fixes must
generalize, not overfit the current 19); local-only/0-token is explicitly
legitimate; non-Fireworks routing gets manually audited and DQ'd during
judging; equal-token tie-breaks TBD. See research/win_conditions.md,
research/top5_forensics.md (rank-1's 0-token/100% is code-verified
non-Fireworks Gemini routing — the exact DQ pattern), and
research/tilt_ab_measurement.md (empirical A/B of the tilt, in progress).
