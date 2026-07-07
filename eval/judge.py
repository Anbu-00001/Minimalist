"""Score eval/results_dev.json against gold answers — no LLM required.

Deterministic per-category checks give three verdicts:
  pass   — answer demonstrably matches gold
  fail   — answer demonstrably wrong (or violates a required format)
  unsure — no cheap check can decide (long-form content, code semantics)

Strict score counts only passes. `unsure` is the ceiling on what an LLM
judge (later, with the Fireworks key) still has to decide.

Usage: .venv/bin/python eval/judge.py [eval/results_dev.json] [--show-fails]
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

from json_repair import repair_json

try:  # optional: the sympy-based checker lighteval/lm-eval-harness use for math
    from math_verify import parse as _mv_parse, verify as _mv_verify
    HAVE_MATH_VERIFY = True
except ImportError:
    HAVE_MATH_VERIFY = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENTIMENT_LABELS = ("positive", "negative", "neutral", "mixed")
STOPWORDS = set("the a an and or of to in on for by with is are was were be been has have had "
                "its it this that these those as at from their they which while but not".split())


# ---------- shared helpers ----------

def _numbers(text: str) -> list[float]:
    out = []
    for m in re.findall(r"-?\$?\d[\d,]*\.?\d*", text):
        try:
            out.append(float(m.replace("$", "").replace(",", "")))
        except ValueError:
            pass
    return out


def _final_number(answer: str) -> float | None:
    """The number the answer commits to: prefer an ANSWER: line, else the
    last number in the last few digit-bearing lines."""
    m = re.search(r"ANSWER\s*[:=]\s*(.+)", answer, re.IGNORECASE)
    if m:
        nums = _numbers(m.group(1))
        if nums:
            return nums[-1]
    lines = [l for l in answer.splitlines() if re.search(r"\d", l)]
    for line in reversed(lines[-3:]):
        nums = _numbers(line)
        if nums:
            return nums[-1]
    nums = _numbers(answer)
    return nums[-1] if nums else None


def _content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z'-]+", text.lower()) if w not in STOPWORDS}


def _overlap(gold: str, answer: str) -> float:
    g = _content_words(gold)
    return len(g & _content_words(answer)) / max(len(g), 1)


def _extract_json(text: str):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    obj = repair_json(text[start:end + 1], return_objects=True)
    return obj if isinstance(obj, dict) else None


def _norm_entity(e: str) -> str:
    e = str(e).strip().lower().rstrip(".")
    return e[4:] if e.startswith("the ") else e


KEY_ALIASES = {"people": "persons", "person": "persons", "names": "persons",
               "organizations": "orgs", "organisations": "orgs", "organization": "orgs",
               "companies": "orgs", "org": "orgs",
               "places": "locations", "location": "locations", "gpe": "locations",
               "date": "dates", "times": "dates"}


def _norm_ner(obj: dict) -> dict[str, frozenset]:
    out = {}
    for k, v in obj.items():
        key = KEY_ALIASES.get(str(k).strip().lower(), str(k).strip().lower())
        vals = v if isinstance(v, list) else [v]
        out[key] = frozenset(_norm_entity(x) for x in vals if str(x).strip())
    return out


def _extract_code(text: str) -> str | None:
    m = re.search(r"```(?:python|py)?\s*(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    if re.search(r"^\s*(def |class |import )", text, re.MULTILINE):
        return text.strip()
    return None


def _run_python(code: str, timeout: float = 5.0) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip()
    except Exception:
        return 1, ""
    finally:
        os.unlink(path)


# ---------- format constraints (from the prompt itself) ----------

WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "a single": 1}


def _format_violation(prompt: str, answer: str) -> str | None:
    p, a = prompt.lower(), answer.strip()
    m = re.search(r"(?:at most|under|no more than|maximum of|in) (\d+) words", p)
    if m and len(a.split()) > int(m.group(1)) * 1.15:
        return f"word limit {m.group(1)} exceeded ({len(a.split())} words)"
    m = re.search(r"exactly (\d+|one|two|three|four|five) sentences?", p)
    if m:
        g = m.group(1)
        want = int(g) if g.isdigit() else WORDNUM[g]
        got = len(re.findall(r"[.!?](?:\s|$)", a))
        if got and got != want:
            return f"wanted exactly {want} sentence(s), got {got}"
    m = re.search(r"(?:exactly|at most) (\d+|one|two|three|four|five) bullet points?", p)
    if m:
        want = WORDNUM.get(m.group(1)) or int(m.group(1))
        got = len(re.findall(r"^\s*(?:[-*•]|\d+\.)\s+", a, re.MULTILINE))
        exact = "exactly" in m.group(0)
        if (exact and got != want) or (not exact and got > want):
            return f"bullet count {got} violates '{m.group(0)}'"
    if re.search(r"one[- ]word (?:answer|only)|provide a one-word", p) and len(a.split()) > 3:
        return "wanted one word"
    return None


# ---------- per-category judges ----------

def _judge_math(t: dict) -> tuple[str, str]:
    if HAVE_MATH_VERIFY:
        try:  # exact/symbolic equivalence first (order matters: gold, answer)
            if _mv_verify(_mv_parse(t["gold_answer"]), _mv_parse(t["answer"])):
                return "pass", "math-verify equivalence"
        except Exception:
            pass  # fall through to tolerance-based comparison
    gold_nums = _numbers(t["gold_answer"])
    if not gold_nums:
        return "unsure", "no number in gold"
    gold = gold_nums[0] if len(gold_nums) == 1 else gold_nums[-1]
    got = _final_number(t["answer"])
    if got is None:
        return "fail", "no number committed in answer"
    tol = 0.011 if "." in t["gold_answer"] else max(2.0, abs(gold) * 0.002)
    if abs(got - gold) <= tol:
        return "pass", f"{got} ≈ {gold}"
    return "fail", f"got {got}, gold {gold}"


def _judge_sentiment(t: dict) -> tuple[str, str]:
    gold_label = next((l for l in SENTIMENT_LABELS if l in t["gold_answer"].lower()), None)
    if gold_label is None:
        return "unsure", "no label in gold"
    a = t["answer"].lower()
    m = re.search(r"label\s*[:=]?\s*(positive|negative|neutral|mixed)", a)
    got = m.group(1) if m else next((l for l in SENTIMENT_LABELS if l in a), None)
    if got is None:
        return "fail", "no label in answer"
    return ("pass", got) if got == gold_label else ("fail", f"got {got}, gold {gold_label}")


def _gold_entities_from_prose(gold: str) -> set[str]:
    """Entities from non-JSON golds: 'Barack Obama (PERSON), ...' or
    '- PERSON: Julius Caesar' / 'Persons: A, B' line formats."""
    ents = set()
    for m in re.finditer(r"([^,\n(]+?)\s*\((PERSON|ORG\w*|LOC\w*|DATE|GPE|MISC)\)", gold, re.IGNORECASE):
        ents.add(_norm_entity(m.group(1)))
    for m in re.finditer(r"^\s*-?\s*(?:persons?|orgs?|organi[sz]ations?|locations?|dates?|misc)\s*:\s*(.+)$",
                         gold, re.IGNORECASE | re.MULTILINE):
        for v in m.group(1).split(","):
            v = v.strip()
            if v and v.lower() not in ("none", "n/a", "-"):
                ents.add(_norm_entity(v))
    return {e for e in ents if e}


def _judge_ner(t: dict) -> tuple[str, str]:
    gold_obj = _extract_json(t["gold_answer"])
    if gold_obj is None:
        # prose gold: judge by entity presence (typing not cheaply checkable)
        ents = _gold_entities_from_prose(t["gold_answer"])
        if not ents:
            return "unsure", "gold is not JSON and no entities parsed"
        a = t["answer"].lower()
        missing = [e for e in ents if not re.search(rf"\b{re.escape(e)}\b", a)]
        if not missing:
            return "pass", f"all {len(ents)} gold entities present"
        if len(missing) >= max(1, len(ents) // 2):
            return "fail", f"missing {sorted(missing)[:4]}"
        return "unsure", f"partial: missing {sorted(missing)[:4]}"
    ans_obj = _extract_json(t["answer"])
    if ans_obj is None:
        return "fail", "answer has no parseable JSON"
    g, a = _norm_ner(gold_obj), _norm_ner(ans_obj)
    for key, gset in g.items():
        if not gset:
            continue
        aset = a.get(key, frozenset())
        if gset != aset:
            missing, extra = gset - aset, aset - gset
            return "fail", f"{key}: missing {sorted(missing)} extra {sorted(extra)}"
    return "pass", "all entity sets match"


def _judge_short_text(t: dict) -> tuple[str, str]:
    """factual_knowledge / logical_reasoning: exact for short golds,
    keyword overlap for long ones."""
    gold, ans = t["gold_answer"].strip(), t["answer"]
    viol = _format_violation(t["prompt"], ans) if t.get("prompt") else None
    if viol:
        return "fail", viol
    if len(gold.split()) <= 5:
        pat = rf"\b{re.escape(gold.lower().rstrip('.'))}\b"
        if re.search(pat, ans[-250:].lower()):
            return "pass", f"'{gold}' in answer tail"
        if re.search(pat, ans.lower()):
            return "unsure", f"'{gold}' mentioned but not as final answer"
        return "fail", f"'{gold}' absent"
    ov = _overlap(gold, ans)
    if ov >= 0.55:
        return "pass", f"keyword overlap {ov:.0%}"
    if ov <= 0.20:
        return "fail", f"keyword overlap {ov:.0%}"
    return "unsure", f"keyword overlap {ov:.0%}"


def _judge_summary(t: dict) -> tuple[str, str]:
    viol = _format_violation(t["prompt"], t["answer"])
    if viol:
        return "fail", viol
    ov = _overlap(t["gold_answer"], t["answer"])
    if ov >= 0.45:
        return "pass", f"format ok, overlap {ov:.0%}"
    if ov <= 0.15:
        return "fail", f"overlap only {ov:.0%}"
    return "unsure", f"format ok, overlap {ov:.0%}"


def _judge_code(t: dict) -> tuple[str, str]:
    code = _extract_code(t["answer"])
    if code is None:
        return "fail", "no code in answer"
    try:
        compile(code, "<ans>", "exec")
    except SyntaxError as e:
        return "fail", f"syntax error: {e.msg}"
    rc, out = _run_python(code)
    if rc != 0:
        return "fail", "code raises at runtime"
    # if gold is runnable and both print something, compare stdout
    gold_code = _extract_code(t["gold_answer"])
    if gold_code:
        grc, gout = _run_python(gold_code)
        if grc == 0 and gout and out:
            return ("pass", "stdout matches gold") if out == gout else ("fail", "stdout differs from gold")
    return "unsure", "runs clean; semantics unchecked"


JUDGES = {
    "mathematical_reasoning": _judge_math,
    "sentiment_classification": _judge_sentiment,
    "named_entity_recognition": _judge_ner,
    "factual_knowledge": _judge_short_text,
    "logical_reasoning": _judge_short_text,
    "text_summarisation": _judge_summary,
    "code_generation": _judge_code,
    "code_debugging": _judge_code,
}


def judge_one(t: dict) -> tuple[str, str]:
    if not str(t.get("answer", "")).strip():
        return "fail", "empty answer"
    return JUDGES[t["true_category"]](t)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_fails = "--show-fails" in sys.argv
    path = args[0] if args else f"{ROOT}/eval/results_dev.json"
    results = json.load(open(path))

    # judge needs the prompt for format checks; join from merged.json
    prompts = {t["task_id"]: t["prompt"] for t in json.load(open(f"{ROOT}/data/dev_tasks/merged.json"))}

    by_cat, by_route = defaultdict(Counter), defaultdict(Counter)
    fails = []
    for t in results:
        t.setdefault("prompt", prompts.get(t["task_id"], ""))
        verdict, why = judge_one(t)
        t["verdict"], t["why"] = verdict, why
        by_cat[t["true_category"]][verdict] += 1
        by_route[t["route"]][verdict] += 1
        if verdict == "fail":
            fails.append(t)

    json.dump(results, open(path, "w"), indent=2, ensure_ascii=False)

    total = Counter(t["verdict"] for t in results)
    n = len(results)
    print(f"\n=== {os.path.relpath(path, ROOT)} — {n} tasks ===")
    print(f"strict score : {total['pass']}/{n} = {total['pass']/max(n,1):.0%}  "
          f"(fail {total['fail']}, unsure {total['unsure']})")
    print(f"ceiling (pass+unsure): {(total['pass']+total['unsure'])/max(n,1):.0%}\n")
    print(f"{'category':<28}{'pass':>6}{'fail':>6}{'unsure':>8}{'strict':>9}")
    for cat in sorted(by_cat):
        c = by_cat[cat]
        s = sum(c.values())
        print(f"{cat:<28}{c['pass']:>6}{c['fail']:>6}{c['unsure']:>8}{c['pass']/s:>8.0%}")
    print(f"\n{'route':<28}{'pass':>6}{'fail':>6}{'unsure':>8}")
    for route in sorted(by_route):
        c = by_route[route]
        print(f"{route:<28}{c['pass']:>6}{c['fail']:>6}{c['unsure']:>8}")

    if show_fails:
        print("\n--- fails ---")
        for t in fails:
            print(f"[{t['true_category']}] {t['task_id']}: {t['why']}")


if __name__ == "__main__":
    main()
