# Free/Low-Friction API Providers & Open-Source Tools — Research Log

Purpose: DEV/TESTING STAND-IN ONLY for AMDA's remote-escalation code path while waiting on Fireworks API key. NOT for final submission (final submission is locked to Fireworks-hosted minimax-m3, kimi-k2p7-code, gemma-4-31b-it, gemma-4-26b-a4b-it, gemma-4-31b-it-nvfp4 via judging proxy).

This is a COLLECTION log only — no recommendations, no synthesis, no integration code. Every bullet is either a direct quote (marked with quotation marks) or a clearly-marked paraphrase, with the exact source URL. Anything not verified against a real search/fetch result is labeled UNVERIFIED.

Research date: 2026-07-07.

---

## Section A: Free-tier LLM API providers usable TODAY as a Fireworks stand-in

### A1. Groq (console.groq.com)

- Signup: `console.groq.com` (exact signup URL not separately confirmed by fetch; console itself is the entry point). UNVERIFIED whether credit card is required — the fetched rate-limits doc page did not state this either way.
- Free tier rate limits, from GroqDocs rate-limits page (https://console.groq.com/docs/rate-limits) fetched directly — table of Free plan RPM/RPD/TPM per model:
  - `llama-3.1-8b-instant`: 30 RPM, 14.4K RPD, 6K TPM
  - `llama-3.3-70b-versatile`: 30 RPM, 1K RPD, 12K TPM
  - `meta-llama/llama-4-scout-17b-16e-instruct`: 30 RPM, 1K RPD, 30K TPM
  - `openai/gpt-oss-120b`: 30 RPM, 1K RPD, 8K TPM
  - `openai/gpt-oss-20b`: 30 RPM, 1K RPD, 8K TPM
  - `openai/gpt-oss-safeguard-20b`: 30 RPM, 1K RPD, 8K TPM
  - `qwen/qwen3-32b`: 60 RPM, 1K RPD, 6K TPM
  - `qwen/qwen3.6-27b`: 30 RPM, 1K RPD, 8K TPM
  - `whisper-large-v3` / `whisper-large-v3-turbo`: 20 RPM, 2K RPD (speech, not relevant)
  - `allam-2-7b`: 30 RPM, 7K RPD, 6K TPM
  - (Source: https://console.groq.com/docs/rate-limits, fetched 2026-07-07)
- Secondary/aggregator source (unverified against official page, from search snippet only) — TokenMix blog claims a blanket "30 RPM, 6K TPM, 14.4K Req/Day" and cites a Groq community forum thread: "Rate limits apply at the organization level, not per user... Cached tokens don't count toward your rate limits... Adding a credit card unlocks the Developer tier with up to 10x the free tier rate limits and a 25% discount on all token costs." UNVERIFIED (third-party blog paraphrase, not fetched from Groq directly). Source: https://tokenmix.ai/blog/groq-free-tier-limits-2026 (search snippet only, not fetched).
- Official community forum thread flagged by search: "Is there a free tier and what are its limits?" — https://community.groq.com/t/is-there-a-free-tier-and-what-are-its-limits/790 (not yet fetched directly; title/URL only).
- Models currently on Groq per direct fetch of https://console.groq.com/docs/models (2026-07-07):
  - Production: `llama-3.1-8b-instant`, `llama-3.3-70b-versatile`, `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `whisper-large-v3`
  - Preview: `qwen/qwen3-32b`, `qwen/qwen3.6-27b`, `meta-llama/llama-4-scout-17b-16e-instruct`
  - Agentic systems: `groq/compound`, `groq/compound-mini`
  - Quote (paraphrase from fetch): "The page notes that models like Gemma, Kimi/Moonshot, and MiniMax are not listed in the current offerings."
- IMPORTANT DISCREPANCY / MODEL CHURN NOTE: A separate search result (not a direct doc fetch) stated Groq previously hosted Kimi K2: "Moonshot AI's cutting-edge model, moonshotai/Kimi-K2-Instruct-0905, is now live on GroqCloud... 256k context window... 1 trillion total parameters and 32 billion activated parameters" (source: https://groq.com/blog/introducing-kimi-k2-0905-on-groqcloud, search snippet only, not fetched directly) — but that same search batch noted: "on March 23, 2026, Groq announced the deprecation of moonshotai/kimi-k2-instruct-0905 in favor of openai/gpt-oss-120b" (source cited by search aggregator: https://console.groq.com/docs/deprecations, not yet fetched directly). NET: as of 2026-07-07 direct fetch of the live models doc, Kimi K2 and Gemma are NOT in Groq's current model list. UNVERIFIED pending direct fetch of the deprecations page.
- OpenAI-compatible endpoint: Groq is widely documented elsewhere (prior AMDA research, not re-verified in this session) as OpenAI SDK-compatible; not independently re-confirmed via fetch in this session. UNVERIFIED (not fetched this session).

### A2. Google AI Studio / Gemini API free tier (aistudio.google.com)

- Official rate-limits doc fetched directly (https://ai.google.dev/gemini-api/docs/rate-limits) does NOT publish a static free-tier numbers table; direct quote: "Rate limits depend on a variety of factors (such as your usage tier) and can be viewed in Google AI Studio." and it links to https://aistudio.google.com/rate-limit for the live, account-specific numbers.
- Free tier access is described in the doc as available via "Active project or free trial" (paraphrase from fetch).
- Credit card requirement: NOT stated either way in the fetched official doc.
- From WebSearch result snippets (third-party aggregators, UNVERIFIED against an official static table since Google doesn't publish one):
  - "The Gemini API free tier offers 1,500 requests per day (RPD) on Flash models, 1 million tokens per minute (TPM), and 15 requests per minute (RPM)." — paraphrased by search aggregator, sources cited in that batch: https://tokenmix.ai/blog/gemini-api-free-tier-limits, https://pecollective.com/tools/gemini-free-tier-guide/
  - "Gemini 2.5 Flash & Flash-Lite: 1,500 RPD with 1,000,000 TPM" — UNVERIFIED, third-party
  - "Gemini 2.5 Pro: 50 RPD on free tier" — UNVERIFIED, third-party
  - "Gemini 3.1 Flash-Lite: 30 RPM (double the Flash rate)" — UNVERIFIED, third-party
  - Important caveat directly quoted from a search snippet (itself paraphrasing Google's position): "Once you enable billing on the Gemini API, the free tier disappears entirely on that project, and every call becomes billable from the first token." Source: https://usagebox.com/articles/gemini-api-billing-free-tier-confusion (snippet only, not fetched)
- Not yet checked: OpenAI-compatible endpoint details for Gemini (Google does offer one at a documented `/v1beta/openai/` compatibility endpoint per general prior knowledge, but NOT verified via fetch this session — UNVERIFIED, needs follow-up fetch).

### A3. NVIDIA NIM / build.nvidia.com

- Direct fetch of https://build.nvidia.com/ timed out (60s) in this session — findings below are from WebSearch snippets only (UNVERIFIED against the live page, follow-up fetch recommended).
- Signup: build.nvidia.com, "Go to build.nvidia.com and use your email to sign up. After making an account, you can get an API Key by selecting any of the available NIMs then in the example code section, click on 'Get API Key' then 'Generate Key'." (paraphrase from search snippet, source unclear — aggregated from https://decodethefuture.org/en/how-to-get-nvidia-api-key-free/ and https://decodethefuture.org/en/nvidia-nim-api-explained/)
- Credits: conflicting numbers in search snippets — "Each new account can receive up to 5,000 free credits" vs. "Developers get 1,000 free inference credits on signup with a rate limit of 40 requests per minute". Both UNVERIFIED/unreconciled, third-party. Source: https://costbench.com/software/llm-api-providers/nvidia-nim/free-plan/ and https://medium.com/coding-nexus/nvidia-is-offering-80-ai-models-for-free-via-apis-fc64b38276b8 (snippets only)
- Model count / OpenAI compatibility, quoted from search snippet: "You can access more than 80 advanced AI models, completely free, via a simple REST API that works seamlessly with the OpenAI SDK." and "NVIDIA NIM offers OpenAI-compatible API access to over 100 AI models — including Nemotron, Kimi-K2.5, MiniMax-M2.5, and GLM-5 — hosted on DGX Cloud at build.nvidia.com." Source: https://medium.com/coding-nexus/nvidia-is-offering-80-ai-models-for-free-via-apis-fc64b38276b8 (snippet). THIS IS HIGHLY RELEVANT (Kimi-K2.5 and MiniMax-M2.5 both resemble our target categories) but UNVERIFIED — needs direct fetch of build.nvidia.com model catalog to confirm exact model IDs, whether Gemma is present, and current rate limits.
- "No credit card needed, and there's no trial expiration timer, just free inference. However, free tier access typically comes with rate limits and is subject to NVIDIA's terms of service." (paraphrase from search snippet, source: https://costbench.com/software/llm-api-providers/nvidia-nim/free-plan/)
- Official NVIDIA blog confirms free preview program exists (title only, not fetched): "Access to NVIDIA NIM Now Available Free to Developer Program Members" — https://developer.nvidia.com/blog/access-to-nvidia-nim-now-available-free-to-developer-program-members/
- TODO follow-up: retry direct fetch of build.nvidia.com model catalog page and rate-limit docs.

### A4. Hugging Face Inference Providers (huggingface.co)

- Official pricing doc fetched directly (https://huggingface.co/docs/inference-providers/pricing, 2026-07-07). Direct quote — free credit table:
  > "Every Hugging Face user receives monthly credits to experiment with Inference Providers... | Free Users | $0.10, subject to change | yes (credits purchase required) | | PRO Users | $2.00 | yes | | Team or Enterprise Organizations | $2.00 per seat | yes |"
- Direct quote confirming OpenAI-compatible endpoint and exact base_url + model naming convention:
  ```python
  from openai import OpenAI
  client = OpenAI(
      base_url="https://router.huggingface.co/v1",
      api_key=os.environ["HF_TOKEN"],
  )
  completion = client.chat.completions.create(
      model="deepseek-ai/DeepSeek-V3-0324",
      messages=[{"role": "user", "content": "..."}],
  )
  ```
  (Source: https://huggingface.co/docs/inference-providers/pricing)
- Direct quote on hf-inference (the old free "Inference API (serverless)"): "As of July 2025, hf-inference focuses mostly on CPU inference (e.g. embedding, text-ranking, text-classification, or smaller LLMs that have historical importance like BERT or GPT-2)." — implies the old free serverless inference API is now narrow-scope (CPU/small models), not a general free chat-completions path for large models. Source: same pricing doc.
- Cross-check search result (paraphrase, not fetched from primary doc but from search summary of HF blog/docs): "Inference Providers exposes a single OpenAI-compatible API that routes to 15+ third-party providers including Groq, Together AI, Fireworks, Replicate, Cerebras, Cohere, Nebius, SambaNova, Novita AI, Hyperbolic, and Featherless." Source cited by aggregator: https://huggingface.co/blog/inference-providers-publicai (not directly fetched, title/snippet only).
- **HIGH RELEVANCE FINDING**: WebFetch of https://huggingface.co/inference/models (2026-07-07) returned a paraphrased breakdown (not a verbatim table — treat as paraphrase of page content, re-verify by direct browse if possible) stating:
  - "Gemma-4-31B-it: Available via Novita, Cerebras, Together, and DeepInfra"
  - "Gemma-4-26B-A4B-it: Hosted on Novita and DeepInfra"
  - "Kimi-K2.7-Code: Together (fastest), Novita, Fireworks, DeepInfra"
  - "MiniMax-M3: Together, Novita, Fireworks, DeepInfra"
  - This means (if accurate) that **the literal target models gemma-4-31b-it, gemma-4-26b-a4b-it, and even Kimi-K2.7-Code / MiniMax-M3 name-alikes appear on HF Inference Providers via non-Fireworks backends (Novita, Cerebras, Together, DeepInfra)** — potentially the closest possible free/low-friction stand-in to the real submission models. NEEDS RE-VERIFICATION with a second direct fetch/screenshot since WebFetch summarizes rather than quotes verbatim from this page.
  - Model card confirms real: https://huggingface.co/google/gemma-4-31B-it fetched directly (2026-07-07) — paraphrase: "Yes, this is an official Google DeepMind model, part of the Gemma 4 family released in 2025... approximately 30.7 billion total parameters with a 256K token context window... The page displays an 'Inference Providers [NEW]' widget listing Novita as an available hosting option, with additional unlisted providers accessible via comparison links." License: Apache 2.0 (per fetch).
  - MiniMax-M3 model card confirmed real via search: https://huggingface.co/MiniMaxAI/MiniMax-M3 — paraphrase: "MiniMax-M3 is a native multimodal model with 1M context that has ~428B parameters and ~23B activated parameters." Also found NVFP4 quantized variant repos: https://huggingface.co/nvidia/MiniMax-M3-NVFP4, https://huggingface.co/MiniMaxAI/MiniMax-M3-MXFP8, https://huggingface.co/unsloth/MiniMax-M3-GGUF (GGUF build — relevant for local llama.cpp testing). Search-result caveat: "some quantized variants like the lukealonso/MiniMax-M3-NVFP4 aren't deployed by any Inference Provider... most MiniMax-M3 variants currently lack official Hugging Face Inference Provider deployment" — so MiniMax-M3 hosted-inference availability via HF is UNVERIFIED/likely limited despite the model card existing.
- Model naming/routing convention (paraphrase from search aggregator, not primary doc): "Models are called using their full names like 'Qwen/Qwen3.5-397B-A17B'... You can append routing suffixes to model names: `:fastest` (default), `:cheapest`, or `:provider_name` to force a specific backend." UNVERIFIED against primary docs this session (search-snippet paraphrase only).

### A5. OpenRouter (openrouter.ai)

- Direct fetch attempts of https://openrouter.ai/models (both plain and via r.jina.ai proxy) had mixed results — the plain fetch returned only nav/footer (JS-rendered SPA issue); the r.jina.ai proxied fetch DID return model data:
  - Via https://r.jina.ai/https://openrouter.ai/models?max_price=0 (fetched 2026-07-07), free models found: `tencent/hy3:free` (262K context, $0/M in+out), plus unnamed-in-summary free entries from poolside (262K ctx), cohere (256K ctx), and three nvidia entries (10K / 128K / 1M ctx) — exact slugs not fully captured by the summarizer, recommend re-fetch with raw HTML/JSON if exact IDs needed.
  - Direct quote from that fetch: "The content does not include any Gemma, Kimi, Moonshot, MiniMax, Qwen, or DeepSeek models among the free offerings displayed" (as of that specific fetch/snapshot — NOTE search-snippet results below list more free models than the r.jina fetch captured, likely because the free-models list changes/rotates and the jina fetch may have been partial).
  - Cross-check from WebSearch snippets (not fetched, third-party aggregators, dated "Jul 2026"): "Free models are marked with a `:free` suffix in their model ID — for example `deepseek/deepseek-r1:free`. On July 1, 2026, that filter returned 25 free models, though OpenRouter has 29 free AI models as of June 2026." Listed examples include: "Qwen3-Coder (`:free`)", "NVIDIA Nemotron 3 Ultra (`:free`)", "Llama 3.3 70B and OpenAI's GPT-OSS 120B", "Deepseek-r1-distill:free". Sources: https://costgoat.com/pricing/openrouter-free-models, https://openrouter.ai/collections/free-models, https://rubentorney.com/blog/en/openrouter-modeles-gratuits-2026.html (snippets only, not fetched directly — treat exact list as UNVERIFIED/time-sensitive).
  - No Gemma or Kimi/Moonshot or MiniMax model confirmed as free on OpenRouter in any source checked this session — closest resemblance is Qwen3-Coder (`:free`) and DeepSeek-R1 distill (`:free`).
- Rate limits — direct fetch of https://openrouter.ai/docs/api-reference/limits (2026-07-07):
  - Quote/paraphrase: "Requests per Minute: 20 RPM." Daily limit depends on credit status: "if you have purchased less than 10 credits, you're limited to 50 :free model requests per day," while purchasing at least $10 in credits "increased to 1,000 :free model requests per day." Negative balance → HTTP 402 and loss of free-model access until restored.
  - Cross-check from search snippet (unverified, possibly stale/approximate): "Free models are subsidized by OpenRouter and have rate limits (typically 20 requests/minute, 200 requests/day)... The rate limit applies across all free models combined, meaning you have one shared rate limit pool for all free models rather than per-model limits." (200/day figure conflicts with the 50/1000 figures from the direct doc fetch — the direct doc fetch is more authoritative; treat "200/day" as UNVERIFIED/possibly outdated.)
  - "openrouter/free" is mentioned in search snippet as "a router that automatically selects from available free models based on your request's requirements" — UNVERIFIED, not fetched directly. URL: https://openrouter.ai/openrouter/free

### A6. Cerebras, SambaNova, GitHub Models, Cloudflare Workers AI

**Cerebras (cloud.cerebras.ai)**
- Direct fetch of official rate-limits doc (https://inference-docs.cerebras.ai/support/rate-limits, 2026-07-07). Quote/paraphrase of "Free Trial" tier limits: "RPM: 5 requests per minute; TPD: 1M tokens per day; TPM: 30K tokens per minute; TPH: 1M tokens per hour." Context length not specified in the fetched excerpt.
- **HIGH RELEVANCE**: Free trial tier models per the same fetch: `gpt-oss-120b`, `zai-glm-4.7`, and **`gemma-4-31b`** — direct quote: "gemma-4-31b - Google's Gemma model with image support (2 images max, 4MB payload)". This means **Cerebras's free tier hosts a model literally named gemma-4-31b** — closest possible free-tier match to the real submission target `gemma-4-31b-it` found in this entire research session. Qwen, Llama, DeepSeek explicitly NOT listed on Cerebras free tier per this fetch.
- Cross-check from search snippets (third-party, not fetched primary): "Cerebras free tier provides 1 million tokens per day permanently with no credit card required... Free tier includes 1M tokens/day, 30 RPM, 8K context, no credit card required... doesn't expire." NOTE: this contradicts the directly-fetched doc's "5 RPM" figure — the 30 RPM number appears to be from an older/different source or conflates a different tier; treat 5 RPM (from direct official doc fetch) as more authoritative, flag 30 RPM as UNVERIFIED/conflicting. Sources: https://www.getaiperks.com/en/ai/cerebras-free-tier-guide, https://adam.holter.com/... (snippets only).
- Speed claim (UNVERIFIED, third-party): "2,600+ tokens per second on wafer-scale silicon... 5-20x faster than typical GPU-based inference." Source: search aggregator snippets, not fetched primary.

**SambaNova Cloud (cloud.sambanova.ai)**
- Not yet directly fetched (search snippets only, UNVERIFIED against primary docs):
  - "All Developers will get $5 of Free Credit to start testing and building with SambaNova Cloud with no credit card required, which translates to millions of tokens on leading open-source models." Source: https://sambanova.ai/blog/sambanova-cloud-developer-tier-is-live
  - "Initial credits will expire in 30 days." vs. a conflicting claim "SambaNova Cloud offers a forever free plan as of May 2026 and the free plan is available indefinitely with no time limit... Free API access with rate limits, All models accessible, Fast time-to-first-token." Both from search snippets, sources: https://community.sambanova.ai/t/is-free-tier-going-away/847, https://costbench.com/software/llm-api-providers/sambanova-cloud/free-plan/ — CONFLICTING, UNVERIFIED, needs direct fetch of https://cloud.sambanova.ai/plans to resolve.
  - No mention found this session of specific Gemma/Kimi/MiniMax model availability on SambaNova — TODO follow-up search.

**GitHub Models (github.com/marketplace/models)**
- Direct fetch of https://docs.github.com/github-models/prototyping-with-ai-models (2026-07-07). Quote/paraphrase of free (Copilot Free tier) rate limits by model classification:
  - "Low Models: 15 requests per minute, 150 requests per day, 8000 in / 4000 out tokens per request, 5 concurrent requests"
  - "High Models: 10 requests per minute, 50 requests per day, 8000 in / 4000 out tokens per request, 2 concurrent requests"
  - "Embedding Models: 15 requests per minute, 150 requests per day, 64000 tokens per request, 5 concurrent requests"
  - Doc excerpt did not name specific models (no Gemma/Llama/DeepSeek/Mistral/Phi explicitly named in the fetched excerpt) but noted: "Access to OpenAI's models is in public preview" and that a "GitHub Models REST API" exists for programmatic/OpenAI-style access. Exact base_url/OpenAI-compat details NOT confirmed this session — TODO follow-up fetch of API reference page.
  - Cross-check search snippet: "High-tier models allow 50 requests per day (10 per minute), mini models allow 150 requests per day, with 8K tokens input and 4K tokens output per request." (Consistent with the direct doc fetch above.) Source: https://getaitools.dev/service/github-models
  - Changelog reference found (title only, not fetched): "GitHub Models now supports moving beyond free limits" — https://github.blog/changelog/2025-06-24-github-models-now-supports-moving-beyond-free-limits/ — implies a paid upgrade path exists beyond the free rate limits above.

**Cloudflare Workers AI (developers.cloudflare.com/workers-ai)**
- From WebSearch snippets (not yet directly fetched, UNVERIFIED against primary pricing doc — TODO fetch https://developers.cloudflare.com/workers-ai/platform/pricing/ directly):
  - "The free allocation allows anyone to use a total of 10,000 Neurons per day at no charge. All limits reset daily at 00:00 UTC."
  - "The free plan includes access to all hosted open-source models. All 47+ models are included — you pick which one to call per request. However... the 70B Llama 3.1 model is available but only on the paid tier (it's classified as a 'GA' model with higher neuron costs)."
  - "To use more than 10,000 Neurons per day, you need to sign up for the Workers Paid plan. On Workers Paid, you will be charged at $0.011 / 1,000 Neurons for any usage above the free allocation."
  - "There is no free allocation for proxied models" (i.e., free tier only covers Cloudflare-hosted models, not proxied/external ones).
  - Source for all above: search aggregator snippets citing https://developers.cloudflare.com/workers-ai/platform/pricing/, https://community.cloudflare.com/t/workers-ai-returns-4006-daily-free-neuron-limit-exceeded-while-dashboard-shows-0/909187, https://toolfreebie.com/cloudflare-workers-ai/ — none fetched directly this session, all UNVERIFIED pending direct doc fetch.
  - No Gemma/Kimi/MiniMax specifically named in these snippets — TODO follow-up search for exact Cloudflare Workers AI model catalog (`@cf/...` model IDs).

---

## Section B: Hugging Face ecosystem

### B1. Current state (2026) of HF's free serverless Inference API

- Direct fetch earlier (Section A4, https://huggingface.co/docs/inference-providers/pricing) established: "As of July 2025, hf-inference focuses mostly on CPU inference (e.g. embedding, text-ranking, text-classification, or smaller LLMs that have historical importance like BERT or GPT-2)." — i.e. the old free serverless API is now narrow-scope, not a general free path to large chat models.
- WebSearch (not directly fetched — search-aggregator paraphrase) on current 2026 status, cross-checking the above: "Hugging Face Inference API in 2026 consists of three products: the Serverless Inference API (free tier with rate limits, best for prototyping), Inference Endpoints (dedicated GPU you spin up per model, $0.50/hr+, scale-to-zero), and Inference Providers (a unified OpenAI-compatible gateway routing to Groq, Together AI, Fireworks, Replicate, Cerebras, and 10+ others)." Source: https://klymentiev.com/blog/huggingface-inference-api (snippet only, UNVERIFIED against primary).
- Same search batch, paraphrase: "The Serverless Inference API offers free access with rate limits for regular Hugging Face users (approximately a few hundred requests per hour)." — "approximately a few hundred requests per hour" is a rough third-party estimate, UNVERIFIED, no exact number found in any primary doc fetched this session. Source: same aggregator batch, also https://huggingface.co/docs/api-inference/index (title/URL surfaced by search, NOT fetched directly this session — TODO follow-up if exact serverless free numbers are needed).
- No explicit deprecation found: "The search results do not indicate that the free Serverless Inference API has been deprecated in 2026... the huggingface_hub library provides a unified interface to run inference with Inference Providers as a streamlined, unified access to models, building on the previous Serverless Inference API." (paraphrase from search synthesis, not a primary-doc quote — UNVERIFIED as a complete/current picture.)
- NET (paraphrase, cross-referencing A4 + B1): free HF "Inference API" access to actually useful chat-capable open models in 2026 runs primarily through **Inference Providers** (https://router.huggingface.co/v1, OpenAI-compatible, $0.10/month free credit for Free users as directly quoted in Section A4) rather than through the old standalone serverless "Inference API," which is now positioned for small/CPU models.

### B2. Trending small instruction-tuned HF models relevant to our 8 task categories

- Math/code (WebSearch synthesis, sources cited by aggregator, not independently fetched from each model's own card this session — UNVERIFIED per-number but model names/URLs are real, checkable at huggingface.co/models):
  - "Gemma 3 4B IT... 71.3% on HumanEval... and 89.2% on GSM8K math reasoning... multimodal input (text and images)... 128K context window." Source: https://www.kdnuggets.com/best-small-language-models-on-hugging-face-right-now (snippet).
  - "Qwen3.5-4B... sits at the center of the Qwen3.5 small series — a lineup that goes from 0.8B all the way to 9B, all sharing the same architecture and all carrying an Apache 2.0 license... native context length of 262,144 tokens, extensible to over one million. The model operates in thinking mode by default... but you can turn this off for faster, direct answers." (Thinking-toggle support confirmed here.) Same source.
  - "Phi-4-reasoning... a reasoning model fine-tuned from Phi-4 for math, science, and coding." Same source.
  - HF Hub live filter/search page for trending math models (real URL, not fetched for exact top result this session): https://huggingface.co/models?other=math&p=0&sort=trending — TODO follow-up direct fetch to confirm current #1 trending entry.
- Structured/JSON output & function calling:
  - "Llama 3.2 3B Instruct... handles tool calling and structured outputs cleanly — Meta built it with agentic use cases in mind." Source: search aggregator (same KDnuggets-style batch), UNVERIFIED per-claim.
  - Official HF docs pages found (titles/URLs real, surfaced by search, not fetched in full this session): "Structured Outputs with Inference Providers" — https://huggingface.co/docs/inference-providers/en/guides/structured-output ; "Function Calling with Inference Providers" — https://huggingface.co/docs/inference-providers/en/guides/function-calling ; "Function Calling" (Hugs guide) — https://huggingface.co/docs/hugs/en/guides/function-calling. Direct quote from search snippet of the structured-output guide: "Structured outputs guarantee a model returns a response that matches your exact schema every time." TODO: fetch these three docs directly for exact schema syntax if needed for implementation later (out of scope for this collect-only pass).
- Sentiment/classification & NER (from earlier WebSearch batch, real HF model URLs):
  - "Sentiment classification BERT Mini is based on Boltuix's BERT Mini, a lightweight version of BERT with only 11.2M parameters, fine-tuned specifically for emotion-based sentiment analysis." Model card: https://huggingface.co/Varnikasiva/sentiment-classification-bert-mini
  - "ModernFinBERT, released in 2025/7, is built on the ModernBERT architecture and trained on a mix of real and synthetic data, with LLM-based label correction applied to public datasets to fix human annotation errors... in some cases improving accuracy by up to 48% over existing models like FinBERT." (Domain-specific — finance sentiment — flagged in case relevant to a finance-sentiment task category.) Source: search snippet, model itself real but not independently fetched/verified this session.
  - "tabularisai/multilingual-sentiment-analysis" — multilingual sentiment+emotion model, "available in 23 languages with structured outputs." Model card URL: https://huggingface.co/tabularisai/multilingual-sentiment-analysis (real URL from search results, not fetched directly).
  - NER: "Popular NER models on Hugging Face include BERT-based models such as dbmdz/bert-large-cased-finetuned-conll03-english for named entity recognition tasks." Model URL (constructed from known naming convention, not independently re-verified this session): huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english — flag as UNVERIFIED exact URL/slug, TODO confirm by direct fetch.
  - HF live filter page (real, not fetched for current top result): https://huggingface.co/models?language=ner&p=8&sort=trending

### B3. HF Spaces / blog posts on "cascade"/"local+verifier"/"token-efficient agent" patterns

- No direct HF blog post or Space was found this session that explicitly demonstrates a "local model + verifier" or "cascade routing" pattern matching AMDA's design. Multiple targeted searches (`huggingface.co/blog "cascade" OR "router" local model verifier token efficient agent`, `huggingface.co/blog small model routing large model cascade verifier agent pattern`, `Hugging Face Spaces demo "router" small large model cost savings verifier`) did NOT surface a matching HF-native blog post or Space. Marking this sub-item's core ask as **NOT FOUND** (searched, came up empty) rather than fabricating a link.
- Adjacent/tangential real HF blog post found and worth noting even though it's not an exact match: "Design Patterns for Building Agentic Workflows" by Diego Carpintero — https://huggingface.co/blog/dcarpintero/design-patterns-for-building-agentic-workflows — paraphrase from search snippet: "a comprehensive guide to building and orchestrating AI Agents using six foundational design patterns: Evaluator-Optimizer, Context-Augmentation, Prompt-Chaining, Parallelization, Routing, and Orchestrator-Workers." (Routing and Evaluator-Optimizer patterns are conceptually adjacent to AMDA's verify-then-escalate design, but this is a general agentic-patterns post, not a cascade/local+verifier-specific one.) NOT independently fetched in full this session — title/URL/snippet only.
- Other adjacent HF blog post surfaced but off-topic (voice, not text-routing): "Reachy Mini goes fully local" — https://huggingface.co/blog/local-reachy-mini-conversation — paraphrase: "describes a cascade approach using the speech-to-speech library, and a cascaded voice pipeline has four stages: VAD, STT, LLM, and TTS." Not relevant to AMDA's text-based verify/escalate loop beyond the generic word "cascade" — flagged as tangential, NOT a match for our use case.
- Non-HF academic papers surfaced by the same searches (real arXiv links, NOT HF-native, included here only because they were found while searching HF specifically and are relevant background — clearly marked as arXiv, not HF):
  - "Is Escalation Worth It? A Decision-Theoretic Characterization of LLM Cascades" — https://arxiv.org/pdf/2605.06350
  - "R2V Agent: Teaching SLMs When to Ask for Help" — https://arxiv.org/pdf/2605.16604
  - "Model Routing as a Trust Problem: Route Receipts for Adaptive AI Systems" — https://arxiv.org/pdf/2605.01710
  - Direct quote/paraphrase from search synthesis (source ambiguous among the above, treat as UNVERIFIED aggregate paraphrase, not a single-source quote): "Cascade approaches run the small model and then apply a rule to decide whether escalation to the large model is needed, with FrugalGPT highlighting that cascades can substantially reduce cost while maintaining quality." "Cascade-style methods query a cheaper model first and escalate only when a scoring rule predicts that the response is insufficient."

### B4. HF's lighteval / EleutherAI's lm-evaluation-harness — deterministic verification approaches

- **lighteval** (https://github.com/huggingface/lighteval, fetched directly 2026-07-07). Direct quote: "Lighteval is your all-in-one toolkit for evaluating LLMs across multiple backends." Task coverage per fetch: "Math and Code: GSM8K, GSM-Plus, MATH, MATH500, AIME24, AIME25, and LiveCodeBench... Knowledge domains: MMLU, TriviaQA, Natural Questions... Multilingual support: Tasks across 200+ languages." The fetched README excerpt did NOT itself spell out exact verification internals (pass@k, answer-extraction regexes) — flagged: "the README does not contain explicit details about math verification methods, pass@k metrics, answer extraction techniques, or specific sample-level scoring mechanisms" in the fetched excerpt; it does mention "detailed, sample-by-sample results to debug" and custom task/metric support. Backends: "Accelerate, VLLM, SGLang, and Hugging Face Inference Endpoints."
- Cross-reference from search: "Lighteval took inspiration from Eleuther's AI Harness and Stanford's HELM." and "LightEval is a newer, actively maintained HF toolkit... supports multiple backends (Transformers, vLLM, HF Inference Endpoints, etc.)... A key difference between LightEval and LLM Foundry for multiple choice tasks like MMLU is that LightEval considers the log probabilities of entire answer sequences, whereas LLM Foundry only considers log probabilities of single letters." Source: https://cohorte.co/blog/lighteval-deep-dive-hugging-faces-all-in-one-framework-for-llm-evaluation (snippet, UNVERIFIED against primary).
- **lm-evaluation-harness** (EleutherAI) — https://github.com/EleutherAI/lm-evaluation-harness (surfaced by search, not directly fetched — findings below are search-snippet paraphrases citing specific harness source files, treat as UNVERIFIED pending direct fetch, though URLs themselves are real and checkable):
  - "The lm-evaluation-harness includes the MATH dataset, which contains 12,500 challenging competition mathematics problems."
  - "The exact match equivalence for math tasks is calculated using the sympy library. The few-shot setup and generated answer extraction are based on the Minerva approach." (Minerva math-answer-extraction approach.)
  - "For task configuration, the exact_match metric supports auxiliary arguments such as ignore_case, ignore_punctuation, and regexes_to_ignore. All metrics supported in HuggingFace Evaluate can also be used in lm-evaluation-harness."
  - Exact dependency/install line: "`math-verify`, `sympy>=1.12`, and `antlr4-python3-runtime==4.11` are required for math tasks, and can be installed via `pip install lm-eval[math]`." — this directly confirms lm-evaluation-harness uses the same `math-verify` HF library documented in Section C4 below, for its own deterministic math-task scoring.
  - Specific file surfaced (real repo path, not fetched in full): https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/leaderboard/math/utils.py — likely contains the actual extraction/comparison code; TODO direct fetch if implementation-level detail is later needed (out of scope for collect-only pass).
  - Minerva math task doc, real repo path: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/minerva_math/README.md (surfaced, not fetched).

---

## Section C: Concrete open-source tools/repos for actual integration

### C1. RouteLLM (lm-sys/RouteLLM)

- Confirmed real, pip-installable, directly fetched from https://github.com/lm-sys/RouteLLM (2026-07-07). Direct quote: "RouteLLM is a framework for serving and evaluating LLM routers." Install: `pip install "routellm[serve,eval]"` (or `pip install -e .` from source, per fetch).
- Four routing methods, direct quote/paraphrase from fetch: "sw_ranking (which uses a weighted Elo calculation for routing), bert (a BERT classifier trained on the preference data), causal_llm (an LLM-based classifier tuned on the preference data), and mf (a matrix factorization model trained on the preference data)." Claim from same fetch: "Trained routers are provided out of the box, which reduce costs by up to 85% on widely-used benchmarks such as MT Bench while maintaining 95% GPT-4 performance." (This 85%/95% figure is RouteLLM's own project claim per the README, not independently verified by us.)
- **Plugs into local+remote OpenAI-compatible setup — CONFIRMED with exact code**, directly fetched from https://github.com/lm-sys/RouteLLM/blob/main/examples/routing_to_local_models.md (2026-07-07):
  ```
  ollama run llama3
  ```
  ```python
  os.environ["OPENAI_API_KEY"] = "sk-XXXXXX"
  client = Controller(
    routers=["mf"],
    strong_model="gpt-4-1106-preview",
    weak_model="ollama_chat/llama3",
  )
  response = client.chat.completions.create(
    model="router-mf-0.11593",
    messages=[{"role": "user", "content": "Hello!"}]
  )
  ```
  OpenAI-compatible server option:
  ```bash
  export OPENAI_API_KEY=sk-...
  python -m routellm.openai_server --routers mf --weak-model ollama_chat/llama3 --config.example.yaml
  ```
  ```python
  import openai
  client = openai.OpenAI(base_url="https://localhost:6060/v1", api_key="no_api_key")
  response = client.chat.completions.create(
    model="router-mf-0.11593",
    messages=[{"role": "user", "content": "Hello!"}]
  )
  ```
  Note from fetch: RouteLLM "uses LiteLLM to support chat completions from a wide-range of open-source and closed models" and allows "any OpenAI-compatible endpoint" by prefixing model names with `openai/`. The threshold value in the model string (e.g. `0.11593`) "routes approximately 50% of queries to GPT-4 based on calibration" (paraphrase from fetch).
- Also on PyPI: https://pypi.org/project/routellm/ (real URL, surfaced by search, not independently fetched).
- Adjacent/competing real repo surfaced by search, NOT lm-sys's own but relevant prior art: NVIDIA's own router blueprint — https://github.com/NVIDIA-AI-Blueprints/llm-router — "Route LLM requests to the best model for the task at hand." (title only, not fetched).

### C2. Constrained decoding: outlines, guidance, GBNF grammars

- **outlines** (dottxt-ai/outlines) — real repo https://github.com/dottxt-ai/outlines. From WebSearch synthesis of official docs (dottxt-ai.github.io/outlines), NOT independently re-fetched via WebFetch this session but multiple real doc URLs surfaced and cross-corroborated:
  - "Outlines works with llama.cpp GGUF models and supports generators built with generate.regex, generate.json, generate.cfg, generate.format and generate.choice, including GPU acceleration."
  - "You can create an Outlines model from a llama.cpp model by first loading a GGUF model with Llama.from_pretrained and then creating an Outlines model using outlines.from_llamacpp()." — i.e. **direct native llama.cpp/GGUF support confirmed**, not limited to HF transformers/vLLM.
  - Also supports transformers/vLLM per general docs listing: https://dottxt-ai.github.io/outlines/reference/models/models/ (real URL, not fetched in full).
  - Dedicated llama.cpp reference doc (real URL, not fetched in full): https://dottxt-ai.github.io/outlines/reference/models/llamacpp/
  - Caveat found: at least one open GitHub issue flags friction — "outlines does not work with gguf models" (https://github.com/dottxt-ai/outlines/issues/550, title only) — suggests some GGUF compatibility issues have been reported historically; treat native support as real but not 100% frictionless per user reports. Also: "LlamaCpp on Mac generates nonsense" — https://github.com/dottxt-ai/outlines/issues/648 (title only).
- **guidance** (guidance-ai/guidance) — real repo https://github.com/guidance-ai/guidance. From search synthesis:
  - "Guidance is available through PyPI and supports a variety of backends including llama.cpp." Confirmed via repo path: `guidance/guidance/models/llama_cpp/_llama_cpp.py` — real file path: https://github.com/guidance-ai/guidance/blob/main/guidance/models/llama_cpp/_llama_cpp.py (surfaced by search, not fetched in full).
  - "You need to install llama-cpp-python with `pip install llama-cpp-python` in order to use guidance.models.LlamaCpp." — i.e. **native llama.cpp support confirmed via the llama-cpp-python binding**, not limited to HF transformers.
  - Third-party compatibility shim also found: "The llama-cpp-guidance package provides an LLM client compatibility layer between llama-cpp-python and guidance" — separate repo https://github.com/nicholasyager/llama-cpp-guidance (real URL, title only, not fetched — a community project, not official guidance-ai code).
- **GBNF grammars** (llama.cpp native grammar format) — real repo paths confirmed by search, matching known llama.cpp repo structure:
  - Grammar folder + README: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md — quote/paraphrase: "The grammars folder contains a handful of sample grammars, including json.gbnf."
  - Ready-made JSON grammar file, real URL: https://github.com/ggml-org/llama.cpp/blob/master/grammars/json.gbnf
  - Usage example (paraphrase from search snippet quoting the repo): `llama-cli -m model.gguf -n 256 --grammar-file grammars/json.gbnf -p 'Request: schedule a call at 8pm; Command:'`
  - Also: "llama.cpp can also convert JSON schemas to grammars either ahead of time or at each request. There's a llama.cpp script examples/json-schema-to-grammar.py that can turn JSON schemas into working GBNF grammars." — real script, path implied: `examples/json-schema-to-grammar.py` in the ggml-org/llama.cpp repo (not independently re-verified by direct fetch this session, but is a long-standing, well-known script in that repo per general knowledge — flag as UNVERIFIED-exact-path pending direct check).
  - Third-party grammar authoring tool surfaced: https://grammar.intrinsiclabs.ai/ ("for authoring more complex JSON grammars" per search snippet) — real URL, not fetched, not an official llama.cpp resource.
  - This directly answers the "ready-made GBNF grammars repo" question: **yes, llama.cpp ships its own `grammars/` folder with a working `json.gbnf`** that could be reused directly instead of hand-writing one; no separate third-party "GBNF grammar zoo" repo was found in this session beyond that.

### C3. DSPy (stanfordnlp/dspy)

- Real repo confirmed: https://github.com/stanfordnlp/dspy (surfaced by search, not independently WebFetched this session — title/README-derived synthesis below, cross-corroborated across multiple result snippets including https://dspy.ai/ the official project site).
- Direct quote (from search synthesis of README/site content): "DSPy is a framework that lets you declare your task as typed inputs and outputs instead of managing messy prompts." "DSPy introduces powerful general-purpose modules that can learn to prompt (or finetune) your language model within your pipeline on your data. When you change your data, make tweaks to your program's control flow, or change your target LM, the DSPy compiler can map your program into a new set of prompts (or finetunes) that are optimized specifically for this pipeline."
- Optimizers named: "COPRO generates and refines new instructions for each step, and optimizes them with coordinate ascent (hill-climbing using the metric function and the trainset). MIPROv2 generates instructions and few-shot examples in each step, with instruction generation that is data-aware and demonstration-aware, using Bayesian Optimization to search over the space of generation instructions/demonstrations."
- Relevance-to-routing-agent assessment: NOT independently confirmed by any source found this session that DSPy has a purpose-built "router" module for local/remote model cascades — its stated scope is prompt/pipeline optimization (compiling programs into optimized prompts/finetunes) rather than runtime model-selection/escalation logic. No direct claim of routing-agent applicability found in sources; flagged as UNVERIFIED/not directly stated (this is an absence-of-evidence note, not a confirmed negative).
- Origin doc found: "DSPy: Compiling Declarative Language Model Calls into ..." (Stanford HAI) — https://hai.stanford.edu/research/dspy-compiling-declarative-language-model-calls-into-state-of-the-art-pipelines (title only, not fetched).

### C4. sympy / math-verify for symbolic MATH-answer verification

- **math-verify** (huggingface/Math-Verify) — real repo https://github.com/huggingface/Math-Verify, real PyPI package https://pypi.org/project/math-verify/. Install per search-synthesized PyPI/README info: `pip install math-verify`, or with inference extras: `pip install 'math-verify[inference]'`.
- Grading algorithm, paraphrase from search synthesis of README: "three-step algorithm: Answer Extraction -> Expression Common Representation Conversion (SymPy) -> Gold Comparison... 1. Answer Extraction: Retrieves the answer from the model output in a format-agnostic manner. 2. Answer Parsing: Converts the extracted answer to a common representation (SymPy), normalizing the extracted answer and parsing it using ANTLR4 grammar. 3. Comparison: Compares the parsed answer with the gold answer, initially attempting string comparison and basic SymPy equality." Requirements: "Python 3.10+... main dependency is latex2sympy2_extended==1.11.0."
- **Exact usage code, directly fetched from https://github.com/huggingface/Math-Verify/blob/main/README.md (2026-07-07):**
  ```python
  from math_verify import parse, verify

  gold = parse("${1,3} \\cup {2,4}$")
  answer = parse("${1,2,3,4}$")

  verify(gold, answer)
  # >>> True
  ```
  This is a real, directly-fetched, verbatim code example — confirms the exact API shape (`parse()` then `verify()`) for symbolic equivalence checking of a model's final answer against a gold answer.
- Confirmed used downstream by EleutherAI's lm-evaluation-harness (see Section B4) as its own math-task exact-match verification dependency — i.e. math-verify is the de facto standard verification library referenced by two separate major open eval frameworks (lighteval and lm-evaluation-harness) found in this session.
- Known friction point found: an open GitHub issue titled "cannot install math-verify" — https://github.com/huggingface/Math-Verify/issues/38 (title only, not fetched — flag as a potential installation gotcha to watch for, unconfirmed root cause).
- HF's own blog post about it, real URL surfaced (not fetched): https://github.com/huggingface/blog/blob/main/math_verify_leaderboard.md ("Math-Verify Leaderboard" blog source file).

### C5. Real GitHub repos implementing "LLM cascade" / "local-first + escalate" patterns

- Direct github.com/search-style queries were run via WebSearch (not github.com's own search UI, which requires auth/JS — used general web search targeting github.com results instead). Results, all real repo URLs:
  - **RouteLLM** itself (already covered in C1) is the most directly relevant, code-complete example of local+remote routing.
  - **llm-use/llm-use** — https://github.com/llm-use/llm-use — direct quote from search snippet (repo description): "LLM orchestration toolkit for agent workflows: planner + workers + synthesis, optional router (LLM + learned fallback), supports OpenAI/Anthropic/Ollama/llama.cpp, real scraping with caching, MCP server integration, and a TUI chat UI." Notably supports llama.cpp directly per its own description. Further paraphrase from search: "includes an optional router with learned fallback capabilities that falls back to a heuristic router if the primary fails."
  - **akiojin/llmlb** — https://github.com/akiojin/llmlb — "Distributed LLM router with load balancing and automatic model distribution." Paraphrase: "routes requests across registered inference endpoints and can proxy to cloud LLM providers via model prefixes, allowing local and cloud models to be used interchangeably."
  - **tashfeenahmed/freellmapi** — https://github.com/tashfeenahmed/freellmapi — direct quote (repo description): "OpenAI-compatible proxy that stacks the free tiers of 16 LLM providers (~1.7B tokens/month) behind one /v1 endpoint — plus any custom OpenAI-compatible endpoint. Smart routing, automatic failover, encrypted keys. Personal experimentation only." NOTE: this repo's own description says "Personal experimentation only" — directly matches AMDA's stated dev/testing-only use case (not for the final submission), and it is itself a real, existing implementation of exactly the "stack multiple free-tier providers behind one OpenAI-compatible endpoint" pattern AMDA is looking for prior art on.
  - **NousResearch/hermes-agent**, feature request thread — https://github.com/NousResearch/hermes-agent/issues/15176 — title: "[Feature]: Add fallback routing from local open-source models to closed-source models after repeated failures" — paraphrase from search: "Hermes Agent starts with a local/open-source model as the primary and automatically switches to a stronger cloud model after repeated failures or lack of progress." (This is an open feature request/issue, not necessarily merged/shipped code — flag as a design-pattern reference, not confirmed production code. UNVERIFIED whether implemented.)
  - **aws-samples/sample-amazon-bedrock-as-llm-fallback** — https://github.com/aws-samples/sample-amazon-bedrock-as-llm-fallback — "production-ready LLM fallback router implementation that demonstrates automatic failover between different AI model providers (OpenAI, Anthropic, Amazon Bedrock) with model-to-model fallback within Bedrock and centralized configuration." (paraphrase from search). AWS official sample repo.
  - Not GitHub, but relevant background paper on the cascade concept generally (real arXiv link): "Cluster, Route, Escalate: Cascaded Framework for Cost-Aware LLM Serving" — https://arxiv.org/html/2606.27457
  - Also relevant: NVIDIA's own official router blueprint (already flagged in C1) — https://github.com/NVIDIA-AI-Blueprints/llm-router

---

## Sources (raw list of every URL visited/cited this session)

### Directly fetched via WebFetch
- https://console.groq.com/docs/rate-limits
- https://console.groq.com/docs/models
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://build.nvidia.com/ (TIMEOUT — no content retrieved)
- https://build.nvidia.com/models (TIMEOUT — no content retrieved)
- https://openrouter.ai/models?max_price=0 (nav/footer only, no model data)
- https://inference-docs.cerebras.ai/support/rate-limits
- https://docs.github.com/github-models/prototyping-with-ai-models
- https://huggingface.co/docs/inference-providers/pricing
- https://openrouter.ai/models?order=top-weekly&max_price=0 (nav/footer only, no model data)
- https://r.jina.ai/https://openrouter.ai/models?max_price=0 (proxy fetch — returned partial model data)
- https://openrouter.ai/docs/api-reference/limits
- https://huggingface.co/google/gemma-4-31B-it
- https://huggingface.co/inference/models
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://cloud.sambanova.ai/plans
- https://github.com/huggingface/lighteval
- https://github.com/lm-sys/RouteLLM
- https://github.com/lm-sys/RouteLLM/blob/main/examples/routing_to_local_models.md
- https://github.com/huggingface/Math-Verify/blob/main/README.md

### Surfaced via WebSearch and cited (snippet/title level; not independently WebFetched this session unless noted above)
- https://www.grizzlypeaksoftware.com/articles/p/groq-api-free-tier-limits-in-2026-what-you-actually-get-uwysd6mb
- https://pricepertoken.com/endpoints/groq/free
- https://community.groq.com/t/is-there-a-free-tier-and-what-are-its-limits/790
- https://www.cloudzero.com/blog/groq-pricing/
- https://tokenmix.ai/blog/groq-free-tier-limits-2026
- https://www.eesel.ai/blog/groq-pricing
- https://tokenmix.ai/blog/groq-api-access-2026-free-tier-rate-limits
- https://costbench.com/software/llm-api-providers/groq/free-plan/
- https://tokenmix.ai/blog/groq-api-pricing
- https://console.groq.com/docs/deprecations
- https://console.groq.com/docs/model/moonshotai/kimi-k2-instruct
- https://portkey.ai/models/groq
- https://kilo.ai/docs/ai-providers/groq
- https://groq.com/blog/introducing-kimi-k2-0905-on-groqcloud
- https://docs.openclaw.ai/providers/groq
- https://console.groq.com/docs/changelog
- https://platform.kimi.ai/docs/models
- https://blog.laozhang.ai/en/posts/gemini-api-free-tier
- https://www.aifreeapi.com/en/posts/gemini-api-rate-limits-per-tier
- https://tokenmix.ai/blog/gemini-api-free-tier-limits
- https://pecollective.com/tools/gemini-free-tier-guide/
- https://ai.google.dev/gemini-api/docs/pricing
- https://help.apiyi.com/en/google-ai-studio-rate-limits-2026-guide-en.html
- https://usagebox.com/articles/gemini-api-billing-free-tier-confusion
- https://www.nocode.mba/articles/google-ai-studio-pricing
- https://aistudio.google.com/rate-limit
- https://medium.com/coding-nexus/nvidia-is-offering-80-ai-models-for-free-via-apis-fc64b38276b8
- https://decodethefuture.org/en/nvidia-nim-api-explained/
- https://developer.nvidia.com/blog/access-to-nvidia-nim-now-available-free-to-developer-program-members/
- https://www.mindstudio.ai/blog/nvidia-nim-free-models-ai-workflows
- https://costbench.com/software/llm-api-providers/nvidia-nim/free-plan/
- https://github.com/NVIDIA/metropolis-nim-workflows/blob/main/README.md
- https://github.com/xRyul/pi-nvidia-nim
- https://github.com/NVIDIA/metropolis-nim-workflows/
- https://decodethefuture.org/en/how-to-get-nvidia-api-key-free/
- https://huggingface.co/docs/inference-providers/index
- https://www.metacto.com/blogs/the-true-cost-of-hugging-face-a-guide-to-pricing-and-integration
- https://huggingface.co/pricing
- https://www.eesel.ai/blog/hugging-face-pricing
- https://klymentiev.com/blog/huggingface-inference-api
- https://free-llm.com/provider/huggingface-inference
- https://huggingface.co/blog/inference-providers-publicai
- https://belski.me/blog/ai_inference_providers_2026_free_tier_deep_dive/
- https://myengineeringpath.dev/tools/hugging-face/
- https://openrouter.ai/collections/free-models
- https://costgoat.com/pricing/openrouter-free-models
- https://www.remoteopenclaw.com/blog/openrouter-free-models-openclaw-guide
- https://openrouter.ai/openrouter/free
- https://rubentorney.com/blog/en/openrouter-modeles-gratuits-2026.html
- https://aitoolsradar.org/blog/guides/openrouter-free-models-2026/
- https://buldrr.com/openrouter-free-api-keys-free-models-simple-guide/
- https://www.teamday.ai/blog/best-free-ai-models-openrouter-2026
- https://openrouter.ai/openrouter
- https://www.getaiperks.com/en/ai/cerebras-free-tier-guide
- https://pricepertoken.com/endpoints/cerebras/free
- https://www.cerebras.ai/pricing
- https://tokenmix.ai/blog/cerebras-api-key-rate-limits-free-tier-2026
- https://aicreditmart.com/ai-credits-providers/cerebras-free-tier-1-million-tokens-day-guide-2026/
- https://www.linkedin.com/posts/adam-holter-b5334327a_cerebras-just-dropped-a-free-1m-tokens-per-activity-7376925874203361280-WAUc
- https://adam.holter.com/cerebras-opens-a-free-1m-tokens-per-day-inference-tier-and-ccerebras-now-offers-free-inference-with-1m-tokens-per-day-real-speed-benchmarks-show-2600-tokens-sec-on-llama4scout-here-are-the-actual-n/
- https://www.cerebras.ai/blog/cerebras-inference-now-available-via-pay-per-token
- https://getfreeai.net/en/services/api/cerebras/
- https://sambanova.ai/blog/sambanova-cloud-developer-tier-is-live
- https://community.sambanova.ai/t/is-free-tier-going-away/847
- https://www.deeplearning.ai/the-batch/sambanova-boosts-llama-3-1-performance-with-fast-free-access-to-largest-model
- https://www.datacenterdynamics.com/en/news/sambanova-launches-ai-inference-cloud/
- https://pricepertoken.com/endpoints/sambanova
- https://www.eesel.ai/blog/sambanova-cloud-pricing
- https://x.com/SambaNovaAI/status/1888379871862137317
- https://medium.com/towardsdev/getting-started-with-sambanova-and-sambacloud-97f0d7e1123a
- https://docs.sambanova.ai/docs/en/models/rate-limits
- https://github.blog/changelog/2025-06-24-github-models-now-supports-moving-beyond-free-limits/
- https://docs.github.com/billing/managing-billing-for-your-products/about-billing-for-github-models
- https://github.com/orgs/community/discussions/149698
- https://getaitools.dev/service/github-models
- https://docs.github.com/en/enterprise-cloud@latest/billing/managing-billing-for-your-products/about-billing-for-github-models
- https://blog.jiatool.com/en/posts/github_models/
- https://github.com/orgs/community/discussions/143855
- https://github.com/mnfst/awesome-free-llm-apis
- https://pecollective.com/blog/ai-free-tiers-compared/
- https://medium.com/codetodeploy/cloudflare-free-llm-apis-or-so-we-thought-5d6275c429c4
- https://community.cloudflare.com/t/workers-ai-returns-4006-daily-free-neuron-limit-exceeded-while-dashboard-shows-0/909187
- https://blog.cloudflare.com/workers-ai-ga-huggingface-loras-python-support/
- https://costbench.com/software/llm-api-providers/cloudflare-workers-ai/free-plan/
- https://toolfreebie.com/cloudflare-workers-ai/
- https://zairalabs.ai/guide/tools/cloudflare-workers-ai/
- https://eastondev.com/blog/en/posts/ai/20251121-workers-ai-tutorial/
- https://huggingface.co/MiniMaxAI/MiniMax-M3
- https://huggingface.co/lukealonso/MiniMax-M3-NVFP4
- https://huggingface.co/nvidia/MiniMax-M3-NVFP4
- https://huggingface.co/MiniMaxAI/MiniMax-M3-MXFP8
- https://huggingface.co/unsloth/MiniMax-M3-GGUF
- https://huggingface.co/Mapika/MiniMax-M3-NVFP4
- https://huggingface.co/Inferact/MiniMax-M3-EAGLE3
- https://huggingface.co/MiniMaxAI/MiniMax-M3/discussions/17/files
- https://huggingface.co/MiniMaxAI/MiniMax-M3/discussions/1
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md
- https://huggingface.co/docs/chat-ui/configuration/llm-router
- https://huggingface.co/docs/transformers/en/model_doc/gemma
- https://blog.starmorph.com/blog/llm-model-names-decoded
- https://huggingface.co/collections/mlx-community/gemma-4
- https://pi.dev/models
- https://github.com/anomalyco/opencode/issues/15092
- https://cohorte.co/blog/lighteval-deep-dive-hugging-faces-all-in-one-framework-for-llm-evaluation
- https://huggingface.co/docs/leaderboards/en/open_llm_leaderboard/about
- https://arxiv.org/pdf/2508.03686
- https://arxiv.org/pdf/2406.11794
- https://huggingface.co/datasets/John6666/forum2/blob/main/eval_finetuned_llm_lighteval_2.md
- https://huggingface.co/datasets/John6666/forum2/blob/main/eval_finetuned_llm_lighteval_1.md
- https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/leaderboard/README.md
- https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/minerva_math/README.md
- https://slyracoon23.github.io/blog/posts/2025-03-21_eleutherai-evaluation-methods.html
- https://github.com/EleutherAI/lm-evaluation-harness/releases
- https://github.com/EleutherAI/lm-evaluation-harness
- https://www.eleuther.ai/projects/large-language-model-evaluation
- https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md
- https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/new_task_guide.md
- https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/leaderboard/math/utils.py
- https://huggingface.co/blog/local-reachy-mini-conversation
- https://huggingface.co/inference/get-started
- https://huggingface.co/blog/Hcompany/holo31
- https://docs.openclaw.ai/providers/huggingface
- https://huggingface.co/blog/daya-shankar/open-source-llms
- https://huggingface.co/docs/huggingface_hub/package_reference/inference_client
- https://www.jan.ai/docs/desktop/remote-models/huggingface
- https://docs.litellm.ai/docs/providers/huggingface
- https://huggingface.co/papers?q=multi-agent+topologies
- https://huggingface.co/models?other=sentiment-analysis
- https://huggingface.co/Varnikasiva/sentiment-classification-bert-mini
- https://huggingface.co/models?library=sentiment-analysis
- https://huggingface.co/models?language=ner&p=8&sort=trending
- https://huggingface.co/docs/transformers/main_classes/pipelines
- https://huggingface.co/models?other=sentiment-classification
- https://huggingface.co/samadpls/sentiment-analysis
- https://www.kdnuggets.com/the-complete-hugging-face-primer-for-2026
- https://huggingface.co/models?pipeline_tag=text-classification&sort=downloads&search=sentiment
- https://huggingface.co/tabularisai/multilingual-sentiment-analysis
- https://www.kdnuggets.com/best-small-language-models-on-hugging-face-right-now
- https://huggingface.co/papers/trending
- https://github.com/fabledruns/awesome-huggingface-models
- https://www.igmguru.com/blog/hugging-face-cheat-sheet
- https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard
- https://huggingface.co/models?other=math&p=0&sort=trending
- https://huggingface.co/blog/hf-skills-training
- https://www.kaggle.com/datasets/zoupet/hugging-face-models-trending
- https://huggingface.co/papers
- https://github.com/huggingface/Math-Verify
- https://pypi.org/project/math-verify/
- https://github.com/huggingface/Math-Verify/pyproject.toml
- https://libraries.io/pypi/math-verify
- https://deepwiki.com/huggingface/Math-Verify/4-usage-guide
- https://github.com/huggingface/Math-Verify/blob/main/extract_answers.py
- https://github.com/huggingface/Math-Verify/issues/38
- https://github.com/huggingface/blog/blob/main/math_verify_leaderboard.md
- https://github.com/lm-sys/RouteLLM/blob/main/README.md
- https://github.com/lm-sys/RouteLLM/blob/main/pyproject.toml
- https://pypi.org/project/routellm/
- https://github.com/NVIDIA-AI-Blueprints/llm-router
- https://gaodalie.substack.com/p/routellm-how-i-route-to-the-best
- https://github.com/olimiemma/RouteLLM_
- https://github.com/nate-lrt/llm-routing
- https://github.com/Liqs-v2/RouteLLM
- https://dottxt-ai.github.io/outlines/latest/guide/getting_started/
- https://dottxt-ai.github.io/outlines/reference/models/llamacpp/
- https://github.com/dottxt-ai/outlines
- https://dottxt-ai.github.io/outlines/reference/models/models/
- https://github.com/ggml-org/llama.cpp
- https://blog.dottxt.ai/how-fast-cfg.html
- https://huggingface.co/blog/davidberenstein1957/ai-blueprint-agentic-rag-part-3-generate
- https://dottxt-ai.github.io/outlines/welcome/
- https://github.com/dottxt-ai/outlines/issues/648
- https://github.com/dottxt-ai/outlines/issues/550
- https://github.com/nicholasyager/llama-cpp-guidance
- https://github.com/ggml-org/llama.cpp/discussions/22640
- https://martinuke0.github.io/posts/2026-01-07-mastering-llamacpp-a-comprehensive-guide-to-local-llm-inference/
- https://self.md/guides/local-llms-llama-cpp/
- https://github.com/guidance-ai/guidance/blob/main/guidance/models/llama_cpp/_llama_cpp.py
- https://tech-insider.org/llama-cpp-tutorial-2026/
- https://blog.steelph0enix.dev/posts/llama-cpp-guide/
- https://weavai.app/blog/en/2026/04/24/llama-cpp-2026-guide-local-ai-inference-setup/
- https://github.com/guidance-ai/guidance
- https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/grammars/json.gbnf
- https://til.simonwillison.net/llms/llama-cpp-python-grammars
- https://www.devshorts.in/p/gbnfggml-bnf-explained-an-approach
- https://withcatai.github.io/node-llama-cpp/guide/grammar
- https://huggingface.co/spaces/Steven10429/apply_lora_and_quantize/blob/main/llama.cpp/grammars/README.md
- https://medium.com/@sridevi17j/gbnf-grammar-structure-your-llm-outputs-with-gbnf-0e71965e76f9
- https://grammar.intrinsiclabs.ai/
- https://github.com/stanfordnlp/dspy
- https://github.com/StanfordMIMI/dspy-helm
- https://github.com/stanfordnlp/dspy/blob/main/docs/docs/faqs.md
- https://github.com/stanfordnlp/dspy/blob/main/docs/docs/learn/optimization/optimizers.md
- https://github.com/evalops/dspy-0to1-guide
- https://dev.to/ashokan/a-beginner-friendly-tutorial-using-dspy-to-enhance-prompt-engineering-with-openai-apis-1nbn
- https://dspy.ai/
- https://arxiv.org/pdf/2508.01159
- https://hai.stanford.edu/research/dspy-compiling-declarative-language-model-calls-into-state-of-the-art-pipelines
- https://tianpan.co/blog/2025-11-03-llm-routing-model-cascades
- https://arxiv.org/html/2606.27457
- https://arxiv.org/pdf/2605.16604
- https://gurusup.com/blog/multi-agent-orchestration-guide
- https://medium.com/@michael.hannecke/the-model-router-running-a-team-of-local-llms-instead-of-one-big-one-fd75eeec9d39
- https://www.buildmvpfast.com/blog/llm-fallback-strategies-primary-model-secondary-model-2026
- https://arxiv.org/pdf/2606.22840
- https://dev.to/crosspostr/implementing-automatic-llm-provider-fallback-in-ai-agents-using-an-llm-gateway-openai-anthropic-kg2
- https://files.sri.inf.ethz.ch/website/papers/dekoninck2024cascaderouting.pdf
- https://github.com/NousResearch/hermes-agent/issues/15176
- https://blog.laozhang.ai/en/posts/openclaw-llm-setup
- https://devactivity.com/insights/community-insight-local-llms-copilot-bridging-cloud-limits-for-peak-productivity/
- https://github.com/aws-samples/sample-amazon-bedrock-as-llm-fallback
- https://github.com/tashfeenahmed/freellmapi
- https://github.com/orgs/community/discussions/190067
- https://github.com/akiojin/llmlb
- https://github.com/llm-use/llm-use
- https://arxiv.org/pdf/2603.24787
- https://arxiv.org/pdf/2601.07965
- https://arxiv.org/pdf/2604.04929
- https://arxiv.org/pdf/2606.12243
- https://huggingface.co/blog/dcarpintero/design-patterns-for-building-agentic-workflows
- https://arxiv.org/pdf/2605.06350
- https://arxiv.org/pdf/2605.01710
- https://arxiv.org/pdf/2603.00724
- https://huggingface.co/docs/inference-providers/en/guides/structured-output
- https://huggingface.co/yahyakhoder/MD2JSON-T5-small-V1
- https://huggingface.co/docs/hugs/en/guides/function-calling
- https://huggingface.co/learn/cookbook/en/structured_generation_vision_language_models
- https://discuss.huggingface.co/t/getting-models-to-output-structured-json/60471
- https://github.com/huggingface/transformers/issues/23102
- https://huggingface.co/docs/text-generation-inference/en/index
- https://huggingface.co/docs/inference-providers/en/guides/function-calling
- https://discuss.huggingface.co/t/recommend-an-ai-model-for-structured-json/43308
- https://huggingface.co/learn/cookbook/en/enterprise_hub_serverless_inference_api
- https://huggingface.co/docs/api-inference/index

**End of log.** Research date 2026-07-07. This is a raw collection with no synthesis, no recommendation, and no integration code — every finding above is either a direct quote (marked) or an explicitly-labeled paraphrase, sourced to a URL. Several items are explicitly flagged UNVERIFIED where only search-snippet (not primary-source fetch) evidence was available, or where sources conflicted with each other (e.g. Cerebras RPM: 5 per official docs fetch vs. 30 per third-party blog; SambaNova free-credit expiration: 30 days per one source vs. "forever free" per another; NVIDIA NIM signup credits: 1,000 vs. 5,000 in different snippets).
