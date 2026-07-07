# Research Log: Constrained Decoding & Deterministic LLM Output Verification

Collected for AMDA (AMD Developer Hackathon Act II, Track 1). COLLECT-ONLY log — bullets are
findings with source URL and verbatim quote or explicitly-marked paraphrase. No synthesis,
no recommendations included below by design.

---

## 1. Constrained / guided decoding libraries

### Outlines (dottxt-ai/outlines)
- URL: https://github.com/dottxt-ai/outlines — Repo description per search snippet: "Outlines is a Python library that allows you to use Large Language Model in a simple and robust way (with structured generation)." (paraphrase of search-result summary)
- URL: https://github.com/dottxt-ai/outlines — WebFetch verbatim: "Structured outputs for LLMs" that work by "guaranteeing output validity during generation rather than parsing afterwards."
- URL: https://github.com/dottxt-ai/outlines — WebFetch verbatim quote: "Most solutions attempt to fix bad outputs after generation using parsing, regex, or fragile code that breaks easily. Outlines guarantees structured outputs during generation — directly from any LLM."
- URL: https://github.com/dottxt-ai/outlines — WebFetch verbatim: "Guaranteed valid structure - No more parsing headaches or broken JSON"
- URL: https://github.com/dottxt-ai/outlines — Supported backends per WebFetch: "Local models: transformers and llama.cpp; Servers: vLLM and Ollama; APIs: OpenAI, Gemini, and Dottxt"
- URL: https://dottxt-ai.github.io/outlines/reference/generation/structured_generation_explanation/ — "How does it work?" reference page exists explaining the generation mechanism (found via search, not fetched in full).
- URL: https://dottxt-ai.github.io/outlines/cookbook/ — Cookbook of structured-generation recipes (found via search listing).
- Paraphrase from search summary: "Outlines can guide models so that they output valid JSON 100% of the time" — regex-based generation, choice selection from predefined options, and JSON schema validation using Pydantic models are supported.
- Underlying paper: URL: https://arxiv.org/abs/2307.09702 — "Efficient Guided Generation for Large Language Models" by Brandon T. Willard and Rémi Louf (July 2023). Paraphrase: shows text generation can be reformulated as transitions between states of a finite-state machine, enabling an index over the LM's vocabulary for guiding generation with regex/CFGs "with almost no overhead compared to generation without any constraints." Implementation released as the open-source Outlines library.

### Guidance (Microsoft / guidance-ai)
- URL: https://github.com/guidance-ai/guidance — Paraphrase: "A guidance language for controlling large language models" — proven open-source Python library where developers express in Python the precise programmatic constraints the model must follow for structured output in JSON, Python, HTML, SQL, etc.
- URL: https://github.com/guidance-ai/guidance — Paraphrase: "constrained generation uses regular expressions and context-free grammars to guide the model's output"; "Guidance enforces constraints by steering the model token by token in the inference layer."
- URL: https://guidance-ai.github.io/llguidance/llg-go-brrr — Paraphrase (from search snippet): "Guidance steers the model token by token in the inference stack, reducing cost and latency by 30-50%." (numeric claim — UNVERIFIED, not independently confirmed by fetching the page directly)
- URL: https://github.com/guidance-ai/llguidance — Description: "Super-fast Structured Outputs." Paraphrase: implements constrained decoding (constrained sampling / structured outputs) for LLMs, can "enforce arbitrary context-free grammar on the output of LLM," performance "on the order of 50μs of CPU time per token" with "negligible startup costs."
- URL: https://news.ycombinator.com/item?id=45345207 — "Sampling and structured outputs in LLMs" HN thread. Paraphrase of discussion: guidance = "a user-friendly library that connects to lots of OSS model serving backends," llguidance = "a core Rust library written for high performance mask computation."

### lm-format-enforcer
- URL: https://github.com/noamgat/lm-format-enforcer — Paraphrase: "Enforce the output format (JSON Schema, Regex etc) of a language model." Solves format issues "by filtering the tokens that the language model is allowed to generate at every timestep, thus ensuring that the output format is respected, while minimizing the limitations on the language model."
- URL: https://github.com/noamgat/lm-format-enforcer — Paraphrase: Two main parsers: `JsonSchemaParser` (JSON Schemas) and `RegexParser` (regular expressions). "Gives the language model freedom to control whitespacing and field ordering in JSON schemas, reducing hallucinations."
- URL: https://github.com/noamgat/lm-format-enforcer — Paraphrase: integrated into vLLM's OpenAI-compatible server; recent versions added union-type support and a "schemaless JSON mode" (`JsonSchemaParser(None)`) that accepts any valid JSON.
- URL: https://haystack.deepset.ai/integrations/lmformatenforcer — Haystack integration page exists for LM Format Enforcer (found via search, confirms ecosystem integration).
- URL: https://github.com/noamgat/lm-format-enforcer/blob/main/samples/colab_llamacpppython_integration.ipynb — Sample notebook showing llama-cpp-python integration (found via search listing; not fetched).

### GBNF grammars in llama.cpp (see also Section 2 below for depth)
- URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — WebFetch verbatim/paraphrase: production rules follow `nonterminal ::= sequence...`; non-terminals must be "a dashed lowercase word, like `move`, `castle`, or `check-mate`."
- URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — Terminals include literal strings (`"1"`) or character ranges (`[1-9]`); negated ranges use `^`, e.g. `[^\n]+ "\n"` matches any character except newlines.
- URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — Repetition operators: `*` (zero or more), `+` (one or more), `?` (optional), `{m}` (exactly m), `{m,n}` (between m and n).
- URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — CLI usage example: `./llama-cli -m <model> --grammar-file grammars/some-grammar.gbnf -p 'Some prompt'`
- URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — JSON-schema-to-grammar conversion: the `-j` flag converts JSON schemas to GBNF; quote: "`additionalProperties` defaults to `false` (produces faster grammars + reduces hallucinations)." Also notes: remote `$ref`s are unsupported in the C++ implementation, and `pattern`s must start with `^` and end with `$`.
- URL: https://github.com/ggml-org/llama.cpp/blob/master/examples/json_schema_to_grammar.py — Script referenced by search results that converts a JSON schema into a working GBNF grammar.

### OpenAI Structured Outputs / JSON mode
- URL: https://developers.openai.com/api/docs/guides/structured-outputs — Paraphrase: "Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema, so you don't need to worry about the model omitting a required key, or hallucinating an invalid enum value." When `response_format` is supplied with `strict: true`, "model outputs will match the supplied schema."
- URL: https://developers.openai.com/api/docs/guides/structured-outputs — Distinction: "While both ensure valid JSON, only Structured Outputs ensure schema adherence. While JSON mode improves model reliability for generating valid JSON outputs, it does not guarantee that the model's response will conform to a particular schema."
- URL: https://developers.openai.com/api/docs/guides/structured-outputs — Reliability claim: "With Structured Outputs, gpt-4o-2024-08-06 achieves 100% reliability in our evals, perfectly matching the output schemas."
- URL: https://developers.openai.com/api/docs/guides/structured-outputs — Caveat: refusals bypass the schema guarantee — "Since a refusal does not follow the schema you have supplied in response_format, the API has a new field `refusal` to indicate when the model refused to answer." Also, a `finish_reason` other than a clean stop (e.g., truncation) means the schema guarantee does not hold.
- URL: https://openai.com/index/introducing-structured-outputs-in-the-api/ — Original announcement post (found via search, not separately fetched).

### Fireworks AI structured outputs
- URL: https://docs.fireworks.ai/structured-responses/structured-response-formatting — Paraphrase: Fireworks supports two methods — "JSON mode (using JSON schemas) and Grammar mode (using custom BNF grammars)."
- URL: https://docs.fireworks.ai/structured-responses/structured-response-formatting — Paraphrase: "Fireworks is taking the schema you provide and forcing the model to decode according to its structure. For each step of the autoregressive decoding, only new tokens that would be considered valid in the provided schema are allowed."
- URL: https://fireworks.ai/docs/structured-responses/structured-output-grammar-based — Paraphrase: "Grammar mode lets you describe the desired context-free grammar in an extended BNF form... Sometimes JSON is not what you need (e.g. it may be finicky with string escaping) and you need some other structured output." "In a full grammar, the root rule always defines the starting point of the grammar."
- URL: https://fireworks.ai/blog/why-do-all-LLMs-need-structured-output-modes — Blog post arguing structured output modes are a necessary LLM feature (found via search, title/thesis only).
- URL: https://fireworks.ai/blog/constrained-generation-with-reasoning — "From text to task: Constrained generation for structured extraction in R1" — post about combining constrained generation with a reasoning model (title + topic only, not fetched in full).
- Paraphrase from search summary (UNVERIFIED precision of numbers, attributed to Fireworks' own benchmark claims): "In Fireworks' benchmarks, their JSON mode provided 120 tokens/sec while the average 'JSON mode' from competing platforms generated 30 tokens/sec."

### XGrammar
- URL: https://github.com/mlc-ai/xgrammar — Paraphrase: "open-source library for efficient, flexible, and portable structured generation... leverages constrained decoding to ensure 100% structural correctness of the output and supports general context-free grammar to enable a broad range of structures, including JSON, regex, custom context-free grammar, etc."
- URL: https://github.com/mlc-ai/xgrammar — Paraphrase: technical approach — "accelerates context-free grammar execution by dividing the vocabulary into context-independent tokens that can be prechecked and context-dependent tokens that need to be interpreted during runtime."
- URL: https://blog.mlc.ai/2026/05/04/xgrammar-2-fast-customizable-structured-generation — Paraphrase: "XGrammar-2 delivers up to 80x efficiency gain compared to XGrammar, and achieves near-zero overhead in LLM serving scenarios." (numeric claim from vendor blog — treat as vendor-reported, UNVERIFIED independently)
- URL: https://arxiv.org/abs/2411.15100 — "XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models" paper.
- URL: https://blog.mlc.ai/2024/11/22/achieving-efficient-flexible-portable-structured-generation-with-xgrammar — Original XGrammar announcement (found via search).
- Paraphrase: XGrammar integrated into SGLang, vLLM, TensorRT-LLM, and MLC-LLM "for strict tool calling."

### vLLM guided/structured decoding (server integration point relevant to multiple libraries above)
- URL: https://docs.vllm.ai/en/latest/features/structured_outputs/ — Paraphrase: "vLLM supports the generation of structured outputs using outlines, lm-format-enforcer, or xgrammar as backends for the guided decoding." Parameters: `guided_choice`, `guided_regex`, `guided_json`, `guided_grammar`.
- URL: https://docs.vllm.ai/en/latest/features/structured_outputs/ — Paraphrase: "vLLM now supports both outlines and XGrammar backends for structured decoding. In cases where XGrammar is insufficient to serve the request, vLLM falls back to Outlines."
- URL: https://www.bentoml.com/blog/structured-decoding-in-vllm-a-gentle-introduction — "Structured Decoding in vLLM: A Gentle Introduction" — paraphrase: "the xgrammar backend offers low time per output token... performs best when grammars are reused, thanks to effective caching," while "the guidance backend excels at fast time to first token, even with complex grammars."
- URL: https://vllm.ai/blog/struct-decode-intro — Official vLLM blog version of the same gentle-introduction piece (found via search).
- URL: https://blog.squeezebits.com/guided-decoding-performance-vllm-sglang — "Guided Decoding Performance on vLLM and SGLang" comparative benchmark post (title/topic found via search, not fetched in full).
- URL: https://developers.redhat.com/articles/2025/06/03/structured-outputs-vllm-guiding-ai-responses — Red Hat developer article on structured outputs in vLLM (found via search).

### Instructor (Pydantic-based validation + reask, adjacent technique)
- URL: https://python.useinstructor.com/ — Paraphrase: "Instructor is a Python library that extracts structured, validated data from Large Language Models (LLMs). It uses Pydantic models to define output schemas and automatically handles validation, retries, and error handling." Works with "OpenAI's GPT models, Anthropic's Claude, Google's Gemini, open source models with Ollama, DeepSeek, and 15+ supported providers."
- URL: https://python.useinstructor.com/concepts/reask_validation/ — Paraphrase: "Instructor wraps your LLM client and enforces Pydantic schema validation on the output, with automatic retry on failure. If validation fails, it automatically retries with the error message included, so the model can fix it." Configurable via `max_retries`.
- URL: https://github.com/567-labs/instructor — Repo: "structured outputs for llms."
- URL: https://python.useinstructor.com/concepts/validation/ — Paraphrase: supports both standard Pydantic validators (code-based) and `llm_validator` (LLM-based validation for things "hard to express programmatically, such as content moderation, tone validation, consistency checks"). NOTE: this reask/LLM-validator path is a *post-hoc* check + re-prompt approach, distinct from pre-generation constrained decoding.
- URL: https://machinelearningmastery.com/the-complete-guide-to-using-pydantic-for-validating-llm-outputs/ — "The Complete Guide to Using Pydantic for Validating LLM Outputs" (found via search).
- URL: https://xebia.com/blog/enforce-and-validate-llm-output-with-pydantic/ — "Enforce And Validate LLM Output With Pydantic" (found via search).
- URL: https://pydantic.dev/articles/llm-intro — "How to Use Pydantic for LLMs: Schema, Validation & Prompts" (found via search).

---

## 2. Grammar-constrained generation in llama.cpp specifically (GBNF)

- URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — Official grammars README (see full syntax details in Section 1 above — production rules, terminals, ranges, repetition operators, `--grammar-file` flag, `-j` JSON-schema-to-grammar conversion, `additionalProperties` default-false note).
- URL: https://mintlify.com/ggml-org/llama.cpp/advanced/grammars — Mirror/rendering of the grammars doc (found via search).
- URL: https://deepwiki.com/ggml-org/llama.cpp/8.1-grammar-and-structured-output — DeepWiki page specifically on "Grammar and Structured Output" for llama.cpp (found via search, not fetched in full).
- URL: https://deepwiki.com/abetlen/llama-cpp-python/6.1-grammar-based-generation — DeepWiki page on grammar-based generation for the llama-cpp-python bindings (found via search).
- URL: https://node-llama-cpp.withcat.ai/guide/grammar (also mirrored at https://withcatai.github.io/node-llama-cpp/guide/grammar) — "Using Grammar" guide for the Node.js llama.cpp bindings (found via search).
- URL: https://til.simonwillison.net/llms/llama-cpp-python-grammars — Simon Willison TIL: "Using llama-cpp-python grammars to generate JSON." Paraphrase from search snippet: demonstrates using a grammar to force valid JSON output via llama-cpp-python.
- URL: https://www.imaurer.com/blog/posts/2023-09-06-llama-cpp-grammars/ — Ian Maurer blog, WebFetch verbatim quotes:
  - "With grammars, I get 100% well-formed JSON responses and the accuracy of the extracted data has improved by approximately 25%."
  - Before grammars: "about 15-20% malformed JSON responses which would require either falling back to a more expensive model or complex parsing logic."
  - Example grammar rule for classification labels: `entity_type ::= "\"drug\"" | "\"variant\"" | "\"biomarker\"" | "\"finding\""` — constrains the model to output only one of four predefined biomedical categories.
  - Analogy quote: constrained generation works "from the beginning of the generation process," like "guardrails in bowling which not only prevents gutter balls (i.e. not well-formed JSON) but also increases the likelihood of a strike (i.e. the correct answer)."
  - Paraphrase: the constrained approach eliminated retry logic and improved reliability beyond mere formatting compliance.
- URL: https://replicate.com/blog/llama-2-grammars — "Jet-setting with Llama 2 + Grammars" — Replicate blog. Paraphrase from search summary: shows using grammars to constrain output to a JSON document matching a given JSON Schema for flight-information extraction tasks.
- URL: https://llama-cpp-agent.readthedocs.io/en/latest/grammar-api-reference/ — "Grammar Generator" API reference for the llama-cpp-agent project (found via search).
- Paraphrase (from search summary, attributing to "Intrinsic Labs"): a "Grammar Builder" tool can generate GBNF grammars from TypeScript type declarations (source not independently fetched — UNVERIFIED which org/repo exactly).
- URL: https://github.com/ggml-org/llama.cpp/discussions/15341 — "gpt-oss and grammar" discussion thread (found via search, topic only — grammar support/limitations discussion for a specific model family).

---

## 3. Self-verification / self-checking patterns and LLM-judge reliability critiques

### Chain-of-Verification (CoVe)
- URL: https://arxiv.org/abs/2309.11495 — "Chain-of-Verification Reduces Hallucination in Large Language Models" (Dhuliawala et al., Sept 2023). Paraphrase: method has the model (i) draft an initial response, (ii) plan verification questions to fact-check its own draft, (iii) answer those questions independently "so the answers are not biased by other responses," then (iv) generate a final verified response. Result: "CoVe decreases hallucinations across a variety of tasks, from list-based questions from Wikidata, closed book MultiSpanQA and longform text generation."
- URL: https://learnprompting.org/docs/advanced/self_criticism/chain_of_verification — Explainer/tutorial page on CoVe (found via search).
- URL: https://arxiv.org/pdf/2309.11495 — PDF version of the same paper.

### LLMs cannot reliably self-correct reasoning
- URL: https://arxiv.org/abs/2310.01798 — "Large Language Models Cannot Self-Correct Reasoning Yet" (Huang, Chen, Mishra, Zheng, Yu, Song, Zhou; ICLR 2024). Paraphrase: examines "intrinsic self-correction," where an LLM attempts to correct its own initial responses "based solely on its inherent capabilities, without external feedback." Finding: "LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades after self-correction."
- URL: https://openreview.net/forum?id=IkmD3fKBPQ — OpenReview page for the same paper (found via search).
- URL: https://arxiv.org/pdf/2310.01798 — PDF version.

### Self-Refine (adjacent iterative self-feedback technique, with caveats)
- URL: https://arxiv.org/abs/2303.17651 — "Self-Refine: Iterative Refinement with Self-Feedback." Paraphrase (from search-result synthesis of secondary sources, not primary abstract fetch): base models need "sufficient few-shot modeling or instruction-following abilities to learn to provide feedback and refine in an in-context fashion."
- URL: https://learnprompting.org/docs/advanced/self_criticism/self_refine — Explainer of Self-Refine and its limitations (found via search). Paraphrase: limitations include reliance on accurate self-critique ("poor feedback halts improvement"), "overfitting or oscillation in ambiguous prompt domains," and the need for domain-specific prompt tuning.
- Paraphrase (secondary-source synthesis, UNVERIFIED against primary paper text): "generated follow-up questions are not always perfect or precise, answers can be off-point, and final refinement of responses can be too excessive."

### Self-consistency / majority voting (verification via multiple samples, not free)
- URL: https://learnprompting.org/docs/intermediate/self_consistency — "Self-Consistency Prompting" explainer. Paraphrase: sample multiple reasoning paths (e.g., via temperature sampling), each producing a final answer; aggregate via majority vote; "the correct answer is more likely to be the one that appears most frequently across diverse reasoning attempts."
- URL: https://calmops.com/algorithms/self-consistency-reasoning/ — "Self-Consistency in LLM Reasoning: Ensemble Methods for Reliable Outputs" (found via search).
- Paraphrase (general knowledge confirmed via search summary): original self-consistency method improved accuracy on GSM8K by aggregating multiple chain-of-thought paths via majority vote; trade-off is "substantial computational overhead" from sampling and aggregating multiple trajectories — i.e., NOT a free verification technique, cost scales with number of samples.

### LLM-as-judge reliability critiques
- URL: https://arxiv.org/html/2604.16790v1 (also PDF at https://arxiv.org/pdf/2604.16790) — "Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering" (April 2026). Paraphrase: "repeated evaluations of the same case can disagree, small prompt edits can swing outcomes, and seemingly semantics-preserving perturbations may elicit divergent verdicts." Probes prompt-induced biases: "position, verbosity, authority/provenance, distraction, chain-of-thought, self-enhancement, and refined-version cues."
- URL: https://openreview.net/forum?id=3GTtZFiajM — "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge." Paraphrase: identifies "12 key potential biases" and proposes a framework called CALM to "systematically quantify and analyze each type of bias in LLM-as-a-Judge."
- URL: https://www.arxiv.org/pdf/2509.26072 — "The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge." Paraphrase: argues "a faithful judge should be invariant to who authored a response and when it was written," but shows "current LLM judges fail this test and their rationales often fail to surface the shortcuts driving their decisions."
- URL: https://arxiv.org/pdf/2411.16594 — "From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge." Paraphrase: documents that "LLM judges tend to prefer longer, authoritative-looking, and well-formatted responses," and exhibit "egocentric bias and preference leakage from their own knowledge."
- URL: https://arxiv.org/pdf/2603.00539 — "Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement" (found via search, title/topic only — code-review-specific judge reliability).
- URL: https://arxiv.org/pdf/2604.18164 — "MM-JudgeBias: A Benchmark for Evaluating Compositional Biases in MLLM-as-a-Judge" (found via search, title/topic only).
- URL: https://arxiv.org/pdf/2604.23178 — "Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines" (found via search, title/topic only).
- URL: https://galileo.ai/blog/llm-as-a-judge-vs-human-evaluation — "LLM-as-a-Judge vs Human Evaluation" (found via search, not fetched in full).

---

## 4. Code-execution-based verification (sandboxed execution)

### E2B
- URL: https://e2b.dev/docs — Official E2B documentation homepage.
- URL: https://e2b.dev/blog/e2b-sandbox — "Code Interpreter Sandbox" E2B blog post (found via search).
- URL: https://e2b.dev/blog/build-ai-data-analyst-with-sandboxed-code-execution-using-typescript-and-gpt-4o — "Build AI data analyst with sandboxed code execution using TS, and GPT-4o" (found via search, title/topic only).
- Paraphrase (from search-result synthesis, secondary sources describing E2B, not E2B's own copy verified verbatim): "E2B is an open-source infrastructure platform for running AI-generated code in secure, isolated sandboxes... E2B's sandboxes are built on Firecracker micro-VMs... boot in under 200ms, support full Linux environments... Each sandbox is ephemeral and fully isolated — malicious or buggy code cannot escape the microVM boundary."
- URL: https://northflank.com/blog/best-alternatives-to-e2b-dev-for-running-untrusted-code-in-secure-sandboxes — Paraphrase: "The only way to run LLM-generated code with truly robust security isolation is to use remote execution options like E2B or Docker... LLMs frequently generate code... executing this code introduces risk: it might be malicious, buggy, or resource-intensive... might accidentally (or intentionally) read sensitive files, access the network, or overwrite system state."
- URL: https://northflank.com/blog/e2b-vs-modal — "E2B vs Modal: comparing AI code execution sandboxes in 2026" (found via search, comparative topic only, not fetched in full).
- URL: https://www.beam.cloud/blog/best-e2b-alternatives — "Open-Source Alternatives to E2B for Sandboxed Code Execution" (found via search).
- URL: https://huggingface.co/docs/smolagents/en/tutorials/secure_code_execution — Hugging Face smolagents "Secure code execution" docs (found via search — relevant since smolagents runs LLM-generated Python for agent tool calls).

### OpenAI Code Interpreter architecture
- URL: https://developers.openai.com/api/docs/guides/tools-code-interpreter — Official OpenAI docs. Paraphrase: "A container is a fully sandboxed virtual machine that the model can run Python code in" — Code Interpreter tool lets models "write and run Python code in a sandboxed environment."
- URL: https://developers.openai.com/api/docs/guides/tools-code-interpreter — Paraphrase: "Auto mode automatically creates a new container or reuses an active container," with configurable memory limits "defaulting to 1 GB if not specified."
- URL: https://ryan.govost.es/2025/openai-code-interpreter/ — "The OpenAI Code Interpreter" by Ryan Govostes — described in search summary as "the most detailed technical writeup," based on observed interactions with Code Interpreter (not independently fetched in full).
- Paraphrase (from search-result synthesis, sourced to the Govostes writeup per the search engine's summary): "OpenAI uses gVisor, a container runtime that provides additional isolation for higher-risk tasks... the Code Interpreter's 'user machine' environment runs on top of gVisor, which provides significant isolation from the host cluster node." Container launched with an entrypoint running a Python web server on port 8080 hosting a `user_machine` FastAPI app, with endpoints like `/check_liveness` (Kubernetes health checks) and `/upload`/`/download` for file transfer.
- URL: https://itnext.io/openais-code-execution-runtime-replicating-sandboxing-infrastructure-a2574e22dc3c — "OpenAI's Code Execution Runtime & Replicating Sandboxing Infrastructure" by Dogukan Tuna, ITNEXT (found via search, not fetched in full).
- URL: https://developers.openai.com/codex/concepts/sandboxing — "Sandbox – Codex" official OpenAI Codex docs on sandboxing concepts (found via search).
- URL: https://medium.com/@Shrishml/making-our-own-code-interpreter-part-1-making-of-a-sandbox-382da3339eaa — "Making our own code interpreter: making of a sandbox" (found via search, not fetched in full).
- URL: https://community.openai.com/t/code-interpreter-sandbox/543222 — OpenAI developer community forum thread discussing the Code Interpreter sandbox (found via search, not fetched).

### Subprocess isolation, timeouts, resource limits (Python-specific patterns)
- URL: https://til.simonwillison.net/python/subprocess-time-limit — Simon Willison TIL, "Running Python code in a subprocess with a time limit" (found via search).
- URL: https://healeycodes.com/running-untrusted-python-code — Andrew Healey, "Running Untrusted Python Code" (found via search).
- URL: https://github.com/openedx/codejail — "codejail" — Open edX's secure code execution library (found via search; relevant prior art for sandboxing student/LLM-submitted Python).
- URL: https://dida.do/blog/setting-up-a-secure-python-sandbox-for-llm-agents — "Setting Up a Secure Python Sandbox for LLM Agents" (found via search).
- URL: https://inference.sh/blog/tools/sandboxed-execution — "Sandboxed Code Execution for AI Agents" (found via search).
- Paraphrase (from search-result synthesis of the above pages, general technique description, not a single verbatim quote): use `asyncio.wait_for()` with a timeout when running subprocesses, catch the timeout exception, then terminate the process; wall-clock timeouts are described as "the most important limit, with execution thresholds commonly set to 5-30 seconds for interactive use or minutes for batch jobs."
- Paraphrase: the `preexec_fn` argument to `subprocess.Popen` is "the correct place to apply resource limits, as it executes in the child process context after fork but before exec," using the `setrlimit` syscall with options such as `RLIMIT_CPU` (CPU time), `RLIMIT_AS` (virtual memory size), `RLIMIT_FSIZE` (max file size).
- Paraphrase: "Never directly use Python's `exec()` or `eval()` on unsanitized code, as these functions execute code within the same process with no isolation... subprocess alone does not constitute a full sandbox." Container-based sandboxes (Docker) offer "moderate startup overhead and solid isolation," while microVM approaches (Firecracker) "sacrifice startup speed for hardware-level isolation."
- Paraphrase (caveat re: cleanup): "When `TimeoutExpired` is raised, termination isn't always guaranteed to clean up everything instantly, especially if the process has child processes still running and consuming resources."

### gVisor / seccomp (isolation mechanism underlying several of the above)
- URL: https://gvisor.dev/docs/architecture_guide/intro/ — Official gVisor architecture intro docs.
- Paraphrase: "gVisor is an open-source application kernel that intercepts system calls and handles them in user space, acting as a security boundary between containers and the host kernel instead of containers talking directly to the host kernel." Default "Systrap" platform "is based on Linux's seccomp-bpf subsystem for system call interception."
- URL: https://northflank.com/blog/how-to-sandbox-ai-agents — "How to sandbox AI agents in 2026: MicroVMs, gVisor & isolation strategies" (found via search).
- Paraphrase: "gVisor provides syscall-level isolation, which is stronger than standard containers but weaker than VMs. The trade-off is performance, as every syscall goes through user-space interception with overhead most felt on I/O-heavy workloads, though usually fine for short-lived code execution like scripts."
- URL: https://www.shayon.dev/post/2026/52/lets-discuss-sandbox-isolation/ — "Let's discuss sandbox isolation" (found via search, not fetched in full).
- URL: https://arxiv.org/pdf/2504.00018 — "SandboxEval: Towards Securing Test Environment for Untrusted Code" (found via search, academic paper on sandbox security testing).

---

## 5. Format-compliance / instruction-following benchmarks

### IFEval
- URL: https://arxiv.org/abs/2311.07911 — "Instruction-Following Evaluation for Large Language Models." WebFetch/paraphrase: "One core capability of Large Language Models (LLMs) is to follow natural language instructions. However, the evaluation of such abilities is not standardized." Introduces "verifiable instructions" — objective, machine-checkable criteria — identifying "25 types of those verifiable instructions" and building "around 500 prompts," each containing one or more verifiable instructions.
- URL: https://arxiv.org/abs/2311.07911 — Example instructions cited directly in the abstract-derived text: "write in more than 400 words" and "mention the keyword of AI at least 3 times."
- Paraphrase (from earlier search summary of the same paper): "IFEval has 541 prompts where a prompt contains verifiable instructions that can be checked with a deterministic program, circumventing the need of an LLM or human as judge." Reports both "strict accuracy" and "loose accuracy," where loose accuracy "accepts minor transformations in the responses."
- Paraphrase: the 25 instruction types span "formatting constraints (e.g., 'write exactly four paragraphs')," "content requirements (e.g., 'include the word delicious at least 3 times')," "structural specifications (e.g., 'start each paragraph with a question')," "length constraints (e.g., 'write between 100-150 words')," and "style requirements (e.g., 'write in JSON format')."
- URL: https://deepeval.com/docs/benchmarks-ifeval — DeepEval docs page implementing/explaining IFEval as a benchmark (found via search).
- URL: https://github.com/Skripkon/IFEval-FC — "IFEval-FC" — a related/derivative benchmark evaluating instruction-following specifically in function-calling argument values (found via search, title/topic only).
- URL: https://arxiv.org/abs/2509.18420 — "Instruction-Following Evaluation in Function Calling for Large Language Models" (found via search, adjacent/derivative benchmark).
- URL: https://aclanthology.org/2025.findings-naacl.344/ — "M-IFEval: Multilingual Instruction-Following Evaluation" (found via search, derivative benchmark).
- URL: https://arxiv.org/pdf/2406.13542 — "Self-play with Execution Feedback: Improving Instruction-following Capabilities of Large Language Models" (found via search — describes an approach using execution feedback, i.e. code-verifiable checks, to generate training data that improves instruction following; title/topic level only).

### Constrained decoding's own cost to reasoning/format-following quality (directly relevant to the "trust rate" goal — collected as-is, not synthesized)
- URL: https://arxiv.org/abs/2408.02442 — "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models" (Tam et al., 2024). WebFetch verbatim: "Structured generation, the process of producing content in standardized formats like JSON and XML, is widely utilized in real-world applications" to extract information from LLMs. Findings: "we observe a significant decline in LLMs reasoning abilities under format restrictions" and "stricter format constraints generally lead to greater performance degradation in reasoning tasks."
- URL: https://arxiv.org/abs/2408.02442 — Paraphrase (from earlier search summary of same paper): "structured formats enhance classification accuracy" but "undermine nuanced reasoning" — i.e., the effect is task-dependent (helps classification-style tasks, hurts open-ended reasoning).
- URL: https://aclanthology.org/2024.emnlp-industry.91.pdf (ACL Anthology version, EMNLP 2024 industry track) — Same "Let Me Speak Freely?" paper, published venue copy.
- URL: https://arxiv.org/abs/2501.10868 (also https://arxiv.org/html/2501.10868v3) — "JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models." Paraphrase: benchmark of "10,000 real-world JSON schemas that encompass a wide range of constraints with varying complexity," assessing constrained decoding across "efficiency in generating constraint-compliant outputs, coverage of diverse constraint types, and quality of the generated outputs." Evaluated six frameworks: "Guidance, Outlines, Llamacpp, XGrammar, OpenAI, and Gemini." Schema sources include GitHub, Kubernetes, API specs, and GlaiveAI function-call schemas.
- URL: https://github.com/epfl-dlab/jsonschemabench (mirrored at https://github.com/guidance-ai/jsonschemabench) — Code/data repo for the above benchmark.
- URL: https://huggingface.co/datasets/epfl-dlab/JSONSchemaBench — Dataset card for JSONSchemaBench.
- Paraphrase (from a separate search-result synthesis, general finding not tied to one single paper — treat as aggregate/UNVERIFIED for exact percentage but consistent across sources): "Recent works have documented performance degradation by 10-30% compared to unconstrained generation under hard structural constraints." Cause described as forcing "an answer field before completing chain-of-thought reasoning," with math-heavy tasks like GSM8K showing "over 30% degradation" in some cited work.
- URL: https://arxiv.org/html/2601.07525v2 — "Thinking Before Constraining: A Unified Decoding Framework for Large Language Models." Paraphrase: proposes letting models "alternate between free-form reasoning and structured generation, deferring structure until reasoning is complete" as a fix for the reasoning/format tension (title + abstract-level paraphrase, not deep-fetched).
- URL: https://arxiv.org/html/2605.02363v1 — "When Correct Isn't Usable: Improving Structured Output Reliability in Small Language Models" (found via search, directly relevant to small/local models specifically — title + topic only, not deep-fetched).
- URL: https://arxiv.org/html/2206.05395v2 — "Why is constrained neural language generation particularly challenging?" (found via search, survey/analysis paper — title only).
- URL: https://arxiv.org/pdf/2604.06066 — "From Hallucination to Structure Snowballing: The Alignment Tax of Constrained Decoding in LLM Reflection" (found via search, title/topic only — suggests constrained decoding can compound errors during self-reflection/verification loops).
- URL: https://arxiv.org/pdf/2606.25605 — "Constraint Tax in Open-Weight LLMs: An Empirical Study of Tool Calling Suppression Under Structured Output Constraints" (found via search, title/topic only — specifically about open-weight/local models).

### Practitioner-reported "JSON mode gotchas" (blog-level, non-academic — flagged as such)
- URL: https://tianpan.co/blog/2025-10-29-structured-outputs-llm-production — "Beyond JSON Mode: Getting Reliable Structured Outputs from LLMs in Production." Paraphrase (from search summary, numbers are blog-author-reported and UNVERIFIED against a primary study): "JSON mode without schema enforcement fails 8-15% of the time in production"; "Testing shows a 2-5% schema mismatch rate with JSON mode—the JSON is always valid, but the structure is not always what you asked for, with missing fields, unexpected field names, and type mismatches being common."
- Same source, paraphrase: "Math problems, symbolic reasoning, complex analysis all showed 10–15% performance degradation when models were locked into JSON-mode compared to free-form generation followed by structured conversion."
- Same source, paraphrase (directly relevant to AMDA's verifier design): "Constrained decoding guarantees syntactic conformance, not semantic correctness—a system with perfect schema enforcement can reliably produce valid JSON, but whether the sentiment label or other values are actually correct for the input is a completely separate question."
- URL: https://tianpan.co/blog/2026-04-16-grammar-constrained-generation-output-reliability — "Grammar-Constrained Generation: The Output Reliability Technique Most Teams Skip" (found via search, same blog/author, not deep-fetched).

---

## 6. Practitioner posts — Hacker News / Medium / Reddit

- URL: https://news.ycombinator.com/item?id=46635309 — "LLM Structured Outputs Handbook" (HN, Jan 2026). Paraphrase: "constrained non-determinism" framing — "we can reliably use LLMs as part of a larger pipeline or process (such as an agent with tool-calling)" because "constrained decoding, also known as structured generation, is one of the most reliable ways to produce structured outputs by enforcing structure during token generation instead of validating the output after it's generated... logits are modified in real time to remove any tokens that would violate your defined structure." Framed as "one of the most underrated features in LLM engines."
- URL: https://news.ycombinator.com/item?id=45345207 — "Sampling and structured outputs in LLMs" (HN). See Section 1 (Guidance/llguidance) for extracted content.
- URL: https://news.ycombinator.com/item?id=44677864 — "Structllm – structured output support to any LLM provider" (HN, July 2025). Paraphrase: tool providing structured-output support across providers; per search summary requires "LLM models have 7B parameters or more."
- URL: https://news.ycombinator.com/item?id=40713952 — "Every Way to Get Structured Output from LLMs" (HN, June 2024). Paraphrase: discusses BAML, "open source under Apache 2.0."
- URL: https://boundaryml.com/blog/structured-output-from-llms — "Every Way To Get Structured Output From LLMs" — BAML Blog, the source article behind the above HN thread.
- URL: https://news.ycombinator.com/item?id=36750083 — "Show HN: Structured output from LLMs without reprompting" (HN, July 2023). Paraphrase: addresses "problems getting models to adhere to schemas like JSON or XML, or regex," with focus on "bulk processing unstructured data or generating synthetic data."
- URL: https://news.ycombinator.com/item?id=44879051 — "How to deal with streaming LLM structured output" (HN — found via search, title/topic only).
- URL: https://news.ycombinator.com/item?id=41419624 — "Show HN: Best Practices for Using Structured Output from LLMs" (HN, Sept 2024). Paraphrase of discussion themes (per search synthesis, not primary-source verified per-comment): "Three practical approaches to enforce structured output are Prompt Engineering, Function Calling, and Output Validation." One commenter noted disliking the overall approach; temperature was reportedly set to 1.0 "to ensure a reasonable amount of variation." Community tips surfaced: prefer YAML over JSON for LLM-friendliness ("less sensitivity to tokenization quirks" per paraphrase), and "when dealing with classification or selection from a predefined list, instructing the AI to return the item's index rather than the full string avoids fragile text matching."
- URL: https://news.ycombinator.com/item?id=44867097 — "Why deterministic output from LLMs is nearly impossible" (HN, found via search, title/topic only).
- URL: https://news.ycombinator.com/item?id=45200925 — "Defeating Nondeterminism in LLM Inference" (HN, found via search, title/topic only).
- URL: https://news.ycombinator.com/item?id=42522610 — "LLM's are non-deterministic: they'll happily give different answers to the *same..." (HN, found via search, title/topic only).
- URL: https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670 — "Practical Techniques to constraint LLM output in JSON format" (Medium, found via search).
- URL: https://medium.com/canoe-intelligence-technology/guided-generation-with-outlines-c09a0c2ce9eb — "Guided Generation with Outlines" (Medium, Canoe Intelligence Technology, found via search).
- URL: https://medium.com/edelman-ai/structured-outputs-the-unsung-hero-for-llm-developers-c8b27df0282b — "Structured Outputs: The Unsung Hero for LLM Developers" (Medium). Paraphrase: "structured outputs are an underappreciated feature that every AI practitioner should know and use."
- URL: https://medium.com/data-from-the-trenches/taming-llm-outputs-59a58ee3246d — "Taming LLM Outputs" (Medium). Paraphrase: "structured text generation is a cornerstone of building robust LLM applications, and constrained decoding techniques guarantee 100% compliance."
- URL: https://medium.com/@docherty/controlling-your-llm-deep-dive-into-constrained-generation-1e561c736a20 — "Controlling your LLM: Deep dive into Constrained Generation" (Medium, found via search).
- URL: https://medium.com/@prestonblckbrn/structured-output-streaming-for-llms-a836fc0d35a2 — "Structured Output Streaming for LLMs" (Medium, found via search — covers grammar-based constrained decoding plus streaming).
- URL: https://medium.com/@brijeshrn/beyond-free-form-text-how-constrained-decoding-is-reshaping-structured-generation-in-llms-5f7a38bef259 — "Beyond Free-Form Text: How Constrained Decoding is Reshaping Structured Generation in LLMs" (Medium). Paraphrase: covers "techniques that guide LLMs to generate valid, well-formed, and faithful outputs without crippling performance" — i.e. acknowledges the quality-cost tradeoff discussed in Section 5.
- URL: https://medium.com/@emrekaratas-ai/structured-output-generation-in-llms-json-schema-and-grammar-based-decoding-6a5c58b698a6 — "Structured Output Generation in LLMs: JSON Schema and Grammar-Based Decoding" (Medium, found via search). Paraphrase: contrasts "using JSON Schema definitions to guide/validate outputs" vs. "grammar-based decoding which enforces rules during generation."
- URL: https://medium.com/@sonitanishk2003/from-chaos-to-structure-a-developers-guide-to-reliable-json-from-llms-de6dc0ffde07 — "From Chaos to Structure: A Developer's Guide to Reliable JSON from LLMs" (Medium, found via search).
- URL: https://medium.com/@zh2408/structured-output-for-beginners-3-must-know-prompting-tips-45a28aa643c6 — "Structured Output for Beginners: 3 Must-Know Prompting Tips" (Medium/DEV cross-post, found via search).
- URL: https://medium.com/@docherty/mastering-structured-output-in-llms-choosing-the-right-model-for-json-output-with-langchain-be29fb6f6675 — "Mastering Structured Output in LLMs 1: JSON output with LangChain" (Medium, found via search).
- Note: targeted queries for `site:reddit.com` + constrained decoding / GBNF / LocalLLaMA returned no indexed results through the search tool available in this session (queries logged: `"constrained decoding" reddit LocalLLaMA JSON`, `reddit LocalLLaMA structured output grammar experience`, `site:reddit.com constrained decoding OR "grammar" OR "structured output" LLM local model`, `reddit.com/r/LocalLLaMA GBNF grammar json extraction`). No Reddit-specific practitioner posts were retrieved despite multiple query variations — flagged as a gap rather than fabricated.

---

## Sources (all URLs visited or returned by search/fetch calls in this session)

- https://github.com/dottxt-ai/outlines
- https://github.com/dottxt-ai/outlines-core
- https://dottxt-ai.github.io/outlines/welcome/
- https://dottxt-ai.github.io/outlines/0.1.1/
- https://dottxt-ai.github.io/outlines/cookbook/
- https://dottxt-ai.github.io/outlines/latest/reference/generation/structured_generation_explanation/
- https://dottxt-ai.github.io/outlines/reference/generation/generation/
- https://tom-doerr.github.io/repo_posts/2025/02/26/dottxt-ai-outlines.html
- https://arxiv.org/abs/2307.09702
- https://arxiv.org/pdf/2307.09702
- https://arxiv.org/pdf/2307.09702v1
- https://id2thomas.medium.com/nlg-outlines-efficient-guided-generation-for-large-language-models-willard-louf-2023-3c9463543901
- https://medium.com/canoe-intelligence-technology/guided-generation-with-outlines-c09a0c2ce9eb
- https://textmodels.tech/efficient-guided-generation-for-large-language-models-abstract-and-intro
- https://www.researchgate.net/publication/372468267_Efficient_Guided_Generation_for_LLMs
- https://huggingface.co/papers/2307.09702
- https://www.semanticscholar.org/paper/Efficient-Guided-Generation-for-Large-Language-Willard-Louf/c4ceaef35bca063815f50d90a087acbd07a65478
- https://github.com/microsoft/guidance/blob/main/guidance/library/_gen.py
- https://github.com/microsoft/guidance/tree/main
- https://www.microsoft.com/en-us/research/project/guidance-control-lm-output/
- https://github.com/guidance-ai/guidance
- https://github.com/guidance-ai/llguidance
- https://github.com/microsoft/Phi-3CookBook/blob/main/md/01.Introduce/Guidance.md
- https://guidance-ai.github.io/llguidance/llg-go-brrr
- https://github.com/microsoft/guidance/issues/281
- https://github.com/CatalinCighi/microsoft-guidance
- https://github.com/microsoft/PhiCookBook/blob/main/md/01.Introduction/01/01.Guidance.md
- https://github.com/noamgat/lm-format-enforcer
- https://github.com/Saibo-creator/Awesome-LLM-Constrained-Decoding
- https://github.com/Saibo-creator/Awesome-LLM-Constrained-Decoding/blob/main/README.md
- https://github.com/noamgat/lm-format-enforcer/blob/main/CHANGELOG.md
- https://github.com/noamgat/lm-format-enforcer/blob/main/samples/colab_llamacpppython_integration.ipynb
- https://mychen76.medium.com/practical-techniques-to-constraint-llm-output-in-json-format-e3e72396c670
- https://www.bentoml.com/blog/structured-decoding-in-vllm-a-gentle-introduction
- https://haystack.deepset.ai/integrations/lmformatenforcer
- https://github.com/noamgat/lm-format-enforcer/blob/main/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- https://mintlify.com/ggml-org/llama.cpp/advanced/grammars
- https://deepwiki.com/ggml-org/llama.cpp/8.1-grammar-and-structured-output
- https://deepwiki.com/abetlen/llama-cpp-python/6.1-grammar-based-generation
- https://node-llama-cpp.withcat.ai/guide/grammar
- https://withcatai.github.io/node-llama-cpp/guide/grammar
- https://til.simonwillison.net/llms/llama-cpp-python-grammars
- https://llama-cpp-agent.readthedocs.io/en/latest/grammar-api-reference/
- https://huggingface.co/spaces/Steven10429/apply_lora_and_quantize/blob/main/llama.cpp/grammars/README.md
- https://github.com/BITcyman/llama.cpp/blob/main/grammars/README.md
- https://github.com/ggml-org/llama.cpp
- https://github.com/ggml-org/llama.cpp/blob/master/examples/json_schema_to_grammar.py
- https://github.com/ggml-org/llama.cpp/discussions/15341
- https://www.imaurer.com/blog/posts/2023-09-06-llama-cpp-grammars/
- https://replicate.com/blog/llama-2-grammars
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://openai.com/index/introducing-structured-outputs-in-the-api/
- https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs
- https://openrouter.ai/docs/guides/features/structured-outputs
- https://www.digitalapplied.com/blog/openai-structured-outputs-complete-guide
- https://docs.x.ai/developers/model-capabilities/text/structured-outputs
- https://dev.to/mattlewandowski93/guaranteed-structured-outputs-with-openai-5g0i
- https://developers.openai.com/cookbook/examples/structured_outputs_intro
- https://medium.com/@piyushsonawane10/getting-structured-outputs-from-openai-models-a-developers-guide-3090e8120785
- https://callsphere.ai/blog/openai-structured-outputs-response-format-json-schema
- https://docs.fireworks.ai/structured-responses/structured-response-formatting
- https://fireworks.ai/blog/why-do-all-LLMs-need-structured-output-modes
- https://fireworks.ai/docs/structured-responses/structured-output-grammar-based
- https://fireworks.ai/blog/constrained-generation-with-reasoning
- https://github.com/BerriAI/litellm/issues/29604
- https://python.useinstructor.com/integrations/fireworks/
- https://x.com/FireworksAI_HQ/status/1885860816911810882
- https://materialsproject.github.io/fireworks/json_schema.html
- https://github.com/mlc-ai/xgrammar
- https://github.com/mlc-ai/xgrammar/blob/main/README.md
- https://catalyst.cs.cmu.edu/projects/xgrammar.html
- https://pypi.org/project/xgrammar/
- https://blog.mlc.ai/2026/05/04/xgrammar-2-fast-customizable-structured-generation
- https://arxiv.org/abs/2411.15100
- https://arxiv.org/pdf/2411.15100
- https://www.semanticscholar.org/paper/XGrammar:-Flexible-and-Efficient-Structured-Engine-Dong-Ruan/274ca059ee4997f1e008bc8962aef3d22897f17a
- https://blog.mlc.ai/2024/11/22/achieving-efficient-flexible-portable-structured-generation-with-xgrammar
- https://docs.vllm.ai/en/latest/features/structured_outputs/
- https://docs.vllm.ai/en/v0.8.4/features/structured_outputs.html
- https://docs.vllm.ai/en/v0.8.2/features/structured_outputs.html
- https://vllm.ai/blog/struct-decode-intro
- https://arxiv.org/html/2509.06631v1
- https://github.com/vllm-project/vllm-ascend/issues/177
- https://blog.squeezebits.com/guided-decoding-performance-vllm-sglang
- https://developers.redhat.com/articles/2025/06/03/structured-outputs-vllm-guiding-ai-responses
- https://docs.vllm.ai/projects/ascend/en/v0.10.0rc1/user_guide/feature_guide/structured_output.html
- https://python.useinstructor.com/
- https://devopsboys.com/blog/llm-output-validation-instructor-pydantic-production-2026
- https://python.useinstructor.com/concepts/reask_validation/
- https://github.com/567-labs/instructor
- https://pydantic.dev/articles/llm-intro
- https://python.useinstructor.com/concepts/validation/
- https://machinelearningmastery.com/the-complete-guide-to-using-pydantic-for-validating-llm-outputs/
- https://github.com/mdwoicke/llm-pydantic-instructor
- https://python.useinstructor.com/learning/validation/basics/
- https://python.useinstructor.com/getting-started/
- https://xebia.com/blog/enforce-and-validate-llm-output-with-pydantic/
- https://arxiv.org/abs/2309.11495
- https://arxiv.org/abs/2309.11495v1
- https://learnprompting.org/docs/advanced/self_criticism/chain_of_verification
- https://www.summarizepaper.com/en/arxiv-id/2309.11495v1/
- https://arxiv.org/pdf/2309.11495
- https://www.research-collection.ethz.ch/server/api/core/bitstreams/468e77de-b21f-4ede-b179-8a52b01a1c5a/content
- https://arxiv.org/pdf/2503.17229
- https://api.semanticscholar.org/arXiv:2309.11495
- https://arxiv.org/pdf/2505.20487
- https://arxiv.org/pdf/2603.00539
- https://arxiv.org/html/2604.16790v1
- https://arxiv.org/pdf/2604.16790
- https://galileo.ai/blog/llm-as-a-judge-vs-human-evaluation
- https://arxiv.org/pdf/2604.18164
- https://arxiv.org/pdf/2604.16706
- https://openreview.net/forum?id=3GTtZFiajM
- https://arxiv.org/pdf/2411.16594
- https://www.arxiv.org/pdf/2509.26072
- https://arxiv.org/pdf/2604.23178
- https://www.beam.cloud/blog/best-e2b-alternatives
- https://huggingface.co/docs/smolagents/en/tutorials/secure_code_execution
- https://ramnode.com/guides/e2b
- https://northflank.com/blog/e2b-vs-modal
- https://northflank.com/blog/best-alternatives-to-e2b-dev-for-running-untrusted-code-in-secure-sandboxes
- https://e2b.dev/docs
- https://arxiv.org/pdf/2606.24937
- https://arxiv.org/pdf/2504.00018
- https://e2b.dev/blog/build-ai-data-analyst-with-sandboxed-code-execution-using-typescript-and-gpt-4o
- https://arxiv.org/pdf/2510.12399
- https://arxiv.org/abs/2311.07911
- https://github.com/Skripkon/IFEval-FC
- https://arxiv.org/pdf/2507.16534
- https://arxiv.org/abs/2509.18420
- https://aclanthology.org/2025.findings-naacl.344/
- https://arxiv.org/pdf/2406.13542
- https://arxiv.org/pdf/2406.11301
- https://arxiv.org/pdf/2505.16944
- https://deepeval.com/docs/benchmarks-ifeval
- https://arxiv.org/pdf/2503.09407
- https://til.simonwillison.net/python/subprocess-time-limit
- https://mbrenndoerfer.com/writing/code-execution-sandboxed-feedback-iterative-refinement-safety
- https://apxml.com/courses/building-advanced-llm-agent-tools/chapter-5-advanced-tool-functionality/code-execution-tools
- https://healeycodes.com/running-untrusted-python-code
- https://github.com/openedx/codejail
- https://inference.sh/blog/tools/sandboxed-execution
- https://dida.do/blog/setting-up-a-secure-python-sandbox-for-llm-agents
- https://runebook.dev/en/docs/python/library/subprocess/subprocess.TimeoutExpired.timeout
- https://sparkco.ai/blog/mastering-the-openai-code-interpreter-a-deep-dive
- https://community.openai.com/t/code-interpreter-sandbox/543222
- https://developers.openai.com/api/docs/guides/tools-code-interpreter
- https://ryan.govost.es/2025/openai-code-interpreter/
- https://itnext.io/openais-code-execution-runtime-replicating-sandboxing-infrastructure-a2574e22dc3c
- https://github.com/VolkanSah/Exploring-the-Code-Interpreter-in-OpenAI-GPT
- https://medium.com/@Shrishml/making-our-own-code-interpreter-part-1-making-of-a-sandbox-382da3339eaa
- https://developers.openai.com/codex/concepts/sandboxing
- https://e2b.dev/blog/e2b-sandbox
- https://developers.openai.com/blog/openai-for-developers-2025
- https://news.ycombinator.com/item?id=46635309
- https://arxiv.org/pdf/2512.19305
- https://news.ycombinator.com/item?id=45345207
- https://news.ycombinator.com/item?id=44677864
- https://arxiv.org/pdf/2606.25605
- https://news.ycombinator.com/item?id=40713952
- https://news.ycombinator.com/item?id=36750083
- https://news.ycombinator.com/item?id=44879051
- https://news.ycombinator.com/item?id=41419624
- https://arxiv.org/pdf/2311.12785
- https://towardsdatascience.com/structured-outputs-with-llms-json-mode-function-calling-and-when-to-use-each/
- https://dev.to/clawgenesis/the-structured-output-pattern-how-to-get-llms-to-return-clean-json-every-time-dod
- https://tokenmix.ai/blog/structured-output-json-guide
- https://techsy.io/en/blog/llm-structured-outputs-guide
- https://tianpan.co/blog/2025-10-29-structured-outputs-llm-production
- https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms
- https://docs.litellm.ai/docs/completion/json_mode
- https://humanloop.com/blog/structured-outputs
- https://docs.cohere.com/docs/structured-outputs
- https://medium.com/@michael.hannecke/beyond-json-picking-the-right-format-for-llm-pipelines-b65f15f77f7d
- https://arxiv.org/pdf/2406.04926
- https://okareo.com/blog/posts/validate-llm-output
- https://www.evidentlyai.com/llm-guide/llm-evaluation-metrics
- https://arxiv.org/pdf/2605.13898
- https://towardsdatascience.com/how-to-perform-comprehensive-large-scale-llm-validation/
- https://arxiv.org/pdf/2312.11681
- https://arxiv.org/pdf/2502.07036
- https://arxiv.org/pdf/2508.15503
- https://arxiv.org/html/2603.03305
- https://arxiv.org/pdf/2603.13351
- https://arxiv.org/html/2601.07525v2
- https://arxiv.org/html/2501.10868v1
- https://arxiv.org/html/2605.02363v1
- https://arxiv.org/html/2206.05395v2
- https://arxiv.org/pdf/2501.10868
- https://arxiv.org/pdf/2604.13006
- https://arxiv.org/pdf/2604.06066
- https://aclanthology.org/2024.emnlp-industry.91.pdf
- https://arxiv.org/abs/2408.02442
- https://arxiv.org/abs/2408.02442v1
- https://huggingface.co/papers/2408.02442
- https://www.aimodels.fyi/papers/arxiv/let-me-speak-freely-study-impact-format
- https://www.emergentmind.com/papers/2408.02442
- https://github.com/567-labs/instructor/issues/956
- https://ui.adsabs.harvard.edu/abs/2024arXiv240802442R/abstract
- https://arxiv.org/html/2408.02442v1
- https://arxiv.org/pdf/2408.02442
- https://tianpan.co/blog/2026-04-16-grammar-constrained-generation-output-reliability
- https://arxiv.org/pdf/2502.05111
- https://arxiv.org/pdf/2508.10111
- https://arxiv.org/pdf/2503.24191
- https://arxiv.org/html/2503.24191v3
- https://arxiv.org/pdf/2506.01151
- https://arxiv.org/pdf/2512.17967
- https://arxiv.org/pdf/2604.14862
- https://arxiv.org/pdf/2603.27905
- https://arxiv.org/pdf/2602.00612
- https://arxiv.org/pdf/2507.16768
- https://arxiv.org/abs/2310.01798
- https://tldr.takara.ai/p/2310.01798
- https://openreview.net/forum?id=IkmD3fKBPQ
- https://www.semanticscholar.org/paper/Large-Language-Models-Cannot-Self-Correct-Reasoning-Huang-Chen/6d4bacb69923e1e94fb4de468b939ce6db32fb51
- https://arxiv.org/pdf/2310.01798
- https://openreview.net/pdf?id=IkmD3fKBPQ
- https://arxiv.org/pdf/2311.08152
- https://arxiv.org/pdf/2507.02778
- https://github.com/AkihikoWatanabe/paper_notes/issues/1382
- https://calmops.com/algorithms/self-consistency-reasoning/
- https://arxiv.org/html/2408.17017v1
- https://arxiv.org/pdf/2403.00260
- https://arxiv.org/pdf/2605.13624
- https://learnprompting.org/docs/intermediate/self_consistency
- https://arxiv.org/pdf/2402.15631
- https://www.kinde.com/learn/ai-for-software-engineering/workflows/llm-fan-out-101-self-consistency-consensus-and-voting-patterns/
- https://arxiv.org/pdf/2505.10772
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12468897
- https://proceedings.iclr.cc/paper_files/paper/2024/file/8b4add8b0aa8749d80a34ca5d941c355-Paper-Conference.pdf
- https://medium.com/@nandanadas88/self-refine-how-language-models-can-improve-their-own-outputs-7a346d14a293
- https://learnprompting.org/docs/advanced/self_criticism/self_refine
- https://www.emergentmind.com/topics/iterative-self-refinement
- https://www.researchgate.net/publication/369740347_Self-Refine_Iterative_Refinement_with_Self-Feedback
- https://arxiv.org/pdf/2606.17514
- https://arxiv.org/pdf/2506.19607
- https://openreview.net/pdf?id=S37hOerQLB
- https://arxiv.org/pdf/2603.15309
- https://arxiv.org/abs/2303.17651
- https://www.shayon.dev/post/2026/52/lets-discuss-sandbox-isolation/
- https://northflank.com/blog/how-to-sandbox-ai-agents
- https://gvisor.dev/docs/architecture_guide/intro/
- https://medium.com/@earlperry562/how-every-major-tech-company-is-sandboxing-ai-agents-differently-f41b65f14d8a
- https://oneuptime.com/blog/post/2026-02-17-how-to-use-gke-sandbox-gvisor-to-isolate-untrusted-workloads-at-the-container-level/view
- https://oneuptime.com/blog/post/2026-02-09-gke-sandbox-gvisor-workload-isolation/view
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11847206
- https://dev.to/pockit_tools/llm-structured-output-in-2026-stop-parsing-json-with-regex-and-do-it-right-34pk
- https://www.quora.com/How-do-I-label-huge-Twitter-data-set-for-training-a-sentiment-analysis-classifier-without-manually-labeling-them
- https://labs.lamatic.ai/p/llm-sentiment-analysis
- https://arxiv.org/pdf/2504.14706
- https://arxiv.org/pdf/2602.06370
- https://medium.com/@beam_villa/quick-and-easy-sentiment-analysis-with-llm-c61c562d059c
- https://arxiv.org/pdf/2012.15349
- https://arxiv.org/pdf/2509.02651
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11853704
- https://arxiv.org/pdf/2502.13044
- https://dev.to/zachary62/structured-output-for-beginners-3-must-know-prompting-tips-8cc
- https://boundaryml.com/blog/structured-output-from-llms
- https://medium.com/@zh2408/structured-output-for-beginners-3-must-know-prompting-tips-45a28aa643c6
- https://medium.com/@docherty/mastering-structured-output-in-llms-choosing-the-right-model-for-json-output-with-langchain-be29fb6f6675
- https://medium.com/@docherty/controlling-your-llm-deep-dive-into-constrained-generation-1e561c736a20
- https://dev.to/shrsv/taming-llms-how-to-get-structured-output-every-time-even-for-big-responses-445c
- https://builder.aws.com/content/2wzRXcEcE7u3LfukKwiYIf75Rpw/how-to-get-structured-output-from-llms-a-practical-guide
- https://www.leewayhertz.com/structured-outputs-in-llms/
- https://medium.com/edelman-ai/structured-outputs-the-unsung-hero-for-llm-developers-c8b27df0282b
- https://medium.com/data-from-the-trenches/taming-llm-outputs-59a58ee3246d
- https://medium.com/@prestonblckbrn/structured-output-streaming-for-llms-a836fc0d35a2
- https://medium.com/@lad.jai/unlocking-structured-outputs-from-llms-methods-tools-and-techniques-197008bc88da
- https://medium.com/better-ml/herding-llms-structured-output-with-constraints-ae157ecf5d81
- https://medium.com/@brijeshrn/beyond-free-form-text-how-constrained-decoding-is-reshaping-structured-generation-in-llms-5f7a38bef259
- https://medium.com/@emrekaratas-ai/structured-output-generation-in-llms-json-schema-and-grammar-based-decoding-6a5c58b698a6
- https://medium.com/@sonitanishk2003/from-chaos-to-structure-a-developers-guide-to-reliable-json-from-llms-de6dc0ffde07
- https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output
- https://arxiv.org/pdf/2401.09967
- https://arxiv.org/html/2504.05410v1
- https://arxiv.org/html/2407.06146v1
- https://dev.to/jhagerer/llm-non-determinism-what-providers-guarantee-and-how-to-build-around-it-3502
- https://news.ycombinator.com/item?id=44867097
- https://www.bentoml.com/llm/getting-started/tool-integration/structured-outputs
- https://news.ycombinator.com/item?id=45200925
- https://arxiv.org/pdf/2508.20912
- https://news.ycombinator.com/item?id=42522610
- https://arxiv.org/pdf/2508.02721
- https://arxiv.org/pdf/2411.12357
