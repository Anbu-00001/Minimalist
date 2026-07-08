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
             temperature: float = 0.0, grammar: str | None = None) -> str | None:
    """`grammar` is a llama.cpp GBNF string, passed via the server's
    per-request `grammar` field (tools/server/README.md). Ignored by
    non-llama backends, which merely won't constrain."""
    text, _ = complete_scored(prompt, max_tokens=max_tokens, system=system,
                              temperature=temperature, grammar=grammar)
    return text


def complete_scored(prompt: str, max_tokens: int = 768, system: str | None = None,
                    temperature: float = 0.0, grammar: str | None = None,
                    ) -> tuple[str | None, float | None]:
    """Like complete(), but also returns the mean token logprob of the
    generation — a free confidence signal (VERDICTS V17). Confidence is None
    when the backend returns no logprobs; callers must treat that as
    "no signal", never as low confidence."""
    if not available():
        return None, None
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    extra = {"grammar": grammar} if grammar else {}
    try:
        resp = _get_client().chat.completions.create(
            model=config.LOCAL_MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            logprobs=True,
            extra_body=extra,
        )
    except Exception:
        return None, None
    text = (resp.choices[0].message.content or "").strip()
    lp = getattr(resp.choices[0], "logprobs", None)
    confidence = None
    if lp and getattr(lp, "content", None):
        vals = [t.logprob for t in lp.content if t.logprob is not None]
        if vals:
            confidence = sum(vals) / len(vals)
    return (text or None), confidence
