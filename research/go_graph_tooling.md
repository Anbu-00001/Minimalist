# Go-lang graph tooling — collect-only research

Date: 2026-07-08
Scope: user asked "Go lang based graphs which might improve our project in any way,"
specifically re: (1) Go graph/CSP libraries for puzzle classes like our
`logical_reasoning` category (seating/ordering/assignment/zebra/knights-and-knaves),
(2) Go LLM orchestration/routing frameworks as design-idea sources, (3) practical
Python↔Go integration patterns and their overhead, (4) Go graph-algorithm libraries
for topological ordering / constraint propagation / CSP.

This file is **collect-only**: facts, URLs, verbatim quotes. No recommendations,
no code, no verdicts. Items found only via search-snippet (not confirmed by direct
fetch) are marked **UNVERIFIED**.

---

## 1. Go graph/CSP libraries for puzzle-class problems (seating/ordering/assignment)

### 1.1 `gnboorse/centipede` — general CSP solver, includes zebra-puzzle-shaped examples

- URL: https://github.com/gnboorse/centipede
- GitHub API metadata (fetched directly, 2026-07-08): **76 stars**, license
  `Apache-2.0`, `pushed_at: 2022-07-11T01:01:05Z` (i.e., **no commits in ~4 years**),
  `open_issues: 4`, not archived.
- README (raw, verbatim): "Centipede is a Constraint Satisfaction Problem solver
  written in Golang." and "The search algorithm used in this library is an
  implementation of backtracking search." and "This library provides an
  implementation of the popular AC-3 algorithm as `solver.State.MakeArcConsistent()`.
  Call this method before calling `solver.Solve()` to achieve best results."
- README also says, verbatim: "The project is very much a **work in progress**,"
  with MRV/LCV/degree heuristics still only "planned future improvements" — i.e.
  no variable-ordering heuristics implemented yet as of last commit.
- Problems is defined via `Variable`/`Constraint`/`Domain` sets with Go 1.18
  generics; example in README shows numeric variables with custom constraint
  functions and an `AllUnique` constraint generator (directly the pattern needed
  for seating/ordering puzzles: "all different" + relational constraints).
- Repo itself references Sudoku ("See the Sudoku solver (sudoku_test.go) for an
  example of how to use arc consistency") and n-queens/map-coloring-style problems
  per the WebSearch snippet summary of repo topics — **UNVERIFIED** for exact
  example file names beyond what the README shows (sudoku_test.go confirmed;
  zebra/map-coloring test file names not independently confirmed by direct fetch).

### 1.2 Zebra puzzle solved in Go — CSP + backtracking, not graph data structures

- URL: https://dev.to/mcaci/solving-the-zebra-puzzle-using-go-571l (fetched directly)
- Verbatim: "A CSP is composed of a Variable set, a Domain set and a Constraint
  set and the problem is solved when all the variables are assigned domain
  values for which all constraints are satisfied."
- Approach used: "a recursive backtracking algorithm" — the article explicitly
  frames the zebra puzzle as CSP-with-backtracking, **not** as a graph-traversal
  problem. No graph library or graph data structure is used.
- Linked repo: `mcaci/zebra-puzzle-example` (models constraint types like
  `constraint`, `togetherWithConstraint`, `nextToConstraint`, `toTheRightConstraint`
  — this constraint taxonomy maps closely onto our seating/ordering puzzle clue
  types, e.g. "next to," "to the right of," "in the same house as").
- Related Medium version of same article exists at
  https://medium.com/@nikiforos_frees/solving-the-zebra-puzzle-using-go-7d3a4084e057
  (WebFetch blocked fetching medium.com directly in this session; content not
  independently re-verified there, but dev.to mirror was fetched and quoted above).

### 1.3 Knights-and-knaves / seating-arrangement solvers specifically in Go

- Searched directly for Go implementations of knights-and-knaves and seating-
  arrangement puzzle solvers. **Finding: none located.** Existing public solvers
  for knights-and-knaves (`nickmarton/KnightsAndKnavesSolver`,
  `Bram-Hub/Knights-and-Knaves-Solver`, `dmackinnon1/knaves`,
  `vuurball/ai-2-knight-or-knave`, etc.) all appear to be Python/Java/JS-based
  per their repo descriptions in search results; no Go-language hit surfaced.
  This is a **negative finding** — worth being explicit that Go has no notable
  purpose-built library or blog writeup for this exact puzzle subtype.

### 1.4 Graph coloring as the CSP-modeling technique — gonum's Sudoku example

- Package: `gonum.org/v1/gonum/graph/coloring`, part of the `gonum/gonum`
  monorepo (confirmed via GitHub API `contents` listing: the `graph/` directory
  of `gonum/gonum` contains a `coloring/` subpackage with files `coloring.go`,
  `coloring_test.go`, `doc.go`, `sudoku_example_test.go`).
- `coloring.go` doc comment (verbatim, fetched from
  `raw.githubusercontent.com/gonum/gonum/master/graph/coloring/coloring.go`):
  "Dsatur returns an approximate minimal chromatic number of g and a
  corresponding vertex coloring using the heuristic Dsatur coloring algorithm.
  If a partial coloring is provided the coloring will be consistent with that
  partial coloring if possible." (cites Brélaz's Dsatur algorithm, doi in source).
- `sudoku_example_test.go` (verbatim, fetched directly): builds a 9x9 Sudoku as
  an undirected graph where each row/column/3x3-block is turned into a complete
  subgraph via `gen.Complete(g, row(i))` / `col(i)` / `block{r,c}` — i.e. "all
  cells in this group must differ" is literally encoded as "these nodes are
  mutually adjacent," then solved by graph coloring (colors = digits 1-9).
  This is a **concrete, verified example of a Go graph library solving a CSP
  puzzle via graph-coloring**, structurally the same technique used for exam
  scheduling / register allocation (see below) and generalizable to any
  "all-different" constraint group — which is the core structural element of
  zebra/seating/ordering puzzles (e.g. "5 people, 5 seats, no two people in the
  same seat" = one all-different constraint group = one complete subgraph).
- gonum/gonum GitHub metadata: **8,410 stars**, license `BSD-3-Clause`,
  `pushed_at: 2026-05-04` (actively maintained), `open_issues: 247`.
- Separately, the standalone `gonum/graph` repo (pre-monorepo) is **archived**:
  GitHub API confirms `archived: true`, description "Graph packages for the Go
  language [DEPRECATED]", last push 2019-04-26 — its functionality was folded
  into `gonum/gonum`'s `graph/` subpackage, which is the actively maintained one.
- `topo` subpackage (`gonum.org/v1/gonum/graph/topo`, doc comments fetched from
  `github.com/gonum/graph/blob/master/topo/tarjan.go`, verbatim): "Sort performs
  a topological sort of the directed graph g returning the 'from' to 'to' sort
  order. If a topological ordering is not possible, an Unorderable error is
  returned listing cyclic components in g." — i.e. topological sort + cycle
  detection via Tarjan's SCC algorithm. This is generic (task-scheduling-shaped)
  functionality, **not** CSP/constraint-propagation-specific; no built-in
  constraint-propagation primitives beyond what coloring/AC-3-style packages
  provide separately.

### 1.5 Graph coloring for scheduling/assignment — general literature, thin Go tooling

- WebSearch summary (general, not Go-specific) confirms the standard mapping:
  "Problems in scheduling, register allocation in compilers, and radio
  frequency assignment can all be formulated as graph coloring tasks." Sources:
  https://reintech.io/blog/graph-coloring-problem-in-go ,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6756213/ (PMC article on graph
  coloring for large scheduling problems — general CS literature, not Go-specific).
- Beyond gonum's `coloring` package (1.4 above), no other actively-maintained,
  purpose-built Go library specifically targeting scheduling/assignment-as-
  graph-coloring was found. One WebSearch summary noted (quoting the underlying
  snippet, **UNVERIFIED** beyond the search snippet) that a 2010-era paper
  "notes there are no publicly released libraries available for graph coloring";
  the Koala library mentioned there is C++, not Go.

### 1.6 Other general-purpose Go graph libraries (topological sort, DAG, etc.)

- `dominikbraun/graph` — https://github.com/dominikbraun/graph
  - GitHub API: **2,188 stars**, license `Apache-2.0`, `pushed_at: 2024-12-11`
    (i.e. **no commits in ~19 months** as of 2026-07-08 — stale but not archived),
    `open_issues: 54`.
  - README (verbatim via fetch): "A library for creating generic graph data
    structures and modifying, analyzing, and visualizing them." Provides DFS/BFS
    traversal, Dijkstra shortest path, strongly-connected-components, topological
    sort (two variants — a non-recursive Kahn's-algorithm `TopologicalSort` and a
    `StableTopologicalSort` for deterministic output), cycle-prevention on DAG-typed
    graphs, transitive reduction, minimum spanning trees, and Graphviz/DOT
    visualization export.
  - This is a **generic graph toolkit**, not CSP/puzzle-specific — same category
    as gonum's `graph` package but with visualization built in. No constraint-
    propagation or backtracking-search functionality.
- Hungarian algorithm (assignment-problem solver, relevant to "who sits where /
  who gets what" bipartite-matching-shaped sub-problems) exists in Go as small,
  low-star community packages: `oddg/hungarian-algorithm` and
  `arthurkushman/go-hungarian` (both found via WebSearch; **not independently
  fetched/verified** beyond search snippets — star counts and maintenance status
  UNVERIFIED). These solve optimal bipartite assignment (O(n³)), a different
  problem shape than zebra/seating puzzles (which are feasibility/enumeration
  CSPs, not cost-minimization assignment), so relevance to our specific puzzle
  category is limited even if the libraries are solid.

---

## 2. Go-based LLM orchestration/routing frameworks — design ideas

### 2.1 `dshills/langgraph-go` — graph-based LLM workflow orchestration with confidence-gated routing

- URL: https://github.com/dshills/langgraph-go
- GitHub API metadata: only **8 stars**, license `MIT`, `pushed_at: 2025-11-18`,
  `open_issues: 0`. This is a small, low-adoption, single/few-maintainer project.
- README explicitly labels it (verbatim): "⚠️ Alpha Software Warning — LangGraph-Go
  is currently in **alpha** stage. The API is not yet stable... **Not using in
  production** without thorough testing."
- Despite low adoption, the **design pattern is directly on-topic** as a design
  idea (not as an adoptable dependency): it models an LLM pipeline as an explicit
  directed graph of nodes with typed state and **conditional edges gated on a
  confidence field**. Verbatim code from README:
  ```go
  // Conditional edges
  engine.Connect("nodeA", "nodeB", func(s Session) bool {
      return s.Confidence > 0.8
  })
  ```
  This is structurally the same shape as our own local→verify→escalate cascade
  (try local, check a pass/fail or confidence signal, conditionally route to the
  next stage) — expressed as a graph edge predicate instead of an if/else chain.
  Also notable: it ships adapters for both local (`graph/model/ollama`, described
  as "Local model execution (no API costs)") and remote providers (OpenAI,
  Anthropic, Google, AWS Bedrock with "Multi-region failover for high
  availability") behind one `ChatModel` interface, plus a "Deterministic replay"
  feature ("Resume workflows from any checkpoint... no external API calls" during
  replay) intended for debugging production runs by replaying exact past traces —
  a debugging-affordance idea (record-then-replay a cascade run without re-billing
  API calls) that is language-agnostic.
- Given 8 stars / alpha status, treat this as **one hobby project's design
  vocabulary**, not evidence of a proven or widely-adopted pattern.

### 2.2 `cloudwego/eino` — ByteDance's Go LLM framework, graph-based composition, no explicit local/remote routing docs found

- URL: https://github.com/cloudwego/eino
- GitHub API metadata: **12,159 stars**, license `Apache-2.0`, `pushed_at:
  2026-07-07` (actively maintained, pushed the day before this research), maintained
  by CloudWeGo (part of ByteDance).
- README (verbatim, via fetch): "an LLM application development framework in
  Golang. It draws from LangChain, Google ADK, and other open-source frameworks,
  and is designed to follow Golang conventions." Has a `compose` module that lets
  you "connect components into graphs and workflows that can run standalone or
  be exposed as tools for agents" — confirms graph-based orchestration as a
  first-class concept in the most-starred Go LLM framework found.
- The README content fetched did **not** surface explicit documentation of a
  local-first/verify/escalate or multi-model-fallback routing pattern — this is
  marked as "not found in fetched content," not as "confirmed absent," since only
  the top-level README was reviewed, not the full docs site.

### 2.3 `maximhq/bifrost` — Go AI gateway with failover/load-balancing (closest analog to a "router" in Go)

- URL: https://github.com/maximhq/bifrost
- GitHub API metadata: **6,347 stars**, license `Apache-2.0`, created
  2025-03-19, `pushed_at: 2026-07-07T21:01:45Z` (actively maintained, very recent
  push), `open_issues: 569`.
- README (verbatim): "Bifrost is a high-performance AI gateway that unifies
  access to 23+ providers (OpenAI, Anthropic, AWS Bedrock, Google Vertex, and
  more) through a single OpenAI-compatible API. Deploy in seconds with zero
  configuration and get automatic failover, load balancing, semantic caching,
  and enterprise-grade features."
- Relevant features list (verbatim bullets from README): "**Automatic
  Fallbacks** - Seamless failover between providers and models with zero
  downtime" and "**Load Balancing** - Intelligent request distribution across
  multiple API keys and providers." Supported providers explicitly include
  **Ollama** alongside cloud providers, per the "Multi-Provider Support" bullet:
  "OpenAI, Anthropic, AWS Bedrock, Google Vertex, Azure, Cerebras, Cohere,
  Mistral, Ollama, Groq, and more" — i.e. it already unifies local + remote
  backends behind one API, same shape as our router's job.
- Architecturally this is a **persistent HTTP gateway service** you run
  continuously (`npx -y @maximhq/bifrost` or `docker run -p 8080:8080
  maximhq/bifrost`, with a web UI at `localhost:8080`) — not a one-shot CLI or
  library call. Written primarily in Go (per repo language breakdown found via
  WebFetch: Go 75.2%, TypeScript 16.5%, Python 4.1%).
- Marketing claim (verbatim, **unverified independently, vendor's own benchmark
  claim**): "50x lower p99 latency than LiteLLM... overhead staying at roughly
  11 microseconds at 5,000 requests per second" — this is Bifrost's own
  performance marketing copy, not third-party-verified in this research pass.
- Design-idea takeaway (not a recommendation): the fallback/load-balancing
  policy vocabulary (weighted distribution across keys/providers, health-based
  routing) is the same conceptual space as our escalation-order policy, just
  expressed as a config-driven gateway rather than inline Python logic.

### 2.4 `tmc/langchaingo` and Ollama itself — for completeness

- `tmc/langchaingo` (LangChain's Go port): GitHub API — **9,511 stars**,
  license `MIT`, `pushed_at: 2026-01-11`. WebSearch summary describes it as
  mirroring LangChain's Model I/O / Agents&Tools / Vector Store abstractions,
  with backend support including "local runtimes like Ollama" alongside
  OpenAI/Anthropic/Bedrock/Mistral. Not independently verified via direct
  README fetch in this session (WebSearch summary only) — **UNVERIFIED** for
  exact quotes, though repo existence/star count is verified via API.
- Ollama itself (https://github.com/ollama/ollama, not independently re-fetched
  this session but widely known/previously verified): written in Go, wraps
  llama.cpp via cgo, is itself the most prominent example of "Go host process
  driving a C/C++ inference engine" — relevant as a precedent for pattern #3
  below (Go-as-glue-layer calling into a non-Go inference runtime), though
  Ollama's own docs were not re-fetched in this pass (WebSearch summary only,
  from `dasroot.net` and `bytesizego.com` blog posts, not primary Ollama docs).
  **UNVERIFIED** at primary-source level in this session; treat as background
  knowledge with directionally-correct shape confirmed by secondary sources.

---

## 3. Practical Python↔Go integration patterns and their overhead

Three patterns exist; all were found in secondary/blog sources plus one primary
source (gopy repo itself). None of this is puzzle-specific — general integration
research, included because the user's question presumes we might call Go code
from this Python codebase.

### 3.1 Subprocess (invoke a Go binary as an external process)

- Simplest pattern, no special build tooling. WebSearch summary paraphrase:
  "Python's subprocess integration is effective for gluing together commands
  and quickly spinning up data-processing scripts... the subprocess pattern is
  likely most practical [for small projects] — it requires no complex build
  configuration or FFI knowledge." (Source: search-synthesized from multiple
  hits including https://freeacademy.ai/blog/python-vs-go-microservices-performance-comparison-2026 ;
  **UNVERIFIED** as a direct quote — this is the WebSearch tool's own summary
  paraphrase of aggregated snippets, not a verbatim quote from one article.)
- Go binaries are cheap to produce and cheap to start. WebSearch-summarized cold
  start figures (multiple sources, treat as **approximate / UNVERIFIED
  precision**): "Go programs can take approximately 200ms before reaching the
  first line of code during initialization" in unoptimized cases, dropping to
  low single-digit milliseconds with initialization-logic trimming (source:
  https://elsyarifx.medium.com/how-we-cut-our-go-api-cold-start-time-from-200ms-to-5ms-0b553ecb7212 ,
  headline verbatim: "How We Cut Our Go API Cold-Start Time From 200ms to 5ms").
  This is orders of magnitude below our 60s boot budget and would be a
  per-request or per-task cost, not a one-time boot cost, if invoked as a
  subprocess per task.
- Go binary size in Docker: multi-stage builds with `CGO_ENABLED=0` and
  `-ldflags="-w -s"`, on a `scratch` or `alpine` base, commonly cited as
  producing images/binaries in the low tens of MB. Verbatim from one source
  (https://dev.to/young_gao/docker-multi-stage-builds-for-go-from-1gb-to-12mb-production-images-2p1h,
  headline): "Docker Multi-Stage Builds for Go: From 1GB to 12MB Images." A Go
  binary added to an existing Python image would plausibly cost single-digit-to-
  low-double-digit MB, negligible against a 10GB compressed budget — **this
  specific size-budget comparison is my own arithmetic, not a sourced claim**.

### 3.2 cgo (compile Go as a C-shared library, call from Python via ctypes/cffi, or the reverse: gopy)

- `go-python/gopy` — https://github.com/go-python/gopy
  - GitHub API: **2,317 stars**, license `BSD-3-Clause`, `pushed_at:
    2026-07-07T01:03:52Z` (actively maintained, pushed the day before this
    research — contradicts an earlier same-session WebFetch summary that
    described it as only having a "December 2023" latest release; the GitHub
    API `pushed_at` field is the more authoritative signal and shows ongoing
    commit activity through 2026), `open_issues: 60`.
  - README (verbatim, via fetch): "gopy generates (and compiles) a CPython
    extension module from a go package." Requires Go ≥1.15 and a valid `go.mod`
    (modules-based builds).
  - Caveat surfaced in docs (paraphrase from fetch, not a direct quote):
    Python-version mismatches between compile-time and run-time (`-vm=python3`
    flag) can cause import failures — i.e. this path is sensitive to Python
    environment/version drift, a real operational cost for a project targeting
    a specific hackathon judging VM image.
- ctypes/cffi via `-buildmode=c-shared` (secondary sources, blog-level):
  - https://blog.kchung.co/faster-python-with-go-shared-objects/ and
    https://dustymabe.com/2016/09/13/sharing-a-go-library-to-python-using-cffi/ —
    both describe building a Go `.so` with `go build -buildmode=c-shared` and
    loading it from Python via `ctypes`/`cffi`, using the C ABI as the
    interop boundary. Content of these two was **not independently fetched**
    this session (WebSearch summary only) — **UNVERIFIED** at quote level.
  - Related but reverse-direction source (Go calling Python in-process via
    CPython embedding, primary fetch performed):
    https://www.ardanlabs.com/blog/2020/09/using-python-memory.html — verbatim
    performance claim: "this code is about 45 times faster than the equivalent
    gRPC code, the function call overhead (without the outliers calculation
    time) is about 237 times faster." But the same article explicitly warns
    (verbatim): "The code we wrote here is tricky and error prone so you should
    have some tight performance goals before going down this path." This is
    Go-calling-Python (opposite direction from what we'd need), but the
    complexity/caveat is symmetric for Python-calling-Go via cgo: manual
    reference-counting-equivalent bookkeeping, C ABI marshaling, build-toolchain
    coupling (CGO_ENABLED, C compiler availability in the Docker build stage).

### 3.3 HTTP microservice (Go binary runs as a local server, Python calls it over loopback HTTP)

- Standard pattern, well-precedented (e.g. Bifrost itself, see 2.3, runs this
  way). Overhead is network-stack + JSON serialization per call, more than
  subprocess-per-task but less operationally fragile than cgo (no shared
  process memory, no ABI coupling, easy to reason about failure modes — the
  Go process crashing doesn't crash the Python process).
- Directly relevant tension for AMDA specifically: the project brief given to
  me states AMDA is "a single hackathon submission (not a long-lived service)"
  with a **boot-to-ready ≤60s** requirement. An HTTP microservice pattern adds
  a second process to start and health-check during that boot window (versus
  subprocess-per-call, which adds ~0 boot-time cost and only per-task latency).
  This is my own inference connecting the sourced boot-time constraint to the
  sourced integration-pattern trade-offs — **not an externally-sourced claim**.

### 3.4 `pyproc` — a fourth, newer pattern (Unix-domain-socket IPC, no cgo, no HTTP)

- URL: https://github.com/YuminosukeSato/pyproc (found via WebSearch, not
  independently fetched — **UNVERIFIED** at quote level)
- Per WebSearch summary: "Unix domain socket based IPC for ML inference and data
  processing" that lets you "Call Python from Go without CGO or microservices,"
  described as running Python "like a local function from Go... offering lower
  latency than HTTP while avoiding CGO complexity." Note: this tool is built for
  the opposite direction (Go calling Python), not Python calling Go — included
  because the underlying pattern (long-lived worker process + local socket IPC)
  is directionally symmetric and could in principle be inverted, but I found no
  equivalent existing tool built specifically for Python-calls-Go over a Unix
  socket. Its own HN discussion thread
  (https://news.ycombinator.com/item?id=45257929) was located but **could not be
  fetched in this session** (WebFetch returned an empty/failed result) — so
  community sentiment on this specific tool is not captured here.

---

## 4. Honesty check: is Go/graphs actually the lever for our `logical_reasoning` gap?

This section reports findings that bear directly on "is this useful," per the
instruction to be honest including a possible null result. These are not
Go-specific but are necessary context to avoid presenting Go findings out of
proportion to their actual leverage.

- Directly relevant academic result: **Logic.py** (arXiv, fetched directly at
  https://arxiv.org/html/2502.15776v1). Verbatim/near-verbatim results: baseline
  "Llama 3.1 70B Instruct alone" scored **24.9% accuracy** on ZebraLogicBench;
  their LLM-formalizes-then-solver-solves approach ("Logic Agent") reached
  **91.4% accuracy** overall (97.86% easy / 88.89% hard) — described as "a
  remarkable 65% absolute improvement... setting a new state-of-the-art with an
  accuracy of over 90%." **Their stack is Python-based** (a Python-embedded DSL
  called Logic.py, translated via LibCST into C, solved with the CBMC bounded
  model checker) — **no Go involved anywhere in this result.**
- Related WebSearch-summarized (not independently fetched, **UNVERIFIED** at
  quote level) findings from the same search pass:
  - CP-Agent (arXiv 2508.07468, "Agentic Constraint Programming") — Python-based
    per its ecosystem (CPMpy, OR-Tools framing in the summary).
  - "Traditional approaches achieve up to 65% accuracy with Python-based
    frameworks like CPMpy and OR-Tools, while performance with the domain-
    specific MiniZinc language peaks around 50%." All three (CPMpy, OR-Tools,
    MiniZinc) are Python-ecosystem-native or have first-class Python bindings;
    none of the search results surfaced a Go-based equivalent framework used in
    any published LLM+solver logic-puzzle benchmark.
  - A multi-agent SMT approach (arXiv 2407.03956, "Solving Zebra Puzzles Using
    Constraint-Guided Multi-Agent Systems") reported "up to a 166% increase in
    fully correct solutions" using an LLM-to-SMT-LIB translation loop with an
    SMT solver — again Python/SMT-LIB tooling in the summary, not Go.
- Net observation (fact, not recommendation): every published result found that
  meaningfully improves LLM accuracy on this exact puzzle class (zebra-style
  logic puzzles) does so by pairing the LLM with a **symbolic solver reached
  from Python** (OR-Tools, CPMpy, MiniZinc, Z3/SMT, or a custom Python DSL to
  C/CBMC) — not by using Go or a Go graph library. Go's own CSP tooling
  (`centipede`, section 1.1) is comparatively immature (76 stars, 4-year-old
  last commit, explicitly self-described as "work in progress" lacking standard
  heuristics) next to OR-Tools/CPMpy/Z3's maturity and existing Python-native
  bindings.

---

## Summary of sources fetched directly (primary) vs. WebSearch-summarized only (secondary/unverified)

**Fetched directly (primary, quotes verified against actual page/file content):**
- https://github.com/gnboorse/centipede (README, raw)
- https://dev.to/mcaci/solving-the-zebra-puzzle-using-go-571l
- https://github.com/gonum/graph/blob/master/topo/tarjan.go
- https://github.com/dominikbraun/graph (README)
- https://raw.githubusercontent.com/gonum/gonum/master/graph/coloring/coloring.go
- https://raw.githubusercontent.com/gonum/gonum/master/graph/coloring/sudoku_example_test.go
- https://github.com/dshills/langgraph-go (README, raw)
- https://github.com/cloudwego/eino (README)
- https://github.com/maximhq/bifrost (README, raw)
- https://github.com/go-python/gopy (README)
- https://www.ardanlabs.com/blog/2020/09/using-python-memory.html
- https://arxiv.org/html/2502.15776v1 (Logic.py paper)
- GitHub REST API (`api.github.com/repos/...`) for stars/license/last-push/
  archived-status/open-issues on: gnboorse/centipede, dominikbraun/graph,
  gonum/gonum, go-python/gopy, dshills/langgraph-go, cloudwego/eino,
  maximhq/bifrost, tmc/langchaingo, gonum/graph (standalone, archived repo)

**Search-snippet only, not independently fetched (treat as UNVERIFIED for exact
wording, though general existence/topic is credible):**
- oddg/hungarian-algorithm, arthurkushman/go-hungarian
- YuminosukeSato/pyproc and its HN thread (fetch attempt failed)
- blog.kchung.co and dustymabe.com cffi/ctypes Go-sharedlib articles
- freeacademy.ai Python-vs-Go microservices comparison
- tmc/langchaingo README content (star count/license verified via API; README
  text is WebSearch-summarized, not independently fetched)
- CP-Agent (arXiv 2508.07468) and the zebra-puzzle multi-agent SMT paper
  (arXiv 2407.03956) — topic/results as reported in WebSearch summaries only
- Ollama's own architecture (cgo usage) — background knowledge + secondary
  blog sources (dasroot.net, bytesizego.com), not Ollama's own primary docs
