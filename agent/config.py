"""Runtime configuration. Everything comes from the environment — the judging
harness injects the real values; a local .env (never shipped) covers dev."""
import os

FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY", "")
FIREWORKS_BASE_URL = os.environ.get("FIREWORKS_BASE_URL", "https://api.fireworks.ai/inference/v1")
ALLOWED_MODELS = [m.strip() for m in os.environ.get("ALLOWED_MODELS", "").split(",") if m.strip()]

# Escalation preference. Non-reasoning models first: a reasoning model's thinking
# trace bills as output tokens, which is what we're ranked on. Code specialist
# is preferred for the two code categories (see router.pick_model).
REMOTE_PREFERENCE = [
    "gemma-4-31b-it",
    "gemma-4-31b-it-nvfp4",
    "gemma-4-26b-a4b-it",
    "kimi-k2p7-code",
    "minimax-m3",
]
CODE_PREFERENCE = ["kimi-k2p7-code"] + REMOTE_PREFERENCE

# Local llama.cpp server (OpenAI-compatible). Started by the container entrypoint;
# if it isn't up, the router simply escalates everything.
LOCAL_BASE_URL = os.environ.get("LOCAL_BASE_URL", "http://127.0.0.1:8080/v1")
LOCAL_MODEL_NAME = os.environ.get("LOCAL_MODEL_NAME", "local")

INPUT_PATH = os.environ.get("INPUT_PATH", "/input/tasks.json")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/results.json")

# 10-minute hard cap on the judging VM; keep headroom for startup + write-out.
TOTAL_BUDGET_S = float(os.environ.get("TOTAL_BUDGET_S", "540"))
REQUEST_TIMEOUT_S = float(os.environ.get("REQUEST_TIMEOUT_S", "25"))  # <30s/request rule
