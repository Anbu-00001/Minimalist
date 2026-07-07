"""The cascade: local first (free), verify, escalate only what fails.

Escalation policy per verdict:
  pass    -> keep local answer
  unknown -> keep local answer if self-consistent, else escalate
  fail    -> escalate to the preferred remote model for the category
"""
import re
import time

from . import config, grammars, local_llm, remote
from .classify import classify
from .verifiers import (SENTIMENT_LABELS, extract_expression, extract_final_number,
                        numbers_agree, run_expression, verify)

SYSTEM = "You are a precise assistant. Answer correctly and concisely. No preamble."

# category-specific nudges keep local answers in a shape the judge expects
PROMPT_HINTS = {
    "mathematical_reasoning": "\n\nWork step by step, then give the final answer on the last line as: ANSWER: <value>",
    "code_debugging": "\n\nIdentify the bug in one sentence, then give the full corrected code in a fenced block.",
    "code_generation": "\n\nReturn the complete function in a fenced code block.",
    "sentiment_classification": "\n\nState the sentiment label first, then a one-sentence justification.",
    "named_entity_recognition": "\n\nList each entity with its type. Use the exact format the task asks for.",
}


# kept lean on purpose: remote input tokens are scored too (VERDICTS V3)
REMOTE_SUFFIX = "\n\nAnswer directly and concisely. Do not show reasoning."


def pick_models(category: str) -> list[str]:
    """Primary + one fallback (used on timeout/verification failure); a third
    attempt is never worth its tokens."""
    prefs = config.CODE_PREFERENCE if category.startswith("code") else config.REMOTE_PREFERENCE
    allowed = [m for m in prefs if m in config.ALLOWED_MODELS]
    if not allowed and config.ALLOWED_MODELS:
        allowed = list(config.ALLOWED_MODELS)
    return allowed[:2]


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


def _sentiment_label_agrees(prompt: str, answer: str) -> bool:
    """Exact-label agreement between the shipped answer and a second,
    grammar-constrained read (free local tokens buy real confidence)."""
    m = re.search(r"label\s*[:=]?\s*(positive|negative|neutral|mixed)", answer.lower())
    stated = m.group(1) if m else next((l for l in SENTIMENT_LABELS if l in answer.lower()), None)
    if stated is None:
        return False
    second = local_llm.complete(
        prompt + "\n\nAnswer with exactly one word: the sentiment label.",
        max_tokens=8, system=SYSTEM, grammar=grammars.SENTIMENT_LABEL_GBNF)
    if not second:
        return True  # constrained read unavailable — keep the verified answer
    return second.strip().lower() == stated


def _math_program_check(prompt: str, answer: str) -> bool:
    """Program-aided verification: independently translate the problem into an
    arithmetic expression, execute it, and compare with the stated answer.
    Deterministic and free (VERDICTS V6)."""
    stated = extract_final_number(answer)
    if stated is None:
        return False
    reply = local_llm.complete(
        prompt + "\n\nWrite ONE Python arithmetic expression (a single line, no "
        "imports, no variables) that computes the final numeric answer. "
        "Output only the expression.",
        max_tokens=96, system=SYSTEM)
    if not reply:
        return False
    expr = extract_expression(reply)
    if expr is None:
        return False
    value = run_expression(expr)
    return value is not None and numbers_agree(stated, value)


def solve(task: dict, deadline: float) -> dict:
    """Answer one task. Returns {task_id, answer, route, category} — route is
    diagnostic only and stripped before writing results."""
    prompt = task["prompt"]
    category = classify(prompt)
    full_prompt = prompt + PROMPT_HINTS.get(category, "")
    time_left = deadline - time.monotonic()

    answer, route = None, "none"

    if local_llm.available() and time_left > 60:
        # constrained decoding only for extraction: JSON-demanding NER prompts
        # get grammar-guaranteed well-formed JSON (VERDICTS V5)
        grammar = (grammars.JSON_GBNF
                   if category == "named_entity_recognition" and "json" in prompt.lower()
                   else None)
        answer = local_llm.complete(full_prompt, system=SYSTEM, grammar=grammar)
        if answer:
            verdict = verify(category, prompt, answer)
            if (verdict == "pass" and category == "sentiment_classification"
                    and time_left > 90 and not _sentiment_label_agrees(prompt, answer)):
                verdict = "fail"  # second constrained read disagrees on the label
            if verdict == "pass":
                route = "local"
            elif (verdict == "unknown" and category == "mathematical_reasoning"
                    and time_left > 90 and _math_program_check(prompt, answer)):
                route = "local+program"
            elif (verdict == "unknown" and category != "mathematical_reasoning"
                    and time_left > 90 and _self_consistent(full_prompt, answer)):
                route = "local+consistent"
            else:
                answer = None  # fail, or unconfident unknown -> escalate

    if answer is None:
        cap = config.REMOTE_MAX_TOKENS.get(category, 384)
        remote_prompt = prompt + REMOTE_SUFFIX
        for model in pick_models(category):
            remote_answer = remote.complete(remote_prompt, model=model,
                                            max_tokens=cap, system=SYSTEM)
            if not remote_answer:
                continue  # timeout/error -> one shot at the fallback model
            answer, route = remote_answer, f"remote:{model}"
            if verify(category, prompt, remote_answer) != "fail":
                break  # verified (or unverifiable) remote answer: ship it

    if answer is None:  # last resort: any local attempt beats an empty string
        answer = local_llm.complete(full_prompt, system=SYSTEM) or "Unable to answer."
        route = route if route != "none" else "fallback"

    return {"task_id": task["task_id"], "answer": answer, "route": route, "category": category}
