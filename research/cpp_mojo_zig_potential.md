# C++/Mojo/Zig Potential — Research Log (COLLECT ONLY)

Research log for AMDA (Track 1 AMD Hackathon), triggered by: "investigate other
languages like C++, mojo and Zig (Only in case they upgrade our project)."
COLLECT ONLY — no code changes, no repo edits outside this file. Bullets = URL
+ verbatim quote or clearly-marked paraphrase. UNVERIFIED = found only via
search snippet, not a direct fetch of the primary source.

**Project facts used as the baseline for this research** (read directly from
the repo, not from search):
- `/home/anbu/26_class/AMDA/Dockerfile`: base image `python:3.12-slim`;
  installs only `libgomp1` via apt (comment: "OpenMP runtime required by the
  prebuilt llama.cpp binaries"); copies a **prebuilt** `tools/llama-b9888/`
  binary directory (39MB on disk) — llama.cpp is not compiled during the
  Docker build today, it's shipped as a binary.
- `docker/entrypoint.sh`: boots `llama-server` on `127.0.0.1:8080` with
  `-t "$(nproc)"` (CPU threads only, no GPU device flags), polls
  `/health` for up to 40s inside the 60s boot budget, then execs
  `python -m agent.main`.
- `agent/local_llm.py`: talks to `llama-server` via the `openai` Python SDK
  (`OpenAI(base_url=config.LOCAL_BASE_URL, ...)`), i.e. HTTP over loopback,
  OpenAI-compatible `/v1/chat/completions`, with a `grammar` field passed
  through `extra_body` for GBNF constrained decoding.
- `agent/verifiers.py`: math verification runs
  `subprocess.run([sys.executable, "-c", f"print(({expr}))"], ...)` — a
  Python subprocess evaluating an arithmetic expression extracted from LLM
  output.
- `requirements.txt`: just `openai>=1.60` and `httpx>=0.27`. No compiled
  extensions currently.
- Local inference is CPU-only in the current architecture (no `--device`
  passthrough, no ROCm/CUDA flags anywhere in Dockerfile/entrypoint).

---

## 1. llama-cpp-python (`abetlen/llama-cpp-python`) — Python bindings that skip the HTTP layer

- Source: https://github.com/abetlen/llama-cpp-python (fetched directly)
  - Description: "Simple Python bindings for @ggerganov's llama.cpp library."
  - "Low-level access to C API via ctypes interface" — confirms it wraps the
    C API via **ctypes**, not cffi, and "mirrors the llama.h header directly"
    (paraphrase of README content).
  - Also ships its own "OpenAI compatible web server" — i.e. the project
    itself offers *both* an in-process API and an HTTP server mode, it isn't
    exclusively a bypass mechanism.
  - Maintenance signal (fetched page, snapshot 2026-07-08): latest release
    tag observed `v0.3.33-hip-radeon` (Jul 6, 2026); repo shows 2,162
    commits, 463 releases, 10.5k stars, 77 open PRs, 597 open issues —
    actively maintained. Note the `-hip-radeon` tag suggests an AMD
    ROCm/HIP build variant exists.

- Source: https://raw.githubusercontent.com/abetlen/llama-cpp-python/main/README.md
  (fetched directly)
  - Verbatim: "Requirements: Python 3.8+, C compiler (Linux: gcc or clang,
    Windows: Visual Studio or MinGW, MacOS: Xcode)."
  - Verbatim: "To install the package, run: `pip install llama-cpp-python`.
    This will also build `llama.cpp` from source and install it alongside
    this python package." — **default pip install compiles from source**,
    requiring a C/C++ toolchain in the build environment.
  - Verbatim: "It is also possible to install a pre-built wheel with basic
    CPU support. `pip install llama-cpp-python --extra-index-url
    https://abetlen.github.io/llama-cpp-python/whl/cpu`" — a
    compiler-free path does exist for CPU-only use.
  - Docker: "A Docker image is available on GHCR... `docker run --rm -it -p
    8000:8000 -v /path/to/models:/models -e MODEL=/models/llama-model.gguf
    ghcr.io/abetlen/llama-cpp-python:latest`"

- **Directly verified (not from search/fetch, from `curl` against the wheel
  index itself)**: `https://abetlen.github.io/llama-cpp-python/whl/cpu/llama-cpp-python/`
  lists, for v0.3.33, a `manylinux2014_x86_64.manylinux_2_17_x86_64` wheel —
  i.e. a genuinely prebuilt, compiler-free wheel for the exact glibc/x86_64
  target AMDA's `python:3.12-slim` container would need. `curl -sIL` on the
  download URL (redirected to
  `release-assets.githubusercontent.com`) returned `content-length:
  23138675` — **~22.1 MB** for the CPU wheel. This confirms a
  no-compiler-needed installation path exists and is small.

- Source: https://pypi.org/project/llama-cpp-python/ (fetched directly)
  - Source distribution itself listed at 70.5 MB; supports Python 3.8–3.14.
  - JSON Schema-constrained output is documented at this level ("constrain
    chat responses to only valid JSON or a specific JSON Schema").

- Source: https://llama-cpp-python.readthedocs.io/en/latest/ (fetched
  directly) — no direct comparison of latency vs the llama.cpp HTTP server
  is present in the docs; no explicit recommendation either way.

- **GBNF grammar support — confirmed real, not just JSON-schema-only.**
  Source: https://deepwiki.com/abetlen/llama-cpp-python/6.1-grammar-based-generation
  (fetched; DeepWiki is a secondary/derived source, cross-checked against
  the initial WebSearch snippet of the actual source file
  `llama_cpp/llama_grammar.py`, which independently listed the same
  pre-defined grammar constants):
  - `LlamaGrammar.from_string(grammar: str)` — "Creates a grammar from a raw
    GBNF string" (direct GBNF input, not just JSON schema).
  - Also `from_file(...)` and `from_json_schema(...)`.
  - Built-in constants include `JSON_GBNF`, `ARITHMETIC_GBNF`, `C_GBNF`,
    `LIST_GBNF` — the `llama_cpp/llama_grammar.py` file itself (per the
    original WebSearch result title/snippet,
    https://github.com/abetlen/llama-cpp-python/blob/main/llama_cpp/llama_grammar.py)
    independently corroborates these names exist in-repo.
  - Paraphrase from DeepWiki: this GBNF implementation "leverages the
    underlying llama.cpp engine's native GBNF support," i.e. it is meant to
    be the same grammar dialect AMDA already uses against `llama-server`'s
    `grammar` field (`agent/local_llm.py`, `agent/grammars.py`) — so
    switching bindings would not require rewriting AMDA's existing GBNF
    grammar strings, if the analysis session wants that datapoint.

- **Latency: no clean win, and one direct signal it can be worse for short
  prompts.** Source:
  https://github.com/abetlen/llama-cpp-python/discussions/2073 (fetched
  directly — GitHub Discussion titled "Diagnosing Latency in llama.cpp
  Python Wrapper for Short Prompts"):
  - Verbatim (maintainer response, per fetch summary): "The wrapper adds
    extra cost just for being in Python. If it calls into C++ too often (say
    per-token callbacks or too much tokenization in Python), that overhead
    is noticeable when the prompt is short."
  - Verbatim: "The GIL can also cause delays if you mix threading or async
    badly."
  - Verbatim: "If the wrapper is doing tokenization in Python, that can
    dominate when the prompt is short."
  - No benchmark numbers were present in the discussion (explicitly noted
    by the fetch as absent) — this is a qualitative engineering discussion,
    not a quantified result.
  - Recommended mitigations discussed: move tokenization to the C++ side,
    pre-warm the model, batch tokens instead of per-token Python callbacks.

- Search-synthesis (WebSearch, multiple secondary sources blended, **mark
  UNVERIFIED** — no single primary source fetched for this specific
  claim): "For HTTP serving specifically, llama-server (the native C++
  server) typically outperforms the Python wrapper when it comes to latency,
  particularly for Time to First Token (TTFT) on single requests, due to
  avoiding Python overhead and the OpenAI API wrapper overhead that the
  Python client introduces... if you absolutely need really low TTFT, you
  should consider serving from a thin C++ worker and only talk to it from
  Python, so Python isn't in the hot path." This is a search-engine-authored
  synthesis of several results, not a verbatim quote from one document —
  treat as a directional signal only.

- General loopback/HTTP overhead context (WebSearch synthesis, UNVERIFIED
  as applied specifically to llama.cpp — these are generic networking
  numbers, not llama.cpp-measured): "A ping to a loopback address typically
  has a round-trip time often under 1ms." Separately, "HTTP request overhead
  adds several milliseconds at minimum when compared to in-process function
  calls," with cross-process/FaaS HTTP overhead cited elsewhere in the
  10s-of-ms range for non-loopback cases. No source directly measured
  llama-server's own loopback HTTP overhead in isolation from model
  inference time.

- Source: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
  (fetched directly) — llama-server (the binary AMDA already ships)
  self-describes as "Fast, lightweight, pure C/C++ HTTP server," and its
  `/completion` endpoint documents a `"grammar"` parameter: "Set grammar for
  grammar-based sampling. Default: no grammar" — confirms GBNF support at
  the HTTP layer AMDA already uses (this is the mechanism `agent/local_llm.py`
  already calls via `extra_body={"grammar": ...}`). The doc does not compare
  itself against llama-cpp-python or make a latency claim either way.

---

## 2. Mojo / MAX (Modular) — current maturity, and any LLM-serving-specific relevance

- Source: https://mojolang.org/docs/faq/ (fetched directly; this is where
  `docs.modular.com/mojo/faq/` 301-redirects to as of 2026-07-08)
  - Verbatim: "Mojo is working towards a 1.0 release in Summer 2026."
  - Current version stated: **1.0.0b2** (beta 2).
  - Open source status, verbatim: "We have committed to open-sourcing Mojo
    in Fall 2026." — **the compiler is not open source as of this
    research date**; only the standard library is (per the same fetch:
    "the Mojo standard library is fully open-source on GitHub").
  - Verbatim on purpose: "Mojo's initial focus is to solve AI programmability
    challenges," with a longer-term ambition "to grow Mojo into a
    general-purpose programming language," and a note that "You can use it
    for other things like HPC, data transformations, writing pre/post
    processing operations."
  - Platform support, verbatim: "Mojo supports Mac and Linux natively and
    supports Windows via WSL."
  - Distribution: available via "any Python or Conda package manager"; two
    packages offered — `mojo` (full dev tools) and `mojo-compiler` (lighter,
    production-focused). Exact package size was not stated on this page.

- Source: https://www.modular.com/blog/the-path-to-mojo-1-0 (fetched
  directly)
  - Verbatim: "we feel confident that Mojo will get to 1.0 sometime in
    2026," and open-sourcing "will also allow us to open source the Mojo
    compiler as promised," tied to the 1.0 release.
  - On what 1.0 actually targets — verbatim/paraphrase blend from fetch:
    Phase 1 (defining 1.0) focuses on **"writing high-performance kernels
    for GPUs and CPUs."** General-purpose systems-programming features
    (the fetch specifically named async models and private member support)
    are **explicitly deferred beyond 1.0**. This is a direct, primary-source
    statement that Mojo 1.0 is scoped as a GPU/CPU-kernel-authoring language
    first, not a general-purpose scripting/glue language — relevant because
    AMDA's candidate uses (math-expression sandboxing, subprocess glue) are
    exactly the kind of general-purpose systems-programming work Modular
    says is *not* the 1.0 target.

- Search result (WebSearch synthesis, cross-referenced against the two
  fetches above so treated as reasonably reliable, but the specific version
  numbers below were not independently re-verified via direct fetch of a
  changelog page — **mark UNVERIFIED for exact dates**): "Modular Platform
  26.2 (March 2026)... expanded hardware support for NVIDIA B300, Jetson
  Thor, DGX Spark, and AMD RDNA consumer GPUs." "Modular 26.4 (June 2026)
  introduced SOTA MoE Serving, Model Bringup via Agent Skills, Mojo 1.0 Beta
  2." "On May 7, 2026, Modular released Mojo 1.0.0 beta 1 and launched the
  language's website, mojolang.org." "BentoML is joining Modular" announced
  February 2026.

- **Real LLM-serving-specific Mojo project found**: `tairov/llama2.mojo`.
  - Source: https://github.com/tairov/llama2.mojo — description: "Inference
    Llama 2 in one file of pure 🔥" (a Mojo port of Karpathy's llama2.c,
    single-file educational/demo inference implementation, not a
    general-purpose serving stack, not GGUF-based).
  - Directly verified via `gh api repos/tairov/llama2.mojo`: `pushed_at:
    2026-02-09`, `stargazers_count: 2123`, `archived: false`,
    `open_issues_count: 0` — actively maintained, reasonably popular, but
    it is a from-scratch reimplementation of llama2.c in Mojo, **not** a
    Mojo wrapper around llama.cpp/GGUF, and not something AMDA could adopt
    without re-implementing model loading/tokenization/inference from
    scratch in Mojo. This is the most direct "Mojo + LLM inference" example
    found; no other GGUF-compatible or llama.cpp-adjacent Mojo project
    surfaced in search.

- **Modular's own MAX platform does have native GGUF support** (this is
  Modular's production inference engine, separate from the llama2.mojo demo
  above):
  - Source: https://www.modular.com/blog/whats-new-in-max-24-4-max-on-macos-fast-local-llama3-native-quantization-and-gguf-support
    (title confirmed via WebSearch result; not deep-fetched — **UNVERIFIED
    contents beyond the title**, but the title itself directly states GGUF
    support was announced in MAX 24.4).
  - Search-synthesis (UNVERIFIED, no single fetch confirms this precise
    phrasing): `max serve --model meta-llama/Llama-3.1-8B-Instruct
    --weight-path <gguf-file>` is presented as a working CLI invocation
    pattern for serving a GGUF checkpoint through MAX.
  - Adopting this would mean **replacing** llama.cpp/llama-server entirely
    with Modular's MAX serving stack — a full platform swap, not an
    incremental addition alongside the existing setup.

- **MAX Docker image sizes — directly measured, and this is the single
  most load-bearing data point for the "would this fit the 10GB cap"
  question:**
  - Source: https://hub.docker.com/r/modular/max-full (fetched directly)
  - **Compressed image size: 11.9 GB** for `modular/max-full`, described as
    "a Universal MAX image supporting both NVIDIA & AMD GPUs," bundling
    "PyTorch, ROCm, CUDA, and cuDNN libraries."
  - **This single image alone (11.9GB) already exceeds AMDA's entire 10GB
    hard compressed-image cap**, before adding anything else (agent code,
    quantized weights, Python deps). Smaller variants exist by name
    (`max-nvidia-base`, `max-amd-base` — described in a WebSearch synthesis
    as excluding cuDNN/full CUDA, bundling only "CPU PyTorch" — **UNVERIFIED
    exact size**: direct WebFetch attempts against
    `hub.docker.com/r/modular/max-nvidia-base` and
    `.../modular/max-amd-base` both failed during this research session
    (timeout / fetch error) and could not be independently confirmed. Given
    PyTorch-CPU alone commonly runs several hundred MB to >1GB, and these
    "base" images still bundle a driver/runtime layer, treat "smaller" as
    directionally true but **not quantified** here.
  - Source: https://pypi.org/project/modular/ (fetched directly) — the
    `pip install modular` entry wheel itself is tiny (1.7 KB for v26.4.0,
    Jun 18 2026), but this is a thin meta-package; the FAQ fetch above notes
    it pulls in the real toolchain via Conda/pip machinery, and the
    Docker image numbers above are a better proxy for actual footprint on
    disk in a container context. The PyPI page also states: "Not available
    for Windows."

---

## 3. Zig — llama.cpp connection (historical) and sandboxing relevance

### 3a. llama.cpp's Zig build — confirmed dead, not current

- **Directly verified via GitHub API** (`gh api search/code?q=repo:ggml-org/llama.cpp+filename:build.zig`
  against the live `ggml-org/llama.cpp` repo, 2026-07-08): **0 results.**
  There is no `build.zig` anywhere in the current llama.cpp repository.
- **Directly verified via `gh pr view 7471 --repo ggml-org/llama.cpp`**:
  - PR title: **"build : remove zig"**
  - PR body, verbatim: **"I don't think the Zig build system adds much
    value, so suggest to remove it. Are there any important use cases?"**
  - `mergedAt: 2024-05-22T17:05:38Z`
  - URL: https://github.com/ggml-org/llama.cpp/pull/7471
- Companion commit found via `gh api search/commits?q=repo:ggml-org/llama.cpp+zig`:
  message **"readme : remove obsolete Zig instructions (#7471)"**, same
  timeframe.
- History for context (all found via the same commit search, dates
  2023–2024): Zig build support was added back in 2023 (`zig : add build.zig
  (#773)`), went through several maintenance passes (`zig : upgrade build
  system support (#1981)`, `[Zig] Rewrite build for Zig 0.11 (#2514)`, CI
  added in `ci : add Zig CI/CD and fix build (#2996)`), then was formally
  removed May 2024. **Conclusion of this sub-question: the llama.cpp↔Zig
  connection is real but purely historical — it was removed over two years
  before this research date (2026-07-08) with an explicit maintainer
  rationale that it wasn't earning its keep.** A third-party community
  binding (`Deins/llama.cpp.zig` — "llama.cpp bindings and utilities for
  zig") surfaced in search but was not fetched/verified for maintenance
  status; flagged UNVERIFIED, existence-only.

### 3b. Zig for sandboxing untrusted math-expression evaluation

- No source found proposing Zig specifically as a sandboxing layer for
  untrusted code/expression evaluation. The search results that came back
  were about **WebAssembly (WASM)** as the actual sandboxing technology
  being discussed in this space, with Zig appearing only as *one of many*
  languages that can compile to WASM.
- Source: (title/URL only, WebSearch snippet, **UNVERIFIED** — not
  fetched) "Notes on sandboxing untrusted code - why Python can't be
  sandboxed, comparing Firecracker/gVisor/WASM approaches" —
  https://gist.github.com/mavdol/2c68acb408686f1e038bf89e5705b28c
- WebSearch synthesis (blended from multiple results, not a single verbatim
  quote): "WebAssembly provides capability-based sandboxing with no
  filesystem, network, or OS access by default, where every import must be
  explicitly granted by the host, with sub-millisecond startup and
  near-bare-metal compute performance. However, arbitrary Python scripts
  cannot currently run in WASM without compiling the Python interpreter
  itself to WASM along with all its C extensions, making WASM not yet
  viable for general-purpose arbitrary code sandboxing."
- Directly relevant to AMDA's actual use case: the sandbox in
  `agent/verifiers.py` evaluates a **math expression string**, not
  arbitrary Python — `subprocess.run([sys.executable, "-c",
  f"print(({expr}))"], ...)`. No source found proposing or benchmarking a
  Zig-compiled expression evaluator against a Python subprocess for this
  specific narrow task (arithmetic-expression eval). This appears to be an
  unexplored/absent niche in current public discussion, not a validated
  approach with evidence either for or against — genuinely no data either
  way.
- Zig's own build system is moving toward WASM sandboxing **for Zig's own
  build scripts** (not a general-purpose offering): Source:
  https://github.com/ziglang/zig/issues/14286 ("Run build.zig logic in a
  WebAssembly sandbox") — WebSearch snippet describes a proposal to compile
  `build.zig` scripts to `wasm32-wasi` with a separate `build_runner`
  executing steps based on granted permissions. This is Zig tooling
  sandboxing *itself*, not a general facility Zig offers to sandbox
  arbitrary other code (like a math expression from an LLM). **UNVERIFIED
  beyond the WebSearch snippet — not directly fetched.**

---

## 4. Docker image / toolchain cost of adding a compiled component to `python:3.12-slim`

- Source: https://hub.docker.com/_/python (WebSearch synthesis reporting
  the page's content) — `python:3.12-slim` uncompressed size reported as
  ~150MB (for reference; AMDA's actual Dockerfile already uses this base
  today, so this is baseline, not incremental cost).

- **build-essential / gcc / g++ (C++ toolchain path, relevant to
  llama-cpp-python's from-source install and to "C++" generally):**
  - Source: https://packages.debian.org/bookworm/build-essential (fetched
    directly) — download size 7.5 kB, installed size 20.0 kB **for the
    meta-package itself**. This number is misleading in isolation: the
    meta-package has near-zero size because its real weight is in its
    dependencies (`gcc`, `g++`, `libc6-dev`, `dpkg-dev`, `make`), which
    Debian's package page does not itemize with sizes on the same page.
  - Source: https://packages.debian.org/bookworm/g++ (fetched directly) —
    the `g++` package metadata itself also shows a tiny "installed size"
    (14–15 kB), for the same reason: it's a thin package depending on
    `gcc` (`4:12.2.0-3`), whose own page was not reached in this session.
    **These Debian package-page sizes systematically understate real
    on-disk cost** because they exclude transitive dependency closures —
    flagging this explicitly so the analysis session doesn't cite the
    20.0kB / 14kB figures as the real cost.
  - Better proxy (directly fetched): https://hub.docker.com/_/gcc/ — the
    official `gcc` Docker image (Debian-based, e.g. tag `14.4.0-trixie`)
    has a **compressed size of 515.3 MB**. This is a reasonable
    order-of-magnitude analogue for "how much does a working gcc/g++
    toolchain weigh on a Debian base" — i.e. several hundred MB, not
    negligible against a 10GB cap but also not remotely close to blowing
    it by itself. Flagged as an **analogue, not a direct measurement of
    `apt-get install build-essential` on `python:3.12-slim` specifically**.
  - Practical mitigation pattern found via WebSearch (generic Docker
    advice, not project-specific, paraphrase): multi-stage builds — install
    `build-essential`, compile, then copy only the compiled artifact into a
    final stage without the toolchain — are the standard way projects avoid
    paying this cost in the shipped image. AMDA's Dockerfile does not
    currently use multi-stage builds (single `FROM python:3.12-slim` stage
    copying prebuilt binaries).

- **llama-cpp-python specifically avoids this cost if the CPU wheel path is
  used** (cross-reference to Section 1): the prebuilt
  `manylinux2014_x86_64` wheel is ~22.1 MB (directly measured via `curl`
  above) and needs **no compiler in the Docker build at all** — this is
  the cheapest of the three languages/tools researched here, by a wide
  margin, *if* the goal is specifically "call llama.cpp from Python without
  an HTTP hop," rather than "adopt C++ generally."

- **Zig toolchain cost:**
  - WebSearch synthesis, cross-referencing two results: current Zig release
    tarballs for `linux-x86_64` run **approximately 47–51 MB** (e.g. a dev
    build cited at 49,100,292 bytes ≈ 47MB; a 0.15.2 release cited at 51.24
    MiB). Zig ships as a **self-contained tarball** (no apt/system package
    manager dependency chain the way gcc pulls Debian deps), so this ~50MB
    figure is closer to the true marginal cost than the Debian
    build-essential numbers above. **UNVERIFIED to the precise byte for
    "the current stable release as of 2026-07-08"** — direct fetch of
    `ziglang.org/download` failed (domain safety-check block during this
    session); the ~47–51MB figures come from WebSearch snippets referencing
    specific dev/release tarballs, not a single authoritative fetch of
    today's exact stable download.

- **Rust (mentioned alongside C++/Zig/Mojo in the original question's
  framing of "toolchain" cost generally):**
  - No precise install-size figure was found via WebSearch; results were
    generic community discussion (rustup GitHub issues about wanting a
    documented size estimate, e.g.
    https://github.com/rust-lang/rustup/issues/1323 "Specify disk space
    required *before* install" — the issue's existence itself indicates
    Rust's own maintainers don't publish a crisp number). Commonly-cited
    community figures for a full `rustup` + stable toolchain install run
    roughly 1–1.5GB **but this specific range was not independently
    confirmed by a direct fetch in this session — mark UNVERIFIED.**

- **Mojo/MAX toolchain cost** (cross-reference to Section 2): this is the
  standout negative data point of the entire research task. The **directly
  measured 11.9GB compressed `modular/max-full` Docker image** on its own
  exceeds AMDA's entire 10GB compressed-image budget, before any agent
  code, Python deps, or model weights are added. Even granting that a
  CPU-only/base variant would be meaningfully smaller (unconfirmed, see
  Section 2), Mojo/MAX is the only one of the three technologies researched
  where a *directly measured, primary-source* number already conflicts with
  the project's hard constraint.

---

## 5. Summary of what was found (not a recommendation — flagging fit vs. non-fit per the collected evidence only)

This section restates only what the collected evidence above shows, without
adding new claims:

- **llama-cpp-python**: the only one of the three where a genuinely
  toolchain-free, small (~22MB), currently-published installation path was
  *directly verified* to exist and to support the same GBNF grammar
  mechanism (`LlamaGrammar.from_string`) AMDA already depends on via
  `llama-server`'s `grammar` field. The evidence on whether it's actually
  *faster* than the current HTTP-over-loopback approach is thin and mixed:
  the only direct primary source on latency (GitHub Discussion #2073) is a
  qualitative discussion of overhead *sources* in the Python wrapper itself,
  not a benchmark showing it beats `llama-server`, and one search-synthesis
  (UNVERIFIED, blended) suggests the native C++ HTTP server can actually
  win on TTFT for single short requests. No source measured llama-server's
  own loopback-HTTP overhead in isolation to compare against.
- **Mojo**: primary-source evidence (Modular's own FAQ and "path to 1.0"
  blog) shows the compiler is still closed-source as of this research date
  (open-sourcing promised for Fall 2026), the language is at beta
  (1.0.0b2), and Modular's own stated Phase-1/1.0 scope is explicitly
  GPU/CPU **kernel** authoring, not general-purpose scripting — the kind of
  work AMDA's candidate use cases (subprocess glue, sandboxing) would
  require. The one real LLM-inference Mojo project found (`llama2.mojo`) is
  an educational single-file reimplementation, not a GGUF/llama.cpp-
  compatible tool AMDA could drop in. Modular's own production platform
  (MAX) does have native GGUF support, but adopting it means replacing
  llama.cpp entirely, and its full Docker image was directly measured at
  11.9GB compressed — already over AMDA's entire 10GB cap by itself.
- **Zig**: the llama.cpp connection is real but was formally removed from
  the llama.cpp repo in May 2024 (directly confirmed via the merged PR and
  its text), over two years before this research date — it is not a live
  or current avenue. No evidence (positive or negative) was found for Zig
  specifically as a sandboxing mechanism for the math-expression-eval use
  case in `agent/verifiers.py`; this appears to be genuinely unexplored
  territory in public sources, not a validated pattern either way. Zig's
  standalone toolchain is small (~50MB self-contained tarball) if it were
  ever needed for something else.

No further analysis, synthesis, or recommendation is provided per the task
instructions — this is a collection log for a separate analysis session.
