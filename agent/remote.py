"""Fireworks client. Every call goes through FIREWORKS_BASE_URL (the judging
proxy) — bypassing it invalidates the submission. Tracks scored token usage."""
import time
from collections import deque

from openai import OpenAI

from . import config

_client = None
usage = {"input_tokens": 0, "output_tokens": 0, "calls": 0}
_call_times: deque[float] = deque()


def _throttle() -> None:
    """Sliding-window wait for config.REMOTE_RPM_LIMIT (dev-only; see config.py)."""
    if config.REMOTE_RPM_LIMIT is None:
        return
    now = time.monotonic()
    while _call_times and now - _call_times[0] > 60:
        _call_times.popleft()
    if len(_call_times) >= config.REMOTE_RPM_LIMIT:
        time.sleep(60 - (now - _call_times[0]) + 0.1)
    _call_times.append(time.monotonic())


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=config.FIREWORKS_API_KEY,
            base_url=config.FIREWORKS_BASE_URL,
            timeout=config.REQUEST_TIMEOUT_S,
            max_retries=1,
        )
    return _client


def complete(prompt: str, model: str, max_tokens: int = 512,
             system: str | None = None) -> str | None:
    """One remote completion. Returns text, or None on failure (caller decides
    the fallback — never raise past this point during a scored run)."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    _throttle()
    try:
        resp = _get_client().chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0,
        )
    except Exception:
        return None
    if resp.usage:
        usage["input_tokens"] += resp.usage.prompt_tokens or 0
        usage["output_tokens"] += resp.usage.completion_tokens or 0
    usage["calls"] += 1
    text = resp.choices[0].message.content or ""
    return text.strip() or None
