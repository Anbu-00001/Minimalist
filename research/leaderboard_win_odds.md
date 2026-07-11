# Leaderboard win-odds — endgame monitor, 2026-07-11 through close

Deadline: **2026-07-12 22:00 UTC** (task-brief-confirmed; see §5 on the
apparent extension from the originally-listed 2026-07-11 16:00 UTC — this
matches the teased `AIatAMD` "BUT WAIT! It is not over!" tweet found by
WebSearch but not directly fetchable, x.com returns 403 to every fetch
method tried across multiple research passes). This document written
starting 2026-07-11 ~13:45 UTC (~19:15 IST), first draft covers the first
~1h of monitoring; the background poller (see §6) keeps extending
`eval/tmp_lb_monitor/snapshots.log` through the night. **Re-check this file
against the tail of that log before the 09:00 IST / 03:30 UTC report
deadline — anything after this doc's last-updated line was not yet folded
into the win-odds table below.**

Method note: the live leaderboard is fetched via
`https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
(Cloudflare blocks a direct fetch; this reader-proxy prefix works). As of
every fetch in this pass (5 separate pulls, 13:05–13:46 UTC), **this URL
renders only the "couldn't be scored yet" (DID NOT QUALIFY) list — the
ranked Qualified table with token/accuracy columns does not render**,
matching `research/endgame_mechanics.md`'s finding from the same morning and
`research/win_conditions.md` §3.5's finding from the night before. Two
alternate URLs (`?track=1`, and the base event page without `/live`) are now
polled every cycle alongside the primary one specifically to catch the
Qualified table if it starts rendering somewhere — none has produced it yet.
**Everything below the Jul-10-evening top-5 in this document is therefore a
model, not a fresh measurement — flagged explicitly throughout.**

---

## 1. Snapshot timeline

| When (UTC) | Source | Qualified table visible? | Field size | Key figures |
|---|---|---|---|---|
| 2026-07-09 ~14:08 | `research/leaderboard_gate_forensics.md`, 2 direct fetch passes | Yes, full | 8 qualified / 71 DNQ = 79 total | Qualified tokens: 4,268 / 5,205 / 5,234 / 5,273 / 5,410 / 5,423 / 10,522 / 27,459. Accuracy: seven at 84.2%, one (rank 7, 10,522 tok) at 89.5%. Gate independently triangulated at **≥16/19 (84.2%)** from k/19 quantization across all 79 visible scores. |
| 2026-07-10 evening (task-brief-reported, not independently re-fetched that pass — `research/win_conditions.md` §3.5 explicitly could not reproduce it live) | operator screenshot | Reported only | 42 qualified / 101 DNQ = 143 total | Top 5: rtq-smart-router **0 tok / 100.0%** (rank 1) — since **code-verified** as an undisclosed non-Fireworks Gemini call, see §3; Kestrel 1,798 tok / 89.5%; Metis 2,138 tok / 84.2%; yassai 2,228 tok / 100.0%; YOLOAI 2,664 tok / 84.2%. Because the table is rank-sorted ascending by tokens, **ranks 2–5 being the four lowest known values means no other qualifier in the visible field was below 1,798 tokens** at that point. |
| 2026-07-10 ~10:35 | lablab.ai `checked` timestamp on AMDA's own DNQ row | N/A (AMDA in DNQ list) | — | AMDA: **ACCURACY_GATE_FAILED, 78.9% = exactly 15/19**, one task short of the gate. This is the pre-accuracy-tilt score (predates commits `3724d6b`/`574892a`). |
| 2026-07-11 13:05–13:12 | `research/endgame_mechanics.md`, 3 fetch passes | No — DNQ-only, ~203 entries | ~203 DNQ visible, qualified count unknown | AMDA row **unchanged**: still `checked Jul 10, 10:35 UTC`, `last resubmitted Jul 11, 13:02 UTC` (≈3.5 min after this repo's `f4d5353` commit). Re-check pipeline confirmed **alive** for other teams same morning (AMD Hybrid Token-Efficient AI Agent checked 09:34 UTC; Mallana checked 12:45 UTC; NanoRouter checked 12:51 UTC). |
| 2026-07-11 13:44–13:46 (this pass) | WebFetch + curl, 2 independent fetches, ~2 min apart | No — same DNQ-only view, 203 `checked` timestamps counted | 203 DNQ | **AMDA row still identical**: 78.9%, checked Jul 10 10:35 UTC, last resubmitted Jul 11 13:02 UTC — **the re-check has not landed as of 13:46 UTC**, ~44 min after the 13:02 UTC resubmit. **NidraRoute** (flagged in the task brief as a suspected second 0-token/100%-accuracy cheat pattern) currently shows **`INFRA_ERROR`** in the DNQ list — no accuracy or token figure visible, i.e. it is **not currently sitting on a visible qualified/100% row**; see §3 for what this could mean. `rtq-smart-router` / `rusetiq` does not appear anywhere in the DNQ list (consistent with it either still being qualified — a table we can't see today — or absent for an unrelated reason; not evidence either way). |
| 2026-07-11 13:46 onward | background Monitor task `b7j4we1r0` (see §6), auto-polling every ~48 min | (ongoing) | (ongoing) | Live-updating; see the tail of `eval/tmp_lb_monitor/snapshots.log` for anything after this document's last edit. |

**AMDA re-check: NOT YET LANDED as of the last poll folded into this
document (13:46 UTC, 2026-07-11).** This is the single highest-priority
event this monitor exists to catch — the moment the `checked` timestamp on
AMDA's row moves past `Jul 10, 10:35 UTC`, that is the first real signal on
whether the accuracy-tilt fixes (and the further logic/sentiment-hardened
image analyzed in `research/final_gate_projection.md`, point-estimate
P(≥16/19) = 93.6%) actually clear the gate. **If the background monitor
catches this before this report is finalized, it is reported at the top of
the final message, not buried here.**

---

## 2. Entries below each token threshold, over time

Because the Qualified table hasn't rendered since 2026-07-10 evening, this
table can only be populated from that one snapshot plus the Jul-9 one — both
carried forward, not re-measured today. Counts are **among visible entries
only** (5 of 42 on Jul 10; all 8 of 8 on Jul 9) — the true count in the full
qualified field is unknown below rank 5/rank 8 respectively.

| Threshold | 2026-07-09 (8 visible / 8 total) | 2026-07-10 evening (5 visible / 42 total) |
|---|---|---|
| < 300 tokens | 0 | 1 (rtq-smart-router, 0 tok — see §3, code-verified cheat pattern, not a legitimate low-token result) |
| < 700 tokens | 0 | 1 (same entry) |
| < 1,500 tokens | 0 | 1 (same entry) |
| < 1,800 tokens | 0 | 1 (same entry; Kestrel at 1,798 is the next-lowest, essentially at this line) |
| < 4,268 tokens (Jul-9's own rank 1) | — | 5 (all 5 visible Jul-10 entries) |

**The load-bearing fact for the strategic question**: on the one occasion
this session has direct visibility into the qualified table's low end
(2026-07-10 evening), **every legitimate entry that could be located was at
1,798 tokens or higher** — nothing "clean" has been observed below that
line at any point in this repo's research history. A genuinely
gate-passing submission anywhere in the 0–1,500 range would, if that pattern
still holds, be competing against an essentially empty field at the low end
— which is exactly why §4's model below finds a mid-range (~700-token)
target dominates on P(rank 1) despite carrying a much less certain P(gate)
than the already-measured ~1,500(→2.7k-actual)-token mode.

---

## 3. DQ / vanish / status-change events

- **rtq-smart-router (rusetiq), Jul-10-evening rank 1, 0 tok / 100.0%** —
  **VERIFIED cheat pattern**, not inference: `research/top5_forensics.md`
  read the shipped `agent.py` directly off GitHub. Every task calls
  Fireworks once, then **unconditionally** calls Google's Gemini API
  directly with a hardcoded plaintext key, and overwrites the Fireworks
  answer with Gemini's whenever Gemini returns anything non-empty — a
  direct, code-confirmed instance of the organizer's stated manual-audit DQ
  trigger ("non-Fireworks routing... will be DQ'd," `research/VERDICTS.md`
  V25). Whether the specific 0-token/100% *mechanism* (Fireworks leg failing
  silently so nothing is metered) is what actually happened is marked
  UNVERIFIED in that research pass, but the underlying non-Fireworks call
  itself is VERIFIED to exist in the shipped code. **Not yet confirmed
  removed from any leaderboard** — we have had no visibility into the
  qualified table since this finding to check whether it vanished. Still
  present or absent is unknown; the background monitor watches for it if the
  table ever renders again.
- **NidraRoute** — the task brief describes this as a second entry matching
  the 0-token/100% cheat profile, but **this session found no prior research
  file documenting that claim independently** (not in `top5_forensics.md`,
  `win_conditions.md`, or elsewhere in `research/`) — it appears to be
  carried in from outside this repo's own research. What this pass **did**
  observe, directly, twice (13:44 and 13:46 UTC): NidraRoute currently sits
  in the **DNQ list with status `INFRA_ERROR`**, first submitted Jul 9
  12:43 UTC, last resubmitted Jul 11 12:31 UTC, checked Jul 11 13:05 UTC —
  no accuracy or token figure shown, because DNQ rows don't carry ranking
  data. Two readings, neither confirmed: **(a)** it was never actually a
  0-tok/100% qualified entry and that claim is stale/mistaken, or **(b)** it
  *was* qualified with that profile at some point and a later resubmission
  (Jul 11 12:31 UTC) broke it into an infra-error state, which would
  functionally remove it from the qualified board **without** requiring an
  organizer DQ action — worth distinguishing from a "vanish" in the DQ
  sense. **Flagged for continued monitoring; if it reappears with a 0-tok/
  100% qualified row, or its `checked` timestamp advances with a new status,
  log it explicitly.**
- **No other vanish/DQ events observed this pass.** The DNQ list grew from
  ~143 total (71 DNQ + 42 qualified, Jul 10 evening) to ~203+ DNQ-only
  visible today (qualified count currently unknown) — consistent with
  ongoing submission volume, not itself a DQ signal.
- **No organizer DQ or tie-break announcement found.** WebSearch this pass
  (query: tie-break/disqualification announcement July 2026) surfaced no
  primary-source statement beyond what `research/VERDICTS.md` V25 already
  has on record from Discord (2026-07-10): *"equal-token tie-breaks TBD."*
  Still unresolved.

---

## 4. Win-odds model

**Scope**: P(rank 1) and P(top 3) for AMDA at four hypothetical token
operating points — {0, 300, 700, 1500} — under two DQ scenarios. This models
*rank given the submission is on the board*, not just gate-pass; gate-pass
probability is folded in as its own factor per level, then multiplied
through to an unconditional figure.

### 4.1 Assumptions, stated explicitly

1. **P(gate) at the 1,500-token label is a real measurement, not a guess**:
   `research/final_gate_projection.md` measured the currently-shipped
   remote-tilted image (factual/NER/summarisation remote-first) at 51/56 =
   91.1% artifact-corrected accuracy on a 56-task sample, giving **P(≥16/19)
   = 93.6% point estimate** (range 80–94% across sensitivity scenarios) —
   and that same measurement found the image's **actual** token cost is
   ≈2.7k on a 19-task run (142 tok/task × 19), materially above the "~1.5k"
   figure this document's token grid uses as a label. **The 1,500 row below
   should be read as "the already-measured, already-shipped high-accuracy
   mode," at its true ~2.7k token cost, not literally 1,500.**
2. **P(gate) at 0/300/700 tokens is NOT measured — it is interpolated** from
   two real anchors in this repo: (a) the **pre-tilt** local-heavy
   configuration scored exactly 78.9% (15/19) on the one real leaderboard
   check that exists (§1); (b) `research/VERDICTS.md` V25 records the
   local-only/self-consistency route at **57% strict on dev** — well below
   the 84.2% gate, and via the binomial model in (3) below, a true per-task
   rate of 57% makes clearing 16/19 astronomically unlikely. On that basis:
   - 0 tok (fully local, no remote calls ever): **P(gate) ≈ 5%** — not zero,
     because math/logic/code have real local verifiers (V6/V15/V21) that
     could plausibly outperform the blended 57% figure on their categories,
     but no measurement supports more than a low-single-digit-to-5% estimate.
   - 300 tok (minimal remote — a couple of short escalation-only calls):
     **P(gate) ≈ 20–25%**, still closer to the pre-tilt 78.9% profile than
     to the full tilt.
   - 700 tok (partial tilt — e.g. factual+NER remote-first, the two
     categories V25 identified as the actual measured shortfall, but without
     summarisation also tilted and/or tighter caps): **P(gate) ≈ 55–65%** —
     retains the two fixes with the largest measured accuracy impact.
   - 1,500-labeled/~2.7k-actual (full tilt, as shipped): **P(gate) = 93.6%**
     (measured, §4.1.1).
3. **Binomial sanity check for a "knife-edge" 84.2% (16/19) qualifier
   surviving a refreshed 19-task gate** (per the task's own framing): modeling
   each task as i.i.d. Bernoulli at rate *r* and asking P(X≥16 of 19):
   - If the observed 84.2% *is* the true generalizing rate (r=0.842, no
     overfitting discount): **P(pass again) ≈ 65%**.
   - If it's mostly rolling-phase overfitting and the true rate is closer to
     0.75 (consistent with `research/win_conditions.md` §4.4's argument that
     the 29.4% rolling pass rate is "very likely an upper bound... of the
     true refreshed-set pass rate"): **P(pass again) ≈ 26%**.
   - If it's a genuinely robust, verifier-backed 90% true rate: **≈ 89%**.
   - **Central planning assumption for "the field's existing knife-edge
     qualifiers": ~50% retention**, i.e. roughly half of today's 16/19-exactly
     qualifiers plausibly drop back out on the refreshed set. This directly
     supports modeling the surviving "clean field" as smaller and possibly
     cheaper (survivors skew toward more genuinely-verified, not just
     luckily-tuned, approaches) than the raw Jul-10 42-qualified count would
     suggest.
4. **Clean-field token floor by close** — trend-extrapolated, not measured:
   the qualified field's token floor (excluding cheat-pattern entries)
   compressed from ≥4,268 (Jul 9, 8 qualifiers) to 1,798 (Jul 10 evening, 42
   qualifiers) in about 30 hours of iteration. Extrapolating a further ~32
   hours to close, with a much larger field (203+ DNQ entries still
   iterating toward qualification) but bounded by real architectural cost
   (§ `research/token_thrift_audit.md`'s finding that per-call overhead is a
   small, largely-fixed cost and the bulk of any remote-touching submission's
   tokens come from unavoidable prompt/output content): assumed
   P(floor < 300 by close) ≈ 10%, P(floor < 700) ≈ 30%, P(floor < 1,500) ≈
   65%, and P(no legitimate 0-token qualifier ties AMDA at 0) ≈ 90%.
5. **DQ scenarios**: (a) rtq-smart-router and any NidraRoute-pattern
   entries are caught and removed before final scoring, consistent with the
   organizer's explicit stated manual-audit process (`VERDICTS.md` V25); (b)
   they are not caught / audit doesn't reach them before scoring, so any
   0-token entry occupies rank 1 ahead of every positive-token submission
   regardless of accuracy, and AMDA-at-0 would face an unresolved tie-break
   against them rather than a clean win.

### 4.2 Win-odds table

**Scenario (a) — suspicious 0-token entries DQ'd before final scoring**

| AMDA token level | P(gate) | P(rank 1 \| gate pass) | P(top 3 \| gate pass) | **P(rank 1), unconditional** | **P(top 3), unconditional** |
|---|--:|--:|--:|--:|--:|
| 0 (fully local) | ~5% | ~97% | ~99% | **~5%** | **~5%** |
| 300 | ~22% | ~90% | ~96% | **~20%** | **~21%** |
| 700 | ~60% | ~70% | ~88% | **~42%** | **~53%** |
| 1,500-labeled (~2.7k actual, shipped) | 93.6% (measured) | ~35% | ~68% | **~33%** | **~64%** |

**Scenario (b) — suspicious 0-token entries NOT DQ'd, tie-break unresolved**

| AMDA token level | P(gate) | P(rank 1 \| gate pass) | P(top 3 \| gate pass) | **P(rank 1), unconditional** | **P(top 3), unconditional** |
|---|--:|--:|--:|--:|--:|
| 0 (fully local) | ~5% | ~15% (ties/loses tie-break vs. earlier-submitted cheat entries) | ~55% | **~1%** | **~3%** |
| 300 | ~22% | 0% (can never beat a literal 0) | ~90% | **0%** | **~20%** |
| 700 | ~60% | 0% | ~78% | **0%** | **~47%** |
| 1,500-labeled (~2.7k actual) | 93.6% | 0% | ~55% | **0%** | **~52%** |

### 4.3 Reading the table

- **For a shot at outright rank 1**, the model finds the **~700-token
  partial-tilt profile dominates both extremes** in scenario (a) — 42%
  unconditional, ahead of both the already-shipped ~2.7k mode (33%, dragged
  down by a field that's already clustering right around/above 1,798) and
  the leaner 300-token mode (20%, dragged down by low P(gate)). **This is
  the single most actionable, non-obvious finding in this model** — but it
  rests entirely on an *unmeasured* P(gate)≈60% for a partial-tilt
  configuration that has not been built or tested; do not treat it as a
  recommendation to ship something untested this close to close without
  validating it first (mirrors `research/final_gate_projection.md`'s own
  STOP/GO caution about same-night unverified changes).
- **For top 3 specifically**, the already-measured ~2.7k high-accuracy mode
  wins in both scenarios (64% / 52%) — its much higher, *measured* P(gate)
  outweighs its worse token-rank odds. This is consistent with
  `research/final_gate_projection.md`'s STOP-ship recommendation: it is the
  safer choice if the goal is "reliably finish somewhere on the podium"
  rather than "maximize the chance of outright first."
- **0 tokens is a trap in scenario (b)** and only middlingly good even in
  scenario (a) — its P(gate) is so low (no measurement supports fully-local
  clearing the gate) that its near-certain rank-if-it-passes doesn't
  compensate. It is dominant *only* conditional on already having passed the
  gate, which is precisely the part with no supporting evidence.
- **The whole model is contingent on §2's single data point** (nothing
  legitimate observed below 1,798 tokens, ever, in this repo's research)
  continuing to hold. If the background monitor catches the Qualified table
  rendering again and finds a new sub-1,000-token legitimate entry, the
  700-token row's P(rank 1\|gate) drops sharply and this section needs
  re-running.

---

## 5. Deadline / tie-break / DQ announcement check

- **Close time used throughout this document (2026-07-12 22:00 UTC)** is
  taken as given from the task brief. A WebSearch this pass for deadline
  language independently surfaced only pre-extension snapshots ("the
  hackathon ends July 11, 2026," "registration... closed July 6th") — **not
  a contradiction of the Jul-12 close**, most likely just search-index
  staleness relative to a live page, and consistent with
  `research/endgame_mechanics.md`'s own record of an original **2026-07-11
  16:00 UTC** deadline plus the teased `AIatAMD` tweet ("BUT WAIT! It is not
  over!") that this and prior research passes have been unable to fetch
  directly (x.com returns HTTP 403 to every method tried, including the
  `r.jina.ai` proxy). **Net read: an extension almost certainly happened;
  its exact terms are still not independently confirmed from primary text,
  only inferred from the task brief and the tweet's headline.**
- **Tie-break rule**: still "TBD" per the one Discord clarification on
  record (`VERDICTS.md` V25). No new organizer statement found this pass.
- **No new DQ announcements found.**
- **No deadline changes beyond the Jul-12 22:00 UTC figure found.**

---

## 6. Ongoing monitoring (background process)

- **Mechanism**: a persistent `Monitor` task runs
  `eval/tmp_lb_monitor/poll_loop.sh`, which fetches the `/live` URL (with up
  to 3 retries ~25s apart per cycle, specifically to catch the
  intermittently-rendering Qualified table) plus two alternate URLs
  (`?track=1`, base event page) every cycle, appends full raw content to
  `eval/tmp_lb_monitor/snapshots.log` with a UTC timestamp header, and emits
  one compact `POLL_EVENT` summary line (AMDA status, NidraRoute status, rtq
  presence, DNQ count, whether "Qualified" appeared anywhere) per cycle.
  Cadence ≈48 minutes between cycle starts (inside the requested 45–60 min
  band once retry time is included). Hard-stops automatically at
  2026-07-12T22:00:00Z.
- **Current task ID**: `b7j4we1r0` (a first version, `bchs8q3wy`, was
  stopped and replaced after its first event revealed a bug — the summary
  line could pick up a non-status AMDA text block from a different URL's
  content; fixed in the current script).
- **Raw log**: `eval/tmp_lb_monitor/snapshots.log` — greppable, append-only,
  usable directly ahead of this document being refreshed.
- **What would trigger an immediate update to this document**: AMDA's
  `checked` timestamp advancing past `Jul 10, 10:35 UTC` (the re-check
  landing — report this immediately, whatever the result); the Qualified
  table rendering (replaces all of §2/§4's modeled figures with real ones);
  any entry vanishing from a previously-seen qualified position (DQ signal);
  any new sub-1,000-token entry appearing.

---

## Sources

- This pass's own fetches: WebFetch + curl on
  `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`,
  2026-07-11 13:44–13:46 UTC (2 independent pulls); WebSearch ×3 (tie-break/
  DQ announcement, deadline extension, `AIatAMD` tweet content).
- `research/endgame_mechanics.md` (2026-07-11 ~13:10 UTC pass).
- `research/win_conditions.md` (2026-07-10 evening pass — Participant Guide
  quotes, §3.5 leaderboard-visibility finding, §4 win-probability math).
- `research/top5_forensics.md` (2026-07-10 evening — rtq-smart-router code
  audit).
- `research/leaderboard_gate_forensics.md` (2026-07-09 — full 8-qualified/
  71-DNQ table, gate triangulation).
- `research/final_gate_projection.md` (2026-07-11 evening — measured P(gate)
  for the shipped image).
- `research/token_thrift_audit.md` (2026-07-11 — remote-call token overhead
  analysis, used for the field-floor plausibility argument in §4.1.4).
- `research/VERDICTS.md` V25 (organizer Discord clarifications, tie-break
  TBD, gate triangulation cross-check).
- `eval/tmp_lb_monitor/snapshots.log` (this pass's own raw archive, ongoing).
