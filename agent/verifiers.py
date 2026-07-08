"""Deterministic answer verification — the cheapest accuracy lever we have.
A local answer that passes verification never spends a scored token.

Verdicts: "pass" (confident, keep local), "fail" (escalate),
"unknown" (no cheap check exists — router decides via policy)."""
import ast
import json
import re
import subprocess
import sys
import tempfile
import textwrap

SENTIMENT_LABELS = {"positive", "negative", "neutral", "mixed"}


def _substantive(cand: str, tree: ast.Module) -> bool:
    """Stray fragments of prose or other languages can parse as Python
    (`max = arr[i];` is a line of JavaScript that does) — real code-task
    answers define something or span multiple lines."""
    if any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                          ast.Import, ast.ImportFrom)) for n in ast.walk(tree)):
        return True
    return sum(1 for l in cand.splitlines() if l.strip()) >= 3


def extract_python_code(text: str) -> str | None:
    """Longest contiguous run of lines that parses as substantive Python
    (EvalPlus-style longest-valid-segment search). The parser is the oracle,
    so prose, fence markers, and language tags exclude themselves."""
    lines = text.splitlines()
    n = len(lines)
    nonempty = [bool(l.strip()) for l in lines]
    best, best_count = None, 0
    for i in range(n):
        if not nonempty[i]:
            continue
        if sum(nonempty[i:]) <= best_count:
            break  # no later start can beat the current best
        for j in range(n, i, -1):
            count = sum(nonempty[i:j])
            if count <= best_count:
                break
            cand = textwrap.dedent("\n".join(lines[i:j])).strip()
            if not cand:
                continue
            try:
                tree = ast.parse(cand)
            except SyntaxError:
                continue
            if _substantive(cand, tree):
                best, best_count = cand, count
                break  # longest segment for this start found
    return best


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


# ---------- program-aided math verification (VERDICTS V6) ----------

_NUM_RE = r"-?\$?\d[\d,]*\.?\d*"
# a safe arithmetic expression: digits/operators plus a small function whitelist
_EXPR_OK = re.compile(r"^(?:\d|[\s+\-*/().,eE_]|\*\*|round|abs|min|max|sum|pow)+$")


def extract_final_number(text: str) -> float | None:
    """The number an answer commits to: an ANSWER: line wins, else the last
    number in the last digit-bearing lines."""
    def nums(s: str) -> list[float]:
        out = []
        for m in re.findall(_NUM_RE, s):
            try:
                out.append(float(m.replace("$", "").replace(",", "")))
            except ValueError:
                pass
        return out

    m = re.search(r"ANSWER\s*[:=]\s*(.+)", text, re.IGNORECASE)
    if m and nums(m.group(1)):
        return nums(m.group(1))[-1]
    for line in reversed([l for l in text.splitlines() if re.search(r"\d", l)][-3:]):
        if nums(line):
            return nums(line)[-1]
    return None


def extract_expression(text: str) -> str | None:
    """Pull a bare arithmetic expression from a model reply (fences stripped),
    rejecting anything outside the arithmetic whitelist."""
    body = re.sub(r"```(?:python|py)?|```", "", text).strip()
    for line in reversed([l.strip() for l in body.splitlines() if l.strip()]):
        line = line.rstrip(".;")
        if re.search(r"\d", line) and _EXPR_OK.match(line):
            return line
    return None


def run_expression(expr: str, timeout: float = 5.0) -> float | None:
    """Evaluate an arithmetic expression in a subprocess; None on any failure."""
    try:
        r = subprocess.run([sys.executable, "-c", f"print(({expr}))"],
                           capture_output=True, text=True, timeout=timeout)
        return float(r.stdout.strip()) if r.returncode == 0 else None
    except Exception:
        return None


def numbers_agree(a: float, b: float) -> bool:
    """Tolerates rounding drift only: |diff| within 2 cents or 0.5% relative."""
    return abs(a - b) <= max(0.02, abs(b) * 0.005)


# ---------- solver-aided logic verification (VERDICTS V15) ----------
# The local model translates an assignment/ordering puzzle into a tiny
# declarative form (people + positions + constraints); a CSP solver decides.
# Uniqueness doubles as the guardrail: an under-translated puzzle has many
# solutions and a mistranslated one usually has none — only a decisive,
# fully-constraining translation ever acts (Logic-LM / SatLM pattern).

_LOGIC_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
# expression whitelist: no dots/brackets/quotes (no attribute access or
# indexing under eval) and no ** (integer-blowup); % allowed for even/odd
_LOGIC_EXPR_OK = re.compile(r"^[a-z0-9_\s()+\-*%<>=!]+$")
_LOGIC_WORDS_OK = {"or", "and", "not", "abs"}
_LOGIC_MAX_VARS = 7          # n! alldiff assignments stays in milliseconds
_LOGIC_MAX_DOMAIN = 10
_LOGIC_MAX_CONSTRAINTS = 20


def parse_logic_translation(text: str):
    """Parse the strict PEOPLE/POSITIONS/C: emission into
    (names, domain, exprs), or None if anything is off-format or outside
    the whitelist. Every identifier in a constraint must be a declared name."""
    names, domain, exprs = [], [], []
    for line in text.splitlines():
        line = line.strip()
        if line.upper().startswith("PEOPLE:"):
            names = [n.strip().lower() for n in line.split(":", 1)[1].split(",") if n.strip()]
        elif line.upper().startswith("POSITIONS:"):
            body = line.split(":", 1)[1].strip()
            m = re.match(r"^(\d+)\s*(?:\.\.|-|to)\s*(\d+)$", body)
            if m:
                lo, hi = int(m.group(1)), int(m.group(2))
                if lo < hi:
                    domain = list(range(lo, hi + 1))
            else:
                try:
                    domain = sorted({int(v) for v in body.split(",")})
                except ValueError:
                    return None
        elif line.upper().startswith("C:"):
            exprs.append(line.split(":", 1)[1].strip().lower())
    if not (2 <= len(names) <= _LOGIC_MAX_VARS) or len(set(names)) != len(names):
        return None
    if any(not _LOGIC_NAME_RE.match(n) or n in _LOGIC_WORDS_OK for n in names):
        return None
    if not domain or len(domain) > _LOGIC_MAX_DOMAIN or len(domain) < len(names):
        return None
    if not exprs or len(exprs) > _LOGIC_MAX_CONSTRAINTS:
        return None
    allowed = set(names) | _LOGIC_WORDS_OK
    for e in exprs:
        if len(e) > 120 or "**" in e or not _LOGIC_EXPR_OK.match(e):
            return None
        idents = set(re.findall(r"[a-z_][a-z0-9_]*", e))
        if not idents & set(names) or idents - allowed:
            return None
    return names, domain, exprs


def solve_logic_csp(names: list[str], domain: list[int], exprs: list[str]):
    """Solve the parsed translation. Returns ('unique', {name: pos}) only
    when exactly one assignment satisfies everything; ('multiple'|'none'|
    'error', None) otherwise. Positions are assumed pairwise distinct — the
    defining property of the assignment/ordering puzzles this targets."""
    from constraint import AllDifferentConstraint, Problem

    problem = Problem()
    problem.addVariables(names, domain)
    problem.addConstraint(AllDifferentConstraint())
    args = ", ".join(names)
    for e in exprs:
        try:
            # whitelist above guarantees the expression is pure arithmetic
            # over declared names; empty builtins leave nothing else callable
            fn = eval(f"lambda {args}: ({e})", {"__builtins__": {}, "abs": abs})
            problem.addConstraint(fn, names)
        except SyntaxError:
            return "error", None
    try:
        it = problem.getSolutionIter()
        first = next(it, None)
        if first is None:
            return "none", None
        if next(it, None) is not None:
            return "multiple", None
        return "unique", dict(first)
    except Exception:
        return "error", None


def _stated_position(name: str, clauses: list[str]) -> int | None:
    """The position an answer assigns to a name: in the first clause that
    mentions the name alongside a number, the number nearest the name.
    Clause = line/comma/semicolon segment — proximity across clause
    boundaries leaks in the neighbouring assignment's digits ("...seat 1,
    Henry in seat 2" puts 1 nearer to Henry than his own 2). Ordinals
    (1st/2nd/...) count as numbers."""
    for clause in clauses:
        m = re.search(re.escape(name), clause)
        if not m:
            continue
        nums = [(min(abs(n.start() - m.end()), abs(m.start() - n.end())), int(n.group(1)))
                for n in re.finditer(r"\b(\d+)(?:st|nd|rd|th)?\b", clause)]
        if nums:
            return min(nums)[1]
    return None


def assignment_matches_answer(solution: dict, answer: str) -> bool:
    """Does the answer's stated assignment agree with the solver's? Every
    name must be stated at its solved position; any contradiction or
    absence counts as disagreement."""
    clauses = re.split(r"[\n,;]", answer.lower())
    return all(_stated_position(name, clauses) == pos
               for name, pos in solution.items())


def format_assignment(solution: dict) -> str:
    """Deterministic prose for a solver-derived assignment, lowest position
    first — the shape the acceptance criteria for these tasks ask for."""
    lines = [f"Position {pos}: {name.capitalize()}"
             for name, pos in sorted(solution.items(), key=lambda kv: kv[1])]
    return "\n".join(lines)


def _word_limit_from_prompt(prompt: str) -> int | None:
    m = re.search(r"(?:in |under |at most |no more than |maximum of )(\d+) words", prompt.lower())
    return int(m.group(1)) if m else None


def verify(category: str, prompt: str, answer: str) -> str:
    if not answer or not answer.strip():
        return "fail"
    a = answer.strip()

    if category in ("code_generation", "code_debugging"):
        code = extract_python_code(a)
        if code is not None:
            # extraction guarantees it parses; run only proves it doesn't raise
            return "pass" if _run_python(code) else "fail"
        if re.search(r"```(?:python|py)\b", a):
            return "fail"  # declared python, but nothing in it parses
        if re.search(r"```|^\s*(function |const |let )", a, re.MULTILINE):
            return "unknown"  # non-python code: syntax not cheaply checkable
        return "fail"  # a code task answered with no code at all

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
