# Endgame leaderboard state — Track 1, live snapshot 2026-07-12 ~17:20 UTC

Research-only pass, read-only, nothing published or contacted. Deadline for
submissions: 2026-07-12 22:00 UTC — this snapshot is ~4h40m before that
deadline.

## 0. Fetch log — what worked, what didn't

**[DIRECTLY OBSERVED]** The plain mirror trick that has "worked all week"
(`curl -s https://r.jina.ai/https://lablab.ai/.../live`, no extra headers)
returned only the **"Did not qualify" (technical-failure) section** of the
page — 240 error-status entries (`ACCURACY_GATE_FAILED`, `PULL_ERROR`,
`TIMEOUT`, `INFRA_ERROR`, etc.), with no ranked/scored table, no token
counts, no rank numbers. Confirmed reproducible 3x (identical 1,686-line
output each time). This matches the task brief's warning that "the ranked
table sometimes doesn't render."

**[DIRECTLY OBSERVED]** Adding `?track=1` to the same URL made no
difference (identical 1,686-line output).

**[DIRECTLY OBSERVED]** The fix: adding the header `-H "x-respond-with:
markdown"` to the same `r.jina.ai` request **did** return the full page,
including the "Automated Scoring Leaderboard" (ranks 1–69) above the
did-not-qualify section. This header is the one new ingredient vs. the
"trick that worked all week" — worth carrying forward for future fetches
if the plain version starts failing again.

**[DIRECTLY OBSERVED]** `https://r.jina.ai/https://lablab.ai/event/amd-developer-hackathon-act-ii`
(the base event page, plain, no special header) rendered fully in one shot
— used for the rules/judging-criteria text in §3.

Both fetches reflect a page timestamped **"Live · Submissions open updated
17:16"** / **"Last score: 17:14 UTC · Leaderboard refreshes in: 1m 46s"** —
i.e. the data below is current as of ~17:14–17:16 UTC on 2026-07-12,
essentially "now."

---

## 1. Full ranked table — Track 1 "Automated Scoring Leaderboard" (all 69 scored entries)

**[DIRECTLY OBSERVED]**. Header text on the page reads: *"Fewest tokens
wins · subject to an accuracy gate · Last score: 17:14 UTC"*. Header counts:
**T1 · General-Purpose AI Agent: 69** scored entries (matches row count
below exactly), T2 · Video Captioning: 67, T3 · Unicorn: 341.

| Rank | Submission title | Team | Tokens | Accuracy | First submitted | Last resubmitted | Scored |
|---|---|---|---|---|---|---|---|
| 1 | Metis | Kingdom of Science | 0 | 84.2% | Jul 8, 13:07 | Jul 12, 16:48 | Jul 12, 04:29 |
| 2 | LeAgent | leMinou | 0 | 94.7% | Jul 8, 14:30 | Jul 12, 05:29 | Jul 12, 07:03 |
| 3 | optimus-router | Solvent Labs | 0 | 63.2% | Jul 9, 02:27 | Jul 12, 11:20 | Jul 12, 12:06 |
| 4 | TERA-v2 | Brute Force | 0 | 89.5% | Jul 7, 20:47 | Jul 12, 16:44 | Jul 12, 15:17 |
| 5 | NidraRoute | Nidra | 0 | 100.0% | Jul 9, 12:43 | Jul 12, 16:31 | Jul 12, 16:32 |
| 6 | ZeroFire — Zero-Token Local-First Routing Agent | PizzaDiet&ColdWater Enterprise | 0 | 52.6% | Jul 10, 21:28 | Jul 12, 16:43 | Jul 12, 16:52 |
| 7 | Velora | 6-7 | 0 | 52.6% | Jul 11, 11:10 | Jul 12, 15:58 | Jul 12, 16:47 |
| 8 | yassai | Solo Stack | 0 | 84.2% | Jul 8, 23:10 | Jul 11, 20:14 | Jul 11, 22:05 |
| 9 | OyeHoye Zero Tokens | oyehoye | 0 | 89.5% | Jul 9, 18:23 | Jul 12, 16:37 | Jul 12, 16:28 |
| 10 | Kartik | Kartik Bhalala | 1,562 | 78.9% | Jul 8, 00:30 | Jul 12, 16:45 | Jul 12, 16:26 |
| 11 | LLM-Router-Agent-qwenv4 | Dolpinotik | 2,246 | 63.2% | Jul 8, 21:07 | Jul 12, 16:29 | Jul 12, 16:17 |
| 12 | HybridRoute | LLM Learner | 2,284 | 94.7% | Jul 10, 18:20 | Jul 12, 15:35 | Jul 12, 16:26 |
| 13 | Cascade Router: Local-First AI Agent | OneNode | 2,765 | 78.9% | Jul 11, 15:44 | Jul 12, 11:28 | Jul 12, 15:40 |
| 14 | Tokomera: Adaptive Query Router | Konglomera | 2,865 | 78.9% | Jul 9, 19:07 | Jul 12, 15:01 | Jul 12, 15:24 |
| 15 | riyadomf submission 2 | AdversaryAI | 2,897 | 89.5% | Jul 11, 06:26 | Jul 12, 14:59 | Jul 12, 15:22 |
| 16 | Token-Miser Router Agent v9 | ritwika | 3,086 | 78.9% | Jul 10, 15:48 | Jul 11, 15:57 | Jul 11, 17:14 |
| 17 | Bastion: Accuracy-First Token Router V22 | Night Lab | 3,094 | 78.9% | Jul 8, 20:54 | Jul 12, 12:21 | Jul 12, 13:01 |
| 18 | OmniEdge RouteIQ — Local-First Intelligent Router | OmniEdge RouteIQ | 3,100 | 94.7% | Jul 10, 11:29 | Jul 12, 17:06 | Jul 12, 16:07 |
| 19 | AIchemist-agent-v4 | AIchemists | 3,254 | 84.2% | Jul 6, 17:47 | Jul 12, 16:56 | Jul 12, 16:43 |
| 20 | Divine agent track 2 | Divine | 3,308 | 84.2% | Jul 8, 13:33 | Jul 12, 14:41 | Jul 11, 17:54 |
| 21 | TokenMiser | minimalist | 3,408 | 94.7% | Jul 9, 18:00 | Jul 12, 12:06 | Jul 12, 12:29 |
| 22 | Beroute | Berking | 3,680 | 78.9% | Jul 11, 03:14 | Jul 11, 16:55 | Jul 11, 17:51 |
| 23 | LocalFirst-4 | jae | 3,753 | 100.0% | Jul 9, 10:08 | Jul 10, 20:41 | Jul 10, 09:13 |
| 24 | BudgetBrain Track 1 Champion Agent | Silver linings | 3,866 | 89.5% | Jul 11, 01:32 | Jul 12, 15:22 | Jul 12, 15:27 |
| 25 | DonieleTheLastAgent | cracking-doniele | 4,045 | 94.7% | Jul 9, 16:11 | Jul 12, 08:02 | Jul 12, 09:33 |
| 26 | SXR Routing Agent | SXR | 4,150 | 89.5% | Jul 8, 22:23 | Jul 12, 10:48 | Jul 12, 11:32 |
| 27 | Token Broker | Indie G | 4,567 | 73.7% | Jul 10, 22:05 | Jul 12, 17:00 | Jul 12, 16:50 |
| 28 | singleThreaded-agent16 | SingleThreaded | 4,652 | 89.5% | Jul 9, 11:16 | Jul 12, 06:48 | Jul 12, 08:42 |
| 29 | Apollo | Trafalgar | 4,676 | 78.9% | Jul 11, 14:34 | Jul 12, 16:17 | Jul 12, 15:32 |
| 30 | ZaynDev — Token-Efficient General-Purpose Agent | ZaynDev | 4,785 | 94.7% | Jul 11, 15:04 (submitted only) | — | Jul 11, 19:05 |
| 31 | CascadeRouter — Token-Efficient Routing Agent | Veritas | 4,871 | 57.9% | Jul 10, 22:40 (submitted only) | — | Jul 11, 17:40 |
| 32 | FrugalRouter | TechMavericks | 5,028 | 52.6% | Jul 11, 09:13 | Jul 12, 16:55 | Jul 12, 13:11 |
| 33 | Hybrid Token Efficient Routing - V9 | EpigenAI | 5,123 | 84.2% | Jul 9, 00:54 | Jul 12, 07:51 | Jul 12, 09:25 |
| 34 | TranscendiantRouter5 | Transcendiant | 5,140 | 84.2% | Jul 8, 14:58 | Jul 12, 15:47 | Jul 12, 16:36 |
| 35 | TokenForge Router | OG_Mode | 5,287 | 89.5% | Jul 8, 20:44 | Jul 9, 10:46 | Jul 10, 02:56 |
| 36 | AMD-Track1-Agent | yohanesfc | 5,318 | 89.5% | Jul 10, 11:42 | Jul 11, 12:09 | Jul 11, 12:31 |
| 37 | NovaAI General Purpose AI Assistant | Khdamin btkhbya | 5,319 | 89.5% | Jul 8, 23:22 (submitted only) | — | Jul 10, 02:52 |
| 38 | RLSym - Local-First Token Routing | RLSym | 5,396 | 94.7% | Jul 7, 09:33 | Jul 12, 16:50 | Jul 12, 09:38 |
| 39 | Hola Precision Agent | Hola | 5,457 | 84.2% | Jul 9, 20:11 | Jul 11, 16:27 | Jul 11, 17:24 |
| 40 | TokenOptimizer — Hybrid Routing System11 | Yashasvi Thakur | 5,494 | 89.5% | Jul 10, 12:26 | Jul 12, 16:13 | Jul 12, 17:08 |
| 41 | Verification-Driven Token-Efficient Routing Agent | Momentum | 5,735 | 100.0% | Jul 9, 06:57 | Jul 10, 21:09 | Jul 11, 17:09 |
| 42 | RepoREpo | Ryzen | 5,788 | 89.5% | Jul 8, 17:18 | Jul 12, 17:09 | Jul 11, 09:25 |
| 43 | BenchSieve | MYSELF | 5,895 | 89.5% | Jul 10, 10:55 | Jul 12, 16:07 | Jul 12, 16:58 |
| 44 | Ascended v.51 | Ascended | 5,911 | 78.9% | Jul 8, 12:22 | Jul 12, 16:33 | Jul 12, 14:30 |
| 45 | 333 TokenTriage Agent | Lyceum | 5,960 | 78.9% | Jul 9, 15:00 | Jul 12, 12:02 | Jul 12, 12:26 |
| 46 | OptiRoute | Slicon Spark | 5,963 | 94.7% | Jul 9, 13:57 | Jul 12, 16:20 | Jul 12, 16:17 |
| 47 | TokenRouter: Cost-Efficient Multi-Model AI Agent | Saving Money | 6,315 | 89.5% | Jul 9, 14:33 | Jul 11, 06:31 | Jul 11, 07:45 |
| 48 | Intelligent Assistant | OP_devs | 6,650 | 52.6% | Jul 12, 13:13 (submitted only) | — | Jul 12, 14:13 |
| **49** | **AMDA — Verify Before You Pay** | **16Bit** | **7,460** | **84.2%** | **Jul 9, 15:51** | **Jul 12, 10:28** | **Jul 12, 12:32** |
| 50 | Project HEPHAESTUS | TokenSaver | 7,607 | 73.7% | Jul 11, 07:41 (submitted only) | — | Jul 11, 17:48 |
| 51 | TERA: Hybrid Token-Efficient Routing Agent | Kshipra | 7,748 | 89.5% | Jul 10, 18:57 | Jul 11, 11:23 | Jul 11, 12:04 |
| 52 | ZMLC+ Local-First Token Router v27-final | RTHack | 7,772 | 68.4% | Jul 9, 09:28 | Jul 12, 15:54 | Jul 12, 16:45 |
| 53 | ROUgentX | Code da Clouds | 7,921 | 78.9% | Jul 10, 15:11 | Jul 12, 15:23 | Jul 12, 16:07 |
| 54 | Vote First, Then Answer | Proxgate | 8,180 | 84.2% | Jul 9, 13:12 | Jul 10, 07:06 | Jul 10, 09:54 |
| 55 | Mybanana ai agent 🍌 | MY Banana | 8,467 | 84.2% | Jul 9, 15:27 | Jul 12, 12:06 | Jul 12, 12:45 |
| 56 | HopRouter: Smart Local/Remote AI Router | HopRouter | 8,615 | 89.5% | Jul 9, 18:50 | Jul 12, 02:59 | Jul 12, 04:31 |
| 57 | ByteRoute | ByteRoute | 8,703 | 84.2% | Jul 10, 00:01 | Jul 11, 21:01 | Jul 12, 00:01 |
| 58 | AstraRoute AI Agent #10 | choatic_team | 8,842 | 89.5% | Jul 9, 20:18 | Jul 12, 16:47 | Jul 12, 13:21 |
| 59 | TokenRouter: cheapest model that gets it right | Saberites | 9,816 | 94.7% | Jul 9, 19:36 | Jul 11, 13:29 | Jul 11, 14:01 |
| 60 | KORA - Token-Efficient Routing Agent | Krako Labs - KORA | 10,310 | 94.7% | Jul 8, 09:40 | Jul 12, 12:26 | Jul 12, 13:03 |
| 61 | Valid Route Hybrid Agent | Cognivox | 10,382 | 68.4% | Jul 12, 15:03 (submitted only) | — | Jul 12, 15:28 |
| 62 | Eco Router AI | Team Skem | 10,903 | 84.2% | Jul 9, 10:14 | Jul 11, 09:47 | Jul 11, 11:17 |
| 63 | Hackathon Agent using Fireworks AI | Pai 1 | 11,021 | 89.5% | Jul 10, 21:23 | Jul 11, 20:59 | Jul 11, 22:28 |
| 64 | ApexFlow AI: Self-Healing Telemetry Gateway (YOLOAI_v15 image) | Tarek Clarke | 11,264 | 94.7% | Jul 11, 15:41 | Jul 12, 16:23 | Jul 12, 04:33 |
| 65 | THRIFT | Vyala_dev01 | 13,415 | 68.4% | Jul 11, 15:37 | Jul 12, 16:32 | Jul 12, 15:15 |
| 66 | router-track1 | EvolutionRouting | 13,922 | 100.0% | Jul 8, 13:30 | Jul 11, 18:53 | Jul 11, 20:01 |
| 67 | TokenForge — Hybrid Token-Efficient Routing Agent | Multimodal TokenForge | 14,032 | 100.0% | Jul 7, 20:22 | Jul 11, 17:50 | Jul 11, 21:23 |
| 68 | OmniSolve | Mjolnir | 14,181 | 100.0% | Jul 7, 12:33 | Jul 7, 16:08 | Jul 10, 07:34 |
| 69 | A Things That Works v4 | Code Vibing | 68,576 | 100.0% | Jul 11, 04:19 | Jul 12, 12:45 | Jul 12, 13:19 |

**[DIRECTLY OBSERVED]** This is the complete ranked table — rank 69 is the
last row before the page transitions to "Did not qualify 239."

**[DIRECTLY OBSERVED] Ranks 1–6, never seen before**: Metis (0/84.2%),
LeAgent (0/94.7%), optimus-router (0/63.2%), TERA-v2 (0/89.5%), NidraRoute
(0/100.0%), ZeroFire (0/52.6%). All six are 0-token entries; none is at
100% except NidraRoute, and the single 100.0%-accuracy 0-token entry
(NidraRoute) is rank 5, not rank 1.

**[DIRECTLY OBSERVED] Our own position**: AMDA — "AMDA — Verify Before You
Pay" (team "16Bit") is currently **rank 49 at 7,460 tokens / 84.2%
accuracy**, scored Jul 12, 12:32 UTC, last resubmitted Jul 12, 10:28 UTC.
This differs from the task brief's assumed "~rank 55 at 8,282 tokens /
89.5% accuracy" — both the token count and the accuracy have moved since
that figure was recorded, evidently from a resubmission/rescoring that
landed between the brief's snapshot and now. **Flagging this back to the
team as the single most important line in this document**: whatever is
live right now scores 7,460 tokens at 84.2%, not 8,282/89.5%.

---

## 2. The "Did not qualify" section — 239 entries

**[DIRECTLY OBSERVED]** Status breakdown (239 total, matches the page's own
"Did not qualify 239" count exactly):

| Status | Count |
|---|---|
| PULL_ERROR | 69 |
| ACCURACY_GATE_FAILED | 64 |
| INFRA_ERROR | 53 |
| TIMEOUT | 31 |
| OUTPUT_MISSING | 8 |
| RUNTIME_ERROR | 8 |
| MISSING_TASKS | 3 |
| INVALID_RESULTS_SCHEMA | 2 |
| OUTPUT_MALFORMED | 2 |

**[DIRECTLY OBSERVED]** This is a "couldn't be scored" bucket, not a "scored
but below gate" bucket in the pure sense — it lumps genuine accuracy-gate
failures in with technical failures (bad Docker image, timeout, malformed
output, etc.). Only the `ACCURACY_GATE_FAILED` subset (64 of 239) reflects
an actual accuracy judgment; the other 175 never got scored at all for
unrelated reasons.

---

## 3. Ranking function — what the evidence actually shows

### 3.1 Is the 84.2% accuracy gate real, and is it applied to the ranked list?

**[INFERRED — high confidence]** The **ranked leaderboard is NOT filtered at
84.2% (16/19)**. The lowest accuracy in the scored/ranked table (rows
1–69 above) is **52.6% (10/19)** — five separate entries sit at exactly
52.6%: ZeroFire (rank 6), Velora (rank 7), FrugalRouter (rank 32),
Intelligent Assistant (rank 48). CascadeRouter (rank 31) sits at 57.9%
(11/19), also well under 84.2%.

**[DIRECTLY OBSERVED]** Cross-checking the "Did not qualify" bucket: every
`ACCURACY_GATE_FAILED` entry sampled there tops out at **47.4% (9/19)** —
the highest score seen among 64 gate-failed entries. No gate-failed entry
was found above 47.4%.

**[INFERRED — high confidence]** Given the ranked table's floor is 52.6%
(10/19) and the did-not-qualify ceiling is 47.4% (9/19), **the real
accuracy gate sits exactly between 9/19 and 10/19 — i.e. it is
approximately 50%, not 84.2%.** This directly contradicts this repo's own
prior forensics (`leaderboard_gate_forensics.md`, `leaderboard_win_odds.md`,
`ban_wave_analysis.md`), which triangulated 84.2% from a 2026-07-09
snapshot where the *visible* qualified rows all happened to cluster at
84.2%+ — that snapshot simply hadn't yet seen any of today's low-accuracy,
zero-token entries (Velora, ZeroFire, optimus-router, etc.), because they
either didn't exist yet or hadn't been resubmitted/rescored yet. The 84.2%
figure was an artifact of a small, high-accuracy-biased sample, not the
actual gate. **The anomaly flagged in the task brief (Velora/Kartik/qwenv4
ranking above or near "gate-passing" entries despite sub-84.2% accuracy) is
now explained: there never was an 84.2% gate on the live board. There is a
much lower one, ~50%.**

**[UNVERIFIABLE]** Whether ~50% is the *exact*, *final*, judging-locked
threshold, or whether the effective gate could still move before 22:00 UTC
(e.g. a stricter bar applied only at final scoring, separate from the live
board), is not something the page states in numeric terms anywhere. The
official Track 1 rules text (event page) says only: *"deciding in real time
which Fireworks AI model is the cheapest one that can still answer
accurately... without falling below the accuracy threshold"* — no number
given. Several *other teams'* own submission descriptions (self-reported,
unverified, not authoritative) claim "80% accuracy gate" (e.g. "smash the
80% accuracy gate," "Clears the 80% accuracy gate at 34% fewer remote
tokens") — this 80% folk belief among competitors does not match either the
84.2% this repo previously inferred or the ~50% this snapshot now shows.
Treat the "gate value" as **genuinely unresolved between community folklore
(~80%), this repo's prior inference (84.2%), and today's direct
observation (~50%, i.e. between 47.4% and 52.6%)** — the direct observation
should be weighted highest since it's the freshest and most complete data,
but it is not a numerically-stated rule.

### 3.2 "Review" status

**[DIRECTLY OBSERVED]** Footer text on the /live page states: *"Scores are
produced by the AMD automated judging system. Entries marked 'Review' are
ranked but held pending manual review before any prize decision."* No row
in either the 69-row ranked table or the 239-row did-not-qualify list
carried a visible "Review" label in this fetch. **[UNVERIFIABLE]** whether
any currently-ranked entry is silently in this state (the label, if
applied, wasn't rendered in the markdown extraction, or none currently
qualifies for it).

### 3.3 Tie-break order among the nine 0-token entries (ranks 1–9)

**[DIRECTLY OBSERVED]** Ranks 1–9, all at exactly 0 tokens:

| Rank | Accuracy | Scored (UTC) | First submitted |
|---|---|---|---|
| 1 Metis | 84.2% | Jul 12, 04:29 | Jul 8, 13:07 |
| 2 LeAgent | 94.7% | Jul 12, 07:03 | Jul 8, 14:30 |
| 3 optimus-router | 63.2% | Jul 12, 12:06 | Jul 9, 02:27 |
| 4 TERA-v2 | 89.5% | Jul 12, 15:17 | Jul 7, 20:47 |
| 5 NidraRoute | 100.0% | Jul 12, 16:32 | Jul 9, 12:43 |
| 6 ZeroFire | 52.6% | Jul 12, 16:52 | Jul 10, 21:28 |
| 7 Velora | 52.6% | Jul 12, 16:47 | Jul 11, 11:10 |
| 8 yassai | 84.2% | Jul 11, 22:05 | Jul 8, 23:10 |
| 9 OyeHoye | 89.5% | Jul 12, 16:28 | Jul 9, 18:23 |

**[INFERRED]** None of the obvious candidate sort keys explain this order:
- **Not accuracy-descending**: NidraRoute (100.0%) is rank 5, below LeAgent
  (94.7%, rank 2) *and* below TERA-v2 (89.5%, rank 4) *and* below Metis
  (84.2%, rank 1).
- **Not scored-time-ascending**: Metis (rank 1) scored 04:29, but rank 8
  (yassai) scored a full day earlier (Jul 11, 22:05) and rank 6/7
  (ZeroFire/Velora) scored latest of all (16:47–16:52) yet sit above rank
  10+.
- **Not first-submitted-time-ascending**: TERA-v2 (Jul 7, 20:47, earliest
  of the nine) is rank 4, not rank 1; Metis (Jul 8, 13:07) is rank 1
  despite three other entries having earlier first-submission timestamps.
- **Not last-resubmitted-time**: no monotonic pattern either.

**[UNVERIFIABLE]** The tie-break rule among 0-token entries is not
disclosed anywhere on the page and could not be reverse-engineered from
this snapshot. Most likely candidate not tested here: internal database
row ID / insertion order (would require a second snapshot capturing the
insertion sequence to confirm) — flagging as the leading hypothesis but
unconfirmed.

---

## 4. Zero-token club — size and accuracies

**[DIRECTLY OBSERVED]** **9 entries** show exactly 0 tokens (ranks 1–9).
Rank 10 (Kartik) is the first positive-token entry at 1,562 tokens — a
**large gap** between the 0-token cohort and the next tier (nothing between
0 and 1,562 tokens). Accuracies within the 0-token club range from 52.6%
(ZeroFire, Velora) up to 100.0% (NidraRoute), spanning the full width of
possible k/19 outcomes above the ~50% floor: {52.6%, 63.2%, 84.2%, 84.2%,
89.5%, 89.5%, 94.7%, 100.0%} plus the two 52.6%s = 9 values total.

---

## 5. Churn vs. prior repo snapshots — evidence of disqualification, removal, or degradation

Compared against `top5_forensics.md`, `leaderboard_win_odds.md`,
`leaderboard_gate_forensics.md`, and `ban_wave_analysis.md`.

### 5.1 `rtq-smart-router` (team `rusetiq`) — confirmed still removed

**[DIRECTLY OBSERVED]** `ban_wave_analysis.md` (2026-07-11 ~18:10 UTC)
documented this entry — Jul-10-evening rank 1 at 0 tokens / 100.0%,
code-verified as an undisclosed non-Fireworks Gemini call — vanishing with
its submission page returning 404. **This snapshot (2026-07-12 17:20 UTC)
confirms it is still absent**: not in the 69-row ranked table, not in the
239-row did-not-qualify list, no hit for "rtq" or "rusetiq" anywhere in
either fetch. The removal from ~26 hours ago has held. This remains the
only confirmed case of an entry actually disappearing from the platform
entirely (as opposed to just dropping out of view).

### 5.2 NEW finding: several previously-qualified, real-token entries have fallen into technical-failure states in just the last 1–2 hours

**[DIRECTLY OBSERVED]** Cross-referencing named entries from
`ban_wave_analysis.md` §1b / the task-brief-quoted figures against this
snapshot:

| Entry | Prior state (this repo, 07-11/07-09) | Current state (this snapshot, 07-12 ~17:20 UTC) | `checked` timestamp |
|---|---|---|---|
| Kestrel | 1,798 tok / 89.5%, qualified (`leaderboard_win_odds.md`/`ban_wave_analysis.md`) | **TIMEOUT**, in did-not-qualify bucket | Jul 12, 15:19 UTC |
| Pahfinder0 (Pathfinder0) | 1,763 tok / 84.2% cited in task-brief figures relayed via `ban_wave_analysis.md` | **INFRA_ERROR**, in did-not-qualify bucket | Jul 12, 13:50 UTC |
| Adaptive Routing Agent (team T_ying_yai) | 5,273 tok / 84.2%, qualified rank 4/8 (`leaderboard_gate_forensics.md`, 07-09) | **TIMEOUT**, in did-not-qualify bucket | Jul 12, 16:43 UTC |
| "minima" (team Tech debt / Minima) | 5,423 tok / 84.2%, qualified rank 6/8 (`leaderboard_gate_forensics.md`, 07-09) | **ACCURACY_GATE_FAILED at 36.8%**, in did-not-qualify bucket | Jul 12, 06:25 UTC |
| YOLOAI (v6→now "v15") | 2,664 tok / 84.2% cited in `ban_wave_analysis.md` as still-live | Two entries found: a **live ranked** one (rank 64, "ApexFlow AI: Self-Healing Telemetry Gateway," 11,264 tok / 94.7%, team Tarek Clarke) *and* a separate **TIMEOUT** did-not-qualify entry also titled "YOLOAI_v15" | ranked one scored Jul 12, 04:33; TIMEOUT one checked Jul 12, 15:19 |
| Route AI (Void Martial Clan), "Hybrid Token-Efficient Routing Agent" (Adam dev teams) | Qualified rank 1–2/8, `leaderboard_gate_forensics.md`, 07-09 | **Not found** in either the 69-row ranked table or (searched substring) the did-not-qualify list under these exact names | — (inconclusive; may be renamed/resubmitted under a different title, can't confirm) |

**[INFERRED]** The pattern across Kestrel / Pahfinder0 / Adaptive Routing
Agent — all `TIMEOUT` or `INFRA_ERROR`, none `ACCURACY_GATE_FAILED`, all
`checked` within the last ~1–2 hours before this snapshot (13:50–16:43
UTC), all previously *working, qualified, real-token* entries — reads much
more like **judging-proxy strain under end-of-hackathon submission load**
than a deliberate ban wave. `ACCURACY_GATE_FAILED` (a content judgment)
would be a stable, reproducible verdict; `TIMEOUT`/`INFRA_ERROR` (an infra
symptom) is exactly what you'd expect from a proxy or scoring pipeline
buckling under a last-hours crush of resubmissions (page shows "▲ +444
[submissions] today," "▲ +42 [drafts] today" — a big spike). This is
consistent with, and corroborates, this repo's own prior chaos-proxy
research (`chaos_proxy_test.md`, `cap2_ship_risks.md`) about the judging
proxy degrading under load. **No evidence of a targeted ban wave was found
in this pass** — the only confirmed deliberate removal remains
`rtq-smart-router` from over a day ago (§5.1). The "minima" case (a real
`ACCURACY_GATE_FAILED` at 36.8%, well below its old 84.2%) is more likely a
broken resubmission (someone pushed a regression) than judging drift, given
accuracy verdicts don't degrade from infra load the way timeouts do.

**[UNVERIFIABLE]** Whether Kestrel/Pahfinder0/Adaptive Routing Agent will
recover on a future re-check before the 22:00 UTC deadline, or whether
they're now locked out of scoring for the remainder of the event, cannot be
determined from a single snapshot.

### 5.3 Net qualified-field size trend

**[DIRECTLY OBSERVED]** Track 1 scored/ranked entries: 8 (07-09 ~14:08 UTC,
per `leaderboard_gate_forensics.md`) → 69 (this snapshot, 07-12 ~17:15
UTC). Did-not-qualify: 71 (07-09) → 239 (this snapshot). Both pools grew
roughly proportionally (~8–9x) over the 3-day window, consistent with the
overall submission count growth (154 → hundreds), not with a shrinking or
purged field.

---

## 6. What token target wins rank ≤ 3

**[INFERRED]** Token count of **0 is a hard prerequisite** for rank ≤ 3 (in
fact for anything above rank 10) — the gap from the 0-token cohort (ranks
1–9) to the first positive-token entry (Kartik, 1,562 tokens, rank 10) is
absolute; no non-zero token count currently beats any 0-token entry.

**[UNVERIFIABLE]** However, **0 tokens alone does not guarantee rank ≤ 3**.
Nine entries already occupy the 0-token cohort, and the tie-break order
among them (§3.3) is not accuracy, not scored-time, not submission-time —
it is unknown. A tenth 0-token, gate-passing (≥~50% accuracy) entry
arriving before 22:00 UTC has no guaranteed insertion point; it could land
anywhere within or after the existing nine depending on whatever hidden key
the board actually sorts ties on. The only observationally *safe* claim:
**reaching 0 tokens gets you into contention for rank ≤ 9 (below all
positive-token entries); reaching rank ≤ 3 specifically requires
additionally beating the tie-break order of at least 6 of the 9
already-there 0-token entries, by a mechanism this pass could not
identify.**

---

## 7. Labeled claim summary

- **[DIRECTLY OBSERVED]**: Full 69-row ranked table (§1); 239-row
  did-not-qualify status breakdown (§2); ranked-table accuracy floor of
  52.6%, did-not-qualify `ACCURACY_GATE_FAILED` ceiling of 47.4% (§3.1);
  "Review" status definition text with no rows currently marked as such
  (§3.2); 9-entry 0-token club composition (§4); `rtq-smart-router` still
  absent (§5.1); Kestrel/Pahfinder0/Adaptive Routing Agent/minima's current
  DNQ statuses and `checked` timestamps (§5.2); AMDA's own current
  rank/tokens/accuracy (§1, bolded row).
- **[INFERRED]**: true accuracy gate is ~50% (between 9/19 and 10/19), not
  84.2% as this repo previously concluded (§3.1); no tie-break key found
  among 0-token ties (§3.3); Kestrel/Pahfinder0/Adaptive-Routing-Agent
  pattern reads as proxy/infra strain, not a ban wave (§5.2); 0 tokens is
  necessary but not sufficient for rank ≤ 3 (§6).
- **[UNVERIFIABLE]**: whether ~50% is the final/locked gate value or could
  still shift before 22:00 UTC; whether any row is silently in "Review"
  status; the exact tie-break mechanism for 0-token entries; whether
  Route AI / "Adam dev teams" entry is gone or just renamed; whether
  Kestrel et al. will recover before the deadline.

---

## Sources

- `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
  with header `x-respond-with: markdown` (ranked table + did-not-qualify
  list + "Review" status footer text) — fetched 2026-07-12 ~17:20 UTC,
  page self-timestamped "Last score: 17:14 UTC."
- `https://r.jina.ai/https://lablab.ai/event/amd-developer-hackathon-act-ii`
  (plain, no header) — Track 1 official rules/judging-criteria text (§3.1),
  fetched same pass.
- This repo: `research/top5_forensics.md`, `research/leaderboard_win_odds.md`,
  `research/leaderboard_gate_forensics.md`, `research/ban_wave_analysis.md`
  — prior snapshots used for the §5 churn comparison.
