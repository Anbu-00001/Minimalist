"""The cascade: local first (free), verify, escalate only what fails.

Escalation policy per verdict:
  pass    -> keep local answer
  unknown -> keep local answer if self-consistent, else escalate
  fail    -> escalate to the preferred remote model for the category
"""
import time

from . import config, local_llm, remote
from .classify import classify
from .verifiers import verify

SYSTEM = "You are a precise assistant. Answer correctly and concisely. No preamble."

# category-specific nudges keep local answers in a shape the judge expects
PROMPT_HINTS = {
    "mathematical_reasoning": "\n\nWork step by step, then give the final answer on the last line as: ANSWER: <value>",
    "code_debugging": "\n\nIdentify the bug in one sentence, then give the full corrected code in a fenced block.",
    "code_generation": "\n\nReturn the complete function in a fenced code block.",
    "sentiment_classification": "\n\nState the sentiment label first, then a one-sentence justification.",
    "named_entity_recognition": "\n\nList each entity with its type. Use the exact format the task asks for.",
}


def pick_model(category: str) -> str | None:
    prefs = config.CODE_PREFERENCE if category.startswith("code") else config.REMOTE_PREFERENCE
    for m in prefs:
        if m in config.ALLOWED_MODELS:
            return m
    return config.ALLOWED_MODELS[0] if config.ALLOWED_MODELS else None


def _self_consistent(prompt: str, first: str) -> bool:
    """Second local sample at higher temperature; agreement = confidence."""
    second = local_llm.complete(prompt, system=SYSTEM, temperature=0.7)
    if not second:
        return False
    a, b = first.strip().lower(), second.strip().lower()
    if a == b:
        return True
    overlap = len(set(a.split()) & set(b.split())) / max(len(set(a.split()) | set(b.split())), 1)
    return overlap > 0.6


def solve(task: dict, deadline: float) -> dict:
    """Answer one task. Returns {task_id, answer, route, category} — route is
    diagnostic only and stripped before writing results."""
    prompt = task["prompt"]
    category = classify(prompt)
    full_prompt = prompt + PROMPT_HINTS.get(category, "")
    time_left = deadline - time.monotonic()

    answer, route = None, "none"

    if local_llm.available() and time_left > 60:
        answer = local_llm.complete(full_prompt, system=SYSTEM)
        if answer:
            verdict = verify(category, prompt, answer)
            if verdict == "pass":
                route = "local"
            elif verdict == "unknown" and time_left > 90 and _self_consistent(full_prompt, answer):
                route = "local+consistent"
            else:
                answer = None  # fail, or unconfident unknown -> escalate

    if answer is None:
        model = pick_model(category)
        if model:
            remote_answer = remote.complete(full_prompt, model=model, system=SYSTEM)
            if remote_answer:
                answer, route = remote_answer, f"remote:{model}"

    if answer is None:  # last resort: any local attempt beats an empty string
        answer = local_llm.complete(full_prompt, system=SYSTEM) or "Unable to answer."
        route = route if route != "none" else "fallback"

    return {"task_id": task["task_id"], "answer": answer, "route": route, "category": category}
