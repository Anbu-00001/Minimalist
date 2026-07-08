# lablab.ai submission — copy-paste fields (Track 1)

## Project Title

AMDA — Verify-Local-First Routing Agent

## Short Description (one paragraph)

A Track 1 agent that treats remote tokens as the scarcest resource in the
game. Every task runs on a baked-in local model first (zero token cost); a
layer of *deterministic verifiers* — code execution, independent program
re-derivation for math, a constraint solver for logic puzzles, label
validation, format checks, JSON schema parsing — decides whether the free
answer is provably good enough. Only tasks that demonstrably fail
verification escalate to Fireworks, and even those answers get audited for
free before we trust them.

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
   hint.
2. **Solve locally & verify deterministically** — a quantized model served by
   llama.cpp inside the container answers first. Then, instead of trusting it,
   we *check* it with code: generated/debugged Python is extracted with a
   parser-oracle (EvalPlus-style longest-valid-segment) and executed; math
   answers are re-derived by independently translating the word problem into
   an arithmetic expression and executing it — a check the reference eval
   frameworks (lighteval, lm-evaluation-harness) don't have; logic puzzles
   are translated into declarative constraints and handed to a CSP solver
   (the Logic-LM/SatLM pattern — translation is extraction, solving is
   exact), whose unique solution can both verify and *supply* the answer;
   sentiment labels are re-read under a constrained grammar; summaries are
   checked against word/sentence constraints from the prompt; NER output is
   generated under a JSON grammar so it cannot be malformed. A verified
   local answer costs zero tokens; for genuinely uncheckable categories a
   self-consistency probe stands in.
3. **Escalate surgically** — only verification failures go to Fireworks,
   through the judging proxy, in a measured preference order (thinking-mode
   models last: they bill their reasoning traces as output tokens — poison
   for a token-ranked leaderboard). Escalated answers aren't blindly
   trusted either: the same free local re-derivation audits the paid answer
   (CRITIC pattern, ICLR 2024), and a grounded disagreement buys one shot
   at the fallback model.

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
- Public GitHub repo URL — https://github.com/Anbu-00001/AMDA (make public!)
- Application URL / demo platform — GHCR image URL
  (ghcr.io/anbu-00001/amda-agent:latest — flip package to PUBLIC before submitting)
