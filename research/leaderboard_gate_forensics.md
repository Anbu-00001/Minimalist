# Leaderboard Gate Forensics — Track 1, live snapshot 2026-07-09

Research-only pass. Fetched the live lablab.ai Track 1 leaderboard directly
(Cloudflare-blocked on direct fetch; used the `https://r.jina.ai/` proxy
prefix, same method as `research/VERDICTS.md` V20 and
`research/zero_token_championship.md` §1.3). Two independent fetch passes
were made a few minutes apart, both against:

`https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`

**Fetch timestamp: 2026-07-09 14:08 UTC** (system clock at fetch time; both
passes were made within the same few minutes of this timestamp, immediately
before this file was written).

Both passes returned **identical counts and identical entries** — no drift
between passes this time (contrast with `zero_token_championship.md` §1.3,
which saw a small discrepancy between its two passes at an earlier, smaller
snapshot). Raw quoted text from pass 2 (verbatim, not paraphrased):

> "Participants 20,727 Teams 4,632 ▲ +175 today Submissions 154 ▲ +130 today
> Drafts in Progress 137 ▲ +34 today"

> "Did not qualify 71"

Pass 2's own summary noted: "The content does not contain a separate
'Qualified' heading with a count number" — the "8 qualified" figure is
derived by counting rows in the qualified table (confirmed identically in
both passes: 8 distinct rows), not from an explicit "Qualified: N" label
elsewhere on the page.

**Honest data-completeness caveat**: `Submissions 154` (lifetime counter) is
larger than `8 qualified + 71 did-not-qualify = 79` visible resolved
entries. The gap (75) is not explained anywhere on the page — plausibly
duplicate/superseded submissions from the same teams, submissions still
mid-scoring, or a counter that includes drafts/re-submits not shown as
distinct leaderboard rows. Not resolved in this pass; flagged rather than
guessed at.

---

## 1. Full qualified + did-not-qualify tables (as fetched)

### Qualified (8/8 captured — matches the row count in both passes)

| Rank | Team | Tokens | Accuracy |
|---|---|---|---|
| 1 | Route AI (Void Martial Clan) | 4,268 | 84.2% |
| 2 | TokenForge Router (OG_Mode) | 5,205 | 84.2% |
| 3 | NovaAI General Purpose AI Assistant (Khdamin btkhbya) | 5,234 | 84.2% |
| 4 | Adaptive Routing Agent (T_ying_yai) | 5,273 | 84.2% |
| 5 | Ligs-Attempt-276 (RLSym) | 5,410 | 84.2% |
| 6 | Minima (Tech debt) | 5,423 | 84.2% |
| 7 | ApexFlow AI: Self-Healing Telemetry Gateway (Tarek Clarke) | 10,522 | 89.5% |
| 8 | Hybrid Token-Efficient Routing Agent (Adam dev teams) | 27,459 | 84.2% |

Cross-checked with a second, differently-worded fetch prompt (pass 2) asking
for raw verbatim quotes of every 84.2%-accuracy row; it independently
returned the same 7 team names/token counts as pass 1's 84.2% rows (Route AI,
TokenForge Router, NovaAI, Adaptive Routing Agent, Ligs-Attempt-276, Minima,
and the "Hybrid Token-Efficient Routing Agent" / Adam dev teams entry),
quoted verbatim e.g.:

> "Route AI Void Martial Clan 4,268 tokens 84.2% accuracy"
> "Hybrid Token-Efficient Routing Agent Adam dev teams 27,459 tokens 84.2% accuracy"

**Correction to the pre-fetch screenshot**: the task brief's screenshot
described "6 of the 8 qualifiers" at exactly 84.2%. This live fetch shows
**7 of 8** at exactly 84.2% (only ApexFlow AI, at 89.5%, differs). Both fetch
passes agree on 7/8, so this is treated as the current, more accurate count
— the screenshot was either taken at a slightly different moment (leaderboard
is live and can change) or undercounted by one; no way to determine which
from here, so both counts are reported rather than silently overwriting the
screenshot's number.

### Did-not-qualify (71/71 captured — matches the page's own "Did not qualify 71" count exactly, confirmed by `wc -l` on the transcribed list)

Full list transcribed from pass 1's fetch (team — failure reason(s) —
accuracy where shown); kept in
`/tmp/claude-1000/-home-anbu-26-class-AMDA/01701512-250e-4586-8141-61eb71a83928/scratchpad/dnq_raw.txt`
for this session (not a project file). Representative raw quotes captured
verbatim during the fetch:

> "We couldn't pull your Docker image. Make sure the package is PUBLIC..." (PULL_ERROR message, recurring verbatim across ~13 entries)
> "Your container was pulled but crashed during evaluation..." (RUNTIME_ERROR)
> "This submission could not be scored..." (used for TIMEOUT, INVALID_RESULTS_SCHEMA, and OUTPUT_MISSING entries alike — the page reuses this phrase across several distinct status codes)
> "The evaluator saw zero model API calls..." (ZERO_API_CALLS, paired with ACCURACY_GATE_FAILED on 2 entries — confirming V20/zero_token_championship's earlier finding that zero-token submissions are not exempt from the gate)

The count of 71 transcribed rows was verified independently against the
page's own "Did not qualify 71" header — they match exactly, so this
appears to be the **complete** did-not-qualify list, not a truncated/
paginated sample (unlike some earlier research passes in this repo that
explicitly could not get a full page).

---

## 2. Is 84.2% really a common cluster point? Yes — and so is every other
## observed percentage, because they're all k/19

Tabulated every distinct accuracy percentage visible anywhere on the page
(qualified + did-not-qualify, ACCURACY_GATE_FAILED entries only — other
failure types don't expose a percentage):

Distinct values observed: 0.0, 10.5, 21.1, 26.3, 31.6, 42.1, 47.4, 52.6,
57.9, 63.2, 68.4, 73.7, 78.9, 84.2, 89.5 (percent).

Checked each against k/n for every denominator n from 2 to 40 (script run
locally against the transcribed list, not hand-checked). **Denominator 19 is
the smallest denominator where all 15 distinct observed percentages match
to within 0.05 percentage points**, i.e. every single accuracy number on the
entire page — qualified and failed alike — is consistent with "k correct
out of a 19-item hidden eval set," with essentially exact agreement:

| Observed | k/19 | Computed | Error |
|---|---|---|---|
| 0.0% | 0/19 | 0.00% | 0 |
| 10.5% | 2/19 | 10.53% | 0.03pp |
| 21.1% | 4/19 | 21.05% | 0.05pp |
| 26.3% | 5/19 | 26.32% | 0.02pp |
| 31.6% | 6/19 | 31.58% | 0.02pp |
| 42.1% | 8/19 | 42.11% | 0.01pp |
| 47.4% | 9/19 | 47.37% | 0.03pp |
| 52.6% | 10/19 | 52.63% | 0.03pp |
| 57.9% | 11/19 | 57.89% | 0.01pp |
| 63.2% | 12/19 | 63.16% | 0.04pp |
| 68.4% | 13/19 | 68.42% | 0.02pp |
| 73.7% | 14/19 | 73.68% | 0.02pp |
| 78.9% | 15/19 | 78.95% | 0.05pp |
| 84.2% | 16/19 | 84.21% | 0.01pp |
| 89.5% | 17/19 | 89.47% | 0.03pp |

(Denominator 38 fits equally well but is just 2×19 with every k doubled —
not new information, the smallest/simplest fit is 19.)

**Hypothesis, well-supported by this arithmetic**: Track 1's hidden LLM-judge
eval set has **19 graded items** (or some mechanism that reduces to
nineteenths — e.g. 19 weighted-equally tasks). 84.2% is common not because
of a shared model ceiling per se, but because **84.2% = 16/19 is exactly the
minimum passing score** (see §3) — so every team that is "just barely
passing" converges on the identical number, because there is no percentage
value between 15/19 (78.9%, failing) and 16/19 (84.2%, passing) that the
grading scheme can produce. Any team hitting the pass bar with no margin to
spare shows 84.2% by construction, not coincidence or shared architecture.
This also explains why raising token budget 5-6x (rank 6 → rank 8: 5,423 →
27,459 tokens) bought **zero** accuracy improvement — both are stuck at the
same 16/19 rung; more tokens didn't flip any additional task from wrong to
right for that team.

ApexFlow AI (89.5% = 17/19) is the one qualifier that clears the bar by a
full extra task, at only ~2x the top team's token count (10,522 vs 4,268) —
notably *not* the 5-6x it cost rank 8 to spend more tokens with no accuracy
gain. This is a real, measured outlier in efficiency-per-accuracy-point, not
just an outlier in raw accuracy.

---

## 3. Accuracy-gate threshold — bracketed tightly

- **Highest failing percentage observed: 78.9%** (= 15/19), on 6 distinct
  did-not-qualify entries: Pahfinder0, Kestrel - v0.29, amd-hackathon-track1,
  rtq-smart-router submission 31, Routing-Agent-That-Works-I-Guess?, TERA:
  Token-Efficient Routing Agent. Confirmed verbatim in pass 2's raw-text
  quote pull, e.g. `"Pahfinder0 ACCURACY_GATE_FAILED" score "78.9%"`.
- **Lowest passing percentage observed: 84.2%** (= 16/19), on 7 of the 8
  qualified entries (§1, §2).
- No entry anywhere on the page shows a percentage strictly between these
  two values — which is expected given §2's finding (there is no k/19
  fraction between 15/19 and 16/19, so the gap is a resolution artifact of
  the eval set size, not evidence of a gate exactly at the midpoint).

**Conclusion**: the real gate threshold is bracketed to the half-open
interval **(78.95%, 84.21%]** — i.e., a submission needs **at least 16 out
of 19** on whatever the hidden eval set weights equally to. This is
materially tighter than anything previously in this repo
(`research/zero_token_championship.md` §1.2 concluded the threshold was "not
publicly documented anywhere," found via guide text + forum + Discord
search). It does not, and cannot from percentage data alone, distinguish
between: (a) a round-number threshold like exactly 80%, (b) a threshold
defined directly as "≥16/19 items correct," or (c) any other value in that
same interval — all are indistinguishable given the eval set's 1/19≈5.26pp
granularity. Practically this makes no difference: **the actionable number
for our own submission is "get at least 16 of however many equally-weighted
graded items exist, if the real eval set is the same size/shape as this
one."** Caveat: this is inferred from a live public leaderboard, not from
the Participant Guide or any official documentation — treat as strong
circumstantial evidence, not a confirmed official number.

---

## 4. Failure-type frequency among the 71 did-not-qualify entries

Tabulated by parsing all 71 transcribed rows (script-counted, not
hand-counted; a few rows carry two tags, e.g. `ACCURACY_GATE_FAILED` +
`ZERO_API_CALLS` together — counted in both rows below, but only once in the
71-row total):

| Failure type | Count | Share of 71 |
|---|---|---|
| ACCURACY_GATE_FAILED | 45 (43 alone + 2 paired with ZERO_API_CALLS) | 63.4% |
| PULL_ERROR | 13 | 18.3% |
| TIMEOUT | 6 | 8.5% |
| RUNTIME_ERROR | 5 | 7.0% |
| ZERO_API_CALLS (always paired w/ ACCURACY_GATE_FAILED here) | 2 | (subset of the 45 above) |
| INVALID_RESULTS_SCHEMA | 1 | 1.4% |
| OUTPUT_MISSING | 1 | 1.4% |

Sum of the mutually-exclusive categories = 43+13+6+5+2+1+1 = 71. Matches the
page's own "Did not qualify 71" total exactly.

**ACCURACY_GATE_FAILED is by far the dominant failure mode (63% of all
non-qualifiers)** — nearly 2/3 of every team that got far enough to be
scored at all still failed on accuracy, not infrastructure. Combined
infra-shaped failures (PULL_ERROR + RUNTIME_ERROR + TIMEOUT +
INVALID_RESULTS_SCHEMA + OUTPUT_MISSING = 13+5+6+1+1 = 26) account for
36.6% — a meaningful chunk, but clearly secondary to the accuracy gate as
the field's actual bottleneck.

**Practical read for our own preflight effort**: infra checks (public
Docker image, container doesn't crash, finishes inside the runtime/request
timeouts, emits schema-valid output) are still worth a final pass — they're
~37% of all failures and 100% preventable by testing before submitting — but
the single highest-leverage thing to verify pre-submission is answer
quality/accuracy against something resembling the real gate, since that is
where roughly two-thirds of the field that even got a valid run is still
failing.

---

## 5. Name-based architecture hints (weak evidence, flagged as such per the task brief)

A striking number of both qualified and did-not-qualify team names contain
near-identical phrasing — "Hybrid Token-Efficient Routing Agent," "Token-
Efficient Routing Agent," "Hybrid Routing Agent," "Token Router" — recurring
across at least ~20 of the ~79 total visible entries, including:

- Qualified #8: "Hybrid Token-Efficient Routing Agent (Adam dev teams)"
- Did-not-qualify: "VoxRouter — Hybrid Token-Efficient Routing Agent,"
  "TokenForge — Hybrid Token-Efficient Routing Agent" (note: distinct from
  qualified #2 "TokenForge Router (OG_Mode)" — a different team with a
  near-duplicate name), "Hybrid Token-Efficient Routing Agent (Track 1),"
  "RouteZero: Hybrid Token-Efficient AI Agent," "TokenOptimizer — Hybrid_
  Routing_System," "Hybrid Routing Agent — Local First, Tokens Last,"
  "TERA: Token-Efficient Routing Agent," "KORA - Token-Efficient Routing
  Agent," "Verification-Driven Token-Efficient Routing Agent," "Token-
  Efficient Routing Agent" (bare), and others.

This pattern (many teams independently landing on nearly the same generic
name) is consistent with a shared starter-kit/reference-implementation name
from the hackathon organizers or a widely-copied example repo, which teams
then lightly customized. **This is offered only as a hypothesis, not a
confirmed fact** — a shared name is weak evidence of shared code, and could
equally just reflect the task brief's own literal category name ("Hybrid
Token-Efficient Routing Agent" is close to the track's own framing) drawing
independent teams to similar naming. Noting it because if true, it would
partly explain §2's clustering (many teams on a similar base architecture
converging on the same 16/19 accuracy) — but this is circumstantial, and the
report does not treat it as established.

---

## Sources (all fetched directly this session)

- `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
  — 2 passes, 2026-07-09, ~14:08 UTC, both agreeing on 8 qualified / 71
  did-not-qualify / 154 total submissions.
- `research/VERDICTS.md` V20 (read for prior methodology/context, not
  re-fetched from source).
- `research/zero_token_championship.md` (read for prior methodology/context
  and the prior "threshold not publicly documented" finding this pass
  updates).

## Answers to the two questions asked

**(a) Best-supported estimate of the accuracy-gate threshold range**: strong
circumstantial evidence the hidden Track 1 eval set has 19 equally-weighted
graded items, and that the pass bar requires **at least 16 of 19 correct
(≥ ~84.2%, definitely > 78.9%)**. This is the tightest bracket this repo has
had on the threshold; still not an official/documented number, but now
backed by direct arithmetic on ~80 live leaderboard entries rather than
absence of information.

**(b) Practical implication for our submission checklist**:
1. Treat "≥16/19-equivalent accuracy" (not some vaguer "reasonably good")
   as the concrete target to test against locally before submitting —
   if the real hidden eval is similarly sized/shaped, there is effectively
   zero partial credit for being close but short (15/19 still fails).
2. Infra robustness (public image, no crash, inside timeout, valid output
   schema) still matters — it's ~37% of all current failures on the board
   — but do not over-invest there at the expense of accuracy work; accuracy
   is the dominant failure mode field-wide (63%).
3. Token count is only worth optimizing *after* the accuracy bar is safely
   cleared — note that rank 8's team spent 5-6x the tokens of ranks 1-6 for
   identical (not better) accuracy, and ApexFlow's one extra correct answer
   (17/19 vs 16/19) was worth more competitively than any amount of extra
   token spending at 16/19. Since our own current status is "not yet
   submitted," this suggests validating against a proxy for "16-of-19-ish"
   accuracy (e.g. the 8 official practice tasks per VERDICTS V20) is higher
   priority than further token-budget shaving, right up until accuracy is
   confidently above the bracket identified here.
