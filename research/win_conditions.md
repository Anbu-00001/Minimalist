# Win Conditions Audit — Track 1, AMD Developer Hackathon Act II

Deadline: **2026-07-11 16:00 UTC**. Written 2026-07-10 evening IST, after tonight's
fix push (~21:30 IST / ~16:00 UTC-5:30 = ~15:30 UTC Jul 10, per git log below).
Every claim below is tagged **PRIMARY** (read directly from the Participant Guide
PDF, a directly-fetched page, or this repo's own git history) or **UNVERIFIED**
(WebSearch synopsis / search-snippet only, primary source not independently
confirmed in this pass). Nothing is presented as fact without one of those tags.

---

## 1. Participant Guide PDF — every rule affecting final scoring (verbatim)

Source: `Participant Guide_ AMD Developer Hackathon (ACT II).pdf`, repo root, read
directly in full (8 pages) this pass. **PRIMARY.**

### 1.1 What Track 1 must submit

> "A **Docker image** pushed to a public registry (e.g. GitHub Container
> Registry, Docker Hub). Check out the Image Architecture requirement at the
> bottom of this document"

Container contract:
> "1. Read tasks from `/input/tasks.json` on startup ... 2. Write results to
> `/output/results.json` before exiting"

**No video, slide deck, GitHub repo, or live-demo URL is listed anywhere in
Track 1's "What to submit" section.** Contrast with Track 3 (§1.6 below),
where all three are explicitly required. This is the first piece of evidence
that Track 1 is not judged on presentation materials — see §2 for
confirmation from the event page itself.

### 1.2 Environment variables (Track 1 only)

> "The harness injects these at runtime. Read them from the environment: do
> not hardcode values or bundle a .env file in your image."

| Variable | Description (verbatim) |
|---|---|
| `FIREWORKS_API_KEY` | "Provided by the harness — use this key, not your own" |
| `FIREWORKS_BASE_URL` | "Base URL for all Fireworks API calls — must be used to configure your client" |
| `ALLOWED_MODELS` | "Comma-separated list of permitted Fireworks AI model IDs, published on launch day" |

> "**Important:** All API calls must go through `FIREWORKS_BASE_URL`. Calls
> that bypass this URL will not be recorded and the submission will score
> zero tokens. Do not hardcode model IDs: read from `ALLOWED_MODELS` at
> runtime."

### 1.3 Track 1 rules (verbatim, full list)

> "- Exit code `0` on success, non-zero on failure
> - Maximum runtime: **10 minutes**
> - Only models in `ALLOWED_MODELS` are permitted, calls to other models
>   invalidate the submission
> - `/output/results.json` must be valid JSON, malformed output scores zero
> - **Local models and tokens used locally count as zero** for the final
>   score; all inference must go through Fireworks AI via `FIREWORKS_BASE_URL`
> - Do not hardcode or cache answers; evaluation uses unseen prompt variants
> - Image compressed size must not exceed 10GB — larger images are rejected
>   before pulling
> - Submissions are rate-limited to 10 per hour per team"

**Reading the "Local models... count as zero" + "all inference must go
through Fireworks" pair together**, cross-checked against the live event
page (§2.2, which frames Track 1 explicitly as "local model **or** call a
remote model via Fireworks AI credits") and against Track 2's environment
section two pages later (*"No API key or model restriction is injected. You
may call any model, API, or framework: use your own credentials inside the
container"* — a Track-2-only freedom, explicitly contrasted with Track 1's
restriction): the most consistent reading is that **local inference is fully
legitimate and free**, and the Fireworks-only mandate applies specifically to
**remote** calls — i.e. you may not call a non-Fireworks remote API (OpenAI,
Anthropic, Google, your own hosted endpoint, etc.) as a way of getting free
intelligence while dodging the token meter. This lines up exactly with
tonight's organizer Discord clarification (per the task brief, not
independently re-verifiable by this researcher since Discord isn't
fetchable): *"non-Fireworks routing will be found in manual audit and
DISQUALIFIED during judging."*

### 1.4 Scoring (verbatim, the entire section)

> "1. **Accuracy gate**: LLM-Judge evaluates each answer against the expected
> intent. Submissions below the accuracy threshold are excluded from the
> leaderboard.
> 2. **Token efficiency**: submissions that pass the accuracy gate are ranked
> ascending by total tokens recorded by the judging proxy. Fewer tokens =
> higher rank."

No numeric threshold is given anywhere in the PDF. (This repo's own
`research/leaderboard_gate_forensics.md` independently triangulated the
threshold to **≥16/19 correct** — see §4 below — from live leaderboard
arithmetic, not from the guide.)

### 1.5 General rules (all tracks, verbatim)

> "- Your container must start and be ready within **60 seconds**
> - Response time per request must be under **30 seconds**
> - All responses must be in **English**
> - Do not hardcode or cache answers to specific inputs — evaluation uses
>   unseen variants
> - Container images must be publicly pullable at submission time"

### 1.6 Image architecture requirement (verbatim)

> "The judging VM runs `linux/amd64`. Your image must include a
> `linux/amd64` manifest or it will fail to pull and score zero."

### 1.7 Track 3 (Unicorn) — included only to show the contrast with Track 1

> "What to submit: GitHub repository URL (Yes) / Demo video (Yes) / Slide
> deck (Yes) / Live demo / hosted URL (Optional but recommended) ... Note:
> automated pre-screening only inspects the GitHub repository, slide deck
> (PDF), and live demo/hosted URL — it does not process the demo video."
>
> "Judging: Submissions are pre-screened automatically for AMD resource
> usage and originality, then **reviewed by human judges**. AMD compute
> usage is a requirement: projects that do not demonstrate it will be
> disqualified."

Track 3 is explicitly a hybrid pre-screen + human-jury track. **Track 1 has
no equivalent jury-review clause anywhere in the guide.**

### 1.8 What the guide does NOT say (checked directly, absent from all 8 pages)

- No accuracy-threshold percentage or fraction.
- No tie-breaking rule for equal token counts.
- No statement distinguishing a "rolling leaderboard" from a separate "final
  evaluation" pass, and no statement about whether prompts change after the
  deadline.
- No mention of video/presentation quality affecting Track 1 scoring.
- No mention of what happens to a submission still in a failing status at
  the exact submission-close instant.

---

## 2. lablab.ai platform meta — is Track 1 pure leaderboard, or is there a jury layer?

### 2.1 The determinative quote — **PRIMARY**, directly fetched this pass and
### independently corroborated by this repo's own earlier research pass

`research/competitors_lablab.md` (2026-07-07 research pass, fetched directly
via the `r.jina.ai` proxy workaround) quotes the official Act II event page:

> "Scoring varies by track. **Tracks 1 and 2** are ranked via **leaderboard**.
> **Track 3 — Unicorn Track** is evaluated by judges using the criteria
> below."

This is as close to a direct organizer answer to "is Track 1 winner purely
leaderboard rank, or is there a jury layer on top" as exists anywhere in the
collected research: **no jury layer for Track 1.** Judging criteria
(Creativity/Originality, Product/Market Potential, Completeness, Use of AMD
Platforms) are listed **only** under Track 3 on that same page.

### 2.2 Track 1's own official description (same source, verbatim)

> "Build an AI agent that completes a fixed set of tasks autonomously by
> deciding in real time whether to use a **local model** or call a **remote
> model via Fireworks AI credits**. The goal: pick the cheapest option every
> time, without falling below the accuracy threshold."
>
> "💡All models and tokens used locally count as **zero** toward the final
> score."
>
> "Want to fine-tune your router? Go for it. Prompt-based and fine-tuned
> approaches are scored exactly the same way: **token count and output
> accuracy**."

This is the organizer's own two-variable description of what Track 1
scoring consists of — token count and output accuracy, nothing else — and it
matches the PDF's Scoring section (§1.4) exactly. **This confirms local-only
is an explicitly endorsed strategy, not a loophole** — which matters directly
for reading the 0-token leaderboard entry discussed in §5.

### 2.3 Track 1 prizes (same source, verbatim)

> 🥇 1st $2,500 / 🥈 2nd $1,500 / 🥉 3rd $1,000, plus a separate "**Best Use
> of Gemma via Fireworks — $1,000**" side prize.

### 2.4 Caveat: the generic lablab.ai submission form may still apply as a
### completeness gate, separately from scoring

`research/hackathon_meta_amd_ecosystem.md` (fetched directly this repo's
earlier pass) quotes lablab.ai's platform-wide **Hackathon Rule Book**
(`lablab.ai/hackathon-rules`, fetched via proxy, corroborated by two
independent guide pages using near-identical wording):

> (paraphrase, corroborated across two independently-fetched pages)
> submissions require both PDF and video presentations in MP4 format; cover
> image required PNG/JPG 16:9; accessible demo URL; judging on a 4-category,
> 5-point scale — Presentation, Business Value, Application of Technology,
> Originality.

This looks, on its face, like it contradicts §2.1-2.2. The most defensible
reconciliation: **this is lablab.ai's generic, platform-wide submission-form
template** (used across all their hackathons, all tracks, all events), which
may be required to have a "complete" submission page at all — but for Track 1
specifically, the Participant Guide (§1.1, §1.4) and the event's own
track-scoring statement (§2.1) both independently and specifically say
scoring is leaderboard-only (accuracy + tokens). **Not fully resolved**: this
researcher could not find an explicit statement reconciling "the generic
rule book requires a video" with "Track 1 is scored by leaderboard only."
Re-fetching `lablab.ai/hackathon-rules` this pass returned only the
disqualification clause (§3.4) and confirmed the specific post-deadline /
tie-break / jury-vs-leaderboard questions are **absent from that document**:

> (this pass, direct re-fetch) "The rulebook does not contain specific
> language addressing: What happens to submissions after the deadline...
> Tie-breaking procedures for equal scores... Distinctions between
> leaderboard-ranked tracks versus jury-judged tracks."

**Practical read**: filling in the submission form (title, short/long
description, cover image, GitHub link if any, video if the form requires
one to publish at all) is plausibly necessary to have a submission entry
that exists/displays correctly on the platform — but there is no evidence
anywhere, across two independent research passes and this one, that its
*quality* affects Track 1's leaderboard rank. Treat as **complete but
don't polish further** (see §7).

### 2.5 UNVERIFIED items from this pass's WebSearch (flagged, not trusted)

A WebSearch synthesis this pass produced the sentence: *"Entries marked
'Review' are ranked but held pending manual review before any prize
decision."* **This could not be traced to any actual quoted page text in the
search results returned** — it reads as the search tool's own generated
gloss, not a verbatim finding. **Marked UNVERIFIED — do not rely on this
for planning.** Similarly, a second WebSearch pass characterized "AMD
automated judging system" language and "manual submission is available for
6 hours post-hackathon for those with valid reasons and prior approval" —
the second phrase **was** traced to a direct proxy-fetch of
`lablab.ai/hackathon-rules` this pass and is treated as **PRIMARY** (platform
-wide rule, not confirmed Track-1-specific, and gated on "prior approval" —
not a blanket allowance).

---

## 3. Timeline mechanics — rolling leaderboard vs. final scoring

### 3.1 What the caption text implies, reasoned through

Given caption (from the task brief, not independently re-fetched by this
researcher — presented as given): *"These submissions couldn't be scored
yet. Fix the issue shown below — image fixes are re-scored automatically on
the next run; other fixes need you to re-save your submission."*

This describes an **ongoing, cyclical re-scoring mechanism** during the
rolling/live phase: pushing a new image tag does not require you to
resubmit the form, because "the next run" will pick it up automatically.
This is reassuring for tonight's push specifically — see §3.3.

### 3.2 The single biggest unresolved unknown: does DID NOT QUALIFY survive
### to the final refreshed-prompt scoring, or is it eliminated at close?

**No primary source anywhere — not the PDF (checked in full), not the event
page, not `hackathon-rules`, not the AMD forum thread (re-fetched this
pass, returned no relevant content), not this repo's prior research —
resolves this.** The task brief's organizer clarification #2 ("final
rankings will use REFRESHED randomized prompts after submissions close so
overfitting won't carry") describes *what set of prompts* gets used for
final scoring, but not *which submissions* get run against it — specifically,
whether a team sitting in DID NOT QUALIFY at the close instant is included
in that final re-run (and could newly qualify on the refreshed set) or is
simply frozen out because their last rolling-phase result was a fail.

**This researcher's honest position: treat this as unresolved, and plan for
the worse case** — i.e., assume reaching QUALIFIED status *before* 16:00 UTC
is the hard requirement, not something recoverable after close. The
"image fixes are re-scored automatically on the next run" language (§3.1)
is evidence of an active, continuous rolling-phase re-scoring loop, which is
the mechanism that would need to catch tonight's push *before* close for
this to matter at all — see §3.3 for why that part looks safe.

### 3.3 Timing of tonight's own push — PRIMARY, from this repo's git history

```
574892a 2026-07-10 20:54 IST  Sentiment offered-label-set guard...
3724d6b 2026-07-10 20:47 IST  Accuracy tilt: remote-first factual+NER after 15/19 gate miss
b1f73dc 2026-07-10 20:42 IST  Add final submission assets and optimize factual knowledge routing
```
20:54 IST = 15:24 UTC, **~24h 36m before the 16:00 UTC Jul 11 deadline**.
The task brief states the image itself was pushed ~21:30 IST (~16:00 UTC),
consistent with a short build/push tail after the last commit. Given §3.1's
"re-scored automatically on the next run" language, there is a wide runway
(24+ hours, many rolling-phase "runs") for the re-score to land and reflect
a passing status well before close — **timing risk on the push itself looks
low**, conditional on the push having actually completed and the image
being publicly pullable (this researcher could not independently verify
pull success tonight — no push-confirmation log exists in the repo; this
matches a real, previously-documented failure mode in
`research/submission_preflight.md`, which found the *same* image tag
unresolvable on the registry in an earlier pass this week. **Re-run
`docker manifest inspect` against the pushed tag before relying on
anything else in this document** — this is the single highest-leverage
five-minute check available.)

### 3.4 Can the submission form be edited after the deadline? Disqualification triggers

`lablab.ai/hackathon-rules`, direct proxy re-fetch this pass — **PRIMARY**:

> "Unethical behavior, such as plagiarism or gaming the voting system, will
> lead to immediate disqualification." ... "If lablab.ai or its event
> partners determine that a participant has acted in a way that undermines
> the fairness or proper functioning of a hackathon — such as cheating,
> tampering with systems, using unauthorized automation, engaging in
> fraudulent behaviour — [they may be removed]."
>
> "Manual submission is available for 6 hours post-hackathon for those with
> valid reasons and prior approval."

The 6-hour grace window exists but requires "valid reasons and prior
approval" — not a routine lever, and not confirmed Track-1-specific. No
language was found anywhere addressing whether the Docker image tag itself
(as opposed to the form) can be changed post-deadline; the safe assumption
is **no** — treat 16:00 UTC as a hard freeze on the image.

### 3.5 The public leaderboard appears to have changed/gone missing tonight — a live, primary-source finding from this pass

Re-fetching `lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
directly this pass (the same URL that yielded full Qualified/Did-Not-Qualify
tables in `research/leaderboard_gate_forensics.md` on 2026-07-09) returned
**only aggregate event-wide stats** (Participants 20,727 / Teams 4,724 /
Submissions 268 / Drafts 222) and a community activity feed — **no
per-track Qualified/Did-Not-Qualify table rendered**, despite three
separately-worded fetch attempts explicitly asking for it. The activity
feed itself contains a directly-relevant, verbatim community complaint:

> "Bring back the leaderboarddd" ... "where is leaderboard now??" ...
> "It was nice to see what are people doing, can you bring it back?"

**This is a genuine, current, primary-source signal** (not a search
snippet) that the public/anonymous view of the Track 1 leaderboard table has
changed or been pulled down since the 2026-07-09 snapshot. Two plausible,
unconfirmed explanations: (a) the detailed table now requires an
authenticated/logged-in session (the task brief's own operator numbers —
42 qualified / 101 DNQ, specific token values — imply the operator *can*
still see this somehow, e.g. a per-team status view or a still-logged-in
session), or (b) the organizers pulled the aggregate table down ahead of
the close/refresh process described in Discord clarification #2. **Neither
is confirmed.** Practical consequence: **this researcher could not
independently re-verify tonight's 42-qualified/101-DNQ figures or the
0/1798/2138/2228/2664 token values via a fresh anonymous fetch** — they are
carried forward in §4 as operator-reported, not independently re-confirmed
in this pass, alongside the one number that *was* independently
triangulated (the ≥16/19 gate) from the 2026-07-09 snapshot.

---

## 4. Win-probability math

### 4.1 The accuracy gate, independently triangulated — PRIMARY (this repo's
### own prior research, arithmetic re-checked)

`research/leaderboard_gate_forensics.md` (2026-07-09 direct fetch, 79 Track 1
entries transcribed and cross-checked against two independent fetch passes)
found every accuracy percentage on the entire page — qualified and failed
alike — fits `k/19` to within 0.05 percentage points, and bracketed the pass
bar to **≥16/19 (≥84.2%)**, with the highest observed failing score being
exactly **15/19 (78.9%)**. This repo's own submission scored **exactly**
78.9% on 2026-07-10 (per the task brief and per tonight's commit message,
`3724d6b`: *"Leaderboard 2026-07-10 scored us ACCURACY_GATE_FAILED at 78.9%
(exactly 15/19; gate is 16/19)"*) — a precise match to the independently
derived threshold, which is strong internal corroboration that both the
19-item eval size and the ≥16/19 bar are real, not coincidental.

### 4.2 Does tonight's fix plausibly flip the needed 1 task?

Tonight's fix (`b1f73dc`, `3724d6b`) makes `factual_knowledge` and
`named_entity_recognition` **unconditionally remote-first** — every task in
those two categories now escalates to Fireworks regardless of what the
local model produces, on the stated reasoning (commit message, verbatim):
*"The categories with no deterministic verifier shipped on the
self-consistency probe (57% strict on dev)."* If the real 19-task set
distributes roughly evenly across AMD's 8 named categories (~2-3 tasks per
category), factual_knowledge + NER together are ~4-5 of the 19 graded
items — a large enough slice that lifting their accuracy from a ~57%
dev-measured local ceiling to whatever Fireworks's remote models score
plausibly flips at least the single task needed to cross from 15→16.
**This is a reasoned, targeted fix aimed at the actual measured shortfall,
not a guess** — but it carries real, undiscounted risk:

- **No accuracy validation exists for the fix itself.** The only
  post-fix artifact in the repo (`submission/demo_out/results.json`,
  filesystem-newer than the fix commits) is 8 answers with no token counts
  and no judge scoring — it shows the NER fix behaving as intended
  (extracted a "March" → TIME entity, matching the fix's explicit "include
  dates and times" instruction) but does **not** confirm gate-passing
  accuracy on anything resembling the real 19-item hidden set.
- **Three commits landed in the final 12 minutes before push** (20:42→20:54
  IST), including a sentiment-answer guard in the very last commit
  (`574892a`) that touches a category which was *not* the diagnosed
  problem — a nonzero chance of a last-minute regression with no time
  budget left to catch it before the deadline.
- **8 practice tasks (1 per category) cannot validate a 2-category
  structural routing change with statistical confidence** — 1 factual +
  1 NER practice task passing/looking-complete says very little about
  the ~4-5 real factual/NER items in the hidden set.

**Estimate: P(gate pass on next re-score) ≈ 45-60%.** This is a genuine,
wide-uncertainty band, not false precision — the fix is well-targeted
(evidence-based, addressed the actual measured category weakness) but
unvalidated against anything resembling the real grading distribution, and
was pushed with no verification runway.

### 4.3 Token ranking, IF the gate is passed

Operator-reported (not independently re-verified this pass — see §3.5) token
values from tonight's screenshot, presented as given: **0 / 1798 / 2138 /
2228 / 2664**, out of 42 total qualifiers. If these are literally the 5
lowest (i.e., current ranks 1-5), our own numbers bracket as follows:

- **Our pre-fix measurement**: 258 tokens across 8 practice tasks with 3
  remote calls (task brief, operator-reported). **This measurement predates
  tonight's routing change** — under the *old* conditional-escalation
  policy, factual_knowledge and NER only escalated when local verification
  failed; under *tonight's* policy they escalate **unconditionally**. On a
  ~19-task hidden set with ~4-5 forced-remote factual/NER calls (up to 256
  max_tokens each, per `agent/config.py`'s `REMOTE_MAX_TOKENS`), the real
  submitted token count is **very likely materially higher than 258 scaled
  up naively** — the task brief's own "~500-900 tokens" estimate already
  seems to anticipate this, but even that may be optimistic if actual
  factual/NER completions run close to the 256-token cap rather than well
  under it.
- **Scenario A (optimistic, ~500-900 tokens)**: ranks between the 0-token
  entry and the 1798-token entry → **rank ~2 of 43**, ahead of at least
  40 of 42 currently-visible qualifiers.
- **Scenario B (fix-tax realistic, ~1200-2200 tokens)**: still likely lands
  at or below the 2138-2228 cluster → **rank ~2-4 of 43**.
- **Scenario C (pessimistic, >2664 or the factual/NER change costs more
  than expected)**: falls out of the known top-5 sample but 42 total
  qualifiers is a wide field — no data exists on the shape of the
  distribution beyond rank 5, so a confident rank estimate is not
  possible in this scenario.

**Caveat that applies to all three scenarios**: 5 known data points out of
42 is a thin, likely-biased sample (a screenshot glance plausibly captures
the *lowest* visible values, not a random sample) — treat the ranking
estimates as directional, not a confident prediction. The 0-token entry
specifically carries its own ambiguity: per §1.3's reading, a genuinely
local-only run legitimately scores 0 tokens and is fully rule-compliant —
but a 0-token score is *also* exactly what a team would show if they routed
to a non-Fireworks API and bypassed the metered proxy entirely (§1.3,
"calls that bypass this URL will not be recorded and the submission will
score zero tokens" — this is stated as a *mechanism*, not a *penalty*,
which is precisely the exploit organizer clarification #3 says will be
caught in manual audit). **From token count alone, a 0-token qualifier is
indistinguishable between "the single best rank in the competition,
legitimately" and "the single most manual-audit-exposed entry in the
competition."** This cuts in our favor at the margin: if audits remove any
non-compliant top-of-leaderboard entries, our own (verifiably
FIREWORKS_BASE_URL-only, per direct inspection of `agent/router.py` and
`README.md` this pass) compliant mid-hundreds/low-thousands token count
moves up, not down.

### 4.4 What does 42-qualified / 101-DNQ (vs. 8/71 on 2026-07-09) say about
### gate difficulty?

Pass rate rose from **8/79 ≈ 10.1%** (2026-07-09) to **42/143 ≈ 29.4%**
(tonight, operator-reported). Two non-exclusive readings:

1. **Genuine improvement** — teams iterating against real feedback (10
   submissions/hour rate limit allows many attempts) are legitimately
   getting better at the 8 capability categories over the week.
2. **Overfitting to the rolling-phase prompt set** — exactly the failure
   mode organizer clarification #2 exists to neutralize (*"final rankings
   will use REFRESHED randomized prompts after submissions close so
   overfitting won't carry"*). A team that iterates against its own
   status-page feedback for days can converge on answers/formats/prompt
   phrasing tuned to the *specific* rolling-phase prompts it keeps seeing,
   without that tuning generalizing to a refreshed prompt set.

**Read for our own planning**: the current 29.4% pass rate is very likely an
**upper bound**, not a stable estimate, of the *true* refreshed-set pass
rate — some meaningful fraction of the current 42 qualifiers may fall back
out once the prompts change. This is not knowable in advance, but it argues
for weighting genuinely-general verification (deterministic code execution,
CSP-solved logic, program-audited math — all things this repo's
architecture is already built around, per `research/VERDICTS.md` V6/V15/V16)
over anything that could be construed as narrow tuning to observed
rolling-phase failures. **One flag worth naming plainly**: tonight's own fix
(§4.2) was made *in direct response to the rolling-phase leaderboard's own
scored feedback* (a 78.9% result on a real submission) — this is normal,
expected iteration on a real, currently-representative sample of the eval
distribution, not narrow prompt-specific tuning, and is a different and
much lower-risk thing than hardcoding to specific observed prompt/answer
pairs (which the guide explicitly and separately prohibits, §1.3, §1.5).

---

## 5. Leverage not being used / already-spent effort with no scoring weight

Per §1.1 (Track 1's "What to submit" = Docker image only, no video/slides/
repo listed) and §2.1 (event page: *"Tracks 1 and 2 are ranked via
leaderboard"*, jury criteria listed **only** under Track 3):

**No evidence anywhere — across three independent research passes in this
repo plus this one — that video/slide/presentation quality affects Track 1's
leaderboard rank or prize eligibility.** The repo's `submission/` directory
already contains `VIDEO_SCRIPT.md`, `captions.srt`, `cover.html`/`cover.png`,
`slides.html`/`slides.pdf`, and `demo_out/results.json` (all added in
tonight's `b1f73dc`, 20:42 IST). This is **sunk cost**, not wasted in the
sense of "actively harmful," but §2.4's caveat is the honest ceiling on its
value: it may be needed to make the submission-form entry *exist/display*
on the platform (generic lablab.ai rule-book requirement, unconfirmed as
Track-1-specific), but there is no mechanism found anywhere by which
polishing it further moves Track 1's score. **Any remaining time before
16:00 UTC is worth more spent on §7's checklist than on video/slide
polish.**

The one genuine, evidence-backed side-prize lever available and apparently
unclaimed in this audit: *"Best Use of Gemma via Fireworks — $1,000"*
(§2.3, `research/VERDICTS.md` V1 independently flagged this same prize and
recommended Gemma-primary escalation for exactly this reason). Whether the
current `ALLOWED_MODELS`-driven escalation order actually favors Gemma
models was not re-checked in this pass — worth a 2-minute grep of
`agent/config.py`'s `REMOTE_PREFERENCE`/escalation order against
`ALLOWED_MODELS` before close, since it is a second prize with apparently
no additional submission requirement beyond winning-via-Gemma on the same
Docker image already being submitted.

---

## 6. Decision consequences

### 6.1 Must do before 16:00 UTC tomorrow (ranked by leverage)

1. **Verify tonight's push actually resolves publicly, right now.**
   `docker manifest inspect ghcr.io/anbu-00001/amda-agent:latest` (or
   equivalent), then a fresh anonymous `docker pull` from a clean cache.
   `research/submission_preflight.md` documents this exact tag failing to
   resolve in an earlier pass this week — treat as a real, not
   hypothetical, risk until re-confirmed tonight. This is the single
   highest-leverage five-minute action available; everything else in this
   document is moot if the image doesn't pull.
2. **If time and the 10/hour rate limit allow, get one more real
   leaderboard re-score before close** to confirm tonight's fix actually
   crosses 16/19 — §4.2 estimated only 45-60% confidence in the fix without
   this, and the rolling-phase feedback loop (§3.1) is the only ground-truth
   signal available. Do not treat the demo_out/results.json practice run as
   sufficient validation (§4.2) — it has no token counts and no judge
   scoring.
3. **Do not make further code changes without a full 8-practice-task local
   run first.** Three commits landed in the final 12 minutes before
   tonight's push with no verification window — do not repeat that pattern
   this close to the deadline; a late regression with no time to catch it
   is a worse outcome than shipping tonight's already-pushed fix untouched.
4. **Confirm no non-Fireworks remote routing exists anywhere in the image**
   (organizer clarification #3's stated manual-audit DQ trigger). A direct
   read of `agent/router.py`/`README.md` this pass shows all remote calls
   routed through `FIREWORKS_BASE_URL` — worth one final grep for any
   stray base-URL override or debug/dev API key before the final push, since
   this is a full-DQ risk, not a rank penalty.
5. **2-minute check**: does the current escalation order actually prefer
   Gemma models when `ALLOWED_MODELS` includes them? (§5 — the $1,000
   Gemma side-prize, zero marginal submission cost.)

### 6.2 Wasted / low-leverage effort (stop spending time here)

- **Further video/slide/cover-art polish.** §1.1 + §2.1 + §5: no mechanism
  found anywhere by which this affects Track 1's leaderboard rank. What
  exists (`submission/`) is very likely already sufficient for any generic
  platform completeness requirement.
- **Chasing the exact numeric accuracy threshold further.** §4.1 already
  has it triangulated to ≥16/19 with strong internal corroboration (our own
  78.9%=15/19 result matches the independently-derived boundary exactly) —
  no further research value here, only re-verification-by-submission value,
  which is what §6.1 item 2 is for.
- **Trying to reverse-engineer the DID-NOT-QUALIFY-at-close question
  further via more web research.** §3.2: checked the PDF, the event page,
  the rule book, and the AMD forum thread directly this pass — none address
  it. More searching is unlikely to surface a different answer; the correct
  response is to plan for the worse case (§6.1 item 2), not keep searching.

### 6.3 Sober win-probability estimate, reasoning shown

- **P(image pulls and runs cleanly on the judging VM)**: not independently
  confirmed this pass (§3.3) — call it 70-85%, given a real prior failure
  of this exact tag earlier this week (`research/submission_preflight.md`)
  that may or may not have been the same underlying problem as tonight's
  build. **Action item 6.1.1 converts this from a guess to a known fact in
  five minutes — do that first.**
- **P(clears the accuracy gate ≥16/19 | image runs) ≈ 45-60%** (§4.2) —
  a targeted, evidence-based fix, unvalidated against the real hidden set,
  with last-minute regression risk from same-night changes.
- **P(qualifies for the leaderboard at all)** ≈ 0.75 × 0.52 (midpoints)
  **≈ 39%**, before accounting for §3.2's unresolved DNQ-at-close question.
  If that question resolves unfavorably (DNQ at close = eliminated,
  independent of any later refresh-set performance), the above is close to
  the real number that matters; if it resolves favorably, this is a
  floor, not the final answer, because a later refresh-set attempt would
  offer a second chance.
- **P(top-3 prize | qualifies)**: §4.3's scenarios put us plausibly in the
  rank ~2-5 band of a 42-wide (currently) qualified field **on today's
  snapshot**, but §4.4 flags that snapshot as a likely-inflated pass rate
  headed for refresh-driven attrition, and §3.5 means none of the specific
  token numbers behind this estimate were independently re-confirmed this
  pass. Call it **20-35% conditional on qualifying** — genuinely
  competitive, not a lock, wide band reflecting real uncertainty in the
  full 42-entry distribution beyond the 5 known points.
- **P(top-3 prize, unconditional) ≈ 0.39 × 0.27 (midpoint) ≈ 10-11%.**

**Overall read**: this is a submission worth finishing carefully, not a
long-shot to abandon and not a lock to stop iterating on. The gate is the
whole game — §6.1 items 1-3 (verify the pull, get one real re-score, don't
regress with more late changes) dominate everything else in expected value.
Presentation polish (§6.2) has measured zero found leverage on the Track 1
prize outcome specifically.
