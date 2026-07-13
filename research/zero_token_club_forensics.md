# Zero-Token Club Forensics — AMD Developer Hackathon Act II, Track 1 (2026-07-12, ~17:20-19:30 UTC)

Scope: read-only research into the cluster of 0-token / near-0-token top-rank entries
named in the task brief — Velora (52.6% acc), yassai / team Solo Stack (84.2%),
OyeHoye Zero Tokens / team oyehoye (89.5%) — following the method established in
`research/top5_forensics.md` (read first; this pass reuses and extends it). Deadline
today 2026-07-12 22:00 UTC. No contact made with organizers, teams, or third parties;
nothing published.

**Important framing carried over from the prior pass**: the `/live` leaderboard URL
does not render a token/accuracy table in a static fetch (via `r.jina.ai` or direct
curl) — as of this session it renders a long list of *unscored/errored* submissions
(96+ entries with statuses like `ACCURACY_GATE_FAILED`, `PULL_ERROR`, `TIMEOUT`,
`INFRA_ERROR`, `INVALID_RESULTS_SCHEMA`). This list is itself useful signal (see
"Graveyard" note below) but contains no ranked token/accuracy table. **We could not
independently re-derive the token/accuracy numbers in the task brief from a live
leaderboard fetch this session either** — they are taken as given, exactly as the
prior pass did for its top-5 table. Everything below the numbers themselves (repo
existence, commit history, code content, GHCR package activity) is independently
verified.

## How the three teams/projects were located

All three were found in the event's project gallery, fetched via
`r.jina.ai` mirror of `https://lablab.ai/event/amd-developer-hackathon-act-ii`
(direct fetch is Cloudflare-blocked). The gallery lists every public submission
card with its one-line pitch and team name — this is a more reliable discovery path
than slug-guessing, and confirmed team names that matched slug-probing attempts:

- **Velora** — team **6-7** — page:
  https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/6-7/velora
- **yassai** — team **Solo Stack** — page (same URL already known from prior pass,
  re-fetched and unchanged):
  https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/solo-stack/yassai
- **OyeHoye Zero Tokens** — team **oyehoye** — page:
  https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/oyehoye/oyehoye-zero-tokens

A web search also surfaced independent (LLM-summarized, unverified) confirmation
that OyeHoye appears in a "Fewest tokens wins" leaderboard view at position 6,
implying ranks 1-5 in that view hold additional 0-token entries not yet identified
by name — consistent with the task brief's "unseen ranks 1-6 likely containing more."

---

## 1. Velora (team 6-7) — 52.6% accuracy per task brief

**GitHub**: https://github.com/IrvanKurniawan624/velora — public, real, substantial,
**actively committed to as of this morning** (last commit `b27687d2`,
2026-07-12T08:14:40Z — about 9 hours before this research pass). 430 KB, dozens of
files: a real `app/` package (config, clients, schemas, services), a `benchmarks/`
suite with its own datasets, tests, and self-reported benchmark reports, `docs/`,
Docker multi-stage build. Two creators listed on the lablab page (Irvan Kurniawan /
`@iv_martabak_manis`, Ellen Yu). Default branch is **`dev`** (HEAD `b27687d2`), not
`main` (`main`'s HEAD `90696789` is a `2026-07-11T18:47:21Z` merge of `dev` at an
earlier point — `dev` has ~9 more commits past that merge, through this morning).
Both branches were read; findings below hold on both.

### (a)/(d) Local model + non-Fireworks call audit

Single remote client instantiated in `app/services/agent.py`:
```python
self.remote_client = OpenAI(
    api_key=api_key or os.environ.get("FIREWORKS_API_KEY", "mock-key"),
    base_url=settings.fireworks_base_url   # default "https://api.fireworks.ai/inference/v1"
)
```
No second client, no `googleapis`, `anthropic`, `openai.com`, or any other external
host anywhere in the repo (`gh api search/code?q=repo:IrvanKurniawan624/velora+http`
returns only 10 hits, all in docs/config/lockfiles, none introducing a second
provider). The local model is Gemma 2B Q4 (on `main`) / Qwen 2.5 3B Q4 (on the
current `dev` branch — the local model was swapped at some point in development).
The math sandbox (`app/services/pyexec.py`) runs `python -I -c <code>` via
`subprocess.run` with an explicitly minimal env (`{"PYTHONIOENCODING": "utf-8"}`,
i.e. no inherited proxy/network env vars) — no network egress path found there either.
**No evidence of any hidden or non-Fireworks network call — the cleanest of the three
entries in this pass on that specific axis.**

### The pre-hydrated cache — the likely real story, and why it complicates the picture

Velora's own README is unusually candid and is worth quoting directly:

> "On benchmark tasks, it achieves **100.0% overall accuracy** while saving **64.9%
> remote token consumption** and executing in **0.59 seconds**... The pre-hydrated
> cache database (`benchmarks/agent_cache.json`) is committed directly to the Git
> repository. On tasks it has seen before, it gets instant **100% fuzzy cache hits**
> and completes the entire test suite in under 1 second using **0 remote tokens**."

Their own ablation table (27-task rehearsal, reproduced verbatim) shows this cache
is doing essentially all the work of the headline number — the underlying routing
logic alone is much weaker:

| Strategy | Accuracy | 80% Gate | Token Savings |
|---|---|---|---|
| Hybrid (Speculative + Cache) | 100.0% | PASS | **64.9%** |
| Fuzzy Cache Only | 92.6% | PASS | ~0% |
| **Speculative Routing Only (no cache)** | **88.9%** | PASS | **-30.2%** (i.e. *more* tokens than baseline) |
| JIT LinUCB Router | 70.4% | **FAIL** | ~0% |
| Rule-Based Classifier | 63.0% | **FAIL** | -8.6% |

**But this cache almost certainly does not survive into the actual graded run.**
`.dockerignore` explicitly excludes `benchmarks/` (and `tests/`, `docs/`) from the
built image. The cache-path resolution logic in `agent.py` only checks
`benchmarks/`, `/app/benchmarks/`, `output/`, `/output/` — since `benchmarks/` is
never copied into the image, the first two never exist inside the container, and
`output`/`/output` would be an empty grading-harness-mounted volume with no
pre-seeded `agent_cache.json` in it at the start of a fresh run. On a truly cold
grading invocation, `self.cache` initializes empty and **every task falls through
to the real "Speculative Routing Only" path** — which their own table shows scores
88.9% accuracy but at **negative token savings** (i.e., it should cost *more*
Fireworks tokens than a naive baseline, not zero).

This creates a genuine, unresolved discrepancy we could not close from code alone:
the architecture we can read does not obviously produce a 0-token outcome on a cold
run, yet the task brief lists Velora at 0 tokens (with 52.6% accuracy — notably
*below* even their own worst rehearsal ablation, and well below the 84.2% gate).
The most parsimonious explanation consistent with everything observed: the
0-token/52.6%-accuracy datapoint is from a specific checked run (possibly an
earlier or partially-broken commit state, given the team was still actively pushing
routing changes as of this morning) rather than a stable characteristic of the
current code, and the team's continued commits through the morning of deadline day
indicate they know something is off and are still chasing it. **Flagged as
UNVERIFIED / genuinely puzzling, not as a confirmed violation** — there is no code
evidence of cheating, only evidence of instability.

### Assessment: **[LEGIT local-only architecture, code is clean] + [ACCURACY UNSTABLE / gate status uncertain]**
No rules-violation evidence (unlike rtq-smart-router). But per the brief's own
52.6% figure, this entry currently reads as a **gate failure**, not a top-rank
threat, and the team's own numbers suggest their real (cache-free) ceiling is
~88.9% accuracy at *positive* token cost, not 0 tokens. Whether they fix this
before 22:00 UTC is unknown and, given continued commits as of 9 hours ago, live.

---

## 2. OyeHoye Zero Tokens (team oyehoye) — 89.5% accuracy per task brief

**Lablab page** (verified, exact title match):
https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/oyehoye/oyehoye-zero-tokens
— created by team **oyehoye** on July 08, 2026. Built by **Nikhil Kapila, Gaurav
Gosain, Zain Raisan** (three named GitHub-linked profiles).

**Github field on the submission page**: `https://github.com/nkapila6/` — **this
is a bare profile URL, not a link to any specific repository.** This is a
meaningfully different (and arguably worse) failure mode than yassai's dead link:
yassai at least *attempted* to link a specific repo (which then 404s); OyeHoye's
own submission form field was never pointed at a repo at all.

### Repo search across all three named contributors

Checked all public repos for all three accounts:
- `nkapila6`: 102 public repos enumerated via `gh api users/nkapila6/repos
  --paginate` — none named or described as related to this hackathon, "oyehoye,"
  "amd," "fireworks," "track1," or "gemma-4-e2b." (One repo, `cc-oyehoye`, is an
  unrelated pre-existing Claude Code sound-effect hook named after the same Bollywood
  song reference — a coincidence, not the submission.)
- `Gaurav-Gosain`: ~100 public repos enumerated — same result, nothing matching.
- `zraisan` (resolved via GitHub user search from the lablab-listed name "Zain
  Raisan"; also confirmed via a personal `MIGraphX-Documentation` repo referencing
  AMD, so this is very likely the right account) — 21 public repos, nothing
  matching.
- `gh api search/code?q=FIREWORKS_BASE_URL+user:<each>` and
  `q=gemma-4-E2B+user:<each>` — **zero results across all three accounts.**
- No GitHub organization named `oyehoye` exists (404).

**Conclusion: no public source repository for this submission could be located
anywhere, from any of the three named team members, by any search method used.**

### What *does* exist: a real, actively-updated Docker image

`gh api users/nkapila6/packages?package_type=container` confirms a public GHCR
package `ghcr.io/nkapila6/oyehoye`, unlike the team's other listed container
(`mcp-local-rag`), **this package has no linked source-repository metadata at all**
— consistent with the submission's own description that the image ships only
compiled artifacts. Version history (`.../packages/container/oyehoye/versions`):

| Tag | Pushed (UTC, today 2026-07-12) |
|---|---|
| `nk1` | 05:16:03 |
| `nk2` | 09:51:01 |
| `nk3` | 09:52:57 |
| `nk4` | 09:53:33 |
| `winning-tag` | 09:54:07 |

Four retagged pushes inside a 3-minute window this morning, the last one literally
named **`winning-tag`**, ~7.5 hours before this research pass and ~12 hours before
the deadline. This is the same "rapid same-day iteration against live feedback"
signature the prior pass flagged in rtq-smart-router's commit history (11 commits
in a day, each a different strategy) — strong circumstantial evidence of active,
knowing tuning toward a specific scoring outcome, though **on its own this is not
proof of a rules violation** — it's consistent with legitimate last-minute
optimization too.

### Submission's own claimed architecture (verbatim, UNVERIFIED against code — no code exists to check)
> "Cost-tiered pipeline: deterministic solvers, spaCy NER, and local Gemma 4 E2B
> handle all 8 task categories at zero Fireworks tokens... Compiled to native .so
> via Cython, so the final Docker image carries no readable source... The client
> exists for offline testing but is never called during a graded run and is not
> compiled into the image... Peak observed memory is 3.66 GiB, a 19-task local run
> completes in 34 seconds."

Notably specific and plausible-sounding (matches the known 19-task fixed set), and
we chose **not** to `docker pull`/decompile the GHCR image to check it, consistent
with the prior pass's decision to treat that as out-of-scope reverse-engineering of
a competitor's binary artifact rather than "reading public source."

### Assessment: **[INSUFFICIENT DATA on architecture] + [SUSPICIOUS on repo-transparency compliance]**
Real, live, actively-iterated Docker artifact (not vaporware like YOLOAI_v6's
1-line-README stub from the prior pass) — but the submission's own "GitHub" field
does not resolve to a repository at all, across three team members' full public
repo lists. If lablab's manual review checks that the Github link field actually
points at inspectable source (which is the literal requirement, and which is
exactly the kind of check that caught rtq), this entry looks vulnerable on that
narrow, mechanical basis independent of whether the underlying claims are true.

---

## 3. yassai (team Solo Stack) — 84.2% accuracy per task brief

**Re-verified today (2026-07-12), unchanged from the 2026-07-10 snapshot in
`top5_forensics.md`:**
- `https://github.com/ashaibani/yassai` → still a clean 404
  (`gh api repos/ashaibani/yassai` → `{"message":"Not Found","status":"404"}`).
- `https://github.com/ashaibani/yassai-placeholder` → still exists but still
  completely empty (`git/trees/HEAD` → `409 Git Repository is empty`), `pushed_at`
  still `2026-07-10T11:44:58Z` (i.e. **not touched in over 2 days**, despite the
  team being 2 days closer to a same-day deadline).
- The lablab submission page's "Github" field points to the empty placeholder;
  the "Demo" field points to the 404'd repo — i.e. **neither link resolves to any
  inspectable code**, and this has now persisted, unfixed, for the last ~48 hours
  of the competition window, including all of deadline day up to this check.

Description (verbatim, still unverifiable against any code): local "small custom
classifier running in-process," "single unified code-execution surface" instead of
native tool-calling to keep prompts compact.

### Assessment: **[SUSPICIOUS on repo-transparency compliance — worse than 2 days ago]**
Same conclusion as the prior pass, strengthened by time: this is not a fresh
mistake that might still get fixed — it's a 48-hour-old broken submission
requirement, sitting through the entire final day, on an account that is otherwise
a real, long-lived, non-fake GitHub user (11 unrelated pre-2026 repos). No new
evidence of code-level wrongdoing (there's still no code to read), but the
compliance gap itself is now harder to explain as an oversight.

---

## Cross-cutting pattern (this pass + prior pass combined, 8 top-rank entries examined total)

| Entry | Repo/source status | Real code readable? | Live/active artifact? |
|---|---|---|---|
| rtq-smart-router (prior, DQ'd) | Real, 11 commits | Yes — contained the violation | Yes |
| Kestrel (prior) | README+LICENSE only, source withheld by design | No | Yes (GHCR, updated live) |
| Metis (prior) | Linked repo is an unrelated pre-existing OSS project | No | Unknown |
| YOLOAI_v6 (prior) | 1-line README stub | No | No |
| yassai (prior + this pass, unchanged) | Dead link + empty placeholder, 48h+ unfixed | No | No |
| **Velora (this pass)** | **Real, substantial, actively committed through this morning** | **Yes — clean, no hidden calls found** | **Yes** |
| **OyeHoye (this pass)** | **No repo at all — Github field is a bare profile URL** | **No** | **Yes (GHCR, retagged 5x this morning, ending "winning-tag")** |

Of 8 top-rank entries examined across both passes, only **2** (rtq, Velora) had
genuinely inspectable public source with no hidden-network-call red flags — and
one of those two (rtq) was DQ'd anyway once inspected, for exactly the kind of
violation a `grep -r googleapis` would catch instantly. The other one (Velora) is
clean on that axis but has its own separate problem: the code's own logic doesn't
obviously reconcile with a 0-token outcome on a fresh run, and the brief's own
52.6%-accuracy figure would put it below the gate. **6 of 8** have some form of
non-inspectable, dead, wrong, or nonexistent public repository — a rate that has
gone *up*, not down, since the prior pass (was 4/5 within just the original top-5).

---

## What this means for our own submission

1. **Repo-transparency is turning out to be a real, mechanically-checkable filter,
   separate from deep code auditing.** rtq needed someone to actually read
   `agent.py` to catch the Gemini call. Catching "Github field doesn't point to a
   real repo" (yassai, OyeHoye) requires nothing more than clicking the link — if
   lablab or AMD does even a cursory manual pass on the top ranks before finalizing
   prizes (which the rtq precedent shows they are willing to do), this alone could
   eliminate a meaningful fraction of the current 0-token cluster. We should make
   sure our own submission's Github field points to our actual, complete,
   README-accurate repo — this is the single cheapest form of due diligence
   available and the prior pass already confirmed we should not assume we're
   exempt from the same scrutiny.
2. **Velora is the one entry in this cluster with a real technical architecture
   worth taking seriously as a peer** (confidence-cascaded local/remote routing,
   persistent normalized cache, symbolic prompt compression, program-aided math via
   sandboxed subprocess) — but per their own numbers and our .dockerignore reading,
   their *real* ceiling without cache assistance is ~88.9% accuracy at *increased*
   (not zero) token cost. If the 52.6% figure in the brief is their current live
   score, they are presently failing the gate, not threatening our rank.
3. **Do not assume OyeHoye is hollow just because it's unauditable.** The GHCR
   package is real, live, and was retagged five times this morning ending in a tag
   literally named "winning-tag" — whoever built it believes it works and was
   tuning it against something (the live leaderboard, most likely) right up until
   a few hours before this check. Treat it as a live threat on tokens/accuracy even
   though we can't verify the mechanism, while separately noting it may be
   vulnerable to elimination on the repo-transparency technicality alone.

---

## Sources (all fetched this session)

- https://lablab.ai/event/amd-developer-hackathon-act-ii (via r.jina.ai — full submission gallery, used to discover team-slug/project-slug pairs for Velora, OyeHoye, yassai)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live (via r.jina.ai — renders an unscored-submissions error list, not a token/accuracy table, as of this session)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/6-7/velora (via r.jina.ai)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/oyehoye/oyehoye-zero-tokens (via r.jina.ai)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/solo-stack/yassai (via r.jina.ai, re-fetch of prior-pass URL)
- https://github.com/IrvanKurniawan624/velora — repo, branches (`dev` vs `main`), commits, full tree, `Dockerfile`, `.dockerignore`, `app/config.py`, `app/services/agent.py` (both branches), `app/clients/local_client.py`, `app/services/pyexec.py`, `README.md` — via `gh api` and `raw.githubusercontent.com`
- `gh api users/nkapila6/repos`, `users/Gaurav-Gosain/repos`, `users/zraisan/repos` (full paginated listings, 102/~100/21 repos respectively)
- `gh api users/nkapila6/packages?package_type=container` and `.../packages/container/oyehoye/versions` (GHCR package + version/tag history)
- `gh api search/code?q=FIREWORKS_BASE_URL+user:<nkapila6|Gaurav-Gosain|zraisan>`, `q=gemma-4-E2B+user:...`, `q=repo:IrvanKurniawan624/velora+http`
- `gh api repos/ashaibani/yassai`, `repos/ashaibani/yassai-placeholder`, `.../git/trees/HEAD` — re-verification of prior-pass findings
- WebSearch: "lablab.ai amd developer hackathon act ii Velora / OyeHoye / yassai OR Solo Stack" — the OyeHoye query returned an (unverified, LLM-summarized) mention of a "Fewest tokens wins" leaderboard view with OyeHoye at position 6, suggesting unseen ranks 1-5 hold more 0-token entries not identified by name in this pass

## Not found / explicitly abandoned after exhaustive attempts

No public source repository for OyeHoye Zero Tokens could be found after checking
all three named contributors' full public repo lists (~220 repos total across the
three accounts) plus targeted GitHub code search for hackathon-specific strings —
reported as a finding in itself (see above), not left as an open lead. We did not
attempt to pull or decompile the `ghcr.io/nkapila6/oyehoye` image, matching the
prior pass's explicit scope boundary against reverse-engineering competitors'
binary artifacts. We did not attempt to independently re-derive the leaderboard's
token/accuracy numbers via a live API call (none was found/authenticated this
session) — all such figures are taken as given from the task brief, per the same
caveat the prior pass documented.
