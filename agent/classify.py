"""Cheap keyword-based category guess. Only steers prompt templates, verifier
choice, and escalation model — a wrong guess degrades gracefully."""
import re

_RULES: list[tuple[str, list[str]]] = [
    ("code_debugging", ["bug", "debug", "fix the", "error in", "incorrect code", "faulty"]),
    ("code_generation", ["write a function", "implement", "def ", "function that", "return a function", "signature"]),
    ("named_entity_recognition", ["entities", "entity", "person, org", "label the", "extract and label"]),
    ("sentiment_classification", ["sentiment", "positive", "negative", "neutral", "tone of the review"]),
    ("text_summarisation", ["summarise", "summarize", "summary", "condense", "in one sentence", "tl;dr"]),
    ("mathematical_reasoning", ["calculate", "how many", "how much", "percent", "%", "total cost", "compute the"]),
    ("logical_reasoning", ["puzzle", "seated", "who is", "truth", "liar", "constraint", "order of", "schedule"]),
    ("factual_knowledge", ["what is", "explain", "define", "how does", "why does", "describe"]),
]


def classify(prompt: str) -> str:
    p = prompt.lower()
    has_code_block = bool(re.search(r"```|def |function\s*\(|class \w+[:(]|console\.log|print\(", prompt))
    scores: dict[str, int] = {}
    for cat, kws in _RULES:
        scores[cat] = sum(1 for kw in kws if kw in p)
    if has_code_block:
        scores["code_debugging"] += 2 if any(w in p for w in ("bug", "fix", "wrong", "error")) else 0
        scores["code_generation"] += 1
    best = max(scores, key=lambda c: scores[c])
    return best if scores[best] > 0 else "factual_knowledge"
