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
    # code FIRST: with "identify the bug" leading, the 4B spent its whole
    # decode budget on bug analysis and never reached the code (2 dev fails,
    # 2026-07-12 cap7 batch1)
    "code_debugging": "\n\nGive the corrected code in a fenced block FIRST, then one short sentence naming the bug. Nothing else.",
    "code_generation": "\n\nReturn the complete function in a fenced code block.",
    "sentiment_classification": "\n\nState the sentiment label first, then a one-sentence justification.",
    # terse local hints (research/local_cap_feasibility.md): a short-answer
    # instruction makes the local answer short-COMPLETE so it fits the tight
    # LOCAL_GEN_CAP without truncating mid-content. Only affects the local
    # path (remote uses REMOTE_HINTS); matters when these run local.
    # NER: completeness wording, NOT "list only" — the terse version made the
    # model stop voluntarily at 44/64 tokens and drop entities outright
    # (research/cap2_ship_risks.md, lost "Grammy Award"). This mirrors the
    # remote hint that fixed the identical failure on the remote path.
    "named_entity_recognition": "\n\nList EVERY entity — persons (keep titles), organizations, locations, dates, times, events, awards. One per line as 'entity: TYPE', no explanation. Keep multi-word date phrases intact as one entity (e.g. 'summer of 1843'). Cities, countries, and regions are LOCATION, never ORGANIZATION.",
    "factual_knowledge": "\n\nAnswer directly in one or two short sentences. State the key facts, no preamble, no elaboration.",
    "logical_reasoning": "\n\nGive the final answer directly (the assignment or conclusion), no working.",
    # the length rule must come FIRST and defer to the task: naming "3
    # sentences" up front made the 4B ship 3 sentences against a task that
    # demanded exactly 2 (dev fail, 2026-07-12)
    "text_summarisation": "\n\nIf the task states a length limit (a sentence or word count), obey it EXACTLY. Otherwise summarize in 2-3 short sentences covering the main points.",
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


def _self_consistent(prompt: str, first: str, max_tokens: int = 768) -> bool:
    """Second local sample at higher temperature; agreement = confidence.
    Cap it like the first sample — an uncapped probe on 2 vCPU times out to
    None and silently reads as 'inconsistent'."""
    second = local_llm.complete(prompt, system=SYSTEM, temperature=0.7,
                                max_tokens=max_tokens)
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


MATH_EXPR_SUFFIX = (
    "\n\nWrite ONE Python arithmetic expression (a single line, no imports, "
    "no variables) that computes the final numeric answer. "
    "Output only the expression.")


def _format_number(v: float) -> str:
    if v == int(v):
        return str(int(v))
    # NOT %g: its 6-significant-digit default truncates 1157.625 -> "1157.62"
    return f"{v:.6f}".rstrip("0").rstrip(".")


def _apply_rounding(value: float, prompt: str) -> float:
    """Honor an explicit rounding instruction: the exact expression value
    (1157.625) judged against a 'round to nearest dollar' task reads as
    instruction non-compliance to an LLM judge even when numerically closer."""
    low = prompt.lower()
    if "round" not in low and "nearest" not in low:
        return value
    if ("cent" in low or "hundredth" in low
            or "two decimal" in low or "2 decimal" in low):
        return round(value, 2)
    return float(round(value))


def _math_local_program(prompt: str) -> tuple[str | None, str]:
    """Expression-first math (PAL, program-aided): have the local model emit
    a ~15-40 token arithmetic expression and EXECUTE it, instead of decoding
    a 150-250 token derivation a 2-vCPU box cannot finish in budget (cap4,
    2026-07-12: uncapped derivations timed out and the 40-token retry shipped
    truncated step-1s — 1/7 dev). Same translate-then-execute move as
    _math_program_check, now used to PRODUCE the answer, not just audit one.
    Falls back to a bare-number ask (32 tokens, always finishes) when no
    usable expression comes back. Returns (answer, route)."""
    reply = local_llm.complete(prompt + MATH_EXPR_SUFFIX, max_tokens=64,
                               system=SYSTEM)
    if reply:
        expr = extract_expression(reply)
        if expr is not None:
            value = run_expression(expr)
            if value is not None:
                final = _apply_rounding(value, prompt)
                # show the work: the expression IS the derivation, and a bare
                # number invites an LLM judge to dock for "no reasoning shown"
                work = f"Computation: {expr} = {_format_number(value)}"
                if final != value:
                    work += f", rounded to {_format_number(final)}"
                return f"{work}\nANSWER: {_format_number(final)}", "local+program"
    bare = local_llm.complete(
        prompt + "\n\nGive ONLY the final numeric answer. No steps, no explanation.",
        max_tokens=32, system=SYSTEM)
    if bare:
        return f"ANSWER: {bare.strip()}", "local-bare"
    return None, "none"


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

    # Math never free-generates under LOCAL_ONLY: expression-first program
    # path — decode ~15-40 tokens and execute, instead of a derivation the
    # 2-vCPU box can't finish (see _math_local_program).
    if (config.LOCAL_ONLY and category == "mathematical_reasoning"
            and local_llm.available() and time_left > 60):
        answer, route = _math_local_program(prompt)

    # Under LOCAL_ONLY a REMOTE_FIRST category still runs locally (free) —
    # UNLESS it is also in LOCAL_ONLY_ESCALATE, which is going remote anyway:
    # generating locally first would burn ~20-50s of budget for an answer
    # we've measured to be unreliable. Same for LOCAL_SKIP (code_debugging:
    # the full corrected program can't be decoded in budget) and math, which
    # just took its program path above.
    _skip_local = (
        (category in REMOTE_FIRST and (
            not config.LOCAL_ONLY or category in config.LOCAL_ONLY_ESCALATE))
        or (config.LOCAL_ONLY and category in config.LOCAL_SKIP)
        or (config.LOCAL_ONLY and category == "mathematical_reasoning"))
    if answer is None and local_llm.available() and time_left > 60 and not _skip_local:
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
        if not answer and config.LOCAL_ONLY:
            # decode timed out and returned EMPTY. Left alone this falls
            # through to a PAID remote call — the hidden source of most
            # remaining escalations. Retry locally at a cap small enough to
            # be guaranteed to finish; a terse local answer costs zero tokens
            # and beats paying for one (2026-07-12 token push).
            answer, confidence = local_llm.complete_scored(
                full_prompt, system=SYSTEM, grammar=grammar,
                max_tokens=config.LOCAL_RETRY_CAP)
        local_answer = answer  # preserved verbatim for the LOCAL_ONLY fallback
        # a confidently-low generation isn't worth a self-consistency probe;
        # None means "no signal", never low (VERDICTS V17)
        low_confidence = (config.LOGPROB_ESCALATE_BELOW is not None
                          and confidence is not None
                          and confidence < config.LOGPROB_ESCALATE_BELOW)
        # Under LOCAL_ONLY, a category outside LOCAL_ONLY_ESCALATE ships its
        # local answer NO MATTER what the extra probes conclude (the restore
        # block below re-ships it on any demotion) — so probes whose only
        # power is to demote (sentiment double-read, self-consistency) are
        # pure time burn there: ~10-50s/task on 2 vCPU, the margin between
        # fitting the 600s kill line and shedding tasks to placeholders.
        # Probes that can IMPROVE the answer (logic solver override) or gate
        # a real escalation (code assertion check) still run.
        _ships_regardless = (config.LOCAL_ONLY
                             and category not in config.LOCAL_ONLY_ESCALATE)
        # a decode that hit the token cap mid-code is NOT salvageable: the
        # parser-oracle extracts a syntactically-valid prefix that "runs
        # clean" while missing half its body (batch1 2026-07-12: two such
        # answers shipped). An odd number of ``` fences means the closing
        # fence never arrived — treat as no answer so code categories
        # escalate and everything else retries/ships-short instead.
        if (answer and category.startswith("code")
                and answer.count("```") % 2 == 1):
            answer = None
            if not _ships_regardless:
                # escalation is available: clear local_answer too, or the
                # restore block below resurrects this exact truncated code
                # and the escalation never fires. Under pure-zero the
                # truncation IS the best available answer (partial credit
                # beats a placeholder), so there local_answer stays and
                # ships directly — same behavior the 19-task dress
                # rehearsal validated — without burning ~45s on a retry
                # that would reproduce the identical truncation.
                local_answer = None
        if answer:
            verdict = verify(category, prompt, answer)
            if (verdict == "pass" and category == "sentiment_classification"
                    and time_left > 90 and not _ships_regardless
                    and not _sentiment_label_agrees(prompt, answer)):
                verdict = "fail"  # second constrained read disagrees on the label
            if (verdict == "pass" and category in ("code_generation", "code_debugging")
                    and time_left > 90 and not _ships_regardless):
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
                    elif _ships_regardless:
                        route = "local-only"  # probe couldn't change the ship
                    elif not low_confidence and _self_consistent(full_prompt, answer):
                        route = "local+consistent"
                    else:
                        answer = None
                elif _ships_regardless:
                    route = "local-only"  # consistency probe couldn't change the ship
                elif not low_confidence and _self_consistent(
                        full_prompt, answer, local_cap or 768):
                    route = "local+consistent"
                else:
                    answer = None
            else:
                answer = None  # fail, or unknown with no time to check -> escalate

    if (answer is None and config.LOCAL_ONLY and local_answer
            and category not in config.LOCAL_ONLY_ESCALATE):
        # local-dominant: an inconclusive verdict ships the local answer
        # rather than paying remote. All free local overrides already ran
        # above (solver/program); this only replaces the paid escalation,
        # keeping scored tokens at zero. Categories in LOCAL_ONLY_ESCALATE
        # (if any are configured) fall through to the remote loop below.
        answer, route = local_answer, "local-only"

    cap = config.REMOTE_MAX_TOKENS.get(category, 384)
    # Under LOCAL_ONLY, a category outside LOCAL_ONLY_ESCALATE must NEVER
    # reach the remote loop — not even when the local generation came back
    # EMPTY (double decode timeout). Before this guard, that empty-answer
    # path silently fell through to a paid call, and with a 0-token club
    # holding ranks 1-9, one such call is the whole leaderboard: the
    # last-resort local retry below handles the empty case instead.
    # ONE exception — the safety valve: if the local server is actually DOWN
    # (fresh probe, not the memoized flag), pure-zero mode would otherwise
    # ship "Unable to answer." for the entire run (0% -> DNQ). A paid,
    # badly-ranked run beats a zeroed one; the valve never opens while the
    # local engine is alive.
    if answer is None and (not config.LOCAL_ONLY
                           or category in config.LOCAL_ONLY_ESCALATE
                           or not local_llm.healthy_now()):
        remote_prompt = prompt + REMOTE_HINTS.get(category, "") + REMOTE_SUFFIX
        doubted = None  # verified remote answer our free audit disagreed with
        models = pick_models(category)
        if config.LOCAL_ONLY:
            # code is the only category that still pays; a second-model
            # fallback would double that bill for a marginal accuracy gain,
            # and the local answer is already there as a backstop.
            models = models[:config.LOCAL_ONLY_MAX_MODELS]
        elif category in REMOTE_FIRST and models:
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
        # LOCAL_REQUEST_TIMEOUT_S, not REQUEST_TIMEOUT_S: this retry calls
        # local_llm, whose client timeout is the longer local one (70s) —
        # gating on the 25s remote figure let an attempt start with less
        # time left than the retry itself could legitimately take
        if deadline - time.monotonic() > config.LOCAL_REQUEST_TIMEOUT_S + 5:
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
                # local-sized cap, NOT the remote cap: REMOTE_MAX_TOKENS
                # (256+) cannot decode locally inside the timeout, which
                # would turn this rescue into a guaranteed second empty
                retry_cap = min(cap, config.LOCAL_GEN_CAP.get(category, 64))
                answer = local_llm.complete(full_prompt, max_tokens=retry_cap,
                                            system=SYSTEM) or "Unable to answer."
        else:
            answer = "Unable to answer."
        route = route if route != "none" else "fallback"

    return {"task_id": task["task_id"], "answer": answer, "route": route, "category": category}
