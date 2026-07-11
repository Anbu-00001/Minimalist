# Endgame mechanics — live leaderboard status + post-close rules, 2026-07-11 ~13:10 UTC (~18:40 IST)

Deadline: **16:00 UTC / 21:30 IST today** — **~2h50m remaining** at time of writing.
Research-only pass. Every claim below is tagged **PRIMARY** (directly fetched/quoted
this pass) or **UNVERIFIED**. Confidence noted where it matters.

---

## THE RECIPE (put this at the top on purpose — poll this yourself)

```
WebFetch: https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live
```

Direct fetch of `lablab.ai` is Cloudflare-blocked; the `r.jina.ai/<full-url>` reader-proxy
prefix works and returned live content **five separate times** in this pass (13:05–13:10
UTC), so it is reliable right now. Practical notes on using it:

- **The word "Qualified" does not currently appear anywhere in the fetched content**
  (confirmed by an explicit literal-string search this pass). Today's fetch surfaces only
  the **"couldn't be scored yet" (did-not-qualify / unresolved) list — ~203 entries** — no
  aggregate Participants/Teams/Submissions header and no ranked Qualified table rendered,
  in 3 separate attempts with different prompts. This differs from the 2026-07-09 pass
  (`leaderboard_gate_forensics.md`), which *did* get a full Qualified table, and roughly
  matches `win_conditions.md` §3.5's 2026-07-10-evening finding that the qualified/
  aggregate view had already gone missing via this method. **We have no current visibility
  into who's qualified today, field size, or the token/accuracy of the current top-10** —
  don't trust the "42 qualified" Jul-10-evening figure as current; it was operator-reported
  and even that pass couldn't independently re-verify it via this same fetch method.
- Each did-not-qualify row **carries its own `checked` timestamp**, distinct from
  `first submitted` / `last resubmitted`. This is the field to poll to know if a re-score
  has actually landed — do not infer a re-score from `last resubmitted` alone.
- Ask the fetch prompt to search for a literal team name/string and quote the surrounding
  block verbatim — broad "summarize the leaderboard" prompts tend to drop or garble the
  specific row you need.

---

## 1. AMDA's live status right now — PRIMARY, confirmed twice ~4 min apart (13:06 and 13:10 UTC)

Verbatim, from the raw fetched markdown (this is literally the first entry on the page):

> "AMDA — Verify Before You Pay ACCURACY_GATE_FAILED
> Your agent ran but didn't reach the minimum accuracy threshold. Improve correctness,
> then re-push your image and re-save your submission.
> 78.9% first submitted Jul 9, 15:51 UTC last resubmitted Jul 11, 13:02 UTC checked
> Jul 10, 10:35 UTC"

**The load-bearing fact: `checked Jul 10, 10:35 UTC` predates every fix in this repo's
git history**, not just today's — checked at 10:35 UTC:
- `checked Jul 10, 10:35 UTC` is **before** the first accuracy-tilt commits `3724d6b`/
  `574892a` (2026-07-10 20:47–20:54 IST = **15:17–15:24 UTC**, i.e. ~5h *after* this check).
- It is also before `77d9c58` "Summarisation remote-first" (2026-07-11 10:00:22 IST =
  **04:30:22 UTC**) and this session's own `f4d5353` "Add remote retry fallback"
  (2026-07-11 18:28:30 IST = **12:58:30 UTC**), which landed while this research was
  running (git status was clean of the earlier `M agent/router.py`/`M agent/verifiers.py`
  by the time this check ran — confirmed via `git log`).

**Conclusion: the 78.9% shown right now is the ORIGINAL, pre-any-fix score.** None of
V25's accuracy-tilt work, the summarisation remote-first change, or the remote-retry-
fallback change has been reflected in any real leaderboard check yet, as of 13:10 UTC.

**`last resubmitted Jul 11, 13:02 UTC`** is a stable, repeatable absolute timestamp (not a
"3 minutes ago" artifact — confirmed unchanged across two fetches 4 minutes apart) and
lands almost exactly 3.5 minutes after `f4d5353`'s commit time (12:58:30 UTC) — consistent
with a build+push+resave cycle right after that commit. **This is circumstantial, not
directly confirmed** — this pass has no access to GHCR/docker credentials to independently
verify the push landed; re-run `docker manifest inspect ghcr.io/anbu-00001/amda-agent:latest`
per `research/submission_preflight.md`'s checklist before trusting the push completed.

**Is the recheck pipeline alive today at all? Yes, for other entries** — captured in the
same pass, other DNQ rows show `Jul 11` checked timestamps, some very recent relative to
fetch time:
- "AMD Hybrid Token-Efficient AI Agent" — checked Jul 11, 09:34 UTC
- "Mallana: AI Runtime for Autonomous Development" — checked Jul 11, 12:45 UTC
- "NanoRouter" — checked Jul 11, 12:51 UTC

So the platform **is** actively re-checking DNQ entries today, including within the last
~20 minutes of fetch time for some teams — AMDA's `checked` timestamp simply hasn't
advanced past Jul 10 yet as of 13:10 UTC. Two live possibilities, not resolved: (a) queue
lag — AMDA's 13:02 UTC resubmit is recent and simply hasn't reached the front of a queue
now carrying ~203 unresolved entries (up from 71 on Jul 9), or (b) the resubmit didn't
fully register (e.g. image not yet pullable) and never entered the queue. **Action: poll
the recipe above every 10–15 min and watch specifically for AMDA's `checked` field to move
past `Jul 10, 10:35 UTC`** — that's the signal a real score exists for any of today's fixes.

---

## 2. Post-close mechanics — still UNVERIFIED, unchanged from yesterday's audit despite a fresh check

Re-checked this pass, no new primary source found beyond what `research/win_conditions.md`
(written 2026-07-10 evening) already established:

- **Re-fetched `lablab.ai/hackathon-rules` directly this pass**: explicitly does **not**
  address (1) what happens to submissions after the deadline, (2) whether the final
  re-scoring run uses whatever image tag is live at execution time vs. a snapshot taken at
  the deadline instant, (3) tie-breaking for equal scores, or (4) whether DNQ-at-close
  entries are included in the final refreshed-prompt run. Only new thing found: "Manual
  submission is available for 6 hours post-hackathon for those with valid reasons and
  **prior approval from organizers or mentors**" (matches yesterday's finding, not a
  routine lever).
- The organizer clarification already on record (`VERDICTS.md` V25, Discord 2026-07-10,
  not independently re-verifiable — Discord isn't fetchable by this researcher): *"final
  rankings re-run on REFRESHED randomized prompts... non-Fireworks routing gets manually
  audited and DQ'd during judging."* This says what prompts get used, **not** which
  submissions get run against them — the DNQ-at-close question specifically remains open.
- `win_conditions.md` §3.1's *"image fixes are re-scored automatically on the next run"*
  language describes the **rolling/live-phase** mechanism (confirmed still active today,
  §1 above) — there is still no statement anywhere found about whether this same
  auto-pickup applies to a push that lands in the final minutes before close, or whether
  the final run instead pulls a tag/digest frozen at 16:00 UTC.
- **No WebSearch this pass surfaced any Reddit/Discord-mirror/forum discussion of this
  question dated within the last 24h.** The informational vacuum is unchanged.

**Standing position (same as `win_conditions.md` §3.2/§6.1, re-affirmed, not newly
resolved): plan for the worse case.** Treat reaching QUALIFIED status **before 16:00 UTC**
as the binding requirement — do not assume a DNQ-at-close entry gets a second chance on the
refreshed prompt set.

---

## 3. Organizer announcements in the last 24h — none found

- Re-searched for deadline extensions, scoring-cadence changes, tie-break decisions, and
  DQ/audit actions. Nothing new surfaced beyond what's already in `VERDICTS.md` V25 /
  `win_conditions.md`.
- The one candidate primary source outside lablab.ai — an AMD/Fireworks-affiliated tweet
  ("BUT WAIT! It is not over! AMD Developer Hackathon: Act II...", `x.com/AIatAMD/status/
  2070526900951232841`) — is **still unreachable**: direct WebFetch returned HTTP 403 this
  pass (x.com blocks non-browser fetches outright; the earlier `r.jina.ai` proxy attempt in
  `competitors_lablab.md` hit an AbuseAlleviationError on the same domain). Content remains
  **UNVERIFIED**, known only from a WebSearch snippet, unchanged from prior passes.
- No lablab.ai banner/alert text about deadline or closing was found on the `/live` page
  in today's fetches (explicitly checked and absent, §1's third fetch).

---

## What this means for the next ~2h45m (until 16:00 UTC)

1. **Poll the recipe above every 10–15 min.** The single fact that matters is whether
   AMDA's `checked` timestamp advances past `Jul 10, 10:35 UTC`. Until it does, we have
   *zero* real signal on any fix shipped since then — not V25's tilt, not the summarisation
   change, not this session's remote-retry-fallback commit (`f4d5353`).
2. **Independently confirm the `f4d5353` image actually pushed and is publicly pullable**
   (`docker manifest inspect ghcr.io/anbu-00001/amda-agent:latest`, then a clean-cache
   `docker pull`) — `research/submission_preflight.md` previously caught this exact tag
   silently failing to resolve on the registry. The 13:02 UTC "last resubmitted" timestamp
   is consistent with a push having happened but is not itself proof it succeeded.
3. **Don't wait passively on this cycle's result before preparing the next fix**, if one is
   ready — the recheck queue is currently carrying ~203 unresolved entries and today's
   observed lag for other teams (checks landing ~15–20 min after presumed resubmit, based
   on Mallana/NanoRouter's timestamps) is a floor, not a ceiling, and AMDA's own resubmit
   has already waited 8+ min with no check yet as of 13:10 UTC.
4. **No visibility into the current qualified field** (top-10 tokens/accuracy) via this
   method today — don't plan against the stale "42 qualified" Jul-10-evening figure as if
   it's current; it wasn't independently re-verified even at the time.
5. **Post-close mechanics are still an open, unresolved risk** (§2) — the only lever this
   changes is urgency: there is no confirmed safety net for reaching QUALIFIED after
   16:00 UTC, so the 10-per-hour submission-rate-limit budget between now and close should
   be spent getting a **confirmed** ≥16/19 check to land before the deadline, not saved.

## Sources (all fetched directly this pass, 2026-07-11 ~13:05–13:12 UTC)

- `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
  — 5 fetch passes, different prompts, cross-checked.
- `https://r.jina.ai/https://lablab.ai/hackathon-rules` — 1 fetch pass, re-checked for
  post-close/tie-break/DNQ-survival language.
- `https://r.jina.ai/https://x.com/AIatAMD/status/2070526900951232841` — HTTP 403, still
  unreachable.
- WebSearch: `lablab.ai AMD Developer Hackathon Act II Track 1 deadline extension
  announcement`; `"AMD Developer Hackathon" Act II Discord announcement disqualification
  OR audit OR "final ranking" July 2026`; `AMD hackathon lablab "Track 1" leaderboard
  site:reddit.com OR site:discord.com OR forum July 11 2026` — no new results beyond
  already-known pages.
- This repo's own `git log` (5 most recent commits, ISO timestamps) — used to establish
  the fix-commit-vs-checked-timestamp ordering in §1.
- Read for context, not re-fetched: `research/leaderboard_gate_forensics.md`,
  `research/win_conditions.md`, `research/VERDICTS.md` (V25), `research/submission_preflight.md`.
