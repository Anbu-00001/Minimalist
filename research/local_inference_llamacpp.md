# Local Inference Engineering Research — llama.cpp, GGUF, Small Models

Research log for AMDA (Track 1 AMD Hackathon). COLLECT ONLY — no conclusions, no model recommendation, no synthesis. Bullets = URL + quote/paraphrase (paraphrase marked). UNVERIFIED = uncertain/unconfirmed claim.

---

## 1. llama.cpp on AMD GPUs (ROCm/HIP) vs CPU-only

- Source: https://github.com/ggml-org/llama.cpp/discussions/15021 (llama-bench, Llama-2-7B Q4_0, no Flash Attention)
  - MI300X: "pp512: 11476.40 ± 72.79 t/s, tg128: 232.92 ± 0.53 t/s" (user @yeahdongcn)
  - RX 7900 XTX: "pp512: 3552.27 ± 101.96 t/s, tg128: 167.11 ± 0.50 t/s"
  - RX 7900 XT: "pp512: 3098.38 ± 24.02, tg128: 116.15 ± 0.06 t/s"
  - MI210: "pp512: 2486.22 ± 9.58, tg128: 124.51 ± 0.04 t/s"
  - Pro W7900: "pp512: 3213.17 ± 80.47, tg128: 121.18 ± 0.06 t/s"
  - Paraphrase: Flash Attention generally helps on newer RDNA3+ arch, but "Pro V620 shows FA slowing performance by ~30%" (user @samteezy) — inconsistent FA optimization across AMD GPU families.
  - Paraphrase: on a watercooled 7900 XTX, Vulkan backend reportedly hit "pp512: 6695.94 ± 211.86 t/s" — outperforming native ROCm HIP in that specific config (user @daMustermann).

- Source: https://llm-tracker.info/howto/AMD-GPUs
  - RX 7900 XT: pp3968 = 2,366 tok/s, tg128 = 97.17 tok/s (Llama-2-7B Q4_0)
  - RX 7900 XTX: pp3968 = 2,576 tok/s, tg128 = 119.09 tok/s (Llama-2-7B Q4_0)
  - Radeon VII (Vega 20, deprecated): pp3968 = 432.28 tok/s, tg128 = 54.42 tok/s — noted as "deprecated in ROCm" with "limited support"
  - Backend comparison table on 7900 XTX (same model): ROCm/HIP = 2,550 prompt tok/s / 119 inference tok/s; Vulkan = 758 / 52.3; CLBlast = 219 / 35.4 — i.e. HIP backend far ahead of Vulkan/CLBlast in this source's numbers (contrasts with the single anecdotal Vulkan-beats-ROCm report above — sources disagree, flagging as UNVERIFIED which is faster in general).
  - Paraphrase: this source states ROCm HIP is roughly "20% slower for prompt processing" and "33% slower for generation" than an equivalent NVIDIA CUDA setup on comparable-tier hardware.

- Source: https://www.mindstudio.ai/blog/running-local-ai-amd-rocm-ollama-lm-studio (per search snippet, not directly fetched — UNVERIFIED detail level)
  - Paraphrase: as of the article's writing ("2026"), AMD ROCm support for local inference has matured but "compatibility layers add friction."

- Source: https://github.com/ikawrakow/ik_llama.cpp/discussions/562 — AMD GPU Vulkan & ROCm/HIP discussion thread exists on the `ik_llama.cpp` fork (a llama.cpp fork with additional quant/perf work); not deep-fetched, noting existence for follow-up. UNVERIFIED contents.

- Source: https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp/README.html — "Llama.cpp Meets Instinct: A New Era of Open-Source AI Acceleration" — official AMD ROCm blog on llama.cpp + Instinct GPUs. Found via search, not deep-fetched; title/URL confirmed real.

- Source: https://rocm.docs.amd.com/en/latest/compatibility/ml-compatibility/llama-cpp-compatibility.html — "ROCm-LLMExt compatibility matrix" — official AMD compatibility matrix page for llama.cpp on ROCm. Confirmed real URL via search; contents not fetched.

- CPU+GPU hybrid inference (paraphrase, from WebSearch synthesis, source page not independently verified): offloading 33 layers to an AMD Ryzen 7 5700U APU (iGPU) reportedly improved prompt processing from 18.54 t/s to 20.16 t/s (~8.7% increase) — cite with caution, UNVERIFIED exact source page.

### Docker / device permissions for ROCm GPU passthrough (relevant since AMDA runs in Docker)
- Source: search results referencing https://rocm.docs.amd.com/projects/llama-cpp/en/docs-26.02/install/llama-cpp-install.html and https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html
  - Paraphrase: to run ROCm-enabled containers you must expose `/dev/kfd` and `/dev/dri` via `--device` flags and add `--group-add video` (and sometimes `render`) for GPU access.
  - Example docker run pattern surfaced in search synthesis:
    ```
    docker run --privileged --network=host \
      --device=/dev/kfd --device=/dev/dri \
      --group-add video --cap-add=SYS_PTRACE \
      --security-opt seccomp=unconfined --ipc=host --shm-size 16G \
      -v $MODEL_PATH:/data rocm/llama.cpp:<TAG>_full
    ```
  - Paraphrase: "/dev/dri/renderD*" and "/dev/kfd" belong to the render group; "/dev/dri/card*" belongs to the video group.
  - Official pre-built ROCm images referenced: `ghcr.io/ggml-org/llama.cpp:full-rocm`, `light-rocm`, `server-rocm` (from llama.cpp docs.md, see section 5 below) and `rocm/llama.cpp` on Docker Hub (https://hub.docker.com/r/rocm/llama.cpp).

### "Unsloth + llama.cpp for Radeon" preset — what it refers to
- Source: https://unsloth.ai/docs/get-started/install/amd — "Fine-tuning LLMs on AMD GPUs with Unsloth Guide"
  - Paraphrase: Unsloth enables fine-tuning LLMs on AMD GPUs "up to 2x faster with ~70% less memory, with no NVIDIA required." Supports "AMD Radeon RDNA 2/3/3.5/4 (RX 6000–9000 series) and data center GPUs including the MI300X (192GB)."
  - Paraphrase: ROCm 6.0+ required — "ROCm 5.x and below have no PyTorch wheels."
- Source: https://unsloth.ai/docs/blog/unleash-the-power-of-amd-official-support-for-unsloth-is-here — "Unleash the Power of AMD: Official Support for Unsloth is Here!" (blog announcing official AMD support).
- Paraphrase (from search synthesis, exact source page among the above): "Unsloth provides llama.cpp for ROCm with prebuilt binaries served to AMD hosts, with source compilation as fallback," and "Unsloth now uses constant fresh up to date llama.cpp prebuilts across CUDA, ROCm, Windows, Linux, and macOS."
- Related community/build guides found (titles/URLs confirmed real, not deep-fetched):
  - https://www.cjvirtuc.io/posts/llama-cpp-rocm/ — "Building llama.cpp with rocm on Fedora 41"
  - https://github.com/mambiux/LLAMA.CPP-ROCm — "A step-by-step guide to setting up llama.cpp with ROCm on AMD APUs"
- Note: search did not surface a single named "Unsloth + llama.cpp for Radeon" branded artifact/repo distinct from the above — the phrase appears to describe the general Unsloth-provides-ROCm-llama.cpp-binaries workflow rather than one specific named repo. Flagging as UNVERIFIED whether the Jupyter preset maps to something more specific than this.

### HIP build details (compiling llama.cpp for Radeon targets)
- Source: https://github.com/ggml-org/llama.cpp/issues/13340 and https://github.com/ggml-org/llama.cpp/docs/build.md (via search synthesis)
  - Paraphrase: gfx1100 target = Radeon RX 7900 XTX/XT/GRE.
  - Build command quoted: `HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1030 -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -- -j 16` (substitute gfx1100 for that arch).
  - Paraphrase: a Docker approach builds directly from source inside a ROCm Ubuntu base image, e.g. `rocm/dev-ubuntu-24.04:7.0-complete`.
  - Paraphrase: one env var pattern seen: `LLAMACPP_ROCM_ARCH=gfx803,gfx900,gfx906,gfx908,gfx90a,gfx942,gfx1010,gfx1030,gfx1032,gfx1100,gfx1101,gfx1102`.
- Source: https://github.com/ggml-org/llama.cpp/issues/14734 — "Regarding the build for 8060S (gfx1151)" — confirms gfx1151 (Radeon 8060S / Strix Halo iGPU) has had open build questions/issues. Not deep-fetched.

---

## 2. GGUF Quantization Tradeoffs (Q4_K_M vs Q5_K_M vs Q6_K vs Q8_0)

- Source: https://github.com/ggml-org/llama.cpp/discussions/2094 (official llama.cpp quantization help discussion)
  - Quoted quant table (7B reference model):
    - Q4_K_M: "3.80G, +0.0535 ppl @ 7B - medium, balanced quality - *recommended*"
    - Q5_K_M: "4.45G, +0.0142 ppl @ 7B - large, very low quality loss - *recommended*"
    - Q6_K: "5.15G, +0.0044 ppl @ 7B - very large, extremely low quality loss"
    - Q8_0: "6.70G, +0.0004 ppl @ 7B - very large, extremely low quality loss - not recommended" (not recommended specifically because of size/speed cost for the ppl gain, not because of quality)
  - Quote: "K-quantizations should be better, at the same file size, then the other ones. S M L means small medium large."
  - Paraphrase: three variants get an explicit "recommended" label in this thread: Q4_K_M, Q5_K_S, Q5_K_M.
  - Quote (paraphrased reasoning against always using the largest format): larger uncompressed formats aren't recommended for typical use despite minimal quality loss because "they will use much more ram and run way slower."

- Source: https://arxiv.org/html/2601.14277v1 — "Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct" (arXiv paper, 2026)
  - Table 2 data (as extracted):
    - Perplexity (WikiText-2): Q4_K_M = 7.56, Q5_K_M = 7.40, Q6_K = 7.35, Q8_0 = 7.33
    - Benchmark averages (unweighted mean across GSM8K, HellaSwag, IFEval, MMLU, TruthfulQA): Q4_K_M = 69.15, Q5_K_M = 69.36, Q6_K = 69.23, Q8_0 = 69.41
    - Model size reduction vs FP16: Q4_K_M = 69.41%, Q5_K_M = 64.35%, Q6_K = 58.98%, Q8_0 = 46.87%
    - Token-generation throughput (tg128, tok/s) reported in this paper's setup: Q4_K_M = 5.12 ± 0.37, Q5_K_M = 6.85 ± 0.13, Q6_K = 6.33 ± 0.13, Q8_0 = 5.03 ± 0.16 (note: non-monotonic — Q5_K_M fastest in their benchmark, likely hardware/kernel-dependent, flagging as notable/counterintuitive)
  - Quote: "Q5_0 is the accuracy-favoring choice with meaningful compression" and "Q4_K_S is the natural balanced default when stronger reduction is needed" — paper's own headline conclusion that format choice matters beyond nominal bit-width.

- Source: https://runaihome.com/blog/quantization-q4-q5-q6-q8-quality-loss-2026/ — "Q4 vs Q5 vs Q6 vs Q8 Quantization: Real Quality Loss Numbers for Local LLMs (2026)" (blog, not deep-fetched, found via search synthesis)
  - Paraphrase: F16 baseline perplexity for a 7B model ~5.96; Q4_K_M raises it to ~6.01; Q8_0 to ~5.96004. Delta between Q4_K_M and Q8_0 quoted as ~0.0531 ppl points, described as below the threshold of "perceptibly different responses in normal conversation."
  - Paraphrase: Q5_K_M offers "noticeably better quality than Q4 with only ~20% size increase"; quality rating quoted as "+0.003 ppl @ Llama-3-8B."
  - Paraphrase: Q4_K_M described as storing "most sensitive layers at 6-bit, recovering 5–8% quality" at ~4.5GB for a 7B model; Q8_0 ~7.7GB for 7B, "under 0.5% quality loss versus FP16."

- Source: search-synthesized from multiple 2026 blog posts (dev.to/pat9000, bmdpat.com, pristren.com, medium.com/@paul.ilvez, kaitchup.substack.com, vucense.com) — titles/URLs confirmed real via search, not individually deep-fetched:
  - https://dev.to/pat9000/gguf-quantization-explained-q4km-vs-q5km-vs-q8-which-to-pick-2026-31pl
  - https://bmdpat.com/blog/gguf-quantization-q4-q5-q8-explained-2026
  - https://pristren.com/blog/gguf-quantization-guide-2026/
  - https://medium.com/@paul.ilvez/demystifying-llm-quantization-suffixes-what-q4-k-m-q8-0-and-q6-k-really-mean-0ec2770f17d3
  - https://kaitchup.substack.com/p/choosing-a-gguf-model-k-quants-i
  - https://vucense.com/dev-corner/gguf-quantization-explained-q4-k-m-vs-q8-0-vs-f16-2026/
  - https://bmdpat.com/blog/gguf-quant-which-to-pick-2026
  - Paraphrase (aggregate claim across these, not independently verified per-source): Q4_K_M reduces a 7B FP16 model (13.5GB) to ~4.1GB "while retaining approximately 92–95% of full-precision output quality."
  - Paraphrase: a "quality retention" comparison quoted Q4_K_M = 100% (baseline), Q5_K_M = 101.5%, Q6_K = 102%, Q8_0 = 103% — with the claim that "the quality jump from Q4_K_M to Q6_K is larger than from Q6_K to Q8_0."
  - Paraphrase: recommendation surfaced — "If you have 16GB+ VRAM and run code generation, math, or structured output tasks, Q6_K or Q8_0 measurably improves accuracy on precision-sensitive workloads," with "the sweet spot for most people" between Q4_K_M and Q6_K.

- Source: https://mintlify.com/ggml-org/llama.cpp/models/quantizing-models — official-looking llama.cpp docs mirror page "Quantizing Models," surfaced via search, not deep-fetched. UNVERIFIED contents beyond title.

---

## 3. Best Small Open-Weight Models (1B–14B) for Math / Code / Structured Output / Instruction-Following

### Qwen3-4B-Instruct-2507 (the model AMDA currently uses)
- Source: https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 (model card benchmark table)
  - Knowledge: MMLU-Pro 69.6, MMLU-Redux 84.2, GPQA 62.0
  - Reasoning: AIME25 47.4, HMMT25 31.0, ZebraLogic 80.2, LiveBench(20241125) 63.0
  - Coding: LiveCodeBench v6 35.1, MultiPL-E 76.8
  - Alignment/Instruction-following: IFEval 83.4, Arena-Hard v2 43.4, Creative Writing v3 83.5, WritingBench 83.4
  - Agent: BFCL-v3 61.9, TAU1-Retail 48.7, TAU1-Airline 32.0
  - Note: card's table (as extracted) does NOT list GSM8K, plain MMLU, HumanEval, or MBPP directly — those are absent, not zero.

### Qwen3-4B-Thinking-2507 (reasoning/"thinking" variant, same family)
- Source: https://dev.to/lukehinds/qwen3-4b-thinking-2507-just-shipped-4e0n
  - AIME25: "81.3% (up from 65.6%)"
  - HMMT25: "55.5% (up from 42.1%)"
  - GPQA: "65.8% (matching the 30B version)" [paraphrase — comparison to an unspecified "30B version"]
  - LiveCodeBench: "55.2% accuracy on recent programming challenges"
  - CFEval: "1852 points"
  - BFCL-v3 (tool use): "71.2%"
  - MultiIF (multilingual instruction-following): "77.3%"
  - Arena-Hard v2: "from 13.7% to 34.9%"
  - Note: this is a third-party dev.to post about the model launch, not the official HF model card — treat numbers as reported-by-article, not independently cross-checked against Qwen's own card.

- Source: https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/discussions/24 — "Add MMLU-Pro evaluation result" — a HF discussion thread specifically about adding an MMLU-Pro result to the card; confirms MMLU-Pro number provenance is community-contributed/discussed, not necessarily in the original release table. Not deep-fetched for content beyond title.

### Qwen3-4B vs Qwen3-8B (instruction-following / consistency)
- Source: search-synthesized from https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/ and other pages (not individually deep-fetched)
  - Paraphrase: "The 8B models claim the top spots, with Qwen3-8B showing remarkably consistent performance across all benchmarks (lowest standard deviation)."
  - Paraphrase: "Qwen3-4B-Instruct-2507 matches or exceeds the teacher on 7 out of 8 benchmarks" [teacher model unspecified in the snippet — likely referring to a distillation-teacher setup in that specific blog, treat as context-specific, UNVERIFIED generalizability].
  - Paraphrase: one source claims Qwen3-4B "beats Gemma-2-27B and Phi-4-14B on most 2026 leaderboards" for instruction following — UNVERIFIED, no specific numbers or leaderboard named in the snippet.

### Gemma 3 4B
- Source: https://arxiv.org/pdf/2503.19786 / https://arxiv.org/html/2503.19786v1 (Gemma 3 Technical Report, Google DeepMind, March 2025)
  - GSM8K: 38.4 (pretrained/base checkpoint, per search synthesis of the report's STEM/code table)
  - HumanEval: 36.0 (same table)
  - Paraphrase: the instruction-tuned Gemma3-4B-IT is reported to outperform the much larger Gemma2-27B-IT on a range of tasks including STEM/math (GSM8K), code (MBPP, HumanEval), reasoning (MMLU), chat, and instruction-following, attributed to a "novel post-training recipe."
  - Note: these GSM8K/HumanEval numbers (38.4 / 36.0) appear to be for the base/pretrained 4B checkpoint, not necessarily the IT (instruct) variant — the IT-vs-2.7B-comparison claim above is qualitative only in what was extracted. Flag as needing the IT-specific numeric table from the PDF for precision. UNVERIFIED exact IT scores.

### Phi-4-mini (3.8B)
- Source: https://www.datalearner.com/en/ai-models/pretrained-models/Phi-4-mini-instruct/analysis and https://arxiv.org/pdf/2503.01743 (Phi-4-Mini Technical Report)
  - Paraphrase: "Phi-4-mini-instruct (3.8B) shows benchmark results of GSM8K: 88.60, HumanEval: 74.40, and MATH: 64."
  - Paraphrase: "Phi-4 Mini scores GSM8k: 88.6%, ARC-C: 83.7%, BoolQ: 81.2%, OpenBookQA: 79.2%, PIQA: 77.6%."
  - Paraphrase: vs. predecessor Phi-3.5-Mini (also 3.8B) — "+8% MMLU," "+12% MATH," "+6% HumanEval."
  - Paraphrase: "Phi-4-Mini's strong reasoning capabilities are shown on coding tasks, and in the HumanEval benchmark, Phi-4-Mini outperforms most of the similar sized and two times larger sized models" (per datalearner.com summary, exact comparison set not itemized).
  - Separately, a different search (topic on "best small LLM" listicles) surfaced this claim for "Phi-4" (14B, not mini): "84.8% MMLU" and "80.4% on the MATH benchmark," described as "the highest of any local model in its class" — this refers to Phi-4 14B, not Phi-4-mini 3.8B; do not conflate the two. Source: aggregate of localaimaster.com pages found via search (https://localaimaster.com/models/phi-4-mini, https://localaimaster.com/blog/small-language-models-guide-2026), not deep-fetched individually. UNVERIFIED which exact Phi-4 variant the 84.8/80.4 numbers belong to — flagged because two different Phi-4 variants (14B vs mini 3.8B) appeared across different search snippets and could be conflated by less careful reading.

### Llama 3.2 3B Instruct
- Source: search synthesis, exact page among results not singularly attributed (candidates: https://huggingface.co/julien-c/Llama-3.2-1B-Instruct, https://llm-stats.com/models/compare/gemma-3-1b-it-vs-llama-3.2-3b-instruct)
  - Paraphrase: "Llama 3.2 3B Instruct scores 77.7% on GSM8K."
  - No HumanEval number was found for Llama 3.2 3B Instruct in this search round — explicitly noted as not found, not zero.

### DeepSeek-R1-Distill-Qwen (1.5B / 7B)
- Source: https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B, https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B, https://arxiv.org/html/2501.12948v1 (DeepSeek-R1 paper)
  - Paraphrase: distilled checkpoints released at 1.5B, 7B, 8B, 14B, 32B, 70B, based on Qwen2.5 and Llama3 series; distillation "based on Qwen2.5-Math-7B" for the math-focused checkpoints.
  - Paraphrase: "DeepSeek-R1-Distill-Qwen-7B achieves 55.5% on AIME 2024, surpassing QwQ-32B-Preview."
  - Paraphrase: "7B model demonstrates strong performance on MATH-500 with 92.8% pass@1."
  - Paraphrase: "Accuracy drops sharply for the 1.5B model, particularly on tasks demanding multistep logical or symbolic reasoning, while latency improves by approximately 16x. However, middle-tier students (7B–14B–32B–70B) retain a high fraction of teacher performance." (this framing/wording appears to be search-tool synthesis, not a direct DeepSeek quote — treat as paraphrase of a paraphrase, lower confidence.)
  - Paraphrase (separate, on quantized versions): "quantized models achieving over 99% accuracy recovery" on Open LLM Leaderboard V1 benchmarks including GSM8K, per https://developers.redhat.com/articles/2025/03/03/deployment-ready-reasoning-quantized-deepseek-r1-models

### IBM Granite (3.x / 4.x families)
- Source: https://developer.nvidia.com/blog/ibms-new-granite-3-0-generative-ai-models-are-small-yet-highly-accurate-and-efficient/, https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models, https://arxiv.org/pdf/2405.04324 (Granite Code Models paper)
  - Paraphrase: "Granite-8B-Code-Base achieves the best average performance of 34.5% outperforming all other models of similar parameter sizes," and Granite Code models are said to outperform CodeGemma at 2B-3B scale, StarCoder2 at 7B-8B scale, and CodeLlama models "with half of the sizes."
  - Paraphrase: Granite 3.2 8B, "with novel inference scaling methods," is claimed to "rival the performance of much larger models like Claude 3.5 Sonnet or GPT-4o on math reasoning benchmarks such as AIME2024 and MATH500" — UNVERIFIED / marketing-sourced claim (IBM's own announcement), no independent numbers given in the snippet.
- Source: https://research.ibm.com/blog/granite-4-1-ai-foundation-models — "Introducing the IBM Granite 4.1 family of models"
  - Paraphrase: Granite 4.1 released April 29, 2026, dense decoder-only models at 3B / 8B / 30B (base + instruct).
  - Paraphrase: "The Granite 4.1 8B instruct model consistently matches or outperforms the Granite 4.0 32B Mixture-of-Experts model."
  - Numbers quoted (source page for these specific numbers among the Granite 4.1 pages, not singularly pinned — likely https://specpicks.com/reviews/ibm-granite-4-1-local-inference-benchmarks-2026 or https://www.aimadetools.com/blog/granite-4-1-complete-guide/):
    - Granite 4.1 8B: HumanEval 87.2, GSM8K 92.49, EvalPlus 80.2
    - Granite 4.1 30B: BFCL v3 (tool calling) 73.68, ahead of "Gemma-4-31B at 72.7"
- Source: https://huggingface.co/blog/ibm-granite/granite-4-nano — "Granite 4.0 Nano: Just how small can you go?"
  - Quote: "Granite 4.0 H 1B – A ~1.5B parameter, dense LLM featuring a hybrid-SSM based architecture."
  - Quote: "Granite 4.0 H 350M – A ~350M parameter, dense LLM featuring a hybrid-SSM based architecture." (traditional transformer versions also mentioned as available at both sizes.)
  - Paraphrase: evaluated across "General Knowledge, Math, Code, and Safety domains," including "IFEval and Berkley's Function Calling Leaderboard v3 (BFCLv3) benchmarks" — actual numeric scores were in charts/appendix not captured by the fetch; flagged UNVERIFIED for exact numbers on the Nano sizes.

### Other small/candidate models surfaced incidentally (names only, worth follow-up; not deeply researched per task scope which said focus on named families)
- "SuperNova-4B" — mentioned in one search snippet as beating Qwen3-4B "by 21pp on ZebraLogic" (paraphrase, source page not pinned down — search for "SuperNova-4B model card" did NOT surface a matching model card; possible confusion with Arcee's "SuperNova-Medius" 14B model at https://huggingface.co/arcee-ai/SuperNova-Medius, which is a different, larger model). UNVERIFIED — flagging likely search-tool hallucination/conflation risk on "SuperNova-4B" specifically.
- "North Mini Code" (Cohere, 30B-A3B MoE, 3B active params) — https://huggingface.co/blog/CohereLabs/introducing-north-mini-code and https://artificialanalysis.ai/models/north-mini-code
  - Paraphrase: released June 9, 2026, Apache 2.0, runs on one H100 at FP8.
  - Paraphrase: "Artificial Analysis Coding Index" score 33.4, above GLM-4.7-Flash (25.9), below Qwen3.6 35B-A3B (35.2).
  - Paraphrase: Artificial Analysis Intelligence Index "21 (estimated)," vs "median: 9" for similar-sized open models.
  - Paraphrase: throughput "108.6 tokens per second (based on Cohere's API)" vs "median: 100.5 t/s."
  - Note: this is a 30B (3B-active MoE) model, not a dense small model in AMDA's stated 1B-14B target — flagging as borderline-in-scope only via its active-parameter count.

### NER / structured extraction with small models
- Source: search synthesis mentioning arxiv papers and a Medium post — https://arxiv.org/pdf/2505.23038 (EL4NER ensemble learning paper), https://medium.com/@bryan.leezc/named-entity-recognition-ner-trilemma-balancing-cost-latency-accuracy-0be093fc8028
  - Paraphrase: "In 2025 benchmarks, Qwen-2.5-Instruct-7B-Q8_0 performed nearly identically to GPT-4.1-Nano and Gemini-Flash-2.0-Lite on NER tasks." (source page for this specific claim not pinned exactly among results — flag UNVERIFIED provenance though the claim itself was returned by search.)
  - Paraphrase: "NuExtract-3.8B (FP16), a Phi-3 model fine-tuned specifically for extraction, performed decently well" on NER/extraction-type tasks.

### Sentiment analysis with small models
- Paraphrase (source not individually pinned among arxiv results, likely https://arxiv.org/pdf/2601.08302 or a related sentiment-analysis paper): "Qwen2.5-7B-Guba-Senti... achieved 85% three-class accuracy on the test set for sentiment classification of stock commentary data."
- Paraphrase: "Even relatively small 7B-parameter LLaMA 2 models, when properly adapted, can exceed the accuracy of specialized models on detecting positive/negative sentiment in stock news."

### Summarization with small models
- Source: https://ascentcore.com/2026/04/01/small-llm-performance-benchmark/ ("Small LLM Performance Benchmark - Research Report")
  - Paraphrase: "AscentCore evaluated 22 quantized configurations of 11 open-source models from 1B to 14B parameters across six description generation task variants, measuring quality using ROUGE and factual consistency."
  - Paraphrase: "Gemma 3 12B and Phi-3 14B offer ROUGE-L scores (0.433–0.435) below Llama 3.1 8B (0.454)" — i.e., in this benchmark, Llama 3.1 8B outscored both Gemma 3 12B and Phi-3 14B on ROUGE-L for the summarization-type task tested, despite being smaller than one of them.

---

## 4. Community/Practitioner Opinions (Reddit r/LocalLLaMA, Hacker News, Medium) on Best Small Model for Agentic/Tool-Use/Structured Tasks (2026)

- Source: https://www.kdnuggets.com/top-7-coding-models-you-can-run-locally-in-2026
  - Paraphrase: r/LocalLLaMA community "actively testing Qwen3.6 27B MTP for local agentic coding, faster inference, and OpenAI-compatible local servers."
  - Paraphrase: "Qwen3.6 27B MTP" recommended as "a strong all-round local model for coding assistants, repo chat, debugging, shell commands, and agentic workflows," reasoning that "Qwen models are strong at coding because they combine reasoning, instruction following, multilingual understanding, tool use, and long-context support."
  - Paraphrase: "Qwen3.5 9B MTP" flagged as "a proper modern Qwen-style coding assistant while being fast, practical, and much easier to run than the 27B or 31B models."
  - Paraphrase: "Gemma 4 31B IT QAT" — NVIDIA-described as "strong for reasoning and agentic tasks, with both thinking and instruct modes."
  - Paraphrase: "North Mini Code" (Cohere, 30B/3B-active MoE) "offers a balance between stronger reasoning than small models while being more efficient."

- Source: search synthesis referencing a specific community thread — paraphrase: "A May 8 r/ollama thread directly compared Qwen 3.6, Qwen3-Coder, and DeepSeek-Coder, with the Qwen 3.6 family winning across the board on local hardware — the 27B dense for tool-using coding agents, the 35B-A3B MoE for general-purpose work on tighter VRAM." Exact thread URL not surfaced by search (r/ollama, not directly linked) — UNVERIFIED thread existence beyond this paraphrase claim.

- Source: https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026 — "Best Local Models for Tool Calling in 2026: Benchmarks & Comparison"
  - Paraphrase: "Five local models were benchmarked on real MCP tool calls: Gemma 4, GLM-5.1, Qwen3, Qwen3-Coder, and Llama 3.3."
  - Paraphrase: "Qwen3 7B is the best local model for tool calling in 2026 — reliable structured JSON tool calls on 8 GB VRAM," while "Qwen3 32B is recommended" for "highest accuracy and complex multi-tool workflows" on 24GB VRAM.
  - Paraphrase: "All five reliable models emit well-formed function-calling JSON, handle parallel calls, and survive strict schema validation in MCP clients."

- Source: https://www.spheron.network/blog/tool-calling-benchmarks-bfcl-tau-bench-latency-optimization/ — BFCL v4 / tau-Bench context
  - Paraphrase: "BFCL v4 tests whether models can correctly identify which function to call and fill its parameters with valid values," with the "v4 release (April 2026) shifting to a holistic agentic evaluation model covering five major areas."

- Source: https://arxiv.org/html/2604.25359v1 — "The Structured Output Benchmark: A Multi-Source Benchmark for Evaluating Structured Output Quality in Large Language Models"
  - Paraphrase: "Function calling achieves 95-99% accuracy with schema validation, while native structured output with constrained decoding works 100% of the time with schema-valid guarantees." "Prompting strategy matters more than model size according to LLMStructBench" [LLMStructBench name as given in search synthesis — treat as reported name, not independently confirmed spelling/existence].
  - Paraphrase: "A 95% per-call rate over 8 steps lands successfully approximately 66% of the time" — illustrating compounding error in multi-step tool-calling chains (general point, not model-specific).

- No direct Hacker News thread URLs were surfaced by search for "best small local LLM 2026" queries — search results returned blog/listicle articles (dev.to, MindStudio, KDnuggets, InsiderLLM, Medium) rather than HN discussion links. Noting this as a gap: HN-specific threads were not found in this research pass despite multiple query attempts.
  - Articles found (titles/URLs real, not all deep-fetched): https://dev.to/danishashko/the-best-llms-for-agentic-coding-in-2026-real-world-not-just-benchmarks-96n ; https://www.mindstudio.ai/blog/best-open-source-llms-agentic-coding-2026 ; https://insiderllm.com/guides/best-local-coding-models-2026/ ; https://medium.com/data-science-collective/what-is-the-best-local-llm-for-coding-in-2026-8dab3619ff89
  - Paraphrase (from one of the above, exact source not pinned): "GLM-5.2 leads the open-weight field on every source, scoring 51.1 on Artificial Analysis Intelligence Index, 62.1 on SWE-Bench Pro, and 79.65 Coding / 73.33 Agentic on LiveBench." (GLM-5.2 is a large model, out of AMDA's local-size scope, noted for context only.)
  - Paraphrase: "Qwen 3.6 Plus is the strongest overall performer for demanding agentic coding tasks, with the longest context window in the class (1M tokens)."
  - Paraphrase: "The cheapest GPU that runs a genuinely useful local coding assistant in 2026 is the 16GB RTX 5060 Ti (~$429) — it runs Qwen3-Coder 14B at Q5 for tab-complete plus a 30B-A3B model at Q4 for agentic chat." (NVIDIA-specific hardware context, not AMD — noted since it's still relevant to "which local model" framing.)

---

## 5. llama-server Specific Features

- Source: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md (official server README, fetched directly)
  - Health endpoint: `/health` — "HTTP status code 200" with body `{"status": "ok"}` when model loaded/ready; "HTTP status code 503" while model still loading.
  - Slots: server exposes `/slots` for multi-slot processing/monitoring. Related flags: `--cache-prompt` (prompt caching / KV cache reuse across requests), `--cache-reuse` (minimum chunk size for cache reuse via KV shifting), `--slot-save-path` (save/restore slot KV cache to files). Per-slot metrics tracked include processing speed and sampling parameters.
  - `--jinja` flag: enables Jinja templating engine for chat formatting; quote: "Tool use requires --jinja flag." Custom templates also settable via `--chat-template` / `--chat-template-file`.
  - OpenAI-compatible endpoints: `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models`. Quote: "OpenAI API compatible chat completions, responses, and embeddings routes."
  - Docker-relevant flags: `-c/--ctx-size N` (context window), `-n/--n-predict N` (max generated tokens), `-ngl/--n-gpu-layers N` (GPU layer offload — "either an exact number, 'auto', or 'all'"), `-t/--threads N` (CPU threads), `--host` (default `127.0.0.1`), `--port` (default `8080`).
  - Example docker invocation pattern quoted: `docker run -p 8080:8080 ... --host 0.0.0.0 --port 8080`.

- Source: https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md — dedicated function-calling doc exists (URL confirmed via search, not deep-fetched in this pass — follow-up candidate).

- Source: search synthesis re: `--jinja` and tool calling behavior — paraphrase: "When using --jinja, llama-server appends a system message if tools are supported, instructing the model to 'Respond in JSON format, either with tool_call (a request to call tools) or with response reply to the user's request'." Also: "OpenAI-style function calling is supported with the --jinja flag (and may require a --chat-template)."

- Source: https://github.com/anomalyco/opencode/issues/1890 — "OpenCode sends tools (and Jinja tool template) to llama.cpp results in 500 error unless --jinja; with --jinja, template crashes (reject filter)" — a real third-party bug report describing a gotcha: without `--jinja`, tool-bearing requests 500; with `--jinja`, some chat templates crash on a Jinja "reject" filter. Not deep-fetched beyond title — flag as a concrete known gotcha worth following up if AMDA uses tool-calling via llama-server.

### Docker-specific gotchas (missing shared libraries)
- Source: https://github.com/ggml-org/llama.cpp/issues/7731 (fetched directly)
  - Exact error quoted: "/main: error while loading shared libraries: libgomp.so.1: cannot open shared object file: No such file or directory"
  - Paraphrase: root cause is a missing GNU OpenMP runtime (`libgomp.so.1`) inside the Docker image, reproduced "even with CUDA and nvidia-container-toolkit properly installed."
  - Note: the referenced fix PR is #7780 (issue text pointed to a closed PR by that number for resolution — exact PR content not independently fetched in this pass).
- Source: https://github.com/ggml-org/llama.cpp/pull/7775 — "Fix missing libgomp.so.1 Error in Docker Container for llama.cpp" (by 0x4139) — paraphrase: fix "involves adding the installation of libgomp1 to the Dockerfile" via apt-get.
- Source: https://github.com/oobabooga/textgen/issues/6917 — same libgomp.so.1 error reported in a different downstream project's Docker setup (oobabooga/text-generation-webui), confirming this is a recurring cross-project gotcha, not a one-off.
- Source: https://github.com/fboulnois/llama-cpp-docker/issues/8 — same libgomp.so.1 error reported in a third independent community Docker packaging of llama.cpp.
- Other adjacent shared-library errors found (titles/URLs real, confirming this class of Docker issue is common across llama.cpp acceleration backends, not deep-fetched individually):
  - https://github.com/ggml-org/llama.cpp/issues/9416 — SYCL-Dockerfile build, `libllama.so` load error after build.
  - https://github.com/ggml-org/llama.cpp/discussions/9073 — CUDA docker image fails with "error while loading shared libraries."
  - https://github.com/ggml-org/llama.cpp/issues/11123 and /issues/11267 — `libllama.so: cannot open shared object file` in llama-cli.
  - https://github.com/ggml-org/llama.cpp/issues/7822 — "CUDA enabled docker container fails to launch."
  - https://github.com/ggml-org/llama.cpp/issues/17193 — `libmtmd.so.0: cannot open shared object file` with server-cuda Docker image.
  - https://github.com/leejet/stable-diffusion.cpp/issues/400 — same libgomp.so.1-missing-in-Docker pattern in a sibling ggml-based project (stable-diffusion.cpp), reinforcing this is a ggml/Dockerfile-base-image pattern, not llama.cpp-specific.

### Official Docker image docs
- Source: https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md (fetched directly)
  - Three core image variants quoted: "Full" — "This image includes both the llama-cli and llama-completion executables and the tools to convert LLaMA models"; "Light" — "This image only includes the llama-cli and llama-completion executables"; "Server" — "This image only includes the llama-server executable."
  - Platforms supported: linux/amd64, linux/arm64, linux/s390x.
  - GPU-enabled variants exist for CUDA (12 & 13), ROCm, MUSA, SYCL (Intel), Vulkan, OpenVino. Quote: "The GPU enabled images are not currently tested by CI beyond being built." (i.e., GPU Docker images are build-tested only, not runtime-tested by CI — a notable caveat for reliability planning.)
  - CUDA quote: "Assuming one has the nvidia-container-toolkit properly installed on Linux, or is using a GPU enabled cloud, cuBLAS should be accessible inside the container."
  - MUSA note: must "set mthreads as default Docker runtime" before execution.
  - SYCL/Intel note: requires device mounting (`--device /dev/dri/...`) and "You may need to install Intel GPU driver on the host machine."
  - `--n-gpu-layers` flag needed to actually offload to GPU when using an accelerated image.

### Model loading / cold-start speed (relevant to AMDA's <60s boot requirement)
- Source: search synthesis (specific attributing page among https://markaicode.com/integrate/docker-with-llamacpp/, https://markaicode.com/tutorial/llamacpp-docker-deployment/, https://oneuptime.com/blog/post/2026-02-08-how-to-run-llm-inference-with-llamacpp-in-docker/view — not individually pinned)
  - Paraphrase: "Using mmap model loading reduces cold-start from 60 seconds to under 2 seconds on an NVMe drive."
  - Paraphrase: "Without memory mapping, llama.cpp loads the entire file into RAM, which takes 40+ seconds for a 7B Q4 model."
  - Paraphrase: "For Docker deployments, the healthcheck configuration typically uses a 40-second start period to allow the container adequate time to initialize and load the model before health checks begin."
  - Paraphrase: recommendation surfaced to explicitly ensure mmap is enabled (i.e., do not pass `--no-mmap`) for faster startup — flagged UNVERIFIED exact flag semantics/default, worth checking directly against current llama.cpp CLI docs before relying on it.
- Source: https://www.docker.com/blog/llama-cpp-pulls-gguf-models-from-docker-hub/ and https://www.docker.com/blog/llama-cpp-resumable-gguf-downloads/ — official Docker blog posts confirming llama.cpp can pull GGUF models directly from Docker Hub / has resumable GGUF downloads as a docker-model-runner feature. Titles/URLs confirmed via search, not deep-fetched for detail.

---

## 6. Tokens/Second Throughput — CPU (10-16 threads) and AMD GPU (ROCm) for 4B-8B Models

### CPU threading behavior (general, not model-specific unless noted)
- Source: search synthesis (candidates: https://notes.suhaib.in/docs/tech/latest/cracking-the-code-of-llamacpp-optimizing-threads-batch-size-and-context-for-peak-performance/, https://markaicode.com/benchmarks/tool-cpu-benchmark/, https://johannesgaessler.github.io/llamacpp_performance — not individually pinned per claim)
  - Paraphrase: "Benchmarks show that performance peaks at eight threads — the exact number of physical cores. When you push beyond that, the memory bandwidth gets saturated, and additional threads end up competing for the same limited pipeline."
  - Paraphrase: "Scaling from 4 to 12 threads shows linear improvements up to 8 threads, then diminishing returns after 10 threads," with best performance when thread count = physical core count (not logical/SMT count).
  - Paraphrase: "There is a noticeable drop in performance when going from 8 to 9 threads" on an example "RX 3700X" [likely Ryzen 7 3700X CPU, name as given in search synthesis] "presumably because [it] only has 8 physical cores."
  - Paraphrase (general CPU inference constraint): "The most important factor for performance is memory bandwidth, and for CPU inference especially, the bandwidth of consumer RAM is much lower compared to the bandwidth of GPU VRAM so the actual CPU doesn't matter much."
  - Paraphrase (hybrid CPU+GPU): "If the model is already running mostly on the GPU, higher CPU thread counts are not automatically better, as opening too many threads causes CPU-side thread contention, scheduling overhead, and context-switching costs to become heavier."

### 7B/8B general CPU numbers (not the specific 4B model, but same size class)
- Source: search synthesis (general, not singularly pinned): "CPU-only inference might get 8-12 tokens per second for 8B models," described as "significantly slower than GPU performance" with "GPU inference... typically 5-10x faster than CPU-only inference."
- Source: search synthesis re: Apple Silicon comparison point (not AMD, noted for scale context only): "On a MacBook M1, llama.cpp can run a quantized LLaMA 7B model at 30 to 50 tokens per second, depending on configuration."
- Source: search synthesis re: Intel MacBook (CPU-only, no GPU accel): "under 10 tok/s for 8B models" — again non-AMD but useful scale reference.

### Qwen3-4B specifically
- Source: search synthesis (page not singularly pinned, GPU not CPU): "One user reported achieving 13.47 tokens/s with Qwen3-4B-Instruct-2507-Q4_K_M using llama.cpp on an Intel GPU with 96% compute utilization." (Intel GPU, not AMD/CPU — noted as closest same-model data point found; flagging that no CPU-specific t/s number for this exact model+quant combo was found in this search round.)
- Source: https://github.com/outsourc-e/qwen36-4090-recipes — "Reproducible llama.cpp configs + per-category quality benches for Qwen3.6-27B on a single RTX 4090" — GitHub repo exists with benchmark configs; paraphrase from search snippet: "using speculative decoding with Qwen3.5-4B as a draft model achieved mean performance of 43 tokens/s and peak of 67 tokens/s on Q4_K_M quantization" — this is for the 27B main model using the 4B as a speculative-decoding draft model on an RTX 4090 (NVIDIA, not AMD) — noted for context on Qwen3.5-4B's role/speed as a draft model specifically, not standalone throughput.
- Explicit note: no CPU-only (10-16 thread) tokens/sec number specifically for Qwen3-4B-Instruct-2507 Q4_K_M was found in this research pass despite dedicated search attempts. This is a gap — flagged for a follow-up direct benchmark run if precise numbers are needed for the submission's performance claims.

### AMD Radeon iGPU numbers (780M, relevant to consumer/mini-PC AMD hardware, and by extension gfx-target adjacency to the hackathon's ROCm/Radeon Jupyter presets)
- Source: search synthesis (candidates: https://zenvanriel.com/ai-engineer-blog/local-ai-integrated-graphics-vulkan-offload/, https://stochasticsandbox.com/posts/deep-dive-mini-pc-local-ai-2026-04-04/, https://medium.com/@techhara/llama-cpp-benchmark-cpu-vs-igpu-93b3cc40ece5 — not individually pinned per number)
  - Paraphrase: "On Q4 quantized 7B parameter models with Vulkan offload, you can expect 12 to 20 tokens per second on the Radeon 780M, and 30 to 50 tokens per second on 3B models."
  - Paraphrase (slightly different range from a second source in the same search): "pushing the same model through Vulkan offload on a Radeon 780M typically gets you into the 8 to 15 tokens per second range" (note: this range and the 12-20 range above are both attributed to Radeon 780M @ Q4 7B in different snippets — inconsistent, flagging both, true figure likely config/context-dependent).
- Source: https://stochasticsandbox.com/posts/deep-dive-mini-pc-local-ai-2026-04-04/ — "Local LLM on a $550 AMD Mini PC: 28B Models at 20 tok/s"
  - Paraphrase: "a MinisForum UM790 Pro running Gemma 4 28B achieved 19.5 tok/s, and Qwen3.5-32B achieved 20.8 tok/s," using "an AMD Ryzen 9 7940HS with Radeon 780M iGPU, 64GB DDR5-5600, and llama.cpp compiled with Vulkan."
  - Paraphrase: Radeon 780M described as found in "Ryzen 7040 and 8040 series chips," "the strongest integrated GPU on the Windows side with twelve RDNA3 compute units."

### Consumer discrete AMD GPU numbers (RX 6800, general reference class for judging-VM-has-AMD-GPU scenario)
- Source: https://llm-tracker.info/howto/AMD-GPUs (search-synthesized, from same page fetched above in section 1)
  - RX 6800 (ROCm, Llama-2-7B Q4_0, 99 GPU layers): pp512 = 1382.74 ± 21.98 t/s (no FA) / 1675.31 ± 13.21 t/s (with FA, both prompt-processing); tg128 = 79.78 ± 0.12 t/s (no FA) / 86.91 ± 0.25 t/s (with FA).
  - Definitional note (from same source): "pp512 measures prompt processing throughput while processing 512 input tokens, while tg128 measures token generation speed while generating 128 tokens continuously. tg128 is closer to everyday perceived speed, while pp512 is better for judging prompt throughput."
  - Note: RX 7600 numbers were specifically searched for but not found in this pass — explicit gap.

---

## Sources (all URLs visited/fetched or surfaced and cited above)

- https://github.com/ggml-org/llama.cpp/discussions/15021
- https://github.com/ikawrakow/ik_llama.cpp/discussions/562
- https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp/README.html
- https://www.mindstudio.ai/blog/running-local-ai-amd-rocm-ollama-lm-studio
- https://lemonade-server.ai/docs/guide/configuration/llamacpp/
- https://rocm.docs.amd.com/en/latest/compatibility/ml-compatibility/llama-cpp-compatibility.html
- https://github.com/mambiux/LLAMA.CPP-ROCm
- https://www.promptquorum.com/local-llms/best-amd-gpus-local-llm
- https://unsloth.ai/docs/get-started/install/amd
- https://unsloth.ai/docs/blog/unleash-the-power-of-amd-official-support-for-unsloth-is-here
- https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/fine_tune/unsloth_Llama3_1_8B_GRPO.html
- https://unsloth.ai/docs/new/changelog
- https://unsloth.ai/
- https://unsloth.ai/docs/blog/unsloth-amd-pytorch-synthetic-data-hackathon
- https://www.cjvirtuc.io/posts/llama-cpp-rocm/
- https://unsloth.ai/docs/models/tutorials/llama-4-how-to-run-and-fine-tune
- https://unsloth.ai/docs/basics/inference-and-deployment/llama-server-and-openai-endpoint
- https://builderai.tools/blog/fine-tuning-llama-3-3-with-unsloth-on-16gb-gpu
- https://github.com/ggml-org/llama.cpp/issues/22364
- https://unsloth.ai/docs/integrations/connections/connect-llama.cpp-to-unsloth-run-ggufs-with-llama-server
- https://medium.com/@jonathan875579/i-tried-running-local-llm-llama-cpp-on-arch-linux-with-an-amd-gpu-f502448fce49
- https://github.com/ggml-org/llama.cpp/discussions/21112
- https://github.com/unslothai/unsloth/issues/5831
- https://www.promptquorum.com/local-llms/llm-quantization-explained
- https://runaihome.com/blog/quantization-q4-q5-q6-q8-quality-loss-2026/
- https://mintlify.com/ggml-org/llama.cpp/models/quantizing-models
- https://arxiv.org/pdf/2601.14277
- https://github.com/ggml-org/llama.cpp/discussions/2094
- https://www.jamesflare.com/quantization-type-llama-cpp/
- https://arxiv.org/html/2601.14277v1
- https://dev.to/pat9000/gguf-quantization-explained-q4km-vs-q5km-vs-q8-which-to-pick-2026-31pl
- https://bmdpat.com/blog/gguf-quantization-q4-q5-q8-explained-2026
- https://pristren.com/blog/gguf-quantization-guide-2026/
- https://medium.com/@paul.ilvez/demystifying-llm-quantization-suffixes-what-q4-k-m-q8-0-and-q6-k-really-mean-0ec2770f17d3
- https://kaitchup.substack.com/p/choosing-a-gguf-model-k-quants-i
- https://vucense.com/dev-corner/gguf-quantization-explained-q4-k-m-vs-q8-0-vs-f16-2026/
- https://bmdpat.com/blog/gguf-quant-which-to-pick-2026
- https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507
- https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/discussions/24
- https://medium.com/@jatingargiitk/all-you-need-to-know-about-qwen2-5-max-cc266858f27d
- https://arxiv.org/pdf/2412.15115
- https://www.emergentmind.com/topics/qwen-2-5-models
- https://arxiv.org/pdf/2409.12186
- https://arxiv.org/pdf/2601.22197
- https://arxiv.org/pdf/2512.15745
- https://arxiv.org/html/2409.12186v3
- https://arxiv.org/pdf/2605.15464
- https://qwenlm.github.io/blog/qwen2.5-llm/
- https://www.researchgate.net/publication/390175982_Gemma_3_Technical_Report
- https://www.gemma4.wiki/benchmark/gemma-4-gsm8k-score
- https://www.emergentmind.com/topics/gemma-3-4b
- https://gemma4-ai.com/blog/gemma4-benchmark
- https://storage.googleapis.com/deepmind-media/gemma/Gemma3Report.pdf
- https://arxiv.org/html/2503.19786v1
- https://namangoyal.com/blog/2025/gemma3/
- https://arxiv.org/pdf/2503.19786
- https://www.datalearner.com/en/ai-models/pretrained-models/Phi-4-mini-instruct/analysis
- https://llm-stats.com/models/compare/phi-4-vs-phi-4-mini
- https://localaimaster.com/models/phi-4-mini
- https://www.labellerr.com/blog/best-small-language-models-under-10b-parameters/
- https://arxiv.org/pdf/2503.01743
- https://www.kdnuggets.com/best-small-language-models-on-hugging-face-right-now
- https://www.microsoft.com/en-us/research/wp-content/uploads/2025/04/phi_4_reasoning.pdf
- https://www.microsoft.com/en-us/research/wp-content/uploads/2024/12/P4TechReport.pdf
- https://arxiv.org/pdf/2412.08905
- https://huggingface.co/microsoft/Phi-4-mini-instruct
- https://llm-stats.com/models/compare/gemma-3-1b-it-vs-llama-3.2-3b-instruct
- https://patmcguinness.substack.com/p/llama-31-405b-70b-and-8b-released
- https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/discussions/81
- https://huggingface.co/julien-c/Llama-3.2-1B-Instruct
- https://medium.com/friendliai/experience-meta-llama-3-1s-outstanding-performance-on-friendli-7fef3510f020
- https://medium.com/@ingridwickstevens/more-llm-acronyms-an-explainer-on-llama-3s-performance-benchmark-values-36722c6dcabb
- https://arxiv.org/pdf/2404.00725
- https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
- https://arxiv.org/pdf/2502.12197
- https://arxiv.org/pdf/2510.22954
- https://arxiv.org/html/2501.12948v1
- https://openrouter.ai/deepseek/deepseek-r1-distill-qwen-7b
- https://www.sitepoint.com/deepseek-r1-open-source-reasoning/
- https://developers.redhat.com/articles/2025/03/03/deployment-ready-reasoning-quantized-deepseek-r1-models
- https://arxiv.org/pdf/2509.00731
- https://www.emergentmind.com/topics/deepseek-r1-distilled-models
- https://arxiv.org/pdf/2603.09803
- https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
- https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
- https://arxiv.org/pdf/2601.09855
- https://ollama.com/library/granite3.3:8b
- https://newsroom.ibm.com/2025-02-26-ibm-expands-granite-model-family-with-new-multi-modal-and-reasoning-ai-built-for-the-enterprise
- https://arxiv.org/pdf/2405.04324
- https://developer.nvidia.com/blog/ibms-new-granite-3-0-generative-ai-models-are-small-yet-highly-accurate-and-efficient/
- https://www.ibm.com/new/announcements/ibm-granite-3-0-open-state-of-the-art-enterprise-models
- https://huggingface.co/ibm-granite/granite-3.3-8b-instruct
- https://www.ibm.com/new/announcements/ibm-granite-3-2-open-source-reasoning-and-vision
- https://www.infoq.com/news/2025/03/ibm-granite-3-2/
- https://www.ibm.com/granite
- https://research.ibm.com/blog/granite-4-1-ai-foundation-models
- https://www.ibm.com/granite/docs/models/granite
- https://www.aimadetools.com/blog/granite-4-1-complete-guide/
- https://designforonline.com/ai-models/ibm-granite-4-0-micro/
- https://designforonline.com/ai-models/granite-4-0-h-small/
- https://specpicks.com/reviews/ibm-granite-4-1-local-inference-benchmarks-2026
- https://www.ibm.com/new/announcements/ibm-granite-4-0-hyper-efficient-high-performance-hybrid-models
- https://artificialanalysis.ai/models/granite-4-1-30b
- https://huggingface.co/blog/ibm-granite/granite-4-nano
- https://www.kdnuggets.com/top-7-coding-models-you-can-run-locally-in-2026
- https://dev.to/danishashko/the-best-llms-for-agentic-coding-in-2026-real-world-not-just-benchmarks-96n
- https://huggingface.co/blog/daya-shankar/open-source-llms
- https://www.mindstudio.ai/blog/best-open-source-llms-agentic-coding-2026
- https://www.compute-market.com/blog/best-gpu-local-coding-llm-2026
- https://www.buildmvpfast.com/articles/best-llms-2026-guide/coding-ai
- https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/
- https://insiderllm.com/guides/best-local-coding-models-2026/
- https://medium.com/data-science-collective/what-is-the-best-local-llm-for-coding-in-2026-8dab3619ff89
- https://zenvanriel.com/ai-engineer-blog/local-ai-integrated-graphics-vulkan-offload/
- https://github.com/ggml-org/llama.cpp/discussions/10879
- https://openbenchmarking.org/test/pts/llama-cpp
- https://stochasticsandbox.com/posts/deep-dive-mini-pc-local-ai-2026-04-04/
- https://medium.com/@techhara/llama-cpp-benchmark-cpu-vs-igpu-93b3cc40ece5
- https://blog.lewman.com/a-537-local-llm-machine.html
- https://forum.radxa.com/t/llama-cpp-benchmarks/27813
- https://news.ycombinator.com/item?id=38081579
- https://unsloth.ai/docs/models/tutorials/qwen3-how-to-run-and-fine-tune/qwen3-2507
- https://arxiv.org/pdf/2604.18556
- https://arxiv.org/pdf/2603.17946
- https://huggingface.co/byteshape/Qwen3-4B-Instruct-2507-GGUF
- https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF
- https://inference.readthedocs.io/en/latest/models/builtin/llm/qwen3-thinking.html
- https://unsloth.ai/docs/get-started/unsloth-model-catalog
- https://arxiv.org/pdf/2601.05752
- https://huggingface.co/unsloth/Qwen3.5-4B-GGUF
- https://unsloth.ai/docs/models/qwen3.5/gguf-benchmarks
- https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md
- https://fossies.org/linux/llama.cpp/tools/server/README.md
- https://dev.to/avatsaev/pro-developers-guide-to-local-llms-with-llamacpp-qwen-coder-qwencode-on-linux-15h
- https://www.glukhov.org/llm-hosting/llama-cpp/
- https://docs.agno.com/models/providers/local/llama-cpp/overview
- https://llama-cpp-python.readthedocs.io/en/latest/server/
- https://github.com/anomalyco/opencode/issues/1890
- https://github.com/ggml-org/llama.cpp/pull/7775
- https://github.com/oobabooga/textgen/issues/6917
- https://github.com/ggml-org/llama.cpp/issues/7731
- https://github.com/fboulnois/llama-cpp-docker/issues/8
- https://app.semanticdiff.com/gh/ggerganov/llama.cpp/pull/7775/overview
- https://github.com/abetlen/llama-cpp-python/issues/1507
- https://github.com/leejet/stable-diffusion.cpp/issues/400
- https://github.com/ggml-org/llama.cpp/issues/9416
- https://github.com/abetlen/llama-cpp-python/issues/1169
- https://github.com/ggml-org/llama.cpp/discussions/4167
- https://www.sandgarden.com/learn/llama-cpp
- https://github.com/ggml-org/llama.cpp/issues/34
- https://www.sitepoint.com/breaking-the-speed-limit-strategies-for-17k-tokens-sec-local-inference/
- https://llm-tracker.info/howto/LLM-Inference-Benchmarking-Cheat%E2%80%91Sheet-for-Hardware-Reviewers
- https://singhajit.com/llm-inference-speed-comparison/
- https://github.com/ggml-org/llama.cpp/discussions/8273
- https://github.com/ggml-org/llama.cpp/issues/9073 (note: cited above as a discussion, listed here per original search hit format)
- https://github.com/ggml-org/llama.cpp/issues/11123
- https://github.com/ggml-org/llama.cpp/issues/17193
- https://github.com/ggml-org/llama.cpp/issues/7822
- https://github.com/ggml-org/llama.cpp/issues/10588
- https://github.com/ggml-org/llama.cpp/issues/11267
- https://www.docker.com/blog/llama-cpp-pulls-gguf-models-from-docker-hub/
- https://github.com/ggml-org/llama.cpp
- https://www.docker.com/blog/llama-cpp-resumable-gguf-downloads/
- https://markaicode.com/integrate/docker-with-llamacpp/
- https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md
- https://markaicode.com/tutorial/llamacpp-docker-deployment/
- https://oneuptime.com/blog/post/2026-02-08-how-to-run-llm-inference-with-llamacpp-in-docker/view
- https://hub.docker.com/r/dustynv/llama_cpp
- https://huggingface.co/docs/hub/gguf-llamacpp
- https://rocm.docs.amd.com/projects/llama-cpp/en/docs-26.02/install/llama-cpp-install.html
- https://rocm.docs.amd.com/projects/llama-cpp/en/docs-25.08/install/llama-cpp-install.html
- https://hub.docker.com/r/rocm/llama.cpp
- https://rocm.docs.amd.com/projects/llama-cpp/en/docs-25.09/install/llama-cpp-install.html
- https://raw.githubusercontent.com/ggml-org/llama.cpp/master/docs/build.md
- https://github.com/ggml-org/llama.cpp/issues/13340
- https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- https://github.com/ggml-org/llama.cpp/issues/14734
- https://llm-stats.com/benchmarks/zebralogic
- https://huggingface.co/blog/yuchenlin/zebra-logic
- https://arxiv.org/html/2502.01100v1
- https://ageofllms.com/ai-news/llms/logic-puzzles-llms-benchmark
- https://www.marktechpost.com/2024/07/20/zebralogic-a-logical-reasoning-ai-benchmark-designed-for-evaluating-llms-with-logic-puzzles/
- https://arxiv.org/html/2604.08477
- https://openreview.net/forum?id=sTAJ9QyA6l
- https://sophon.at/tools/openreward-generalreasoning-zebra
- https://aclanthology.org/2025.acl-long.664.pdf
- https://unsloth.ai/docs/models/qwen3.5
- https://qwen.readthedocs.io/en/latest/getting_started/speed_benchmark.html
- https://www.aimagicx.com/blog/local-ai-models-2026-qwen-mistral-llama-hardware-guide
- https://localllm.in/blog/llamacpp-vram-requirements-for-local-llms
- https://github.com/ggml-org/llama.cpp/discussions/20969
- https://github.com/outsourc-e/qwen36-4090-recipes
- https://www.articsledge.com/post/named-entity-recognition-ner
- https://aiportalx.com/models/task/named-entity-recognition-ner
- https://arxiv.org/pdf/2403.13737
- https://arxiv.org/pdf/2505.23038
- https://arxiv.org/pdf/2510.11537
- https://medium.com/@bryan.leezc/named-entity-recognition-ner-trilemma-balancing-cost-latency-accuracy-0be093fc8028
- https://link.springer.com/article/10.1007/s40747-025-02074-6
- https://arxiv.org/pdf/2308.03279
- https://arxiv.org/pdf/2402.18041
- https://arxiv.org/pdf/2312.08495
- https://www.clickrank.ai/llm-leaderboard/
- https://acecloud.ai/blog/best-open-source-llms/
- https://localaimaster.com/blog/small-language-models-guide-2026
- https://techsy.io/en/blog/best-open-source-llms-2026
- https://computingforgeeks.com/open-source-llm-comparison/
- https://iternal.ai/llm-selection-guide
- https://arxiv.org/pdf/2505.06947
- https://arxiv.org/pdf/2601.08302
- https://arxiv.org/pdf/2601.03940
- https://baeseokjae.github.io/posts/best-local-llm-models-2026/
- https://awesomeagents.ai/leaderboards/small-language-model-leaderboard/
- https://ascentcore.com/2026/04/01/small-llm-performance-benchmark/
- https://arxiv.org/pdf/2512.06266
- https://arxiv.org/pdf/2601.02752
- https://huggingface.co/arcee-ai/SuperNova-Medius
- https://ai.google.dev/gemma/docs/core/model_card_4
- https://arxiv.org/pdf/2509.07260
- https://build.nvidia.com/nvidia/nemotron-3-super-120b-a12b/modelcard
- https://arxiv.org/pdf/2606.05250
- https://arxiv.org/pdf/2508.21113
- https://arxiv.org/pdf/2601.02186
- https://artificialanalysis.ai/models/north-mini-code
- https://sebastianraschka.com/blog/2026/north-mini-code-agentic-coding.html
- https://huggingface.co/blog/CohereLabs/introducing-north-mini-code
- https://toolsclaw.com/blogs/north-mini-code-developer-guide
- https://explainx.ai/blog/cohere-north-mini-code-open-source-agentic-coding-2026
- https://petronellatech.com/blog/cohere-north-mini-code-benchmarked-top-tier-open-source-ai-coding-that-stays-on-your-network/
- https://openrouter.ai/cohere/north-mini-code:free
- https://designforonline.com/ai-models/cohere-north-mini-code/
- https://www.developersdigest.tech/blog/cohere-north-mini-code-open-weight-coding-model
- https://dev.to/lukehinds/qwen3-4b-thinking-2507-just-shipped-4e0n
- https://www.communeify.com/en/blog/qwen3-4b-thinking-2507-256k-context-reasoning/
- https://artificialanalysis.ai/models/qwen3-4b-2507-instruct-reasoning
- https://lmstudio.ai/models/qwen/qwen3-4b-thinking-2507
- https://www.kaggle.com/datasets/naviniklag/qwen3-4b-thinking-2507
- https://huggingface.co/Qwen/Qwen3-4B-Thinking-2507
- https://qwenlm.github.io/blog/qwen2.5-math/
- https://forum.proxmox.com/threads/tutorial-run-llms-using-amd-gpu-and-rocm-in-unprivileged-lxc-container.157920/page-2
- https://rocm.docs.amd.com/projects/radeon/en/latest/docs/advanced/vllm/build-docker-image.html
- https://oxomichael.github.io/en/posts/2026-03-22-ai-local-llamacpp-opencode/
- https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.0.2/install/3rd-party/llama-cpp-install.html
