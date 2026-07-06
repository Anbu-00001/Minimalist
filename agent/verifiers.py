"""Deterministic answer verification — the cheapest accuracy lever we have.
A local answer that passes verification never spends a scored token.

Verdicts: "pass" (confident, keep local), "fail" (escalate),
"unknown" (no cheap check exists — router decides via policy)."""
import json
import re
import subprocess
import sys
import tempfile

SENTIMENT_LABELS = {"positive", "negative", "neutral", "mixed"}


def _extract_code(text: str) -> str | None:
    m = re.search(r"```(?:python|py|javascript|js)?\s*(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    if re.search(r"^\s*(def |class |function |const |let )", text, re.MULTILINE):
        return text.strip()
    return None


def _python_syntax_ok(code: str) -> bool:
    try:
        compile(code, "<answer>", "exec")
        return True
    except SyntaxError:
        return False


def _run_python(code: str, timeout: float = 5.0) -> bool:
    """Execute candidate code in a subprocess; True if it exits cleanly."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


def _word_limit_from_prompt(prompt: str) -> int | None:
    m = re.search(r"(?:in |under |at most |no more than |maximum of )(\d+) words", prompt.lower())
    return int(m.group(1)) if m else None


def verify(category: str, prompt: str, answer: str) -> str:
    if not answer or not answer.strip():
        return "fail"
    a = answer.strip()

    if category in ("code_generation", "code_debugging"):
        code = _extract_code(a)
        if code is None:
            return "fail"
        looks_python = "def " in code or "import " in code or "print(" in code
        if looks_python:
            if not _python_syntax_ok(code):
                return "fail"
            # run only self-contained snippets; function defs alone always exit 0
            return "pass" if _run_python(code) else "fail"
        return "unknown"  # non-python code: syntax not cheaply checkable

    if category == "sentiment_classification":
        return "pass" if any(lbl in a.lower() for lbl in SENTIMENT_LABELS) else "fail"

    if category == "text_summarisation":
        limit = _word_limit_from_prompt(prompt)
        if limit and len(a.split()) > int(limit * 1.1):
            return "fail"
        if "one sentence" in prompt.lower() and a.count(". ") > 1:
            return "fail"
        return "unknown"

    if category == "named_entity_recognition":
        if "json" in prompt.lower():
            try:
                json.loads(a[a.find("{"):a.rfind("}") + 1] or a)
            except Exception:
                return "fail"
        wants = [w for w in ("person", "org", "location", "date") if w in prompt.lower()]
        hits = sum(1 for w in wants if w in a.lower())
        return "unknown" if not wants or hits >= max(1, len(wants) - 1) else "fail"

    if category == "mathematical_reasoning":
        # must at least commit to a number
        return "unknown" if re.search(r"-?\d[\d,]*\.?\d*", a) else "fail"

    # factual_knowledge, logical_reasoning: no cheap deterministic check
    return "unknown"
