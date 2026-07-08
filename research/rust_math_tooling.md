# Rust math tooling research — collect-only notes

Date: 2026-07-08. Scope: does the Rust ecosystem offer anything usable for
AMDA's "program-aided math verification" step (currently: LLM emits a bare
arithmetic expression string → `subprocess.run([sys.executable, "-c",
f"print(({expr}))"], timeout=5.0)` → compare numeric result to the model's
stated answer)? Constraints repeated for context while reading this file:
Docker image hard-capped at 10GB compressed, 60s boot-to-ready budget,
project is Python.

This file is **collection only** — facts, URLs, verbatim quotes. No
recommendations, no code, no verdicts. A separate analysis pass reads this.

---

## 1. Rust crates for safely evaluating untrusted arithmetic expression strings

### fasteval (`likebike/fasteval`)
- URL: https://github.com/likebike/fasteval , crates.io: https://crates.io/crates/fasteval
- Verbatim (GitHub README, via fetch): fasteval is "designed to evaluate
  untrusted expressions safely. By default, an expression can only perform
  math operations; there is no way for it to access other types of
  operations (like network or filesystem or external commands)."
- Verbatim caveat: "it _is_ possible for you (the developer) to define
  custom functions which might perform dangerous operations. It is your
  responsibility to make sure that all custom functionality is safe."
- Built-in guards against malicious expressions: length > 4KB, nesting
  depth > 32, more than 64 values, more than 64 sub-expressions — all
  configurable; parser errors out if exceeded.
- Performance claim (docs.rs, https://docs.rs/fasteval/): "fasteval
  consistently achieves the fastest times across every benchmark and in
  every mode of operation (interpreted, compiled, and unsafe)." Benchmarked
  against caldyn, rsc, meval, calc, tinyexpr (C). Compiled mode: 6x caldyn.
  Interpreted mode: 2x the closest competitor (rsc). vs tinyexpr (C, unsafe
  vars): 3x compiled, 1.2x interpreted.
- **Maintenance status (important):** crates.io API
  (https://crates.io/api/v1/crates/fasteval) reports newest version 0.2.4,
  **last updated 2020-01-25**. Total downloads 282,499; recent downloads
  93,125. This crate has not been touched in roughly six years as of this
  research date.
- A community fork exists: `fasteval3` (crates.io:
  https://crates.io/crates/fasteval3), newest version 3.0.1, last updated
  2023-11-29, but total downloads only 3,027 (recent: 50) — very low
  adoption relative to the original.
- No Python bindings found for fasteval or fasteval3 in any search performed.

### evalexpr (`ISibboI/evalexpr`)
- URL: https://github.com/ISibboI/evalexpr , crates.io: https://crates.io/crates/evalexpr
- Verbatim (README via GitHub fetch): "This crate makes extensive use of
  the `Result` pattern and is intended to never panic," with the
  acknowledged exception of allocation-failure panics, which the maintainers
  say Rust doesn't currently let them prevent or formally guarantee against.
- Verbatim, directly on-point for this research question: **"This crate was
  not built with untrusted input in mind, but due to its simplicity and
  freedom of panics it is likely secure."** This is a hedge, not a safety
  guarantee — contrast with fasteval's explicit "designed to evaluate
  untrusted expressions safely" framing.
- The crate allows user-registered custom functions; if the host app wires
  in custom functions, "the user needs to ensure that the functions they
  provide to the crate never panic" — i.e. no sandboxing of custom
  functions, only of the built-in operator set.
- Maintenance status: crates.io API reports newest version **13.1.0**,
  **last updated 2025-11-26** — actively maintained. Total downloads
  8,398,866; recent downloads 1,414,908. Much higher adoption than fasteval.

### meval / meval-rs (`rekka/meval-rs`)
- URL: https://github.com/rekka/meval-rs
- Verbatim: goal is to be "convenient to use, while allowing for some
  flexibility," intended for "configuration of numerical computations in
  Rust" (config files, CLI args) — not framed around untrusted-input safety
  at all.
- Verbatim: the project describes itself as "a toy project" for "learning
  Rust," with "no plan to make this anything more than _math expression ->
  number_ converter," and recommends other libraries for advanced use.
- No explicit statement about safety against untrusted/malicious input.
- Maintenance status: crates.io API reports newest version 0.2.0, **last
  updated 2018-09-30**. Total downloads 1,379,894, recent 158,831. Stale
  (~8 years) but was previously popular.

### rhai (`rhaiscript/rhai`) — embedded scripting language, not just an evaluator
- URL: https://github.com/rhaiscript/rhai , https://rhai.rs/
- Verbatim (https://rhai.rs/book/about/features.html, via fetch):
  - "_Don't Panic_ guarantee – Any panic is a bug. It never panics the host
    system."
  - "Protected against malicious attacks – such as stack-overflow,
    over-sized data, and runaway scripts etc."
  - "Sand-boxed – the scripting Engine, if declared immutable, cannot
    mutate the containing environment unless explicitly permitted."
  - Script execution can be progress-tracked and manually terminated.
  - The implementation "passes Miri" (Rust's UB detector).
  - Language features can be surgically disabled (loops, individual
    keywords/operators) to further restrict what untrusted scripts can do.
- This is explicitly a general-purpose sandboxed scripting engine (a
  superset use case), not narrowly an "evaluate one arithmetic expression"
  tool — heavier-weight than fasteval/evalexpr/meval for this specific job.
- **Performance — honest/counterintuitive finding:** verbatim from
  https://rhai.rs/book/about/benchmarks.html (via fetch): **"In general,
  Rhai is roughly 2x slower than Python 3, which is a bytecodes
  interpreter, for typical real-life workloads."** Specific numbers given
  there for a Fibonacci microbenchmark: Rhai (perf build) 2.25s vs V8/Node
  0.07s. The docs also state: "the purpose of Rhai is not to be blazing
  fast, but to make it as easy and versatile as possible to integrate with
  native Rust applications." So "it's Rust" does not automatically mean
  "faster than Python" once you're running an AST-walking interpreter
  rather than compiled native code — this applies to rhai specifically,
  not to compiled-expression evaluators like fasteval.
- Maintenance status: crates.io API reports newest version 1.25.1, last
  updated 2026-05-29 (very recent/actively maintained). Total downloads
  8,120,097; recent downloads 2,185,781 — comparable adoption to evalexpr.
- No Python bindings for rhai were found in any search performed (searched
  "rhai python bindings pyo3 rhai-py" directly — no dedicated package
  surfaced).

### Comparison to the Python subprocess sandbox (safety guarantees)
- The Python subprocess approach (`subprocess.run([sys.executable, "-c",
  f"print(({expr}))"], timeout=5.0)`) sandboxes by process boundary: the
  spawned interpreter has the same privileges as the parent process (no
  additional OS-level sandboxing such as seccomp/namespaces implied by that
  call alone) but a bug/crash/hang can't corrupt the parent's memory, and a
  timeout kills it. Nothing about `subprocess.run` alone prevents the
  executed Python string from doing `import os; os.system(...)` etc. — the
  "safety" in AMDA's current design comes from constraining what strings
  the LLM is asked to produce (a bare arithmetic expression) and from the
  process boundary/timeout, not from a hardened interpreter restriction.
  (This is inferred directly from the `subprocess.run` call given in the
  task description, not from an external source.)
- fasteval and rhai, by contrast, are safe **by construction**: the
  evaluator's grammar has no way to spell "import a module" or "call an
  arbitrary function" unless the host application explicitly registers a
  dangerous custom function/variable. That is a stronger, language-level
  guarantee rather than a process-boundary guarantee — but only fasteval
  and rhai make this claim explicitly; evalexpr and meval do not (see
  quotes above).
- No direct primary-source benchmark comparing "spawn a Python subprocess
  to eval an arithmetic string" against "call a Rust evaluator" for this
  specific use case (LLM-generated math expression verification) was found
  despite targeted searches (queries tried: "program aided / program of
  thought LLM math expression safe eval sandbox subprocess rust",
  "restrictedpython vs simpleeval vs subprocess safe math expression
  evaluation python", etc.). This appears to be a gap in public
  writeups/benchmarks, not a settled comparison — **marking this
  explicitly as NOT FOUND rather than guessing.**
- Indirect data point on subprocess overhead, Python core devs' own numbers
  (https://bugs.python.org/issue11314, verbatim from the issue thread):
  Python 3.2-era measurements: "fork + execv + waitpid: 4794.4 ms" and
  "subprocess.popen: 10152.1 ms" for 1000 iterations in one of their test
  loops (i.e. ~5-10ms per subprocess in that specific benchmark loop,
  exact methodology not restated here — read the issue directly before
  citing a per-call number). The thread's conclusion, paraphrased: overhead
  differences were considered insignificant for typical applications and
  matter mainly under high-volume process creation.
- Separate secondary/UNVERIFIED data point via search snippet only (not
  independently fetched from a primary source): a SuperFastPython article
  ("Forking Processes is 20x Faster Than Spawning in Python",
  https://superfastpython.com/fork-faster-than-spawn/) reportedly states
  forking 1,000 processes ≈ 2.07s (≈2.07ms/process) vs spawning 1,000
  processes ≈ 42.3s (≈42.3ms/process) — **UNVERIFIED, only seen via search
  snippet, not fetched directly.**
- fasteval's own microbenchmarks (docs.rs page) operate in the
  nanosecond-to-microsecond range per expression evaluation (compiled/
  unsafe modes), which is orders of magnitude below subprocess-spawn
  latency (milliseconds) — this is an apples-to-oranges comparison (in-
  process function call vs new OS process) but is the closest concrete
  numeric contrast found for "Rust evaluator speed" vs "subprocess speed."

---

## 2. Rust evaluators callable from Python (PyO3/maturin) — practical integration cost

### PyO3 / maturin, general facts
- PyO3: https://github.com/pyo3/pyo3 , https://pyo3.rs/ — "Rust bindings
  for the Python interpreter," supports writing native Python extension
  modules or embedding Python in a Rust binary; supports CPython, PyPy,
  GraalPy.
- Maturin: https://github.com/PyO3/maturin , https://www.maturin.rs/ —
  build/publish tool for PyO3 (and cffi/uniffi) extensions as Python wheels.
  Verbatim (maturin docs, via search synthesis): "You need Rust 1.83 or
  later and Python 3.9 or later" for maturin itself; typical workflow is
  write Rust → annotate with PyO3 macros → compile to `.so`/`.pyd` →
  `import` like any Python module.
- Verbatim (maturin distribution docs, via search): the official
  `pyo3/maturin` Docker image "is based on the manylinux2014 image and is
  very basic, containing only Python, maturin, and stable Rust" — i.e. a
  build-time-only container; not something you'd want in a slim runtime
  image.
- Maturin has a `--strip` flag "to strip the library for minimum file
  size" (per maturin docs, via search synthesis) — relevant if a team did
  build a custom Rust extension for this project.
- Named production users of PyO3 per its own docs/search summary: Polars,
  Ruff, Pydantic v2, orjson, cryptography, Hugging Face tokenizers — i.e.
  the tooling itself is mature and widely used in production Python
  packages generally, independent of whether it's a good fit for AMDA's
  specific narrow use case.

### A concrete, already-existing PyO3 wrapper around a safe expression evaluator: `py-evalexpr`
- PyPI: https://pypi.org/project/py-evalexpr/ — wraps the `evalexpr` Rust
  crate via PyO3. Exposes `evaluate`, `evaluate_int`, `evaluate_float`, and
  a `StatelessContext` class. Install via `pip install py-evalexpr`.
- This means a Python project genuinely could pull in a Rust arithmetic
  evaluator via a normal `pip install`, without touching Rust/Cargo/maturin
  at build time, **as long as a prebuilt wheel exists for the target
  platform/Python version** (see wheel sizes below) — it would only need a
  Rust toolchain if pip had to build from sdist because no matching wheel
  exists.
- Exact wheel sizes, latest version 1.1.1, fetched from PyPI JSON API
  (https://pypi.org/pypi/py-evalexpr/json):
  - `manylinux_2_17_x86_64` (cp311): 502,419 bytes (~0.5 MB)
  - `manylinux_2_17_aarch64` (cp311): 498,217 bytes
  - `musllinux_1_2_x86_64` (cp311): 673,236 bytes
  - `win_amd64` (cp311): 353,283 bytes
  - `macosx_11_0_arm64` (cp311): 455,017 bytes
  - (full table has cp311/cp312/cp313 variants; sizes above are
    representative — all sub-megabyte to ~0.7MB.) This is negligible
    against a 10GB image cap.
  - Both manylinux **and** musllinux wheels are published, meaning it
    would install as a prebuilt wheel on both glibc-based (Debian/Ubuntu-
    slim) and musl-based (Alpine) Python base images without needing a
    Rust compiler in the Docker build.
- No independent verification was done of `py-evalexpr`'s maintenance
  activity/star count/last-release date beyond the PyPI listing itself
  (version 1.1.1 present); treat its long-term maintenance status as
  unconfirmed beyond "a released, installable package with multi-platform
  wheels exists today."

### Symbolica (see also section 3) as a second concrete example
- PyPI: https://pypi.org/project/symbolica/ — "Symbolica provides fully
  typed Python bindings using the pyo3 crate" (from symbolica.io release
  post, https://symbolica.io/posts/stable_release/, verbatim).
  `pip install symbolica`.
- Exact wheel sizes for version 1.0.2 (fetched via PyPI JSON API,
  https://pypi.org/pypi/symbolica/1.0.2/json):
  - `manylinux_2_17_x86_64` (cp38-abi3): 22,951,270 bytes (~22.9 MB)
  - `macosx_10_12_x86_64` (cp310-abi3): 22,518,957 bytes
  - `macosx_11_0_arm64` (cp310-abi3): 20,654,181 bytes
  - Uses the stable ABI (`abi3`) tag, meaning one compiled wheel per
    platform covers many Python versions (cp38+) rather than needing a
    separate wheel per Python minor version.
  - ~23MB is still trivial against a 10GB image budget, but is ~45x larger
    than the py-evalexpr wheel, consistent with Symbolica being a full CAS
    rather than a bare expression evaluator.
- Symbolica license, per crates.io API (https://crates.io/api/v1/crates/symbolica):
  license field reported as **"Non-standard"** — corroborates the
  symbolica.io post's own framing that it is "source available" and "free
  for hobbyists" / "free for non-commercial use" rather than a standard
  OSI-approved open-source license (MIT/Apache/BSD). Worth flagging
  explicitly since it differs from the fully-permissive licensing of e.g.
  sympy (BSD) that the project's existing math-verify/sympy dependency
  presumably relies on.

### General build-complexity takeaway (facts only, no recommendation)
- Because manylinux/musllinux wheels exist for at least these two examples
  (py-evalexpr, symbolica), a slim Docker image would not need `rustc`/
  `cargo` in the final image or even in the build stage, provided pip can
  resolve a matching prebuilt wheel for the base image's platform tag and
  Python version — this is the same story as any other popular PyO3-backed
  package (orjson, tokenizers, cryptography, etc., all ship manylinux
  wheels).
- If no matching wheel existed for a given platform/Python combination,
  pip would fall back to building from source, which *would* require a
  Rust toolchain in the build environment — this is a real risk only for
  unusual platforms (e.g. less-common architectures) or brand-new Python
  versions not yet covered by a project's `abi3`/per-version wheel matrix.

---

## 3. Rust symbolic-math / CAS crates (sympy analog)

### Symbolica
- URL: https://symbolica.io/ , crates.io: https://crates.io/crates/symbolica ,
  release post: https://symbolica.io/posts/stable_release/
- Verbatim: "Symbolica is a blazing fast computer algebra system for Python
  and Rust, born of a need to push the boundaries of computations in
  science and enterprise." Also: "Symbolica is world-class in rational
  arithmetic, outperforming Mathematica, Maple, Form, Fermat, and other
  computer algebra packages" (per search-result synthesis of the site's own
  marketing copy — treat the "outperforming" claim as the vendor's own
  characterization, not an independently verified benchmark).
- Capabilities listed: building/manipulating symbolic expressions, pattern
  matching with wildcards, solving linear systems with symbolic
  parameters, converting to rational polynomials, derivatives, integration,
  polynomial factorization, series expansion.
- No direct feature-parity comparison to sympy was found in the fetched
  content (the release post does not claim to be a sympy replacement; it
  positions itself around performance/rational arithmetic rather than
  breadth of coverage). Whether it covers the breadth of sympy (calculus,
  ODEs, number theory, geometry, statistics, etc.) was not established by
  this research — **not verified either way.**
- Licensing caveat repeated from section 2: "Non-standard" per crates.io,
  source-available / free-for-hobbyists-and-noncommercial per the vendor's
  own post — not a standard permissive OSS license.
- Companion MIT-licensed crates were spun out: **Numerica** (high-
  performance number types: "error-tracking floats and finite field
  structs") and **Graphica**, together described as "18.5k lines of
  open-sourced code" (symbolica.io release post, verbatim-adjacent
  paraphrase of the post's own description).

### rusymbols
- URL: https://github.com/simensgreen/rusymbols , crates.io:
  https://crates.io/crates/rusymbols
- Verbatim (GitHub README via search synthesis): "rusymbols is a Rust
  crate for symbolic mathematics. It aims to become a full-featured
  computer algebra system (CAS) while keeping the code as simple as
  possible in order to be comprehensible and easily extensible." States
  its goal is "at least to become similar to SymPy" — i.e. explicitly
  aspirational/not-there-yet by the project's own framing.
- Design pillars stated: simplicity, speed ("maybe not at maximum speed,
  but still fast"), safety, universality (nalgebra compatibility).
- Maturity: latest version found was 0.1.2, crates.io metadata indicating
  last update around February 2021 — stale, ~5 years old as of this
  research date, and pre-1.0.

### Rust community's own assessment of CAS maturity
- Source: Rust users forum thread "Computer Algebra System in Rust,"
  https://users.rust-lang.org/t/computer-algebra-system-in-rust/49016
  (fetched directly).
- Verbatim/paraphrased findings from that thread: "nalgebra is definitely
  an option. But it is not a CAS" (distinguishing linear-algebra libraries
  from true symbolic CAS). A prototype called **bullet** was discussed with
  the explicit warning "**DO NOT USE IN PRODUCTION**" and support for
  symbolic differentiation/basic expression trees but no matrix support.
  Another crate, **algebraics** (real algebraic numbers, polynomial
  factoring), was explicitly characterized in the thread as "not a CAS"
  either, but a narrower numerical library. Suggestions in the thread
  included porting the Yacas CAS kernel to Rust via c2rust, or building on
  the `maths_traits` crate; an older `algebra` crate was noted as
  abandoned.
- Thread's overall picture (paraphrased, not a single verbatim line):
  as of that discussion, no production-ready, sympy-comparable CAS existed
  natively in Rust; contributors were still at the foundational/prototype
  stage. Note the thread's date was not confirmed during this research —
  treat "as of that discussion" as approximate; Symbolica (section above)
  postdates or was not mentioned in that thread and is the most complete
  Rust CAS found in this research, with the license caveat noted above.

---

## 4. "Derivation paths" — step-by-step derivation/proof representation in Rust

Honest headline: **no mature, widely-adopted Rust tool was found that is
purpose-built for "represent or verify a step-by-step arithmetic/math
word-problem derivation."** What exists is either (a) general-purpose
proof assistants aimed at formal logic/type theory, not word-problem-style
arithmetic derivations, or (b) one small, early-stage, explicitly
experimental project that does track rewrite steps for simple arithmetic.

### The one close-ish match: Croof
- URL: https://github.com/alexjercan/croof
- Verbatim/paraphrased from README (via fetch): described as "a minimal,
  readable proof-oriented language for defining and evaluating mathematical
  objects and theorems," enabling formalization through definitions,
  axioms, and algebraic manipulation.
- It does track step-by-step transformation: the README shows sample
  output of the form "Expression: 1 + 1 - 1 + 1 => succ(0) + 1 ... - 0 + 2
  => 2 ... Result: 2" with each transformation step annotated by the rule
  applied — i.e. this is a genuine (if toy-scale) "derivation path" output.
- Scope is narrow: natural numbers (ℕ), booleans, arithmetic operators
  (+, *, -), logical operators (&&, ||), comparisons (<) — explicitly
  scoped to "simple math expressions" per the repo's own title/description.
- Maturity: 39 GitHub stars, 3 forks, 67 total commits per the fetched
  README/repo stats — small, early-stage/experimental project. The README
  has a "Future Extensions" section listing unimplemented features
  (complex data types, improved evaluation strategies), which the project
  itself frames as still in progress.

### Other Rust proof-assistant-adjacent projects found (general survey, not derivation-path-specific)
Source: https://github.com/newca12/awesome-rust-formalized-reasoning
(fetched directly; this is a curated awesome-list, not a primary source
for any individual project's claims — treat the one-line descriptions
below as the awesome-list's own summaries).
- **Acorn** (https://github.com/acornprover/acorn) — "theorem prover with
  built-in AI assistant."
- **Canonical** (https://github.com/chasenorman/Canonical) — "solver for
  type inhabitation in dependent type theory."
- **Esther** (https://github.com/aodhneine/esther) — "simple automated
  proof assistant."
- **hakim** (https://github.com/babaeee/hakim) — "hacky interactive
  theorem prover."
- **homotopy-rs** (https://github.com/homotopy-io/homotopy-rs) —
  "implementation of homotopy.io proof assistant" (homotopy type theory,
  not arithmetic word problems).
- **LSTS** (https://github.com/Lambda-Mountain-Compiler-Backend/LSTS) —
  "proof assistant that is also a programming language."
- **minimo** (https://github.com/gpoesia/minimo) — "an environment for
  learning formal mathematical reasoning from scratch."
- **Noq** (https://github.com/tsoding/Noq) — "Not Coq. Simple expression
  transformer that is not Coq."
- **OxiLean** (https://github.com/cool-japan/oxilean) — "theorem prover &
  dependent type checker inspired by Lean 4."
- **Poi** (https://github.com/advancedresearch/poi) — "pragmatic
  point-free theorem prover assistant."
- **watson** (https://github.com/Dragon-Hatcher/watson) — "a proof
  assistant with an extensible syntax system and Lua-based tactics."
- Equational-reasoning / rewrite-adjacent (closer to "derivation" in
  spirit, but for research/SMT contexts, not word-problem math):
  **cyclegg** (https://github.com/nadia-polikarpova/cyclegg, "cyclic
  theorem prover for equational reasoning using egraph"), **ruler**
  (https://github.com/uwplse/ruler, "rewrite rule inference using equality
  saturation"), **Carcara** (https://github.com/ufmg-smite/carcara, "proof
  checker and elaborator for SMT proofs in the Alethe format"), **rate**
  (https://github.com/krobelus/rate, "clausal proof checker (DRAT, DPR)
  for certifying SAT solvers' unsatisfiability results").
- None of these are positioned, in their own one-line descriptions, as
  tools for "verify that an LLM's step-by-step arithmetic word-problem
  solution is correct" — they target formal logic, dependent type theory,
  or SMT/SAT proof certificates, which is a different problem domain from
  AMDA's math word-problem verification. No claim is made here about their
  internal maturity beyond what's quoted; most were not independently
  fetched beyond the awesome-list's one-line summary.

### No "sympy .simplify() with step tracking"-style CAS was found in Rust
- Targeted searches for a Rust equivalent of "step-by-step equation
  solver" surfaced only numeric-only solvers (**eqsolver**,
  https://crates.io/crates/eqsolver — "numerically solving equations,
  optimising objective functions, and integrating functions," no symbolic
  step output) and a very small symbolic-algebra crate (**expression-solver-rust**,
  https://github.com/natepisarski/expression-solver-rust) whose README was
  not fetched in this research (title/description only, via search
  snippet — **UNVERIFIED** beyond that).
- Conclusion for this question, stated plainly per the task's request for
  honesty: **nothing notable found.** The Rust ecosystem does not appear to
  have a "derivation path" tool that is more mature or more applicable to
  AMDA's word-problem-verification use case than what a hackathon team
  could build in a few lines of Python (e.g. logging each transformation
  step manually), and Croof (the one project that does show step
  annotations) is a 39-star, 67-commit hobby project scoped to natural
  numbers/booleans — not something to depend on for a hackathon submission
  judged partly on reliability.

---

## 5. Direct performance/safety comparison data: subprocess vs Rust evaluator, for this exact use case

Stated plainly, per the task's explicit request to report an honest "not
useful" finding where applicable: **no primary-source benchmark, blog post,
or GitHub issue discussion was found that directly compares "spawn a
Python subprocess to eval an untrusted arithmetic expression" against
"call a Rust expression evaluator" for this specific use case (verifying
an LLM's math word-problem answer).** Searches tried (see queries above)
surfaced only:
- General subprocess-overhead numbers (Python core devs' own bug-tracker
  discussion, https://bugs.python.org/issue11314, quoted in section 1).
- General Rust-vs-Python speed comparisons unrelated to this specific
  sandboxing question (e.g. generic "Rust vs Python 2026 benchmarks"
  blog content, not fetched as it's off-topic aggregator material).
- fasteval's own in-process microbenchmarks (nanosecond/microsecond scale)
  and Rhai's own benchmark showing it is ~2x *slower* than Python for
  typical workloads (both quoted in section 1) — useful as reference
  points but neither is a same-paper comparison against a subprocess
  sandbox.
- Python-side alternatives to subprocess sandboxing that did surface in
  search (not Rust, included here only because they came up while
  searching for prior art on "safe eval" comparisons and may be useful
  context for the analysis pass): **simpleeval**
  (https://github.com/danthedeckie/simpleeval, "Simple Safe Sandboxed
  Extensible Expression Evaluator for Python," whitelists functions,
  blocks dangerous operations by design, has built-in limits like a max
  exponent of 4,000,000) and **RestrictedPython**
  (AST-based restriction, used in Plone CMS; per search synthesis it had a
  disclosed vulnerability CVE-2021-32819 via `_getattr_` allowing forbidden
  attribute access — i.e. AST-restriction sandboxes have a track record of
  being bypassable). These are pure-Python, not Rust, so strictly outside
  this research's scope, but flagged as the closest thing found to a
  documented safety comparison point for "expression sandboxing" in
  general.

---

## Source list (all URLs cited above, deduplicated)

- https://github.com/likebike/fasteval
- https://crates.io/crates/fasteval
- https://docs.rs/fasteval/
- https://crates.io/crates/fasteval3
- https://crates.io/api/v1/crates/fasteval (JSON API, fetched)
- https://crates.io/api/v1/crates/fasteval3 (JSON API, fetched)
- https://github.com/ISibboI/evalexpr
- https://crates.io/crates/evalexpr
- https://crates.io/api/v1/crates/evalexpr (JSON API, fetched)
- https://github.com/rekka/meval-rs
- https://crates.io/api/v1/crates/meval (JSON API, fetched)
- https://github.com/rhaiscript/rhai
- https://rhai.rs/
- https://rhai.rs/book/about/features.html (fetched)
- https://rhai.rs/book/about/benchmarks.html (fetched)
- https://crates.io/api/v1/crates/rhai (JSON API, fetched)
- https://bugs.python.org/issue11314 (fetched)
- https://superfastpython.com/fork-faster-than-spawn/ (UNVERIFIED, snippet only)
- https://github.com/pyo3/pyo3
- https://pyo3.rs/
- https://github.com/PyO3/maturin
- https://www.maturin.rs/
- https://pypi.org/project/py-evalexpr/
- https://pypi.org/pypi/py-evalexpr/json (fetched)
- https://symbolica.io/
- https://symbolica.io/posts/stable_release/ (fetched)
- https://crates.io/crates/symbolica
- https://crates.io/api/v1/crates/symbolica (JSON API, fetched)
- https://pypi.org/project/symbolica/
- https://pypi.org/pypi/symbolica/1.0.2/json (fetched)
- https://github.com/simensgreen/rusymbols
- https://crates.io/crates/rusymbols
- https://users.rust-lang.org/t/computer-algebra-system-in-rust/49016 (fetched)
- https://github.com/alexjercan/croof (fetched)
- https://github.com/newca12/awesome-rust-formalized-reasoning (fetched)
- https://crates.io/crates/eqsolver
- https://github.com/natepisarski/expression-solver-rust (UNVERIFIED, snippet only)
- https://github.com/danthedeckie/simpleeval

## Notes on gaps / things not verified

- Did not independently fetch/verify: expression-solver-rust README,
  py-evalexpr's own GitHub repo (404'd when a guessed URL was tried; the
  correct repo URL was not tracked down), the exact date of the Rust CAS
  forum thread, whether Symbolica's Python wheels include musllinux
  variants (only manylinux/macOS were seen in the fetched JSON for version
  1.0.2 — Windows and other platforms may also exist but were not listed
  in the fetched summary).
- Did not find any primary source specifically discussing Docker
  image-size or cold-boot-time impact of adding a PyO3-based dependency —
  this was inferred from wheel-size data (sub-MB to ~23MB, both trivial
  against a 10GB cap) rather than any article measuring container boot
  time with/without such a dependency.
- All "no direct comparison found" statements above reflect the searches
  actually performed in this session; they are not a certification that no
  such comparison exists anywhere on the web.
