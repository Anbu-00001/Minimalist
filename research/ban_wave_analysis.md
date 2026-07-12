# Ban-wave / gate-shift analysis — 2026-07-11 ~18:10 UTC (~23:40 IST)

Scope: verify two claims relayed in the task brief — (1) a purge of entries
"around 1,750 to 0 tokens," (2) "Token-Miser Router Agent v9" QUALIFIED at
78.9% / 3,086 tokens, implying the gate moved from 16/19 to ≤15/19. **Bottom
line up front: neither claim is supported by any data source this pass could
reach. One real, concrete removal was found — but it's a single targeted DQ
(the already-known rtq-smart-router Gemini-cheat entry), not a token-range
purge — and the gate-boundary evidence directly contradicts a move to 15/19.**

---

## 0. Data-source status (read this before trusting anything below)

- **`eval/tmp_lb_monitor/snapshots.log` is thin, not "overnight."** It spans
  only **13:44:38–13:52:31 UTC on 2026-07-11** (~8 minutes of wall-clock
  time, 2 real poll cycles), not the intended overnight run. The background
  `poll_loop.sh` process is **not currently running** (confirmed via `ps
  aux` — no match), and the log has no `LOOP_STOP` marker, so it died
  silently sometime after 13:52 UTC without completing a single 48-minute
  cycle, let alone running through the night. **Per the task's own fallback
  instruction, this pass relied primarily on fresh polls (5 independent curl/
  WebFetch pulls, 13:44–18:08 UTC today) plus diffing against the three named
  prior-research files.**
- **The ranked Qualified table (token/accuracy columns) never rendered in
  any fetch this pass** — 5 fresh polls of `/live`, `/live?track=1`, and the
  base event page, plus a WebFetch pass, all confirm zero occurrences of the
  literal string "Qualified" anywhere in the returned content. This matches
  every prior research pass in this repo going back to 2026-07-10 evening
  (`leaderboard_win_odds.md`, `endgame_mechanics.md`, `top5_forensics.md` all
  independently hit the same wall). **The only time this repo ever had
  direct visibility into the Qualified table was 2026-07-09 14:08 UTC**
  (`leaderboard_gate_forensics.md`, 8/8 qualified rows). Everything about
  "who's currently qualified and at what token/accuracy" below rank 5 is
  therefore inference from DNQ-list absence and gallery-page liveness
  checks, not a direct measurement — flagged throughout.
- **The prior-state figures quoted in the task brief itself do not match
  the three cited source files.** The task brief states: "yassai
  1,377/89.5% → later 2,228; Pahfinder0 1,763/84.2%; Metis 1,797→2,138;
  Kestrel 2,520/100%; NidraRoute 0/100% → later 2,578/84.2%." Checked every
  one of these numbers against `research/leaderboard_win_odds.md`,
  `research/top5_forensics.md`, `research/endgame_mechanics.md`, and a
  full-text grep of `research/*.md`: **none of 1,377 / 1,763 / 1,797 / 2,520
  / 2,578 appears anywhere in this repo.** What the cited files actually
  record for the one real Jul-10-evening top-5 snapshot
  (`top5_forensics.md`) is: rtq-smart-router 0/100.0%, **Kestrel 1,798/
  89.5%** (not 2,520/100%), Metis 2,138/84.2% (matches the brief's "later"
  figure only), **yassai 2,228/100.0%** (matches the brief's "later" figure
  only; accuracy differs from the brief's "1,377/89.5%" first-seen claim),
  YOLOAI_v6 2,664/84.2%. Pahfinder0 is not in that top-5 at all — the one
  place it appears in this repo is `leaderboard_gate_forensics.md`
  (2026-07-09), **in the DID-NOT-QUALIFY list at 78.9% (15/19)**, the exact
  opposite of "qualified at 1,763/84.2%." **Treat the task brief's specific
  numbers as unreliable / possibly conflated with a different or
  mis-remembered screenshot; this report uses only what's independently
  verifiable.**

---

## 1. VANISHED-ENTRY LEDGER

### 1a. Confirmed real removal — the one solid finding this pass

**`rtq-smart-router` (team `rusetiq`), Jul-10-evening rank 1, 0 tok /
100.0% — its own submission page now 404s.**

```
curl -s https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/rusetiq/rtq-smart-router-submission-41
```
returns lablab.ai's own custom not-found page verbatim: *"Even AI can't find
this page. Looks like we took a wrong turn somewhere!"* (confirmed via a
fresh fetch this pass, 2026-07-11 ~18:05 UTC). The entry is also **absent
from the entire current base-event gallery page** (512KB fetch, ~1,248
listed submissions, zero hits for "rtq-smart-router" or "rusetiq") — it
isn't paginated-away, it is gone from the platform.

This is exactly the entry `research/top5_forensics.md` code-audited and
found **hardcodes a plaintext Gemini API key and unconditionally overwrites
every Fireworks answer with an undisclosed Gemini call** — a direct match
to the organizer's stated manual-audit DQ trigger. That research explicitly
recommended flagging it. **Read together: this looks like the organizer's
manual audit caught and removed exactly this one entry** — real evidence of
enforcement happening, but it is a **targeted single-entry DQ tied to a
specific, provable rules violation**, not a range-based purge. No other
entry in this entire investigation showed the same 404 signature.

### 1b. DNQ-list churn — vanished from the DID-NOT-QUALIFY view, but NOT removed from the platform

Diffing the full DNQ list at **13:51:11 UTC** (last usable capture in
`snapshots.log`, 201 parsed entries) against a fresh pull at **~18:01:48
UTC** (215 parsed entries) found **34 names present in the old DNQ list and
absent from the new one**, including several at the accuracy values the task
brief cares about: `Ascended v.31` (78.9%), `LLM-Router-Agent-noge-v4`
(78.9%), `routerx-agent` (78.9%), `TokenMiser` (INFRA_ERROR, no accuracy),
`NidraRoute` (INFRA_ERROR), `HopRouter: Smart Local/Remote AI Router`
(73.7%), `Verification-Driven Token-Efficient Routing Agent` (73.7%),
`Token Saver v1` (73.7%), `optimus-router` (57.9%), `ROUgentX` (63.2%), and
~24 more INFRA_ERROR/PULL_ERROR/TIMEOUT entries with no accuracy shown.

**Directly checked whether these are actually gone from the platform (not
just the DNQ view) — they are not.** Three spot-checks, each fetched fresh
this pass:

| Entry | Direct-URL check | Result |
|---|---|---|
| `NidraRoute` | `.../nidra/nidraroute` | **Live**, real page (`AI app: NidraRoute...`), no 404 |
| `TokenMiser` | `.../minimalist/tokenmiser` | **Live**, real page, no 404 |
| `routerx-agent` | `.../rm-rf/routerx-agent` | **Live**, real page, no 404 |

All three, plus `LLM-Router-Agent-noge-v4` and `HopRouter`, also have live
listing entries in the current base-gallery page. **None of the 34
"vanished" names show the rtq-smart-router 404 pattern.** The much more
mundane explanation, also directly visible in the same diff: this is a
fast-churning field of 200+ scrappy submissions, and teams are **renaming on
every resubmit** — the "newly appeared" side of the same diff (48 names)
contains obvious version-bumps of the "vanished" names: `A Things That
Works v1` → `v2`, `Frugal Token v6` → `v7`, `Metis - ( infra error 😍 )` →
`Metis - ( infra error 😍💔 )`, `Tokenless-11` → `Tokenless-13`, `RouterAI
v15` → `v11`, `TokenOptimizer — Hybrid Routing System4` → `System7`,
`vinci-monsoon-j4` → `j6`, `k4k Kartik` → `k4 Kartik`. A brand-new status,
**`MISSING_TASKS`**, also appeared this pass on `Token Saver v1` (was 73.7%
ACCURACY_GATE_FAILED at 13:51 UTC, is `MISSING_TASKS` at 18:01 UTC) — a
broken resubmission, self-inflicted, not an organizer action. One more new
status, **`MODEL_VIOLATION`**, appeared on a single, previously-unseen entry
(`Base42: The Cost-Aware AI Operating System`, checked 17:20 UTC) — the
organizer's audit pipeline evidently *can* and does flag specific rule
violations (consistent with §1a), but this is one new entry catching a
violation, not evidence of a sweep through the existing field.

**Verdict on "1,750 to 0 tokens purge": not confirmed, and directly
contradicted by the spot-checks.** DNQ rows never carry a token figure at
all (only accuracy, since by definition they never billed a qualifying
score), so the DNQ list cannot even be used to test a token-based
hypothesis directly — and every near-zero/low-token-profile name checked
(`NidraRoute`, `TokenMiser`, `routerx-agent`) is still alive and pullable
on the platform. **`Pahfinder0`** (the entry closest to the "1,763" figure
in the task brief) also still has a live gallery listing today (team
`pathfinder0`, placeholder "testtesttest..." description) — no vanish
signal at all, and its one hard data point in this repo (`78.9%`
ACCURACY_GATE_FAILED on 2026-07-09) contradicts the brief's "1,763/84.2%
qualified" framing outright. **`yassai`** and **`Kestrel`** (now at "v0.74,"
up from "v0.68" on Jul 10 — active, ongoing iteration) both still have live
gallery listings with no vanish signal either.

**Net read**: one real, targeted, rules-violation-driven removal
(rtq-smart-router); everything else that looked like "vanishing" this pass
is ordinary DNQ-list churn from rapid resubmission/renaming in a
200+-entry field, not a purge.

---

## 2. GATE BOUNDARY

**No direct measurement possible** — see §0, the Qualified table has not
rendered in any fetch since 2026-07-09. Everything here is inference from
what's still failing.

**Is 78.9% (15/19) really in?** The strongest evidence available says no,
and it's fairly direct: **multiple distinct entries sat at exactly 78.9% and
were still showing `ACCURACY_GATE_FAILED` in the freshest fetch this pass
(~18:01 UTC, hours after the alleged "Token-Miser qualifies at 78.9%"
observation)** — `riyadomf submission 2` (checked Jul 11, 11:50 UTC) and
`minima vx` (checked Jul 11, 03:30 UTC) both remain in DNQ at 78.9% in the
current fetch. If the gate had genuinely dropped to ≤15/19, these two
should have flipped to qualified along with everything else at that score —
they haven't. **AMDA's own pre-fix image** is the same story: `78.9%,
ACCURACY_GATE_FAILED`, unchanged since `checked Jul 10, 10:35 UTC` through
every fetch in this repo's history including this pass's.

**Are 73.7% (14/19) entries still in DNQ, bracketing the gate to (14/19,
15/19]?** No — the evidence points the other way. `73.7%` entries are
*also* still failing right alongside `78.9%` entries in the same fetch
(`Project HEPHAESTUS`, checked Jul 11 09:08 UTC, present in **both** the
13:51 and 18:01 UTC snapshots unchanged; `Tokomera: Adaptive Query Router`,
73.7%, also stable across both). Both accuracy rungs (14/19 and 15/19)
co-existing as failing, simultaneously, in the freshest data this pass could
get, is inconsistent with a gate anywhere at or below 15/19 — it's exactly
what you'd expect from the **same 16/19 gate `leaderboard_gate_forensics.md`
triangulated on 2026-07-09**, still standing.

**Token-Miser Router Agent v9 specifically**: does not appear anywhere in
either DNQ snapshot (old or new), and — because the Qualified table never
rendered — cannot be confirmed as qualified either. Its only public data
point found this pass is its **own submission-page marketing copy**
(base-gallery fetch, team `ritwika`): *"A hybrid routing agent that answers
8 task categories with near-zero Fireworks tokens... 9/9 correct on the
sample set at 627 tokens."* That is a **self-reported dev/rehearsal-set
claim** (9/9 = 100%, 627 tokens) — structurally different from, and not
corroborating, the task brief's specific "78.9% / 3,086 tokens, QUALIFIED"
figure (different accuracy, different token count, different eval context —
"sample set" vs. the hidden 19-task grader). **No source located anywhere
substantiates the claim that Token-Miser Router Agent v9 is a qualified
entry at 78.9%/3,086 tokens.**

**Conclusion**: the gate-boundary evidence gathered this pass is consistent
with the gate remaining at **≥16/19 (84.2%)**, unchanged from the
2026-07-09 triangulation. No evidence found supports a move to ≤15/19.

**The AMDA irony, confirmed as stated**: AMDA's OLD (pre-tilt) image really
did score exactly 78.9% (15/19) on Jul 10 — one task under a real 16/19
gate, but it would already clear a hypothetical 15/19 gate. That gate shift
appears not to have happened, so this is moot for us either way: the
**CURRENT** shipped image (digest `fb43f519`, HEAD `f4d5353`) measures
**17.3/19 expected, P(≥16/19) = 93.6%** per `research/final_gate_projection.md`
— it clears the real (still-16/19) gate comfortably regardless of whether
the 15/19 rumor is true. **Higher-priority operational flag, unrelated to
the gate-boundary question**: AMDA's own row is currently showing
`INFRA_ERROR` (checked Jul 11, 15:33 UTC, on a resubmit at 14:14 UTC) — the
accuracy-tilted image has **not yet actually been scored** as of this
report. That is the thing actually blocking us right now, not a gate
threshold change.

---

## 3. UPDATED WIN ODDS — AMDA at ~2,702 projected tokens

**Caveat up front**: with the Qualified table never visible this pass, this
is necessarily built from the last real measurement (`top5_forensics.md`,
Jul-10 evening) plus this pass's liveness checks — not a fresh ranked
fetch. Keep the model simple, per the task's own instruction.

### 3.1 What changed vs. `leaderboard_win_odds.md`

The prior document's Scenario (a) ("rtq-smart-router and any similar
cheat-pattern entries are caught and removed before final scoring") was
written as an **assumption to model against**. This pass **confirms it
actually happened** for rtq-smart-router specifically (§1a's 404). That is
the one concrete update: **Scenario (a) is no longer hypothetical for this
entry** — AMDA's effective rank-1 competition starts at Kestrel, not a
0-token cheat entry.

Nothing else materially updates the field-composition picture: no new
sub-1,798-token legitimate qualifier was found (Token-Miser's 627-token
figure is an unverified self-report, not a leaderboard measurement — see
§2), and every previously-known top-5 name besides rtq-smart-router is
still alive and, in Kestrel's case, actively iterating (v0.68 → v0.74).

### 3.2 The field, as best it can be reconstructed

| Entry | Tokens | Accuracy | Gate margin (vs. 84.2%/16-19 line) | Status this pass |
|---|--:|--:|--:|---|
| rtq-smart-router | 0 | 100.0% | n/a — proven cheat | **REMOVED (404 confirmed)** |
| Kestrel | 1,798 | 89.5% (17/19) | **+1 task** of slack | Live, actively iterating (now v0.74) |
| Metis | 2,138 | 84.2% (16/19) | **0 — exact knife-edge** | Live, no vanish signal |
| yassai | 2,228 | 100.0% (19/19) | **+3 tasks** of slack *(if real — repo/code unverifiable, flagged in `top5_forensics.md`)* | Live, no vanish signal |
| **AMDA (current image)** | **~2,702** | **17.3/19 expected, 93.6% P(≥16/19)** *(measured, not self-reported)* | **+1.3 tasks expected**, but distributional (not a fixed score) | Not yet scored — INFRA_ERROR on last check |
| YOLOAI_v6 | 2,664 | 84.2% (16/19) | **0 — exact knife-edge** | Not re-checked this pass; no vanish signal in the one search done |

Four names are confirmed cheaper than AMDA's ~2,702 tokens and confirmed
still live: Kestrel, Metis, yassai, YOLOAI_v6. Two of the four (Metis,
YOLOAI_v6) sit exactly on the 16/19 knife-edge — per
`leaderboard_win_odds.md` §4.1.3's binomial retention model, a knife-edge
16/19 has roughly a **coin-flip (~50%) chance of surviving a refreshed
19-task prompt set**, versus AMDA's **measured** 93.6%. Kestrel's +1-task
margin (17/19) and yassai's +3-task margin (19/19, if real) are
meaningfully safer bets to survive a refresh than a bare 16/19, and both
are also cheaper than AMDA on tokens today — they remain the two hardest
obstacles to outright rank 1.

### 3.3 P(rank 1) / P(top 3) — simple model, assumptions stated

Assumptions: (1) final ranking = qualify, then rank ascending by tokens
among qualifiers; (2) each of Kestrel/Metis/yassai/YOLOAI_v6's displayed
accuracy is i.i.d.-Bernoulli-representative of a true per-task rate, used
to estimate P(survive refreshed 16/19 gate) the same way
`leaderboard_win_odds.md` §4.1.3 did (16/19 exact ≈ 50% retention, 17/19
≈ 89%, 19/19 ≈ near-certain if the figure is real); (3) AMDA's P(gate) =
93.6% is taken as measured, not modeled; (4) no visibility below rank 5, so
an unknown number of legitimate sub-2,702-token qualifiers may exist in the
field that this pass simply cannot see — this is the single biggest source
of uncertainty and is not something the model below can correct for.

- **P(AMDA ranks below Kestrel)**: high (~85-90%) — Kestrel is cheaper
  (1,798 vs ~2,702) and its 17/19 has a materially better refresh-survival
  chance (~89%) than a coin flip, so it's the single hardest entry to pass
  on tokens *and* to hope drops out on accuracy.
- **P(AMDA ranks below yassai, conditional on yassai's 100% being real)**:
  similarly high — cheaper and an even safer margin. But this is the
  weakest-evidenced of the four (dead/404 GitHub repo, no code ever
  verified, per `top5_forensics.md` §4) — some non-trivial chance this
  figure doesn't hold up under audit or refresh, unlike Kestrel where the
  live, actively-updated GHCR image at least confirms an actual working
  artifact exists.
- **P(AMDA ranks above Metis and/or YOLOAI_v6)**: meaningfully better than
  50/50 for at least one of the two — both are on the exact knife-edge with
  ~50% modeled refresh-survival, against AMDA's measured 93.6%. This is
  the most actionable, evidence-backed part of the model: **AMDA is more
  likely than not to leapfrog at least one of the two knife-edge
  qualifiers cheaper than it today**, purely on gate robustness, even
  though it can't beat either on raw token count if both do survive.
- **P(rank 1), unconditional**: low — realistically requires both Kestrel
  and yassai to fail to hold their positions (drop out, get DQ'd, or get
  beaten some other way), which nothing in this pass's evidence suggests is
  likely. **Rough estimate: ~10-20%**, driven almost entirely by the
  yassai-repo-is-unverifiable uncertainty rather than anything newly found
  this pass. This is lower than `leaderboard_win_odds.md`'s own ~33%
  modeled figure for the ~2.7k mode — that document's number was computed
  before confirming Kestrel and yassai are both still alive and cheaper;
  this pass's field-liveness checks make the "AMDA is the cheapest safe
  qualifier" case weaker, not stronger.
- **P(top 3), unconditional**: moderate-to-good — **~55-65%**, roughly
  unchanged from `leaderboard_win_odds.md`'s own ~64% figure for this token
  mode. AMDA's measured 93.6% gate-pass is the dominant factor; it mainly
  needs one of {Metis, YOLOAI_v6} to fail their knife-edge refresh (~50%
  each, independent-ish) to clear a top-3 slot ahead of at least one
  currently-cheaper knife-edge qualifier, and there's no confirmed evidence
  of a large wave of new sub-2,702-token *safe* (non-knife-edge) qualifiers
  having appeared since Jul 10 evening.
- **Biggest unknown, stated plainly**: this model only accounts for the 4
  named entries this repo has ever had eyes on. The field grew from ~143
  total (Jul 10 evening) to 200+ DNQ-only-visible entries today, and **the
  qualified side of that growth is completely invisible to this
  investigation** — there could be new, cheaper, safely-qualified entrants
  the DNQ-list method can never surface. Nothing found this pass either
  confirms or rules that out.

### 3.4 The one thing worth doing right now, independent of any of this

**Fix the INFRA_ERROR blocking AMDA's own re-check** (§2's operational
flag). None of the win-odds math above matters until the current image
actually gets scored — right now AMDA doesn't have a real accuracy number
on the board at all, tilted or not.

---

## 4. Organizer announcements — none found

- WebSearch (2 queries: disqualification/banned-submissions language;
  accuracy-gate-threshold-change/Discord language) surfaced no primary
  source. One WebSearch response asserted *"some entries are marked
  'Review'... held pending manual review before any prize decision"* — this
  is the **same unverified search-engine-generated gloss already flagged as
  untraceable-to-source** in `research/win_conditions.md` §2.5 from a prior
  pass; it reproduced again this pass and is **not** treated as evidence of
  anything.
- Direct re-fetch of `lablab.ai/hackathon-rules` this pass: only the
  existing generic disqualification clause (*"cheating, tampering with
  systems, using unauthorized automation... the participant may be removed
  from the event"*) — the same language already on record via
  `VERDICTS.md` V25, nothing new about a gate change, ban wave, or
  tie-break rule.
- No new deadline, tie-break, or scoring-methodology announcement found
  anywhere this pass.

---

## Sources (this pass)

- `eval/tmp_lb_monitor/snapshots.log` (existing, thin — see §0) + `ps aux`
  (confirmed the background poller is not running).
- 5 fresh fetches this pass (curl + WebFetch, `r.jina.ai` proxy,
  2026-07-11 13:44–18:08 UTC): `/live` ×2 (18:01, 18:07 — near-identical,
  likely within the reader-proxy's cache window), `/live?track=1`, base
  event page, plus direct submission-page checks for `rtq-smart-router`,
  `NidraRoute`, `TokenMiser`, `routerx-agent`.
- WebSearch ×3 (ban/DQ announcement, gate-threshold-change announcement,
  "Review" status follow-up).
- `research/leaderboard_win_odds.md`, `research/top5_forensics.md`,
  `research/endgame_mechanics.md`, `research/leaderboard_gate_forensics.md`,
  `research/final_gate_projection.md`, `research/verify_local_decision.md`,
  `research/win_conditions.md` §2.5 — read for prior-state diff and cross-
  checks.
