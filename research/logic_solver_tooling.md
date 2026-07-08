# Research: Deterministic local CSP/SAT/SMT solver tooling for logical_reasoning verification

Collect-only research dump. No recommendations, no code. Every claim below has a URL;
verbatim quotes are marked with quotation marks and a source; paraphrases are marked
"(paraphrase)". Anything I could not directly fetch (WebFetch failed / blocked, only
have search-snippet-level info) is marked **UNVERIFIED**.

Research date: 2026-07-08.

---

## 1. python-constraint / python-constraint2

**Status: real, actively maintained, pip-installable.**

- PyPI (old name): https://pypi.org/project/python-constraint/
- PyPI (current/maintained name): https://pypi.org/project/python-constraint2/
- GitHub (canonical repo, org took over from original author): https://github.com/python-constraint/python-constraint
- Docs: http://python-constraint.github.io/python-constraint/
- Docs API reference: https://python-constraint.github.io/python-constraint/reference.html
- Docs getting-started: https://python-constraint.github.io/python-constraint/intro.html
- Original home (archival, by creator Gustavo Niemeyer): https://labix.org/python-constraint

### Maintenance / install
From direct fetch of the GitHub repo (https://github.com/python-constraint/python-constraint):
- "The project appears actively maintained. The latest release (2.6.0) was published on June 29, 2026, and the repository shows 424 commits on the main branch." (paraphrase of WebFetch summary, not a page quote, but derived from real repo metadata visible on the page)
- Important note found on the repo: **"this software must be installed with `pip install python-constraint2`, as the original pip release will not be updated."**
- Install:
  ```
  pip install python-constraint2
  ```
  Conda/Mamba alternative also documented: `conda install python-constraint2`.
- Despite the install name being `python-constraint2`, the **import name stays `constraint`** (confirmed by usage examples below — `from constraint import *`).

From direct fetch of https://pypi.org/project/python-constraint2/:
- Description: "A module for efficiently solving CSPs (Constraint Solving Problems) over finite domains."
- Latest version: **2.6.0**, released **Jun 29, 2026**
- Requires **Python >=3.11**; supports 3.11, 3.12, 3.13, 3.14
- License: BSD-2-Clause
- File sizes: "Source distribution (tar.gz): 823.9 kB. Wheel distributions range from 1.8 MB to 4.3 MB depending on Python version and platform." — i.e. this is a small, mostly-pure-Python package (some platform-specific wheels suggest optional compiled acceleration, but base footprint is well under 5 MB).
- Key stated feature (quote): "String constraints are preferable over functions and lambdas. These strings are automatically parsed to faster built-in constraints."

### API shape (from direct fetch of GitHub README and docs page)
Basic variable/domain/constraint/solve pattern:
```python
from constraint import *
problem = Problem()
problem.addVariable("a", [1,2,3])
problem.addVariable("b", [4,5,6])
problem.getSolutions()
```
Adding a constraint (string form, per the "prefer strings" guidance):
```python
problem.addConstraint("a*2 == b")
problem.getSolutions()
```
Multiple variables + built-in AllDifferentConstraint:
```python
problem.addVariables(["a", "b"], [1, 2, 3])
problem.addConstraint(AllDifferentConstraint())
problem.getSolutions()
```
Docs page (http://python-constraint.github.io/python-constraint/, direct fetch) also shows the lambda form:
```python
>>> from constraint import *
>>> problem = Problem()
>>> problem.addVariable("a", [1,2])
>>> problem.addVariable("b", [3,4])
>>> problem.getSolutions()
[{'a': 2, 'b': 4}, {'a': 2, 'b': 3}, {'a': 1, 'b': 4}, {'a': 1, 'b': 3}]
>>> problem.addConstraint(lambda a, b: a*2 == b, ("a", "b"))
>>> problem.getSolutions()
[{'a': 2, 'b': 4}]
```

### Built-in constraint classes (from docs page fetch)
Listed on http://python-constraint.github.io/python-constraint/ :
`AllDifferentConstraint`, `AllEqualConstraint`, `ExactSumConstraint`, `MinSumConstraint`,
`MaxSumConstraint`, `ExactProdConstraint`, `MinProdConstraint`, `MaxProdConstraint`,
`VariableExactSumConstraint`, `VariableMinSumConstraint`, `VariableMaxSumConstraint`,
`VariableExactProdConstraint`, `VariableMinProdConstraint`, `VariableMaxProdConstraint`,
`InSetConstraint`, `NotInSetConstraint`, `SomeInSetConstraint`, `SomeNotInSetConstraint`,
`FunctionConstraint`.

API reference methods (paraphrase from docs fetch):
- `Problem.addVariable(name, domain)` — assigns a variable with possible values
- `Problem.addConstraint(constraint, variables)` — constraint can be a Constraint instance,
  a callable/lambda, or (new in v2) a Python-evaluable string expression, automatically parsed
- `Problem.getSolution()` — returns one valid assignment
- `Problem.getSolutions()` — returns all valid assignments as a list

The docs index also mentions worked examples titled "Basics," "Rooks problem," and "Magic
squares" (page section headers seen in the fetch, full bodies not captured).

### Third-party usage example: Zebra/Einstein puzzle with python-constraint
Found via search (title suggests a full worked example): "Project: Solving Einstein's Puzzle
with Python-Constraint" — https://artificialcognition.github.io/who-owns-the-zebra
**UNVERIFIED** — WebFetch to this URL was blocked by network/tool restrictions on all
attempts (`Unable to verify if domain artificialcognition.github.io is safe to fetch`), so
I could not confirm its actual code content. Only the title/URL is confirmed to exist via
search results.

---

## 2. Z3 (Microsoft's SMT solver) — Python bindings

**Status: real, actively maintained, pip-installable, well documented, many logic-puzzle examples exist in the wild.**

- PyPI: https://pypi.org/project/z3-solver/
- GitHub (main Z3 repo): https://github.com/Z3Prover/z3
- Official Z3 Python API doc: http://z3prover.github.io/api/html/z3.html
- Online Z3 Guide (Python): https://microsoft.github.io/z3guide/programming/Z3%20Python%20-%20Readonly/Introduction/
- Community Z3Py tutorial: https://ericpony.github.io/z3py-tutorial/guide-examples.htm

### Package facts (direct fetch of https://pypi.org/project/z3-solver/)
- Description quote: **"Z3 is a theorem prover from Microsoft Research with support for bitvectors, booleans, arrays, floating point numbers, strings, and other data types."**
- Latest version: **4.16.0.0**, released **February 19, 2026**
- Install: `pip install z3-solver`
- License: MIT
- Supported platforms: Windows (x86, x86-64, ARM64), macOS (15.0+, x86-64/ARM64), Linux (manylinux 2.27+ x86-64, manylinux 2.38+ ARM64)
- Distribution sizes (from PyPI file listing, direct fetch): source `z3_solver-4.16.0.0.tar.gz` = 5.1 MB; **wheels ranging from 13.3 MB to 47.5 MB depending on platform**.
  - A follow-up search cross-check (search-snippet level, **UNVERIFIED** as a second independent source but consistent with the direct fetch) gave: "Windows ARM64: 15.1 MB; Windows x86-64: 16.4 MB; Windows x86: 13.3 MB; manylinux2 glibc 2.38+ ARM64: 27.3 MB."
- Maintainers listed: Audrey Dutcher and Nikolaj Bjorner.
- The PyPI page as fetched did **not** list any `Requires-Dist` third-party Python dependencies (my fetch summary: "No specific dependencies or code examples are listed on this PyPI page.") — i.e. the wheel appears to be self-contained (bundles the compiled Z3 native library), consistent with it being a large binary wheel. I could not directly confirm a "zero dependencies" statement in package metadata text — treat that inference as **UNVERIFIED**, only the "no deps listed on the page" observation is directly fetched.

### Verbatim Z3Py usage pattern (from search-summarized official tutorial pages)
"Z3Py is the Z3 API in Python. You can create a general purpose solver with `Solver()`, add
constraints using the method `add`, and solve the asserted constraints with the `check()`
method." (paraphrase of search summary of https://ericpony.github.io/z3py-tutorial/guide-examples.htm and https://microsoft.github.io/z3guide/... — not independently WebFetched, so treat the exact wording as **UNVERIFIED**, though the general Z3Py API shape (`Solver()`, `.add()`, `.check()`, `.model()`) is corroborated by the full code samples below which WERE directly fetched.)

### Real, directly-fetched full code example — Zebra Puzzle in Z3
Source: GitHub Gist by user "salarian", file `zebra.py`, created March 29, 2017.
URL: https://gist.github.com/salarian/51b81083cbf6ce436929ffd191a63905
Full code (verbatim, via direct WebFetch):

```python
# Python solution to the famous Zebra puzzle using Z3. The puzzle statement
# is available on Wikipedia (https://en.wikipedia.org/wiki/Zebra_Puzzle)

import z3

tags = (
    ('nationality', ('brit', 'swede', 'dane', 'german', 'norse')),
    ('pet', ('dog', 'bird', 'cat', 'horse', 'fish')),
    ('drink', ('tea', 'coffee', 'milk', 'beer', 'water')),
    ('smoke', ('palmal', 'dunhil', 'blends', 'bluemas', 'prince')),
    ('colour', ('red', 'green', 'white', 'yellow', 'blue'))
)

nationality, pet, drink, smoke, colour = range(5)
brit, swede, dane, german, norwegian = range(5)
dog, bird, cat, horse, fish = range(5)
tea, coffee, milk, beer, water = range(5)
pallmall, dunhill, blends, bluemasters, prince = range(5)
red, green, white, yellow, blue = range(5)

def print_solution(m):
    for i, row in enumerate(m):
        print("hosue %d: %s" %
              (i+1, '\t'.join([tags[j][1][r[i][j].as_long()]
                               for j in range(5)])))

def match(H, conditions):
    return [H[c[0]] == c[1] for c in conditions]

def member(H, conditions):
    return z3.Or([z3.And(match(H[i], conditions)) for i in range(5)])

def nextto(H, p1, p2):
    return z3.Or([z3.And(match(H[i], p1) + match(H[i+1], p2))
                   for i in range(4)])

def neighbor(H, p1, p2):
    return z3.Or(nextto(H, p1, p2), nextto(H, p2, p1))

def nthelem(H, n, conditions):
    return z3.And(match(H[n], conditions))

H = [[z3.Int("x_%s_%s" % (i+1, tags[j][0])) for j in range(5)]
     for i in range(5)]

cells_c = [z3.And(0 <= H[i][j], H[i][j] <= 4)
           for i in range(5) for j in range(5)]

cols_c = [z3.Distinct([H[i][j] for i in range(5)])
          for j in range(5)]

hint1 = member(H, [(nationality, brit), (colour, red)])
hint2 = member(H, [(nationality, swede), (pet, dog)])
hint3 = member(H, [(nationality, dane), (drink, tea)])
hint4 = nextto(H, [(colour, green)], [(colour, white)])
hint5 = member(H, [(drink, coffee), (colour, green)])
hint6 = member(H, [(pet, bird), (smoke, pallmall)])
hint7 = member(H, [(smoke, dunhill), (colour, yellow)])
hint8 = nthelem(H, 2, [(drink, milk)])
hint9 = nthelem(H, 0, [(nationality, norwegian)])
hint10 = neighbor(H, [(smoke, blends)], [(pet, cat)])
hint11 = neighbor(H, [(pet, horse)], [(smoke, dunhill)])
hint12 = member(H, [(drink, beer), (smoke, bluemasters)])
hint13 = member(H, [(nationality, german), (smoke, prince)])
hint14 = neighbor(H, [(nationality, norwegian)], [(colour, blue)])
hint15 = neighbor(H, [(smoke, blends)], [(drink, water)])

s = z3.Solver()
s.add(cells_c + cols_c)
s.add(hint1, hint2, hint3, hint4, hint5, hint6, hint7, hint8)
s.add(hint9, hint10, hint11, hint12, hint13, hint14, hint15)

if s.check() == z3.sat:
    m = s.model()
    r = [[m.evaluate(H[i][j]) for j in range(5)]
         for i in range(5)]
    print_solution(r)
else:
    print("failed to solve")
```

Other Zebra-puzzle-in-Z3 sources found (not fetched, links only, for cross-reference):
- Another gist: https://gist.github.com/sriram-srinivasan/2981825217f0802d9fbd9878578a711d ("zebra puzzle; z3 based solution.")
- Z3's own examples folder has a general example.py (not zebra-specific): https://github.com/Z3Prover/z3/blob/master/examples/python/example.py
- Rosetta Code has a Zebra puzzle page with multiple language solutions: https://rosettacode.org/wiki/Zebra_puzzle (not confirmed to include Z3/Python specifically)

### Real, directly-fetched content — Knights and Knaves in Z3
Source: Jamie Collinson's blog, "Solving Knights and Knaves with Z3"
URL: https://jamiecollinson.com/blog/solving-knights-and-knaves-with-z3/
(Publication date not shown on the fetched page.)

Install note (quote): **"Installing the python interface to Z3 will also set up Z3 on your system (there's no separate installation needed):"** via `pip install z3-solver`.

Core modeling idea (paraphrase from fetch): variables represent people as Booleans (True =
Knight, True-teller; False = Knave, liar). "A claims X is true" becomes: (A is a Knight) iff
(X is actually true).

Basic example code (verbatim, via direct WebFetch):
```python
from z3 import *

A, B = Bools("A B")
s = Solver()
s.add((A == True) == And(A == False, B == False))

if s.check() != sat:
    print("No solution")
else:
    print(s.model())
```

Enumerating all solutions (verbatim, via direct WebFetch):
```python
def print_solutions(s):
    if s.check() != sat:
        print("No solution")
    else:
        while s.check() == sat:
            model = s.model()
            print(model)
            s.add(Or([d() != model[d] for d in model]))
```

The article states it covers "four increasingly complex puzzles with corresponding Z3
implementations, from two-person scenarios to three-person logical chains," and mentions
real-world Z3 use cases: program verification, VM allocation, automated program synthesis,
circuit design (paraphrase).

Other Knights-and-Knaves-with-Z3 resources found (link only, not fetched):
- https://github.com/pylogic/kkpuzzles ("Knights and Knaves puzzles question and solver formation with z3")
- Discussion thread: https://lobste.rs/s/39ize6/solving_knights_knaves_with_z3

### Other real Z3-puzzle-solver repositories found and directly fetched
- **datahaven/Z3PuzzleSolvers** — https://github.com/datahaven/Z3PuzzleSolvers
  README quote: **"A collection of example code to solve logic puzzles using the Python Z3 SMT solver."** Puzzles sourced from puzzler.com. Files include (per repo listing, direct fetch): `AlphacipherSolver.py`, `BorderSumSudoku.py`, `ChainLinkSolver.py`, `FutoshikiSolver.py`, `MosaicSolver.py`, `StarsSolver.py`, `SuguruSolver.py`, `SujikoSolver.py`. (Grid/logic puzzles, not seating/zebra-style specifically, but same tooling pattern.)
- **taw/puzzle-solvers** — https://github.com/taw/puzzle-solvers
  Confirmed (direct fetch) to use Z3 in Python. README quote: **"Unfortunately Z3 was not available for Ruby or even Python 3, so I decided to do some exercises to learn how to use Z3 with Python 2.x."** Puzzle types solved per repo (direct fetch): Bridges, Light Up, Mini Sudoku, Nonogram, Self-referential puzzles, Sudoku, Verbal Arithmetic, Cryptic Logic puzzles, Letter Connections, Slitherlink, Trees, Nurikabe, Kakuro, Algebra Problems, Geometry Problems, Physics Kinematics Problems, Bit Tricks. (Again, mostly grid/cipher puzzles, not seating-arrangement-style, but demonstrates breadth of Z3 puzzle-solving usage.)
- **merriam/Z3-Examples** — https://github.com/merriam/Z3-Examples — "Z3 (Z3Py) Constraint Solver Well Documented Source Examples." Found via search only; **UNVERIFIED** content (not fetched — the fetch attempt for a related tautvidas.com blog on this topic also failed/was blocked).

### Seating-arrangement / river-crossing specific Z3 examples
- Search (not direct fetch) surfaced: "A seating arrangement puzzle can be modeled in Z3
  using boolean variables representing whether a person sits in a chair... constraints can be
  defined such that if Alice sits on the left or right, Charlie cannot sit in the middle..."
  — general technique description, source page unclear/aggregator. **UNVERIFIED**, no single
  authoritative fetched example found for seating-arrangement-in-Z3 specifically.
- River-crossing: found a Python blog post (not Z3-specific, appears to use plain
  search/graph algorithms, not a solver library): "Solving River-Crossing puzzles using
  python" — https://lahirumadushankablog.wordpress.com/2017/10/27/solving-river-crossing-puzzles-using-python/ — **UNVERIFIED**, not fetched, and per search summary this approach models
  the puzzle as a graph search (states = who's on which bank) rather than as a CSP/SMT
  encoding, so it may not be a good analogy for a Z3/OR-tools "translate to formula, solve"
  pattern.
- General note found via search: river-crossing puzzles are commonly solved via graph/BFS
  state-space search rather than constraint solvers (paraphrase, aggregated from multiple
  search snippets, **UNVERIFIED** as an authoritative claim — no single primary source
  directly fetched for this specific claim).

---

## 3. Google OR-Tools CP-SAT solver — Python API

**Status: real, actively maintained by Google, pip-installable, has a documented Python API and is used for scheduling/assignment-class problems similar to logic puzzles.**

- PyPI: https://pypi.org/project/ortools/
- Official CP-SAT docs (Google Developers): https://developers.google.com/optimization/cp/cp_solver
- Official "Solving a CP Problem" page: https://developers.google.com/optimization/cp/cp_example
- GitHub repo: https://github.com/google/or-tools
- Example source file (directly fetched): https://github.com/google/or-tools/blob/stable/ortools/sat/samples/cp_sat_example.py
- Community CP-SAT primer (extensive third-party doc): https://github.com/d-krupke/cpsat-primer and https://d-krupke.github.io/cpsat-primer/
- hakank's personal OR-tools page (many worked example models): https://www.hakank.org/google_or_tools/ — **UNVERIFIED contents**, WebFetch to hakank.org failed on every attempt (connection refused), only know of its existence/topic via search snippets.

### Package facts (direct fetch of https://pypi.org/project/ortools/)
- Description quote: **"This project hosts operations research tools developed at Google and made available as open source under the Apache 2.0 License."**
- Latest version: **9.15.6755**, released **January 14, 2026**
- Install: `pip install ortools`
- Requires Python >=3.9
- Wheel sizes observed on the PyPI page (direct fetch, sampled across platforms): CP314
  Linux x86-64 29.8–29.9 MB; CP313 Windows 23.9 MB; CP312 macOS ARM64 21.9 MB; CP39 Linux
  ARM64 27.6 MB.
- Cross-check via search (not independently fetched, **UNVERIFIED** as a second source but
  consistent with the direct PyPI fetch): "ortools wheel files range from approximately 21.9
  MB to 29.9 MB depending on platform and Python version."
- Core capabilities per PyPI page (paraphrase): constraint programming (CP-SAT), linear/mixed-integer programming (Glop, MPSolver), vehicle routing, graph algorithms.

### Dependencies (search-derived, UNVERIFIED — not independently confirmed via a direct fetch of package metadata)
Search result claim: **"OR-Tools requires the following dependencies: absl-py, immutabledict, numpy, pandas, protobuf, and typing-extensions."** Source page for this specific claim was not identified/fetched directly — treat as UNVERIFIED, though plausible and consistent with known OR-Tools Python packaging (protobuf is used for OR-Tools' internal model representation).
Also found (search only, historical/context, UNVERIFIED): a past GitHub issue noted Windows
wheel packages once reached 108 MB after adding the `ortools.math_opt` module, exceeding a
PyPI file-size limit, with developers later moving to a shared library to cut this back down
— https://github.com/pypi/support/issues/3714 (title: "File Limit Request: ortools - 125 MB
(windows wheel packages)"). This suggests OR-Tools' dependency/size footprint has fluctuated
across releases and platform-specific wheels can be considerably larger than the current
Linux ~30MB figure.

### Real, directly-fetched full code example — minimal CP-SAT model
Source: https://github.com/google/or-tools/blob/stable/ortools/sat/samples/cp_sat_example.py
(verbatim via direct WebFetch):

```python
#!/usr/bin/env python3

from ortools.sat.python import cp_model

def main() -> None:
    """Minimal CP-SAT example to showcase calling the solver."""
    
    # Creates the model.
    model = cp_model.CpModel()
    
    # Creates the variables.
    var_upper_bound = max(50, 45, 37)
    x = model.new_int_var(0, var_upper_bound, "x")
    y = model.new_int_var(0, var_upper_bound, "y")
    z = model.new_int_var(0, var_upper_bound, "z")
    
    # Creates the constraints.
    model.add(2 * x + 7 * y + 3 * z <= 50)
    model.add(3 * x - 5 * y + 7 * z <= 45)
    model.add(5 * x + 2 * y - 6 * z <= 37)
    
    # Sets objective function.
    model.maximize(2 * x + 2 * y + 3 * z)
    
    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    # Prints solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Maximum of objective function: {solver.objective_value}\n")
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("No solution found.")
    
    # Statistics.
    print("\nStatistics")
    print(f" status : {solver.status_name(status)}")
    print(f" conflicts: {solver.num_conflicts}")
    print(f" branches : {solver.num_branches}")
    print(f" wall time: {solver.wall_time} s")

if __name__ == "__main__":
    main()
```
This is a linear-arithmetic optimization example, not itself a logic puzzle, but shows the
`cp_model.CpModel()` / `new_int_var` / `model.add(...)` / `CpSolver().solve(model)` API
shape referenced elsewhere for puzzle modeling.

### OR-Tools used for logic-puzzle-class problems (search-level evidence only)
- hakank.org is repeatedly cited across multiple independent search results as containing a
  large personal collection of OR-Tools CP-SAT models for classic logic/combinatorial
  puzzles (Einstein/Zebra-style puzzles included per a "Common constraint programming
  problems" index page: https://www.hakank.org/common_cp_models/). I could **not** confirm
  the specific zebra-puzzle file or its content directly — every WebFetch attempt to
  hakank.org domains failed with `connect ECONNREFUSED`. Treat existence of a hakank
  OR-Tools zebra-puzzle model as **UNVERIFIED** (search-snippet only): "the Einstein puzzle
  (a variant of the Zebra puzzle) in multiple languages, including OR-tools CP-SAT/Python"
  (paraphrase of a search summary).
- Google's own docs page (https://developers.google.com/optimization/cp/cp_solver) —
  WebFetch to developers.google.com failed on all attempts (blocked), so I could not directly
  confirm whether Google's official docs include a logic-puzzle example there; only the
  linear-arithmetic example above (fetched from GitHub, not the docs site) was confirmed.
- A practical/independent write-up was found via search: "A practical introduction to
  Constraint Programming using CP-SAT and Python" (pganalyze blog) —
  https://pganalyze.com/blog/a-practical-introduction-to-constraint-programming-using-cp-sat
  — search summary describes an assignment-style example ("Alice, Bob, and Carol pooling
  money with constraints like Alice contributing at least as much as Bob..."), i.e. the
  assignment/allocation puzzle class relevant to seating/ordering puzzles. **UNVERIFIED**
  (not directly fetched).

---

## 4. LLM-to-formal-solver translation for verification (the exact target pattern)

This is well-established as an active academic research area — multiple named systems exist
that do "LLM translates NL problem -> formal representation -> deterministic solver decides
-> answer (optionally fed back to LLM for self-refinement)."

### Logic-LM (Pan, Albalak, Wang, Wang — UCSB)
- arXiv abstract page (directly fetched): https://arxiv.org/abs/2305.12295
- Code: https://github.com/teacherpeterpan/Logic-LLM (linked from the abstract, not independently fetched)
- Venue: EMNLP 2023 Findings; submitted May 20, 2023, revised October 19, 2023.
- Full abstract (verbatim, via direct fetch of arXiv abstract page):
  > "Large Language Models (LLMs) have shown human-like reasoning abilities but still struggle with complex logical problems. This paper introduces a novel framework, Logic-LM, which integrates LLMs with symbolic solvers to improve logical problem-solving. Our method first utilizes LLMs to translate a natural language problem into a symbolic formulation. Afterward, a deterministic symbolic solver performs inference on the formulated problem. We also introduce a self-refinement module, which utilizes the symbolic solver's error messages to revise symbolic formalizations. We demonstrate Logic-LM's effectiveness on five logical reasoning datasets: ProofWriter, PrOntoQA, FOLIO, LogicalDeduction, and AR-LSAT. On average, Logic-LM achieves a significant performance boost of 39.2% over using LLM alone with standard prompting and 18.4% over LLM with chain-of-thought prompting. Our findings suggest that Logic-LM, by combining LLMs with symbolic logic, offers a promising avenue for faithful logical reasoning."
- Note: "LogicalDeduction" is one of its five benchmark datasets — this is exactly the
  ordering/seating-from-clues puzzle class AMDA cares about (paraphrase/inference, dataset
  name only confirmed, not its contents).

### SatLM (Ye, Chen, Dillig, Durrett)
- arXiv abstract page (directly fetched): https://arxiv.org/abs/2305.09656
- Venue: NeurIPS 2023; submitted May 16, 2023, final version October 11, 2023.
- Full abstract (verbatim, via direct fetch of arXiv abstract page):
  > "Prior work has combined chain-of-thought prompting in large language models (LLMs) with programmatic representations to perform effective and transparent reasoning. While such an approach works well for tasks that only require forward reasoning (e.g., straightforward arithmetic), it is less effective for constraint solving problems that require more sophisticated planning and search. In this paper, we propose a new satisfiability-aided language modeling (SatLM) approach for improving the reasoning capabilities of LLMs. We use an LLM to generate a declarative task specification rather than an imperative program and leverage an off-the-shelf automated theorem prover to derive the final answer. This approach has two key advantages. The declarative specification is closer to the problem description than the reasoning steps are, so the LLM can parse it out of the description more accurately. Furthermore, by offloading the actual reasoning task to an automated theorem prover, our approach can guarantee the correctness of the answer with respect to the parsed specification and avoid planning errors in the solving process. We evaluate SATLM on 8 different datasets and show that it consistently outperforms program-aided LMs in the imperative paradigm. In particular, SATLM outperforms program-aided LMs by 23% on a challenging subset of the GSM arithmetic reasoning dataset; SATLM also achieves a new SoTA on LSAT and BoardgameQA, surpassing previous models that are trained on the respective training sets."
- This is directly analogous to AMDA's existing math "program-aided verification" pattern,
  but for logic: SatLM explicitly targets "constraint solving problems that require more
  sophisticated planning and search" where plain program-aided (imperative code) approaches
  are "less effective" — directly relevant framing for whether to extend AMDA's math
  approach to logic_reasoning.

### ICLR 2024 Workshop paper on LLM+Z3 self-refinement
- URL: https://openreview.net/pdf?id=xw06d8NQAd (title from search result: appears to be
  published at "ICLR 2024 Workshop on Secure and Trustworthy Large Language Models")
- **UNVERIFIED / not independently confirmed** — direct WebFetch was blocked by an OpenReview
  bot-check page ("Complete the check below to continue to OpenReview"), so I could not
  extract the actual title, authors or abstract text. What I have is only the earlier
  WebSearch-tool's own synthesized summary (not a page quote), which described: "a novel
  framework that integrates LLMs with a unified Z3 solver, where the LLM translates natural
  language problems into executable neural-symbolic codes, which are then processed by the
  Z3 solver to yield outputs," including "a Self-Refinement Module... that passes
  unsuccessful execution results from the Z3 solver back to the LLM," applied to "deductive
  reasoning, first-order logic reasoning and constraint satisfaction problems." Treat all of
  this paragraph as **UNVERIFIED** (search-engine synthesis, not a direct source quote).

### Global Constraint LLM Agents for Text-to-Model Translation (Cai, Kadıoğlu, Dilkina)
- URL (directly fetched): https://arxiv.org/html/2509.08970v1
- Target formal framework: **MiniZinc** (a constraint modeling language, not Z3/OR-tools
  directly, but same "NL -> formal CSP -> deterministic solve" pattern).
- Quote (verbatim, via direct fetch): **"Natural language descriptions of optimization or satisfaction problems are challenging to translate into correct MiniZinc models"**
- Pipeline (paraphrase of direct fetch): multiple specialized LLM agents each detect and
  generate MiniZinc code for one global-constraint type (e.g. `all_different`, `cumulative`);
  a separate "assembler agent" integrates the snippets into one complete, executable MiniZinc
  model, handling variable declarations, objective, and solve directives. Quote: **"multiple specialized large language model (LLM) agents decompose the modeling task by global constraint type."**
- Stated result (paraphrase, not independently verified against the paper's actual tables):
  this decomposed multi-agent approach "outperforms direct prompting and chain-of-thought
  strategies on standard benchmarks."

### Automated Constraint Model Generation in Configuration Problems (MDPI)
- URL: https://www.mdpi.com/2076-3417/15/12/6518 (title: "Large Language Model-Driven
  Framework for Automated Constraint Model Generation in Configuration Problems")
- **UNVERIFIED** — WebFetch to mdpi.com failed (no output / likely blocked). Only known via
  the earlier WebSearch summary: uses a fine-tuned-LLM system referred to as "ACMG" (Automatic
  Constraint Model Generator) that "leverage[s] fine-tuned LLMs to automate the translation of
  natural language problem descriptions into formal CSP models" (paraphrase of search
  summary, not a direct page quote).

### Other related work found via search only (titles/URLs only, not fetched — listed for completeness, all UNVERIFIED content)
- "A Solver-in-the-Loop Framework for Improving LLMs on Answer Set Programming for Logic
  Puzzle Solving" — https://arxiv.org/abs/2512.17093 — targets Answer Set Programming (ASP,
  via solvers like clingo) rather than CSP/SAT, specifically for logic-puzzle solving; search
  summary says it "only requires problem specifications in natural language and their
  solutions."
- "Logic-of-Thought: Empowering Large Language Models with Logic Programs for Solving Puzzles
  in Natural Language" — https://arxiv.org/abs/2505.16114 (also html: https://arxiv.org/html/2505.16114) — search summary: "Leverages LLMs to translate puzzle rules and states into
  answer set programs... Demonstrates near-perfect accuracy across various grid puzzles."
- "Bridging Natural Language and ASP: A Hybrid Approach Using LLMs and AMR Parsing" —
  https://arxiv.org/pdf/2511.08715
- "Leveraging Large Language Models to Generate Answer Set Programs" (KR 2023) —
  https://proceedings.kr.org/2023/37/kr2023-0037-ishay-et-al.pdf — search summary: "finds
  that LLMs can convert natural language descriptions of puzzles into answer set programming
  languages surprisingly well."
- "Empowering LLMs with Logical Reasoning: A Comprehensive Survey" —
  https://arxiv.org/html/2502.15652v4 — survey covering "solver-based methods that use LLMs
  to translate natural language into symbolic languages such as logic programming,
  first-order logic, constraint satisfaction, or boolean satisfiability formulations"
  (paraphrase of search summary) — likely a good index of further citations but not itself
  fetched/verified here.
- "Bridging Language Models and Symbolic Solvers via the Model Context Protocol" —
  https://drops.dagstuhl.de/storage/00lipics/lipics-vol341-sat2025/LIPIcs.SAT.2025.30/LIPIcs.SAT.2025.30.pdf — appears to connect LLMs to SAT solvers via MCP; not fetched.
- "Reliable Reasoning Beyond Natural Language" — https://arxiv.org/pdf/2407.11373 — surfaced
  under the Z3-translation search; not fetched, content/relevance unconfirmed.
- "Adaptive Selection of Symbolic Languages for Improving LLM Logical Reasoning" —
  https://arxiv.org/html/2510.10703 — not fetched.
- "Can Large Language Models Reason and Optimize Under Constraints?" —
  https://arxiv.org/pdf/2603.23004 — not fetched.
- Workshop/venue potentially relevant as an ongoing-research pointer: "LLM-Solve 2026" —
  https://sites.google.com/view/llm-solve-2026 — not fetched, relevance/content unconfirmed.

---

## 5. Installation footprint summary (facts gathered above, repeated here for convenience)

All figures below are as reported on the respective PyPI pages via direct WebFetch on
2026-07-08 (see sections above for full sourcing):

| Package | Latest version seen | sdist size | wheel size range | Python req |
|---|---|---|---|---|
| python-constraint2 | 2.6.0 (Jun 29, 2026) | 823.9 kB | 1.8 MB – 4.3 MB | >=3.11 |
| z3-solver | 4.16.0.0 (Feb 19, 2026) | 5.1 MB | 13.3 MB – 47.5 MB | not captured |
| ortools | 9.15.6755 (Jan 14, 2026) | not captured | ~21.9 MB – 29.9 MB (sampled platforms) | >=3.9 |

Notes:
- python-constraint2 is by far the lightest of the three — small, mostly-pure-Python-scale
  package.
- z3-solver bundles a compiled native theorem-prover binary inside the wheel, hence the
  10-40x larger wheel size vs. python-constraint2; PyPI page did not surface explicit
  Python-level dependencies.
- ortools wheels are comparably large to z3-solver on Linux (~30MB), and per search-only
  (UNVERIFIED) evidence pulls in several pure-Python dependencies (absl-py, immutabledict,
  numpy, pandas, protobuf, typing-extensions) — pandas/numpy in particular could add
  meaningfully to total installed size and image build time beyond the wheel size itself,
  though numpy/pandas are likely already present in most ML-container base images. A past
  GitHub issue (https://github.com/pypi/support/issues/3714) shows ortools' Windows wheel
  once ballooned to 108-125MB before a fix, indicating the footprint is not perfectly stable
  release-to-release.
- None of the three sizes above are individually close to a 10GB Docker image cap in
  isolation; the comparison would matter more in aggregate with the rest of AMDA's
  dependencies (base Python image, local model weights, existing math-verification tooling,
  etc.) — no data was collected in this pass on AMDA's current image budget breakdown, since
  that is out of scope for this collect-only pass.

---

## Fetch reliability notes (meta, for the analysis session)

Several domains consistently failed to WebFetch during this session, apparently due to a
tool-side domain-verification/allowlist restriction unrelated to the pages' actual
availability (error text: "Unable to verify if domain X is safe to fetch. This may be due to
network restrictions or enterprise security policies blocking claude.ai.") or plain
`ECONNREFUSED`/empty-output failures:
- pypi.org — intermittent: succeeded on 2nd/3rd retry for z3-solver, ortools, and
  python-constraint2 pages, but failed on first attempts.
- github.com — intermittent: succeeded on retry for python-constraint main repo, OR-Tools
  source file, datahaven/Z3PuzzleSolvers, taw/puzzle-solvers.
- developers.google.com — failed on every attempt (3 tries). Google's own CP-SAT docs pages
  were never directly fetched; all Google-docs-derived content above is search-snippet level
  (UNVERIFIED) except the GitHub-hosted example.py source, which was fetched successfully
  from github.com instead.
- hakank.org — failed on every attempt (ECONNREFUSED). hakank's large personal library of
  OR-Tools logic-puzzle models (including a purported zebra/Einstein puzzle model) could
  **not** be directly confirmed; only known to exist via search snippets.
- jamiecollinson.com — failed twice, then succeeded on 3rd attempt (Knights and Knaves
  content above is fully verified from that successful fetch).
- artificialcognition.github.io, www.tautvidas.com, python-constraint.github.io (docs site,
  intro.html specifically), openreview.net, mdpi.com — failed on all attempts made; content
  from these is either absent or marked UNVERIFIED above.

Given the intermittent nature of these failures, a later research pass could likely retrieve
the still-missing pages (Google's own CP-SAT docs, hakank.org's puzzle index, the OpenReview
PDF, the MDPI paper) simply by retrying.
