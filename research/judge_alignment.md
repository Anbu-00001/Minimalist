# Judge Alignment: does AMDA's answer-formatting risk a real LLM judge? (2026-07-09)

Research question (task brief): our dev-time proxy judge (`eval/judge.py`) is
regex/keyword-overlap based, not an LLM, and V22 found it had a real bug
(penalizing terse-but-correct logic answers via `_overlap()` denominator
dilution — fixed same day). This pass asks: independent of our proxy's own
bugs, what does the published LLM-as-judge literature say about how a REAL
LLM judge treats terseness, missing justification, and format-marker
reliance, for the specific grading shape AMD uses — "LLM-Judge evaluates
each answer against the expected intent" (Participant Guide, quoted
verbatim in `research/zero_token_championship.md` §1.1) — a single
free-text answer graded against an intent/reference description, not a
head-to-head comparison of two answers.

Verification standard applied throughout: every claim below is either (a)
quoted/paraphrased from an abstract I fetched directly (marked
**[VERIFIED]**, with the fetch tool's own extracted text), or (b) reported
as a WebSearch synopsis I did not independently open (marked
**[UNVERIFIED]**, per this repo's existing convention in
`academic_literature_survey.md`). Nothing below is invented or recalled
from training-data memory of paper contents.

---

## 0. The framing question first: how studied is AMD's actual setup?

**Short answer: not very. The literature overwhelmingly studies pairwise
comparison ("which of these two responses is better"), and this is stated
explicitly, by name, in the papers themselves — not just my inference.**

- **[VERIFIED]** Li et al., "Evaluating Scoring Bias in LLM-as-a-Judge"
  (arXiv:2506.22316, Ant Group, DASFAA 2026): "While existing research has
  concentrated on biases in comparative evaluations, scoring-based
  evaluations — which assign an absolute score and are often more practical
  in industrial applications — remain under-investigated." This paper exists
  specifically to fill that gap, and it identifies bias types that are
  *structurally different* from the classic pairwise ones: **rubric order
  bias**, **score ID bias** (how scoring options are labeled), and
  **reference answer score bias** (bias introduced by a reference answer
  present in the scoring prompt) — none of which is "prefers longer/more
  verbose text."
- **[VERIFIED]** Wu et al., "Pairwise or Pointwise? Evaluating Feedback
  Protocols for Bias in LLM-Based Evaluation" (arXiv:2504.14716) directly
  compares the two protocols on the same material and finds pointwise is
  the *more stable* of the two: **"Pairwise preferences flip in about 35%
  of the cases, compared to only 9% for absolute scores."** Mechanism:
  "Pairwise protocols are more vulnerable to distracted evaluation.
  Generator models can exploit spurious attributes (or distractor features)
  favored by the LLM judge, resulting in inflated scores for lower-quality
  outputs." AMD's setup ("evaluate this one answer against the expected
  intent") is pointwise/absolute, not pairwise — this is the closest direct
  evidence found that our actual grading shape is *less* bias-prone than
  the literature's dominant subject.
- **[VERIFIED]** Norman, Rivera, Hughes, "Reliability without Validity"
  (arXiv:2606.19544, UC Berkeley — already cited in VERDICTS V19): 21
  judges, 9 providers, MT-Bench + JudgeBench + RewardBench, 118 runs,
  ~541,000 judgments. Their headline verbosity number — **"verbosity bias
  is small (<0.011) across the cohort"** — is explicitly qualified as
  measured **"under a single pairwise rubric."** Also found: kappa
  deflation of 33-41 percentage points between raw exact-match agreement
  and chance-corrected Cohen's kappa (i.e., judges look far more reliable
  by naive agreement than they actually are); rankings shift by up to 14
  positions across benchmarks; and — importantly — **position bias >0.10
  in two production-deployed judges despite >0.95 test-retest reliability**,
  which is itself a pairwise/listwise-only phenomenon (see §1).

**Conclusion for §0**: the honest picture is a genuine literature gap, not
a resolved question. What exists (a) confirms pointwise/absolute scoring —
AMD's actual mechanism — is measurably more stable than the pairwise setup
90% of the bias literature studies, and (b) tells us the *kind* of bias
that survives into pointwise grading is different in nature (prompt-design
artifacts like rubric ordering and score-ID labeling — things we don't
control and can't hedge against from the answer side) rather than a clean
"rewards verbosity" mechanism. No paper found runs the specific ablation
"terse-but-correct vs. verbose-but-equally-correct, graded pointwise
against an intent description" — the exact case that matters most for us.
Treat everything below as the best available adjacent evidence, not a
direct measurement of our situation.

---

## 1. Which biases are well-established, and which don't transfer to AMD's setup

Per CALM's own 12-bias taxonomy (already cited in VERDICTS V19):

- **[VERIFIED]** Ye et al., "Justice or Prejudice? Quantifying Biases in
  LLM-as-a-Judge" (arXiv:2410.02736). Fetched the HTML body directly (not
  just the abstract). The 12 biases: Position, **Verbosity**,
  Compassion-fade, Bandwagon-effect, Distraction, Fallacy-oversight,
  Authority, Sentiment, Diversity, **Chain-of-Thought (CoT)**,
  Self-enhancement, Refinement-aware. Per their own Table 2, **most biases
  (including Position) are tested in a pairwise-comparison setup; only
  self-enhancement and refinement-aware biases use single-answer scoring.**
  Verbosity bias is defined exactly as expected — "LLM judges favor longer
  responses, even if they are not as clear, high-quality, or accurate than
  shorter alternatives" — but is tested by having GPT-4-Turbo *pad* a
  low-quality answer while preserving its content, then measuring whether
  the judge is fooled. Their **Robustness Rate** (higher = less fooled) for
  this exact manipulation: ChatGPT 0.900, GPT-4-Turbo 0.915, **GPT-4o
  0.977**, Claude-3.5 0.952, Qwen2 0.884. Frontier judges are quite
  resistant to naive length-padding specifically — a materially different
  (and more reassuring) picture than the "verbosity bias is rampant" framing
  sometimes repeated in blog summaries.
- Same source: **CoT bias, as CALM actually defines it, is not "does the
  judge reward an answer that shows its reasoning."** It's "the model's
  evaluation results may vary with and without CoT" — i.e., whether the
  JUDGE itself reasons step-by-step before scoring changes the JUDGE's own
  verdict consistency, not whether the answer being judged contains
  reasoning. This is a distinction worth being precise about: CALM's CoT
  bias is not direct evidence either way for "does a terse answer get
  penalized for lacking justification." I did not find a CALM sub-bias that
  isolates that specific question.
- **Position bias is structurally pairwise/listwise by definition** — it's
  about order effects between multiple candidates shown to the judge in one
  prompt (arXiv:2406.07791, "Judging the Judges: A Systematic Investigation
  of Position Bias in Pairwise Comparative Assessments by LLMs" —
  **[UNVERIFIED]**, title/scope only from search snippet, but the title
  itself states "Pairwise Comparative"). AMD grades one answer against an
  intent description with no second candidate present, so **position bias
  does not apply to our grading shape at all.** Same logic likely applies
  to bandwagon-effect and some framing of self-enhancement (which needs
  either two candidates or judge-authorship metadata we have no control
  over) — several of the 12 named biases are simply off-topic for a
  single-answer intent-match gate.
- Self-preference / family bias: **[UNVERIFIED]** (search-snippet level,
  did not independently open) — multiple 2025-2026 papers (arXiv:2604.06996,
  2508.06709, 2410.21819, 2604.22891) report judges tend to score outputs
  from their own model family higher, with wide and inconsistent effect
  sizes across judge models (one synopsis claimed a 75-84% self-family
  win-rate for two frontier judges and the *opposite* direction, 10-41%
  self-under-rating, for a third) — this is a real, cited phenomenon but not
  independently confirmed here, and more importantly: **we don't know what
  model AMD uses as the judge**, so there is no actionable lever — we can't
  choose to match or avoid a family we can't identify. Noted for
  completeness, not actionable.

**Bottom line for §1**: verbosity, format, and CoT/explanation-presence
bias are real, published, and measurable — but (a) the strongest,
best-replicated numbers are from pairwise setups that don't structurally
match AMD's grading, (b) frontier judges measured under a comparable
length-padding manipulation are fairly robust (88-98% robustness rate), and
(c) an entire fraction of the "12 biases" (position, most of
self-enhancement) simply doesn't apply when there's no second candidate to
compare against.

---

## 2. Does a real LLM judge penalize terse/structured answers lacking justification?

This is the question that matters most for our solver-derived
`"Monday: Sarah\nTuesday: Mark..."`-style answers (V22).

**No paper found runs this exact ablation in a pointwise, intent-match
setting.** The closest and most directly useful adjacent evidence points
the other way from what we feared:

- **[VERIFIED]** "Reassessing Extractive QA Datasets at Scale: LLM-as-a-Judge
  and In-Depth Analyses" (arXiv:2504.11972, from HTML body via search
  synopsis, high-confidence claim reproduced from the paper's own framing):
  LLM-judge correlation with human judgment on short-answer QA rises from
  EM=0.17 and F1=0.36 to **0.85** specifically because the judge does
  *semantic* matching rather than lexical overlap — their own example:
  "The early Polish state" vs. "Poland" scores 0% on word-overlap F1 despite
  identical meaning, but an LLM judge correctly recognizes the match. This
  is functionally the *same bug shape* V22/V23 found and fixed in our own
  regex-based judge (`_overlap()`'s denominator diluted by a
  "Justification:" tail the terse gold never needed) — except the finding
  here is that **LLM judges are specifically better than overlap-style
  metrics at crediting terse-but-correct answers**, not worse. This is
  reassuring evidence, not merely an absence of bad news: the exact failure
  mode our proxy judge had is a documented weakness of *keyword-overlap*
  scoring, one that LLM judges are shown to structurally avoid by matching
  semantics/intent rather than counting shared words.
- **[VERIFIED]** CALM's verbosity-bias robustness rates (§1) were measured
  on the *inverse* direction (does padding a bad answer fool the judge into
  scoring it higher) — but the same mechanism (judges reward
  content/information, not raw token count, when the content is
  discernible) argues against a clean-but-terse structured answer being
  penalized purely for shortness, provided the content that answers the
  question is present and unambiguous. Our solver output is exactly that:
  dense, unambiguous, fully responsive to "who sits where" — it isn't
  *missing* information, it's missing prose padding around information that
  is already fully present.
- A secondary consideration in our favor: several informal/blog syntheses
  of "format bias" (not independently verified against a primary paper —
  see caveat below) describe the bias as judges reading **markdown
  structure, bullet points, and organization as a signal of thoroughness**,
  scoring plain unstructured prose lower than structured content of equal
  substance. If that direction of bias is real, our solver answers
  (`Day: Name` per line) are already *maximally structured* — closer to
  what that bias would reward than penalize. This is speculative
  extrapolation from an unverified claim, not a confirmed finding, but it
  cuts toward "no action needed," not toward "add prose."
- Countervailing, honestly-reported finding: **[UNVERIFIED]**, secondary
  characterization of a Berkeley math-judge study (from
  `www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-121.pdf`, not
  independently opened) reports that "when O3-mini and Claude 3.7 were
  provided with human-developed grading schemes, neither model accurately
  graded solutions, often overestimating the quality of solutions by a
  factor of up to 20, and frequently awarded points for incorrect or
  unjustified reasoning." If accurate, the failure direction is LLM judges
  being *too lenient* on unjustified reasoning, not too strict — again
  cutting against the "terse answers get penalized" worry, though for a
  different (accuracy-of-grading, not bias) reason.

**No evidence found supports the hypothesis that a real LLM judge penalizes
a terse-but-substantively-complete structured answer for lacking prose
justification, in a pointwise/intent-match setting.** The available
evidence (semantic-matching QA judges, CALM's content-vs-padding
robustness, the lenient-grading finding) leans the other way. This is
adjacent evidence, not a direct measurement — flagged honestly per the
task's verification standard — but it gives no reason to add prose to
solver answers.

---

## 3. Math/code: final value only vs. showing work

- **[VERIFIED]** "Rethinking Math Reasoning Evaluation: A Robust
  LLM-as-a-Judge Framework Beyond Symbolic Rigidity" (arXiv:2604.22597).
  Abstract, quoted directly: "Models are evaluated on mathematical
  reasoning benchmarks by verifying the correctness of the final answer
  against a ground truth answer. A common approach for this verification is
  based on symbolic mathematics comparison, which fails to generalize
  across diverse mathematical representations and solution formats. In
  this work, we offer a robust and flexible alternative to rule-based
  symbolic mathematics comparison. We propose an LLM-based evaluation
  framework for evaluating model-generated answers, enabling accurate
  evaluation across diverse mathematical representations and answer
  formats." This paper's entire premise is that **LLM judges are MORE
  format-tolerant than symbolic/rule-based checkers** (the same category
  our own `eval/judge.py` and math-verify belong to), not less. It says
  nothing about requiring shown work — only about final-answer format
  flexibility — but on that narrower question the direction is unambiguous.
- No paper found specifically ablates "final-value-only" vs. "full
  step-by-step derivation" holding final-answer-correctness fixed, in a
  pointwise LLM-judge-against-intent setting for math. The nearest
  adjacent finding (Berkeley math-judge study, §2, unverified secondary
  source) suggests LLM math judges err toward *leniency* on reasoning
  completeness/justification, which — if true — argues against needing to
  show work for the judge's benefit specifically.
- For code: **[VERIFIED]** "Don't Judge Code by Its Cover: Exploring Biases
  in LLM Judges for Code Evaluation" (arXiv:2505.16222). Abstract, quoted
  directly: "Functionally correct code often exhibits variations — such as
  differences in variable names, comments, or formatting — that should not
  influence its correctness. [...] all tested LLM judges are susceptible to
  both positive and negative biases, resulting in inflated or unfairly low
  scores. [...] LLM judges remain vulnerable to these biases even when
  prompted to generate test cases before scoring." This confirms code
  judges (without execution) ARE swayed by surface style including
  comments — but the bias runs **both directions** (positive and negative)
  and is about incidental style variation (naming, comment presence,
  formatting), not a clean, directional "bare code without comments scores
  lower" finding. There is no evidence here that a comment-free function
  body is systematically penalized versus a commented one; the risk this
  paper documents is noise/inconsistency in either direction, not a lever
  we can reliably pull by adding comments.

**V4 relevance ("local answers polished, remote answers lean")**: nothing
found requires revising this for math/code specifically. The one clear,
directly-verified point is that LLM math judges are *designed to be* more
format-tolerant than the symbolic/regex checkers we use internally — which
if anything argues our own `eval/judge.py`/verifier format requirements
(needing a parseable final number, needing code to parse as Python) are
STRICTER than what a real LLM judge would need, not laxer. That is a
reassuring asymmetry: our local dev tooling is the more demanding grader on
this axis, not the real one.

---

## 4. Format-marker reliance ("ANSWER: <value>") — risk of over-fitting to our own proxy judge's literal parsing?

This is the sharpest, most concrete finding in this research pass.

`eval/judge.py`'s `_final_number()` (lines 49-63) **requires** finding a
number, preferring one after a literal `ANSWER\s*[:=]` regex match, falling
back to trailing digit-bearing lines. This is a hard literal-string
dependency in OUR proxy. The question was whether shipping the "ANSWER:"
line specifically to satisfy this regex creates risk if a real LLM judge
doesn't parse for that exact marker (either because format compliance
itself becomes a scored dimension, or because omitting it in some edge
case would cause the real judge to fail to locate our answer).

- The math-judge-format-tolerance finding in §3 (arXiv:2604.22597) directly
  answers the second half: an LLM judge reading natural language does not
  need a literal marker to locate "the number this answer commits to" the
  way a regex does — it can read the whole response and identify the
  final/intended answer regardless of surface presentation. This is
  precisely the capability gap the paper's title names ("Beyond Symbolic
  Rigidity") — symbolic/rule-based extraction is the rigid one; LLM
  judging is the flexible one.
- No evidence found suggests an LLM judge would positively require or
  reward a specific literal marker string like `ANSWER:` as a format-
  compliance signal (as distinct from just making the final answer easy to
  find, which any clearly-written answer does). The `ANSWER:` line is best
  understood as a **convenience anchor for our own regex-based tooling**
  (`eval/judge.py`, `agent/verifiers.py`'s math check) and a mild clarity
  aid for a real judge, not a requirement the real judge imposes. Nothing
  found suggests keeping it is harmful, and nothing found suggests dropping
  it would sink an otherwise-clear answer with a real LLM judge — the risk
  asymmetry is opposite to what was worried about: **our own regex proxy
  is the fragile, marker-dependent grader; the real LLM judge is expected
  to be the robust one.**
- The one genuinely-relevant pointwise-specific bias found (§0,
  arXiv:2506.22316's "reference answer score bias") is about the *judge's
  prompt design* (whether/how a reference answer is embedded in the
  grading prompt), which is entirely outside our control — not about our
  own answer's formatting. Not actionable from our side.

**Conclusion for §4**: keep `ANSWER:` — it costs nothing, helps our own
dev-time verification remain cheap and deterministic, and there's no
evidence it either helps or hurts against a real judge. But do not treat it
as load-bearing for the real gate, and do not warp answer content
specifically to make our own regex happy at the expense of genuinely
answering the intent — the literature's direction is that the real judge
is the more format-forgiving reader, our own tooling is the strict one.

---

## 5. Recommendation

**V4's posture holds. No answer-formatting change is indicated by this
research.** Specifically:

1. **Terse solver answers (V22 shape, `"Monday: Sarah"` etc.): keep as-is.**
   No evidence found that pointwise LLM judges penalize dense, unambiguous,
   fully-responsive structured answers for lacking prose. The adjacent
   evidence (semantic-matching QA judges scoring terse-correct answers
   *better* than overlap metrics; CALM's high robustness rates against
   content-preserving padding; a math-judge study leaning lenient on
   justification) leans toward this being safe, not risky. The failure
   mode we found and fixed in our OWN judge (V22/V23: `_overlap()` penalizing
   terseness via denominator dilution) is specifically the kind of error
   LLM judges are shown to avoid by matching semantics/intent instead of
   counting shared words — i.e., a real judge is less likely to have had
   V22's bug in the first place, not more.
2. **`ANSWER:` marker: keep it, but stop treating it as a risk lever
   either way.** It's free, it disambiguates for both our own regex and a
   real reader, and the literature (arXiv:2604.22597) suggests real LLM
   judges are the format-*tolerant* party in this relationship — the
   marker is a convenience, not a compliance requirement to hedge against.
3. **Math/code final-answer-only vs. showing work: no change needed.**
   No paper found requires shown work for a pointwise LLM judge to credit a
   correct final answer against a stated intent; the one relevant finding
   available leans toward judges being too lenient on justification
   quality, not too strict about its presence.
4. **Local-polished / remote-lean split (V4/V3): keep, downgrade the
   confidence of the *reason* slightly, not the policy.** V4's original
   citation (2411.16594) could not be verified to contain the specific
   "prefer longer, authoritative-looking, well-formatted" phrasing from its
   abstract alone (fetched directly — the abstract text available did not
   contain that sentence). The underlying claim is still well-founded, just
   better anchored to a different, directly-verified primary source: Zheng
   et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
   (arXiv:2306.05685 — **[VERIFIED]**, abstract quotes: "We examine the
   usage and limitations of LLM-as-a-judge, including position, verbosity,
   and self-enhancement biases..."), the seminal source the whole
   later literature (CALM, "Reliability without Validity," etc.) builds on.
   Recommend citing 2306.05685 alongside/instead of 2411.16594 for this
   specific claim in any future write-up. The policy itself (local answers
   free to be clean and complete since local tokens cost nothing; remote
   answers lean since they're metered) remains correct on cost-benefit
   grounds alone even where the bias-avoidance rationale is weaker than
   V4 stated it — polishing free local answers is a strict-dominance move
   regardless of judge behavior (it can only help or be neutral, never
   hurt token rank), so this recommendation doesn't actually depend on
   resolving the citation question.
5. **Genuine open risk, not resolved by this research, worth stating
   plainly**: no paper found runs the precise ablation that matters most —
   pointwise, intent-match grading of a terse-structured answer vs. a
   verbose-prose answer of identical substance. Everything above is the
   best *adjacent* evidence available, triangulated from pairwise-bias
   literature, pointwise-scoring-bias literature (a much smaller
   corpus), semantic-QA-judge literature, and math/code-judge literature —
   not a direct measurement of AMD's exact setup with an unknown judge
   model. This should be read as "no red flag found after a genuine
   search," not "proven safe."

---

## Sources (all URLs fetched or searched this pass)

Directly fetched (abstract or body quoted verbatim above):
- arXiv:2506.22316 — Evaluating Scoring Bias in LLM-as-a-Judge
- arXiv:2410.02736 — Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (CALM)
- arXiv:2604.22597 — Rethinking Math Reasoning Evaluation: A Robust LLM-as-a-Judge Framework Beyond Symbolic Rigidity
- arXiv:2407.01085 — Explaining Length Bias in LLM-Based Preference Evaluations
- arXiv:2601.08843 — Rubric-Conditioned LLM Grading: Alignment, Uncertainty, and Robustness
- arXiv:2408.08656 — LLMs Are Biased Towards Output Formats! (confirmed: about generation format variance, NOT judge bias — do not conflate)
- arXiv:2504.14716 — Pairwise or Pointwise? Evaluating Feedback Protocols for Bias in LLM-Based Evaluation
- arXiv:2411.16594 — From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge (abstract fetch did not surface the specific "prefer longer/well-formatted" quote — flagged, not asserted)
- arXiv:2306.05685 — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (seminal source, confirms position/verbosity/self-enhancement bias by name)
- arXiv:2505.16222 — Don't Judge Code by Its Cover: Exploring Biases in LLM Judges for Code Evaluation
- arXiv:2606.19544 — Reliability without Validity (already cited in VERDICTS V19; re-verified with more detail this pass)

Search-snippet level only, not independently opened (**[UNVERIFIED]**,
noted inline above): arXiv:2504.11972 (Extractive QA LLM-judge), 2406.07791
(position bias, pairwise-only by title), 2604.06996 / 2508.06709 /
2410.21819 / 2604.22891 (self-preference/family bias cluster), Berkeley
math-judge grading-scheme study (EECS-2025-121.pdf), assorted "format bias"
blog syntheses (tianpan.co, channel.tel) — used only as directional color,
never as the basis for a numeric claim in the recommendation.
