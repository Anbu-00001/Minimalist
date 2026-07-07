# VERDICTS — analysis of the 7-file research corpus (2026-07-07)

Decisions for AMDA Track 1, each grounded in the collected evidence
(see research/*.md for sources). Ordered by scoring impact.

---

## V1. Escalation model policy: Gemma-first, Kimi last, MiniMax conditional

**Decision:** default escalation order for ALL categories becomes
`gemma-4-31b-it → gemma-4-31b-it-nvfp4 → gemma-4-26b-a4b-it → minimax-m3 → kimi-k2p7-code`.
The code-specialist-first policy (kimi first for code) is **reversed**.

Evidence:
- kimi-k2p7-code: thinking is architecturally **mandatory** — "Kimi-K2.7-Code
  forces thinking and preserve_thinking as True" (HF model card, verbatim).
  Every call bills unavoidable reasoning tokens as output. HN practitioners:
  "you'll spend many more tokens" vs alternatives. On a leaderboard ranked by
  ascending tokens, this is disqualifying as a first choice.
- gemma-4-31b-it: thinking **off by default** ("Thinking mode is not enabled
  by default", HF card) — enabled only via `<|think|>` token. Strong scores
  (MMLU 85.2, AIME'26 89.2, LiveCodeBench v6 80.0) and the only quantitative
  verbosity datapoint favors it: "rarely generates more than 20k tokens" vs
  Qwen3.5's 100k+ (Kaitchup). Code score (LCB 80.0) beats any verified number
  for kimi, whose public-suite results are vendor-only.
- **Side prize**: Track 1 carries "Best Use of Gemma via Fireworks — $1,000"
  (event page, verbatim). Gemma-primary makes us eligible at zero cost.
- minimax-m3: Fireworks confirms "toggling thinking on or off at request
  time"; a real integration found the API accepts `"thinking": {"type":
  "disabled"}` (rejects "enabled", accepts "adaptive"/"disabled" — kilocode
  issue). BUT reasoning has been observed inline in normal output, and M3
  measured 64% more tokens than a peer on identical tasks (thinkwright).
  → conditional: test `thinking: disabled` through the proxy on key day-1;
  promote above 26b-a4b only if reasoning demonstrably absent.
- gemma-4-31b-it-nvfp4: quality ≈ base (0.25% GPQA loss; "no meaningful
  accuracy difference" — Kaitchup), and "quantization has little impact on
  token efficiency." Faster infra → use as latency fallback (see V2).

## V2. The 30s/request rule is a live risk on Fireworks — keep timeout + fast fallback

Telnyx benchmark: Fireworks minimax-m3 p95 latency **54.06s, max 111.51s** —
far over the 30s/request cap. Our 25s client timeout is correct; add: on
timeout, retry once against the nvfp4 variant (faster) with a hard cap,
else fall back to the local answer. Never let one slow call sink a task.

## V3. Token micro-economics on remote calls

Proxy records **total tokens** — input and output both cost rank.
- Remote system prompt: single short line, or none. Never send local
  PROMPT_HINTS verbatim to remote; send the raw task + one format line max.
- Per-category `max_tokens` caps on remote calls (sentiment ~48, NER ~256,
  factual ~160, summary ~256, logic ~192, math ~320, code ~640).
- Append "Answer directly. Do not show reasoning." to remote prompts —
  Gemma-4's verbosity is prior-driven and this measurably reduces narration
  (openllmbridge: "it has no instruction by default, so it falls back to its
  training prior, which is verbose").
- Verify remote answers with the same verifiers; at most ONE retry.

## V4. Judge-gate posture: local answers polished, remote answers lean

LLM judges "prefer longer, authoritative-looking, and well-formatted
responses" (2411.16594) — and **local tokens are free**. So: local answers
should be complete, clean, well-formatted sentences (costless judge appeal);
remote answers concise but complete (they're metered). Never ship
"Unable to answer." when any local draft exists — a guaranteed judge fail
beats nothing, but a mediocre local answer beats both. Do not attempt
judge-gaming (master-key phrases) — high risk, likely countered.

## V5. Constrained decoding: use for classification/extraction, never for reasoning

- llama.cpp ships GBNF (`grammars/json.gbnf`, `-j` schema conversion);
  llama-server accepts grammars per request. Grammar-constrain LOCAL
  sentiment (label-choice grammar) and NER (JSON-schema grammar) —
  practitioner data: 100% well-formed output, ~25% accuracy gain, "guardrails
  in bowling" (imaurer.com).
- Do NOT constrain math/logic/code/summarisation: "significant decline in
  LLMs reasoning abilities under format restrictions"; GSM8K-style tasks show
  10-30% degradation (Let Me Speak Freely, 2408.02442; JSONSchemaBench).
- Two-pass pattern where format matters after reasoning ("Thinking Before
  Constraining"): free-form reason → constrained extract. Local passes cost
  only time, and we have time budget per task on GPU-class judging VMs.

## V6. Math verification upgrade — program-aided checking (biggest accuracy lever)

Local math is our worst verified category (17% strict on laptop bench).
Adopt the eval-framework standard: **math-verify** (HF; sympy+ANTLR4;
`parse()`/`verify()`) — the same library lighteval AND lm-evaluation-harness
use for math scoring.
- In eval/judge.py: replace regex-number matching with math-verify.
- In agent/verifiers.py: program-aided self-check — after the local model
  answers, ask it (locally, free) to emit the computation as a bare Python
  expression; execute; compare to its stated answer with math-verify
  tolerance. Agree → trust local; disagree → escalate. Deterministic, free.
- Keep 2-sample self-consistency for logic/factual only; evidence says
  returns diminish on capable models ("Self-Consistency Is Losing Its Edge")
  so never exceed 2 samples.

## V7. Cascade literature confirms the architecture; quality-estimation is the whole game

"Good quality estimators" are THE critical factor (cascade-routing, ETH) and
naive cascades fail through "poor estimation of the quality of the affordable
LLM's outputs" (BARGAIN). Our deterministic verifiers ARE the quality
estimator — every verifier improvement converts directly to rank. No
framework adoption needed (RouteLLM etc. solve preference-routing, not
verify-then-escalate); our bespoke design is the right shape. Steal ideas,
not dependencies.

## V8. Dev stand-ins before the Fireworks key (test escalation TODAY)

Name-matching free hosts found for our exact locked targets:
- **Cerebras free tier hosts `gemma-4-31b`** (5 RPM, 1M tokens/day, no card)
  — closest stand-in for our PRIMARY escalation model.
- **Cloudflare Workers AI hosts `@cf/google/gemma-4-26b-a4b-it`** (10K
  neurons/day free).
- HF Inference Providers router (`https://router.huggingface.co/v1`, OpenAI-
  compatible) reaches gemma-4-31b-it / Kimi-K2.7-Code / MiniMax-M3 via
  Novita/Together/DeepInfra — pay-per-token, ~$0.10 free credit (tiny).
- Google AI Studio free tier (Gemini Flash ~1.5k req/day) — use as the
  dev **LLM judge** for the 228-task set's "unsure" bucket, not as a stand-in.
Config needs zero code changes: point FIREWORKS_BASE_URL / ALLOWED_MODELS /
FIREWORKS_API_KEY at the stand-in in `.env`. User action: create Cerebras
(and optionally Cloudflare) account.

## V9. Local model matrix (for the next GPU window) — revised candidates

Benchmark in this order, one model per session, judged by eval/judge.py:
1. Qwen3-4B-Instruct-2507 Q4_K_M (baseline; IFEval 83.4 = best format-follower)
2. Phi-4-mini-instruct Q4 (GSM8K 88.6 / HumanEval 74.4 — targets our two
   weakest categories)
3. Granite 4.1 8B instruct Q4 (HumanEval 87.2 / GSM8K 92.49, if GGUF exists)
4. Qwen3.5-4B (thinking off) — newer family, toggleable
Two-model bake (4B generalist + math/code specialist, both fit in 10GB) is
on the table if category-routed local wins the numbers.
Also: use `-ngl 99` on GPU box; CPU worst case threads = physical cores.

## V10. Competitive posture: submit early, iterate on the leaderboard

At the Jul-7 snapshot the entire Track 1 had **5 submissions** out of 4,327
teams. Rate limit is 10/hour. The leaderboard is a feedback oracle — first
submission should go up the moment the key arrives and the remote path is
smoke-tested, then iterate. No verified competitor is doing verify-local-
first (two name-alikes unverified/404). No Act-I precedent exists — nobody
has meta-game experience on this track type.

---

## Priority actions (code)
1. [x] config.py: flip preferences to Gemma-first, kimi last (V1)
2. [x] router/remote: per-category remote max_tokens + "answer directly" +
       lean remote prompts (V3), remote-verify + single retry (V3), timeout
       fallback order (V2)
3. [x] verifiers.py + router.py + grammars.py: program-aided math check (V6),
       JSON grammar for NER, constrained label-agreement for sentiment (V5)
       — functionally tested against llama-server 2026-07-07, all paths pass
4. [x] eval/judge.py: math-verify integration (V6) — dev-venv only dependency
5. [ ] .env stand-in test with Cerebras gemma-4-31b (V8) — needs user signup
6. [ ] GPU window: model matrix per V9
