# Fireworks AI Model Research Log — AMDA Track 1

Research collection only. Raw facts with URLs and quotes/paraphrases. No synthesis, no recommendations.

Models in scope (Fireworks-hosted remote escalation targets):
- minimax-m3
- kimi-k2p7-code
- gemma-4-31b-it
- gemma-4-26b-a4b-it
- gemma-4-31b-it-nvfp4

---

## 1. minimax-m3 (MiniMax M3)

### Fireworks model page
- URL: https://fireworks.ai/models/fireworks/minimax-m3
- Context window: 512K tokens (per Fireworks model page).
- Pricing (serverless): Input $0.30 / 1M tokens; Cached input $0.06 / 1M tokens; Output $1.20 / 1M tokens.
- Parameter count: "MiniMax-M3 is a native multimodal model with 512K context running ~428B parameters and ~23B activated parameters." (verbatim quote from page description) — MoE architecture, ~428B total / ~23B activated.
- Quote (verbatim): "It brings native multimodality, enabling deeper semantic fusion across text, image, and video. M3 also introduces MiniMax Sparse Attention (MSA) to improve long context efficiency, achieving frontier-level performance across long-horizon agentic benchmarks, excelling in both coding and cowork."
- Supported features per page: function calling = yes, image input = yes, fine-tuning = not supported, embeddings = not supported.
- Page did NOT explicitly label the model "reasoning" or state max output tokens separately from context window (fetch summary said "not specified").

### Fireworks launch blog
- URL: https://fireworks.ai/blog/minimax-m3-launch (title: "MiniMax M3 is live: long context + native multimodality at 1/20th the price")
- Quote (verbatim): "At launch, we're supporting up to 500K tokens of context, but are partnering closely with the MiniMax team to bring the full 1M-token context window length in the coming days." — i.e., Fireworks currently caps at 500K even though model card elsewhere says 512K/1M native.
- **Reasoning/thinking toggle confirmed**: Quote (verbatim): "M3 supports toggling thinking on or off at request time, with both modes sharing the same pricing." Implementation per fetch summary: add `"thinking": {"type": "enabled"}` to the request payload (need to verify exact field name/schema against MiniMax's own API docs — see below; this was a WebFetch-tool paraphrase of the blog, not a direct verbatim quote of a code sample, so treat the exact JSON key as UNVERIFIED until cross-checked).
- Pricing history note: "Initially 2x M2.7 pricing during private launch... Now permanently dropped to match M2.7 rates following open-weight release." Long-context requests >512K tokens billed at a higher rate (per paraphrase).
- Speed claims (paraphrased from fetch): per-token compute dropped 95% at 1M-token context; 9x speedup in pre-filling; 15x speedup in decoding; "more than 4× faster than open-source Flash-Sparse-Attention and flash-moba" (quote, exact wording per fetch tool — verify against original page text if quoting downstream).
- Benchmark claim (paraphrase): "Surpasses all open-source models in overall intelligence per Artificial Analysis' index" and "exceeds several closed-source models including Opus 4.6" — specific numeric scores not captured in this fetch.

### Requesty.ai model listing
- URL: https://www.requesty.ai/models/fireworks/minimax-m3
- Context window: 512K tokens; Max output listed as 512K tokens (same as context — likely just reflecting context limit, not a distinct output cap; UNVERIFIED whether there's a separate max_tokens output ceiling).
- Pricing: Input $0.30/1M, Output $1.20/1M, Cache read $0.06/1M (matches Fireworks page).
- Benchmark numbers listed: Coding Index 58.6%, GPQA Diamond 92.9%, Intelligence Index 44.4%, τ²-Bench 88.9%. (Source of these indices e.g. Artificial Analysis not specified on the page per fetch; treat index methodology as UNVERIFIED.)

### Telnyx inference benchmark (third-party, cross-provider)
- URL: https://telnyx.com/resources/inference-minimax-m3-benchmark
- Quote: "Telnyx MiniMax M3 delivered 144.9 tok/s median throughput. Together AI managed 119.8 tok/s." (21% throughput advantage claimed by Telnyx, self-reported).
- E2E latency: Telnyx 7.56s median, Together AI 7.77s, Fireworks 8.52s (median). On longer outputs (100k input/1k output) Telnyx ~48% faster than Fireworks per paraphrase.
- Tail latency quote: "Telnyx MiniMax M3 had a p95 E2E of 14.72s and a max of 19.85s. Fireworks MiniMax M3 had a p95 of 54.06s and a max of 111.51s." — i.e., Fireworks showed much higher tail latency variance in this particular (vendor-authored, so potentially biased) benchmark.
- Note: this benchmark focuses on latency/throughput only; does not report reasoning-token counts or verbosity.

---

## 2. kimi-k2p7-code

### Identity
- This is "Kimi K2.7 Code" (a.k.a. "Kimi-K2.7-Code"), Moonshot AI's coding-specialized variant built on top of Kimi K2.6. Per WebSearch synthesis of the MarkTechPost article (URL below): "Moonshot AI Releases Kimi K2.7-Code: a Coding Model Reporting +21.8% on Kimi Code Bench v2 Over K2.6," released June 12, 2026.
- Fireworks blog title (verbatim): "Kimi K2.7 Code on Fireworks: Better Agents, Lower Cost per Task, Available Day-0" — https://fireworks.ai/blog/kimi-k2p7-code

### Architecture (Hugging Face model card)
- URL: https://huggingface.co/moonshotai/Kimi-K2.7-Code
- Total parameters: 1 trillion (1T); Activated parameters: 32B per token.
- MoE: 384 experts total, 8 selected per token + 1 shared expert; 61 layers (incl. 1 dense layer); attention = MLA (Multi-head Latent Attention); vocab size 160K; vision encoder = MoonViT (+400M params).
- Context window: 256K tokens (262,144).
- Native INT4 quantization noted by one third-party site (automatio.ai — see below); ~595GB on-disk size per that same source (UNVERIFIED against an official Moonshot source, only found via a third-party summary).

### Reasoning/thinking mode — MANDATORY, cannot be disabled (important for token-efficiency scoring)
- Quote (verbatim, from HF model card fetch): **"Kimi-K2.7-Code forces thinking and preserve_thinking as True."**
- Paraphrase from same card: reasoning mode is mandatory and cannot be disabled; the model maintains "full reasoning content across multi-turn interactions" via the preserve_thinking feature.
- Corroborated by a second independent source, codersera.com "Kimi K2.7 Code: The Complete Guide" (surfaced via WebSearch, not independently re-fetched): "Thinking mode is mandatory; disabling it returns an API error." Also per that same search-tool paraphrase: "Temperature, top-p, and penalties are server-locked, preventing customization." (URL: https://codersera.com/blog/kimi-k2-7-complete-guide-2026/ — flagging this specific quote as coming from the WebSearch tool's synthesis of the page, not a direct WebFetch verbatim pull; treat exact wording as paraphrase-grade, but the substantive claim — mandatory thinking, no disable — is corroborated independently by the HF model card's "forces thinking" line.)
- devops.com (URL below) paraphrase: "K2.7-Code forces thinking mode on, and you can't turn it off."

### Token-efficiency claims (Moonshot / Fireworks)
- Quote (verbatim, HF model card via fetch): "reducing thinking-token usage by approximately 30% compared with Kimi K2.6."
- Fireworks blog (https://fireworks.ai/blog/kimi-k2p7-code) verbatim quotes captured via fetch:
  - "1T total parameters, 32B active per token, a 256K context window"
  - "shorter generations, smaller context on every following turn, faster loops, fewer retries"
  - "cost per finished task is meaningfully lower" (vs. K2.6 at same rate card)
  - "A 30% cut in reasoning tokens is, to us, worth more than a 30% cut in price." (Fireworks' own framing)
- WebSearch paraphrase of same blog: "Because agentic workflows compound costs over long sequences, spending fewer tokens on 'thinking' results in faster loops, lower overall task costs, and less reliance on redundant context."

### Benchmarks — two different tables found, both vendor/aggregator-reported, NOT reconciled here
- Table A (Moonshot's own proprietary K2.7-vs-K2.6 deltas, via MarkTechPost/HF fetch):
  | Benchmark | K2.6 | K2.7-Code | Δ |
  |---|---|---|---|
  | Kimi Code Bench v2 | 50.9 | 62.0 | +21.8% |
  | Program Bench | 48.3 | 53.6 | +11.0% |
  | MLS Bench Lite | 26.7 | 35.1 | +31.5% |
  | Kimi Claw 24/7 | 42.9 | 46.9 | +9.3% |
  | MCP Atlas | 69.4 | 76.0 | +9.5% |
  | MCP Mark Verified | 72.8 | 81.1 | +11.4% |
  - Explicit caveat captured via WebSearch synthesis of MarkTechPost: "as of June 12, 2026, there are no independent third-party numbers for K2.7 on the standard public suites — SWE-bench Verified, SWE-bench Pro, Terminal-Bench, LiveCodeBench, GPQA Diamond, AIME, or MMLU-Pro." and "Every benchmark published for K2.7 so far is a Moonshot proprietary benchmark... Treat the scores as vendor-reported and directional, not independently verified."
  - URL: https://www.marktechpost.com/2026/06/12/moonshot-ai-releases-kimi-k2-7-code-a-coding-model-reporting-21-8-on-kimi-code-bench-v2-over-k2-6/
- Table B (automatio.ai aggregator page, standard public-suite-style numbers — origin/methodology unclear, UNVERIFIED, and appears to directly contradict Table A's caveat that no public-suite numbers existed at release):
  | Benchmark | Score |
  |---|---|
  | SWE-Bench | 78.2% |
  | HumanEval | 94.2% |
  | MMLU | 87.2% |
  | MMLU Pro | 71.4% |
  | AIME 2025 | 91.5% |
  | GSM8k | 97.2% |
  | GPQA | 65.8% |
  | IFEval | 88.5% |
  | LiveCodeBench | 68.5% |
  | DocVQA | 90.1% |
  - URL: https://automatio.ai/models/kimi-k2-7-code — also gave headline "78.2% SWE-Bench" in its own title: "Kimi K2.7 Code: 262k Context, 78.2% SWE-Bench, $0.95/M Tokens"
  - Context window per this source: 262,144 tokens; "Max Output" also listed as 262,144 tokens (i.e., same as context, likely not a distinct output cap — UNVERIFIED as a true separate max_tokens ceiling).

### Fireworks pricing (docs.fireworks.ai/serverless/pricing, fetched)
- Standard tier: Input $0.95 / Cached input $0.19 / Output $4.00 (per 1M tokens).
- Priority tier: Input $1.425 / Cached input $0.285 / Output $6.00 (per 1M tokens).
- Matches figures independently listed on https://fireworks.ai/blog/kimi-k2p7-code (Input $0.95/M, Output $4.00/M, cache hits $0.19/M).

### GitHub / Cline integration references
- https://github.com/cline/cline/issues/11553 — "Fireworks AI: add Kimi K2.7 Code, Qwen 3.7 Plus, MiniMax M3; remove deprecated models" (issue tracking adding these exact 2 of our 5 models to Cline's Fireworks provider list).
- https://github.com/cline/cline/pull/11554 — corresponding PR, same title.
- https://github.com/nicobailon/pi-subagents/issues/325 — "Fireworks Kimi rejects subagent tool schema with conflicting 'if' definitions" (surfaced via WebSearch; suggests some tool-schema/function-calling friction with Fireworks' Kimi endpoint specifically; not independently fetched for detail, title only — UNVERIFIED beyond the title).

### Hacker News discussion
- Story found via HN Algolia API (https://hn.algolia.com/api/v1/search?query=Kimi%20K2.7): "Kimi K2.7-Code: open-source coding model with better token efficiency" — objectID 48502347, 463 points, 240 comments, linking to https://huggingface.co/moonshotai/Kimi-K2.7-Code
- Comment thread (fetched https://news.ycombinator.com/item?id=48502347), notable verbatim/paraphrased points:
  - User `kmike84` (paraphrase): Kimi K2.6 enables "lazy prompting" workflows similar to Claude Code but requires "much more precise" prompts than Opus, "often resulting in higher token usage despite cheaper per-token pricing."
  - User `DCKing` (quote): "you'll spend many more tokens and will have to do more managing of the model" with Kimi compared to Claude Sonnet — suggesting total process token cost may not actually be lower.
  - User `regularfry` (quote): "Kimi K2.5 and K2.6 models will comment out failing tests rather than fix" — a behavioral/quality complaint (about K2.5/K2.6, not confirmed for K2.7-Code specifically).
  - Users `Bnjoroge`, `jwbron` (paraphrase): recommend using Kimi for implementation only, after Claude/other models handle planning.
  - Overall thread paraphrase (from WebFetch synthesis): "The consensus suggests Kimi's efficiency gains from lower token costs are offset by reduced code quality and increased oversight requirements." (Note: this is the fetch tool's own summarization of sentiment, not a single verbatim comment — treat as paraphrase.)
- Other HN stories surfaced (titles/points/comments only, not individually fetched):
  - "Kimi K2.7 Code is generally available in GitHub Copilot" — https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/ — 417 points / 182 comments.
  - "Kimi Code K2.7" (Moonshot tweet) — https://twitter.com/Kimi_Moonshot/status/2065377579130142937
  - "Kimi K2.7 Code" (Kimi resources page) — https://www.kimi.com/resources/kimi-k2-7-code
  - "Kimi K2.7 Code" (platform quickstart docs) — https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart

---

## 3. gemma-4-31b-it

### Fireworks model page
- URL: https://fireworks.ai/models/fireworks/gemma-4-31b-it
- Context window: "256K tokens (also listed as 262k tokens in specifications)" (both numbers appeared in the fetch — likely 262,144 = 256*1024, i.e. same number expressed two ways; noting both as found).
- Max output tokens: not specified on page per fetch.
- Pricing: not shown on this Fireworks page (see pricing notes below — not found in docs.fireworks.ai/serverless/pricing table either; that page only listed minimax-m3 and kimi-k2p7-code explicitly, with unlisted models "priced by parameter count and architecture," tier ">16B parameters = $0.90/1M tokens" per costbench.com/pricepertoken.com-style summaries found via WebSearch — UNVERIFIED whether this tier actually applies to gemma-4-31b-it).
- Reasoning/thinking: **Yes** — quote (verbatim): "configurable thinking mode" is listed as a feature.
- Function calling: supported (per fetch).
- Full verbatim description quote: "Gemma 4 31B IT is a multimodal dense model by Google DeepMind with 30.7B parameters. It supports text and image input with a 256K context window, configurable thinking mode, native function calling, and multilingual support in 140+ languages."

### Google DeepMind official page
- URL: https://deepmind.google/models/gemma/gemma-4/
- Model family per this page (paraphrase): variants include E2B & E4B (edge models for mobile/IoT), and 12B/26B/31B "larger variants optimized for consumer GPUs," designed to enable "frontier intelligence on personal computers" (quote).
- Benchmark table captured for "Gemma 4 31B IT Thinking" (i.e., with thinking mode on) via fetch:
  | Benchmark | Score |
  |---|---|
  | MMLU (Multilingual Q&A) | 85.2% |
  | MMMU Pro (Multimodal reasoning) | 76.9% |
  | AIME 2026 (Mathematics) | 89.2% |
  | LiveCodeBench v6 (Competitive coding) | 80.0% |
  | GPQA Diamond (Scientific knowledge) | 84.3% |
  | τ2-bench (Agentic tool use) | 86.4% |
  - Note: this fetch pass did not surface context window length or explicit licensing text on this page (later evidence, e.g. HN/OpenRouter, points to Apache 2.0 — see Section 4).

### ai.google.dev developer docs (family-wide, applies to 31B too)
- URL: https://ai.google.dev/gemma/docs/core
- Quote/paraphrase: Gemma 4 spans four architectures — "Small Sizes: 2B and 4B effective parameter models for 'ultra-mobile, edge, and browser deployment'"; "Dense: 31B parameter model bridging server-grade and local execution"; "Mixture-of-Experts: 26B A4B model designed for 'high-throughput, advanced reasoning'"; "Unified: 12B encoder-free model for multimodal tasks."
- Context windows (paraphrase): "Small models feature 128K context capacity, while medium models support extended 256K windows."
- Quote: "All family members feature 'highly capable reasoners, with configurable thinking modes.'"
- Quote: models include "a dedicated draft model for speculative decoding, enabling significantly faster inference with no quality loss" (multi-token prediction / MTP).
- Quantization formats mentioned: BF16, SFP8, Q4_0, with QAT (Quantization-Aware Training) options, downloadable from Kaggle and Hugging Face.

### NVIDIA build page (base, non-quantized model)
- URL: https://build.nvidia.com/google/gemma-4-31b-it — surfaced in search results as a hosting/build page for the base gemma-4-31b-it model on NVIDIA's platform (title only: "gemma-4-31b-it Model by Google"; not independently fetched in depth).

### Hacker News — official announcement threads (titles/points/comments only, via HN Algolia API fetch and one WebSearch pass; two different vantage points on the same news, numbers NOT reconciled here)
- Via https://hn.algolia.com/api/v1/search?query=Gemma%204 fetch: "Google releases Gemma 4 open models" → https://deepmind.google/models/gemma/gemma-4/ — 1,812 points / 474 comments.
- Via a separate WebSearch pass: reported "As of April 3, 2026, the Hacker News thread showed about 1211 points and 360 comments" for a submission of https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/ (a different canonical URL than the deepmind.google one) — flagging the discrepancy in point/comment counts across the two search passes without reconciling; these may be two distinct HN submissions of the same announcement, or a stale/live count mismatch.
- Paraphrase from that WebSearch pass: "Gemma 4 is available in four versatile sizes: Effective 2B (E2B), Effective 4B (E4B), 26B Mixture of Experts (MoE) and 31B Dense."
- Licensing theme (quote): "Apache 2.0 is a big shift" was described as "one of the phrases that appeared repeatedly in highly upvoted comments," with Hugging Face co-founder Clément Delangue quoted calling it "a huge milestone." (Release date corroborated elsewhere as April 3, 2026 — see OpenRouter listing in Section 4.)
- Other related HN stories (titles/points/comments only, not independently fetched for comment content):
  - "Gemma 4 12B: A unified, encoder-free multimodal model" — https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/ — 1,062 pts / 401 comments.
  - "Gemma 4 on iPhone" — https://apps.apple.com/nl/app/google-ai-edge-gallery/id6749645337 — 868 pts / 234 comments.
  - "Accelerating Gemma 4: faster inference with multi-token prediction drafters" — https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/ — 687 pts / 330 comments.
  - "Indexing a year of video locally on a 2021 MacBook with Gemma4-31B (50GB swap)" — https://blog.simbastack.com/indexed-a-year-of-video-locally/ — 471 pts / 142 comments.
  - "Running Gemma 4 locally with LM Studio's new headless CLI and Claude Code" — https://ai.georgeliu.com/p/running-google-gemma-4-locally-with — 407 pts / 103 comments.
  - "Gemma 4 QAT models: Optimizing compression for mobile and laptop efficiency" — https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/ — 406 pts / 130 comments.
  - "April 2026 TLDR Setup for Ollama and Gemma 4 26B on a Mac mini" — https://gist.github.com/greenstevester/fc49b4e60a4fef9effc79066c1033ae5 — 330 pts / 123 comments.
  - "Google Gemma 4 Runs Natively on iPhone with Full Offline AI Inference" — https://www.gizmoweek.com/gemma-4-runs-iphone/ — 303 pts / 187 comments.
  - "I ran Gemma 4 as a local model in Codex CLI" — https://blog.danielvaughan.com/i-ran-gemma-4-as-a-local-model-in-codex-cli-7fda754dc0d4 — 285 pts / 116 comments.

### Third-party token-efficiency comparison (31B specifically vs. Qwen3.5 27B)
- URL: https://kaitchup.substack.com/p/gemma-4-31b-vs-qwen35-27b-inference (paywalled article; only free-preview portion retrievable)
- Quote (verbatim): Gemma 4 31B "rarely generates more than 20k tokens, especially compared with Qwen3.5, which often overthinks and can exceed 100k tokens."
- Paraphrase: "Gemma 4 31B achieves higher accuracy on most of the benchmarks tested" vs Qwen3.5 27B, "with only marginal gaps on MMLU Pro and GPQA Diamond."
- Quote: Gemma 4 31B answers are "remarkably consistent" despite Google's recommended temperature of 1.0, "which typically increases variability."
- Paraphrase: using a "CoDeC metric" for generalization vs memorization, "Gemma 4 31B appears to generalize much better, which means its benchmark scores are more likely to reflect its actual capabilities."
- Caveat: detailed token-efficiency/inference-speed/latency/memory numbers are behind the Kaitchup paywall; only the qualitative 20k-vs-100k-token claim above was retrievable in the free preview.

---

## 4. gemma-4-26b-a4b-it

### Fireworks model page
- URL: https://fireworks.ai/models/fireworks/gemma-4-26b-a4b-it (confirmed to exist via WebSearch result title "Gemma 4 26B A4B IT API & Playground | Fireworks AI"; page content pulled via WebSearch synthesis, not an independent WebFetch pass)
- Paraphrase: "Gemma 4 26B A4B IT is a multimodal Mixture-of-Experts model by Google DeepMind with 25.2B total parameters (3.8B active). It supports text and image input with a 256K context window, configurable thinking mode, native function calling."
- Architecture: MoE, "the 'A' in 26B A4B stands for 'active parameters'... By only activating a 4B subset of parameters during inference, the Mixture-of-Experts model runs much faster than its 26B total might suggest." (paraphrase from WebSearch synthesis) — "Despite 25.2B total parameters, only 3.8B activate per token during inference — delivering near-31B quality at a fraction of the compute cost" (paraphrase).
- Trending/listed as available on Fireworks with function-calling and vision support (per WebSearch synthesis of fireworks.ai listing pages).

### Hugging Face model card
- URL: https://huggingface.co/google/gemma-4-26B-A4B-it
- Context window: 256K tokens.
- Benchmark table (as fetched):
  | Benchmark | Score |
  |---|---|
  | MMLU Pro | 82.6% |
  | GPQA Diamond | 82.3% |
  | MMMU Pro (Vision) | 73.8% |
  | LiveCodeBench v6 | 77.1% |
  | AIME 2026 (no tools) | 88.3% |
  | Codeforces ELO | 1718 |
- Thinking-mode API parameters (quote/paraphrase from fetch):
  - "Trigger thinking via `<|think|>` token in system prompt; remove token to disable thinking."
  - "Set `enable_thinking=True/False` in `apply_chat_template()`."
  - **Default behavior (quote): "Thinking mode is not enabled by default."** (This directly conflicts with community reports below claiming the model thinks/reasons verbosely "by default" / cannot be fully suppressed — logging both without reconciling.)
  - When enabled, output format (quote): `<|channel>thought\n[reasoning]<channel|>[answer]`
  - Multi-turn note (quote): "In multi-turn conversations, the historical model output should only include the final response. Thoughts from previous model turns must _not be added_ before the next user turn begins."
  - Note: "For E2B/E4B variants without thinking enabled, empty thought tags still generate" (paraphrase).
  - Recommended sampling params: `temperature=1.0`, `top_p=0.95`, `top_k=64` (quote-adjacent).
  - `processor.parse_response()` function documented to auto-separate reasoning from final answer (paraphrase).
- A separate, non-"-it" base repo also exists: https://huggingface.co/google/gemma-4-26B-A4B (found via search, not independently fetched).

### Community: "how to enable/disable thinking" discussion (Hugging Face)
- URL: https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/discussions/6 — "How to enable thinking" (title only, surfaced via WebSearch; not independently fetched for full thread content beyond what's summarized under the model-card bullet above about `<thought>` tags vs `<thinking>` tags — one WebSearch synthesis pass noted: "The model uses `<thought>` tags instead of `<thinking>` tags.")

### Pricing cross-references
- **OpenRouter** (https://openrouter.ai/google/gemma-4-26b-a4b-it, fetched): Pricing "$0.06 per 1M input tokens / $0.33 per 1M output tokens." Context window listed as "262K tokens." Release date: "April 3, 2026." License: "Apache 2.0." Paraphrase: "near-31B quality at a fraction of the compute cost" via sparse activation. Prompt caching "can reduce effective costs by 60-80% depending on context repetition patterns" (OpenRouter-specific framing, not necessarily transferable to Fireworks' own cache-pricing mechanics).
- **OpenRouter free tier**: a separate listing exists at https://openrouter.ai/google/gemma-4-26b-a4b-it:free ("Gemma 4 26B A4B (free)") — surfaced in search results only, not independently fetched.
- Note: these are OpenRouter's own pricing, NOT Fireworks' — Fireworks-specific pricing for this exact model ID was not found on docs.fireworks.ai/serverless/pricing (that page only enumerated minimax-m3 and kimi-k2p7-code by name among our 5 target models).

### Other hosting platforms (existence confirmed via search, not deep-fetched)
- Ollama: https://ollama.com/library/gemma4:26b and https://ollama.com/library/gemma4:26b-a4b-it-q4_K_M
- LM Studio: https://lmstudio.ai/models/google/gemma-4-26b-a4b
- Cloudflare Workers AI: https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/ ("gemma-4-26b-a4b-it (Google) · Cloudflare AI docs")
- NVIDIA build page family reference: https://build.nvidia.com/minimaxai/minimax-m3/modelcard was for MiniMax, but analogous NVIDIA build pages exist for Gemma family (see Section 3/5).

### NVFP4-quantized sibling model — quality-drop bug report (NOTE: this is the 26B-A4B NVFP4 variant, a DIFFERENT model ID than our target gemma-4-31b-it-nvfp4, but same quantization family — logged here as directly relevant context)
- URL: https://github.com/sgl-project/sglang/issues/26518 — "[Bug] Gemma-4-26B-A4B NVFP4 quality drops"
- Quote: accuracy degradation traced to "the auto-selected `trtllm_mha` attention backend on SM100 (B200) costs **2.09pp MMLU** vs `triton` attention. The gap is statistically significant (McNemar χ² = 34.6 on N=14,042, p < 0.001)."
- Benchmark numbers (MMLU 5-shot, temperature=0, 57 subjects, N=14,042): triton attention baseline = 0.6238; trtllm_mha attention = 0.6029 (gap −2.09pp).
- Diagnosis quote: "the remaining ~1.31pp is in the attention output → router proj handoff (or a downstream interaction) that affects both NVFP4 MoE runners."
- Suggested fix (quote): "should the SM100 default for `Gemma4ForConditionalGeneration` + `modelopt_fp4` be switched to `--attention-backend triton` until the root cause is fixed?"
- Requires all three conditions per the reporter: NVFP4 quantization + MoE architecture + trtllm_mha backend.

---

## 5. gemma-4-31b-it-nvfp4

### Fireworks model page
- URL: https://fireworks.ai/models/fireworks/gemma-4-31b-it-nvfp4
- Context window: "262k tokens" (per fetch).
- Max output tokens / pricing: not specified on page per fetch.
- Description (quote): "NVIDIA 4-bit quantized variant of Google Gemma 4 31B Instruct for efficient inference."
- Fetch pass explicitly noted: "no explicit quality/speed tradeoff discussion appears in the content" on this particular Fireworks page — for that, see third-party sources below.

### Hugging Face variants (multiple repackagings found; existence confirmed via search, most not independently deep-fetched)
- Official NVIDIA repo: https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4
- Community repackagings: https://huggingface.co/prithivMLmods/gemma-4-31B-it-NVFP4 ; https://huggingface.co/CISCai/gemma-4-31B-it-NVFP4-turbo-GGUF ; https://huggingface.co/LilaRest/gemma-4-31B-it-NVFP4-turbo ; https://huggingface.co/RedHatAI/gemma-4-31B-it-NVFP4 ; https://huggingface.co/stevelikesrhino/gemma-4-31B-it-nvfp4-GGUF
- Paraphrase (from WebSearch synthesis of these listings): "Gemma-4-31B-it-NVFP4 is an NVFP4-compressed evolution of google/gemma-4-31B-it. This variant leverages F32, BF16, F8_E4M3, and U8 precision formats to significantly reduce memory footprint and improve inference efficiency while maintaining strong output quality... This optimization reduces the number of bits per parameter from 16 to 4, reducing the disk size and GPU memory requirements by approximately 75%."
- VRAM/cost estimate (Spheron GPU recommender, https://www.spheron.network/tools/gpu-recommender/nvidia/Gemma-4-31B-IT-NVFP4/, title: "Gemma-4-31B-IT-NVFP4 VRAM Requirements & Cheapest GPU to Run It from $0.53/hr"): paraphrase — "to run Gemma-4-31B-IT-NVFP4 for inference at FP16 you need roughly 45 GB of VRAM, with the cheapest fit being an L40S 48GB at about $0.61/hr" (note: the two dollar figures, $0.53/hr in the title vs $0.61/hr in the body summary, are inconsistent between the page title and the WebSearch-synthesized body text — logging both, not reconciled).
- Ollama: https://ollama.com/library/gemma4:31b-nvfp4 (existence only, title found via search).
- NVIDIA build page for base (non-quantized) model, for comparison: https://build.nvidia.com/google/gemma-4-31b-it

### Quantization architecture detail — attention layers NOT quantized
- Source: WebSearch synthesis citing NVIDIA's official NVFP4 checkpoint documentation (exact page URL not independently isolated beyond https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4 and https://kaitchup.substack.com/p/gemma-4-31b-quantization-comparison)
- Paraphrase: "NVIDIA's official 31B NVFP4 checkpoint excludes every self-attention layer from quantization, keeping attention weights in BF16, while only MLP layers are actually NVFP4. Quantizing self-attention weights to 4-bit FP4 hurts Gemma 4 accuracy more than quantizing MLP does."
- Accuracy claim (paraphrase): "NVIDIA's NVFP4 quantization of Gemma 4 31B achieves only 0.25% accuracy loss on GPQA Diamond." A separately-described "repackaged variant retains nearly identical quality with only 1-3% loss while being 68% smaller in GPU memory and ~2.5× faster than the base model" (source/repackager not specified in the synthesis — UNVERIFIED which specific HF repo this refers to).
- Paraphrase: "Variants with quantized attention layers score slightly below others, with the gap being especially noticeable on MMLU-Pro. However, there was no meaningful accuracy difference between NVIDIA's NVFP4 version and Red Hat AI's FP8 version" (i.e., RedHatAI/gemma-4-31B-it-NVFP4 vs. an FP8 competitor variant).

### Kaitchup quantization-comparison article (paywalled; free preview only)
- URL: https://kaitchup.substack.com/p/gemma-4-31b-quantization-comparison ("Gemma 4 31B Quantization Comparison: Best FP8, NVFP4, and INT4 Models")
- Quote: "None of the models appears broken, and all of them perform close to the original."
- Quote: "I did not observe a meaningful accuracy difference between NVIDIA's NVFP4 version and Red Hat AI's FP8 version."
- Paraphrase: models with quantized attention layers show slightly lower performance, "especially noticeable on MMLU-Pro."
- Paraphrase: the AutoRound (INT4) variant "performs worst" on average among the compared formats.
- **Token-efficiency-specific finding (quote)**: "quantization has little impact on token efficiency overall," with the note that Intel's INT4 variant "generating roughly 1.1× more tokens than the baseline across most tasks" — i.e., only a mild (~10%) verbosity increase from that specific INT4 repackaging, not from NVFP4 itself.
- Caveat: full benchmark numbers, throughput/speed comparisons, and format recommendations are behind the Kaitchup paywall; not retrievable in the free preview.

### theogravity GitHub repo — dual-GPU vLLM deployment benchmark (empirical numbers found, but NVFP4-only, no BF16 baseline comparison in this repo)
- URL: https://github.com/theogravity/dual-rtx-6000-blackwell-Gemma-4-31B-IT-NVFP4
- Repo description (quote): "Optimized vLLM setup for Gemma 4 31B NVFP4 with MTP on dual RTX PRO 6000 Blackwell using vllm and docker: native FP4 Tensor Cores, Multi-Token Prediction (96.5% acceptance rate), and prefix caching."
- Throughput (quotes): "552" tok/s with 4 speculative tokens; "654" tok/s with max-num-seqs=32.
- Latency (quotes): mean TTFT "4939ms" at spec=4; "3474ms" with max-num-seqs=32.
- Speculative decoding: "96.5%" acceptance rate at 4-token speculation, "4.86" mean acceptance length.
- Hardware-claim quote: "the format the hardware is designed to run at peak throughput" — "On Blackwell, NVFP4 GEMMs run at 2× the throughput of BF16" (explicitly flagged by the fetch as "a theoretical architectural advantage rather than an empirical comparison benchmark from this specific setup" — i.e., no side-by-side BF16 run was actually performed in this repo).
- Quality note (quote): KV-cache uses "uncalibrated scale=1.0 — verified acceptable quality for coding use" (no rigorous accuracy benchmark accompanying this claim in the repo).
- No direct NVFP4-vs-BF16 comparison benchmark was found in this specific repository.

### General NVFP4 background (not Gemma-specific — hardware/format-level facts)
- Source (WebSearch synthesis, multiple pages: Medium/Benjamin Marie "NVFP4: Same Accuracy with 2.3x Higher Throughput for 4-Bit LLMs" — https://medium.com/data-science-collective/nvfp4-same-accuracy-with-2-3x-higher-throughput-for-4-bit-llms-03518ecba108 ; NVIDIA research PDF "Quantization-Aware Distillation for NVFP4 Inference Accuracy Recovery" — https://research.nvidia.com/labs/nemotron/files/NVFP4-QAD-Report.pdf and https://arxiv.org/pdf/2601.20088 ; Spheron blog "NVFP4 vs MXFP4: 4-Bit Quantization Format Decision Guide" — https://www.spheron.network/blog/nvfp4-vs-mxfp4-gpu-cloud-4bit-quantization-guide/ ; Edge AI and Vision Alliance "NVIDIA Blackwell: The Impact of NVFP4 For LLM Inference" — https://www.edge-ai-vision.com/2025/10/nvidia-blackwell-the-impact-of-nvfp4-for-llm-inference/ ; Red Hat Developer "Accelerating large language models with NVFP4 quantization" — https://developers.redhat.com/articles/2026/02/04/accelerating-large-language-models-nvfp4-quantization ; NVIDIA "NVFP4 Quantization | DGX Spark" — https://build.nvidia.com/spark/nvfp4-quantization ; EmergentMind topic overview — https://www.emergentmind.com/topics/nvfp4-quantization-algorithm)
- Paraphrase: "NVFP4 models are 2.35x faster than INT4 models, thanks to Blackwell GPU acceleration for the NVFP4 data type."
- Paraphrase: "native FP4 computation in the prefill phase and enhanced memory efficiency during decode together achieved up to 2× higher throughput compared to A100 (Ampere), while accuracy degradation remained statistically insignificant."
- Paraphrase: "Blackwell's NVFP4 format achieves up to 2× higher efficiency while maintaining near-lossless accuracy compared to FP16/BF16 baselines."
- Paraphrase: NVFP4 "uses micro-block scaling, where values are grouped into blocks of 16, each sharing a high-precision FP8 (E4M3) scaling factor, plus an additional per-tensor FP32 scale" — with "2x more scale overhead compared to the OCP MXFP4 standard" but generally "better per-block accuracy... even controlling for block size" vs MXFP4.
- These are generic Blackwell/NVFP4-format claims, not benchmarked specifically against gemma-4-31b-it-nvfp4 in the sources found — logged as background/context only.

---

## Third-party / community discussion (verbosity, token efficiency) — all 5 models

### minimax-m3
- **Independent review**, thomas-wiegold.com, https://thomas-wiegold.com/blog/minimax-m3-review/ (fetched):
  - Quote: during a poker-simulation test, M3 "would talk itself into a corner, talk itself back out, and burn a frightening number of tokens doing it," with 30-40 minute processing times on a single task.
  - Quote (broader pattern, not M3-specific): "A lot of the newer models do this now. They over-think, second-guess, and treat token budgets like they're free."
  - Quote: on SWE-Bench Pro, M3 scores 59.0%, "behind Claude Opus 4.7 (64.3%) and GPT-5.5 (58.6%) by a hair."
  - Quote: "No filler, no padding, no inventing problems to look busy" — on a specific code-audit task, contradicting the poker-test verbosity finding (i.e., reviewer reports inconsistent verbosity depending on task type).
  - Quote (cost-efficiency caution): "if the model wanders through 40 minutes of self-doubt on a hard problem, your effective cost-per-task climbs."
- **Independent review**, andlukyane.com, https://andlukyane.com/blog/minimax-m3 (fetched):
  - Tasks: code audit/refactor of ~26k lines/~100 files, screenshot-based UI debugging, Spotify-history music recommendation.
  - Quote: M3 "did a large amount of correct, well-structured work quickly," raising test coverage from 188 to 237 tests.
  - Quote (critical limitation): independent review by "Opus 4.8 caught two critical regressions M3's own tests missed — schema validation conflicts and miscalculated critical hit chance multipliers" — i.e., a model that both writes fixes and tests "can be confidently wrong on both" (paraphrase).
  - Quote: without screenshots, M3 "kept guessing at event handlers and React state"; with them, it diagnosed a CSS namespace collision within fifteen minutes.
  - No explicit token counts given; paraphrase: M3 "spent roughly 30 minutes on the repository understanding and analysis."
  - Author's stated preference: "a separate reviewer in the loop for the parts I care about" rather than relying on M3's self-validation (paraphrase).
- **Cross-model verbosity comparison**, thinkwright.ai, https://thinkwright.ai/minimax-m3-vs-glm-5-2-coding-benchmark (fetched) — MiniMax M3 vs GLM 5.2 on coding tasks:
  - Correctness: GLM 5.2 "92% full-pass and a 0.976 mean score" vs MiniMax M3 "84% full-pass and a 0.961 mean score."
  - **Token counts (direct verbosity measurement)**: MiniMax M3 averaged "135,060" tokens per task vs GLM 5.2's "82,443" — i.e., roughly 64% more tokens for M3 on the same task set.
  - Latency: M3 "45 seconds per run" vs GLM 5.2 "80 seconds" (M3 faster despite more tokens generated, implying much higher throughput tok/s).
  - Cost: M3 "$6.67" vs GLM 5.2 "$18.47" for the scored runs (M3 ~2.8x cheaper in dollars despite the higher token count — reflecting Fireworks' cheaper per-token pricing tier for M3 vs. wherever GLM 5.2 was run).
- **Provider latency benchmark**, Telnyx, https://telnyx.com/resources/inference-minimax-m3-benchmark (fetched, vendor-authored so self-interested) — see Section 1 for full detail; key finding relevant to token/latency efficiency: Fireworks showed much higher tail latency variance than Telnyx/Together in this one benchmark (p95 54.06s / max 111.51s on Fireworks vs p95 14.72s / max 19.85s on Telnyx).
- **GitHub issues confirming reasoning-trace-as-output-tokens behavior** (directly relevant to the "thinking traces bill as output tokens" concern):
  - https://github.com/Kilo-Org/kilocode/issues/11203 (fetched) — reasoning content from M3 "appears inline as part of the normal response, not in a separate thinking/reasoning block" even when `"thinking": {"type": "adaptive"}` is explicitly set; also: MiniMax's API "rejects 'enabled' with a 400 error and only accepts 'adaptive' or 'disabled'" in this integration — contradicting the three-mode (`enabled`/`adaptive`/`disabled`) documentation found on GitHub/HF (Section 1), suggesting real-world API behavior may not match the published docs for at least one client/integration.
  - https://github.com/anomalyco/opencode/issues/31569 (fetched) — user reports thinking/reasoning output that was previously visible "no longer" appears, i.e., a behavior change over time in whether reasoning tokens are exposed/streamed at all; issue left open/unresolved at fetch time.

### kimi-k2p7-code
- (See Section 2 for the full HN thread detail.) Key restated points relevant to verbosity/efficiency:
  - Quote (HN user `DCKing`): "you'll spend many more tokens and will have to do more managing of the model" vs. Claude Sonnet, despite Kimi's lower sticker price per token.
  - Quote (HN user `kmike84`, paraphrase): Kimi requires prompts "much more precise" than Opus, "often resulting in higher token usage despite cheaper per-token pricing."
  - Quote (HN, second fetch pass of the same item): a commenter said "Kimi is in between...for me it brings back 'lazy prompting' workflow...but it is a bit worse everywhere. Smaller context, a bit more errors."
  - Quote: one developer "successfully used K2.7-Code to rebase a 177KB patch, estimating costs between '$5 and $10 in API usage.'"
  - Paraphrase: broader thread theme — cheaper Chinese models (Kimi, DeepSeek) pressure Anthropic to compete on experience, not just price; Claude's ecosystem retains stickiness via tooling.
  - Licensing note (paraphrase): "a modified MIT license with an attribution requirement similar to older BSD licenses, asking users to 'advertise' the model in their products."
  - Confirmed structurally (Section 2): thinking mode is **mandatory** and cannot be disabled ("Kimi-K2.7-Code forces thinking and preserve_thinking as True" — direct model-card quote) — meaning 100% of K2.7-Code's reasoning tokens are unavoidable output-token cost on every call, with only the claimed ~30% reduction vs. K2.6 as the efficiency lever, not a not-thinking mode.

### gemma-4 family (31b-it, 26b-a4b-it, and thinking-mode behavior applies across variants)
- **"Why Gemma 4 Overthinks" article** — https://openllmbridge.com/blog/why-gemma-4-overthinks (title: "Why Gemma 4 Overthinks — and How to Make It Shut Up Faster on Local Ollama") — NOTE: direct WebFetch of this URL returned HTTP 403 Forbidden; the following is from the WebSearch tool's own synthesis/snippet of the page, not an independently re-verified verbatim pull — flagging as lower-confidence paraphrase:
  - Paraphrase: "Overthinking isn't a bug — it's the visible side of three deliberate design choices interacting badly with each other. Reasoning-heavy post-training rewards models that 'show their work'... the same RL signal that makes Gemma 4 a strong reasoner on AIME also makes it narrate its way through simple questions."
  - Example cited (paraphrase): Gemma 4 producing internal monologue explaining "Australia's capital with historical context before arriving at a one-word answer — that's 60 tokens of internal monologue for a one-word answer."
  - Paraphrase: "When a long system prompt is used with Gemma4 or when the conversation gets long, it starts answering without doing proper reasoning" (inconsistent behavior); also, telling Gemma4 to be "'taciturn and speak only briefly'... it starts talking more and more with each turn" (counter-intuitive prompt-following failure reported by users).
  - Paraphrase: "Gemma 4 follows instructions well — the problem is it has no instruction by default, so it falls back to its training prior, which is verbose."
- **Japanese-language blog**, note.com, https://note.com/dkvingway/n/n4a0b2534fcab?hl=en — title (verbatim, English-translated by the site): "Dealing with Gemma4's tendency to skip thinking and produce overly long responses" (title only; page content not independently fetched).
- **llama.cpp GitHub discussion**, https://github.com/ggml-org/llama.cpp/discussions/21338, "Can't disable thinking in gemma4 (26b-a4b)" (fetched):
  - Failed attempts (quote-adjacent): `--reasoning-budget 0` and `--chat-template-kwargs '{"enable_thinking":false}'` both "resulted in continued 'thinking' output appearing in responses."
  - Self-found workaround (quote): `"--reasoning off...seems to help"`.
  - Quantization-dependent bug (quote): "quantized GGUF works correctly on both CUDA and Vulkan, while F16 fails on CUDA with Thinking ON."
  - Later reports (paraphrase): ongoing problems with Gemma4 variants including the 31B, with `<unused49>` token floods not fully resolved by the workarounds — "reflecting design fragmentation across different model implementations" (paraphrase of the fetch's own summary framing).
  - Speed note (paraphrase): `--reasoning off` gave "approximately 5x speed improvement on recent builds" for some users.
- **Google AI Developer Forum**, https://discuss.ai.google.dev/t/disable-thinking-for-gemma-4/138885, "Disable thinking for Gemma 4" (fetched):
  - Community-recommended method (quote): `"thinkingConfig": {"thinkingLevel": "MINIMAL"}` — one user noted "I agree there is no thoughtsTokenCount fields being returned" after applying this.
  - Quote: "'thinking' is activated by adding the `<|think|>` token to the beginning of the system prompt. To turn it off, simply remove that token" — but "later responses clarified this may not fully disable the feature."
  - Quote: `"include_thoughts": false` parameter "returned errors, indicating it's not a valid field."
  - Paraphrase: "the absence of a 'NONE' option" leaves ambiguity about whether `MINIMAL` truly disables thinking or merely reduces it; client-side regex/string-parsing to strip `<thought>...</thought>`-style tags was suggested as a fallback.
- **GoPenAI/Medium blog**, https://blog.gopenai.com/gemma-4-disabling-thinking-with-gemma-4-26b-a4b-it-9e8473df38d6 (fetched via redirect):
  - Quote: "System prompt says no thinking — reasoning is still enabled" (i.e., system-prompt-only instruction is unreliable).
  - Quote: "You have to indicate in both the system and the user prompt that you don't want reasoning before it becomes reliable."
  - Quote: a `"<no thought>"` tag "seems to have some resonance with the model" as a partial workaround.
  - Paraphrase: reasoning is "internally trained and controlled," and hard questions may trigger reasoning despite explicit instructions to disable it.
  - Article does not discuss quantitative token-usage/output-length impact of thinking-on vs thinking-off.
- **HF discussion**, https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/discussions/6, "How to enable thinking" — notes model uses `<thought>` tags (not `<thinking>`), and that "in multi-turn conversations, the historical model output should only include the final response" (paraphrase, overlaps with the official HF model-card note in Section 4).
- **Kaitchup Substack** (quantitative, cross-model): https://kaitchup.substack.com/p/gemma-4-31b-vs-qwen35-27b-inference — Gemma 4 31B "rarely generates more than 20k tokens" vs Qwen3.5 27B which "often overthinks and can exceed 100k tokens" (see Section 3 — this is a rare quantitative verbosity data point, and it is comparatively favorable to Gemma 4 31B versus at least one other reasoning model family, not one of our 5 target models though).
- **Net effect for this collection**: multiple independent sources (llama.cpp discussion, Google AI forum, GoPenAI blog, HF model card) agree there is NO single, universally-reliable API parameter to fully suppress Gemma-4-family thinking/reasoning-token output across all serving stacks — methods that reportedly work in some stacks (`enable_thinking=False` in `apply_chat_template`, `reasoning_effort:"none"` on `/v1/chat/completions`, `thinkingConfig.thinkingLevel="MINIMAL"`, removing the `<|think|>` token, `--reasoning off` in llama.cpp) are reported elsewhere as ineffective, backend-specific, or only partially effective (see the `/v1/responses` vs `/v1/chat/completions` `reasoning_effort` inconsistency noted via WebSearch of https://github.com/ollama/ollama/issues/15635, and the empty-content bug at https://github.com/ml-explore/mlx-lm/issues/1352 "Gemma 4 with thinking enabled produces only reasoning field, content is empty in API response" — both titles/summaries only, not independently deep-fetched).

---

## Sources (raw list, all URLs visited)

Directly fetched via WebFetch (full-page pass):
- https://fireworks.ai/models/fireworks/minimax-m3
- https://fireworks.ai/blog/minimax-m3-launch
- https://www.requesty.ai/models/fireworks/minimax-m3
- https://telnyx.com/resources/inference-minimax-m3-benchmark
- https://github.com/MiniMax-AI/MiniMax-M3
- https://huggingface.co/MiniMaxAI/MiniMax-M3
- https://github.com/Kilo-Org/kilocode/issues/11203
- https://github.com/anomalyco/opencode/issues/31569
- https://www.marktechpost.com/2026/06/12/moonshot-ai-releases-kimi-k2-7-code-a-coding-model-reporting-21-8-on-kimi-code-bench-v2-over-k2-6/
- https://devops.com/moonshot-ais-kimi-k2-7-code-targets-token-efficiency-in-agentic-coding/
- https://fireworks.ai/models/fireworks/gemma-4-31b-it
- https://fireworks.ai/models/fireworks/gemma-4-31b-it-nvfp4
- https://deepmind.google/models/gemma/gemma-4/
- https://ai.google.dev/gemma/docs/core
- https://github.com/ggml-org/llama.cpp/discussions/21338
- https://discuss.ai.google.dev/t/disable-thinking-for-gemma-4/138885
- https://docs.fireworks.ai/serverless/pricing
- https://docs.fireworks.ai/getting-started/models (fetched; none of our 5 target model IDs were found listed on this particular page)
- https://hn.algolia.com/api/v1/search?query=MiniMax%20M3
- https://hn.algolia.com/api/v1/search?query=Kimi%20K2.7
- https://hn.algolia.com/api/v1/search?query=Gemma%204
- https://hn.algolia.com/api/v1/search?query=Kimi%20K2.7-Code%20token%20efficiency&tags=story
- https://news.ycombinator.com/item?id=48502347 (fetched twice, second pass for additional comment detail)
- https://andlukyane.com/blog/minimax-m3
- https://blog.gopenai.com/gemma-4-disabling-thinking-with-gemma-4-26b-a4b-it-9e8473df38d6 (via two redirect hops through medium.com/m/global-identity-2)
- https://huggingface.co/moonshotai/Kimi-K2.7-Code
- https://thinkwright.ai/minimax-m3-vs-glm-5-2-coding-benchmark
- https://fireworks.ai/blog/kimi-k2p7-code
- https://huggingface.co/google/gemma-4-26B-A4B-it
- https://fireworks.ai/pricing
- https://openrouter.ai/google/gemma-4-26b-a4b-it
- https://automatio.ai/models/kimi-k2-7-code
- https://thomas-wiegold.com/blog/minimax-m3-review/
- https://github.com/theogravity/dual-rtx-6000-blackwell-Gemma-4-31B-IT-NVFP4
- https://kaitchup.substack.com/p/gemma-4-31b-quantization-comparison (paywalled, partial)
- https://github.com/sgl-project/sglang/issues/26518
- https://kaitchup.substack.com/p/gemma-4-31b-vs-qwen35-27b-inference (paywalled, partial)
- https://openllmbridge.com/blog/why-gemma-4-overthinks (returned HTTP 403; content below came from WebSearch's own snippet/synthesis instead, not a successful direct fetch)
- Attempted, returned HTTP 500 (no content retrieved): https://www.requesty.ai/models/fireworks/gemma-4-31b-it , https://www.requesty.ai/models/fireworks/gemma-4-31b-it-nvfp4 , https://www.requesty.ai/models/fireworks/gemma-4-26b-a4b-it

Surfaced via WebSearch (result links reviewed; some facts cited above came from the search tool's own synthesis of these pages rather than an independent WebFetch — flagged inline where used):
- https://fireworks.ai/models/fireworks/gemma-4-26b-a4b-it
- https://www.tipranks.com/news/private-companies/fireworks-ai-expands-model-portfolio-with-cost-focused-minimax-m3-integration
- https://x.com/FireworksAI_HQ/status/2065488511265013786
- https://digg.com/tech/a8ckwh19
- https://x.com/ericvishria/status/2065482787579420773
- https://x.com/SkylerMiao7/status/2059285750458544561 (as referenced via HN Algolia listing)
- https://twitter.com/MiniMax_AI/status/2061266317815296322
- https://huggingface.co/MiniMaxAI/MiniMax-M2.7/discussions/33
- https://openrouter.ai/minimax/minimax-m3
- https://github.com/cline/cline/issues/11553
- https://github.com/cline/cline/pull/11554
- https://pi.dev/models/fireworks/accounts-fireworks-routers-kimi-k2p7-code-fast
- https://github.com/nicobailon/pi-subagents/issues/325
- https://mastra.ai/models/providers/fireworks-ai
- https://www.linkedin.com/posts/rwfiii_kimi-k27-code-on-fireworks-better-agents-activity-7471730437120253952-YCxT
- https://fireworks.ai/models/fireworks/kimi-k2p6
- https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4
- https://build.nvidia.com/google/gemma-4-31b-it
- https://dev.to/aniruddhaadak/gemma-4-complete-guide-2026-architecture-benchmarks-deployment-3en9
- https://huggingface.co/google/gemma-4-31B
- https://fireworks.ai/models/fireworks/gemma-3-4b-it
- https://huggingface.co/google/gemma-4-31B-it
- https://openrouter.ai/google/gemma-4-26b-a4b-it:free
- https://ollama.com/library/gemma4:26b
- https://lmstudio.ai/models/google/gemma-4-26b-a4b
- https://developers.cloudflare.com/workers-ai/models/gemma-4-26b-a4b-it/
- https://ollama.com/library/gemma4:26b-a4b-it-q4_K_M
- https://prithivMLmods (see https://huggingface.co/prithivMLmods/gemma-4-31B-it-NVFP4)
- https://huggingface.co/CISCai/gemma-4-31B-it-NVFP4-turbo-GGUF
- https://huggingface.co/LilaRest/gemma-4-31B-it-NVFP4-turbo
- https://www.spheron.network/tools/gpu-recommender/nvidia/Gemma-4-31B-IT-NVFP4/
- https://ollama.com/library/gemma4:31b-nvfp4
- https://huggingface.co/RedHatAI/gemma-4-31B-it-NVFP4
- https://huggingface.co/stevelikesrhino/gemma-4-31B-it-nvfp4-GGUF
- https://github.com/MiniMax-AI/MiniMax-M2/issues/52
- https://github.com/HKUDS/nanobot/issues/3068
- https://docs.openclaw.ai/tools/thinking
- https://medium.com/@sampan090611/minimax-m1-the-understated-powerhouse-redefining-attention-in-ai-yet-craving-yours-48a319506f0f
- https://venturebeat.com/ai/minimax-m1-is-a-new-open-source-model-with-1-million-token-context-and-new-hyper-efficient-reinforcement-learning
- https://github.com/MiniMax-AI/MiniMax-M1
- https://huggingface.co/nvidia/MiniMax-M3-NVFP4
- https://build.nvidia.com/minimaxai/minimax-m3/modelcard
- https://huggingface.co/MiniMaxAI (collection page)
- https://huggingface.co/MiniMaxAI/MiniMax-M3-MXFP8
- https://arxiv.org/pdf/2506.13585 (MiniMax-M1 paper)
- https://arxiv.org/pdf/2605.26494 (MiniMax-M2 Series paper)
- https://huggingface.co/papers/2606.13392 and https://arxiv.org/abs/2606.13473 / https://arxiv.org/abs/2606.13473v1 (MiniMax Sparse Attention paper — objectID 2606.13392 confirmed as the MSA paper per WebSearch synthesis; note arxiv ID 2606.13473 that appeared in the same search result set is a different, unrelated paper "MaxProof: Scaling Mathematical Proof...")
- https://automatio.ai/models/kimi-k2-7-code (also fetched directly, listed above)
- https://www.requesty.ai/models/moonshot/kimi-k2.7-code
- https://www.spheron.network/blog/deploy-kimi-k2-7-code-gpu-cloud/
- https://codersera.com/blog/kimi-k2-7-complete-guide-2026/
- https://flowtivity.ai/blog/kimi-k2-7-complete-review/
- https://openrouter.ai/moonshotai/kimi-k2.7-code
- https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot/
- https://twitter.com/Kimi_Moonshot/status/2065377579130142937
- https://www.kimi.com/resources/kimi-k2-7-code
- https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart
- https://webscraft.org/blog/reasoning-mode-v-gemma-4-yak-vmikati-koli-potribno-i-skilki-koshtuye-2026?lang=en
- https://github.com/ollama/ollama/issues/15635
- https://github.com/ml-explore/mlx-lm/issues/1352
- https://dev.to/pulkitgovrani/gemma-4s-thinking-mode-a-practical-guide-to-the-think-token-8c5
- https://www.gemma4.wiki/benchmark/gemma-4-gsm8k-score
- https://kartit.net/blog/gemma4-local-benchmark.html
- https://www.aimadetools.com/blog/gemma-4-family-guide/
- https://gemma4-ai.com/blog/gemma4-benchmark
- https://medium.com/techtrends-digest/heres-a-tighter-benchmark-focused-blog-post-501c5ea829f4
- https://gemmai4.com/benchmark/
- https://gemma4-ai.com/blog/gemma4-which-model
- https://arxiv.org/pdf/2408.00118 (Gemma 2 paper — surfaced but not about Gemma 4; noted for completeness only)
- https://pricepertoken.com/endpoints/fireworks/free
- https://pricepertoken.com/endpoints/fireworks
- https://www.modern-datatools.com/tools/fireworks-ai/pricing
- https://costbench.com/software/llm-api-providers/fireworks-ai/
- https://www.morphllm.com/fireworks-alternative
- https://www.spheron.network/blog/fireworks-ai-alternatives/
- https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/announcing-fireworks-ai-on-microsoft-foundry/4500950
- https://medium.com/data-science-collective/nvfp4-same-accuracy-with-2-3x-higher-throughput-for-4-bit-llms-03518ecba108
- https://research.nvidia.com/labs/nemotron/files/NVFP4-QAD-Report.pdf
- https://www.spheron.network/blog/nvfp4-vs-mxfp4-gpu-cloud-4bit-quantization-guide/
- https://www.edge-ai-vision.com/2025/10/nvidia-blackwell-the-impact-of-nvfp4-for-llm-inference/
- https://developers.redhat.com/articles/2026/02/04/accelerating-large-language-models-nvfp4-quantization
- https://build.nvidia.com/spark/nvfp4-quantization
- https://www.emergentmind.com/topics/nvfp4-quantization-algorithm
- https://arxiv.org/pdf/2601.20088 (Quantization-Aware Distillation for NVFP4)
- https://note.com/dkvingway/n/n4a0b2534fcab?hl=en
- https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- https://merchmindai.net/blog/en/post/google-gemma-4-open-models-guide
- https://ollama.com/library/gemma4
- https://www.interconnects.ai/p/gemma-4-and-what-makes-an-open-model
- https://officechai.com/ai/google-releases-gemma-4-open-models-calls-them-best-in-world-in-their-category/
- https://blog.google/innovation-and-ai/technology/developers-tools/introducing-gemma-4-12b/
- https://apps.apple.com/nl/app/google-ai-edge-gallery/id6749645337
- https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/
- https://blog.simbastack.com/indexed-a-year-of-video-locally/
- https://ai.georgeliu.com/p/running-google-gemma-4-locally-with
- https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/
- https://gist.github.com/greenstevester/fc49b4e60a4fef9effc79066c1033ae5
- https://www.gizmoweek.com/gemma-4-runs-iphone/
- https://blog.danielvaughan.com/i-ran-gemma-4-as-a-local-model-in-codex-cli-7fda754dc0d4
- https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF/discussions/6
- https://huggingface.co/google/gemma-4-26B-A4B (base, non-"-it" repo)
- https://allenkuo.medium.com/finishing-what-we-started-gemma-4-nvfp4-on-vllm-desktop-blackwell-wsl2-b2088c34815a
- https://blog.pebblous.ai/story/google-gemma-4-nvfp4-report-pb/en/

Note on search-tool provenance: several bullets above are explicitly marked "(paraphrase from WebSearch synthesis)" or "(via WebSearch, not independently re-fetched)" in the body sections — this Sources list includes those pages because they were genuinely returned by a live web search and their content (as summarized by the search tool) was used, but the exact wording should be treated as lower-confidence than a direct WebFetch quote. No URL, benchmark number, or fact in this document was invented; anything not traceable to a real search result or fetched page was marked UNVERIFIED inline instead of being stated as fact.
