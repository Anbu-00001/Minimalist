# cap2 ship risk assessment — factual_knowledge / NER local decode caps (2026-07-12, pre-close)

**Verdict up front**: split the categories. **factual_knowledge → SHIP LOCAL**
(remove from `REMOTE_FIRST`). **named_entity_recognition → KEEP REMOTE** (leave
in `REMOTE_FIRST`). This is not a hedge — it is what both the literature and a
direct before/after comparison on our own dev sample point to, independently.

Change required: `agent/router.py:49` —
`REMOTE_FIRST = {"factual_knowledge", "named_entity_recognition", "text_summarisation"}`
→ `REMOTE_FIRST = {"named_entity_recognition", "text_summarisation"}`.
No other code change needed — `config.LOCAL_GEN_CAP["factual_knowledge"] = 56`
and `PROMPT_HINTS["factual_knowledge"]` are already wired into `router.solve()`
and fire automatically once `factual_knowledge` leaves `REMOTE_FIRST`
(`router.py:217-218`).

Verification standard (matches `research/judge_alignment.md`): claims from a
primary source I fetched directly this session are marked **[VERIFIED]**;
claims from a web-search synopsis I did not open are **[UNVERIFIED]**; claims
computed directly from this repo's own data/code (re-running `eval/judge.py`
against on-disk results, reading source) are marked **[REPO DATA]** — these
are the strongest evidence in this report, stronger than the literature,
because they measure our exact system on our exact dev sample.

---

## 0. The decisive evidence: a direct before/after comparison already exists on disk

This is the single most load-bearing finding in this report, and it didn't
require new web research — it required reading two existing dev runs
correctly.

`research/final_gate_projection.md` (2026-07-11, **[REPO DATA]**) ran the
**pre-cap2 image** (factual/NER/summarisation all `REMOTE_FIRST`, i.e. NER
answered by the remote model with its completeness hint) on a 56-task sample
(7/category × 8 categories) and hand-verified every fail/unsure against
acceptance criteria:

| category | judge-strict | **artifact-corrected** | what the correction was |
|---|---|---|---|
| factual_knowledge (**remote**) | 3/7 | **7/7 (100%)** | 4 unsure = correct paraphrases under-credited by keyword overlap |
| named_entity_recognition (**remote**) | 6/7 | **6/7 (86%)** | the one miss: answer covered 4/5 required items, tagged "Geneva Conference" ORG instead of emitting bare "Geneva" LOCATION — a conservative, defensible entity-boundary call |

I re-graded **this session's `eval/tmp_cap_full/` run** (2026-07-12, the actual
cap2 config: `LOCAL_ONLY=1`, `LOCAL_GEN_CAP` factual=56/NER=64 + the terse
`PROMPT_HINTS`, same 7-per-category/56-task shape) the same way — ran
`eval/judge.py`'s own judge functions against every task, then read every
non-pass answer against its `acceptance_criteria` by hand:

| category | judge-strict (this run) | **artifact-corrected** (my read) | what changed vs the remote run above |
|---|---|---|---|
| factual_knowledge (**local, cap2**) | 3/7 | **6-7/7 (86-100%)** | same shape: 4/4 "unsure" cases are complete, correct paraphrases (keyword-overlap artifact, not a real gap) — statistically indistinguishable from remote's 7/7 |
| named_entity_recognition (**local, cap2**) | 4/7 | **4-5/7 (57-71%)** | the pre-existing Geneva-type miss reappears (same defensible entity-boundary call), **plus two NEW completeness failures not present in the remote run**: `chatgpt_named_entity_recognition_med_1` (Beyonce) **drops "Grammy Award" as an entity entirely** — not mislabeled, not truncated, just absent from the answer; `gemini_named_entity_recognition_med_2_dup2` (Ada Lovelace) truncates gold's `"summer of 1843"` to `"1843"` **and** adds two entities the gold explicitly says shouldn't be there (`"Analytical Engine": ORG`, `"London": LOCATION"` when gold states `LOCATION: None`) |

**factual_knowledge shows no measurable degradation switching to local+cap2.**
**named_entity_recognition shows a real, new degradation** — not a formatting
artifact, not a judge-scoring quirk, but entities that are genuinely absent
from the answer against an acceptance criterion that explicitly names them
("Answer must list... Grammy Award as ORGANIZATION").

### 0.1 This is not a token-budget problem — raising the NER cap will not fix it

Checked directly against `research/local_cap_feasibility.md`'s own live
measurement table (**[REPO DATA]**, already in this repo, re-read for this
report): at `NER cap=64` with the terse prompt, the model's natural,
complete-feeling output used only **44 of the 64 available tokens** (18.51s
of a 25s budget) — the model *chose* to stop, it did not hit the cap. The
Beyonce answer in this session's cap2 run is ~30 tokens against a 64 cap —
same pattern, massive unused headroom. **A 4B model asked to "list only, one
entity per line, no explanation" is stopping before it has emitted every
required entity, not being cut off by the cap.** This means the fix this
research was asked to evaluate (a higher NER cap) is evaluated and rejected:
it spends decode-time budget on a lever that isn't the bottleneck. See §3 for
the one lever that plausibly is.

---

## 1. Terse-answer risk under an LLM judge (factual_knowledge)

### 1.1 What was already known (`research/judge_alignment.md`, 2026-07-09)

That file is a thorough prior pass on this exact question and its conclusion
holds: **no paper found runs the precise ablation** (pointwise, intent-match
grading of a terse-but-complete answer vs. a verbose one of identical
substance). The closest adjacent evidence leans reassuring: semantic-matching
QA judges credit terse-correct answers *better* than keyword-overlap metrics
(arXiv:2504.11972, "The early Polish state" vs "Poland" scoring 0% F1 despite
identical meaning); CALM's length-padding robustness rates for frontier
judges are high (GPT-4o 0.977, Claude-3.5 0.952 — resistant to being fooled by
padding a *bad* answer, the mirror image of the risk here).

### 1.2 New evidence found this session

**[UNVERIFIED — fetched via a summarization tool, not read raw]**
arXiv:2604.23178, "Judging the Judges: A Systematic Evaluation of Bias
Mitigation Strategies in LLM-as-a-Judge Pipelines" — the fetched summary
reports family-heterogeneous verbosity preference with actual effect sizes:
**"Pro, Flash, and Llama prefer longer answers (+0.24 to +0.44), Claude
prefers concise (-0.12), and GPT-4o is neutral (-0.04)."** This is a more
concrete, if less certain (single-fetch, not independently re-verified),
number than anything in the prior pass — it says verbosity bias is real and
non-trivial for *some* judge families (Gemini Pro/Flash, Llama), not a
uniformly small effect. **We do not know which model AMD's judge is**
(unresolved in `judge_alignment.md` too), so this is a real, non-zero,
un-hedgeable risk in the abstract.

The same fetch's other reported finding directly favors us, though: when the
paper tested explicit **complete-vs-truncated** answer pairs (not
equal-content-different-length, but genuinely complete vs genuinely
incomplete), **"all models correctly prefer the complete response (0.88-1.00
accuracy)"** — i.e., every judge family tested reliably detects and penalizes
missing content, regardless of its own length-preference quirk. This is the
finding that reframes the whole report: length bias (does the judge like
longer text for its own sake) and completeness detection (does the judge
notice something is missing) are different mechanisms, and the second one is
consistently reliable while the first is family-dependent. That maps directly
onto why factual (terse but *complete*) and NER (sometimes *incomplete*) are
different risk profiles — see §2.

**[UNVERIFIED]** General web synthesis (not a single strong primary source,
several blogs converged on the same claim): rubrics with explicit
"prioritize correctness" / conciseness-neutral language measurably suppress
verbosity bias — "a rubric that emphasizes correctness and relevance makes
unnecessarily long or self-reasoning responses appear less clear." AMD's own
published checklist (quoted in the task brief) already says **"Prioritize
correctness first"** and explicitly warns that **"generic responses do not"**
pass the accuracy threshold — language that, per this (unverified, blog-level)
mitigation research, is exactly the kind of rubric wording that suppresses
length-driven scoring. Weak evidence on its own, but it points the same
direction as everything else in this section.

### 1.3 Verdict for factual_knowledge: LOW risk, ship local

Three independent lines converge: (a) no direct evidence in either research
pass that pointwise/intent-match judges penalize terse-but-complete answers;
(b) our own dev-sample re-grading (§0) shows local+cap2 factual answers are
substantively complete against acceptance criteria at the same rate as the
already-qualified remote path (86-100% either way); (c) the one concrete new
number found this session (2604.23178) shows judges reliably reward
*completeness*, which is what our terse answers have, even where some judge
families have an independent, modest, family-specific length preference we
can't target away because the judge model is unknown. The risk that remains
is real but small and untargetable — not a reason to hold factual_knowledge
back.

---

## 2. NER completeness risk

### 2.1 Direct evidence: our own dev sample (§0), restated as the finding

Two of seven cap2 NER dev tasks lost content that the acceptance criteria
explicitly required, and neither loss was a truncation artifact (§0.1). This
is the strongest evidence in the report and it does not depend on any
literature.

### 2.2 What the literature adds

**[UNVERIFIED — search-synopsis level]** Standard NER evaluation practice
distinguishes **exact match** from **relaxed/partial match** scoring
specifically because "NER systems that correctly identify a valid named
entity without exactly matching the human-annotated entity... generate both
false positives and false negatives when using exact match evaluation" — i.e.
the evaluation research field itself treats missing/boundary-mismatched
entities as a real, double-counted error mode, not a formatting nuance a
lenient reader waves through.

Attempted a direct, primary-source check specifically on "does an LLM judge
give partial credit for an incomplete entity list" (arXiv:2601.00411,
"Do LLMs Judge Distantly Supervised NER Labels Well?" — **[VERIFIED, fetched
directly, but the paper doesn't answer the question]**): the paper confirms
LLM-judge NER evaluation explicitly checks "that all potential labels have
been assigned," and reports **model-family-heterogeneous handling of missing
entities** — on a sentence-completeness check, "GPT-5 and GPT-OSS-120B handle
these near-perfectly (F1 99.2 and 97.4), while Gemma-3-27B-IT discards all 60
such sentences" — but does not isolate partial-completeness scoring from
whole-sentence accept/reject decisions, so it doesn't directly resolve
"does a judge partially credit 5-of-6 entities." Read narrowly, it doesn't
move the estimate either way; read for texture, it reinforces that
missing-entity handling is inconsistent across judge model families, which
argues for not betting the accuracy gate on a specific (favorable) judge
behavior we can't verify.

The most relevant number found is the one already cited in §1.2: judges are
reliable (**88-100% accuracy, per arXiv:2604.23178's fetched summary**) at
correctly preferring a demonstrably complete answer over a demonstrably
incomplete one. That evidence, read for NER rather than factual, is the
opposite of reassuring: it says a real LLM judge is *likely* to notice that
"Grammy Award" is missing from an answer whose acceptance criteria names it
explicitly.

### 2.3 Verdict for named_entity_recognition: HIGH risk, keep remote

The case against shipping local NER doesn't need the literature — it's in
our own data. Cap2's tight prompt-plus-cap combination produces answers that
are shorter than what a "list every entity" instruction should produce, and
the missing content is exactly the kind of gap (a whole named entity absent,
a required date-qualifier dropped) that both general NER evaluation practice
and the one concrete LLM-judge finding available say gets caught, not
forgiven.

---

## 3. Mitigations considered

1. **Raise the NER cap** (the task's suggested first lever). **Rejected on
   the evidence in §0.1**: the model isn't hitting the current 64-token cap
   when it drops entities (44/64 and ~30/64 tokens used in the two failing
   cases) — more headroom doesn't make the model decide to extract "Grammy
   Award." This lever doesn't reach the actual failure.
2. **Add the proven completeness hint to the LOCAL NER prompt.** Real lever,
   not evaluated live this session — flagged, not shipped. `router.py`'s
   `REMOTE_HINTS["named_entity_recognition"]` already carries *"List every
   entity, including dates and times... Cities, countries, and regions are
   LOCATION, never ORGANIZATION"* — added on 2026-07-10 specifically because
   the remote path dropped an entity under a similar "concisely" pull
   (VERDICTS V25, live-verified fix: "returned all 4 entities at 83in/19out
   tokens"). The **local** `PROMPT_HINTS["named_entity_recognition"]**
   (`router.py:32`) has the LOCATION/ORGANIZATION clause but **not** the
   "list every entity, including dates and times" completeness clause — an
   asymmetry that plausibly explains part of the gap. Adding it costs zero
   scored tokens (it's a local prompt, never sent remote). **Not recommended
   to ship blind tonight**: it is untested against the live server at the
   cap2 cap, there is no time in the remaining window to re-run
   `local_cap_feasibility.md`'s live-server methodology to confirm it fixes
   Beyonce/Ada-Lovelace-shaped drops without blowing the 25s budget, and a
   wrong guess here is exactly the kind of last-minute unverified change
   `research/final_gate_projection.md`'s own STOP/GO rule (2026-07-11) argues
   against this close to a deadline. Worth a post-submission follow-up, not
   a pre-close gate.
3. **Do nothing, keep NER remote.** Recommended. Zero new risk, and per §4
   the token upside of moving NER local specifically is smaller than it
   looks.

---

## 4. Token economics: the NER token upside is smaller than the headline number suggests

`research/token_thrift_audit.md` (**[REPO DATA]**, already in this repo)
directly measured real remote-call token costs (`words × 1.3` heuristic,
consistent across rows even if the absolute tokenizer differs):

| category | fixed overhead (SYSTEM+SUFFIX+hint) | mean raw prompt (tokens) | mean output (tokens, real generations) | rough total/call |
|---|--:|--:|--:|--:|
| factual_knowledge | 24.7 | ~19.2 | 59.7 | **~104** |
| named_entity_recognition | 55.9 | ~69.2 | 19.6 | **~145** |

NER's remote calls are not the cheap side of this pair — its longer input
sentences and larger hint overhead make it cost *more* per call than
factual, despite a much shorter output. **Keeping NER remote and moving only
factual_knowledge local captures the factual-side savings (the bigger single
lever) while forgoing only the smaller of the two.**

Flagging honestly, not resolving: extrapolating this repo's own measured
per-call costs across a 19-task grading run (≈2 factual + 2 NER calls at the
category-per-19-tasks model `final_gate_projection.md` uses) puts the
factual+NER token upside at roughly 500 tokens total (~6% of the 8,282-token
qualified run) — well short of the task brief's "~6,100 projected tokens
(−26%)" figure for cap2. That figure may be right (e.g., if it also credits
avoided `REMOTE_FIRST` bounded-retry doubling — `router.py`'s `models =
models + models[:1]` line, which only fires for `REMOTE_FIRST` categories and
would double a factual/NER call's cost on any transient miss — or if it was
computed a different way not reconstructed here), but it is **not
independently reproduced by this report** from the token-overhead data on
disk, and the split recommended here (factual only) captures materially less
of it than "both local" would. This is a real, open gap between two numbers
in this repo — worth a 10-minute reconciliation before the submission
description cites a specific token figure, but not a reason to hold the
factual-only change, which is justified on accuracy grounds independent of
the exact token count.

---

## 5. Recommendation (restated) and what NOT to do

- **factual_knowledge → LOCAL.** Remove from `REMOTE_FIRST`
  (`router.py:49`). Evidence: no literature finding that terse-complete
  answers are penalized in intent-match grading; our own dev sample shows
  local+cap2 factual matches the already-qualified remote path's
  artifact-corrected accuracy (86-100% either way, n=7 each); AMD's stated
  "prioritize correctness first" rubric language is the kind that
  (weakly-sourced, but directionally consistent) literature says suppresses
  length bias specifically.
- **named_entity_recognition → stays REMOTE.** No code change (it's already
  in `REMOTE_FIRST`). Evidence: our own dev sample shows cap2's local NER
  drops real, acceptance-criteria-named entities that the remote path (with
  its completeness hint) does not drop; the failure is a model/prompt
  completeness gap, not a token-budget truncation (so raising the cap is a
  dead-end lever, verified against this repo's own live-server measurements);
  the one concrete LLM-judge number found this session says judges reliably
  catch exactly this kind of incompleteness (88-100%).
- **Do not** raise `LOCAL_GEN_CAP["named_entity_recognition"]` expecting it
  to fix completeness — §0.1 shows the model isn't using the cap it already
  has.
- **Do not** ship the local NER completeness-hint fix (§3.2) tonight without
  a live re-test — it's the right next experiment, not a verified fix.
- **Verify, before citing it externally**, whether the "~6,100 tokens / −26%"
  cap2 projection in the task brief was computed on a "both categories local"
  basis — if so, the recommended (factual-only) split will not reach that
  number; a smaller, still-real improvement over the qualified 8,282-token
  run is what this report's own token-overhead reconstruction supports (§4).

---

## Sources

**[REPO DATA]** (this repo, read/executed directly this session):
- `research/final_gate_projection.md` — pre-cap2, remote-first factual/NER,
  56-task artifact-corrected results (§0 table, left column)
- `eval/tmp_cap_full/{batch1_clean,batch2,batch3,batch4}/results.json` — the
  actual cap2 run this report grades (§0 table, right column); re-graded live
  this session via `eval/judge.py`'s `judge_one()` against
  `data/dev_tasks/merged.json` gold/acceptance data (script:
  `/tmp/claude-1000/.../scratchpad/grade_cap2.py`, not part of the repo)
- `research/local_cap_feasibility.md` §1/§5 — live-server token-usage-vs-cap
  measurements (§0.1)
- `research/token_thrift_audit.md` §1/§3 — remote per-call token overhead
  measurements (§4)
- `research/judge_alignment.md` — prior-session literature review, not
  duplicated, cross-checked (§1.1)
- `research/VERDICTS.md` V25 — the original remote NER completeness-hint fix
  this report proposes mirroring locally (§3.2)
- `agent/router.py`, `agent/config.py` — current `REMOTE_FIRST`,
  `LOCAL_GEN_CAP`, `PROMPT_HINTS`, `REMOTE_HINTS` (read directly for the
  recommended change and the hint-asymmetry finding)

**[VERIFIED]** (fetched directly this session):
- arXiv:2601.00411 ("Do LLMs Judge Distantly Supervised Named Entity Labels
  Well?") — fetched HTML; confirms LLM-judge NER checks for "all potential
  labels... assigned," reports family-heterogeneous completeness handling;
  does not isolate partial-credit scoring (§2.2)

**[UNVERIFIED]** (search-synopsis or single-fetch-summary level, not
independently re-read from raw text):
- arXiv:2604.23178 ("Judging the Judges: A Systematic Evaluation of Bias
  Mitigation Strategies in LLM-as-a-Judge Pipelines") — fetched-summary
  reported per-family verbosity effect sizes and 0.88-1.00
  complete-vs-truncated accuracy (§1.2, §2.2) — the single most
  action-relevant new number this session found; treat as directionally
  informative, not a confirmed quote, until independently re-verified
- General NER exact-match-vs-partial-match evaluation convention (§2.2) —
  search-synthesis level, standard-enough field knowledge that it's
  low-risk, but not a specific paper quote
- Rubric-wording-suppresses-verbosity-bias claim (§1.2) — multiple
  convergent blog sources, no single strong primary citation found in the
  time available
