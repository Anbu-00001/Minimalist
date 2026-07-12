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
from .verifiers import (assignment_matches_answer, extract_expression,
                        extract_final_number, extract_python_code,
                        format_assignment, numbers_agree,
                        parse_logic_translation, primary_function_name,
                        run_expression, run_with_assertions, solve_logic_csp,
                        stated_sentiment_label, verify)

SYSTEM = "You are a precise assistant. Answer correctly and concisely. No preamble."

# category-specific nudges keep local answers in a shape the judge expects
PROMPT_HINTS = {
    "mathematical_reasoning": "\n\nWork step by step, then give the final answer on the last line as: ANSWER: <value>",
    "code_debugging": "\n\nIdentify the bug in one sentence, then give the full corrected code in a fenced block.",
    "code_generation": "\n\nReturn the complete function in a fenced code block.",
    "sentiment_classification": "\n\nState the sentiment label first, then a one-sentence justification.",
    # terse local hints (research/local_cap_feasibility.md): a "list only /
    # no notes" instruction makes the local answer short-COMPLETE so it fits
    # the tight LOCAL_GEN_CAP without truncating mid-content. Only affects the
    # local path (remote uses REMOTE_HINTS); matters when these run local.
    "named_entity_recognition": "\n\nList only, one entity per line as 'entity: TYPE'. No explanation. Each entity under exactly one type; cities, countries, and regions are LOCATION, never ORGANIZATION.",
    "factual_knowledge": "\n\nAnswer directly in one or two short sentences. State the key facts, no preamble, no elaboration.",
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
REMOTE_FIRST = {"factual_knowledge", "named_entity_recognition", "text_summarisation"}
# text_summarisation added 2026-07-11 morning: the A/B measurement that would
# have justified keeping it local was lost (scratchpad wipe + agent session
# limits), so the call is made by dominance: the gate is binary and worth
# everything (DNQ at close may be frozen out of the refreshed-prompt final);
# ~2k extra input tokens worst case drops 2-3 ranks but keeps us qualified,
# and a 31B-class remote model summarizes at least as well as the local 4B.
# Bonus: remote is ~2s vs 30-60s local on 2vCPU for long passages.

# per-category nudge for the remote call itself; kept to one short sentence
REMOTE_HINTS = {
    "named_entity_recognition": " List every entity, including dates and times. Keep titles and honorifics as part of PERSON names. Cities, countries, and regions are LOCATION, never ORGANIZATION.",
    # routes remote math answers through the ANSWER-line extraction branch,
    # whose fraction/percent handling is already hardened (2102e09)
    "mathematical_reasoning": " End with ANSWER: <value>.",
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


def _sentiment_label_agrees(prompt: str, answer: str) -> bool:
    """Exact-label agreement between the shipped answer and a second,
    grammar-constrained read (free local tokens buy real confidence)."""
    stated = stated_sentiment_label(answer)
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
    if numbers_agree(stated, value):
        return True
    # "15%" stated while the program computed 0.15 (or the reverse) is the
    # same commitment in different units — but only when percent context is
    # actually present, so a stray x100 coincidence (cents-vs-dollars class
    # of error) can never bless a genuinely wrong answer
    if "%" in answer or "percent" in prompt.lower():
        if numbers_agree(stated, value * 100) or numbers_agree(stated * 100, value):
            return True
    return False


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
    local_answer = None  # best local generation, for LOCAL_ONLY fallback

    if local_llm.available() and time_left > 60 and (
            category not in REMOTE_FIRST or config.LOCAL_ONLY):
        # constrained decoding only for extraction: JSON-demanding NER prompts
        # get grammar-guaranteed well-formed JSON (VERDICTS V5)
        grammar = (grammars.JSON_GBNF
                   if category == "named_entity_recognition" and "json" in prompt.lower()
                   else None)
        # short-input categories get a tight decode cap so the local
        # generation finishes inside the 2-vCPU request budget instead of
        # timing out to empty (config.LOCAL_GEN_CAP; VERDICTS/cpu_inference)
        local_cap = config.LOCAL_GEN_CAP.get(category)
        answer, confidence = (
            local_llm.complete_scored(full_prompt, system=SYSTEM, grammar=grammar,
                                      max_tokens=local_cap)
            if local_cap else
            local_llm.complete_scored(full_prompt, system=SYSTEM, grammar=grammar))
        local_answer = answer  # preserved verbatim for the LOCAL_ONLY fallback
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

    if (answer is None and config.LOCAL_ONLY and local_answer
            and category not in config.LOCAL_ONLY_ESCALATE):
        # local-dominant: an inconclusive verdict ships the local answer
        # rather than paying remote. All free local overrides already ran
        # above (solver/program/self-consistency); this only replaces the
        # paid escalation, keeping scored tokens at zero. Categories in
        # LOCAL_ONLY_ESCALATE (code) fall through to the remote loop below —
        # their local failures are unrecoverable without escalation.
        answer, route = local_answer, "local-only"

    if answer is None:
        cap = config.REMOTE_MAX_TOKENS.get(category, 384)
        remote_prompt = prompt + REMOTE_HINTS.get(category, "") + REMOTE_SUFFIX
        doubted = None  # verified remote answer our free audit disagreed with
        models = pick_models(category)
        if category in REMOTE_FIRST and models:
            # remote-first has no verified-local answer to fall back on: a
            # transient remote blip zeroes the task (practice-01, bundle
            # smoke 2026-07-11). One bounded retry of the primary model
            # after both preferences fail buys back that failure mode.
            models = models + models[:1]
        for model in models:
            # a hung proxy makes each attempt cost up to 2x the read timeout;
            # deadline-blind retries here are what ran the blackhole chaos
            # scenario 80s past budget (research/chaos_proxy_test.md) — don't
            # start an attempt the budget can't absorb
            if deadline - time.monotonic() < config.REQUEST_TIMEOUT_S + 10:
                break
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
