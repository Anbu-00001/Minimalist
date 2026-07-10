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


def stated_sentiment_label(answer: str) -> str | None:
    """An explicit 'label: X' statement wins outright. Otherwise, the
    earliest-occurring label word — NOT set-iteration order, which finds
    "positive" inside a "mixed" answer's own justification ("...positive
    aspects...negative aspects...") before the word "mixed" that was
    actually declared (research/benchmark_run_2026-07-07.md)."""
    a = answer.lower()
    m = re.search(r"(?:label|sentiment|overall)\s*[:=]?\s*(positive|negative|neutral|mixed)", a)
    if m:
        return m.group(1)
    hits = [(a.find(l), l) for l in SENTIMENT_LABELS if l in a]
    return min(hits)[1] if hits else None


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
    if m:
        # a bare fraction on the ANSWER line is one committed value, not two
        # ("ANSWER: 3/4" must read 0.75, never 4.0)
        f = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*\.?\s*",
                         m.group(1))
        if f and float(f.group(2)) != 0:
            return float(f.group(1)) / float(f.group(2))
        if nums(m.group(1)):
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


_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def _ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _position_labels(prompt: str, n: int) -> list[str]:
    """Position labels matching the puzzle's own vocabulary. Gold answers
    consistently use the puzzle's own terms (day names, ordinals) rather
    than a generic "Position N" — a strict matcher then marks an otherwise
    exactly-correct solver assignment wrong over label wording alone
    (VERDICTS V22: found in the full 228-task benchmark — all 8 non-pass
    "solver"-route tasks had the exactly-correct assignment, wrong only in
    how positions were labeled). Falls back to bare numbers, never invents
    a labeling scheme not evidenced in the prompt itself."""
    lower = prompt.lower()

    # every day individually named -- ordered by CALENDAR, not first mention:
    # the solver's positions 1..n encode earliest-to-latest, and a constraint
    # like "not on Wednesday" can mention a day before the enumeration does,
    # which would scramble a mention-ordered mapping (2026-07-09 audit)
    found_days = [d for d in _DAYS if re.search(rf"\b{d}\b", lower)]
    if len(found_days) >= n:
        return [d.capitalize() for d in found_days[:n]]

    # a day RANGE ("scheduled from Monday to Thursday") only names the two
    # endpoints -- the days between are implied by calendar order, not
    # invented: still grounded in the puzzle's own two stated day names
    m = re.search(r"\b(" + "|".join(_DAYS) + r")\b.{0,15}?\b(?:to|through)\b"
                  r".{0,15}?\b(" + "|".join(_DAYS) + r")\b", lower)
    if m:
        start, end = _DAYS.index(m.group(1)), _DAYS.index(m.group(2))
        if 0 <= end - start == n - 1:
            return [d.capitalize() for d in _DAYS[start:end + 1]]

    if re.search(r"\bseats?\b", lower):
        return [f"Seat {i}" for i in range(1, n + 1)]

    if re.search(r"\b1st\b", lower):
        return [_ordinal(i) for i in range(1, n + 1)]

    return [str(i) for i in range(1, n + 1)]


def format_assignment(solution: dict, prompt: str = "") -> str:
    """Deterministic prose for a solver-derived assignment, lowest position
    first, using the puzzle's own position vocabulary when detectable
    (VERDICTS V22) — bare numbers otherwise, never a hardcoded "Position N"
    that matches no puzzle's actual wording."""
    positions = sorted(set(solution.values()))
    labels = _position_labels(prompt, len(positions)) if prompt else [str(p) for p in positions]
    rank = {pos: i for i, pos in enumerate(positions)}
    lines = [f"{labels[rank[pos]]}: {name.capitalize()}"
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
        stated = stated_sentiment_label(a)
        if stated is None:
            return "fail"
        # a prompt that offers a closed label set makes any answer outside
        # that set wrong even when it's a valid sentiment word — "mixed"
        # for a positive/negative/neutral task fails the judge regardless
        # of how defensible it reads (generalization guard, 2026-07-10)
        offered = {l for l in SENTIMENT_LABELS if l in prompt.lower()}
        if offered and stated not in offered:
            return "fail"
        return "pass"

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


# ---------- code value verification (VERDICTS V21) ----------
#
# _run_python above only proves the extracted block doesn't crash when run as
# a *script*. A candidate answer is almost always a bare `def f(...): ...`
# with no call site, so running it as a script never actually invokes the
# function body -- `return nums[0]` for a "find the max" spec passes cleanly,
# since indexing a non-empty list never raises. The check below actually
# calls the function against independently-generated example assertions.

def primary_function_name(code: str) -> str | None:
    """Name of the first top-level function definition, if any."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return node.name
    return None


def run_with_assertions(code: str, assertions: list[str], timeout: float = 5.0) -> bool | None:
    """Splice candidate code with example-based assert statements and actually
    execute the calls -- this exercises the function's return values, not just
    whether the module body raises.

    Model-generated asserts are themselves unreliable (CodeT-line literature:
    only ~35-51% of LLM-generated tests are valid on some benchmarks, and
    treating them as ground truth degrades valid solutions), so each assert
    is executed independently and tallied rather than run as one fatal block:
      - AssertionError        -> counted as a failure (a real value mismatch)
      - any other exception   -> the ASSERT is broken (wrong name/arity/type),
                                 discarded entirely, never held against the code
    Verdict: True when asserts pass and none fail; False only when failures
    outnumber passes (a lone dissenter among passing asserts is more likely a
    wrong assert than wrong code); None when nothing usable executed or the
    signal is mixed -- callers must never read None as disagreement."""
    valid = []
    for line in assertions:
        line = line.strip()
        if not line.startswith("assert "):
            continue
        try:
            ast.parse(line)
        except SyntaxError:
            continue
        valid.append(line)
    if not valid:
        return None
    tally = ["_p = _f = 0"]
    for a in valid:
        tally += ["try:",
                  f"    {a}",
                  "    _p += 1",
                  "except AssertionError:",
                  "    _f += 1",
                  "except Exception:",
                  "    pass"]
    tally.append("print(_p, _f)")
    out = _run_python_output(code + "\n\n" + "\n".join(tally), timeout=timeout)
    if out is None:
        return None
    try:
        passed, failed = map(int, out.split())
    except ValueError:
        return None
    if failed == 0 and passed > 0:
        return True
    if failed > passed:
        return False
    return None


def _run_python_output(code: str, timeout: float = 5.0) -> str | None:
    """Like _run_python but returns the script's stdout (stripped), or None
    on non-zero exit/timeout."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None
