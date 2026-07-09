# Competitive differentiation — what's actually publicly knowable about the other 7 qualified Track 1 teams (2026-07-09)

Research-only pass, triggered by leaderboard anxiety ("1000 other Claude Code with
Fable doing the same stuff"). Builds on `research/VERDICTS.md` V7 (cascade
literature: quality-estimation is the critical factor, our verifiers ARE the
quality estimator) and V19 (FrugalGPT/cascade academic framing) — does not
re-derive those, only adds new evidence: this time we could actually read
code.

**Headline: unlike the 2026-07-07 research pass (`competitors_lablab.md`,
which found zero readable Track-1 repos), this pass found and read 4 of the 8
qualified teams' actual submitted source.** That is a materially different,
better evidentiary position than "we can't tell, everything's closed" — and
the honest verdict below is built on that real code, not on team names.

---

## 1. The leaderboard is real and was independently re-fetched

Fetched `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/live`
directly and it returned the exact same 8 rows the user's screenshot showed,
plus the team (not just project) names and overall event stats:

| Rank | Project | Team | Tokens | Accuracy |
|---|---|---|---|---|
| 1 | Route AI | Void Martial Clan | 4,268 | 84.2% |
| 2 | TokenForge Router | OG_Mode | 5,205 | 84.2% |
| 3 | NovaAI General Purpose AI Assistant | Khdamin btkhbya | 5,234 | 84.2% |
| 4 | Adaptive Routing Agent | T_ying_yai | 5,273 | 84.2% |
| 5 | Ligs-Attempt-276 | RLSym | 5,410 | 84.2% |
| 6 | Minima | Tech debt | 5,423 | 84.2% |
| 7 | ApexFlow AI: Self-Healing Telemetry Gateway | Tarek Clarke | 10,522 | 89.5% |
| 8 | Hybrid Token-Efficient Routing Agent (**us**) | Adam dev teams | 27,459 | 84.2% |

Event totals shown on the same page: 20,727 participants, 4,632 teams, 154
scored submissions, 137 drafts in progress, 71 that did not qualify (matches
the "71 more did not qualify" in the prompt).

**Note the accuracy clustering**: 7 of 8 teams sit at exactly 84.2%. That's
almost certainly the same fixed accuracy-gate task set producing the same
pass/fail count for anyone above threshold, not 7 teams independently
converging on an identical score by chance — the gate looks like a hard
floor most competent submissions clear, and once cleared, token count is the
only thing separating rank 1 from rank 6. Only ApexFlow (89.5%, see below)
and our own submission differ.

## 2. What was found for each team

Method: fetched the lablab.ai project page for each via the
`https://r.jina.ai/` proxy (direct fetch is Cloudflare-blocked, confirmed
again this session), extracted the GitHub link if shown, verified the repo
exists via the GitHub API, then read the README and the actual entrypoint
code — not just the marketing blurb — for the 4 that resolved to a real,
non-empty repo.

### Route AI (#1, Void Martial Clan) — repo found, but empty
- lablab.ai page fetched successfully; description is generic ("intelligent
  orchestration layer... dynamically selects the most appropriate language
  model... straightforward tasks handled by lightweight models, complex
  tasks escalated to premium models").
- GitHub link on the page: `github.com/dindinmhs/tokenpilot`. Confirmed this
  repo **exists** (`api.github.com/repos/dindinmhs/tokenpilot` → 200) but is
  **empty** — 0 bytes, no language, created the same week as the hackathon.
  **No code to read.** Cannot characterize rank #1's real architecture
  beyond its own marketing prose, which describes a plain N-tier *router*
  (pick one model per task, no cascade/local-first/verification language at
  all) — but that prose is unverifiable against actual code.

### TokenForge Router (#2, OG_Mode) — not located
- No working lablab.ai slug found (`og_mode/tokenforge-router` and
  `og-mode/tokenforge-router` both 404). WebSearch's own synthesized
  summaries repeatedly described it as "solving simple math and greetings
  locally for free, escalating only complex reasoning... starting with a
  1-token judge" — **flagging this explicitly as UNVERIFIED**: no actual
  source URL backed that specific description in any search result, so it
  may be search-tool confabulation rather than a real quote. Not used as
  evidence either way.

### NovaAI General Purpose AI Assistant (#3, Khdamin btkhbya) — repo read
- GitHub: `github.com/KaananeTaha/AMD-AI-Hackathon` (confirmed real, Python,
  pushed 2026-07-07). Read the README in full.
- **Architecture, confirmed from the README's own file-by-file table**:
  `classifier.py` does "zero-token keyword heuristics" to pick one of 8
  categories, then `agent.py`/`llm.py` **always** calls a Fireworks model —
  one of three tiers (`strong`=minimax-m3, `code`=kimi-k2p7-code,
  `cheap`=gemma-4-26b) chosen by category. **There is no local-answering
  path and no verification step anywhere in the file list** (only
  `classifier.py`, `agent.py`, `llm.py`, `profile_models.py`,
  `test_classifier.py` — no verifier/checker file). This is a clean
  three-tier **model-selection router**: every task costs some tokens, the
  only lever is which tier.

### Adaptive Routing Agent (#4, T_ying_yai) — not located
- No working lablab.ai slug found (`t_ying_yai/...` and `t-ying-yai/...`
  both 404). No GitHub repo found via search. Genuinely unverifiable —
  marked as such, not guessed from the name.

### Ligs-Attempt-276 (#5, RLSym) — repo read
- GitHub: `github.com/source2destination/act2-agent` (confirmed real, C#,
  pushed 2026-07-07). README is thin, but the code itself is the strongest
  primary source of any competitor found this session.
- **Architecture, confirmed by reading `src/Harness.cs` and
  `src/HarnessProgram.cs` directly**: the shipped harness's own top-of-file
  comment states it plainly: *"v1 strategy: remote-only through the proxy...
  The local-ensemble rung slots in at the marked point once judging-VM
  hardware is known."* — i.e. **the public, submitted image has no local
  model at all**; a local tier was planned but is not in what's shipped.
  Every task is answered by exactly one Fireworks call (model chosen from
  `ALLOWED_MODELS` by a hardcoded family-preference list, with a
  code-specialist override for code categories), with one retry only on a
  *transient* failure (timeout/error) — never a retry or check on a
  *wrong* answer. No deterministic verification of any kind. A separate
  comment notes the team's actual "classifier/analyzer/costsweep/baselines"
  tooling is **deliberately excluded** from the public repo ("the public
  image must be assumed decompiled") — so whatever routing sophistication
  they have is intentionally not publishable, and what's readable is
  category-tuned prompts only.

### Minima (#6, Tech debt) — repo read
- GitHub: `github.com/Stephen-Kimoi/fine-tune-llm-query-router-amd`
  (confirmed real, Python, pushed 2026-07-07; also a public lablab.ai
  tutorial, "Fine-Tune a Query Router to Cut LLM Costs"). Read the README
  and `agent.py` in full — this is the most substantively different
  architecture of anything found.
- **Architecture, confirmed by reading the actual entrypoint code**: a
  fine-tuned **DistilBERT** (66M params) binary easy/hard classifier —
  actual gradient-trained ML, not prompt heuristics — runs locally for free
  and picks `MODEL_CHEAP` vs `MODEL_EXPENSIVE`. But `agent.py`'s own
  docstring says it plainly: *"all answer-generating calls go through
  FIREWORKS_BASE_URL... the router itself runs locally and costs zero
  tokens"* — **every single task still makes a real, counted Fireworks
  call**; the fine-tuned model only chooses *which* tier, never answers
  anything itself, and there is no verification/re-derivation of the
  answer once it comes back.
- Their own README volunteers an unusually candid limitation, worth citing
  directly: the labeled dataset is "heavily skewed (80 easy / 3 hard out of
  83 queries)... there's barely an accuracy gap to route around" for their
  chosen model pair — i.e. by their own admission, smart tier-selection
  barely matters for this task distribution, because most queries are easy
  for either tier. That's a real, independent data point (not ours)
  consistent with the idea that the bigger lever is avoiding the remote
  call *entirely* on easy tasks (our zero-token local-first shape), not
  picking which paid tier answers them.

### ApexFlow AI: Self-Healing Telemetry Gateway (#7, Tarek Clarke) — repo read, richest find
- GitHub: `github.com/tarek-clarke/resilient-rap-framework`, `amd-hackathon`
  branch (confirmed real; **repo created January 2026**, i.e. it predates
  the hackathon's July 6 kickoff by 6 months — this is a pre-existing PhD
  research codebase, per the README's own "Academic Context" section,
  Tarek Clarke's active PhD thesis on resilient stream integration
  pipelines at TalTech, with a `track1_agent/` folder bolted on for this
  hackathon). Read the README and `track1_agent/agent.py` in full — this
  is the only qualified team whose actual judged Track-1 entrypoint code
  was fully readable.
- **The README claims an "11-qubit Variational Quantum Classifier (VQC)
  trained on a physical 156-qubit IBM Heron r2 QPU" routes tasks, for
  "exactly $0 remote tokens."** Reading `agent.py` line by line shows this
  claim does not match the shipped control flow:
  - `BinaryQuantumRouter.route()` really does run a Qiskit VQC circuit (or
    a classical fallback) and returns a `(local|remote, confidence)`
    decision, and `process_task()` computes it and **prints** it — but then
    **never branches on it**. The actual routing is a hardcoded category
    check: `SIMPLE_CATEGORIES = {factual, sentiment, summarisation, ner}` →
    try local Gemma GGUF (1B/4B via llama-cpp-python) first, escalate to
    Fireworks only if the local answer is `< 10` characters or empty;
    `COMPLEX_CATEGORIES = {math, code_debug, code_gen, logic}` → **always**
    remote, no local attempt ever made. The quantum router's output is
    dead code as far as this function is concerned.
  - There's also a fully-built `local_eval()` — a 0.0–1.0 category-aware
    quality scorer (checks for numeric answers on math, code fences on
    code, entity-type words on NER, etc.) — that is likewise **never
    called** anywhere in the visible `process_task`/`main` pipeline. Two
    separate, non-trivial pieces of "verification-shaped" machinery exist
    in the file and are not wired up.
  - The one verification step that **is** live, for `COMPLEX_CATEGORIES`,
    is inside `run_remote_model()`: after getting an answer, it sends the
    question and that answer **back to the same remote model** with the
    prompt *"Check your answer carefully. If it is correct, return it
    unchanged. If there are errors, fix them"* — a second paid call, same
    model, asking itself "are you sure?" This is a concrete, code-verified
    instance of exactly the **LLM-self-judgment pattern** our own design
    (V7) argues against in favor of deterministic re-derivation — not a
    speculative comparison, this is what their shipped code does for every
    math/logic/code task.
  - Net read: ApexFlow is the one competitor that structurally resembles
    us most (real local model, real local-first attempt on a task subset,
    zero-token intent) — but its "verification" for the categories that
    matter most (math, logic, code) is same-model self-review, not
    execution/solving, and its most-marketed differentiator (quantum
    routing) doesn't actually gate anything in the code as shipped. Its
    89.5% accuracy (the one outlier above the 84.2% floor) is plausibly
    explained by that expensive complex-category path (local Gemma +
    always-remote + self-verify pass) rather than by the quantum router,
    which this reading shows contributes nothing to correctness.

### Adam dev teams / our own entry (#8)
Not researched here — that's us.

## 3. Broader field context (from the main hackathon page, not competitor-specific)

A direct fetch of the main Track 1 listing page (not just the /live
leaderboard) surfaced roughly 25 other Track 1 submission names/blurbs
beyond our 8 (e.g. "Zero-Token Routing Agent" — "solves math, logic, and
code locally with a small Gemma model and verified execution"; "ZMLC+
Local-First Token Router" — "separates deterministic/verifiable tasks from
lossy ones using rules, verifiers, and optional local inference"; "R-A-T-W-
I-G" — "a deterministic-first Track 1 hybrid agent"). These are one-line
blurbs only, not read as code, and none of them are among our 8 qualified
peers — but they establish that **"local-first + some notion of
deterministic verification" is a shared vocabulary across many entrants in
this specific hackathon**, not a name-only coincidence. This matters for
calibration: the idea's *framing* ("verify deterministically, don't just
trust the model") is clearly not unique to us at the level of a one-line
pitch. What we could not determine for any of these ~25 (no code read) is
whether "verified execution" or "verifiers" in their blurbs means actual
re-derivation (program-executes-the-math, solver-solves-the-logic) or just
a length/format check dressed in that language — which is exactly the gap
this research closed for ApexFlow specifically (their "verification"
language in spirit vs. what the code does are two different things).

## 4. Answering the actual question: is "deterministic re-derivation, not
## LLM self-judgment" something we have evidence competitors AREN'T doing?

Honest answer, not oversold:

**For 2 of 8 qualified peers (NovaAI, Ligs-Attempt-276/act2-agent), yes —
directly confirmed by reading their shipped code.** Neither has any
verification step of any kind, deterministic or LLM-based. Both are pure
"classify once, call one remote model once, ship the answer" architectures.
This is the plainest possible contrast with our cascade.

**For 1 of 8 (Minima), yes on a related axis — confirmed by reading their
shipped code.** They never attempt a free local answer at all (every task
pays a Fireworks call); their local computation is ML-based *tier
selection*, not answer verification. So "deterministic re-derivation of the
answer" doesn't apply to them because there's no local answer to verify —
but it does mean our zero-token-first shape is a real structural difference
from theirs, not just branding.

**For 1 of 8 (ApexFlow, the accuracy outlier), the answer is genuinely
mixed and the most interesting finding of this research.** They DO have a
real local-first path for simple categories, but their verification is a
length check, not correctness-checking, and for the categories where
correctness is hardest (math, logic, code) their one "verification" step is
literally the same-model-asks-itself-are-you-sure pattern our design
explicitly rejects. So: **on this specific axis (deterministic re-derivation
vs. LLM self-judgment), we have direct, code-verified evidence that our
approach differs from the one team that comes structurally closest to us.**

**For 4 of 8 (Route AI, TokenForge Router, Adaptive Routing Agent, and
partially Route AI's empty repo), the honest answer is we cannot tell.**
Route AI's linked repo exists but is empty (no code shipped publicly, or
not yet pushed) — rank #1 on the leaderboard is *not* readable, which is
worth sitting with: the actual top performer is the one competitor whose
approach is completely opaque to us. TokenForge Router and Adaptive Routing
Agent could not be located at all (no working lablab.ai page, no GitHub
repo found via search) — genuinely closed, not merely "we assume they're
generic." No architecture claim is made about these three.

**So: "we have specific evidence, not just an assumption" is true for half
the field (4 of 8) and false/unknowable for the other half — including the
#1 team.** The right framing for the submission narrative is not "nobody
else does deterministic verification" (unfalsifiable and half-contradicted
by our own findings — the ~25-name field survey shows plenty of entrants
using "verified"/"deterministic" language, even if we can't confirm what
that means in code for most of them) — the right framing is the narrower,
fully defensible claim: *for the specific peers whose code we could read,
none combine (a) a genuinely free zero-token local-first attempt with (b)
correctness verification by independent re-derivation (program execution
for math, constraint solving for logic) rather than model self-review.*
That claim is true, checkable, and doesn't require knowing what the
unreadable half of the field is doing.

## 5. What actually IS fully verifiable, regardless of competitors: our own
## measured rigor this session (V21–V24)

Per the user's framing — pivot to what we control. This is not new research,
it's the concrete, dated evidence already sitting in `research/VERDICTS.md`
from earlier today (2026-07-09), restated here because it's the strongest
plank of the "how are we different" answer that needs zero assumptions
about anyone else:

- **V21**: found and fixed a real correctness gap in our own code verifier —
  the old check only proved generated code "doesn't crash as a script," not
  that it's logically correct (`def get_max(nums): return nums[0]` passed
  the old check). Fixed with spec-derived `assert` generation, tri-state
  (never regresses below the old floor), hardened again in V24 against
  over-aggressive demotion per fresh literature (CodeT, 2602.10522,
  2603.28653) on the unreliability of single-candidate LLM-generated tests.
- **V22**: the 228-task benchmark's `logical_reasoning` strict score was
  suppressed at 57% by a labeling-format bug in *our own answer formatter*
  (`"Position N"` vs. the puzzle's own vocabulary — day names, ordinals,
  seat numbers, day ranges) — the CSP solver's actual reasoning was correct
  in every single one of the 8 originally-failing cases. Fixed across three
  rounds (each round caught by re-running the fix and reading real
  failures, not trusting a re-score), landing at **76% strict / 92% solver
  route accuracy**, up from 57%/5-13.
- **V23/V24**: an independent second-pass audit found and fixed 7 wrong
  dataset gold answers (grok-sourced math golds, independently
  recomputed), found the earlier "math capability gap" claim was itself
  wrong (self-corrected same day: only 3 of 10 "failures" were real agent
  errors, all via a rate-limited dev-only fallback route — the shipped
  `local+program` verification route went **28/28, a perfect record**, on
  the corrected golds), and closed with a hardcode-compliance grep audit
  (clean: no task-specific strings in `agent/`, all config env-read at
  runtime).

None of that requires knowing anything about the other 7 teams. It's
falsifiable, it's dated, it's in the repo, and it demonstrates the kind of
scrutiny ("read the actual failing example before trusting the score, twice
independently") that the competitive research above shows at least 3 of 4
readable competitor codebases did not visibly apply to their own
verification claims (dead-code quantum router and dead-code quality scorer
in ApexFlow; no verification code at all in NovaAI/act2-agent).

## 6. Honest verdict

**Is our architecture unique? No — and the evidence for that is now better
than "we assume," it's a field survey: dozens of Track 1 entrants use
"local-first," "deterministic," and "verified" in their own pitches. The
idea is shared vocabulary in this specific hackathon.**

**Is "deterministic re-derivation instead of LLM self-judgment" something we
can show, with code, that at least some real qualified competitors are NOT
doing? Yes, for 4 of the 7 other qualified teams (NovaAI: no verification
at all; Ligs-Attempt-276: no verification at all, remote-only by the
maintainers' own comment; Minima: no local answer to verify at all; ApexFlow:
real local-first but correctness-checking that's a length heuristic for
easy tasks and same-model self-review for hard ones — the exact anti-pattern
our design targets). That is a genuinely defensible, source-cited claim, not
a hallucinated one, and ApexFlow in particular is a strong, concrete,
apples-to-apples contrast because they are the single most architecturally
similar team we could actually read.**

**Is it something we can claim about the whole field, including the #1 team?
No, and don't. Route AI (rank 1) links to an empty repo. TokenForge Router
(rank 2) and Adaptive Routing Agent (rank 4) could not be found at all.
Half the leaderboard above us is genuinely opaque. Overclaiming "nobody else
does this" would be false on its face given the ~25-name field survey's own
language, and unfalsifiable for the specific teams we're actually racing.**

**The number that should carry the most weight in the next few hours is not
the differentiation story — it's rank. We are 8th of 8 qualified teams, at
27,459 tokens against a tight 4,268–5,423 cluster for the top 6. All 6 of
those teams, plus us, sit at the identical 84.2% accuracy floor — meaning
the entire visible gap to rank 1 (23,191 tokens) is pure token-efficiency
execution, not an accuracy tradeoff we're making on purpose. Architectural
superiority on paper (a genuine zero-token local-first cascade, when
NovaAI/Minima/act2-agent always pay for at least one remote call per task)
has not yet shown up in our own leaderboard result. Something in our current
config/routing is escalating far more than the design intends, or far more
than it needs to for this specific accuracy floor. That gap is fully within
our control to close before the 4PM UTC deadline tomorrow, and closing it
would matter more to the outcome than any competitive-differentiation
narrative — the differentiation story is a fine thing to have ready for a
README/video, but it does not move rank; tokens do.**

**Bottom line for "how are we different," usable without overclaiming:**
*"Where we could read competitor code, we found either no verification step
at all, or a verification step that asks the same model to grade itself.
Ours re-executes: program-checks the math, solves the logic with a CSP
solver, and only escalates on a real, checkable disagreement. We can't say
that about the whole field — half the teams above us on the leaderboard are
closed-source or unreachable, including the #1 team — but we can say it,
with citations, about the specific competitors whose code we actually read.
Separately and unconditionally: we have our own dated record of finding and
fixing real bugs in our own measurement (a code verifier that didn't check
correctness, a labeling bug that hid a working solver's real 92% behind a
57% score, 7 wrong dataset golds) — that rigor is true regardless of what
anyone else built, and it's the more defensible half of the pitch tonight."*
