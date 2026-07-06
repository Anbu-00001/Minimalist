"""Local model client (llama.cpp server, OpenAI-compatible, on localhost).
Local tokens score zero, so this is always worth trying first. Degrades
gracefully: if the server isn't running, available() is False and the router
escalates everything."""
import httpx
from openai import OpenAI

from . import config

_client = None
_available: bool | None = None


def available() -> bool:
    global _available
    if _available is None:
        try:
            httpx.get(config.LOCAL_BASE_URL.replace("/v1", "/health"), timeout=2.0)
            _available = True
        except Exception:
            _available = False
    return _available


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key="unused",
            base_url=config.LOCAL_BASE_URL,
            timeout=config.REQUEST_TIMEOUT_S,
            max_retries=0,
        )
    return _client


def complete(prompt: str, max_tokens: int = 768, system: str | None = None,
             temperature: float = 0.0) -> str | None:
    if not available():
        return None
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        resp = _get_client().chat.completions.create(
            model=config.LOCAL_MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except Exception:
        return None
    text = resp.choices[0].message.content or ""
    return text.strip() or None
