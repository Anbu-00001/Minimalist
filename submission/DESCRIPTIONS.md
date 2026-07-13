# lablab.ai submission — copy-paste fields (Track 1)

## Project Title

AMDA — Local-Dominant Verified Routing Agent

## Short Description (one paragraph)

A Track 1 agent that treats remote tokens as the scarcest resource in the
game — and pays them on exactly one condition. All eight categories run on
a baked-in local model (zero token cost): math answers are *computed*, not
generated (the model emits a short arithmetic expression, we execute it);
logic answers are checked — and can be overridden — by a constraint solver;
code is extracted with a parser-oracle, executed, and tested against
model-written assertions. Only a code answer that demonstrably fails that
verification buys a single capped Fireworks call. Everything else ships
free, in answer shapes tuned and re-validated on a 228-task private dev set.

## Long Description

**The insight.** Track 1 ranks accuracy-gate survivors by total proxy-recorded
tokens, and local inference counts as zero. So the winning agent isn't the one
with the best prompts — it's the one that *knows when its free answer is
already correct*. Confidence, not capability, is the scarce resource.

The academic lineage here is the LLM cascade (FrugalGPT, Chen et al. 2023:
"match the performance of the best individual LLM with up to 98% cost
reduction"). The strongest published critique of cascades — that they are
"limited primarily by structural cost, since cascades pay the cheap model
before any escalation decision" (Bouchard 2026) — is structurally
neutralized by this competition's rules: our cheap model's tokens are
scored at zero. Track 1 is the exact regime where the cascade dominates.

**The architecture.** AMDA is a three-stage cascade:

1. **Classify** — a keyword-rule classifier (no LLM, no tokens) tags each task
   with one of the 8 categories and selects a category-specific answer format
   hint. Tasks are then solved cheapest-category-first, so a time-budget
   squeeze can never cost more than the slowest tail.
2. **Solve locally, compute where possible, verify deterministically** — a
   quantized model served by llama.cpp inside the container answers
   everything, with per-category decode caps sized so every generation
   finishes on 2 vCPUs. Math never decodes a derivation at all: the model
   emits a ~20-token arithmetic expression, we execute it and ship the exact
   value (PAL-style, with rounding instructions honored) — a path that
   scored 7/7 on dev math at zero tokens. Logic puzzles are translated into
   declarative constraints for a CSP solver (the Logic-LM/SatLM pattern),
   whose unique solution can both verify and *override* the free-form
   answer. Generated/debugged code is extracted with a parser-oracle
   (EvalPlus-style longest-valid-segment), executed, and tested against
   assertions the model writes from the spec alone — plus a fence-parity
   guard that catches truncated code a syntax check would miss. NER decodes
   under a JSON grammar when JSON is requested, so it cannot be malformed.
3. **Escalate surgically** — the ONLY paid path: a code answer that
   demonstrably fails verification buys one capped Fireworks call through
   the judging proxy (Gemma-4 first; thinking-mode models last, since they
   bill reasoning traces as output tokens — poison on a token-ranked
   leaderboard). Every other category ships its local answer, full stop.
   Expected scored-token bill for a clean run: **zero**.

**Evaluation-driven.** We built a 228-task private dev set spanning all 8
categories from five independent generators — including fully synthetic tasks
whose gold answers are *computed* (arithmetic evaluated, logic puzzles
brute-forced, NER entities injected) so gold labels cannot be wrong — plus a
deterministic judge measuring exactly what the leaderboard measures: accuracy
and tokens. Every routing threshold in the agent is set from measurements,
not vibes.

**Compliance.** Reads /input/tasks.json, writes /output/results.json, exits 0.
All Fireworks calls go through FIREWORKS_BASE_URL with models from
ALLOWED_MODELS, read from the environment at runtime. linux/amd64 image,
under 10GB, boots in seconds, degrades gracefully to remote-only if the local
server fails.

## Technology & Category Tags (suggested)

Python, llama.cpp, Fireworks AI, Docker, AMD, agents, routing, token-efficiency

## Fields still needed at submit time

- Cover image (1:1.6-ish landscape PNG) — TODO
- Video presentation URL (YouTube unlisted) — script in VIDEO_SCRIPT.md
- Slide presentation (PDF) — outline in SLIDES_OUTLINE.md
- Public GitHub repo URL — https://github.com/Anbu-00001/Minimalist (public ✓)
- Application URL / demo platform — GHCR image URL
  (ghcr.io/anbu-00001/amda-agent:latest (public ✓, anonymous pull verified))
