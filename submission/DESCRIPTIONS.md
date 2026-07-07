# lablab.ai submission — copy-paste fields (Track 1)

## Project Title

AMDA — Verify-Local-First Routing Agent

## Short Description (one paragraph)

A Track 1 agent that treats remote tokens as the scarcest resource in the
game. Every task runs on a baked-in local model first (zero token cost); a
layer of *deterministic verifiers* — code execution, label validation, format
checks, JSON schema parsing — decides whether the free answer is provably good
enough. Only tasks that demonstrably fail verification escalate to Fireworks,
routed to the cheapest-capable allowed model for their category.

## Long Description

**The insight.** Track 1 ranks accuracy-gate survivors by total proxy-recorded
tokens, and local inference counts as zero. So the winning agent isn't the one
with the best prompts — it's the one that *knows when its free answer is
already correct*. Confidence, not capability, is the scarce resource.

**The architecture.** AMDA is a three-stage cascade:

1. **Classify** — a keyword-rule classifier (no LLM, no tokens) tags each task
   with one of the 8 categories and selects a category-specific answer format
   hint.
2. **Solve locally & verify deterministically** — a quantized model served by
   llama.cpp inside the container answers first. Then, instead of trusting it,
   we *check* it with code: generated/debugged Python is syntax-checked and
   executed; sentiment labels are validated against the allowed set;
   summaries are checked against word/sentence/bullet constraints extracted
   from the prompt; NER output is parsed against the requested JSON schema.
   A verified local answer costs zero tokens, and for genuinely uncheckable
   categories a self-consistency probe (second sample, agreement threshold)
   stands in for verification.
3. **Escalate surgically** — only verification failures go to Fireworks,
   through the judging proxy, to a model chosen per category: a code
   specialist for code tasks, the strongest non-reasoning generalist
   elsewhere (reasoning models bill their thinking traces as output tokens —
   poison for a token-ranked leaderboard).

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
