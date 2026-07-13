"""Runtime configuration. Everything comes from the environment — the judging
harness injects the real values; a local .env (never shipped) covers dev."""
import os

FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY", "")
FIREWORKS_BASE_URL = os.environ.get("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")
ALLOWED_MODELS = [m.strip() for m in os.environ.get("ALLOWED_MODELS", "").split(",") if m.strip()]

# Escalation preference (research/VERDICTS.md V1). Gemma-first: thinking is
# off by default on Gemma-4 (HF card), it has the best measured verbosity
# profile of the five, and Gemma usage qualifies for a Track 1 side prize.
# kimi-k2p7-code goes LAST despite being the code specialist — its thinking
# mode is architecturally mandatory and bills as output tokens on every call.
# minimax-m3 stays below the Gemmas until `thinking: disabled` is proven to
# strip reasoning through the judging proxy (test on key day-1).
REMOTE_PREFERENCE = [
    "gemma-4-31b-it",
    "gemma-4-31b-it-nvfp4",
    "gemma-4-26b-a4b-it",
    "minimax-m3",
    "kimi-k2p7-code",
]
CODE_PREFERENCE = REMOTE_PREFERENCE  # mandatory thinking outweighs code specialty

# code is the ONLY category that still escalates under LOCAL_ONLY, so its
# output cap is the single biggest lever on the final token bill. Real code
# answers measured ~120-250 output tokens; 384 fits them with room while
# cutting the 640 tail (2026-07-12 token push, target <1500 scored tokens).
_CODE_CAP = int(os.environ.get("CODE_CAP", "384"))

# Hard output caps for remote calls — every output token costs leaderboard
# rank, and Gemma-4's default prior is verbose (VERDICTS V3).
REMOTE_MAX_TOKENS = {
    "sentiment_classification": 48,
    "named_entity_recognition": 256,
    "factual_knowledge": 256,  # remote-first now; a truncated answer judges as wrong
    "text_summarisation": 256,
    "logical_reasoning": 192,
    "mathematical_reasoning": 320,
    "code_debugging": _CODE_CAP,
    "code_generation": _CODE_CAP,
}

# Under LOCAL_ONLY only ONE remote model is attempted (no second-model
# fallback): a fallback doubles the scored-token bill for the one category
# that still pays, and the local answer is already there as a backstop.
LOCAL_ONLY_MAX_MODELS = int(os.environ.get("LOCAL_ONLY_MAX_MODELS", "1"))

# When a local generation returns EMPTY (decode timed out), retry locally with
# a tiny cap that is guaranteed to finish instead of falling through to a paid
# remote call. This is what turns "mostly local" into "only code ever pays" —
# the empty-timeout fallthrough was the hidden source of most remaining
# remote calls (measured 2026-07-12: 6 of batch2's escalations were empties).
LOCAL_RETRY_CAP = int(os.environ.get("LOCAL_RETRY_CAP", "40"))

# Local llama.cpp server (OpenAI-compatible). Started by the container entrypoint;
# if it isn't up, the router simply escalates everything.
LOCAL_BASE_URL = os.environ.get("LOCAL_BASE_URL", "http://127.0.0.1:8080/v1")
LOCAL_MODEL_NAME = os.environ.get("LOCAL_MODEL_NAME", "local")

INPUT_PATH = os.environ.get("INPUT_PATH", "/input/tasks.json")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/results.json")

# 10-minute hard cap on the judging VM; keep headroom for startup + write-out.
# 555 (was 540): local-dominant needs the extra 15s of working time, and the
# real margin still holds — external kill ~600s, server boot ~4s, incremental
# flush means write-out is already on disk at every instant.
TOTAL_BUDGET_S = float(os.environ.get("TOTAL_BUDGET_S", "555"))
REQUEST_TIMEOUT_S = float(os.environ.get("REQUEST_TIMEOUT_S", "25"))  # <30s/request rule

# LOCAL calls get a longer leash than remote: the <30s/request rule governs
# proxy requests, not our own in-container llama.cpp. On 2 vCPU the model
# decodes ~2.3-2.8 tok/s, so a 25s timeout silently truncates ANY local
# generation past ~55 tokens to EMPTY — measured 2026-07-12 as the root cause
# of both the phantom escalations (empty -> paid remote) and the math
# collapse (empty -> 40-token retry -> derivation cut before the answer,
# 1/7 dev). 50s admits ~110-token generations; per-category LOCAL_GEN_CAP
# keeps each one sized to finish well inside it.
LOCAL_REQUEST_TIMEOUT_S = float(os.environ.get("LOCAL_REQUEST_TIMEOUT_S", "70"))

# Local-dominant mode: route every category through the local model and ship
# its best (verifier-improved) answer instead of ever paying a remote call.
# The free local overrides (math program-check, logic CSP solver,
# self-consistency) still run and still improve answers — only the paid
# escalation is suppressed. Near-zero scored tokens; trades a little accuracy
# on the hard tail for a decisive token-rank gain (2026-07-12: real grader
# put remote-first at 8,282 tokens / rank 55 — winning needs local dominance).
# Defaults off so it can never alter the shipped image unless explicitly set.
LOCAL_ONLY = os.environ.get("LOCAL_ONLY", "").lower() in ("1", "true", "yes")

# Categories that STILL escalate to remote even under LOCAL_ONLY.
# Comma-separated env override; empty string = pure LOCAL_ONLY.
LOCAL_ONLY_ESCALATE = set(
    c.strip() for c in os.environ.get("LOCAL_ONLY_ESCALATE", "").split(",")
    if c.strip())
# EMPTY by default since 2026-07-12 evening — pure zero-token mode. The
# live leaderboard (research/endgame_leaderboard_state.md) showed (a) the
# real accuracy gate is ~50%, not the 84.2% this repo long believed, so
# local-only accuracy clears it with a wide cushion, and (b) NINE entries
# hold ranks 1-9 at exactly 0 tokens with rank 10 starting at 1,562 — one
# single escalation call therefore costs more rank than several wrong code
# answers. code_generation/code_debugging escalation (the previous default)
# remains available via env override for non-competition use.
# named_entity_recognition was in this set 2026-07-12 morning
# (research/cap2_ship_risks.md: capped-local NER dropped "Grammy Award",
# scored 4-5/7) — but that measurement ran under the TERSE local hint
# ("List only... No explanation"), and the model stopped VOLUNTARILY at 44
# of 64 tokens: the under-listing tracks the instruction, not the budget.
# Removed after switching the local NER hint to the completeness wording
# that already fixed the same failure on the remote path ("List every
# entity, including dates...") — re-validated on dev before ship. At ~640
# real tokens per proxy call and 2-3 NER tasks in the hidden set, NER
# escalation alone (~1,300-1,900 tokens) would sink the <1,500 target.

# Categories whose LOCAL attempt is skipped under LOCAL_ONLY (straight to
# remote). Empty by default: code_debugging sat here for a few hours on
# 2026-07-12 on the theory that its ~150-250-token corrected-program output
# couldn't decode in budget — but that was never actually measured failing
# (cap4's timeout placeholders were all code_generation), and the leaderboard
# shows a 0-token club at ranks 7-9, making every avoidable remote call a
# rank lost. A local-first debug attempt is free, gated by the same
# execution-verify + fence-parity truncation guard as codegen, and still
# escalates on failure via LOCAL_ONLY_ESCALATE — the remote call happens
# only when it actually buys accuracy.
LOCAL_SKIP = set(
    c.strip() for c in os.environ.get("LOCAL_SKIP", "").split(",")
    if c.strip())

# Per-category cap on LOCAL decode length. On 2 vCPU the model decodes at
# ~4 tok/s and SLOWS with depth (research/cpu_inference_speed.md §5), so an
# uncapped 768-token local generation for a short-input category (factual,
# NER) blows the 25s request budget and returns EMPTY — which then escalates,
# defeating the whole point of going local (measured 2026-07-12: 5/7 factual
# local generations returned len 0). A tight cap makes the generation finish
# in time and ship a short, correct local answer at zero scored tokens.
# Only categories with SHORT inputs benefit — summarisation's long-passage
# prefill is the bottleneck there, so it is not capped here (stays remote).
def _cap_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


# Caps sized to ~2.3-2.8 tok/s real-server decode
# (research/local_cap_feasibility.md measured factual@80 -> 36s and
# NER@112 -> 40s) against the 50s LOCAL_REQUEST_TIMEOUT_S, and paired with
# category PROMPT_HINTS so the answer comes out short-COMPLETE rather than
# truncated mid-content. EVERY local category is capped now: any uncapped
# generation (default 768) is guaranteed to hit the timeout, return empty,
# and either pay a remote call or ship a truncated retry — cap4's two
# failure modes (2026-07-12: 37-38s/task, math 1/7).
# mathematical_reasoning is absent on purpose: it doesn't free-generate —
# it goes through the expression-first program path in router.solve().
LOCAL_GEN_CAP = {
    "factual_knowledge": _cap_env("LOCAL_CAP_FACTUAL", 56),
    # 128, not 88: a JSON-grammar NER answer spends ~1.5x the tokens of the
    # line format (quotes/braces), and a 10-entity listing truncated mid-JSON
    # is an unparseable fail (measured 2026-07-12, Geneva task @88). The cap
    # only binds on long listings — the model stops at natural end otherwise.
    "named_entity_recognition": _cap_env("LOCAL_CAP_NER", 128),
    # 88, not 56: the 4B reasons step-by-step despite the "no working" hint,
    # and 56 cut one dev answer before it stated the full assignment
    # (gemini_logical_easy, 2026-07-12).
    "logical_reasoning": _cap_env("LOCAL_CAP_LOGIC", 88),
    # 88, not 64: 64 tokens ≈ 48 words — an "exactly 50 words" task was
    # physically unsatisfiable under it (dev, 2026-07-12). 88 ≈ 66 words.
    "text_summarisation": _cap_env("LOCAL_CAP_SUMM", 88),
    "sentiment_classification": _cap_env("LOCAL_CAP_SENT", 48),
    # 128 (was 104): the two longest dev codegen answers truncated mid-body
    # at 104 and the parser-oracle salvaged a runs-clean-but-gutted prefix
    # that shipped (2026-07-12 batch1). 128 tokens (~47s decode) covers both
    # of those answers (~105-125 tokens) while keeping headroom against a
    # loaded judging VM — several entries fell to TIMEOUT today; the fence-parity guard in router.solve() escalates
    # anything that still truncates.
    "code_generation": _cap_env("LOCAL_CAP_CODEGEN", 128),
    "code_debugging": _cap_env("LOCAL_CAP_CODEDBG", 128),
}

# Mean-token-logprob floor: an unverifiable local answer below it skips the
# self-consistency probe and escalates immediately (VERDICTS V17). None
# disables the gate. Set ONLY from measured dev-set calibration — see
# research/VERDICTS.md V17 for the distribution data behind the value.
LOGPROB_ESCALATE_BELOW: float | None = None

# Client-side throttle for dev-time remote testing against free-tier stand-ins
# (e.g. Cerebras' 5 RPM) that would otherwise return 429s indistinguishable
# from "model unavailable" and corrupt benchmark numbers with rate-limit
# noise rather than real accuracy signal. None = no throttling (the real
# Fireworks judging proxy has no such constraint; never set this for a
# submission run).
REMOTE_RPM_LIMIT: int | None = (
    int(os.environ["REMOTE_RPM_LIMIT"]) if os.environ.get("REMOTE_RPM_LIMIT") else None
)
