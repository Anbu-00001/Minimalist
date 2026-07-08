# Open-Source Quality/Verification Tools — Round 2 Research Log

Purpose: COLLECT-ONLY continuation of prior research (`research/free_apis_opensource_tools.md`). This pass specifically targets hallucination-detection libraries, small local judge/verifier models, published cascade cost-savings numbers, structured-output/entity-extraction correctness checkers, and llama.cpp-specific confidence signals — items NOT already covered by the prior pass (which already found and the project already decided on: RouteLLM, outlines, guidance, DSPy, GBNF grammars, math-verify).

No recommendations, no synthesis, no code, no other repo files touched. Every bullet is either a direct quote (quotation marks) or a clearly marked paraphrase, with source URL. Anything only seen via a search snippet (not a direct WebFetch) is marked UNVERIFIED.

Research date: 2026-07-08.

---

## Section 1: Hallucination-detection / answer-verification libraries (not full LLM-judge calls)

### 1.1 UQLM (cvs-health/uqlm) — HIGH RELEVANCE

- Real repo, directly fetched: https://github.com/cvs-health/uqlm (2026-07-08).
- Direct quote: "UQLM is a Python library for Large Language Model (LLM) hallucination detection using state-of-the-art uncertainty quantification techniques."
- Install: `pip install uqlm` (from PyPI, per fetch).
- Four scorer categories, per fetch:
  1. **Black-Box Scorers** (paraphrase): "assess uncertainty by measuring the consistency of multiple responses generated from the same prompt" — work with any LLM, "without requiring access to internal model states." (No judge LLM call needed — this is the category most relevant to a deterministic-verifier use case.)
  2. **White-Box Scorers** (paraphrase): "leverage token probabilities to estimate uncertainty" — requires access to the LLM's internal/logprob output (i.e., usable with a local llama.cpp model that exposes logprobs).
  3. **LLM-as-a-Judge Scorers** (paraphrase): "use one or more LLMs to evaluate the reliability of the original LLM's response" — this is the category AMDA explicitly wants to avoid as the primary mechanism.
  4. **Ensemble and Long-Text Scorers**: combinations/claim-level variants of the above.
- Local/open model support confirmed via fetch: "the documentation shows examples using `ChatOllama` for local models like Llama and Mistral, and supports any 'LangChain Chat Model'" (paraphrase) — implies llama.cpp-served local models would work if exposed via an OpenAI/Ollama-compatible LangChain wrapper.
- Not yet independently verified: exact black-box scorer algorithm names (e.g. self-consistency, NLI-based) — the fetch summarized rather than quoted the full scorer list. TODO follow-up if implementation detail needed.

### 1.2 SelfCheckGPT (potsawee/selfcheckgpt) — HIGH RELEVANCE

- Real repo, directly fetched README: https://github.com/potsawee/selfcheckgpt/blob/main/README.md (2026-07-08). Also on PyPI: `pip install selfcheckgpt` (per fetch).
- Underlying paper: "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models" — https://arxiv.org/abs/2303.08896
- Five variants, per fetch (paraphrase per variant, with deterministic/LLM-call status noted):
  - **SelfCheckBERTScore** — "Uses semantic similarity scoring based on BERT embeddings to compare sentences against sampled passages. This is lightweight and doesn't require LLM calls."
  - **SelfCheckMQAG** (Multiple-choice QA Generation) — generates questions from sentences, answers them against sampled passages, scores consistency; "does involve an underlying model but operates deterministically once instantiated."
  - **SelfCheckNgram** — "Calculates negative log probability scores using n-gram matching... fully deterministic and lightweight, operating at both sentence and document levels without external LLM calls."
  - **SelfCheckNLI** (marked "Recommended" per fetch) — "Uses DeBERTa-v3-large fine-tuned on Multi-NLI to assess entailment/contradiction... doesn't require querying an external LLM."
  - **SelfCheckLLMPrompt** — "Prompts an LLM to assess whether sentences are supported by contexts. Requires calling external models (Mistral, Llama2, or OpenAI APIs), making it the most computationally expensive variant." (This is the one variant that IS an LLM-judge call — the other four are not.)
- Verbatim usage example from fetch:
  ```python
  from selfcheckgpt.modeling_selfcheck import SelfCheckNLI
  selfcheck_nli = SelfCheckNLI(device=device)
  sent_scores_nli = selfcheck_nli.predict(
      sentences=sentences,
      sampled_passages=[sample1, sample2, sample3]
  )
  ```
- Core mechanism, paraphrase from search synthesis (not independently re-quoted from the README fetch, treat as secondary corroboration): "if an LLM has knowledge of a given concept, sampled responses are likely to be similar and contain consistent facts; for hallucinated facts, stochastically sampled responses are likely to diverge and contradict one another." This requires generating multiple samples of the SAME answer (temperature-sampled reruns) as its input — a cost/latency tradeoff to note (multiple local generations, still zero paid-API cost, but more local compute per verified answer).

### 1.3 LettuceDetect (KRLabsOrg/LettuceDetect) — HIGH RELEVANCE, also answers Q2 (small model)

- Real repo, directly fetched README and TINYLETTUCE.md: https://github.com/KRLabsOrg/LettuceDetect (2026-07-08).
- Direct quote (paraphrase of stated purpose): "a lightweight and efficient tool for detecting hallucinations in Retrieval-Augmented Generation (RAG) systems. It identifies unsupported parts of an answer by comparing it to the provided context." (Token-level span detection, not a single yes/no score.)
- License: "MIT License" (direct quote from fetch).
- Install: `pip install lettucedetect -U` (direct quote from fetch), or `pip install -e .` from source.
- Verbatim usage example from README fetch:
  ```python
  from lettucedetect.models.inference import HallucinationDetector
  detector = HallucinationDetector(
      method="transformer",
      model_path="KRLabsOrg/lettucedect-base-modernbert-en-v1",
  )
  predictions = detector.predict(context=contexts, question=question, answer=answer, output_format="spans")
  ```
- Benchmark claim, direct quote from README fetch: "Up to **17 F1 points improvement** over baseline LLM judges like GPT-4.1-mini across different languages." Also (paraphrase): for code-agent tasks, a fine-tuned 2B detector "substantially outperforms the off-the-shelf detectors and large LLM judges tested" (exact numbers not given in the fetched excerpt).
- Base model sizes per fetch: "210M" and "610M" parameter EuroBERT-based variants (`lettucedect-base-modernbert-en-v1` / `lettucedect-large-...`).
- **TinyLettuce sub-family (docs/TINYLETTUCE.md, directly fetched) — smallest verifier models found in this whole research pass:**
  - Direct quote: "TinyLettuce‑17M (17M parameters)" plus "Ettin-32M" (32M) and "Ettin-68M" (68M parameter) siblings.
  - Purpose per fetch: "Generate synthetic training data for hallucination detection and training tiny Ettin encoders on it."
  - Benchmark, direct quote: "TinyLettuce‑17M reaches 90.87% F1" on synthetic test data, "outperforming GPT‑5‑mini (83.69%), GPT‑OSS‑120B (83.38%), and Qwen3‑235B (79.84%)." (Self-reported by the project; not independently re-verified against a third party.)
  - License, direct quote: "All models and code are MIT licensed and ready for production deployment."
  - Verbatim usage:
    ```python
    from lettucedetect.models.inference import HallucinationDetector
    detector = HallucinationDetector(
        method="transformer",
        model_path="KRLabsOrg/tinylettuce-ettin-17m-en-v1"
    )
    spans = detector.predict(
        context=["Your context here"],
        question="Your question",
        answer="Your answer",
        output_format="spans"
    )
    ```
  - Note per fetch: "Models are available via Hugging Face and run efficiently on CPU hardware." — at 17M-68M params this is trivially small enough to fit alongside a local llama.cpp model in a 10GB Docker image budget.
  - Caveat: this model family is designed for RAG-style "is the answer supported by the given context passage" checking, not general open-domain factual correctness without a source document — relevant if AMDA's task categories include any retrieval/context-grounded tasks, less directly applicable to e.g. pure math/code tasks.

### 1.4 Vectara HHEM-2.1-Open — also answers Q2

- Real model, directly fetched HF model card: https://huggingface.co/vectara/hallucination_evaluation_model (2026-07-08).
- Direct quote, parameter count: "0.1B params" (~100M parameters).
- Direct quote, license: "apache-2.0"
- Verbatim usage code from fetch:
  ```python
  from transformers import AutoModelForSequenceClassification

  pairs = [
      ("The capital of France is Berlin.", "The capital of France is Paris."),
  ]

  model = AutoModelForSequenceClassification.from_pretrained(
      'vectara/hallucination_evaluation_model', trust_remote_code=True)

  model.predict(pairs)
  ```
- Mechanism, paraphrase from fetch: takes (premise, hypothesis) pairs and "returns a score between 0 and 1" where "0 means that the hypothesis is not evidenced at all by the premise and 1 means the hypothesis is fully supported by the premise." Same premise/hypothesis-entailment design as SelfCheckNLI (1.2) — checks an answer against a *given* source text, not open-domain fact-checking.
- Efficiency claim, UNVERIFIED (from search snippet, not the fetched model card directly): "HHEM-2.1-Open can be run on consumer-grade hardware, occupying less than 600MB RAM space at 32-bit precision and elapsing around 1.5 second for a 2k-token input on a modern x86 CPU." Source: search-synthesis of https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model and related pages, not independently re-fetched.
- Related repo (title/URL only, not fetched): leaderboard comparing many LLMs' hallucination rates on summarization — https://github.com/vectara/hallucination-leaderboard

---

## Section 2: Small/quantized judge or reward models usable as a free local verifier (<~2B params)

(Cross-reference: TinyLettuce-17M/32M/68M and HHEM-2.1-Open (~100M) from Section 1 are themselves squarely in this category — smallest found overall. Additional dedicated "judge"/"reward" models below.)

### 2.1 Flow-Judge-v0.1 (flowaicom/flow-judge) — 3.8B, borderline over the ~2B target but closest full general-purpose "judge" model found

- Real repo, surfaced by search and cross-corroborated via search synthesis of the README (not independently WebFetched raw in this session — treat body text below as paraphrase, URLs are real): https://github.com/flowaicom/flow-judge
- Paraphrase: "Flow-Judge-v0.1 is an open-source, lightweight (3.8B) language model optimized for LLM system evaluations," architecture based on Phi-3.5-mini, from Flow AI (Aug 2024).
- Paraphrase: comes with "pre-defined metrics such as RESPONSE_CORRECTNESS or RESPONSE_FAITHFULNESS," supports "Hugging Face Transformers and vLLM" backends. No llama.cpp-native backend confirmed this session — UNVERIFIED whether it runs via GGUF.
- License, per search synthesis: "Apache 2.0."
- Also available quantized: https://huggingface.co/flowaicom/Flow-Judge-v0.1-AWQ (real URL, not fetched — AWQ quantization, not GGUF).
- Note: at 3.8B params this exceeds the user's stated "<~2B" target but is included because it's the most-cited dedicated small open "judge" model family found; the RAG-hallucination-specific models in Section 1.3/1.4 are smaller and better fit the size constraint.

### 2.2 Atla Selene Mini (AtlaAI/Selene-1-Mini-Llama-3.1-8B) — 8B, over target, noted for completeness

- Real model, search-corroborated (not independently WebFetched): https://hf.co/AtlaAI/Selene-1-Mini-Llama-3.1-8B, also on Ollama: https://ollama.com/atla/selene-mini
- Paraphrase: "a state-of-the-art small language model-as-a-judge (SLMJ)... fine-tuned from Llama-3.1-8B using a loss strategy combining direct preference optimization (DPO) and supervised fine-tuning (SFT)," reported as "the highest-scoring 8B generative model on RewardBench, surpassing strong baselines like GPT-4o and specialized judges." Paper: https://arxiv.org/abs/2501.17195 ("Atla Selene Mini: A General Purpose Evaluation Model").
- At 8B params this is too large for the user's stated <2B / 10GB-image-budget constraint alongside an existing local model — noted only as a data point that "Mini" branding in this space still means 8B, not <2B.

### 2.3 Glider (PatronusAI) — Phi-3.5-mini-based, ~3.8B, also over target

- Search-corroborated, not independently fetched. Paraphrase: "Glider is a fine-tuned version of Microsoft Phi-3.5 Mini" (PatronusAI, Dec 2024); comparison claim (paraphrase, UNVERIFIED/third-party synthesis): "Glider and Selene consistently outperform both FlowJudge and Phimini 3.5 across most evaluation datasets, though Glider and Selene require over 15 GiB of cache, more than double the ~7.2 GiB used by FlowJudge and Phimini." No direct repo URL captured this session — TODO follow-up (`patronus-ai` GitHub org) if needed.

### 2.4 TinyRM family — 400M+, process/preference reward models

- From search synthesis of an arXiv paper "Tiny Reward Models" (https://arxiv.org/pdf/2507.09973), UNVERIFIED/not independently fetched: "The TinyRM family includes models as small as 400 million parameters and achieves competitive performance with models over 175 times larger on Reasoning and Safety preference modeling tasks." No confirmed GitHub/HF repo link captured this session for TinyRM specifically — TODO follow-up if this needs to be pinned down further; only the arXiv paper URL is confirmed real.

### 2.5 Small process-reward-model repos (math/reasoning step verification), lower confidence

- **Awesome-Process-Reward-Models** (curated list, real repo, not fetched in full): https://github.com/RyanLiu112/Awesome-Process-Reward-Models
- **RLHFlow/RLHF-Reward-Modeling** (real repo, not fetched): https://github.com/RLHFlow/RLHF-Reward-Modeling — paraphrase from search: "Recipes to train reward model for RLHF."
- **allenai/reward-bench** (real repo, not fetched): https://github.com/allenai/reward-bench — "the first evaluation tool for reward models" (paraphrase), useful if AMDA ever wants to benchmark candidate small judge models against each other rather than a specific model itself.
- Paraphrase from search synthesis (source ambiguous among several arXiv results, UNVERIFIED aggregate): "Process reward models have been trained with Llama-3.2-1B-Instruct, where best-of-4 accuracy outperforms Top-1 accuracy by 4% on GSM8K" — Llama-3.2-1B-Instruct itself is a real, well-known open model under 2B params and a plausible PRM backbone size, but no single confirmed off-the-shelf "1B PRM checkpoint" repo/URL was captured this session for that specific claim — flag as UNVERIFIED / needs a follow-up fetch to find the exact checkpoint if this path is pursued later.

---

## Section 3: Open-source repos implementing "local-first, deterministic-verify, escalate-on-failure" with PUBLISHED cost numbers

Two small, independent (low-profile, not widely-known/starred — treat as individual-hobbyist-scale projects rather than established frameworks) GitHub repos were found that match this exact architecture description very closely, with self-reported numbers. Both directly fetched.

### 3.1 askalf/hybrid — closest architectural match found in this entire research pass

- Real repo, directly fetched: https://github.com/askalf/hybrid (2026-07-08).
- Repo tagline, direct quote: "Local-first LLM router: answer the easy majority on a small local model, escalate only the hard queries to any OpenAI-compatible frontier endpoint. ~160 lines, stdlib-only."
- **Verification is deterministic, not an LLM judge**, per fetch, using layered tiers:
  - "Solver tier": closed-form arithmetic, exact unit conversions, percentage-change via Python `Fraction` math.
  - "Template tier": "Five rigid word-problem shapes parsed deterministically and solved exactly."
  - "Category rules": escalate known-weak domains (code, proofs, puzzles) outright.
  - "Setup re-derivation": "Model transcribes equations; system solves linear systems exactly via Gaussian elimination over `Fraction`s — escalates if the model contradicts its own transcription."
  - "Verify tier": "Model answers and plugs numbers back into problem relationships; re-derives checks exactly — escalates if any check fails."
  - "Self-consistency": "Answer multiple times concurrently; escalate on disagreement."
- Direct quote (design note on a fundamental limit of exact-oracle verification, worth noting as a design lesson): "the derive tier's lesson, inverted. The model's real job on a word problem is transcription, and transcription is the one surface the exact oracle cannot check."
- **Published numbers (self-reported, from the README)**:
  - Benchmark set (22 labeled queries, local model `qwen2.5:7b`): "17/22 (77%) answered without a frontier call."
  - Separate holdout test (24 queries): "22/24 on-box (92%)" with "11/24 answered in 0 ms."
  - Dollar-cost framing, direct quote: "~52% of frontier spend avoided (not 75%)" — note the repo's own README explicitly flags the difference between the query-count-kept-local percentage (77-92%) and the dollar-cost-avoided percentage (52%), because harder escalated queries cost disproportionately more in tokens.
  - Per-1000-query economics, direct quote: "~$2.86 all-frontier → ~$1.37 hybrid."
  - Safety/accuracy claim, direct quote: "17/17 on-box answers correct (ZERO wrong answers served)" in the benchmark set.
- Local model used: `qwen2.5:7b` default (per fetch); optional `llama3.2:3b` "for vote/creative tiers only."
- Self-reported caveats/limitations (direct quotes): "The oracle solves the system the model transcribes; it cannot check the transcription against the problem" (a wrong-but-internally-consistent transcription can pass); "only linear systems are in reach" (nonlinear/set-logic problems fall through to escalation); "Capacity honesty: on a CPU box the model tiers run seconds-to-a-minute per query and effectively serially"; and one documented failure — "one wrong-served answer is the documented transcription-leak trap" found on the holdout set.
- Relevance note: this is a very close conceptual match to AMDA's own architecture (deterministic re-derivation/exact-check verifiers gating escalation, not an LLM judge) and is the one repo found this session that publishes a "percent kept local" number (77-92%) directly comparable in kind to AMDA's own measured 46%-kept-local figure, plus a distinct dollar-cost-avoided percentage (52%) showing the two metrics diverge.

### 3.2 NadirRouter/NadirClaw

- Real repo, directly fetched: https://github.com/NadirRouter/NadirClaw (2026-07-08).
- Repo tagline, direct quote: "Open-source LLM router & AI cost optimizer. Routes simple prompts to cheap/local models, complex ones to premium — automatically. Drop-in OpenAI-compatible proxy for Claude Code, Codex, Cursor, OpenClaw. Saves 40-70% on AI API costs. Self-hosted, no middleman."
- Verification mechanism, direct quote: default is a "rule-based heuristic verifier (refusals, truncation, JSON-format failures, ~1ms)" — explicitly deterministic/heuristic, not an LLM call. An optional trained "DeBERTa-v3-small cross-encoder" is available via a `nadirclaw[trained]` extra but is described as secondary.
- **Published cost-savings numbers (self-reported)**:
  - Direct quote: "40–70% lower" costs, overall range.
  - Claude Code case study, direct quote/paraphrase: "57% reduction ($24.18 → $10.29)."
  - OpenClaw agent scenario: "62% reduction ($31.45 → $11.92)."
  - "Context Optimize" feature: "61.5% input token reduction on structured payloads" (benchmarked on Claude Opus 4.6 only, per fetch — generalization to other models not claimed).
  - Tiered presets, direct quote: "Conservative setup: 38% savings; Balanced: 52% savings; Aggressive: 65% savings."
- Local model support: confirmed Ollama, e.g. direct quote: `NADIRCLAW_SIMPLE_MODEL=ollama/llama3.1:8b`, with example models `llama3.1:8b`, `qwen3:32b`, `deepseek-r1:14b` shown in docs. **llama.cpp itself is not specifically named** in the fetched material — only Ollama is shown as the local-inference path.
- Benchmark provenance, per fetch: cites "RouterBench: held-out, n=11,420" and "RouterArena: sub_10, n=809, public leaderboard" as benchmark sources, and separately flags that "real-world claims ('typical 8-hour coding day') are anecdotal session logs, not longitudinal studies."

### 3.3 Cross-reference note

Both 3.1 and 3.2 are small/low-profile individual repos (not corroborated star counts or independent third-party validation found this session) — their numbers are self-reported in their own READMEs and were not cross-checked against any independent benchmark or paper in this session. Flagged accordingly; a later analysis pass may want to check repo star/fork counts and commit history before treating these as credible comparison points.

---

## Section 4: Structured-output / JSON-schema / entity-extraction correctness checkers (beyond json.loads)

### 4.1 Instructor (instructor-ai/instructor)

- Real repo, directly fetched: https://github.com/instructor-ai/instructor (2026-07-08).
- Direct quote: "Get reliable JSON from any LLM. Built on Pydantic for validation, type safety, and IDE support."
- Install: `pip install instructor` (direct quote).
- Retry mechanism, paraphrase from fetch: validates extracted data against Pydantic models; "Failed validations are automatically retried with the error message" — the LLM is fed back the validation error and asked to correct its output, up to a retry limit. (This is a validate-then-retry-with-the-*same*-model loop, not an escalate-to-a-different-model loop — worth distinguishing from AMDA's verify-then-escalate pattern.)
- Local model support confirmed, direct quote: "Ollama (local)" listed as a supported provider, with example syntax `instructor.from_provider("ollama/llama3.2")`.
- Popularity claim, UNVERIFIED (from search-snippet synthesis, not the direct fetch): "the most popular option at 11K+ GitHub stars and 3M+ monthly downloads." Source: search aggregator, not independently confirmed via a stars-count fetch this session.

### 4.2 Guardrails AI (guardrails-ai/guardrails)

- Real repo, directly fetched README: https://github.com/guardrails-ai/guardrails (2026-07-08).
- Direct quote: "Guardrails is a Python framework that helps build reliable AI applications by performing two key functions: 1. Guardrails runs Input/Output Guards in your application that detect, quantify and mitigate the presence of specific types of risks. 2. Guardrails help you generate structured data from LLMs."
- Install: `pip install guardrails-ai` (direct quote).
- Validators are pulled from a separate "Guardrails Hub" rather than being bundled a-la-carte in the base package, per fetch: "a collection of pre-built measures of specific types of risks (called 'validators')," installed individually, e.g. `hub://guardrails/regex_match`, `hub://guardrails/competitor_check`, `hub://guardrails/toxic_language` (all direct-quoted install identifiers from the fetch).
- Mixed deterministic/LLM-dependent, per fetch (paraphrase): base validators like regex-match and competitor-check are deterministic; but "for structured data generation, it uses either function calling or prompt optimization depending on LLM capabilities — both requiring LLM calls" for the generation side (the *validation* of already-produced structured data can still be deterministic/regex-based even if generation assistance uses the LLM).
- Related PII/entity-extraction validator, from search synthesis (not independently fetched this session): "the GuardrailsPII validator uses Presidio and GLiNER to detect and anonymize PII in the generated text, with a combination of Presidio and GLiNER yielding the highest performing results." Repo: https://github.com/guardrails-ai/guardrails_pii (real URL, not fetched).

### 4.3 GLiNER (urchade/GLiNER) — deterministic, local, zero-LLM-call entity-extraction correctness tool

- Real repo, directly fetched: https://github.com/urchade/GLiNER (2026-07-08).
- Direct quote: "Zero-shot NER | Relation Extraction | PII Detection | Information Extraction | Token Classification."
- License: "Apache-2.0" (direct quote from fetch).
- Install: `pip install gliner` (direct quote).
- Verbatim usage example from fetch:
  ```python
  from gliner import GLiNER
  model = GLiNER.from_pretrained("gliner-community/gliner_small-v2.5")
  entities = model.predict_entities(text, labels, threshold=0.5)
  ```
- Local execution confirmed, paraphrase from fetch: "Runs Anywhere," "optimized to run on CPUs and consumer hardware," no external LLM API call required; "supports quantization and compilation optimizations for edge deployment."
- Size variants referenced in the repo (per fetch, exact param counts not given in the fetched excerpt): small/medium/large tiers, e.g. `gliner_small-v2.5`. TODO follow-up: fetch a specific model card (e.g. `gliner-community/gliner_small-v2.5` on HF) for exact parameter count if precision is needed later.
- Relevance: if AMDA has any task category that extracts named entities/structured spans, GLiNER is a real, small, deterministic-at-inference-time (no sampling randomness in the same sense as an LLM) local model that could cross-check an LLM's claimed extracted entities against independently-extracted ones — a genuinely different mechanism from json.loads/schema-shape validation, since it validates semantic content correctness, not just structural conformance.

### 4.4 Other structured-output libraries surfaced (list-level, from imaurer/awesome-llm-json), not independently fetched — included for completeness since they were surfaced fresh in this pass and are not on the excluded list

- Source list: https://github.com/imaurer/awesome-llm-json (real repo, surfaced by search, not independently WebFetched this session — items below are paraphrased from search-engine synthesis of that list, URLs are real/checkable):
  - **Formatron** (MIT) — paraphrase: "an efficient and scalable constrained decoding library that enables controlling over language model output format using f-string templates that support regular expressions, context-free grammars, JSON schemas, and Pydantic models... integrates seamlessly with various model inference libraries." (Real project name, not independently verified beyond this search synthesis this session.)
  - **Transformers-cfg** (MIT) — paraphrase: "extends Hugging Face Transformers with context-free grammar (CFG) support via an EBNF interface... enables grammar-constrained generation with minimal changes to existing code of transformers and supports JSON mode and JSON Schema."
  - **jsonformer** (1rgs/jsonformer) — real repo surfaced directly by search title: "A Bulletproof Way to Generate Structured JSON from Language Models," https://github.com/1rgs/jsonformer (title only, not fetched in full).
  - Note: none of these four were independently WebFetched this session; treat as UNVERIFIED pending direct README fetch if adopted for consideration later.

---

## Section 5: llama.cpp-specific tooling for cheap local confidence/verification signals (beyond GBNF grammars)

### 5.1 `/completion` endpoint logprobs / n_probs (llama-server) — directly confirmed

- Directly fetched: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md (2026-07-08).
- Direct quote: `n_probs`: "If greater than 0, the response also contains the probabilities of top N tokens for each generated token given the sampling settings."
- Response structure per fetch: a `probs`/`completion_probabilities` array per generated token, each containing `id`, `logprob` (float), `token`, `bytes`, and a nested `top_logprobs` array of alternative-token probabilities.
- `post_sampling_probs`, direct quote: "Returns the probabilities of top `n_probs` tokens after applying sampling chain." When enabled, `logprob` is replaced with `prob` (0.0–1.0 range) and `top_logprobs` becomes `top_probs`.
- Per fetch, recent versions made `logprobs` OpenAI-compatible, defaulting to pre-sampling probs (paraphrase, not a direct quote from the fetched excerpt but stated as a summarized fact from the same fetch).
- **This is a genuinely usable, already-exposed, zero-extra-dependency confidence signal**: a caller can request `n_probs` on a llama-server `/completion` call and compute e.g. mean/min token logprob of the generated answer as a cheap self-confidence proxy, without any extra model or library — directly answers Q5's core ask. No dedicated "confidence" or "self-assessment" endpoint name exists (confirmed absent per fetch: "No dedicated perplexity computation endpoint exists... No separate perplexity tool is mentioned" for `/completion`/`/embedding`), so this would need to be computed manually from the raw per-token logprobs returned.

### 5.2 `llama-perplexity` tool — corpus-level, NOT single-answer self-assessment

- Directly fetched: https://github.com/ggml-org/llama.cpp/tree/master/tools/perplexity (2026-07-08).
- Direct quote: "The `perplexity` example can be used to calculate the so-called perplexity value of a language model over a given text corpus. Perplexity measures how well the model can predict the next token with lower values being better."
- Important finding: per fetch, this tool "is not designed for scoring individual generated responses. It operates on text corpora (datasets), with the Wikitext-2 test set being the standard benchmark among contributors... perplexity as a model-wide evaluation metric, not a mechanism for self-assessing single outputs" (paraphrase of the fetched page's framing). Advanced flags mentioned in the fetch: `--kl-divergence-base path/to/logit/binary/file.kld` and `--kl-divergence` for KL-divergence statistics between two models' output distributions.
- Older/legacy usage pattern found in a 2023-era GitHub Discussion (https://github.com/ggml-org/llama.cpp/discussions/406, directly fetched): `./main --perplexity -m models/7B/ggml-model-q4_0.bin -t 10 -f wikitext-2-raw/wiki.test.raw` — this predates the current `llama-perplexity` binary naming/tool split but shows the same underlying corpus-perplexity concept has existed since early llama.cpp.
- Conclusion relevant to Q5: `llama-perplexity` is NOT directly usable as a per-answer confidence signal out of the box (it's a batch/corpus evaluation tool) — the `/completion` endpoint's `n_probs`/`logprob` fields (5.1) are the more directly applicable signal for scoring a single generated answer's confidence.

### 5.3 Mirostat sampling (`--mirostat`, `--mirostat-ent`, `--mirostat-lr`) — entropy-target sampler, generation-time not post-hoc

- From search synthesis (multiple corroborating snippets, not independently WebFetched from the primary llama.cpp server/completion README this session — treat as UNVERIFIED-exact-wording though the parameter names themselves are well-established/real):
  - "`--mirostat-ent` sets the Mirostat target entropy (tau), which represents the desired perplexity value for the generated text... default value is 5.0."
  - "`--mirostat`: Enable Mirostat sampling, controlling perplexity during text generation (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mirostat 2.0)."
  - "`--mirostat-lr`: the Mirostat learning rate, parameter eta (default: 0.1)."
  - Example usage found: `--mirostat 2 --mirostat-lr 0.05 --mirostat-ent 3.0`
  - Paraphrase of algorithm intent: "Mirostat is an algorithm that actively maintains the quality of generated text within a desired range during text generation... avoiding low-quality output caused by excessive repetition (boredom traps) or incoherence (confusion traps)."
- Relevance caveat: Mirostat is a *generation-time* sampler that targets a fixed entropy during decoding (i.e., it changes HOW the answer is generated to stay within a perplexity band) — it does not itself emit a post-hoc confidence score for a finished answer the way `n_probs`/logprobs (5.1) can. Noted here since it is llama.cpp-specific and entropy/confidence-adjacent, but it answers a different question (controlling generation quality) than Q5 (scoring already-generated answer confidence).

### 5.4 "Adaptive-P" / confidence-adaptive samplers — found via search only, UNVERIFIED

- From search synthesis only, not fetched from any primary llama.cpp doc or PR this session — treat entirely as UNVERIFIED, and the exact repo/PR implementing it was not captured:
  - "Adaptive-P is a stateful, dynamic alternative to standard Top-P sampling that continuously shifts the probability threshold based on how confident the model has been over the last few tokens."
  - "The adaptive-p sampler tracks the actual probability of tokens the model selects and uses an Exponential Moving Average to maintain a 'running state' of the model's confidence. When the probability distribution flattens (indicating uncertainty), the sampler widens the threshold..."
  - TODO follow-up: confirm whether "Adaptive-P" is an actual merged llama.cpp sampler (in `common/sampling.cpp` or similar) or a third-party/proposed-only concept — not established either way this session.

---

## Sources (raw list, this session only)

### Directly fetched via WebFetch
- https://github.com/cvs-health/uqlm
- https://huggingface.co/vectara/hallucination_evaluation_model
- https://github.com/ggml-org/llama.cpp/discussions/406
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/stanford-futuredata/FrugalGPT
- https://arxiv.org/abs/2305.05176
- https://github.com/potsawee/selfcheckgpt/blob/main/README.md
- https://github.com/askalf/hybrid
- https://github.com/NadirRouter/NadirClaw
- https://github.com/KRLabsOrg/LettuceDetect/blob/main/docs/TINYLETTUCE.md
- https://github.com/KRLabsOrg/LettuceDetect/blob/main/README.md
- https://github.com/guardrails-ai/guardrails
- https://github.com/ggml-org/llama.cpp/tree/master/tools/perplexity
- https://github.com/instructor-ai/instructor
- https://github.com/urchade/GLiNER

### Surfaced via WebSearch and cited (snippet/title level; not independently WebFetched this session unless noted above)
- https://github.com/ThaTechMaestro/hallucination-detection
- https://github.com/Mattbusel/LLM-Hallucination-Detection-Script
- https://github.com/topics/hallucination-detection
- https://github.com/julienbrasseur/llm-hallucination-detector
- https://github.com/topics/llm-hallucination
- https://github.com/topics/hallucination
- https://github.com/EdinburghNLP/awesome-hallucination-detection
- https://arxiv.org/html/2510.07545v1 (ChartJudge-2B)
- https://arxiv.org/pdf/2502.04313
- https://arxiv.org/pdf/2605.02915
- https://github.com/vectara/hallucination-leaderboard
- https://www.vectara.com/blog/introducing-the-next-generation-of-vectaras-hallucination-leaderboard
- https://www.vectara.com/blog/hallucination-detection-commercial-vs-open-source-a-deep-dive
- https://www.vectara.com/blog/hhem-2-1-a-better-hallucination-detection-model
- https://www.vectara.com/blog/cut-the-bull-detecting-hallucinations-in-large-language-models
- https://arxiv.org/html/2501.17195v1 (Atla Selene Mini)
- https://galtea.ai/blog/exploring-state-of-the-art-llms-as-judges
- https://www.atla-ai.com/post/selene-1-mini
- https://github.com/benchflow-ai/awesome-evals
- https://huggingface.co/blog/AtlaAI/selene-1-mini
- https://ollama.com/atla/selene-mini
- https://arxiv.org/abs/2501.17195
- https://huggingface.co/AtlaAI/Selene-1-Mini-Llama-3.1-8B
- https://github.com/flowaicom/flow-judge
- https://github.com/flowaicom/flow-judge/blob/main/README.md
- https://flow-ai.com/blog/flow-judge
- https://flow-ai.com/judge
- https://huggingface.co/flowaicom/Flow-Judge-v0.1-AWQ
- https://github.com/RyanLiu112/Awesome-Process-Reward-Models
- https://arxiv.org/pdf/2403.13787
- https://github.com/allenai/reward-bench
- https://github.com/RLHFlow/RLHF-Reward-Modeling
- https://arxiv.org/pdf/2507.09973 (Tiny Reward Models)
- https://arxiv.org/html/2502.10325v1
- https://github.com/sanjibanc/agent_prm (via search synthesis)
- https://arxiv.org/pdf/2412.11006
- https://github.com/askalf/hybrid (also fetched, listed above)
- https://github.com/nandth/model-router-ai
- https://github.com/openclaw/openclaw/issues/10969
- https://github.com/topics/model-routing?l=python&o=desc&s=forks
- https://github.com/ypollak2/llm-router/blob/main/ROADMAP.md
- https://github.com/anyscale/llm-router
- https://arxiv.org/html/2605.06350
- https://arxiv.org/html/2606.27457
- https://tianpan.co/blog/2025-11-03-llm-routing-model-cascades
- https://arxiv.org/html/2511.07396 (C3PO)
- https://openreview.net/pdf?id=e4IlBqhbTO
- https://arxiv.org/pdf/2604.19781
- https://arxiv.org/pdf/2506.11887
- https://lingjiaochen.com/papers/2024_FrugalGPT_TMLR.pdf
- https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/
- https://dev.to/portkey/frugalgpt-reducing-llm-costs-improving-performance-2797
- https://aithority.com/ait-featured-posts/cheap-and-fast-the-strategy-of-llm-cascading-frugal-gpt/
- https://github.com/stanford-futuredata/FrugalGPT/blob/main/intro.ipynb
- https://huggingface.co/papers/2305.05176
- https://nexos.ai/blog/frugal-gpt/
- https://github.com/ai-in-pm/SelfCheckGPT
- https://www.alphaxiv.org/resources/2303.08896v3
- https://github.com/mruderman/selfcheckgpt-SELF-FACT-CHECKING
- https://pypi.org/project/selfcheckgpt/
- https://arxiv.org/pdf/2401.08358
- https://arxiv.org/abs/2303.08896
- https://arxiv.org/pdf/2303.08896
- https://huggingface.co/blog/adaamko/lettucedetect
- https://medium.com/@bogdanandreig/lettucedetect-a-lightweight-framework-for-catching-ai-hallucinations-d6fbe127609d
- https://github.com/nagatharun/LettuceDetect-for-Hallucination-in-AI-Agents.
- https://towardsdatascience.com/lettucedetect-a-hallucination-detection-framework-for-rag-applications/
- https://arxiv.org/pdf/2605.02504
- https://huggingface.co/KRLabsOrg/lettucedect-large-modernbert-en-v1/blob/afdd20e26c7f26690e3adfe6dd19073e095cb825/README.md
- https://github.com/guardrails-ai/guardrails_pii
- https://learnbybuilding.ai/tutorial/structured-data-extraction-with-guardrails-and-llms/
- https://github.com/guardrails-ai/guardrails-internal
- https://guardrailsai.com/guardrails/docs/concepts/validators
- https://openai.github.io/openai-guardrails-python/
- https://guardrailsai.com/docs/concepts/validators
- https://www.guardrailsai.com/docs/how_to_guides/hosting_validator_models
- https://guardrailsai.com/hub
- https://www.guardrailsai.com/docs/how_to_guides/generate_structured_data
- https://deepwiki.com/ggml-org/llama.cpp/3.8-adapters-and-fine-tuning
- https://arxiv.org/pdf/2311.09731
- https://arxiv.org/pdf/2509.23234
- https://blog.alexewerlof.com/p/sampling-args-in-llama-server
- https://llama-cpp.com/
- https://github.com/ggml-org/llama.cpp/blob/master/tools/completion/README.md
- https://smcleod.net/2025/04/llm-sampling-parameters-guide/
- https://manpages.debian.org/testing/llama.cpp-tools-extra/llama-perplexity.1.en.html
- https://github.com/oobabooga/textgen/wiki/03-%E2%80%90-Parameters-Tab
- https://github.com/byroneverson/llm.cpp/blob/master/examples/main/README.md
- https://arxiv.org/pdf/2509.02510
- https://github.com/abetlen/llama-cpp-python/issues/312
- https://github.com/abetlen/llama-cpp-python/pull/329
- https://arxiv.org/pdf/2411.00759
- https://arxiv.org/pdf/2510.13940
- https://github.com/imaurer/awesome-llm-json
- https://github.com/imaurer/awesome-llm-json/blob/main/README.md
- https://awesome.ecosyste.ms/projects/github.com%2Fimaurer%2Fawesome-llm-json
- https://toolerific.ai/ai-tools/opensource/imaurer-awesome-llm-json
- https://awesome.ecosyste.ms/lists/imaurer/awesome-llm-json
- https://jeffjjohnston.github.io/2025/05/19/llm-structured-output/
- https://github.com/otriscon/llm-structured-output
- https://github.com/1rgs/jsonformer
- https://github.com/vishvaRam/Structured-Output-Examples-for-LLMs
- https://techsy.io/en/blog/best-llm-structured-output-libraries
- https://medium.com/@octave.dumont/dont-trust-the-llm-alone-making-zero-shot-ner-work-under-domain-shift-097669939737
- https://github.com/yaminivibha/LLM_InformationRetrieval
- https://arxiv.org/pdf/2511.14998
- https://github.com/topics/llm-extraction?o=desc&s=forks
- https://arxiv.org/pdf/2410.14748
- https://github.com/daviden1013/llm-ie
- https://www.medrxiv.org/content/10.64898/2026.01.19.26344287.full.pdf
- https://pypi.org/project/uqlm/ (implied by fetch, not independently visited)
- https://tianpan.co/blog/2025-11-03-llm-routing-model-cascades

**End of log.** Research date 2026-07-08. Raw collection only — no synthesis, no recommendation, no integration code, no other repo files modified. Items explicitly marked UNVERIFIED where only search-snippet (not primary-source WebFetch) evidence was available. The strongest new findings for AMDA's specific questions, at a glance (still not a recommendation, just an index of what's above): smallest local verifier models = TinyLettuce-17M (Section 1.3) and HHEM-2.1-Open ~100M (Section 1.4); non-LLM-judge hallucination-consistency library = SelfCheckGPT's four non-LLM variants (Section 1.2) and UQLM's black-box/white-box scorers (Section 1.1); closest architectural/numeric comparison points for the verify-then-escalate cascade = askalf/hybrid and NadirRouter/NadirClaw (Section 3, both self-reported, low-profile repos); llama.cpp-native confidence signal = `/completion` endpoint's `n_probs`/`logprob` fields (Section 5.1), with `llama-perplexity` confirmed NOT applicable to single-answer scoring (Section 5.2).
