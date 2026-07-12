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

# Hard output caps for remote calls — every output token costs leaderboard
# rank, and Gemma-4's default prior is verbose (VERDICTS V3).
REMOTE_MAX_TOKENS = {
    "sentiment_classification": 48,
    "named_entity_recognition": 256,
    "factual_knowledge": 256,  # remote-first now; a truncated answer judges as wrong
    "text_summarisation": 256,
    "logical_reasoning": 192,
    "mathematical_reasoning": 320,
    "code_debugging": 640,
    "code_generation": 640,
}

# Local llama.cpp server (OpenAI-compatible). Started by the container entrypoint;
# if it isn't up, the router simply escalates everything.
LOCAL_BASE_URL = os.environ.get("LOCAL_BASE_URL", "http://127.0.0.1:8080/v1")
LOCAL_MODEL_NAME = os.environ.get("LOCAL_MODEL_NAME", "local")

INPUT_PATH = os.environ.get("INPUT_PATH", "/input/tasks.json")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/results.json")

# 10-minute hard cap on the judging VM; keep headroom for startup + write-out.
TOTAL_BUDGET_S = float(os.environ.get("TOTAL_BUDGET_S", "540"))
REQUEST_TIMEOUT_S = float(os.environ.get("REQUEST_TIMEOUT_S", "25"))  # <30s/request rule

# Local-dominant mode: route every category through the local model and ship
# its best (verifier-improved) answer instead of ever paying a remote call.
# The free local overrides (math program-check, logic CSP solver,
# self-consistency) still run and still improve answers — only the paid
# escalation is suppressed. Near-zero scored tokens; trades a little accuracy
# on the hard tail for a decisive token-rank gain (2026-07-12: real grader
# put remote-first at 8,282 tokens / rank 55 — winning needs local dominance).
# Defaults off so it can never alter the shipped image unless explicitly set.
LOCAL_ONLY = os.environ.get("LOCAL_ONLY", "").lower() in ("1", "true", "yes")

# Categories that STILL escalate to remote even under LOCAL_ONLY — the
# carve-out for tasks where a local failure is a hard, unrecoverable loss the
# free verifiers can't rescue. code_generation/code_debugging measured 3/7
# "Unable to answer." under pure LOCAL_ONLY (batch1, 2026-07-12): the local
# model either emits no parseable code or times out, and unlike math/logic
# there is no zero-token solver to fall back on. Escalating only these keeps
# the expensive-but-decisive code answers while every other category stays
# free. Comma-separated env override; empty string = pure LOCAL_ONLY.
LOCAL_ONLY_ESCALATE = set(
    c.strip() for c in os.environ.get(
        "LOCAL_ONLY_ESCALATE", "code_generation,code_debugging").split(",")
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


# Caps sized to ~2.5 tok/s real-server decode (research/local_cap_feasibility.md
# measured factual@80 -> 36s and NER@112 -> 40s, both OVER the 25s budget).
# Halved to fit, and paired with a terse local PROMPT_HINT so the answer comes
# out short-COMPLETE rather than truncated mid-content.
LOCAL_GEN_CAP = {
    "factual_knowledge": _cap_env("LOCAL_CAP_FACTUAL", 56),
    "named_entity_recognition": _cap_env("LOCAL_CAP_NER", 64),
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
