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
from .verifiers import (SENTIMENT_LABELS, assignment_matches_answer,
                        extract_expression, extract_final_number,
                        extract_python_code, format_assignment, numbers_agree,
                        parse_logic_translation, primary_function_name,
                        run_expression, run_with_assertions, solve_logic_csp,
                        verify)

SYSTEM = "You are a precise assistant. Answer correctly and concisely. No preamble."

# category-specific nudges keep local answers in a shape the judge expects
PROMPT_HINTS = {
    "mathematical_reasoning": "\n\nWork step by step, then give the final answer on the last line as: ANSWER: <value>",
    "code_debugging": "\n\nIdentify the bug in one sentence, then give the full corrected code in a fenced block.",
    "code_generation": "\n\nReturn the complete function in a fenced code block.",
    "sentiment_classification": "\n\nState the sentiment label first, then a one-sentence justification.",
    "named_entity_recognition": "\n\nList each entity with its type, each entity under exactly one type. Cities, countries, and regions are LOCATION, never ORGANIZATION. Use the exact format the task asks for.",
}


# kept lean on purpose: remote input tokens are scored too (VERDICTS V3)
REMOTE_SUFFIX = "\n\nAnswer directly and concisely. Do not show reasoning."

# Accuracy-first tilt (leaderboard 2026-07-10: 15/19, gate needs 16/19).
# These categories have no deterministic verifier — they shipped on the
# self-consistency probe, our weakest signal (57% strict on dev, vs ~100%
# for program-checked math and 92% for solver-checked logic). A consistent
# 4B is still a 4B on world knowledge and entity typing; qualifiers spend
# 1.8k-5.4k tokens, so buying remote accuracy here is cheap. Both prompts
# are short (low scored input cost) — unlike summarisation, whose long
# passages would bill heavily and whose dev fails were mostly judge/data
# artifacts, so it stays local.
REMOTE_FIRST = {"factual_knowledge", "named_entity_recognition"}

# per-category nudge for the remote call itself; kept to one short sentence
REMOTE_HINTS = {
    "named_entity_recognition": " Cities, countries, and regions are LOCATION, never ORGANIZATION.",
}


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


def _stated_sentiment_label(answer: str) -> str | None:
    """An explicit 'label: X' statement wins outright. Otherwise, the
    earliest-occurring label word — NOT SENTIMENT_LABELS' fixed tuple order,
    which finds "positive" inside a "mixed" answer's own justification
    ("...positive aspects...negative aspects...") before ever considering
    the word "mixed" that was actually declared (research/benchmark_run_2026-07-07.md)."""
    a = answer.lower()
    m = re.search(r"(?:label|sentiment|overall)\s*[:=]?\s*(positive|negative|neutral|mixed)", a)
    if m:
        return m.group(1)
    hits = [(a.find(l), l) for l in SENTIMENT_LABELS if l in a]
    return min(hits)[1] if hits else None


def _sentiment_label_agrees(prompt: str, answer: str) -> bool:
    """Exact-label agreement between the shipped answer and a second,
    grammar-constrained read (free local tokens buy real confidence)."""
    stated = _stated_sentiment_label(answer)
    if stated is None:
        return False
    second = local_llm.complete(
        prompt + "\n\nAnswer with exactly one word: the sentiment label.",
        max_tokens=8, system=SYSTEM, grammar=grammars.SENTIMENT_LABEL_GBNF)
    if not second:
        return True  # constrained read unavailable — keep the verified answer
    return second.strip().lower() == stated


def _math_program_check(prompt: str, answer: str) -> bool | None:
    """Program-aided verification: independently translate the problem into an
    arithmetic expression, execute it, and compare with the stated answer.
    Deterministic and free (VERDICTS V6). Tri-state: True/False means a real
    comparison happened; None means no check was possible (no stated number,
    local model unavailable, no usable expression) — callers must not treat
    None as disagreement (VERDICTS V16)."""
    stated = extract_final_number(answer)
    if stated is None:
        return None
    reply = local_llm.complete(
        prompt + "\n\nWrite ONE Python arithmetic expression (a single line, no "
        "imports, no variables) that computes the final numeric answer. "
        "Output only the expression.",
        max_tokens=96, system=SYSTEM)
    if not reply:
        return None
    expr = extract_expression(reply)
    if expr is None:
        return None
    value = run_expression(expr)
    if value is None:
        return None
    return numbers_agree(stated, value)


def _code_assertion_check(prompt: str, code: str) -> bool | None:
    """CRITIC-lite value check (VERDICTS V21): `verify()`'s script-only run
    can't catch a wrong-but-non-crashing candidate (`return nums[0]` for a
    "find the max" spec never raises), since a bare function definition is
    never actually called as a script. The local model, shown only the task
    spec -- never the candidate code, so the same misreading can't leak into
    both the answer and its own check -- writes a few example assertions
    against the candidate's own function name; we splice and execute them.
    Tri-state like _math_program_check: None means no usable assertion was
    produced, not disagreement."""
    name = primary_function_name(code)
    if name is None:
        return None
    reply = local_llm.complete(
        prompt + f"\n\nWrite exactly 3 Python assert statements that check "
        f"correct behavior of a function named `{name}`, one per line, no "
        "explanation. Example format: assert " + name + "(...) == ...",
        max_tokens=160, system=SYSTEM)
    if not reply:
        return None
    # only asserts that actually CALL the candidate's function can judge it;
    # an assert against some other name raises NameError at runtime, which
    # would read as a failure and falsely demote a correct answer (V23 audit)
    assertions = [l for l in reply.splitlines()
                  if l.strip().startswith("assert ")
                  and re.search(rf"\b{re.escape(name)}\s*\(", l)]
    return run_with_assertions(code, assertions)


LOGIC_TRANSLATE_SUFFIX = (
    "\n\nTranslate the puzzle above into constraints. Output EXACTLY this "
    "format and nothing else:\n"
    "PEOPLE: name1, name2, ...\n"
    "POSITIONS: 1..N\n"
    "C: <one constraint per line>\n"
    "Use lowercase first names as integer position variables. Allowed "
    "operators: == != < > <= >= + - * % abs() and or not. Examples:\n"
    "C: emily == 3\n"
    "C: frank == grace + 1\n"
    "C: abs(ivy - emily) != 1\n"
    "C: henry % 2 == 0")


def _logic_solver_check(prompt: str, answer: str) -> tuple[str, str | None]:
    """Solver-aided logic verification (VERDICTS V15): the local model
    translates the puzzle into a declarative constraint form — extraction,
    not reasoning (SatLM) — and a CSP solver decides. Returns
      ('agree', None)    unique solution matches the stated answer
      ('override', text) unique solution contradicts it; text is the
                         solver-derived answer
      ('skip', None)     no decisive translation — under-translation yields
                         multiple solutions, mistranslation usually none, so
                         uniqueness itself is the guardrail."""
    reply = local_llm.complete(prompt + LOGIC_TRANSLATE_SUFFIX,
                               max_tokens=256, system=SYSTEM)
    if not reply:
        return "skip", None
    parsed = parse_logic_translation(reply)
    if parsed is None:
        return "skip", None
    status, solution = solve_logic_csp(*parsed)
    if status != "unique":
        return "skip", None
    if assignment_matches_answer(solution, answer):
        return "agree", None
    return "override", format_assignment(solution, prompt)


def solve(task: dict, deadline: float) -> dict:
    """Answer one task. Returns {task_id, answer, route, category} — route is
    diagnostic only and stripped before writing results."""
    prompt = task["prompt"]
    category = classify(prompt)
    full_prompt = prompt + PROMPT_HINTS.get(category, "")
    time_left = deadline - time.monotonic()

    answer, route = None, "none"

    if local_llm.available() and time_left > 60 and category not in REMOTE_FIRST:
        # constrained decoding only for extraction: JSON-demanding NER prompts
        # get grammar-guaranteed well-formed JSON (VERDICTS V5)
        grammar = (grammars.JSON_GBNF
                   if category == "named_entity_recognition" and "json" in prompt.lower()
                   else None)
        answer, confidence = local_llm.complete_scored(full_prompt, system=SYSTEM,
                                                       grammar=grammar)
        # a confidently-low generation isn't worth a self-consistency probe;
        # None means "no signal", never low (VERDICTS V17)
        low_confidence = (config.LOGPROB_ESCALATE_BELOW is not None
                          and confidence is not None
                          and confidence < config.LOGPROB_ESCALATE_BELOW)
        if answer:
            verdict = verify(category, prompt, answer)
            if (verdict == "pass" and category == "sentiment_classification"
                    and time_left > 90 and not _sentiment_label_agrees(prompt, answer)):
                verdict = "fail"  # second constrained read disagrees on the label
            if (verdict == "pass" and category in ("code_generation", "code_debugging")
                    and time_left > 90):
                code = extract_python_code(answer)
                # a script-only "doesn't crash" pass can't see a wrong-but-
                # non-crashing bug (VERDICTS V21) -- a real assertion
                # disagreement demotes the verdict; no usable assertion
                # (None) leaves today's script-only pass untouched
                if code is not None and _code_assertion_check(prompt, code) is False:
                    verdict = "fail"
            if verdict == "pass":
                route = "local"
            elif verdict == "unknown" and time_left > 90:
                if category == "mathematical_reasoning":
                    if _math_program_check(prompt, answer) is True:
                        route = "local+program"
                    else:
                        answer = None
                elif category == "logical_reasoning":
                    status, solver_answer = _logic_solver_check(prompt, answer)
                    if status == "agree":
                        route = "local+solver"
                    elif status == "override":
                        # the solver's unique solution beats a free-form
                        # guess at our worst category (VERDICTS V15)
                        answer, route = solver_answer, "solver"
                    elif not low_confidence and _self_consistent(full_prompt, answer):
                        route = "local+consistent"
                    else:
                        answer = None
                elif not low_confidence and _self_consistent(full_prompt, answer):
                    route = "local+consistent"
                else:
                    answer = None
            else:
                answer = None  # fail, or unknown with no time to check -> escalate

    if answer is None:
        cap = config.REMOTE_MAX_TOKENS.get(category, 384)
        remote_prompt = prompt + REMOTE_HINTS.get(category, "") + REMOTE_SUFFIX
        doubted = None  # verified remote answer our free audit disagreed with
        for model in pick_models(category):
            remote_answer = remote.complete(remote_prompt, model=model,
                                            max_tokens=cap, system=SYSTEM)
            if not remote_answer:
                continue  # timeout/error -> one shot at the fallback model
            answer, route = remote_answer, f"remote:{model}"
            if verify(category, prompt, remote_answer) == "fail":
                continue
            if (category == "mathematical_reasoning"
                    and deadline - time.monotonic() > 120
                    and _math_program_check(prompt, remote_answer) is False):
                # free local audit of the paid answer (VERDICTS V16): a real
                # disagreement buys the fallback model one shot — but the
                # audit itself can be wrong, so the doubted answer is held,
                # never discarded; if both models end up doubted, the
                # higher-preference one ships
                if doubted is None:
                    doubted = (remote_answer, route)
                continue
            break  # verified remote answer, no grounded doubt: ship it
        else:
            if doubted is not None:
                answer, route = doubted

    if answer is None:  # last resort: any local attempt beats an empty string
        # A repeat of the identical full-length prompt just to get nothing
        # new is exactly what timed out reasoning-heavy categories the first
        # time (constrained-Docker test, 2026-07-08: 2 threads, 25s cap --
        # the retry burned a second 25s for the same failure). Use the
        # category's already-tuned cap (much smaller than the 768 default
        # for factual/math/logic) so the retry has a real chance to finish,
        # and skip it outright once there isn't time left to even try --
        # a missing TOTAL_BUDGET_S deadline scores the whole run zero, which
        # is worse than one weak answer (main.py's own design rule).
        if deadline - time.monotonic() > config.REQUEST_TIMEOUT_S + 5:
            if category == "mathematical_reasoning":
                # even the 320-token cap still carries the "work step by
                # step" hint (full_prompt), which needs more decode time
                # than a slow 2-thread box has left to give (constrained-
                # Docker test, 2026-07-08: 320 tokens of derivation still
                # timed out where 160-192 token categories succeeded) --
                # the derivation is a nicety we can't afford twice; drop it
                # and ask for the bare number instead.
                retry_prompt = prompt + "\n\nGive ONLY the final numeric answer. No steps, no explanation."
                answer = local_llm.complete(retry_prompt, max_tokens=32, system=SYSTEM) or "Unable to answer."
            else:
                answer = local_llm.complete(full_prompt, max_tokens=cap, system=SYSTEM) or "Unable to answer."
        else:
            answer = "Unable to answer."
        route = route if route != "none" else "fallback"

    return {"task_id": task["task_id"], "answer": answer, "route": route, "category": category}
