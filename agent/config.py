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
