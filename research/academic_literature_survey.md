# Academic Literature Survey — LLM Cascades, Confidence, Token-Efficiency, LLM-as-Judge

Quick, collect-only pass (breadth over depth). Purpose: gather primary-source facts/URLs/quotes for
AMDA's "local-first, verify, escalate-on-fail" architecture and its LLM-judge-graded, token-ranked
scoring. No analysis/synthesis/recommendations included — raw material only.

Papers already known before this pass (NOT re-listed below): RouteLLM, PAL, PoT, CRITIC (ICLR 2024),
ProgCo, IFEval, Logic-LM (2305.12295), SatLM (2305.09656), ZebraLogic (2502.01100), BIG-Bench Extra
Hard (2502.19187), s1 / budget forcing (2501.19393), "Inverse Scaling in Test-Time Compute"
(2507.14417), "Do Thinking Tokens Help or Trap?" (2506.23840), "Cluster, Route, Escalate"
(2606.27457), a cascade-routing paper from ETH, BARGAIN (cascade critique), "Let Me Speak Freely"
(2408.02442), JSONSchemaBench, math-verify/lighteval/lm-evaluation-harness.

Verification key: **[VERIFIED]** = abstract page opened and quoted directly. **[UNVERIFIED]** = seen
only via search-result snippet; title/ID/authors not confirmed by opening the source.

---

## Topic 1 — LLM cascades / model routing for cost efficiency

### 1. FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance
**[VERIFIED]** — Lingjiao Chen, Matei Zaharia, James Zou. arXiv:2305.05176. https://arxiv.org/abs/2305.05176
> "We outline and discuss three types of strategies that users can exploit to reduce the inference
> cost associated with using LLMs: 1) prompt adaptation, 2) LLM approximation, and 3) LLM cascade...
> we propose FrugalGPT, a simple yet flexible instantiation of LLM cascade which learns which
> combinations of LLMs to use for different queries in order to reduce cost and improve accuracy...
> FrugalGPT can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost
> reduction or improve the accuracy over GPT-4 by 4% with the same cost."
Relevance: Topic 1 (foundational/seminal cascade paper — precedes but not previously logged this session; directly names the small→large deferral pattern AMDA implements).

### 2. Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey
**[VERIFIED]** — Yasmin Moslem, John D. Kelleher. arXiv:2603.04445. https://arxiv.org/abs/2603.04445
> "The rapid growth of large language models (LLMs) with diverse capabilities, costs, and domains has
> created a critical need for intelligent model selection at inference time... a systematic analysis
> of state-of-the-art multi-LLM routing and cascading approaches" organized via "a conceptual
> framework that characterizes routing systems along three dimensions: when decisions are made, what
> information is used, and how they are computed."
Relevance: Topics 1 and 5 (this IS the high-value survey the task asked to look for — maps the whole subfield: difficulty-aware routing, preference alignment, clustering, RL, uncertainty quantification, cascading).

### 3. Universal Model Routing for Efficient LLM Inference
**[VERIFIED]** — Wittawat Jitkrittum, Harikrishna Narasimhan, Ankit Singh Rawat, Jeevesh Juneja, Congchao Wang, Zifeng Wang, Alec Go, Chen-Yu Lee, Pradeep Shenoy, Rina Panigrahy, Aditya Krishna Menon, Sanjiv Kumar. arXiv:2502.08773. https://arxiv.org/abs/2502.08773
> "Model routing is a simple technique for reducing the inference cost of large language models
> (LLMs), wherein one maintains a pool of candidate LLMs, and learns to route each prompt to the
> smallest feasible LLM." Introduces UniRoute for routing to *unseen* models at test time via feature
> vectors from predictions on representative prompts, with "cluster-based routing and a learned
> cluster map," validated on "more than 30 unseen LLMs."
Relevance: Topic 1 — relevant to AMDA's "try up to 2 remote models in preference order" design (model-pool routing theory).

### 4. Is Escalation Worth It? A Decision-Theoretic Characterization of LLM Cascades
**[VERIFIED]** — Dylan Bouchard. arXiv:2605.06350. https://arxiv.org/abs/2605.06350
> "Model cascades, in which a cheap LLM defers to an expensive one on low-confidence queries, are
> widely used to navigate the cost-quality tradeoff at deployment... we establish piecewise concavity
> of the cost-quality frontier... A lightweight pre-generation router exceeds the best cascade policy
> on four of five datasets, mainly because it avoids the cheap model's generation cost on queries sent
> directly to a larger model rather than because of a stronger routing signal. These results suggest
> that cascade performance is limited primarily by structural cost, since cascades pay the cheap model
> before any escalation decision, rather than by a shortage of intermediate stages."
Relevance: Topic 1 — directly interrogates whether cascading (vs. up-front routing) is worth it; the finding that cascades "pay the cheap-model cost before escalation" is a structural point relevant to AMDA's local-first design (though local tokens are free for AMDA, unlike this paper's assumed cost model — noted as a fact, not analyzed further per instructions).

### 5. C3PO: Optimized Large Language Model Cascades with Probabilistic Cost Constraints for Reasoning
**[VERIFIED]** — Antonios Valkanas, Soumyasundar Pal, Pavel Rumiantsev, Yingxue Zhang, Mark Coates. arXiv:2511.07396. https://arxiv.org/abs/2511.07396
> "We propose C3PO, a self-supervised framework enabling cascaded LLM inference where less powerful
> models handle routine queries while difficult cases escalate to stronger models... employs
> conformal prediction to bound the probability that inference cost exceeds a user-specified budget."
> Evaluated on GSM8K, MATH-500, BigBench-Hard, and AIME.
Relevance: Topic 1 — cascade optimization for reasoning-heavy tasks (math/logic), same task families AMDA covers (math, logical reasoning categories).

### 6. RouterEval: A Comprehensive Benchmark for Routing LLMs to Explore Model-level Scaling Up in LLMs
**[VERIFIED]** — Zhongzhan Huang, Guoming Ling, Yupei Lin, Yandong Chen, Shanshan Zhong, Hefeng Wu, Liang Lin. arXiv:2503.10657. https://arxiv.org/abs/2503.10657
> "Routing large language models (LLMs) is a new paradigm that uses a router to recommend the best
> LLM from a pool of candidates for a given input." RouterEval comprises "over 200,000,000 performance
> records for 12 popular LLM evaluations" across "more than 8,500" models; "most [existing Routing LLM
> methods] still have significant room for improvement."
Relevance: Topic 1 — large-scale routing benchmark; useful if AMDA needs an evaluation methodology reference for its own router/verifier design.

### 7. xRouter: Training Cost-Aware LLMs Orchestration System via Reinforcement Learning
**[VERIFIED]** — Cheng Qian, Zuxin Liu, Shirley Kokane, Akshara Prabhakar, Jielin Qiu, Haolin Chen, Zhiwei Liu, Heng Ji, Weiran Yao, Shelby Heinecke, Silvio Savarese, Caiming Xiong, Huan Wang. arXiv:2510.08439. https://arxiv.org/abs/2510.08439
> "Static escalation rules and keyword heuristics under-utilize this spectrum and fail to adapt across
> task types. We present xRouter, a tool-calling-based routing system in which a learned router can
> either answer directly or invoke one or more external models. The router is trained end-to-end with
> reinforcement learning using an explicit, cost-aware reward that encodes cost-performance
> trade-offs, eliminating the need for hand-engineered routing rules."
Relevance: Topics 1 and 3 — explicitly critiques "static escalation rules" (AMDA's verifier-then-escalate is one such static rule) in favor of a learned, cost-aware RL router; also directly relevant to token/cost-aware orchestration.

### 8. Efficient LLM Collaboration via Planning
**[UNVERIFIED]** — arXiv:2506.11578. https://arxiv.org/html/2506.11578v4
Search snippet: describes small-model-first, confidence-based-criterion escalation to a large model as the existing cascade paradigm, and proposes a planning-based collaboration alternative.
Relevance: Topic 1.

### 9. Towards Efficient Multi-LLM Inference: Characterization and Analysis of LLM Routing and Hierarchical Techniques
**[UNVERIFIED]** — arXiv:2506.06579. https://arxiv.org/html/2506.06579v1
Search snippet: a systematic characterization/analysis paper of multi-LLM routing and cascading/hierarchical techniques (routing across independently-trained LLMs, contrasted with intra-model MoE).
Relevance: Topics 1 and 5 (survey/characterization-adjacent).

### 10. LLM Performance Predictors: Learning When to Escalate in Hybrid Human-AI Moderation Systems
**[UNVERIFIED]** — arXiv:2601.07006. https://arxiv.org/html/2601.07006
Search snippet: trains a meta-model ("LLM Performance Predictor") from log-probabilities, entropy, and "novel uncertainty attribution indicators" to decide when to escalate from an LLM to human review, framed as cost-aware selective classification.
Relevance: Topics 1 and 2 — escalation-decision meta-model built directly from cheap logprob/entropy signals, close analog to AMDA's deterministic verifier deciding local-vs-remote.

---

## Topic 2 — Confidence estimation / cheap uncertainty signals for escalation decisions

### 11. Confidence Improves Self-Consistency in LLMs (CISC)
**[VERIFIED]** — Amir Taubenfeld, Tom Sheffer, Eran Ofek, Amir Feder, Ariel Goldstein, Zorik Gekhman, Gal Yona. arXiv:2502.06233 (also ACL 2025 Findings). https://arxiv.org/abs/2502.06233
> "We introduce Confidence-Informed Self-Consistency (CISC). CISC performs a weighted majority vote
> based on confidence scores obtained directly from the model... reducing the required number of
> reasoning paths by over 40% on average... the most calibrated confidence method proved to be the
> least effective for CISC... LLMs can effectively judge the correctness of their own outputs."
Relevance: Topic 2 — a cheap, model-internal confidence signal (no external verifier needed) that reduces sampling cost while improving accuracy; direct alternative/complement to AMDA's deterministic verifier cascade.

### 12. Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs
**[VERIFIED]** — Jannik Kossen, Jiatong Han, Muhammed Razzak, Lisa Schut, Shreshth Malik, Yarin Gal. arXiv:2406.15927. https://arxiv.org/abs/2406.15927
> Semantic entropy probes (SEPs) "approximate semantic entropy directly from a single generation's
> hidden states, eliminating the computational overhead of sampling multiple outputs." Performs
> comparably to prior sampling-based approaches while generalizing better out-of-distribution.
Relevance: Topic 2 — explicitly framed as a "cheap" (single-forward-pass) confidence/hallucination signal, directly on-topic for "is there recent work on cheap/free confidence signals."

### 13. Semantic Energy: Detecting LLM Hallucination Beyond Entropy
**[VERIFIED]** — Huan Ma, Jiadong Pan, Jing Liu, Yan Chen, Joey Tianyi Zhou, Guangyu Wang, Qinghua Hu, Hua Wu, Changqing Zhang, Haifeng Wang. arXiv:2508.14496. https://arxiv.org/abs/2508.14496
> Semantic entropy "relies on post-softmax probabilities and fails to capture inherent model
> uncertainty effectively." Semantic Energy instead "leverages the inherent confidence of LLMs by
> operating directly on logits of penultimate layer," combining semantic clustering with a
> "Boltzmann-inspired energy distribution"; reported >13% AUROC improvement over semantic entropy.
Relevance: Topic 2 — a 2025 successor/critique of semantic-entropy-style uncertainty, logit-based cheap signal.

### 14. Detecting hallucinations in large language models using semantic entropy
**[UNVERIFIED]** (foundational precursor to #12/#13, not independently re-opened this pass) — Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, Yarin Gal. Nature 630, 625–630 (2024). Referenced via search snippets citing this as "Farquhar et al. (2024)."
Relevance: Topic 2 — origin of "semantic entropy" as an uncertainty metric (clusters semantically-equivalent generations, computes entropy over clusters) that #12 and #13 build on/critique.

### 15. LLM Performance Predictors — see entry #10 above (also filed under Topic 1).

### 16. Confidence-Based Response Abstinence: Improving LLM Trustworthiness via Activation-Based Uncertainty Estimation
**[UNVERIFIED]** — arXiv:2510.13750. https://arxiv.org/pdf/2510.13750
Search snippet: uses model activations (not sampling) as an uncertainty signal to decide when an LLM should abstain from answering rather than answer unreliably.
Relevance: Topic 2 — another "cheap" (activation-based, no extra sampling) confidence signal for abstain/escalate decisions.

### 17. Systematic Evaluation of Uncertainty Estimation Methods in Large Language Models
**[UNVERIFIED]** — arXiv:2510.20460. https://arxiv.org/html/2510.20460v1
Search snippet: benchmarks multiple UQ methods; mentions a "CoCoA" hybrid approach combining likelihood-based confidence with agreement/self-consistency signals for improved calibration and discrimination.
Relevance: Topic 2 — comparative evaluation across cheap vs. expensive confidence-estimation methods.

### 18. Confidence Estimation through Verbalized Probability
**[UNVERIFIED]** — arXiv:2511.14275. https://arxiv.org/pdf/2511.14275
Search snippet: studies eliciting calibrated confidence via the model verbalizing its own probability estimate (a zero-extra-inference-cost signal, since it's part of the same generation).
Relevance: Topic 2 — verbalized-confidence line of work; general finding elsewhere in these searches is that verbalized confidence is "often poorly calibrated" unless specifically trained/prompted for it.

---

## Topic 3 — Token-efficient / cost-aware LLM agent design

### 19. Token-Budget-Aware LLM Reasoning (TALE)
**[VERIFIED]** — Tingxu Han, Zhenting Wang, Chunrong Fang, Shiyu Zhao, Shiqing Ma, Zhenyu Chen. arXiv:2412.18547 (also ACL 2025 Findings). https://arxiv.org/abs/2412.18547
> "We find that the reasoning process of current LLMs is unnecessarily lengthy and it can be
> compressed by including a reasonable token budget in the prompt, but the choice of token budget
> plays a crucial role in the actual compression effectiveness. We then propose a token-budget-aware
> LLM reasoning framework that dynamically adjusts the number of reasoning tokens based on the
> reasoning complexity of each problem."
Relevance: Topic 3 — directly about minimizing scored/reasoning tokens per task while preserving accuracy, i.e., the same axis AMDA is scored on (ascending total scored tokens after passing the judge gate).

### 20. Budget-Aware Tool-Use Enables Effective Agent Scaling
**[VERIFIED]** — Tengxiao Liu, Zifeng Wang, Jin Miao, I-Hung Hsu, Jun Yan, Jiefeng Chen, Rujun Han, Fangyuan Xu, Yanfei Chen, Ke Jiang, Samira Daruki, Yi Liang, William Yang Wang, Tomas Pfister, Chen-Yu Lee. arXiv:2511.17006. https://arxiv.org/abs/2511.17006
> "For these agents, scaling involves not only 'thinking' in tokens but also 'acting' via tool calls."
> Finds agents "lack awareness of their tool-call budgets, limiting effectiveness." Introduces "Budget
> Tracker" plugin and "BATS (Budget Aware Test-time Scaling)" which "dynamically adjusts strategy
> based on remaining resources," with "a unified cost metric accounting for both tokens and tool
> consumption."
Relevance: Topic 3 — unified token+tool-call cost metric and explicit "budget awareness" concept for multi-step agents, relevant to any future AMDA agent-loop design (not just single-shot local/remote calls).

### 21. BudgetThinker: Empowering Budget-Aware LLM Reasoning with Control Tokens
**[UNVERIFIED]** — arXiv:2508.17196. https://arxiv.org/html/2508.17196v2
Search snippet: uses special control tokens plus a two-stage training pipeline to give the model precise control over its own reasoning length/budget.
Relevance: Topic 3.

### 22. SelfBudgeter: Adaptive Token Allocation for Efficient LLM Reasoning
**[UNVERIFIED]** — arXiv:2505.11274. https://arxiv.org/pdf/2505.11274
Search snippet: the model self-predicts and allocates its own token budget per problem before/while reasoning.
Relevance: Topic 3.

### 23. Token Economics for LLM Agents: A Dual-View Study from Computing and Economics
**[UNVERIFIED]** — arXiv:2605.09104. https://arxiv.org/html/2605.09104
Search snippet: analyzes LLM agent token consumption jointly from a systems/computing angle and an economics angle (cost modeling).
Relevance: Topic 3.

---

## Topic 4 — LLM-as-judge reliability and biases (new since 2411.16594-style findings)

### 24. A Survey on LLM-as-a-Judge
**[VERIFIED]** — Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni, Jian Guo. arXiv:2411.15594. https://arxiv.org/abs/2411.15594
> "This paper provides a comprehensive survey of LLM-as-a-Judge, addressing the core question: How
> can reliable LLM-as-a-Judge systems be built? We explore strategies to enhance reliability,
> including improving consistency, mitigating biases, and adapting to diverse assessment scenarios...
> we propose methodologies for evaluating the reliability of LLM-as-a-Judge systems, supported by a
> novel benchmark designed for this purpose."
Relevance: Topics 4 and 5 — survey specifically of the LLM-as-judge subfield (note: distinct arXiv ID from the already-known 2411.16594-style bias paper; confirmed as a different, real paper by opening the abstract).

### 25. Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge
**[VERIFIED]** — Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer, Chao Huang, Pin-Yu Chen, Nitesh V Chawla, Xiangliang Zhang. arXiv:2410.02736. https://arxiv.org/abs/2410.02736
> Identifies "12 key potential biases" and introduces CALM, "an automated framework to systematically
> assess each bias category through automated and principle-guided modification." Finds "while
> advanced models have achieved commendable overall performance, significant biases persist in
> certain specific tasks."
Relevance: Topic 4 — a 12-category bias taxonomy + automated bias-measurement framework (CALM) for LLM judges, broader than the length/formatting bias already known.

### 26. Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias
**[UNVERIFIED]** — arXiv:2606.19544. https://arxiv.org/pdf/2606.19544
Search snippet: large-scale study distinguishing "reliability" (consistency) from "validity" (actual correctness) for LLM judges — argues a judge can be internally consistent yet not valid.
Relevance: Topic 4 — directly relevant to trusting a remote LLM-judge's accuracy gate: consistency alone isn't proof the judge's verdicts are correct.

### 27. The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge
**[UNVERIFIED]** — arXiv:2509.26072. https://arxiv.org/html/2509.26072v2
Search snippet: identifies shortcut/spurious-cue biases in LLM judges that go unacknowledged/unreported by the judges themselves.
Relevance: Topic 4.

### 28. Fairness or Fluency? An Investigation into Language Bias of Pairwise LLM-as-a-Judge
**[UNVERIFIED]** — arXiv:2601.13649. https://arxiv.org/pdf/2601.13649
Search snippet: examines language/fluency-driven bias specifically in pairwise (as opposed to pointwise/rubric) LLM-judge comparisons.
Relevance: Topic 4.

### 29. Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines
**[UNVERIFIED]** — arXiv:2604.23178. https://arxiv.org/pdf/2604.23178
Search snippet: evaluates concrete mitigation strategies (not just cataloguing biases) for LLM-judge pipelines; search summary also references two other 2025-2026 lines of work — one on "calibration-based bias correction and confidence intervals" for judge sensitivity/specificity, another applying item response theory to judges themselves ("reliability as a property of the measurement instrument").
Relevance: Topic 4 — mitigation-focused rather than just bias-cataloguing.

---

## Topic 5 — Recent (2025-2026) survey papers on the cascade/routing subfield

(Primary find is entry #2 above, "Dynamic Model Routing and Cascading for Efficient LLM Inference: A
Survey," arXiv:2603.04445 — restated here for visibility since this sub-topic asked for it explicitly.)

### 30. Large Language Models Hallucination: A Comprehensive Survey
**[UNVERIFIED]** — arXiv:2510.06265. https://arxiv.org/pdf/2510.06265
Search snippet: broad survey of LLM hallucination detection/mitigation methods, which overlaps with the confidence/uncertainty-signal literature relevant to escalation decisions.
Relevance: Topics 2 and 5 — survey-level map of the hallucination-detection side of the cheap-confidence-signal space.

---

## Additional notes on search process (factual, not analysis)

- Search queries used (WebSearch tool, no direct Google Scholar access — confirmed hard to fetch
  directly, consistent with task brief): "LLM cascade small model first escalate arxiv 2025", "LLM
  model routing cost efficient inference survey arxiv", "confidence estimation uncertainty
  quantification LLM answer when to escalate arxiv", "self-consistency logprob confidence LLM cheap
  uncertainty signal arxiv 2025", "LLM-as-judge bias reliability arxiv 2025 2026", "token-efficient
  LLM agent budget aware multi-step reasoning arxiv 2025", "cost-aware agent tool use token budget
  reinforcement learning arxiv", "verifier model deterministic check LLM output before escalation
  arxiv", "RouteLLM follow up hybrid LLM routing benchmark arxiv 2025 2026", "LLM judge length bias
  verbosity arxiv 2025", "FrugalGPT cost LLM API cascade arxiv", "semantic entropy hallucination
  detection LLM arxiv Nature", "calibration LLM confidence verbalized probability arxiv 2025", "math
  verification program aided cheap check LLM answer correctness arxiv 2025".
- 14 of 30 listed papers were verified by directly opening the arXiv abstract page (WebFetch) and
  quoting the abstract verbatim; the remainder are marked UNVERIFIED (search-snippet only) per the
  task's verification requirement.
- Two WebFetch calls to arxiv.org abstract pages transiently failed with a domain-verification error
  and were successfully retried immediately after.
- Some math-verification search results (e.g. MATH-VF step-wise formal verification, ValiMath,
  Pessimistic Verification for Open-Ended Math) surfaced but were judged too close to the
  already-known PAL/PoT/math-verify cluster to include as new; not listed above to respect the
  "don't re-surface known work" instruction, though they were not independently confirmed as
  duplicates of any specific known paper — flagging this judgment call for the reader.
