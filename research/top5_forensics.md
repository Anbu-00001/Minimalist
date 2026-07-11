# Top-5 Leaderboard Forensics — AMD Developer Hackathon Act II, Track 1 (2026-07-10 evening)

Scope: the user-supplied current top-5 leaderboard snapshot (Jul 10 evening):

| Rank | Project | Team | Tokens | Accuracy |
|---|---|---|---|---|
| 1 | rtq-smart-router submission 41 | rusetiq | 0 | 100.0% |
| 2 | Kestrel - v0.68 | SoloPlayer | 1,798 | 89.5% |
| 3 | Metis - v(lost count + 3) | Kingdom of Science | 2,138 | 84.2% |
| 4 | yassai | Solo Stack | 2,228 | 100.0% |
| 5 | YOLOAI_v6 | YoloAI | 2,664 | 84.2% |

This is a NEW pass — none of these 5 overlap with the entries already logged in
`research/competitors_lablab.md` or `research/competitive_differentiation.md`
(that earlier pass covered Route AI, TokenForge Router, NovaAI,
Adaptive Routing Agent, Ligs-Attempt-276, Minima, ApexFlow — an 8-team
leaderboard that has been completely reshuffled since). All 5 of today's top
entries were found and their public GitHub repos located. Method: `gh api`
to search GitHub by name/owner, then brute-force slug probing of
`https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/<team>/<project>`
via the `r.jina.ai` proxy (direct fetch is Cloudflare-blocked) until the page
title matched the leaderboard project name exactly, then WebFetch to extract
the submission's own description, GitHub link, and team/creator names.
Repo contents were then pulled directly via `gh api` (trees/blobs) and
`raw.githubusercontent.com`, not just READMEs.

**Important caveat on methodology**: the `/live` leaderboard URL that a prior
session (2026-07-09) used to independently re-fetch token/accuracy numbers
now renders a *different* widget ("Top Submissions by community vote" +
"Top Builders by points") — no token-count table is present in that page as
of this fetch. The raw page dump also contains three live community
comments reading "Bring back the leaderboarddd" / "where is leaderboard
now??" (x2), suggesting the token/accuracy leaderboard view itself may be
temporarily broken or reorganized on lablab.ai's end. **We could not
independently re-derive the tokens/accuracy numbers in the table above from
a live page fetch this session — they are taken as given from the task
brief.** Everything below that number is independently verified against the
individual project pages and GitHub repos, which were all locatable and
fetchable.

---

## 1. rtq-smart-router submission 41 (#1, team rusetiq) — 0 tokens, 100.0% accuracy

**Lablab page** (verified real, exact title match):
https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/rusetiq/rtq-smart-router-submission-41
— Team: rusetiq. Creator: "aarush diwakar". Submitted July 08, 2026.

**GitHub** (linked directly from the submission page, and independently
confirmed by the repo's own `push_ghcr.sh` which sets
`IMAGE_NAME="rtq-smart-router:latest"`): https://github.com/rusetiq/rtqsort
— public, 8 files, 11 commits, all dated **2026-07-08**, last push
2026-07-09T06:55:01Z. Docker image: `ghcr.io/rusetiq/rtqsort:latest`.

### (a) Local model claimed vs. shipped

The submission page's own description (still live, verbatim via WebFetch):
> "a local, zero token classification step: a 2 bit quantized gemma 4 e2b
> model running in a constrained docker environment (4gb ram, 2 vcpus)"

The repo's `submission_description.md` (same claim, more detail):
> "Upon container boot, the agent spawns a background `llama-server`
> instance compiled from source via CMake. It loads a highly optimized
> 2-bit quantized version of Google's Gemma 4 E2B model
> (`gemma-4-E2B-it-Q2_K.gguf`, ~3 GB)... zero-shot classifies incoming
> prompts into 8 distinct capability domains."

**This does not match the shipped code.** The full commit log:

```
b70aa7cc | 2026-07-08T18:15:27Z | refactor: add gemini-3.1-flash-lite double-check stage
13ac8c55 | 2026-07-08T18:02:31Z | refactor: use minimax-m3 and custom system prompt to optimize accuracy
e0f7a2cd | 2026-07-08T14:48:39Z | refactor: select and use kimi-k2p7-code model for all tasks
da0ee015 | 2026-07-08T14:37:47Z | refactor: direct single gemma-31b-it model inference, remove all routing
abd934cc | 2026-07-08T14:36:45Z | refactor: use direct single-model inference, bypass classification
168935a3 | 2026-07-08T14:27:29Z | fix: resolve agent accuracy issues
aee45ff9 | 2026-07-08T14:08:47Z | fix: cloud classification and robust code clean-up
df9fe15e | 2026-07-08T14:00:07Z | refactor: remove local SLM, use Fireworks-only routing
eec9c97b | 2026-07-08T13:48:12Z | fix: better system prompts, token budgets, model routing for Track 1 models
c6f75c59 | 2026-07-08T13:18:46Z | fix: correct Gemma 4 GGUF model download and add code post-processing parser
0fba6a87 | 2026-07-08T13:02:24Z | initial commit: rtq-smart-router hybrid routing agent
```

The local Gemma/llama-server design existed only in the first two commits
and was explicitly ripped out at `df9fe15e` ("remove local SLM, use
Fireworks-only routing") — 6 commits before the final one. The
`submission_description.md` marketing copy was never updated afterward and
still describes the abandoned architecture. **The shipped `Dockerfile` has
zero trace of it**: `FROM python:3.10-slim`, installs only
`openai>=1.0.0` and `python-dotenv>=1.0.0`, copies only `agent.py`. No
CMake, no llama.cpp, no GGUF download, despite `build.sh` (which is not
what the `Dockerfile` runs) still describing "Clone and compile llama.cpp
(llama-server)... Download Gemma 4 E2B Q2_K GGUF (~3 GB)."

### (b)/(c) What the shipped agent.py actually does — and (d) the DQ finding

Full logic of the final `agent.py` (HEAD, `b70aa7cc`), reproduced because
it's short and the exact wording matters:

```python
client = OpenAI(api_key=api_key, base_url=base_url)   # base_url = FIREWORKS_BASE_URL
...
for task in tasks:
    messages = [
        {"role": "system", "content": "You are a highly accurate AI assistant. Make no mistakes and attain 100% accuracy for each question. Keep your answers direct and do not overthink."},
        {"role": "user", "content": prompt}
    ]
    answer = "Unable to generate answer."
    for attempt in range(3):
        try:
            response = client.chat.completions.create(model=model, messages=messages, temperature=0.1, max_tokens=1000)
            answer = response.choices[0].message.content.strip()
            break
        except Exception:
            ...retry with backoff...

    try:
        gemini_client = OpenAI(
            api_key="AIzaSy...REDACTED",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        gemini_messages = [
            {"role": "system", "content": "You are a expert corrector. Review the proposed answer for the user prompt. If the answer is correct and complete, output the answer exactly as is. If the answer has any errors, inaccuracies, or is incomplete, output the corrected version of the answer. Output only the final answer directly without any explanations or meta-commentary."},
            {"role": "user", "content": f"User Prompt: {prompt}\n\nProposed Answer: {answer}"}
        ]
        gemini_response = gemini_client.chat.completions.create(model="gemini-3.1-flash-lite", messages=gemini_messages, temperature=0.1, max_tokens=1000)
        corrected_answer = gemini_response.choices[0].message.content.strip()
        if corrected_answer:
            answer = corrected_answer
    except Exception:
        pass
```

Every single task: (1) calls Fireworks once via the harness-provided
`FIREWORKS_BASE_URL`, model preference-ordered toward `minimax-m3`, with
retries; then (2) **unconditionally** calls Google's Gemini API directly at
`generativelanguage.googleapis.com` using a **hardcoded, plaintext API key
committed to the public repo** (`AIzaSy...REDACTED`),
and if Gemini returns anything non-empty, **that Gemini answer overwrites
the Fireworks answer as the final submitted result.**

This is a direct, code-confirmed instance of exactly the failure mode the
organizer's Discord DQ warning describes ("any network calls to
non-Fireworks endpoints... Gemini... will be DQ'd in manual audit"). It is
not disguised — the submission page's own "Technologies" tag list
literally includes **"Gemini AI"** alongside "AI/ML API" and "Gemma."

### The 0-token / 100%-accuracy mechanism — best evidence, marked as inference

We do not have visibility into lablab.ai's judging proxy internals, so this
part is **inference from the code, not a confirmed mechanism** — flagged
explicitly:

The hackathon's token counter almost certainly meters only traffic through
the harness-provided `FIREWORKS_BASE_URL`. This code calls Fireworks first,
but **regardless of whether that call succeeds, fails, times out, or the
model name doesn't resolve**, the code always falls through to the Gemini
call and prefers its output. If the Fireworks leg fails on every task in
the judge's environment (wrong/unavailable model string, rate limit, auth
issue, or anything else that raises inside the `try` before a completion is
billed), the token meter would legitimately record **0** Fireworks tokens
— while the *actual* answers, good enough to plausibly clear the accuracy
gate at 100%, are being generated for free by an un-metered outside model.
Whether this is what happened for "submission 41" specifically cannot be
confirmed without the judge's logs, but it is a concrete, mechanically
plausible explanation consistent with every fact we could verify, and it
matches exactly the "proxy bypass" hypothesis flagged in the task brief.
**Marked UNVERIFIED as the specific cause of rank #1's score; VERIFIED that
the code contains an undisclosed non-Fireworks network call capable of
producing this effect.**

### (e) What we can legitimately adopt

Nothing architectural — their real lesson is negative (don't do this). The
one legitimately interesting thing in their commit history is the *speed*
of iteration (11 substantive commits in a single day, each renaming to a
different single-model strategy) — evidence that this team was doing rapid
trial-and-error against the live leaderboard rather than principled design,
which is itself useful competitive intelligence: the #1 slot on this
leaderboard is occupied by a since-abandoned local-model idea plus what
reads as an accidental or intentional metering loophole, not a stronger
architecture than ours.

---

## 2. Kestrel - v0.68 (#2, team SoloPlayer) — 1,798 tokens, 89.5% accuracy

**Lablab page** (verified, exact title match):
https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/soloplayer/kestrel-v068
— Team: SoloPlayer. Creator: "Petr Novák". Submitted July 6, 2026 (day 1).

**GitHub**: https://github.com/py-tr/kestrel-agent — public, but **contains
no source code**: only `LICENSE` and a 1,584-byte `README.md`. Repo size 1
(KB), created and pushed once, 2026-07-08T09:13Z, never updated since.

The README states this explicitly, and it's worth quoting in full because
it's an unusually candid statement of intent:

> "## Source
> The full agent source will be published in this repository at submission
> finalization, ahead of judging. It is withheld during the live
> competition window for competitive reasons — the runnable artifact above
> is the complete, scoreable deliverable."

The "runnable artifact" they point to instead is a GitHub Container
Registry image, `ghcr.io/py-tr/kestrel:a2`. We confirmed via
`gh api users/py-tr/packages?package_type=container` that this package
**is real and public** (`"visibility":"public"`), and — notably — was
**updated as recently as 2026-07-10T15:13:54Z**, i.e. today, hours before
this research pass, confirming the team is actively iterating and pushing
new image builds during the live competition window, consistent with the
"v0.68" version string.

### Findings

- **(a) local model**: unknown — cannot verify, source withheld.
- **(b) escalation policy**: cannot verify from code. The README's prose
  claims ("Kestrel decides how much work each task actually needs and
  spends accordingly") is marketing language identical in register to
  every other team's pitch; no mechanism is specified.
- **(c) token minimization**: cannot verify. README claims "no boilerplate,
  no wasted round trips" and that "all inference is routed through the
  harness-provided Fireworks endpoint using only the permitted models,
  with credentials and the model list read from the environment at
  runtime" — this is a *self-reported* compliance claim, not something we
  could confirm by reading code.
- **(d) non-Fireworks calls**: **cannot be audited**. This is the one
  submission in the top 5 that is genuinely and admittedly opaque by
  design during the competition window. We explicitly did not attempt to
  `docker pull`/decompile the GHCR image — that would go beyond "read
  public source" and into reverse-engineering a competitor's binary
  artifact, which is out of scope for this research pass.
- **(e) what to adopt**: the pattern of "container starts in ~1 second"
  and CI-built-and-tested-on-every-change image discipline (per the
  README) is a legitimate operational practice worth matching if we
  aren't already there — fast cold start directly protects against
  timeout-driven accuracy loss.

**Conclusion for Kestrel: genuinely unverifiable, not evidence of
wrongdoing.** Unlike rtq-smart-router, there is no code to contradict their
claims — there's simply no code, publicly, right now.

---

## 3. Metis - v(lost count + 3) / "v(lost count + 4)" (#3, team Kingdom of Science) — 2,138 tokens, 84.2% accuracy

**Lablab page** (verified, exact title match — note the leaderboard snapshot
says "+3", the live page currently reads "+4", i.e. one more resubmission
happened between the leaderboard screenshot and this fetch):
https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/kingdom-of-science/metis
— Team: "Kingdom of Science", created July 08, 2026.

**GitHub link on the submission page**: https://github.com/earendil-works/pi
(this is the *only* link on the page, used for both "GitHub" and "Demo").

### This link does not correspond to a Track 1 submission

`earendil-works/pi` is a real, large (1,133-file, TypeScript), **actively
maintained since 2025-08-09** open-source project — its own description:
"AI agent toolkit: unified LLM API, agent loop, TUI, coding agent CLI."
It has 30+ long-lived feature branches (`model-registry`, `better-approvals`,
`grammar-constraints`, etc.), a full CI/contributor pipeline, and a generic
multi-provider `packages/ai/src/providers/fireworks.ts` (Fireworks is just
one of many supported providers in their SDK, unrelated to this hackathon).

We searched the repo directly for any trace of the submission's own
marketing claims and found **zero matches**:
- `gh api search/code?q=isotonic+repo:earendil-works/pi` → 0 results
  (their description claims "isotonic-calibrated confidence gating").
- `gh api search/code?q=Metis+repo:earendil-works/pi` → 0 results.
- No branch named anything like `amd-hackathon`, `track1`, or `metis`.

**Conclusion: the public GitHub repo linked from Metis's lablab.ai
submission page contains no verifiable Track 1 agent code.** It's either a
copy-paste error (they linked their team's/individual's general tooling
repo instead of a dedicated submission repo) or a deliberate choice to
satisfy the "must link a GitHub repo" field without exposing real logic. We
cannot distinguish these from outside. Either way, **their described
architecture cannot be verified against real code**, only against their own
prose.

### Their own claimed architecture (submission page, verbatim/near-verbatim, UNVERIFIED against code)

> "most tasks don't need a frontier model, and the ones that do should be
> identified before you pay for them — not after." Local-first on
> "Qwen2.5-3B (local quantized model)," sampled "multiple times in
> parallel to measure agreement," escalate via "isotonic-calibrated
> confidence gating based on consensus, token-level confidence, and
> per-category signals." Math gets "program-aided verification." "An
> adaptive governor watches the runtime budget and downshifts sampling if
> the clock runs short." Self-reported rehearsal numbers: "95.8% judged
> accuracy while escalating only 29% of tasks" with "~1,400 total paid
> tokens in their 48-task rehearsal."

Notably, this description — local quantized model, sampling for agreement,
isotonic calibration, program-aided math verification, deterministic
escalation gating — is architecturally the closest match to our own design
philosophy of anything found in this pass (or in the prior
`competitive_differentiation.md` pass, where ApexFlow was the closest
match but with same-model self-review instead of real verification). If
true, Metis would be a genuine architectural peer. **But we have zero code
evidence it's true** — this is prose only, and the one prose claim we could
mechanically check (their own repo link) failed to substantiate it.

### (e) What to adopt
Nothing new we can verify — but the *prose itself* (if their claims are
real) validates our own design direction: program-aided math verification
+ local-first + calibrated escalation is apparently converging territory
among the stronger teams in this specific hackathon, independent of code
access.

---

## 4. yassai (#4, team Solo Stack) — 2,228 tokens, 100.0% accuracy

**Lablab page** (verified, exact title match):
https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/solo-stack/yassai
— Team: "Solo Stack". Creator: "Mo Ashaibani" (Software Engineer).

**GitHub link on the submission page**: https://github.com/ashaibani/yassai
— **this returns a clean 404**, confirmed independently three ways:
`gh api repos/ashaibani/yassai` → `{"message":"Not Found","status":"404"}`;
`curl -I https://github.com/ashaibani/yassai` → `HTTP/2 404`;
`curl -I https://api.github.com/repos/ashaibani/yassai` → `HTTP/2 404`.

The same lablab.ai page also links to a second repo,
**`github.com/ashaibani/yassai-placeholder`** — this one does exist but is
**completely empty** (`gh api .../git/trees/HEAD` → `"Git Repository is
empty."`, HTTP 409), created 2026-07-10T11:44:58Z (today). The account
`ashaibani` (real GitHub user since 2016, 11 unrelated older repos — a PHP
blog, a Svelte starter, a world-cup raffle app, etc. — genuinely this
person's account, not a fake) currently has **no publicly accessible
repository containing any yassai code whatsoever.**

### Findings

- **(a)–(d)**: cannot be verified — there is no code to read, publicly,
  right now. This is the one entry in the top 5 that currently fails
  lablab.ai's own stated submission requirement ("every submission to have
  a PUBLIC GitHub repo") at a literal, checkable level — not "opaque by
  design" like Kestrel (which openly explains the withholding and still
  gave a real, live, public runnable image), but a broken/dead link with a
  same-named empty placeholder sitting next to it.
- Submission page's own description (verbatim, for the record, UNVERIFIED
  against code): local "small custom classifier running in-process" for
  task categorization; "single unified code-execution surface" exposing
  tools instead of native model tool-calling, to keep prompts compact;
  "shorter prompts, fewer retries, and tokens spent on answers rather than
  orchestration overhead."
- **(e) what to adopt**: the "unified code-execution surface instead of
  native tool-calling" idea (if real) is a genuinely interesting token-
  saving lever distinct from anything in our current design — routing
  every tool invocation through one code-exec surface avoids per-tool
  JSON-schema/function-calling overhead in the prompt. Worth considering
  independent of whether this specific team's claim is verifiable, since
  the idea stands on its own merits.

---

## 5. YOLOAI_v6 (#5, team YoloAI) — 2,664 tokens, 84.2% accuracy

**Lablab page** (verified, exact title match):
https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/yoloai/yoloai
— Creator: "Satish Saini" (@Satishsaini905).

**GitHub**: https://github.com/sainisatish/YoloAIRouter — public, but
**contains only a 1-line README** (`raw` content: `# YoloAIRouter`, 14
bytes total, single commit, 2026-07-09T16:17:56Z). No agent code, no
Dockerfile, nothing.

### Findings

- **(a)–(d)**: cannot be verified — no code exists in the repo.
- Submission page's own description (verbatim, UNVERIFIED against code):
  "Every task is attempted locally first. The keep-vs-escalate decision is
  estimated entirely for free using self-consistency (agreement across
  local samples), deterministic format/structure checks, and a local
  self-verification pass where the model judges its own answer YES/NO."
  Claims a "TokenAccountant that mirrors the scoring rule, counting only
  remote, non-cached tokens." Claims to be "Contract-safe by construction...
  exits 0, stays within the 10-minute / 30-second-per-request budgets, is
  ready in under 60s, reads env-injected credentials (never hardcoded),
  emits schema-valid JSON."
- Worth flagging: their own description explicitly says credentials are
  "never hardcoded" — a claim we obviously can't verify given there's no
  code, but notable as the exact opposite of what we independently
  confirmed in rtq-smart-router's actual shipped code (hardcoded Gemini
  key).
- Their described "self-verification pass where the model judges its own
  answer YES/NO" is, if accurate, the same same-model-self-review pattern
  our design (`VERDICTS.md` V7) explicitly argues against as weaker than
  independent re-derivation — consistent with the pattern already found in
  ApexFlow in the prior research pass. But again: prose only, unverifiable.
- **(e) what to adopt**: nothing new — their one concrete, plausible-sounding
  mechanism (a "TokenAccountant that mirrors the scoring rule") is a good
  practice (know your own token count before the judge tells you) but is
  something we should already be doing internally regardless of their
  example.

---

## Cross-cutting pattern across the current top 5

| Rank | Project | Repo status | Real code readable? |
|---|---|---|---|
| 1 | rtq-smart-router | Real code, 11 commits | **Yes** — and it contradicts its own marketing, and makes an undisclosed Gemini call |
| 2 | Kestrel | README + LICENSE only, source explicitly withheld until "finalization" | No |
| 3 | Metis | Real repo linked, but it's an unrelated 2025-founded open-source project, not their submission | No |
| 4 | yassai | Linked repo 404s; only an empty same-day placeholder repo exists | No |
| 5 | YOLOAI_v6 | 1-line README stub | No |

**Four of the current top five have GitHub repos that do not contain
inspectable Track 1 agent source code**, for four different reasons
(withheld-by-design, wrong-repo, dead-link, empty-stub). The one repo that
*does* have real code (rank #1) is the one where reading it turned up a
rules violation. This is worth sitting with honestly: it means the "read
the code, find the truth" method that worked well in the prior
`competitive_differentiation.md` pass (4 of 8 readable) is now hitting a
much higher opacity rate at the very top of the leaderboard (1 of 5
readable) — either because stronger/gamier teams have learned to keep
source private during the live window (Kestrel says so outright), or
because top ranks are disproportionately occupied by teams exploiting
scoring-proxy edge cases that don't require showing real work (rtq-smart-
router), or both. We should not conclude "the other 4 are also gaming the
proxy" — that's not evidenced and would be exactly the kind of overclaim
the prior research pass warned against. What IS evidenced: we cannot audit
them, and lablab.ai's own "public GitHub repo" requirement is being
satisfied only nominally by at least 2 of the 5 (Kestrel's is code-free by
admission; yassai's doesn't resolve at all).

---

## What we should do about it — ranked

1. **Report rtq-smart-router to the organizers, or at minimum flag it
   internally as the strongest evidence this research has produced of a
   DQ-worthy violation.** We have code-level proof (not speculation) of an
   undisclosed direct call to `generativelanguage.googleapis.com` with a
   hardcoded key, in the exact shape the organizer's own Discord DQ warning
   describes. This is the single most actionable finding of this pass — if
   the manual audit catches it (and it's trivial to catch: `grep -r
   googleapis` across their repo would do it), rank #1 likely disappears
   from the field entirely, which matters more to our own effective rank
   than any token optimization we could make in the remaining hours before
   the Jul 11 16:00 UTC deadline. We are not the enforcement mechanism, but
   this is worth surfacing to whoever can flag it (organizer Discord/audit
   channel), factually and without editorializing beyond what the code
   shows.
2. **Do not assume rank #2/#4/#5's real architectures are weaker than
   ours just because their repos are empty/dead/withheld** — that's
   unverifiable in either direction, and after the refreshed-prompt re-run
   post-deadline, a genuinely well-built hidden entry (Kestrel looks the
   most credible of the three opaque ones: real, actively-updated public
   Docker image, candid README, plausible token count relative to
   accuracy) could easily still beat us on tokens. Plan for that
   possibility rather than the comfortable read that the opaque entries
   are hollow.
3. **If Metis's self-reported architecture is real** (isotonic-calibrated
   confidence gating, program-aided math verification, adaptive runtime
   governor) it is the one genuinely worth treating as a serious technical
   peer, not just a marketing pitch — it's the closest match to our own
   design philosophy found in either research pass. We can't verify their
   numbers, but the *shape* of the idea (calibrate a confidence signal
   with isotonic regression rather than a raw threshold, and let a runtime
   governor downshift sampling under time pressure) is a legitimate,
   adoptable technique independent of whether Metis itself actually
   ships it — worth a scoped look at our own escalation-threshold logic
   before the deadline if time allows, but only as a stretch item; it is
   not proven to beat what we already have.
4. **The "unified code-execution surface instead of native tool-calling"
   idea from yassai's description** is a plausible, low-risk-to-evaluate
   token-saving lever (fewer JSON-schema tokens in every prompt) worth a
   quick internal check against our own current tool-calling approach —
   but again, sourced from unverifiable marketing prose, so treat as a
   hypothesis to test against our own harness, not an established fact
   about a competitor.
5. **Lowest priority**: nothing from Kestrel or YOLOAI_v6's prose
   descriptions is actionable beyond what our own `VERDICTS.md` already
   establishes (self-model-judging is weaker than independent
   re-derivation; fast cold-start protects against timeout losses) — these
   confirm existing plans rather than surfacing anything new.

---

## Sources (all fetched this session)

- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/rusetiq/rtq-smart-router-submission-41 (via r.jina.ai)
- https://github.com/rusetiq/rtqsort (repo, commits, all files read directly)
- https://github.com/rusetiq/rtqsort/blob/main/agent.py
- https://github.com/rusetiq/rtqsort/blob/main/submission_description.md
- https://github.com/rusetiq/rtqsort/blob/main/Dockerfile
- https://github.com/rusetiq/rtqsort/blob/main/build.sh, run_local.sh, push_ghcr.sh
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/soloplayer/kestrel-v068 (via r.jina.ai)
- https://github.com/py-tr/kestrel-agent (README, LICENSE only)
- https://github.com/py-tr/Kestrel/pkgs/container/kestrel (GHCR package, confirmed public via `gh api users/py-tr/packages`)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/kingdom-of-science/metis (via r.jina.ai)
- https://github.com/earendil-works/pi (repo, tree, branch list, code search)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/solo-stack/yassai (via r.jina.ai)
- https://github.com/ashaibani/yassai (confirmed 404 three ways)
- https://github.com/ashaibani/yassai-placeholder (confirmed empty repo)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/yoloai/yoloai (via r.jina.ai)
- https://github.com/sainisatish/YoloAIRouter (README-only stub)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live (via r.jina.ai, raw curl dump — current state is a community-vote widget, not a token/accuracy table; contains live user comments asking where the leaderboard went)
- `gh api search/repositories`, `gh api search/code`, `gh api search/users`, `gh api users/<login>/repos`, `gh api repos/<owner>/<repo>`, `gh api repos/<owner>/<repo>/git/trees/HEAD?recursive=1`, `gh api users/<login>/packages` — used throughout for independent verification of every repo claim above.

## Not found / explicitly abandoned after exhaustive attempts

Nothing in the top 5 was left completely unfound — all 5 lablab.ai
submission pages and all 5 linked GitHub repos (or their absence) were
located and checked. The only genuine dead end was the *content* of 3 of
those repos (Kestrel, Metis's link, yassai, YOLOAI_v6 — four, not three;
see table above), which is reported as such above rather than guessed at.
