# Logic-Escalation Economics Research Log — AMDA Track 1

Research collection only. Raw facts with URLs and quotes/paraphrases. No synthesis, no
recommendations, no strategy conclusions. Direct quotes are in quotation marks;
paraphrases are marked as such. Anything found only via a search-engine synopsis
(and not confirmed by directly fetching the primary page/PDF) is marked **UNVERIFIED**.

Context note on dates: this research was run under a system clock reporting current
date 2026-07-08. Some arXiv IDs below (2601.xxxxx–2606.xxxxx) reflect that ambient
date and are reported as found.

Research question (verbatim from task brief): given that the AMDA scoring pipeline
gates on an LLM-judge accuracy pass BEFORE ranking by ascending total scored tokens,
and logical_reasoning constraint-satisfaction puzzles (seating, zebra/Einstein,
knights-and-knaves, river-crossing) are the current biggest confirmed accuracy hole
(9 pass / 23 fail; both local model and remote non-thinking gemma-4-31b fail these),
is there primary-source evidence that thinking/extended-reasoning mode measurably
improves accuracy on this specific puzzle class, what it costs in tokens, and whether
"budget forcing" / short reasoning traces capture most of the gain cheaply.

---

## 1. Does reasoning/thinking mode improve accuracy on constraint-satisfaction logic puzzles specifically?

### 1.1 ZebraLogic (AI2 / Bill Yuchen Lin et al.) — the canonical zebra-puzzle benchmark

- Paper URL: https://arxiv.org/abs/2502.01100 (also https://arxiv.org/html/2502.01100v1)
- Authors: Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha
  Poovendran, Peter Clark, Yejin Choi. Submitted Feb 3, 2025 (v1); last revised Jul 15,
  2025 (v2).
- Quote (verbatim, abstract, confirmed by direct fetch of the arXiv abstract page):
  "We investigate the logical reasoning capabilities of large language models (LLMs)
  and their scalability in complex non-monotonic reasoning. To this end, we introduce
  ZebraLogic, a comprehensive evaluation framework for assessing LLM reasoning
  performance on logic grid puzzles derived from constraint satisfaction problems
  (CSPs)... Our results reveal a significant decline in accuracy as problem complexity
  grows -- a phenomenon we term the curse of complexity. This limitation persists even
  with larger models and increased inference-time computation, suggesting inherent
  constraints in current LLM reasoning capabilities."
- Note the last sentence directly: the paper's own framing is that MORE inference-time
  compute (i.e., more thinking) does **not** rescue accuracy once puzzle complexity
  passes a threshold — "This limitation persists even with larger models and
  increased inference-time computation."
- I could not get the full per-model results table to render via WebFetch (both the
  arXiv HTML page and a companion GitHub gist by the lead author returned only prose/
  abstract content, not the table; the official leaderboard at
  https://huggingface.co/spaces/allenai/ZebraLogic is a JS-rendered Space that
  WebFetch could not extract as text). The following numbers therefore come from
  WebSearch result synopses, not a direct fetch of the table itself — **UNVERIFIED**:
  - "o1 outperforms all other models, achieving an overall accuracy of 81.0% on the
    benchmark. In comparison, the best-performing open-weight non-reasoning LLM,
    Sonnet-3.5-1022, only reaches 36.2%." (search synopsis, source cited as the
    ZebraLogic materials)
  - "Medium-complexity puzzles showed a significant decline, with o1 maintaining
    92.1% accuracy but dropping to 42.5% on large-scale problems." (search synopsis)
  - A companion author gist (https://gist.github.com/yuchenlin/2b1f444fc3e9aed973b4b69f9b3926c0)
    was directly fetched and DOES contain this verbatim line: "The best LLM, Claude
    3.5 Sonnet, can only solve 33.4% of all puzzles and just 12.4% of the hard
    puzzles." — this is a slightly different (earlier-snapshot) number than the 36.2%
    figure above; both are attributed to Claude 3.5 Sonnet as the best non-reasoning
    model, so treat the exact percentage as version-dependent but the qualitative
    finding (reasoning models >> non-reasoning models on ZebraLogic; ~2-2.5x gap) as
    corroborated across two independent fetches.
- The author gist also states (directly fetched, verbatim): "Recent research shows
  that greedy decoding usually leads to better performance in hard reasoning
  tasks...most models have better performance in greedy decoding." (tangential to
  the thinking-mode question but relevant to how these benchmarks are usually run.)

### 1.2 BIG-Bench Extra Hard (BBEH) — "Zebra Puzzles" and "Boolean Expressions" tasks

- Paper URL: https://arxiv.org/abs/2502.19187 (PDF: https://arxiv.org/pdf/2502.19187,
  HTML: https://arxiv.org/html/2502.19187v1); also ACL Anthology:
  https://aclanthology.org/2025.acl-long.1285.pdf
- Confirmed via WebSearch synopsis (cross-checked model list against a second,
  independent WebFetch of the same underlying table — see caveat below) that Table 2
  compares "a random baseline, five general-purpose models (Llama 3.1 8b Instruct,
  Gemma2 27b IT, Gemini 2.0 Flash-Lite, Gemini 2.0 Flash, and GPT4o), and three
  reasoning-specialized models (Distill R1 Qwen 32b, DeepSeek R1, and o3-mini
  (high))."
- **This is the single most directly relevant and most surprising data point found
  in this research pass**, so I flag its verification status carefully. A WebFetch of
  https://arxiv.org/html/2502.19187v1 returned the following Table 2 row values for
  the "Zebra Puzzles" task:
  - Gemma2 27b IT: 23.0%
  - Gemini 2.0 Flash-Lite: 32.0%
  - Gemini 2.0 Flash: 44.5%
  - GPT4o: 32.0%
  - DeepSeek R1: 8.0%
  - o3-mini (high): 67.5%
  And for the "Boolean Expressions" task from the same table:
  - Gemma2 27b IT: 25.0%
  - Gemini 2.0 Flash-Lite: 24.0%
  - Gemini 2.0 Flash: 27.0%
  - GPT4o: 22.5%
  - DeepSeek R1: 55.5%
  - o3-mini (high): 67.0%
  **Verification status: UNVERIFIED at the individual-cell level.** I attempted a
  second, independent fetch of the raw PDF (https://arxiv.org/pdf/2502.19187) to
  cross-check this table and it failed to return readable table text (binary/image
  content). I could not independently confirm the DeepSeek R1 = 8.0% on Zebra
  Puzzles cell against a second source. It is plausible on its face — it would be
  consistent with the "curse of complexity" / inverse-scaling findings below — but
  treat the exact number as a single-fetch extraction, not independently
  cross-verified. The corroborating detail (the exact model roster: Llama 3.1 8b
  Instruct, Gemma2 27b IT, Gemini 2.0 Flash-Lite/Flash, GPT4o, Distill R1 Qwen 32b,
  DeepSeek R1, o3-mini (high)) DID match between two independent search/fetch
  results, which increases confidence the table itself is being read correctly even
  if a single cell value could be mis-OCR'd.
- If the DeepSeek R1 = 8.0% figure is accurate, the qualitative finding is: on the
  Zebra Puzzles task specifically, one prominent reasoning-specialized model
  (DeepSeek R1) scored far *below* a smaller non-reasoning model (Gemma2 27b IT,
  23.0%), while on Boolean Expressions the same reasoning model scored far *above*
  (55.5% vs 25.0%). I.e., in this data, "reasoning mode helps" is task-dependent even
  within the logic-puzzle-adjacent BBEH suite, and does not uniformly hold for
  zebra-style constraint puzzles. Only o3-mini (high) — a reasoning model with
  configurable effort — was strong on BOTH (67.5% and 67.0% respectively).
- Separately (also via WebSearch synopsis, not yet fetched from the primary
  paper page directly — **UNVERIFIED**): "Gemma 4 31B from Google currently leads
  the BIG-Bench Extra Hard leaderboard with a score of 0.744 across 11 evaluated AI
  models." This 74.4% figure matches (see §4 below) the figure independently found
  on the Gemma-4-31B-it Hugging Face model card, so I treat the 74.4% number itself
  as reasonably well corroborated (two independent sources), though I could not
  confirm from either source whether that number was measured with the model's
  optional thinking mode ON or OFF (see §4).

### 1.3 BIG-Bench Hard (original, Suzgun et al.) — CoT vs answer-only on logical_deduction-class tasks

- Paper URL: https://arxiv.org/abs/2210.09261
- Authors: Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay,
  Hyung Won Chung, Aakanksha Chowdhery, Quoc V. Le, Ed H. Chi, Denny Zhou, Jason Wei.
  Submitted Oct 17, 2022. (Confirmed via direct WebFetch of the abstract page.)
- Quote (verbatim, abstract): "We find that applying chain-of-thought (CoT) prompting
  to BBH tasks enables PaLM to surpass the average human-rater performance on 10 of
  the 23 tasks, and Codex (code-davinci-002) to surpass the average human-rater
  performance on 17 of the 23 tasks. Since many tasks in BBH require multi-step
  reasoning, few-shot prompting without CoT, as done in the BIG-Bench evaluations
  ..., substantially underestimates the best performance and capabilities of language
  models, which is better captured via CoT prompting."
- Note: BBH's "logical_deduction" (three/five/seven objects — an ordering-puzzle-style
  task very close to AMDA's seating/ordering puzzle category) is one of the 23 BBH
  tasks, but I was not able to extract the task-specific CoT-vs-no-CoT delta for
  logical_deduction alone from the fetched content (only the abstract-level aggregate
  statistics above were retrievable). A WebSearch synopsis (not independently
  fetched — **UNVERIFIED**) separately reported: "Chain-of-thought prompting confers
  substantial gains, enabling Codex (d-002) in CoT regime to reach 73.9%—a +17.3
  percentage point improvement over answer-only prompting" — this appears to be an
  aggregate-BBH number, not logical_deduction-specific; flagged as UNVERIFIED and of
  uncertain task scope.
- Also UNVERIFIED (search synopsis only): "even logically invalid CoT rationales
  deliver nearly the same accuracy gains as valid ones (Δ ≈ −2%, p ≈ 0.025),
  suggesting that surface form and multi-step demonstration structure—not strict
  logical fidelity—drive the observed improvements." I could not identify which paper
  this specific claim originates from (it surfaced in a search synopsis without a
  clear attributed source separate from the BBH paper); treat as unverified and of
  unconfirmed provenance.

### 1.4 Same-family reasoning-vs-non-reasoning pair: Qwen3-30B-A3B Instruct-2507 vs Thinking-2507

- Primary source, directly fetched Hugging Face model cards (highest-confidence data
  point in this file for a clean same-family A/B):
  - Qwen3-30B-A3B-**Instruct**-2507 (non-thinking):
    https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507 — benchmark table
    (directly fetched) reports **ZebraLogic: 90.0**, AIME25: 61.3, HMMT25: 43.0,
    GPQA: 70.4, LiveBench 20241125: 69.0. The same table lists comparison models
    Deepseek-V3-0324 (ZebraLogic 83.4) and Gemini-2.5-Flash (ZebraLogic 57.9).
  - Qwen3-30B-A3B-**Thinking**-2507: https://huggingface.co/Qwen/Qwen3-30B-A3B-Thinking-2507
    — benchmark table (directly fetched) does **not** list a ZebraLogic score at all.
    It reports AIME25: 85.0, HMMT25: 71.4, GPQA: 73.4 (compared in the same table
    against Gemini-2.5-Flash-Thinking and Qwen3-235B-A22B).
  - So for this same-family pair, I could NOT obtain a direct ZebraLogic thinking-vs-
    non-thinking comparison (the Thinking variant's card simply omits that
    benchmark). What IS directly confirmed: on AIME25 (math, not logic-puzzle, but
    the closest reasoning-heavy benchmark reported by both cards), Thinking scores
    85.0 vs Instruct's 61.3 (+23.7 points); on GPQA, Thinking scores 73.4 vs
    Instruct's 70.4 (+3.0 points, much smaller gap).
  - An earlier WebSearch (before the direct HF fetches above) had produced a
    **conflicting and now-superseded** synopsis claiming "Qwen3-30B-A3B-Instruct-2507
    achieved 93.0% accuracy [on ZebraLogic] with CoT prompting, while ...Thinking-2507
    achieved 95.5%." This does not match the directly-fetched Instruct card's own
    reported 90.0 ZebraLogic figure, and I could not find the 95.5% Thinking figure on
    the Thinking card at all. **I am flagging the 93.0/95.5 pair as UNVERIFIED and
    likely unreliable** — it conflicts with a primary-source direct fetch and should
    not be trusted without independent confirmation.

### 1.5 "Reasoning Effort and Problem Complexity" — Tents puzzle (logic grid / CSP puzzle) scaling study

- Paper URL: https://arxiv.org/abs/2503.15113
- Authors: Benjamin Estermann, Roger Wattenhofer. Submitted Mar 19, 2025. (Confirmed
  via direct WebFetch of abstract page.)
- Quote (verbatim, abstract): "We use the infinitely scalable Tents puzzle, which has
  a known linear-time solution, to analyze this scaling behavior. Our results show
  that reasoning effort scales with problem size, but only up to a critical problem
  complexity. Beyond this threshold, the reasoning effort does not continue to
  increase, and may even decrease. This observation highlights a critical limitation
  in the logical coherence of current LLMs as problem complexity increases..."
- Models tested (from a direct WebFetch of the HTML full text,
  https://arxiv.org/html/2503.15113): Gemini 2.0 Flash Thinking (DeepMind), OpenAI
  o3-mini, DeepSeek R1, Qwen/QwQ-32B-Preview — i.e., this paper tests only
  reasoning-mode models against each other on a CSP-style puzzle, not a thinking-vs-
  non-thinking pair on the same base model, so it cannot directly answer "does
  thinking help vs not" — but it is direct evidence that even among reasoning models,
  results diverge sharply: "DeepSeek R1: Second-best performance; also reached
  [solved] size 100" vs "Qwen/QwQ-32B-Preview: Significantly degrades with increasing
  problem size, struggling to solve instances larger than 25" (paraphrase from
  fetched content) and "No model solved problems with a problem size exceeding 100"
  (paraphrase).
- Directly relevant to token cost: paraphrase from the same fetch: "DeepSeek R1
  consistently uses more tokens than o3-mini across problem sizes" while o3-mini had
  the highest success rate — i.e., in this study more reasoning tokens did not
  correlate with better accuracy across models. Also: "High reasoning effort enables
  solving larger instances but also increases token usage for smaller, already
  solvable problems" (paraphrase) — i.e. thinking-token overhead is paid even on easy
  instances where it isn't needed.

### 1.6 "Inverse Scaling in Test-Time Compute" — more thinking can actively hurt constraint tracking

- Paper URL: https://arxiv.org/abs/2507.14417
- Authors: Aryo Pradipta Gema, Alexander Hägele, Runjin Chen, Andy Arditi, Jacob
  Goldman-Wetzler, Kit Fraser-Taliente, Henry Sleight, Linda Petrini, Julian Michael,
  Beatrice Alex, Pasquale Minervini, Yanda Chen, Joe Benton, Ethan Perez. Submitted
  Jul 19, 2025 (v1); revised Dec 15, 2025 (v2). Confirmed via direct WebFetch of the
  abstract page.
- Quote (verbatim, abstract): "We construct evaluation tasks where extending the
  reasoning length of Large Reasoning Models (LRMs) deteriorates performance,
  exhibiting an inverse scaling relationship between test-time compute and
  accuracy. Our evaluation tasks span four categories: simple counting tasks with
  distractors, regression tasks with spurious features, **deduction tasks with
  constraint tracking**, and advanced AI risks. We identify five distinct failure
  modes when models reason for longer: 1) Claude models become increasingly
  distracted by irrelevant information; 2) OpenAI o-series models resist distractors
  but overfit to problem framings; 3) models shift from reasonable priors to spurious
  correlations; 4) **all models show difficulties in maintaining focus on complex
  deductive tasks**; ..."
- This is a directly on-point primary source: one of the paper's four evaluation task
  categories is explicitly "deduction tasks with constraint tracking" (i.e., exactly
  the zebra/knights-and-knaves/seating-puzzle shape), and the paper's core finding is
  that for these tasks, LONGER reasoning traces can make accuracy WORSE, not better,
  across multiple frontier model families.

### 1.7 JustLogic — reasoning vs non-reasoning models on synthetic deductive reasoning

- Paper URL: https://arxiv.org/abs/2501.14851
- Authors: Michael K. Chen, Xikun Zhang, Dacheng Tao. Submitted Jan 24, 2025 (v1);
  revised May 9, 2025 (v2). Confirmed via direct WebFetch of abstract page.
- Quote (verbatim, abstract): "Our experimental results on JustLogic reveal that (i)
  state-of-the-art (SOTA) reasoning LLMs perform on par or better than the human
  average but significantly worse than the human ceiling, and (ii) SOTA
  non-reasoning models still underperform the human average."
- Additional numbers found via WebSearch synopsis (**UNVERIFIED** — not confirmed via
  direct fetch of a results table): "Llama3-8B (57.8%), Llama3-70B (64.6%), and
  GPT-4o (65.6%), perform significantly worse than the average human performance
  (73.0%). In contrast, ...OpenAI o1-preview, performed substantially better, with an
  accuracy of 81.0%." This is a general (not puzzle-grid-specific) synthetic deductive
  reasoning benchmark, not zebra/seating/knights-and-knaves puzzles per se, but is
  reasoning-benchmark-adjacent.

---

## 2. Token cost delta of thinking mode

### 2.1 Primary/semi-primary sources with concrete numbers

- **"Reasoning Models Can Be Effective Without Thinking"**
  URL: https://arxiv.org/abs/2504.09858 (also https://arxiv.org/pdf/2504.09858)
  Authors: Wenjie Ma, Jingxuan He, Charlie Snell, Tyler Griggs, Sewon Min, Matei
  Zaharia. Submitted Apr 14, 2025. Confirmed via direct WebFetch of the abstract page.
  - Quote (verbatim, abstract): "Using the state-of-the-art DeepSeek-R1-Distill-Qwen,
    we find that bypassing the thinking process via simple prompting, denoted as
    NoThinking, can be surprisingly effective. When controlling for the number of
    tokens, NoThinking outperforms Thinking across a diverse set of seven challenging
    reasoning datasets--including mathematical problem solving, formal theorem
    proving, and coding--especially in low-budget settings, e.g., 51.3 vs. 28.9 on
    ACM 23 with 700 tokens... Our method outperforms a range of baselines with
    similar latency using Thinking, and is comparable to Thinking with significantly
    longer latency (up to 9x)."
  - Additional number found via WebSearch synopsis of the same paper's results
    (**UNVERIFIED** at table level — a second direct PDF fetch to the same paper
    returned unreadable binary content, so this specific cell was not independently
    cross-checked): "On MiniF2F and ProofNet, NoThinking is comparable to Thinking
    across all values of k while using 3.3–3.7x fewer tokens." Formal theorem proving
    (MiniF2F/ProofNet) is structurally close to constraint-satisfaction logic (both
    require exact multi-step formal correctness), though not the same task type as
    zebra/seating puzzles.
  - Together: this paper's headline claim is a **9x latency multiplier** for Thinking
    to match a NoThinking+parallel-sampling approach at comparable accuracy, and (less
    verified) a **3.3–3.7x token multiplier** specifically on formal-proof-style tasks.

- **AdaptThink: Reasoning Models Can Learn When to Think**
  URL: https://arxiv.org/abs/2505.13417 (fetched via
  https://ar5iv.labs.arxiv.org/html/2505.13417). Authors: Jiajie Zhang, Nianyi Lin,
  Lei Hou, Ling Feng, Juanzi Li (Tsinghua University). Confirmed via direct fetch.
  - Quote (verbatim, abstract): "Notably, on three math datasets, AdaptThink reduces
    the average response length of DeepSeek-R1-Distill-Qwen-1.5B by 53% and improves
    its accuracy by 2.4%, highlighting the promise of adaptive thinking-mode
    selection for optimizing the balance between reasoning quality and efficiency."
  - Per-dataset numbers extracted from the fetched content (paraphrase of a results
    table, moderate confidence — single fetch, not independently cross-checked cell
    by cell):
    - GSM8K: 50.9% length reduction, +4.1% accuracy
    - MATH500: 63.5% length reduction, +1.4% accuracy
    - AIME2024: 44.7% length reduction, +1.6% accuracy
    - DeepSeek-R1-Distill-Qwen-7B (larger model): average 40.1% response-length
      reduction with +2.3% accuracy gains across benchmarks.
  - Note: these are math datasets, not logic-grid puzzles, but the result pattern
    (large token savings AND a small accuracy improvement, not just a tradeoff) is
    directly relevant to the "is full thinking worth the tokens" question.

### 2.2 Aggregator/blog sources on general thinking-mode token multipliers (lower confidence, explicitly marked)

These did not come from arXiv papers or model vendor documentation; they are
industry-blog aggregations found via WebSearch. I list them because the task brief
asked for "real token cost delta" data points, but they should be weighted much less
than §2.1 and are marked UNVERIFIED / secondary throughout:

- tokenmix.ai (blog, "Thinking Tokens Trap: How Reasoning Models Burn max_tokens
  (2026)"): reported via WebSearch synopsis as claiming "Real billing data from
  Claude, Gemini, and DeepSeek R1 show 4-15x cost multipliers when thinking tokens
  are enabled" and "Production routing patterns typically cut thinking-token spend by
  60 to 80% with zero detectable quality loss on easy tasks." **UNVERIFIED**
  (WebFetch of this exact domain was blocked by the fetch tool's domain-safety
  check during this session, so I could not confirm this directly from the source
  page — reported here only as a search-engine synopsis of a secondary blog.)
- aioutlooks.com (blog, "Thinking Tokens Explained"): WebSearch synopsis reported "A
  single thinking call can spend 3 to 10x the tokens of a normal completion."
  **UNVERIFIED**, secondary blog.
- eg3.com: WebSearch synopsis reported "Internal-reasoning tokens can be $5-50× the
  visible volume" and "reasoning traces often consume 5–10× more tokens than the
  final answer" and "Reasoning multiplies the effective output by 5-20 times on
  agentic tasks." **UNVERIFIED**, secondary blog, and internally the numbers from
  this single source already span a 4x range (5x to 20x) depending on task type,
  underscoring how noisy/context-dependent these public multiplier claims are.
- **Observation (not a citation, a pattern noted across the above secondary
  sources):** every blog-sourced token-multiplier figure I found fell somewhere in
  the broad 3x–30x range, with no two sources agreeing on an exact number, and each
  source's own claims varied 2-4x internally depending on task type. This is reported
  as a factual observation about source disagreement, not a synthesized estimate.

### 2.3 Nous Research "Measuring Thinking Efficiency in Reasoning Models" (semi-primary — vendor research blog, not peer reviewed)

- URL: https://nousresearch.com/measuring-thinking-efficiency-in-reasoning-models-the-missing-benchmark
- Directly fetched. Methodology (paraphrase): tested multiple large reasoning models
  across three task categories, generation limit 30,000 tokens, reasoning effort set
  to "high," reasoning tokens extracted from API responses / char-to-token ratio
  analysis.
- Quote/paraphrase from direct fetch, on the "Logic Puzzles" category specifically:
  "Efficiency gap reduced to 'far less pronounced than for math and knowledge
  questions'" for logic puzzles, compared to a much larger gap for math and knowledge
  tasks. This directly suggests that for logic-puzzle-shaped tasks specifically,
  models' reasoning-token usage is closer together across models than it is for
  math — i.e., the puzzle-type-specific multiplier may be smaller than the general
  3x-30x figures being thrown around for reasoning tasks broadly.
- Other concrete numbers from the same direct fetch (math domain, for token-scale
  calibration only, not logic-puzzle-specific): "DeepSeek-R1-0528 vs gpt-oss-120b on
  single AIME problem: 3,104 vs 268 reasoning tokens respectively" — an 11.6x
  difference between two specific reasoning models on one math problem, illustrating
  that even among "thinking-enabled" models the token cost varies enormously by
  model, not just by thinking-on/off.
- The report explicitly states (direct fetch) it "lacks direct ablation studies
  showing accuracy-to-token tradeoffs when deliberately reducing reasoning budgets on
  identical tasks" — i.e., it is a cross-model comparison, not a same-model
  budget-forcing study.

### 2.4 "Reasoning Token Efficiency Leaderboard" (heyneo.com — first-party vendor benchmark blog, not peer reviewed)

- URL: https://heyneo.com/blog/reasoning-token-efficiency-leaderboard
- Directly fetched. Published June 12, 2026 by "the HeyNEO Team" (an AI engineering
  platform); described in the page itself as first-party (their own benchmark, not an
  aggregation of others' numbers).
- Methodology (direct quote): "Logic Puzzles — knights and knaves, muddy children,
  hat puzzles, river crossings, graded as boolean True/False extraction" is one of
  four 5-task categories (20 tasks total across all categories) — this is the single
  closest benchmark description to AMDA's own logical_reasoning puzzle mix found in
  this entire research pass.
- However, the fetched content only exposed AGGREGATE (all-category) results, not the
  Logic-Puzzles-only breakdown, despite a follow-up fetch attempt specifically
  requesting the category split (the page states results are further broken out only
  in a linked GitHub repo / CLI tool that was not fetched in this session). Aggregate
  table (June 9, 2026 snapshot; direct fetch):

  | Model | Accuracy | Reasoning Tokens | Efficiency (acc/1000 tokens) |
  |---|---|---|---|
  | Gemini 2.5 Pro | 80.0% | 1,900 | 0.421 |
  | Grok-4.3 | 60.0% | 216 | 2.78 |
  | Claude Opus 4.8 | 65.0% | adaptive | — |
  | DeepSeek-R1 | 65.0% | — | — |
  | Kimi-K2 | 65.0% | — | — |
  | GPT-4.1 | 40.0% | — | — |

  These are ALL-CATEGORY aggregates (AIME math + Logic Puzzles + Code Debugging +
  Formal Proofs combined, 20 tasks, so N is small per model — treat precision as
  low), not logic-puzzle-isolated numbers. Flagging clearly: **the Logic-Puzzles-only
  cells could not be extracted**, only the combined-category table above.

---

## 3. "Budget forcing" — does limited/short reasoning capture most of the gain cheaply?

### 3.1 s1: Simple test-time scaling (the paper the task brief explicitly named)

- Paper URL: https://arxiv.org/abs/2501.19393 (v1/v2/v3 all resolve to the same
  record); code: https://github.com/simplescaling/s1; project page:
  https://simplescaling.github.io/
- Authors: Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei,
  Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, Tatsunori
  Hashimoto. Submitted Jan 31, 2025 (last revised Mar 1, 2025). Confirmed via direct
  WebFetch of the abstract page.
- Quote (verbatim, abstract): "we develop budget forcing to control test-time compute
  by forcefully terminating the model's thinking process or lengthening it by
  appending 'Wait' multiple times to the model's generation when it tries to end.
  This can lead the model to double-check its answer, often fixing incorrect
  reasoning steps. After supervised finetuning the Qwen2.5-32B-Instruct language
  model on s1K and equipping it with budget forcing, our model s1-32B exceeds
  o1-preview on competition math questions by up to 27% (MATH and AIME24). Further,
  scaling s1-32B with budget forcing allows extrapolating beyond its performance
  without test-time intervention: from 50% to 57% on AIME24."
- Additional detail from a direct fetch of the full HTML text
  (https://ar5iv.labs.arxiv.org/html/2501.19393): Figure 4(a) caption, quoted: "For
  the three rightmost dots, we prevent the model from stopping its thinking 2/4/6
  times, each time appending 'Wait' to its current reasoning trace." Also: "For
  AIME24 specifically, Figure 1 indicates the final result: at 7,320 tokens, s1-32B
  achieves 57% accuracy" (paraphrase of the fetch tool's reading of Figure 1), and
  performance "does eventually flatten out at six times" [Wait-insertions]
  (paraphrase).
- **Limitation explicitly noted**: I could not extract a granular
  budget-vs-accuracy table (e.g., accuracy at 1K, 2K, 4K, 8K tokens) from either the
  abstract page or the ar5iv full-text fetch — the paper communicates the
  budget-forcing sweep primarily via a figure (Figure 4a), which the fetch tool could
  read the caption of but not the underlying plotted data points. So the specific
  claim in the task brief — "does short reasoning get MOST of the accuracy gain at a
  FRACTION of the token cost" — is only partially answerable from what I could fetch:
  the paper's own framing is that MORE forced continuation (up to 6x "Wait"
  insertions) monotonically increases accuracy up to a saturation point, not that a
  short trace captures most of the gain; the 50%→57% jump (AIME24) is presented as
  the full extrapolated gain from budget forcing, and I do not have a confirmed
  intermediate data point (e.g., "at 2x Wait-insertions, accuracy is already at
  55%") from what was fetchable in this session.

### 3.2 AdaptThink — adaptively skip thinking on easy items (see also §2.1)

- Same paper as cited above: https://arxiv.org/abs/2505.13417. Central point directly
  relevant to "budget forcing" framing: rather than forcing a SHORT trace on every
  problem, AdaptThink teaches the model to skip thinking ENTIRELY on problems it
  judges easy, and only think on hard ones. Quote (verbatim, abstract): "we first
  demonstrate that NoThinking, which prompts the reasoning model to skip thinking and
  directly generate the final solution, is a better choice for relatively simple
  tasks in terms of both performance and efficiency." This is evidence for a
  DIFFERENT budget-economy strategy than s1's "force a short-but-nonzero trace" — it
  is binary (think fully or not at all, chosen per-problem) rather than a continuous
  token-budget dial, and the paper's own result (55.9%→ average across the three
  math datasets, 40-63% length reduction with SMALL POSITIVE accuracy deltas, not
  losses) is direct evidence that indiscriminately-full thinking is not required to
  get (in that paper's tasks) the accuracy benefit.

### 3.3 "Do Thinking Tokens Help or Trap?"

- Paper URL: https://arxiv.org/abs/2506.23840 (fetched via
  https://ar5iv.labs.arxiv.org/html/2506.23840). Authors: Bowen Ding, Yuhan Chen,
  Futing Wang, Lingfeng Ming, Tao Lin (Zhejiang University, Boston University,
  ByteDance, Westlake University). Confirmed via direct fetch.
- Quote (verbatim, abstract): "our pilot study reveals that these thinking-token-
  induced behaviors are not essential for effective problem-solving and may even
  hinder correct reasoning within constrained token budgets."
- Numbers extracted from the direct fetch (paraphrase/quote mix, moderate
  confidence): "ThinkTokenPenalty baseline: Achieves 30.6% token reduction while
  maintaining comparable accuracy on the base model"; "DuP-PO results: Delivers 4.0
  points average performance gain alongside 15.4% token reduction across six
  benchmarks"; "MATH500 performance: Shows 3.5-point improvements with 24.7% token
  savings on simpler problems." Also a striking direct-fetch quote: "Incorrect
  responses contain twice as many thinking tokens as correct ones, suggesting
  thinking tokens often indicate reasoning failure rather than success" — i.e., in
  this paper's data, LONGER thinking traces CORRELATE WITH BEING WRONG, not right.
  This is a second independent primary source (alongside §1.6, Inverse Scaling in
  Test-Time Compute) suggesting that more reasoning tokens is not a reliable proxy
  for "more correct," at least on the task types these two papers studied (not
  logic-grid puzzles specifically, but general reasoning/math tasks).

### 3.4 "Thinking with Reasoning Skills: Fewer Tokens, More Accuracy"

- Paper URL: https://arxiv.org/abs/2604.21764 (fetched via
  https://ar5iv.labs.arxiv.org/html/2604.21764). Authors: Guangxiang Zhao, Qilong
  Shi, Xusen Xiao, Xiangzheng Zhang, Tong Yang, Lin Sun (Qiyuan Tech, Tsinghua
  University, University of Hong Kong, Peking University). Confirmed via direct
  fetch.
- Quote (verbatim, abstract): "We propose to summarize and store reusable reasoning
  skills distilled from extensive deliberation and trial-and-error exploration, and
  to retrieve these skills at inference time to guide future reasoning... we find
  that it significantly reduces reasoning tokens while improving overall
  performance."
- Numbers from direct fetch: on math benchmarks, "17.5% cost reduction" with "0.7%"
  accuracy improvement (Gemini-3-Flash); for GPT-4o-mini on math tasks, "1.8 accuracy
  points" gained with reduced cost; on the hardest instances specifically, "token
  consumption dropped from approximately 15,000 to 7,000 tokens while maintaining
  superior accuracy compared to forced-brevity baselines like TALE or Chain-of-Draft."
  Note this paper evaluates coding and math tasks, not logic-grid puzzles, but is
  further corroborating evidence (a third independent paper, alongside §3.2 and
  §3.3) that reduced-token reasoning strategies can match or beat full-length
  thinking on reasoning-adjacent tasks.

---

## 4. Gemma-4-31B and MiniMax-M3/M2 specific data

### 4.1 Gemma-4-31B-it — thinking mode default state and benchmark scores

- Primary source: Hugging Face model card, directly fetched twice —
  https://huggingface.co/google/gemma-4-31B-it
- Quote (verbatim, from the "Best Practices"/trigger section): "Thinking is enabled
  by including the `<|think|>` token at the start of the system prompt. To disable
  thinking, remove the token." Also (paraphrase from the same fetch): for models
  other than the smaller E2B/E4B variants (this includes the 31B model), disabling
  thinking still emits empty thought-tag scaffolding: `<|channel>thought\n<channel|>`
  before the final answer.
- Benchmark numbers reported on the same card (direct fetch): AIME 2026 (no tools):
  89.2%; MMLU Pro: 85.2%; GPQA Diamond: 84.3%; LiveCodeBench v6: 80.0%; BigBench
  Extra Hard: 74.4%. Also stated on the card: Gemma 3 (predecessor) scored only
  20.8% on AIME 2026, illustrating the generational jump attributed to Gemma 4's
  thinking-capable architecture.
- **Critical gap**: I could NOT confirm, from the directly-fetched model card itself,
  whether these benchmark numbers were measured with thinking mode ON or OFF. Two
  separate direct fetches of the same page specifically hunting for this footnote
  both came back empty: "The document does **not specify** whether the reported
  benchmark results were measured with thinking mode enabled or disabled... contains
  no notation, footnotes, or headers indicating the thinking mode state during
  evaluation." A WebSearch synopsis (of a secondary blog, not the primary card —
  **UNVERIFIED**) asserted "The official results from Google's Model Card cover
  instruction-tuned models with thinking enabled," and separately that "Gemma 4
  [is] able to produce 4,000+ tokens of reasoning before committing to an answer" —
  but since this could not be confirmed against the primary card text itself, I flag
  it as UNVERIFIED and note the primary source is genuinely ambiguous on this point.
  I attempted to cross-check via Artificial Analysis
  (https://artificialanalysis.ai/models/gemma-4-31b) and a Medium benchmark writeup,
  but both fetches failed due to the fetch tool's domain-safety check being unable to
  verify those domains during this session (not a confirmed-blocked/paywalled result,
  just a tool-side failure — worth retrying in a future session).
- Corroborating independent source for the 74.4% BBEH figure: a WebSearch synopsis
  (of llm-stats.com/benchmarks/big-bench-extra-hard, not directly fetched — that
  domain's WebFetch was refused by the tool's domain-safety check — **UNVERIFIED as
  primary, but a second independent number matching the HF card**) stated "Gemma 4
  31B from Google currently leads the BIG-Bench Extra Hard leaderboard with a score
  of 0.744 across 11 evaluated AI models."
- No ZebraLogic, knights-and-knaves, or seating/ordering-puzzle-specific score for
  Gemma-4-31B-it was found anywhere in this research pass, verified or unverified.
  Direct WebSearch queries combining "gemma-4-31b" with ZebraLogic / constraint
  satisfaction / logic puzzle returned no matching results — the model does not
  appear to have been evaluated on that specific benchmark by any source indexed by
  search at the time of this research.

### 4.2 MiniMax-M3 — thinking toggle mechanics and benchmark data

- Fireworks blog (directly fetched): https://fireworks.ai/blog/minimax-m3-launch —
  quote (paraphrase of directly-fetched content): "To enable reasoning capabilities
  via the Fireworks API, add `"thinking": {"type": "enabled"}` to your request
  payload." Also directly quoted: "both modes sharing the same pricing. Enable
  thinking for complex reasoning and agentic tasks; disable it for lower-latency
  scenarios like chat and code completion" and "Thinking mode...and regular
  inference mode sharing the same pricing," meaning no PER-TOKEN price premium for
  enabling reasoning on Fireworks specifically (this does not mean zero extra
  TOKENS — thinking mode still generates additional reasoning tokens that are billed
  at the same per-token rate, just not a higher rate).
- MiniMax official platform docs (directly fetched):
  https://platform.minimax.io/docs/guides/text-m3-function-call — confirms
  "Interleaved Thinking" mechanics: "Anthropic SDK: Thinking is enabled by default...
  the `content` field contains `<think>` tags which will be automatically
  preserved." For the OpenAI-compatible SDK path, thinking is controlled via
  `extra_body={"reasoning_split": True/False}`, but this only changes WHERE the
  thinking content is returned (separate `reasoning_details` field vs inline
  `<think>` tags), not whether thinking happens at all — no documented way to fully
  disable thinking was found in this specific doc page (contrast with the Fireworks
  blog's `"thinking": {"type": "enabled"}` framing, which implies a corresponding
  "disabled" option exists at the Fireworks layer specifically — consistent with
  what an earlier AMDA research file, research/routing_cascade_research.md /
  VERDICTS.md, already recorded from a kilocode GitHub issue: the M3/M2 API "accepts
  `"thinking": {"type": "disabled"}`" — not independently re-verified in this
  session, cross-referenced from prior research only).
- Artificial Analysis (directly fetched): https://artificialanalysis.ai/models/minimax-m3
  — "MiniMax-M3 achieved a composite score of 44 on the Artificial Analysis
  Intelligence Index, ranking #2 out of 93 models in its class." Token usage: "When
  evaluated on the Intelligence Index, MiniMax-M3 'generated 89M output tokens, which
  is better than average compared to other open weight models of similar size
  (median: 92M).'" No thinking-on-vs-off ablation was present on this page, and no
  logic-puzzle-specific or ZebraLogic score was found for M3 on this page.
- BridgeBench (found via WebSearch synopsis only; a direct WebFetch of
  https://www.bridgebench.ai/reasoning/minimax-m3 returned an error and could not be
  retried successfully in this session — **UNVERIFIED**): "MiniMax M3 achieved 40.4%
  overall on BridgeBench's reasoning benchmark." No further breakdown obtained.
- MiniMax-M2 technical report (one generation behind M3, but the closest thing to a
  primary academic paper found for this model family): https://arxiv.org/pdf/2605.26494
  ("The MiniMax-M2 Series: Mini Activations Unleashing Max Real-World Intelligence").
  Directly fetched (PDF). The fetch explicitly could NOT find, in the visible
  extracted sections: (a) any thinking-mode-on vs off accuracy ablation, (b) any
  token cost/length comparison between thinking modes, (c) any BIG-Bench Hard,
  ZebraLogic, or logic-puzzle-specific score. The paper's own summary states it
  covers "general architecture and performance across standard benchmarks (MATH,
  MMLU, HumanEval, etc.)" per the fetch tool's read, none of which are the
  constraint-satisfaction logic-puzzle category AMDA cares about.
- No data point (verified or unverified) was found anywhere in this research pass
  that reports MiniMax-M2 or M3 accuracy specifically on zebra/seating/knights-and-
  knaves/river-crossing-style puzzles, with or without thinking enabled.

---

## 5. Gaps / things NOT found in this research pass

Recorded explicitly per instructions (collect-only, so noting absence of evidence is
itself useful to the later analysis session):

- No source was found giving a clean, same-model, same-puzzle-type "thinking ON
  accuracy X% vs thinking OFF accuracy Y%, at token cost Z" triple specifically for
  zebra/seating/knights-and-knaves/river-crossing puzzles. The closest same-family
  pair with a directly-fetched primary number (Qwen3-30B-A3B Instruct-2507 vs
  Thinking-2507, §1.4) had a ZebraLogic score for the non-thinking variant (90.0) but
  no ZebraLogic score at all published for the thinking variant.
- No data at all (verified or not) was found for Gemma-4-31B or MiniMax-M2/M3 on
  ZebraLogic, knights-and-knaves, seating/ordering puzzles, or river-crossing
  puzzles specifically — the two models named in the task brief's point 4 simply do
  not appear to have public benchmark numbers on this exact task family.
  BIG-Bench-Extra-Hard (which does include a "Zebra Puzzles" sub-task) has a Gemma-4-
  31B AGGREGATE score (74.4%) but not a Zebra-Puzzles-only sub-score for that model
  in anything I could fetch.
- The heyneo.com Reasoning Token Efficiency Leaderboard (§2.4) is the one source
  found whose task taxonomy exactly matches AMDA's logic-puzzle list (knights and
  knaves, muddy children, hat puzzles, river crossings) AND separately reports
  reasoning-token counts, but its category-level (as opposed to all-category-
  aggregate) breakdown could not be retrieved in this session — only the combined
  20-task numbers were fetchable.
- s1's budget-forcing sweep (§3.1) is real and directly on-topic for the "does a
  short trace get most of the gain cheaply" question, but the intermediate points on
  the accuracy-vs-token curve were only available as an unreadable figure, not a
  table, in what was fetchable this session — only the two endpoints (no
  intervention baseline ~50% vs full budget-forced ~57% on AIME24) were confirmed
  in text.
