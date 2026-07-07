# LLM Routing, Cascade, and Self-Consistency Research Log — AMDA Track 1

Research collection only. Raw facts with URLs and quotes/paraphrases. No synthesis, no recommendations, no strategy conclusions. Paraphrases are marked as such; direct quotes are in quotation marks. UNVERIFIED labels are used where a fetch tool could not confirm details independently.

Context note on dates: searches were run under a system clock reporting current date 2026-07-07. Some "2026"-dated arXiv IDs and blog posts appearing below (e.g. 2605.xxxxx, 2606.xxxxx, 2601-2604.xxxxx) reflect that ambient date. These are reported as found; I have not independently verified server-side timestamps beyond what the arXiv abstract pages themselves state.

---

## 1. "LLM cascade" routing papers on arXiv (2024-2026)

### FrugalGPT
- URL: https://arxiv.org/abs/2305.05176
- Authors: Lingjiao Chen, Matei Zaharia, James Zou (Stanford). Submitted May 9, 2023.
- Quote (verbatim, abstract): "we outline and discuss three types of strategies that users can exploit to reduce the inference cost associated with using LLMs: 1) prompt adaptation, 2) LLM approximation, and 3) LLM cascade. As an example, we propose FrugalGPT, a simple yet flexible instantiation of LLM cascade which learns which combinations of LLMs to use for different queries in order to reduce cost and improve accuracy. Our experiments show that FrugalGPT can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost."
- Confirmed real: yes, canonical arXiv record with full abstract retrieved directly.

### RouteLLM
- URL: https://arxiv.org/abs/2406.18665
- Authors: Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed Kadous, Ion Stoica. v1 submitted June 26, 2024. Published at ICLR (Thirteenth International Conference on Learning Representations, per search result).
- Quote (verbatim, abstract): "we propose several efficient router models that dynamically select between a stronger and a weaker LLM during inference, aiming to optimize the balance between cost and response quality... Our evaluation on widely-recognized benchmarks shows that our approach significantly reduces costs—by over 2 times in certain cases—without compromising the quality of responses. Interestingly, our router models also demonstrate significant transfer learning capabilities, maintaining their performance even when the strong and weak models are changed at test time."
- Confirmed real: yes.

### Hybrid LLM (Cost-Efficient and Quality-Aware Query Routing)
- URL: https://arxiv.org/abs/2404.14618
- Authors: Dujian Ding, Ankur Mallick, Chi Wang, Robert Sim, Subhabrata Mukherjee, Victor Ruhle, Laks V.S. Lakshmanan, Ahmed Hassan Awadallah. Submitted April 22, 2024. Accepted ICLR 2024 main conference (per search result; also listed on Microsoft Research and openreview.net id=02f3mUtqnM).
- Paraphrase (from WebFetch of abstract page): routes queries to either a small or large model based on "predicted query difficulty and the desired quality level"; the quality threshold "can be adjusted dynamically during testing to seamlessly trade quality for cost as per the scenario requirements"; testing found the method could "reduce calls to the large model by up to 40% while maintaining response quality."
- Confirmed real: yes.

### AutoMix
- URL: https://arxiv.org/abs/2310.12963 ; code: https://github.com/automix-llm/automix ; project page: https://automix-llm.github.io/automix/
- Authors: Pranjal Aggarwal, Aman Madaan, Ankit Anand, Srividya Pranavi Potharaju, Swaroop Mishra, Pei Zhou, Aditya Gupta, Dheeraj Rajagopal, Karthik Kappaganthu, Yiming Yang, Shyam Upadhyay, Mausam, Manaal Faruqui. Submitted Oct 19, 2023. Published NeurIPS 2024 (per neurips.cc proceedings PDF link found).
- Paraphrase: "strategically routes queries to larger LMs, based on the approximate correctness of outputs from a smaller LM"; uses "a few-shot self-verification mechanism, which estimates the reliability of its own outputs without requiring extensive training" and "a POMDP based router that can effectively select an appropriately sized model, based on answer confidence." Results: "reducing computational cost by over 50% for comparable performance" across five LMs and five datasets.
- Confirmed real: yes.

### A Unified Approach to Routing and Cascading for LLMs ("cascade routing")
- URL: https://arxiv.org/abs/2410.10347 ; SRI Lab (ETH Zurich) page: https://www.sri.inf.ethz.ch/publications/dekoninck2024cascaderouting
- Authors: Jasper Dekoninck, Maximilian Baader, Martin Vechev. ArXiv ID 2410.10347 (2024).
- Paraphrase: contrasts routing (single model chosen per query) vs. cascading (sequentially runs increasingly larger models until satisfactory); argues existing approaches "lack formal proofs of optimality, fail to identify the conditions under which these strategies are most effective, and are unable to combine both paradigms"; derives "a novel optimal strategy for cascading," proves optimality of an existing routing strategy, and proposes "cascade routing," a unified framework; finds "good quality estimators" are the critical factor; experiments show cascade routing "consistently outperforms individual approaches by a large margin."
- Confirmed real: yes (also on OpenReview id=AAl89VNNy1 and has a PDF at files.sri.inf.ethz.ch).

### Gatekeeper (search-engine title showed as "I Know What I Don't Know: Improving Model Cascades Through Confidence Tuning")
- URL: https://arxiv.org/abs/2502.19335 (also arxiv.org/html/2502.19335v1)
- Authors: Stephan Rabanser, Nathalie Rauschmayr, Achin Kulshrestha, Petra Poklukar, Wittawat Jitkrittum, Sean Augenstein, Congchao Wang, Federico Tombari. v1 submitted Feb 26, 2025; v3 revised Oct 23, 2025.
- Note: the WebFetch of the abstract page returned the actual paper title as "Gatekeeper: Improving Model Cascades Through Confidence Tuning" — different from the search-result-displayed title "I Know What I Don't Know..." This discrepancy is UNVERIFIED as to which is the canonical current title (possibly a title change between versions); flagging directly.
- Quote (verbatim, abstract): "In this work we introduce a novel loss function called Gatekeeper for calibrating smaller models in cascade setups. Our approach fine-tunes the smaller model to confidently handle tasks it can perform correctly while deferring complex tasks to the larger model... Experiments across image classification, language modeling, and vision-language tasks show that our approach substantially improves deferral performance."
- Confirmed real: yes, but title discrepancy noted above is UNVERIFIED.

### UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing
- URL: https://arxiv.org/abs/2605.18796 (also arxiv.org/pdf/2605.18796)
- Author: Varun Kotte (single-author, per fetch). Submitted May 11, 2026.
- Paraphrase: introduces UCCI, "uses calibrated uncertainty scores to decide when queries should be escalated from smaller to larger language models"; "employs isotonic regression to convert token-level margin uncertainty into per-query error probabilities and applies constrained cost minimization to select escalation thresholds." On a production NER workload (75,000 queries, 4B vs 12B instruction-tuned LLMs on H100 GPUs): "31% reduction in inference costs (95% confidence interval: 27-35%) while maintaining micro-F1 score of 0.91," outperforming "entropy thresholding, split-conformal routing, and learned threshold approaches," reducing calibration error "from 0.12 to 0.03."
- Confirmed real: appears on arXiv with abstract fetched directly; single-author production-style paper — UNVERIFIED whether peer-reviewed/published anywhere beyond arXiv.

### Cluster, Route, Escalate: Cascaded Framework for Cost-Aware LLM Serving
- URL: https://arxiv.org/abs/2606.27457 (also arxiv.org/html/2606.27457)
- Authors: Yasmin Moslem, Magdalena Kacmajor, Vasudevan Nedumpozhimana, Ammar Abbas, Solmaz Panahi, David Lynch, Zhuangzhuang Nie, Alexandros Agapitos, Aleksandar Milenovic, Hongmeng Song, Yucheng Shi, Yue Pan, Patricia Buffini, John D. Kelleher. Submitted June 25, 2026.
- Paraphrase: two-stage system — Stage 1 clusters incoming requests, routes each cluster to "the most cost-effective model" under a tunable budget parameter; Stage 2 quality-assesses Stage 1 output and escalates to stronger models when insufficient. Claims to maintain "97-99% of the strongest model's accuracy while reducing Time Per Output Token," requiring only correctness labels (no manual re-tuning when models change).
- Confirmed real: yes, arXiv abstract fetched directly.

### Is Escalation Worth It? A Decision-Theoretic Characterization of LLM Cascades
- URL: https://arxiv.org/abs/2605.06350 (pdf: arxiv.org/pdf/2605.06350, html: arxiv.org/html/2605.06350)
- Author found via search: Dylan Bouchard (single author per search-derived summary; not independently cross-checked via direct abstract-page fetch, so name is UNVERIFIED pending direct fetch).
- Paraphrase (from search-engine-summarized abstract): "Model cascades, in which a cheap LLM defers to an expensive one on low-confidence queries, are widely used to navigate the cost-quality tradeoff at deployment. Existing approaches largely treat the deferral threshold as an empirical hyperparameter..." Develops "a decision-theoretic framework grounded in constrained optimization and duality, establishing piecewise concavity of the cost-quality frontier for two-model cascades." For a pool of k models, "characterizes the frontier achievable by deterministic two-model threshold cascades as the pointwise envelope over pairwise cascades." Validated on MATH, MMLU, TriviaQA, SimpleQA, LiveCodeBench across eight models from five providers; finds "cascade performance is limited primarily by structural cost, since cascades pay the cheap model before any escalation decision, rather than by a shortage of intermediate stages."
- Confirmed real: appears in multiple independent search hits (arxiv.org/pdf, arxiv.org/html) — treat as real; author attribution UNVERIFIED (not fetched directly from abstract page).

### Semantic Agreement Enables Efficient Open-Ended LLM Cascades
- URL: https://arxiv.org/abs/2509.21837 ; also ACL Anthology: https://aclanthology.org/2025.emnlp-industry.171/
- Authors: Duncan Soiffer, Steven Kolawole, Virginia Smith (Carnegie Mellon University), per search-engine abstract summary.
- Paraphrase: proposes "semantic agreement—meaning-level consensus between ensemble outputs—as a training-free signal for reliable deferral," arguing that when diverse model outputs agree semantically, "their consensus is a stronger reliability signal than token-level confidence." Evaluated from 500M to 70B-parameter models: "semantic cascades match or surpass target-model quality at 40% of the cost and reduce latency by up to 60%." Requires no model internals, works across black-box APIs, robust to model updates.
- Confirmed real: yes — cross-confirmed by EMNLP Industry Track 2025 Anthology listing.

### C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning
- URL: https://arxiv.org/abs/2511.07396 (also arxiv.org/html/2511.07396v1)
- Authors: Antonios Valkanas, Soumyasundar Pal, Pavel Rumiantsev, Yingxue Zhang, Mark Coates. Submitted Nov 10, 2025. Poster at NeurIPS 2025 (per neurips.cc/virtual/2025/poster/116958) and OpenReview id=e4IlBqhbTO.
- Quote/paraphrase (verbatim fragment from fetch): a self-supervised cascade framework where "small, cheap models handle easy queries, and only the hardest examples are escalated to more powerful models." Minimizes regret without labeled data, "uses conformal prediction for cost control," provides theoretical guarantees on generalization and cost. Tested on GSM8K, MATH-500, BigBench-Hard, AIME.
- Confirmed real: YES — this name was explicitly requested to be checked for existence in the task brief; confirmed as a real, NeurIPS-2025-accepted paper (not to be confused with any unrelated same-acronym work).

### SATER: A Self-Aware and Token-Efficient Approach to Routing and Cascading
- URL: https://arxiv.org/abs/2510.05164 ; ACL Anthology (EMNLP 2025 main): https://aclanthology.org/2025.emnlp-main.531/
- Authors: Yuanzhe Shen, Yide Liu, Zisu Huang, Ruicheng Yin, Xiaoqing Zheng, Xuanjing Huang. Submitted Oct 4, 2025.
- Quote (verbatim fragment): "LLMs demonstrate remarkable performance across diverse tasks, yet their effectiveness frequently depends on costly commercial APIs." SATER combines "fine-tuning with preference optimization and confidence-based rejection mechanisms." Two-stage training: Stage I preference optimization using shortest-correct/longest-incorrect responses; Stage II prompt-based fine-tuning teaching the SLM to reject complex tasks. At inference, rejected queries go directly to LLMs (pre-generation mode) or via weighted majority voting (cascade mode). Claims: "achieves comparable performance while consistently reducing computational costs by over 50% and cascade latency by over 80%."
- Confirmed real: yes, cross-confirmed via ACL Anthology EMNLP 2025 listing.

### Routoo: Learning to Route to Large Language Models Effectively
- URL: https://arxiv.org/abs/2401.13979 (also export.arxiv.org/abs/2401.13979v2, openreview.net id=RQ9fQLEajC)
- Submitted Jan 25, 2024; latest version Oct 2, 2024.
- Paraphrase: comprises "a performance predictor and cost-aware selector"; the predictor is "a lightweight LLM that estimates the expected performance of various underlying LLMs on a given prompt without executing them"; the selector picks the most suitable model given cost/latency constraints. Results: "Routoo matches the performance of the Mixtral 8x7b model while reducing inference costs by one-third. When integrating GPT4 into the model pool, Routoo nearly matches GPT4's performance at half the cost and exceeds it with a 25% cost reduction."
- Confirmed real: yes.

### Universal Model Routing for Efficient LLM Inference (UniRoute)
- URL: https://arxiv.org/abs/2502.08773 (html: arxiv.org/html/2502.08773v1)
- Authors: Wittawat Jitkrittum, Harikrishna Narasimhan, Ankit Singh Rawat, Jeevesh Juneja, Congchao Wang, Zifeng Wang, Alec Go, Chen-Yu Lee, Pradeep Shenoy, Rina Panigrahy, Aditya Krishna Menon, Sanjiv Kumar (Google). v1 Feb 12, 2025; v2 revised July 22, 2025.
- Quote (verbatim, abstract): "Model routing is a simple technique for reducing the inference cost of large language models (LLMs), wherein one maintains a pool of candidate LLMs, and learns to route each prompt to the smallest feasible LLM. Existing works focus on learning a router for a fixed pool of LLMs. In this paper, we consider the problem of dynamic routing, where new, previously unobserved LLMs are available at test time. We propose UniRoute... Experiments on a range of public benchmarks show the effectiveness of UniRoute in routing amongst more than 30 unseen LLMs."
- Confirmed real: yes.

### Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey
- URL: https://arxiv.org/abs/2603.04445 (pdf: arxiv.org/pdf/2603.04445)
- Authors: Yasmin Moslem, John D. Kelleher. v1 Feb 23, 2026; v2 revised Apr 21, 2026.
- Paraphrase: surveys routing paradigms — "query difficulty assessment, human preferences, clustering, uncertainty measurement, reinforcement learning, multimodality, and cascading methods." Presents a framework characterizing routing systems along three dimensions: "decision timing, information utilized, and computational methods." Quote (verbatim fragment): "well-designed routing systems can outperform even the most powerful individual models by strategically leveraging specialized capabilities across models while maximizing efficiency gains."
- Confirmed real: yes. NOTE: same first author (Yasmin Moslem) and co-author (John D. Kelleher) as the "Cluster, Route, Escalate" paper above — this survey and that applied paper appear to be from the same research group, published ~4 months apart.

### Arch-Router: Aligning LLM Routing with Human Preferences
- URL: https://arxiv.org/abs/2506.16655 ; model: https://huggingface.co/katanemo/Arch-Router-1.5B ; code: https://github.com/katanemo/archgw
- Authors: Co Tran, Salman Paracha, Adil Hafeez, Shuguang Chen. Submitted June 19, 2025.
- Paraphrase: "a compact 1.5B model that learns to map queries to domain-action preferences for model routing decisions," matching queries to user-defined domains (e.g., travel) or action types (e.g., image editing); "supports seamlessly adding new models for routing without requiring retraining or architectural modifications." Claimed SOTA on conversational routing datasets vs. proprietary models.
- Also seen on Hacker News (Show HN) — see Section 5 below for HN threads about this same project (66 points / 15 comments and a separate 1-point/0-comment submission).
- Confirmed real: yes.

### Awesome-Routing-LLMs (curated list / taxonomy, not a paper but a survey resource)
- URL: https://github.com/MilkThink-Lab/Awesome-Routing-LLMs
- Paraphrase (from WebFetch summary): organizes LLM routing papers into three paradigms — "Pre-judgment Routing" (decisions before generation: e.g. CARROT, xRouter, EmbedLLM, RadialRouter, RouteLLM, BEST-Route), "Verification Routing" (adaptive during generation: e.g. RelayLLM, FusionRoute, AutoMix, SATER), and "Memory-based Routing" (e.g. Eagle, ProxRouter, GraphRouter); also covers benchmarks (RouterBench, RouterEval) and safety concerns.
- Note: several of the named systems in this list (CARROT, xRouter, EmbedLLM, RadialRouter, BEST-Route, RelayLLM, FusionRoute, Eagle, ProxRouter, GraphRouter, RouterBench, RouterEval) are UNVERIFIED by me beyond this repo listing — I did not independently fetch/confirm each of these individual papers exists with a real arXiv record. Flagging as UNVERIFIED / not independently checked.

### Other cascade/routing papers surfaced in search but not deep-dived (titles + URLs only, contents UNVERIFIED beyond title)
- "ReLope: KL-Regularized LoRA Probes for Multimodal LLM Routing" — https://arxiv.org/pdf/2603.24787
- "Confidence-Driven Multi-Scale Model Selection for Cost-Efficient Inference" — https://arxiv.org/pdf/2602.22090
- "From Sampled Outcomes to Capability Distributions: Rethinking Supervision for LLM Routing" — https://arxiv.org/pdf/2606.06924
- "Uncertainty Propagation in LLM-Based Systems" — https://arxiv.org/pdf/2604.23505
- "AutoRelAnnotator: Calibrated Model Cascades for Cost-Efficient Relevance Evaluation in Sponsored Search" — https://arxiv.org/pdf/2606.25871
- "Robust Batch-Level Query Routing for Large Language Models under Cost and Capacity Constraints" — https://arxiv.org/pdf/2603.26796
- "Beyond GPT-5: Making LLMs Cheaper and Better via Performance-Efficiency Optimized Routing" — https://arxiv.org/pdf/2508.12631
- "Towards a Cascaded LLM Framework for Cost-effective Human-AI Decision-Making" / "Cascaded Language Models for Cost-Effective Human–AI Decision-Making" — https://arxiv.org/html/2506.11887v2 and v3
- "Reliable LLM-Based Edge-Cloud-Expert Cascades for Telecom Knowledge Systems" — https://arxiv.org/html/2512.20012v1
- "RouteJudge: An Open Platform for Reproducible and Preference-Aware LLM Routing" — https://arxiv.org/pdf/2606.18774
- "Privacy-Preserving LLMs Routing" — https://arxiv.org/pdf/2604.15728
- "Model Routing as a Trust Problem: Route Receipts for Adaptive AI Systems" — https://arxiv.org/html/2605.01710v1
- "vLLM Semantic Router: Signal Driven Decision Routing for Mixture-of-Modality Models" — https://arxiv.org/pdf/2603.04444
- These titles came directly from WebSearch result lists (titles verbatim as returned); I did not fetch their abstracts, so contents beyond the title are UNVERIFIED.

---

## 2. Self-consistency and confidence-estimation for small LLMs

### Self-Consistency Improves Chain of Thought Reasoning in Language Models (the original paper)
- URL: https://arxiv.org/abs/2203.11171
- Authors: Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou. Submitted March 21, 2022 (v1).
- Quote (verbatim, full abstract): "Chain-of-thought prompting combined with pre-trained large language models has achieved encouraging results on complex reasoning tasks. In this paper, we propose a new decoding strategy, self-consistency, to replace the naive greedy decoding used in chain-of-thought prompting. It first samples a diverse set of reasoning paths instead of only taking the greedy one, and then selects the most consistent answer by marginalizing out the sampled reasoning paths. Self-consistency leverages the intuition that a complex reasoning problem typically admits multiple different ways of thinking leading to its unique correct answer. Our extensive empirical evaluation shows that self-consistency boosts the performance of chain-of-thought prompting with a striking margin on a range of popular arithmetic and commonsense reasoning benchmarks, including GSM8K (+17.9%), SVAMP (+11.0%), AQuA (+12.2%), StrategyQA (+6.4%) and ARC-challenge (+3.9%)."
- Confirmed real: yes, canonical/foundational paper (widely cited, ICLR 2023).

### Confidence Improves Self-Consistency in LLMs (CISC)
- URL: https://arxiv.org/abs/2502.06233
- Authors: Amir Taubenfeld, Tom Sheffer, Eran Ofek, Amir Feder, Ariel Goldstein, Zorik Gekhman, Gal Yona. v1 Feb 10, 2025; v2 Sept 29, 2025.
- Paraphrase/quote fragments: proposes "Confidence-Informed Self-Consistency (CISC)," which "enhances self-consistency decoding by using model confidence scores in weighted majority voting." Quote: "CISC outperforms self-consistency in nearly all configurations, reducing the required number of reasoning paths by over 40% on average." Also relates to the OpenReview-listed "Two Samples Are Enough: Verbal Confidence Meets Self-Consistency in Reasoning LLMs" (https://openreview.net/forum?id=66D3rZrNjV) surfaced in the same search — title/claim ("just two samples are enough to achieve strong and reliable confidence estimation") not independently fetched/confirmed beyond the search snippet; UNVERIFIED.
- Confirmed real: yes for CISC/2502.06233 (direct abstract fetch).

### Self-Consistency Is Losing Its Edge: Diminishing Returns and Rising Costs in Modern LLMs
- URL: https://arxiv.org/abs/2511.00751 (abstract fetched directly)
- Author: Chiyan Loo. v1 Nov 2, 2025; v2 May 7, 2026.
- Paraphrase: argues self-consistency "has grown increasingly inefficient as models improved and may actually hurt performance on problems modern models solve reliably." Testing with Gemini 2.5 on HotpotQA and MATH-500 found "minimal accuracy improvements from additional sampled paths: 0.4% gain on HotpotQA across 20 samples and 1.6% on MATH-500," while "token expenses rise proportionally with sample count." Performance "leveled off quickly and occasionally declined at higher sample counts." Recommends "limiting multi-path sampling to problems that demonstrably challenge a model's single-pass capabilities."
- Confirmed real: yes — this is a direct critique paper of self-consistency, relevant to whether AMDA's design should rely on sampling-based self-consistency for its verifier layer.

### Two Failures of Self-Consistency in the Multi-Step Reasoning of LLMs
- URL: https://arxiv.org/abs/2305.14279
- Authors: Angelica Chen, Jason Phang, Alicia Parrish, Vishakh Padmakumar, Chen Zhao, Samuel R. Bowman, Kyunghyun Cho (NYU and Anthropic, per search-engine summary — Anthropic affiliation UNVERIFIED, not independently confirmed via direct fetch of author affiliations).
- Paraphrase: distinguishes "hypothetical consistency" (can a model predict what its own output would be in a hypothetical other context) and "compositional consistency" (consistency of final outputs when intermediate sub-steps are replaced with the model's own outputs for those steps); finds "multiple variants of the GPT-3/-4 models exhibit poor consistency rates across both types of consistency on a variety of tasks."
- Also surfaced as an HN submission: "Two Failures of Self-Consistency in the MultiStep Reasoning of LLMs (2024) [pdf]" — https://par.nsf.gov/servlets/purl/10542787 (2 points, 0 comments).
- Confirmed real: yes.

### Reliability-Aware Adaptive Self-Consistency for Efficient Sampling in LLM Reasoning
- URL: https://arxiv.org/pdf/2601.02970 (also arxiv.org/html/2601.02970v1)
- Not deep-fetched; title and existence only, from WebSearch results. Paraphrase from search snippet: adaptive self-consistency approaches "rely on stopping criteria based on answer frequency or agreement patterns, implicitly treating all sampled responses as equally informative, often leading to inefficient sampling." Content beyond this UNVERIFIED.

### Universal Self-Consistency for Large Language Model Generation
- URL: https://arxiv.org/pdf/2311.17311
- Not deep-fetched. Paraphrase from search snippet: "the number of samples supported by Universal Self-Consistency is bounded by the context length of the underlying LLM." Content beyond this UNVERIFIED.

### Systematic Evaluation of Uncertainty Estimation Methods in Large Language Models
- URL: https://arxiv.org/html/2510.20460v1 — title/existence only, not deep-fetched, UNVERIFIED beyond title.

### Rethinking LLM Uncertainty: A Multi-Agent Approach to Estimating Black-Box Model Uncertainty
- URL: https://arxiv.org/pdf/2412.09572 — title/existence only, not deep-fetched, UNVERIFIED beyond title.

### General paraphrase on confidence-estimation approaches (from search-engine synthesis, not a single paper)
- Paraphrase: "approaches use the agreement across multiple samples, the model's internal representations, or directly prompting the model to verbalize its confidence" as ways of estimating LLM confidence for cascade/routing decisions. This is a search-engine-generated summary spanning multiple sources, not a verbatim quote from one paper — flagged accordingly.

---

## 3. Token-efficiency / cost-optimization framing in production LLM systems (company blog posts)

### Anthropic — "Building Effective AI Agents"
- URL: https://www.anthropic.com/engineering/building-effective-agents (also mirrored at anthropic.com/news/building-effective-agents and anthropic.com/research/building-effective-agents)
- Note: direct WebFetch of this URL failed twice with "Command failed with no output" (tool error, not a content finding) — content below is reconstructed from WebSearch-returned paraphrase of the page, not a direct fetch, so treat phrasing as paraphrase, not verbatim.
- Paraphrase: "Routing classifies an input and directs it to a specialized followup task. This workflow allows for separation of concerns, and building more specialized prompts." "Routing works well for complex tasks where there are distinct categories that are better handled separately, and where classification can be handled accurately, either by an LLM or a more traditional classification model/algorithm." Practical example given: "routing easy/common questions to smaller models like Claude 3.5 Haiku and hard/unusual questions to more capable models like Claude 3.5 Sonnet to optimize cost and speed."
- Confirmed real: the post is a well-known, real Anthropic engineering post (independently well-established); exact verbatim wording of the routing section is UNVERIFIED here since direct fetch failed — only search-engine paraphrase obtained.

### Anthropic — prompt caching (context for cost optimization, from aggregator sources, not fetched directly from Anthropic docs in this session)
- Paraphrase (from third-party aggregator search results, not Anthropic's own site directly): "Cache hits cost 90% less than standard input tokens, with cache reads at 0.10× standard input — a 90% discount... The write costs 1.25× standard input for a 5-minute TTL, or 2.0× for a 1-hour TTL." UNVERIFIED against Anthropic's own docs page (platform.claude.com/docs/en/build-with-claude/prompt-caching) since that page itself was not directly fetched in this session — only surfaced via WebSearch snippet.

### Google Cloud — "A Developer's Guide to Model Routing" (Medium, Google Cloud Community, by Karl Weinmeister)
- URL: https://medium.com/google-cloud/a-developers-guide-to-model-routing-1f21ecc34d60
- Quote (verbatim, from direct fetch): "Model routing is an architectural pattern designed to solve this optimization problem. It involves maintaining a pool of candidate LLMs and routing each incoming prompt to the most suitable model." "That's often the smallest, fastest, and most cost-effective model that can successfully complete the task."
- Quote (verbatim) on semantic routing mechanics: "Routes are defined, each with a name and a list of representative example phrases. A text embedding model converts all of these utterances into high-dimensional numerical vectors that capture their semantic meaning, which are then stored in an efficient index." "When a new user query arrives, the same embedding model converts it into a vector. Finally, a vector similarity search is performed between the query's vector and all the utterance vectors in the index, and the route whose utterances are most similar to the query is selected as the winner."
- Paraphrase: describes Gemini 2.5 family tiered deployment — "Pro handles complex reasoning, Flash serves general-purpose tasks, and Flash-Lite handles high-volume, latency-sensitive operations."
- Confirmed real: yes, direct fetch succeeded.

### Fireworks AI — "How Factory Grew Open Model Usage 2-3x in Six Months on Fireworks" (Factory Router case study)
- URL: https://fireworks.ai/blog/Factory
- Quote (verbatim, from direct fetch): "Factory Router, now in private preview, lowers cost 30-40% per average task by matching each task to the most cost-efficient model that clears the reliability bar."
- Quote (verbatim): "Blended cost per task fell to 6–20% of frontier while open-model usage grew ~3X; throughput rose 5–15X per dollar."
- Quote (verbatim): "The routing data shows a roughly even split across customers, where a third of tasks are hard enough to warrant the latest frontier model, a third are routine enough for the most cost-efficient, and a third fall in between."
- Quote (verbatim): "Factory Router is moving toward broad availability, extending automatic, cost-efficient model selection to every user without requiring expertise in each new release."
- Confirmed real: yes, direct fetch succeeded. This is a real customer-case-study blog post from Fireworks AI, directly on-topic (small-model-first / cost-efficient routing in production).

### Anyscale — "Building an LLM Router for High-Quality and Cost-Effective Responses"
- URL: https://www.anyscale.com/blog/building-an-llm-router-for-high-quality-and-cost-effective-responses
- Quote (verbatim, from direct fetch): decides "which queries are routed to a closed LLM and which to an OSS LLM based on the query's complexity or domain specificity." Uses "a causal-LLM classifier" routing between GPT-4 and Mixtral-8x7B.
- Quote (verbatim) on data labeling: Mixtral-8x7B producing "a very strong answer" is rated 4-5, adequate responses rate 3, difficult queries rate 1-2.
- Quote (verbatim): "finetune a Llama3-8B model as our causal LLM classifier" using "human preference data, designed to direct simple queries to a more cost-effective model."
- Quote (verbatim) on results: routers "can achieve the same performance as our baselines with up to a 70% cost reduction on MT Bench, a 30% cost reduction on MMLU, and a 40% cost reduction on GSM8K." On GSM8K, causal-LLM router needed "11.75%" of GPT-4 calls for a given quality bar vs. "19.69%" for random routing.
- Confirmed real: yes, direct fetch succeeded. (Note: this Anyscale blog appears to be a precursor/companion piece to the RouteLLM paper — same GPT-4/Mixtral framing, same causal-LLM-classifier method, likely same research group; relationship between the two UNVERIFIED but strongly suggested by content overlap.)

### Groq — general positioning (from aggregator/SEO source, not Groq's own blog directly)
- Source found: https://www.digitalapplied.com/blog/llm-model-routing-2026-cost-quality-optimization-engineering-guide (third-party blog, not Groq's own site)
- Paraphrase: "For most teams, Groq should be a routing layer, not a religion. Use it to absorb cheap, fast, high-volume work. Keep stronger models available for hard or risky requests." "Teams that implement a tuned routing layer report bill reductions in the 40-85% range... because most production traffic never needed a frontier model in the first place." Groq's own "Batch API cuts costs 50% for async jobs, and prompt caching halves input costs on repeated prefixes" (unverified against Groq's own docs directly).
- Confirmed real: this is a THIRD-PARTY aggregator/SEO blog post, not an official Groq engineering post — flagging clearly as such; no genuine Groq-authored blog post about routing/cascades was found in this search session.

### General note on OpenAI and Together AI
- No genuine OpenAI-authored blog post specifically about "model router" cost savings was found in this session's searches; results returned were third-party pricing-comparison/aggregator sites (e.g., cloudzero.com, metacto.com, morphllm.com) discussing OpenAI's pricing tiers, not an OpenAI engineering blog post on routing architecture. Flagging as NOT FOUND (official OpenAI routing blog post).
- Similarly, no genuine Together AI-authored blog post specifically about routing/cascade architecture was found; results were pricing aggregator pages. Flagging as NOT FOUND (official Together AI routing blog post) in this session.
- Third-party paraphrase seen repeatedly across aggregator sites (origin unclear, presented as general industry claim, NOT attributed to a specific primary source): "Production teams report 60-80% bill reduction when caching, batching, and routing all apply to the workload." Treat as an unattributed/aggregator claim, not a verified primary-source data point.

---

## 4. Prompt compression research: LLMLingua family and competitors

### LLMLingua (original)
- URL: https://arxiv.org/abs/2310.05736 ; project site: https://llmlingua.com/llmlingua.html ; code: https://github.com/microsoft/LLMLingua
- Authors: Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, Lili Qiu (Microsoft Corporation). v1 Oct 9, 2023; v2 Dec 6, 2023.
- Quote (verbatim, full abstract): "...this paper presents LLMLingua, a coarse-to-fine prompt compression method that involves a budget controller to maintain semantic integrity under high compression ratios, a token-level iterative compression algorithm to better model the interdependence between compressed contents, and an instruction tuning based method for distribution alignment between language models. We conduct experiments and analysis over four datasets from different scenarios, i.e., GSM8K, BBH, ShareGPT, and Arxiv-March23; showing that the proposed approach yields state-of-the-art performance and allows for up to 20x compression with little performance loss."
- Confirmed real: yes.

### LLMLingua-2
- URL: https://arxiv.org/abs/2403.12968 ; Microsoft Research project page: https://www.microsoft.com/en-us/research/project/llmlingua/llmlingua-2/ ; code: https://aka.ms/LLMLingua-2
- Authors: Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, H. Vicky Zhao, Lili Qiu, Dongmei Zhang. v1 March 19, 2024; v2 revised Aug 12, 2024.
- Quote (verbatim, full abstract): "...existing approaches compress prompts by removing tokens or lexical units according to their information entropy obtained from a causal language model such as LLaMa-7B. The challenge is that information entropy may be a suboptimal compression metric: (i) it only leverages unidirectional context and may fail to capture all essential information needed for prompt compression; (ii) it is not aligned with the prompt compression objective. To address these issues, we propose a data distillation procedure to derive knowledge from an LLM to compress prompts without losing crucial information, and meantime, introduce an extractive text compression dataset. We formulate prompt compression as a token classification problem to guarantee the faithfulness of the compressed prompt to the original one, and use a Transformer encoder as the base architecture... Our approach leads to lower latency by explicitly learning the compression objective with smaller models such as XLM-RoBERTa-large and mBERT... our model is 3x-6x faster than existing prompt compression methods, while accelerating the end-to-end latency by 1.6x-2.9x with compression ratios of 2x-5x."
- Confirmed real: yes.

### LongLLMLingua
- URL: https://arxiv.org/abs/2310.06839
- Authors: Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, Lili Qiu. v1 Oct 10, 2023; v2 revised Aug 12, 2024.
- Paraphrase/quote fragments: addresses three obstacles in long-context scenarios — "increased computational demands, diminished performance, and positional bias." On NaturalQuestions: "up to 21.4% performance boost with around 4x fewer tokens in GPT-3.5-Turbo" and "94.0% cost reduction in the LooGLE benchmark." Compressing ~10k-token prompts at 2x-6x ratios: "can accelerate end-to-end latency by 1.4x-2.6x."
- Confirmed real: yes.

### 500xCompressor
- URL: https://arxiv.org/abs/2408.03094 ; ACL Anthology: https://aclanthology.org/2025.acl-long.1219/
- Paraphrase (from search snippet, not independently fetched from abstract page): "operates by first pretraining on large corpora, such as the Arxiv Corpus, to learn effective compression strategies, and is then fine-tuned on specific datasets like ArxivQA"; "achieves compression ratios ranging from 6x to 500x, achieving 27-90% reduction in calculations and 55-83% memory savings, while retaining 70-74% (F1) and 77-84% (Exact Match) of the LLM capabilities compared to using non-compressed prompts." Content UNVERIFIED beyond this search-engine paraphrase (not directly fetched from arxiv.org/abs/2408.03094 in this session).
- Confirmed real (existence): yes, cross-confirmed via ACL Anthology listing (accepted ACL 2025 long paper).

### Selective Context
- Referenced via PCToolkit search result. Paraphrase: "uses a small language model to judge self-information of tokens, and then tokens with low self-information are pruned from the original prompt... removing redundant content measured by self-information." Not independently fetched from a dedicated Selective Context arXiv page in this session — URL for the original Selective Context paper was not directly captured; flagging as UNVERIFIED / needs direct citation lookup.

### PCToolkit
- URL: https://arxiv.org/pdf/2403.17411
- Title from search result: "PCToolkit: A Unified Plug-and-Play Prompt Compression Toolkit of Large Language Models." Per search snippet, incorporates Selective Context, LLMLingua, LongLLMLingua, SCRL, and "Keep it Simple (KiS)" as distinct compressor plug-ins. Content beyond this UNVERIFIED (not independently fetched from abstract page).

### Characterizing Prompt Compression Methods for Long Context Inference
- URL: https://arxiv.org/pdf/2407.08892 — title/existence only, surfaced in search results; content UNVERIFIED, not deep-fetched.

---

## 5. Hacker News and Medium practitioner write-ups

Method note: HN results obtained directly from the Hacker News Algolia Search API (hn.algolia.com/api/v1/search), which returns raw JSON (title, url, points, num_comments, story_text where applicable) — these are primary-source HN metadata, not search-engine paraphrases.

### HN search: "LLM router cost" (tags=story)
- "NadirClaw, LLM router that cuts costs by routing prompts right" — https://github.com/doramirdor/NadirClaw — 1 point, 1 comment
- "Nadir: Open-source LLM router that cuts API costs 30-60% (MIT License)" — https://getnadir.com/ — 2 points, 0 comments
- "Building an LLM Router for High-Quality and Cost-Effective Responses" — https://www.anyscale.com/blog/building-an-llm-router-for-high-quality-and-cost-effective-responses — 1 point, 0 comments (see Section 3 for content)
- "ClawRouter – Open-source LLM router that saves 78% on inference costs" — https://github.com/BlockRunAI/ClawRouter — 12 points, 1 comment
- "Build, test, and deploy your own LLM router" — https://platform.mintii.ai/login — 2 points, 2 comments
- "LLM-Use – An LLM router that chooses the right model for each prompt" — https://github.com/JustVugg/llm-use — 3 points, 2 comments
- "LLM Router – Open-source prompt router for multi-LLM deployments" (NVIDIA AI Blueprints) — https://github.com/NVIDIA-AI-Blueprints/llm-router — 2 points, 0 comments
- "1.5B LLM routing model that aligns to preferences, not leaderboards" (Arch-Router) — https://huggingface.co/katanemo/Arch-Router-1.5B — 4 points, 0 comments
- "Arch-Router – Aligning LLM Routing with Human Preferences" — https://arxiv.org/abs/2506.16655 — 1 point, 0 comments
- "Arch-Router – 1.5B model for LLM routing by preferences, not benchmarks" — https://github.com/katanemo/archgw — 66 points, 15 comments (highest-engagement Arch-Router submission)
- "Route your prompts to the best LLM" (Unify) — https://unify.ai/chat?default=true — 298 points, 126 comments (highest engagement in this search — general LLM routing product)
- "API router that picks the cheapest model that fits each query" — https://www.komilion.com/ — 1 point, 1 comment
- "InferShrink – Cut LLM API costs 10x with automatic model routing" — https://pypi.org/project/infershrink/ — 2 points, 0 comments
- "GPT Router – Open-Source API Gateway for LLMs" — https://github.com/Writesonic/GPTRouter — 15 points, 11 comments
- "Switchpoint AI – Cut LLM Cost and Improve Performance with Auto Routing" — https://www.switchpoint.dev/ — 5 points, 0 comments

### HN search: "cut LLM costs" (tags=story)
- "AgentReady – Drop-in proxy that cuts LLM token costs 40-60%" — https://agentready.cloud/hn — 8 points, 13 comments
- "Adaptive RAG – How we cut LLM costs without sacrificing accuracy" — https://pathway.com/developers/showcases/adaptive-rag/ — 8 points, 1 comment (content detailed below)
- "Delta – Cut LLM inference costs 30-60% with lossless compression" — https://www.triage-sec.com/blog/delta-ltsc — 6 points, 0 comments
- "Changes that cut our LLM pipeline costs more than model-switching did" — HN item id 48608978, self-text post, author Abbas_Maka, 4 points, 0 comments, created 2026-06-20 (full text below)
- "Headroom (OSS): Cuts LLM costs by 85%" — https://github.com/chopratejas/headroom — 3 points, 5 comments
- "Adference – OpenRouter-style proxy that cuts LLM costs with ads" — https://adference.xyz/ — 3 points, 3 comments
- "TokenSurf – Drop-in proxy that cuts LLM costs 40-94%" — https://tokensurf.io — 3 points, 0 comments
- "A 3-Layer Cache Architecture Cuts LLM API Costs by 75%" — https://github.com/kylemaa/distributed-semantic-cache — 2 points, 1 comment
- "I built a proxy that cuts LLM costs 40-60% – no AI involved" — https://agentready.cloud/hn — 2 points, 1 comment
- "I made a grammar-free prompt language that cuts LLM token costs by 56%" — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6438839 — 1 point, 0 comments
- "WatchLLM – Semantic caching to cut LLM API costs by 70%" — https://www.watchllm.dev/ — 1 point, 0 comments
- "Sleipner.ai – Cut Your LLM Costs by 40-70% (Private Beta)" — https://www.sleipner.ai/ — 1 point, 0 comments
- "Compressor V2: three compression layers for a 50% LLM agent cost cut" — https://www.edgee.ai/blog/posts/introducing-compressor-v2 — 9 points, 0 comments
- "I Cut Vercel's JSON-Render LLM Costs by 89% Using Toon" — https://mateolafalce.github.io/2026/ — 1 point, 0 comments
- "Cut Costs, Not Accuracy: LLM-Powered Data Processing with Guarantees" (BARGAIN paper) — https://arxiv.org/abs/2509.02896 — 2 points, 0 comments (content detailed below)

### HN item full text (self-post) — "Changes that cut our LLM pipeline costs more than model-switching did"
- URL: https://news.ycombinator.com/item?id=48608978 (Algolia object ID 48608978)
- Author: Abbas_Maka. Points: 4. Created: 2026-06-20T13:05:31Z.
- Quote (verbatim, full self-text): "I have been building multiple LLM systems and for our Organization biggest cost savings weren't from prompt-wordsmithing or model switchings. Sharing useful to anyone watching their token bill : 1) JSON → TOON for structured output: JSON was not made for LLMs. well you can implement your own verison that fits for your needs that reduce tokens usage but what worked for us was TOON. TOON cut output our tokens by ~30% same information, way less syntax tax. 2) Full markdown/HTML → condensed markdown: Using markdown for writing your prompts, getting intermediate results or communication between your Agents eats a lot of tokens. We swithced to condesed markdown and short system prompts that replicate Caveman. this alone cut just on input token costs ~50% on calls that pass prior context forward which can be implemented between Agent Calls. 3) Long Do/Don't instruction lists → 2-3 multi-shot examples: Counterintuitive one - replacing a large lists of DO's and Don'ts for agents rules don't help. rather couple of concrete examples that convers major and all cases actually improved output quality more reliably and it's usually fewer tokens once the instruction list gets long enough to cover real edge cases. I have seen most people on this sub reddit talk about using open-source or cheaper models. Like we were spending thousands of dollar's but this all changes alone helped reduce cost by 60%. edit: Open to Discussion, anyone whether something similar would help their setup." [Typos are original/verbatim from the poster.]
- Note: this is a raw, low-engagement (4 points, 0 comments at fetch time) Show-HN-style self-post — treat as an anecdotal practitioner data point, not peer-reviewed or independently verified.

### Pathway.com — "Adaptive RAG: How we cut LLM costs without sacrificing accuracy"
- URL: https://pathway.com/developers/showcases/adaptive-rag/
- Quote (verbatim, from direct fetch): "4x cost reduction of RAG LLM question answering while maintaining good accuracy."
- Quote (verbatim): "dynamically adapt the number of documents in a RAG prompt using feedback from the LLM."
- Quote (verbatim): expands the prompt "according to a geometric series, such as doubling the number of documents;" "The total cost of repeated calls to the LLM with expanding prompts only grows linearly."
- Quote (verbatim): "more than 60% of questions need only one supporting document."
- Quote (verbatim, worked example): "The summed count of documents in the 6 prompts needed to reach 64 supporting documents is 1+2+4+...+64 = 127 = 2*64 -1."
- Quote (verbatim): "retrieved context documents explain and justify the answer of the LLM and the fewer context documents are needed, the easier it is to verify."
- Confirmed real: yes, direct fetch succeeded. Note: this is RAG-context-scaling cost optimization (adaptive retrieval depth), not model-cascade routing per se, but directly relevant to "verify-then-escalate" framing for cost control.

### "Cut Costs, Not Accuracy: LLM-Powered Data Processing with Guarantees" (BARGAIN)
- URL: https://arxiv.org/abs/2509.02896
- Authors: Sepanta Zeighami, Shreya Shankar, Aditya Parameswaran. v1 Sept 2, 2025; v2 revised Sept 12, 2025.
- Quote (verbatim, full abstract): "...The model cascade framework provides a blueprint to manage this trade-off, by using the confidence of LLMs in their output (e.g., log-probabilities) to decide on which records to use the affordable LLM. However, existing solutions following this framework provide only marginal cost savings and weak theoretical guarantees because of poor estimation of the quality of the affordable LLM's outputs. We present BARGAIN, a method that judiciously uses affordable LLMs in data processing to significantly reduce cost while providing strong theoretical guarantees on the solution quality. BARGAIN employs a novel adaptive sampling strategy and statistical estimation procedure... Experimental results across 8 real-world datasets show that BARGAIN reduces cost, on average, by up to 86% more than state-of-the-art, while providing stronger theoretical guarantees on accuracy of output..."
- Confirmed real: yes, direct fetch of abstract succeeded. Directly on-topic: explicit critique that "existing [cascade] solutions... provide only marginal cost savings and weak theoretical guarantees because of poor estimation of the quality of the affordable LLM's outputs" — a specific documented weakness of naive cascade/verifier designs.

### Medium — "The 2025 LLM API Playbook: How We Cut API Costs By 67% Without Sacrificing Quality (Part 3/3: Production Secrets)"
- URL: https://rasiksuhail.medium.com/the-2025-llm-api-playbook-how-we-cut-api-costs-by-67-without-sacrificing-quality-part-3-3-18d8977b46b0
- Author: Rasiksuhail (Medium). Not independently fetched in full in this session (only surfaced via WebSearch title/snippet) — flagging title and URL as found, content beyond the title UNVERIFIED here (see below for a separate, similarly-titled post that WAS fetched directly).

### Blog (personal) — "How I Reduced LLM Costs by 67% in Production" by Martin Kostov
- URL: https://martinkostov.me/blog/how-to-reduce-llm-api-costs-in-production
- Quote (verbatim, from direct fetch): "a 67% reduction in monthly API spend - without users noticing a single thing."
- Quote (verbatim): three core techniques were "caching, prompt compression, and model routing."
- Quote (verbatim): "cache hit rate settled at around 38% of total requests, yielding approximately ~29% reduction in token spend."
- Quote (verbatim): "average prompt length dropped by ~41% across the board" (prompt compression).
- Quote (verbatim): "~31% of total remaining API cost reduced through routing" (model routing).
- Quote (verbatim): "Each lever independently moved the needle. But the combination compounded." Cumulative cost-remaining figures given as: "After caching...71%...After prompt compression...58%...After model routing...40%."
- Quote (verbatim): "user satisfaction metric...did not statistically change. The product felt faster." And: "you cannot optimize what you don't measure."
- Confirmed real: yes, direct fetch succeeded — this is an independent personal/practitioner blog (not a company blog), describing caching + compression + routing stacked together, with a specific attributed cost breakdown (100% → 71% → 58% → 40% of original spend across the three levers in sequence).

### Medium — general aggregator/SEO-style posts surfaced (titles only, not verified as substantive first-hand practitioner accounts; likely SEO content)
- "LLM Cost Optimization: A Practical Guide for Engineering Teams" by Vishnu N C — https://medium.com/@vishnu_73501/llm-cost-optimization-a-practical-guide-for-engineering-teams-95bca0e9aaf3
- "8 LLM Cost Optimization Techniques Every AI Engineer Should Know" by Sachin Kasana — https://medium.com/codetodeploy/8-llm-cost-optimization-techniques-every-ai-engineer-should-know-a45a1cb1d838
- "Prompt Compression — Hands on Guide for LLM Lingua-2" by Devesh Surve — https://deveshsurve.medium.com/prompt-compression-hands-on-guide-for-llm-lingua-2-2baac53800d6
- "Prompt Compression in Large Language Models (LLMs): Making Every Token Count" by Sahin Ahmed — https://medium.com/@sahin.samia/prompt-compression-in-large-language-models-llms-making-every-token-count-078a2d1c7e03
- These titles/URLs came directly from WebSearch results; none were fetched for verbatim content in this session — flagging as found-but-not-verified-in-depth.

---

## 6. 2026-dated content specifically

The following items are dated 2026 (by arXiv submission timestamp or blog post date) and were highlighted for recency, cross-referenced with their fuller entries above:

- UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing — submitted May 11, 2026. https://arxiv.org/abs/2605.18796 (Section 1)
- Cluster, Route, Escalate: Cascaded Framework for Cost-Aware LLM Serving — submitted June 25, 2026. https://arxiv.org/abs/2606.27457 (Section 1)
- Is Escalation Worth It? A Decision-Theoretic Characterization of LLM Cascades — arXiv ID 2605.xxxxx range (May 2026 per ID). https://arxiv.org/abs/2605.06350 (Section 1)
- Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey — v1 Feb 23, 2026; v2 Apr 21, 2026. https://arxiv.org/abs/2603.04445 (Section 1)
- Self-Consistency Is Losing Its Edge — v2 revised May 7, 2026 (v1 was Nov 2025). https://arxiv.org/abs/2511.00751 (Section 2)
- HN self-post "Changes that cut our LLM pipeline costs more than model-switching did" — created 2026-06-20. HN item 48608978 (Section 5)
- HN Show-HN "I Cut Vercel's JSON-Render LLM Costs by 89% Using Toon" — https://mateolafalce.github.io/2026/ (Section 5; year visible in URL path itself, not independently confirmed via fetch)
- Fireworks AI Factory Router blog post — no explicit date captured in fetch; appears in Fireworks' current/2026-era blog based on model names mentioned (Kimi K2.7, MiniMax) which are 2026-era models per other AMDA research files. https://fireworks.ai/blog/Factory (Section 3) — dating is INFERRED, not a directly confirmed timestamp, flagged as such.
- Various third-party aggregator/SEO pages explicitly titled "...2026" (Groq pricing, Vertex AI pricing, OpenAI pricing, Together AI pricing guides) — these are pricing-comparison content, not primary research/engineering writing, and are of secondary value to the cascade-routing research angle; listed in Section 3 with that caveat.

---

## Sources (raw list of every URL visited/fetched or directly cited from search results in this session)

https://arxiv.org/abs/2305.05176
https://arxiv.org/abs/2605.18796
https://arxiv.org/pdf/2605.18796
https://arxiv.org/abs/2406.18665
https://arxiv.org/abs/2404.14618
https://arxiv.org/abs/2310.12963
https://github.com/automix-llm/automix
https://automix-llm.github.io/automix/
https://arxiv.org/abs/2203.11171
https://arxiv.org/abs/2511.00751
https://arxiv.org/abs/2310.05736
https://arxiv.org/abs/2403.12968
https://www.microsoft.com/en-us/research/project/llmlingua/llmlingua-2/
https://github.com/microsoft/LLMLingua
https://llmlingua.com/llmlingua.html
https://arxiv.org/abs/2310.06839
https://arxiv.org/abs/2408.03094
https://aclanthology.org/2025.acl-long.1219/
https://arxiv.org/pdf/2403.17411
https://arxiv.org/pdf/2407.08892
https://www.anthropic.com/engineering/building-effective-agents (fetch failed; content via search paraphrase only)
https://www.anthropic.com/news/building-effective-agents
https://medium.com/google-cloud/a-developers-guide-to-model-routing-1f21ecc34d60
https://fireworks.ai/blog/Factory
https://www.anyscale.com/blog/building-an-llm-router-for-high-quality-and-cost-effective-responses
https://hn.algolia.com/api/v1/search?query=LLM%20router%20cost&tags=story
https://hn.algolia.com/api/v1/search?query=cut%20LLM%20costs&tags=story
https://hn.algolia.com/api/v1/search?query=self-consistency%20LLM&tags=story
https://hn.algolia.com/api/v1/search?query=small%20model%20verifier%20pattern&tags=story
https://hn.algolia.com/api/v1/search?query=Changes%20that%20cut%20our%20LLM%20pipeline%20costs
https://news.ycombinator.com/item?id=48608978
https://pathway.com/developers/showcases/adaptive-rag/
https://arxiv.org/abs/2509.02896
https://martinkostov.me/blog/how-to-reduce-llm-api-costs-in-production
https://rasiksuhail.medium.com/the-2025-llm-api-playbook-how-we-cut-api-costs-by-67-without-sacrificing-quality-part-3-3-18d8977b46b0
https://arxiv.org/abs/2502.19335
https://arxiv.org/abs/2510.05164
https://aclanthology.org/2025.emnlp-main.531/
https://arxiv.org/abs/2606.27457
https://arxiv.org/abs/2509.21837
https://aclanthology.org/2025.emnlp-industry.171/
https://arxiv.org/abs/2511.07396
https://neurips.cc/virtual/2025/poster/116958
https://openreview.net/forum?id=e4IlBqhbTO
https://arxiv.org/abs/2401.13979
https://export.arxiv.org/abs/2401.13979v2
https://openreview.net/forum?id=RQ9fQLEajC
https://arxiv.org/abs/2502.08773
https://arxiv.org/abs/2603.04445
https://arxiv.org/abs/2506.16655
https://huggingface.co/katanemo/Arch-Router-1.5B
https://github.com/katanemo/archgw
https://github.com/MilkThink-Lab/Awesome-Routing-LLMs
https://arxiv.org/abs/2305.14279
https://par.nsf.gov/servlets/purl/10542787
https://arxiv.org/abs/2502.06233
https://openreview.net/forum?id=66D3rZrNjV
https://arxiv.org/abs/2410.10347
https://www.sri.inf.ethz.ch/publications/dekoninck2024cascaderouting
https://openreview.net/forum?id=AAl89VNNy1
https://arxiv.org/pdf/2601.02970
https://arxiv.org/pdf/2311.17311
https://arxiv.org/html/2510.20460v1
https://arxiv.org/pdf/2412.09572
https://arxiv.org/pdf/2603.24787
https://arxiv.org/pdf/2602.22090
https://arxiv.org/pdf/2606.06924
https://arxiv.org/pdf/2604.23505
https://arxiv.org/pdf/2606.25871
https://arxiv.org/pdf/2603.26796
https://arxiv.org/pdf/2508.12631
https://arxiv.org/html/2506.11887v2
https://arxiv.org/html/2506.11887v3
https://arxiv.org/html/2512.20012v1
https://arxiv.org/pdf/2606.18774
https://arxiv.org/pdf/2604.15728
https://arxiv.org/html/2605.01710v1
https://arxiv.org/pdf/2603.04444
https://www.digitalapplied.com/blog/llm-model-routing-2026-cost-quality-optimization-engineering-guide
https://github.com/doramirdor/NadirClaw
https://getnadir.com/
https://github.com/BlockRunAI/ClawRouter
https://platform.mintii.ai/login
https://github.com/JustVugg/llm-use
https://github.com/NVIDIA-AI-Blueprints/llm-router
https://unify.ai/chat?default=true
https://www.komilion.com/
https://pypi.org/project/infershrink/
https://github.com/Writesonic/GPTRouter
https://www.switchpoint.dev/
https://agentready.cloud/hn
https://www.triage-sec.com/blog/delta-ltsc
https://github.com/chopratejas/headroom
https://adference.xyz/
https://tokensurf.io
https://github.com/kylemaa/distributed-semantic-cache
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6438839
https://www.watchllm.dev/
https://www.sleipner.ai/
https://www.edgee.ai/blog/posts/introducing-compressor-v2
https://mateolafalce.github.io/2026/
https://medium.com/@vishnu_73501/llm-cost-optimization-a-practical-guide-for-engineering-teams-95bca0e9aaf3
https://medium.com/codetodeploy/8-llm-cost-optimization-techniques-every-ai-engineer-should-know-a45a1cb1d838
https://deveshsurve.medium.com/prompt-compression-hands-on-guide-for-llm-lingua-2-2baac53800d6
https://medium.com/@sahin.samia/prompt-compression-in-large-language-models-llms-making-every-token-count-078a2d1c7e03
