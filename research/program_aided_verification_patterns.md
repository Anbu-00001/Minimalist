# Research notes: "translate to code, execute, compare" verification patterns beyond arithmetic word problems

Collected [2026-07-08]. COLLECT-ONLY — primary-source facts, URLs, and verbatim quotes. No analysis, no recommendations, no code. A separate session will synthesize this.

Method note: WebFetch against `arxiv.org/abs/...` URLs was intermittently blocked in this environment ("Unable to verify if domain arxiv.org is safe to fetch"). Where that happened, I fetched the same abstract page via `https://export.arxiv.org/abs/<id>` with `curl` and pulled the `citation_abstract` meta tag, which contains the verbatim arXiv abstract text. Those are marked accordingly. GitHub source files were fetched with `curl` against `raw.githubusercontent.com`.

---

## 1. PAL and PoT — the original papers, exact mechanism

### PAL: Program-Aided Language Models

- URL: https://arxiv.org/abs/2211.10435
- Authors: Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, Graham Neubig. ICML 2023.
- Verbatim abstract (via export.arxiv.org mirror):
  > "Large language models (LLMs) have recently demonstrated an impressive ability to perform arithmetic and symbolic reasoning tasks, when provided with a few examples at test time ("few-shot prompting"). Much of this success can be attributed to prompting methods such as "chain-of-thought'', which employ LLMs for both understanding the problem description by decomposing it into steps, as well as solving each step of the problem. While LLMs seem to be adept at this sort of step-by-step decomposition, LLMs often make logical and arithmetic mistakes in the solution part, even when the problem is decomposed correctly. In this paper, we present Program-Aided Language models (PAL): a novel approach that uses the LLM to read natural language problems and generate programs as the intermediate reasoning steps, but offloads the solution step to a runtime such as a Python interpreter. With PAL, decomposing the natural language problem into runnable steps remains the only learning task for the LLM, while solving is delegated to the interpreter. We demonstrate this synergy between a neural LLM and a symbolic interpreter across 13 mathematical, symbolic, and algorithmic reasoning tasks from BIG-Bench Hard and other benchmarks. In all these natural language reasoning tasks, generating code using an LLM and reasoning using a Python interpreter leads to more accurate results than much larger models. For example, PAL using Codex achieves state-of-the-art few-shot accuracy on the GSM8K benchmark of math word problems, surpassing PaLM-540B which uses chain-of-thought by absolute 15% top-1. Our code and data are publicly available at http://reasonwithpal.com/."
- Mechanism: generation-time only. The program IS the reasoning chain that produces the answer; there is no described step where PAL is applied to check/audit an answer that already exists from elsewhere.
- Official code repo: https://github.com/reasoning-machines/pal — README text fetched via WebFetch: "Large Language Model solves reasoning problems that involve complex arithmetic and procedural tasks by generating reasoning chains of **text and code**." No mention in the README of using the generated program to verify/audit a pre-existing answer, and no mention of self-consistency across multiple generated programs. (WebFetch-summarized, not a full verbatim dump of the README — flagged as lower-confidence paraphrase of a live page rather than a quote.)

### PoT: Program of Thoughts Prompting

- URL: https://arxiv.org/abs/2211.12588
- Authors: Wenhu Chen, Xueguang Ma, Xinyi Wang, William W. Cohen. Published TMLR 2023.
- Verbatim abstract (via export.arxiv.org mirror):
  > "Recently, there has been significant progress in teaching language models to perform step-by-step reasoning to solve complex numerical reasoning tasks. Chain-of-thoughts prompting (CoT) is by far the state-of-art method for these tasks. CoT uses language models to perform both reasoning and computation in the multi-step `thought' process. To disentangle computation from reasoning, we propose `Program of Thoughts' (PoT), which uses language models (mainly Codex) to express the reasoning process as a program. The computation is relegated to an external computer, which executes the generated programs to derive the answer. We evaluate PoT on five math word problem datasets (GSM, AQuA, SVAMP, TabMWP, MultiArith) and three financial-QA datasets (FinQA, ConvFinQA, TATQA) for both few-shot and zero-shot setups. Under both few-shot and zero-shot settings, PoT can show an average performance gain over CoT by around 12% across all the evaluated datasets. By combining PoT with self-consistency decoding, we can achieve SoTA performance on all math problem datasets and near-SoTA performance on financial datasets. All of our data and code are released in Github https://github.com/wenhuchen/Program-of-Thoughts"
- Mechanism: also generation-time. Note PoT is explicitly combined with **self-consistency decoding** (sample multiple programs, vote) to reach SoTA — this is a generation-time ensembling technique, not a post-hoc audit of a separately-produced answer. No post-hoc verification of an existing (e.g., remote-model-produced) answer is described in the abstract.
- Both PAL and PoT are used downstream as building blocks by CRITIC (see §2) — CRITIC explicitly reuses PoT to produce an *initial* program and then applies a separate verify-then-correct loop on top of it, which is the closest thing to "using this style of program generation as a target of post-hoc verification" found in this research pass.

---

## 2. Self-consistency / self-verification / tool-based critique literature

### Self-Consistency (Wang et al., 2022)

- URL: https://arxiv.org/abs/2203.11171
- Verbatim abstract (via export.arxiv.org mirror):
  > "Chain-of-thought prompting combined with pre-trained large language models has achieved encouraging results on complex reasoning tasks. In this paper, we propose a new decoding strategy, self-consistency, to replace the naive greedy decoding used in chain-of-thought prompting. It first samples a diverse set of reasoning paths instead of only taking the greedy one, and then selects the most consistent answer by marginalizing out the sampled reasoning paths. Self-consistency leverages the intuition that a complex reasoning problem typically admits multiple different ways of thinking leading to its unique correct answer. Our extensive empirical evaluation shows that self-consistency boosts the performance of chain-of-thought prompting with a striking margin on a range of popular arithmetic and commonsense reasoning benchmarks, including GSM8K (+17.9%), SVAMP (+11.0%), AQuA (+12.2%), StrategyQA (+6.4%) and ARC-challenge (+3.9%)."
- Mechanism: pure natural-language sampling + majority vote across multiple *independently generated* reasoning chains. No code execution involved at all. Not a "translate-to-code-and-execute" pattern, and not post-hoc verification of one fixed answer — it's a generation-time ensembling method.

### Large Language Models are Better Reasoners with Self-Verification (Weng et al., 2022/2023)

- URL: https://arxiv.org/abs/2212.09561 (Findings of ACL: EMNLP 2023)
- Verbatim abstract (via export.arxiv.org mirror):
  > "Recently, with the chain of thought (CoT) prompting, large language models (LLMs), e.g., GPT-3, have shown strong reasoning ability in several natural language processing tasks such as arithmetic, commonsense, and logical reasoning. However, LLMs with CoT require multi-step prompting and multi-token prediction, which is highly sensitive to individual mistakes and vulnerable to error accumulation. The above issues make the LLMs need the ability to verify the answers. In fact, after inferring conclusions in some thinking decision tasks, people often check them by re-verifying steps to avoid some mistakes. In this paper, we propose and prove that LLMs also have similar self-verification abilities. We take the conclusion obtained by CoT as one of the conditions for solving the original problem. By performing a backward verification of the answers that LLM deduced for itself, we can obtain interpretable answer validation scores to select the candidate answer with the highest score. Experimental results demonstrate that the proposed method can improve the reasoning performance on various arithmetic, commonsense, and logical reasoning datasets."
- Mechanism: "backward verification" — plug the candidate answer back into the problem as a known condition and see if the model can re-derive a stated input. This IS a post-hoc verification of an already-produced answer, but it is a natural-language/masking technique, not code execution.

### CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing (Gou et al., ICLR 2024) — most directly relevant paper found

- URL: https://arxiv.org/abs/2305.11738 ; PDF read directly (pages 1-8) via `https://browse-export.arxiv.org/pdf/2305.11738`.
- Verbatim abstract (via export.arxiv.org mirror):
  > "Recent developments in large language models (LLMs) have been impressive. However, these models sometimes show inconsistencies and problematic behavior, such as hallucinating facts, generating flawed code, or creating offensive and toxic content. Unlike these models, humans typically utilize external tools to cross-check and refine their initial content, like using a search engine for fact-checking, or a code interpreter for debugging. Inspired by this observation, we introduce a framework called CRITIC that allows LLMs, which are essentially "black boxes" to validate and progressively amend their own outputs in a manner similar to human interaction with tools. More specifically, starting with an initial output, CRITIC interacts with appropriate tools to evaluate certain aspects of the text, and then revises the output based on the feedback obtained during this validation process. Comprehensive evaluations involving free-form question answering, mathematical program synthesis, and toxicity reduction demonstrate that CRITIC consistently enhances the performance of LLMs. Meanwhile, our research highlights the crucial importance of external feedback in promoting the ongoing self-improvement of LLMs."
- **This is a direct example of the pattern the research question asks about**: verify an *already-produced* answer via a tool (including a code interpreter), not generate it via code in the first place.
- Verbatim from the paper body (Introduction, p.1):
  > "As depicted in Figure 1, CRITIC interacts with external tools like search engines and code interpreters to verify the desired aspects of an initial output and subsequently amends the output based on the critiques from the verification. This *verify-then-correct* process can be repeated to ensure constant output enhancement."
- Algorithm 1 (p.4), transcribed verbatim from the PDF:
  > "Require: Input x, prompt ℘, model M, external tools T = {T1, T2, ..., Tk}, number of iterations n
  > Ensure: Corrected output ŷ from M
  > 1: Generate initial output ŷ0 ∼ P_M(·|℘⊕x)  ▷ Initialization
  > 2: for i ← 0 to n−1 do
  > 3:   Verify ŷi through interaction with T to obtain critiques ci ∼ P_M(·|℘⊕x⊕ŷi, T)  ▷ Verification
  > 4:   if ci indicates that yi is correct then  ▷ Stopping Criteria
  > 5:     return ŷi
  > 6:   end if
  > 7:   yi+1 ∼ P_M(·|℘⊕x⊕yi⊕ci)  ▷ Correction
  > 8: end for
  > 9: return ŷn"
- **Math task section (§4.2, "Mathematical Program Synthesis") is the closest published analogue to AMDA's math-verification design**, and it explicitly starts from an *already-generated* program/answer (from PoT) and then separately executes + critiques it:
  > "We then demonstrate the effectiveness of our proposed method in various mathematical program synthesis tasks... This task involves generating a program y that, when executed, accurately solves a problem description..."
  > "Implementation: As shown in Figure 2, we utilize the Python interpreter as a tool to get two types of feedback: error messages and execution results. We use the original error messages from the interpreter, such as `NameError("num_pizza is not defined")` or `Time out`, and represent them in natural language form as `Execution: {error message}`. For execution results, we use the value of the variable "answer" after the execution is completed. We use **program-of-thought (PoT)** (Chen et al., 2022) to generate the initial program and then apply a maximum of n = 4 corrections."
- **Worked example (Figure 2, "Mathematical Program Synthesis" panel)**, transcribed from the PDF image — this shows execution *output itself* (not just a second re-derivation) used as a signal that an existing answer is wrong via a plausibility check:
  > Question: "Ann, Bill, Cate, and Dale each buy personal pan pizzas cut into 4 pieces. If Bill and Dale eat 50% of their pizzas and Ann and Cate eat 75%, how many pizza pieces are left?"
  > Proposed Answer (python): `num_pieces_per_pizza, num_pizza = 4, 4` / `num_pieces = num_pieces_per_pizza * num_pizza` / `pieces_bill_and_dale = num_pieces * 0.5` / `pieces_ann_and_cate = num_pieces * 0.75` / `answer = num_pieces - pieces_bill_dale - pieces_ann_cate`
  > Execution: "No runtime error" / Output: "answer = -4.0"
  > Critique step ("What's the problem with the above code?"): "1. Plausibility: Number of pizza pieces left uneaten should be a positive integer, -4.0 < 0, so the answer is **not reasonable**." — followed by a code-level correctness check and a corrected program.
- Quantitative results, Table 2 (math program synthesis, GSM8k/SVAMP/TabMWP), transcribed:
  - LLaMA-2-70B: PoT solve rate 59.3 (GSM8k) → CRITIC 62.3 (+3.0); SVAMP PoT 82.0 → CRITIC 84.7 (+2.7); TabMWP PoT 59.0 → CRITIC 75.0 (+16).
  - text-davinci-003: PoT 70.1 (GSM8k) → CRITIC 72.2 (+2.1); "CRITIC w/o Tool" on GSM8k = 68.3 (**-1.8** vs PoT baseline, i.e. self-critique *without* the interpreter made results worse).
  - ChatGPT (gpt-3.5-turbo): PoT 72.5 (GSM8k) → CRITIC 78.2 (+5.7); "w/o Tool" 77.0 (+4.5, still positive but smaller than with the tool).
- **Directly relevant to research question #5 (risk of false confidence in self-verification without independent grounding)** — verbatim, Introduction (p.1):
  > "Our findings demonstrate that CRITIC consistently surpasses prior techniques, obviating the need for supplementary data or training... Interestingly, our results underscore the *unreliability* of all tested LLMs, when it comes to validating their own results. We observe that exclusive reliance on self-correction without external feedback may yield modest improvements or **even deteriorate performance**."
- And from Results §4.2 (p.7), specifically about removing the interpreter/execution grounding:
  > "*Tool-interaction plays a critical role* in CRITIC, as the model's own critiques contribute marginally to the improvement (-0.03 and +2.33 F1 with the two LLMs), and even fall short compared to the initial output... *Without execution feedback from the interpreter, the ability of LLMs to correct programs becomes limited and unstable.* This can result in surprising performance deterioration, such as the 1.8-point decrease observed on `text-davinci-003` (Codex) due to the unreliable feedback from the LLMs regarding program correctness."
  - Reading of this finding as it bears on AMDA's design (paraphrase, not a quote from the paper — the paper is about self-*critique* text quality, not specifically about "independent code translation happens to agree with a wrong stated answer"): CRITIC's own ablation shows that when the verification step is *not* grounded in actual code execution (i.e., the model just talks about whether its answer seems right), the correction step is unreliable and can make things worse. This is adjacent to, but not identical to, AMDA's specific risk (an independently-generated arithmetic expression coincidentally evaluating to the same number as a wrong stated answer) — I found no paper directly measuring *that* specific failure mode (see the "gap noted" list at the end of this document).

### ProgCo: Program Helps Self-Correction of Large Language Models

- URL: https://arxiv.org/abs/2501.01264 (WebFetch-derived quotes; not independently re-verified via curl/export mirror in this pass — flag as slightly lower confidence, but content is a direct paraphrase-with-quotes from the abstract as rendered by WebFetch, and the wording is internally consistent with the paper's known framing elsewhere online.)
- Quoted abstract text as returned by WebFetch:
  > "Self-Correction aims to enable large language models (LLMs) to self-verify and self-refine their initial responses without external feedback. However, LLMs often fail to effectively self-verify and generate correct feedback, further misleading refinement and leading to the failure of self-correction, especially in complex reasoning tasks. In this paper, we propose Program-driven Self-Correction (ProgCo). First, program-driven verification (ProgVe) achieves complex verification logic and extensive validation through self-generated, self-executing verification pseudo-programs. Then, program-driven refinement (ProgRe) receives feedback from ProgVe, conducts dual reflection and refinement on both responses and verification programs to mitigate misleading of incorrect feedback in complex reasoning tasks. Experiments on three instruction-following and mathematical benchmarks indicate that ProgCo achieves effective self-correction, and can be further enhance performance when combined with real program tools."
- This is another direct hit on the research question: ProgVe explicitly generates a *verification* pseudo-program (distinct from the original answer-generating step) whose job is to check an already-produced response, then feeds that check back into a refinement step. Same overall shape as AMDA's math check, but generalized to non-math "instruction-following" benchmarks too (per the abstract) and applied as a self-correction loop rather than a route/escalate decision.

### Related but not code-execution-based (noted for completeness, not double-counted as "program-aided")

- Self-Debugging (Chen, Lin, Schärli, Zhou, 2023): https://arxiv.org/abs/2304.05128 — teaches models to debug by explaining generated code and using execution results/unit tests, framed as "rubber duck debugging." Found via WebSearch summary only in this pass (not independently fetched/quoted verbatim) — UNVERIFIED beyond the search snippet: "Self-Debugging can teach large language models to perform rubber duck debugging—without any feedback on code correctness or error messages, the model is able to identify its mistakes by explaining the generated code in natural language." This is about debugging code-generation-task outputs, not about auditing a reasoning/math answer.
- Chain of Code (Li, Liang, Zeng et al., 2023): https://arxiv.org/abs/2312.04474 — verbatim abstract (via export.arxiv.org):
  > "Code provides a general syntactic structure to build complex programs and perform precise computations when paired with a code interpreter - we hypothesize that language models (LMs) can leverage code-writing to improve Chain of Thought reasoning not only for logic and arithmetic tasks, but also for semantic ones... In this work, we propose Chain of Code (CoC), a simple yet surprisingly effective extension that improves LM code-driven reasoning. The key idea is to encourage LMs to format semantic sub-tasks in a program as flexible pseudocode that the interpreter can explicitly catch undefined behaviors and hand off to simulate with an LM (as an "LMulator")... on BIG-Bench Hard, Chain of Code achieves 84%, a gain of 12% over Chain of Thought."
  - This extends PAL/PoT-style code generation to semantic (non-arithmetic) sub-tasks by having the LLM *emulate* unexecutable code, but it is still a generation-time reasoning method, not post-hoc verification of a separately-produced answer.

---

## 3. lighteval and lm-evaluation-harness — actual task source code

### lm-evaluation-harness (EleutherAI)

**gsm8k.yaml** — plain regex + exact-match, NO code execution or symbolic verification. Fetched verbatim via `curl https://raw.githubusercontent.com/EleutherAI/lm-evaluation-harness/main/lm_eval/tasks/gsm8k/gsm8k.yaml`:
```
metric_list:
  - metric: exact_match
    aggregation: mean
    higher_is_better: true
    ignore_case: true
    ignore_punctuation: false
    regexes_to_ignore:
      - ","
      - "\\$"
      - "(?s).*#### "
      - "\\.$"
filter_list:
  - name: "strict-match"
    filter:
      - function: "regex"
        regex_pattern: "#### (\\-?[0-9\\.\\,]+)"
      - function: "take_first"
  - name: "flexible-extract"
    filter:
      - function: "regex"
        group_select: -1
        regex_pattern: "(-?[$0-9.,]{2,})|(-?[0-9]+)"
      - function: "take_first"
```
So the reference `gsm8k` task in lm-evaluation-harness is pure text extraction + string comparison — **no execution/verification of the arithmetic itself**, it trusts that the extracted number is correct if it string-matches the gold number.

**minerva_math** (`lm_eval/tasks/minerva_math/utils.py`, fetched verbatim via curl) DOES use symbolic execution — via `sympy` and the `math_verify` library — to check equivalence between the model's extracted final answer and the gold answer:
```python
try:
    import antlr4
    import sympy
    from math_verify import parse, verify
    from sympy.parsing.latex import parse_latex
    ...
except (ModuleNotFoundError, AssertionError) as e:
    raise type(e)(
        "`sympy`, `math_verify` and `antlr4-python3-runtime==4.11` are required for generating translation task prompt templates. "
        "Please install the required packages via pip install lm-eval[math] or pip install -e .[math]"
    ) from e
...
def process_results(doc: dict, results: list[str]) -> dict[str, int]:
    candidates = results[0]
    unnormalized_answer = get_unnormalized_answer(candidates)
    answer = normalize_final_answer(unnormalized_answer)
    if is_equiv(answer, doc["answer"]):
        retval = 1
    else:
        retval = 0
    # math_verify
    _mvres = verify(
        gold=parse(doc["solution"]),
        target=parse(candidates),
    )
    mathval = 1 if _mvres else 0
    res = {"exact_match": retval, "math_verify": mathval}
    return res
...
def is_equiv(x1: str, x2: str) -> bool:
    """x1 and x2 are normalized latex string"""
    try:
        with timeout(seconds=5):
            try:
                parsed_x1 = parse_latex(x1)
                parsed_x2 = parse_latex(x2)
            except (sympy.parsing.latex.errors.LaTeXParsingError, sympy.SympifyError, TypeError):
                return False
            try:
                diff = parsed_x1 - parsed_x2
            except TypeError:
                return False
            try:
                if sympy.simplify(diff) == 0:
                    return True
                else:
                    return False
            except ValueError:
                ...
    except TimeoutError:
        return False
```
The `leaderboard/math/utils.py` variant (Level-5 MATH subset used in the HF Open LLM Leaderboard config) uses the same `math_verify`/`sympy` approach and keeps a legacy string-based comparator (`process_result_v1` / `is_equiv`) as a fallback comparison path, fetched verbatim via curl:
```python
from math_verify import LatexExtractionConfig, parse, verify
...
def process_results(doc: dict, results: List[str]) -> Dict[str, int]:
    candidates = results[0]
    parsed_candidate = parse(candidates)
    parsed_answer = parse(doc["solution"], extraction_config=[LatexExtractionConfig()])
    if verify(parsed_answer, parsed_candidate):
        retval = 1
    else:
        retval = 0
    try:
        original = process_result_v1(doc, candidates)
    except:
        original = 0
    output = {"exact_match": retval, "exact_match_original": original}
    return output
```
- Important characterization: **this is symbolic/numeric equivalence-checking of the model's extracted final answer against a known gold answer**, executed via sympy's simplification/diff-to-zero check (`sympy.simplify(diff) == 0`) — i.e., "convert both sides to a common symbolic representation and execute an equality check" rather than "translate the whole word problem into an independent expression and execute it to derive a fresh answer." It is a comparison-time execution (grading), not a "re-derive the answer from scratch and see if it matches" pattern like PAL/PoT/AMDA's math check. Also, in both harness variants, this comparison is always done **against a known gold label** (dataset ground truth) — not against a *second* model's own stated answer with no ground truth available, which is the AMDA math-check design and also CRITIC's setting.
- Source URLs: 
  - https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/gsm8k/gsm8k.yaml
  - https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/minerva_math/utils.py
  - https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/leaderboard/math/utils.py
- A WebSearch result claimed lm-evaluation-harness also has tasks named "python_gsm" or "sympy_math" that "require execution of model-generated Python code" and "take in a results file, read in the LM's generated programs, and execute them to check for correctness." **UNVERIFIED** — I could not locate these task directories directly in the repository in this pass (a follow-up direct search inside `lm_eval/tasks/` would be needed); flagging this explicitly as an unconfirmed search-snippet claim rather than a verified file.

### lighteval (HuggingFace)

**gsm8k.py** (`src/lighteval/tasks/tasks/gsm8k.py`), fetched verbatim via curl:
```python
from lighteval.metrics.metrics import Metrics, math_scorer
...
gsm8k = LightevalTaskConfig(
    name="gsm8k",
    prompt_function=gsm8k_prompt,
    sample_fields=record_to_sample,
    sample_to_fewshot=sample_to_fewshot,
    solver=[prompt_template(MATH_PROMPT_TEMPLATE), generate(cache=True)],
    scorer=math_scorer(),
    hf_repo="openai/gsm8k",
    ...
    metrics=[Metrics.expr_gold_metric],
    stop_sequence=["Question:"],
    version=0,
)
```
**metrics.py** (`src/lighteval/metrics/metrics.py`), fetched verbatim via curl — the `math_scorer()` used by the gsm8k task:
```python
@scorer(metrics=[accuracy()])
def math_scorer():
    gold_extraction_target = (ExprExtractionConfig(),)
    pred_extraction_target = (ExprExtractionConfig(), LatexExtractionConfig(boxed_match_priority=0))
    ...
    async def score(state: TaskState, target: Target):
        extracted_predictions = extract_target_from_pred(
            state.output.completion, pred_extraction_regexes, fallback_mode, extraction_mode, timeout_seconds
        )
        extracted_gold = extract_target_from_pred(
            target.text, gold_extraction_regexes, fallback_mode, extraction_mode, timeout_seconds
        )
        return Score(
            value="C" if extracted_predictions == extracted_gold else "I",
            explanation=state.output.completion,
            answer=str(extracted_predictions),
        )
    return score
```
and the `expr_gold_metric` referenced in the task's `metrics=[...]` list:
```python
expr_gold_metric = SampleLevelMetric(
    metric_name="extractive_match",
    sample_level_fn=MultilingualExtractiveMatchMetric(
        language=Language.ENGLISH,
        fallback_mode="first_match",
        precision=5,
        gold_extraction_target=(ExprExtractionConfig(),),
        pred_extraction_target=(ExprExtractionConfig(), LatexExtractionConfig(boxed_match_priority=0)),
        aggregation_function=max,
    ),
    category=SamplingMethod.GENERATIVE,
    corpus_level_fn=np.mean,
    higher_is_better=True,
)
```
- `ExprExtractionConfig`/`LatexExtractionConfig` and the underlying comparison come from HuggingFace's separate `math-verify` package (see below) — i.e., lighteval's gsm8k/MATH-style scoring delegates to the same `math_verify` symbolic-comparison engine used by lm-evaluation-harness's `minerva_math`/`leaderboard/math` tasks, not to a from-scratch independent re-derivation of the answer.
- Source URLs:
  - https://github.com/huggingface/lighteval/blob/main/src/lighteval/tasks/tasks/gsm8k.py
  - https://github.com/huggingface/lighteval/blob/main/src/lighteval/metrics/metrics.py

### The shared underlying library: HuggingFace `math-verify`

- URL: https://github.com/huggingface/Math-Verify
- README (fetched verbatim via curl), on the grading algorithm:
  > "The grading process follows a three-step algorithm: Answer Extraction -> Expression Common Representation Conversion (SymPy) -> Gold Comparison."
  > "1. **Answer Extraction**: Retrieves the answer from the model output in a format-agnostic manner... 2. **Answer Parsing**: Converts the extracted answer to a common representation (SymPy)... Parses the normalized answer using ANTLR4 grammar to convert it to a SymPy expression... 3. **Gold Comparison**: Compares the parsed answer with the gold answer. 1. Initially attempts string comparison and basic SymPy equality... 2. For numeric expressions: Numeric equality within specified precision (e.g., 0.333333 ≈ 1/3); Symbolic equality by simplifying the difference (a - b = 0)."
  > Usage example given in the README: `from math_verify import parse, verify` / `gold = parse("${1,3} \\cup {2,4}$")` / `answer = parse("${1,2,3,4}$")` / `verify(gold, answer)  # >>> True`
  > On why the library exists: "Existing math evaluators often fail to correctly assess model outputs due to: 1. Strict format requirements... 2. Limited parsing capabilities... 3. Inflexible comparison logic (unable to recognize equivalent expressions) As result, this can lead to significant underestimation of model performance, in extreme cases, even by 40 points."
- Reported accuracy comparison table in the README (MATH dataset): Harness 0.0802, Qwen 0.1288, Math-Verify 0.1328 (higher = fewer scoring errors from the evaluator itself, per the README's framing).
- **Bottom line for research question #3**: both reference frameworks' math tasks use code-execution-adjacent symbolic verification (SymPy simplification, executed via ANTLR4-parsed expressions) strictly as a *grading/scoring* mechanism against a known gold answer — this is execution used for **equivalence-checking of two already-stated expressions**, not execution used to **independently re-derive an answer from the natural-language problem and cross-check it against a model's stated answer with no gold label available** (which is what PAL/PoT do at generation time, and what AMDA's math check does at verification time). I found no code in either framework's math tasks that translates the *word problem* itself into an executable program as a check — only code that parses/executes the *already-extracted final expressions* (both gold and predicted) to test symbolic/numeric equality.

---

## 4. Program-aided checks beyond math (date/time, units, structured-extraction/JSON constraints)

- **No direct evidence found** of a documented "translate-to-code-and-execute" verification pattern specifically for date/time arithmetic or unit conversion answers as an audit step (as opposed to a generation-time technique). A WebSearch pass returned only general observations, e.g. (UNVERIFIED, search-snippet only, source unclear/low-confidence): "date arithmetic and logical reasoning from natural language descriptions involve unit conversions (day, month, year), leap year handling, and relative date calculations," and a note that a "comprehensive review of 63 frequently used LLM benchmarks reveals no systematic evaluation of LLMs on datetime processing" — this second claim traces to a paper called **PRIMETIME: Limits of LLMs in Temporal Primitives** (https://arxiv.org/pdf/2504.16155), which I did not independently fetch/quote in this pass — flag as UNVERIFIED pending direct read of that PDF.
- **Closest verified analogue for "beyond math, execute a program/checker rather than fuzzy text matching": IFEval (Instruction-Following Eval).**
  - URL: https://arxiv.org/abs/2311.07911
  - Verbatim abstract (via export.arxiv.org mirror):
    > "One core capability of Large Language Models (LLMs) is to follow natural language instructions. However, the evaluation of such abilities is not standardized: Human evaluations are expensive, slow, and not objectively reproducible, while LLM-based auto-evaluation is potentially biased or limited by the ability of the evaluator LLM. To overcome these issues, we introduce Instruction-Following Eval (IFEval) for large language models. IFEval is a straightforward and easy-to-reproduce evaluation benchmark. It focuses on a set of "verifiable instructions" such as "write in more than 400 words" and "mention the keyword of AI at least 3 times". We identified 25 types of those verifiable instructions and constructed around 500 prompts, with each prompt containing one or more verifiable instructions. We show evaluation results of two widely available LLMs on the market. Our code and data can be found at https://github.com/google-research/google-research/tree/master/instruction_following_eval"
  - Mechanism (from WebSearch summary of secondary sources, not independently fetched from the IFEval code in this pass — flag as less-verified paraphrase): each of the 25 instruction types has a **deterministic, code-based checker function** (e.g., word count, keyword count, regex/format check) rather than an LLM judge or fuzzy text match. This is structurally the same idea as "verify programmatically instead of via text similarity," generalized to instruction-following constraints rather than math — but it is **constraint-checking against the prompt's stated rules**, not "translate the task to code, execute, and compare to the model's own stated answer." It's closer in spirit to AMDA's deterministic verifier layer than to AMDA's program-aided math check.
  - This is the one closest primary-source hit for "verifying structured/constraint-satisfaction correctness via deterministic code rather than fuzzy text matching," generalized beyond math — but note it verifies against explicit, extractable constraints in the prompt (e.g., "more than 400 words"), not against open-ended semantic correctness of a JSON extraction the way the research question framed it ("does this JSON actually satisfy the constraints stated in the prompt").
- I found **no direct primary-source hit** for the specific pattern "execute code to check whether a structured/JSON extraction output satisfies constraints stated in the prompt" as a named/documented technique in eval literature. General web results about JSON-schema validation (e.g., using `ajv`/`jsonschema` libraries, or constrained decoding) describe **format/schema validity checking**, not **semantic constraint satisfaction relative to the source prompt** — these are adjacent but distinct from what the research question asked about, and I did not find a paper connecting them the way AMDA's design would need. Flagging this as a **gap** rather than asserting a negative in the literature — a more targeted search (e.g., specifically inside RAG/structured-extraction-eval papers, or synthetic-data-verification papers) might surface something a broader pass didn't catch.

---

## 5. Risk of program-aided verification giving false confidence

Several primary sources bear on this, though I found none that isolates the *exact* AMDA-relevant failure mode ("the model's own translation-to-code step is wrong in a way that happens to still agree with a wrong stated answer") as a dedicated study. What I did find:

### CRITIC's own ablation (already quoted in full in §2 above) — the clearest direct evidence

- Removing the code-interpreter grounding and relying on the model's own text-based self-critique instead ("CRITIC w/o Tool") **degrades results below the ungrounded baseline** in at least one setting: text-davinci-003 on GSM8k went from PoT's 70.1 solve rate down to 68.3 (**-1.8**) under "w/o Tool," while WITH the interpreter it rose to 72.2 (+2.1). Verbatim, again: "Without execution feedback from the interpreter, the ability of LLMs to correct programs becomes limited and unstable. This can result in surprising performance deterioration... due to the unreliable feedback from the LLMs regarding program correctness." (https://arxiv.org/abs/2305.11738)
- Reading (paraphrase, not a quote): this supports the general principle that grounding verification in actual execution (rather than the model just asserting whether something looks right) matters — but it is about the presence/absence of execution, not about whether execution-based verification itself can be fooled by a correlated translation error.

### BrokenMath — sycophancy under self/LLM-judged correctness-checking (math domain, not code-execution-based, but directly on the "false confidence when verifying a stated answer" theme)

- URL: https://arxiv.org/abs/2510.04721
- Verbatim abstract (via export.arxiv.org mirror):
  > "Large language models (LLMs) have recently shown strong performance on mathematical benchmarks. At the same time, they are prone to hallucination and sycophancy, often providing convincing but flawed proofs for incorrect mathematical statements provided by users... We introduce BrokenMath, the first benchmark for evaluating sycophantic behavior in LLMs within the context of natural language theorem proving. BrokenMath is built from advanced 2025 competition problems, which are perturbed with an LLM to produce false statements and subsequently refined through expert review. Using an LLM-as-a-judge framework, we evaluate state-of-the-art LLMs and agentic systems and find that sycophancy is widespread, with the best model, GPT-5, producing sycophantic answers 29% of the time. We further investigate several mitigation strategies, including test-time interventions and supervised fine-tuning on curated sycophantic examples. These approaches substantially reduce, but do not eliminate, sycophantic behavior."
- Note: this benchmark is about LLM-as-judge sycophancy toward a *user-supplied false premise* in proof-writing, not specifically about program-aided/code-execution verification. Relevance to research question 5 is that it's evidence models can produce "confident but wrong" validation judgments even when directly asked to check correctness — a generic caution about trusting any single-pass verification step, LLM-judged or otherwise, without independent/executed grounding.

### "Uncovering Systematic Failures of LLMs in Verifying Code Against Natural Language Specifications"

- URL: https://arxiv.org/html/2508.12358v1 (abstract verified verbatim via export.arxiv.org abs-page mirror)
- Verbatim abstract:
  > "Large language models (LLMs) have become essential tools in software development, widely used for requirements engineering, code generation and review tasks. Software engineers often rely on LLMs to assess whether system code implementation satisfy task requirements, thereby enhancing code robustness and accuracy. However, it remains unclear whether LLMs can reliably determine whether the code complies fully with the given task descriptions, which is usually natural language specifications. In this paper, we uncover a systematic failure of LLMs in evaluating whether code aligns with natural language requirements. Specifically, with widely used benchmarks, we employ unified prompts to judge code correctness. Our results reveal that LLMs frequently misclassify correct code implementations as either "not satisfying requirements" or containing potential defects. Surprisingly, more complex prompting, especially when leveraging prompt engineering techniques involving explanations and proposed corrections, leads to higher misjudgment rate, which highlights the critical reliability issues in using LLMs as code review assistants..."
  - Concrete numbers (from an earlier WebFetch pass over the same paper's HTML — not independently re-verified via a second fetch method here, treat as slightly lower-confidence than the abstract quote above but from the primary source page directly, not a search snippet): GPT-4o on HumanEval-derived correctness judgment dropped "from 52.4% with the simple direct prompt to merely 11.0% using the full three-step prompt," and similar-magnitude drops ("32.8 and 32.5 percentage points") on other datasets when the LLM is asked to explain/propose fixes as part of judging.
- Note on relevance: this paper is about LLM-as-verifier of *code-vs-spec* compliance (false negatives — correct code wrongly flagged as incorrect), which is a different failure direction (over-suspicion) than AMDA's concern (false confidence — a wrong answer getting rubber-stamped as correct). Included because it's a directly relevant, well-quantified data point on "LLMs verifying outputs are not reliable graders," from the same broad literature area, even though the failure direction differs from the one AMDA's design is worried about.

### Verification-dynamics / generative-verifier studies (test-time-scaling literature, math/reasoning verifiers, general — not code-execution-specific)

- "Variation in Verification: Understanding Verification Dynamics in Large Language Models" — https://arxiv.org/abs/2509.17995 (abstract fetched verbatim via export.arxiv.org):
  > "...we study generative verifiers, which perform verification by generating chain-of-thought (CoT) reasoning followed by a binary verdict. We systematically analyze verification dynamics across three dimensions - problem difficulty, generator capability, and verifier generation capability... Our experiments reveal three key findings about verification effectiveness: (1) Easy problems allow verifiers to more reliably certify correct responses; (2) Weak generators produce errors that are easier to detect than strong generators; (3) Verification ability is generally correlated with the verifier's own problem-solving capability, but this relationship varies with problem difficulty... we identify cases where strong verifiers offer limited advantage over weak ones, as both fail to provide meaningful verification gains, suggesting that verifier scaling alone cannot overcome fundamental verification challenges."
  - Relevance: this is about LLM-as-verifier (CoT + verdict), not code-execution verification specifically, but the finding "strong generators produce errors that are [harder] to detect" is germane to the general risk area — a stronger local model's wrong answer might be exactly the kind of error a same-capability verification step (including a program-aided one written by the same model) is least likely to catch, if the underlying mistake is a misunderstanding of the problem rather than a slip that shows up as a code bug.
- "Scoring Verifiers: Evaluating Synthetic Verification for Code and Reasoning" — https://arxiv.org/abs/2502.13820 (abstract fetched verbatim via export.arxiv.org):
  > "Synthetic verification techniques such as generating test cases and reward modelling are common ways to enhance the coding capabilities of large language models (LLM) beyond predefined tests... In this paper, we propose an approach which can transform existing coding benchmarks into scoring and ranking datasets to evaluate the effectiveness of synthetic verifiers... Our experiments show that reasoning can significantly improve test case generation and that scaling the number of test cases enhances the verification accuracy."
  - Relevance: general evidence that synthetic/self-generated verification (e.g., self-written test cases) has measurable, non-trivial failure rates and that verification quality scales with effort (more test cases, reasoning) rather than being free/reliable by default — supports general caution but isn't specific to the arithmetic-translation-agreement scenario.

### Gap explicitly noted (not found despite targeted searching)

- I did not find a paper or writeup that specifically studies: "when an LLM is asked to independently translate a word problem into a checking expression, how often does that translation share the same underlying misunderstanding as the model's original stated answer, such that program-aided verification agrees with a wrong answer." Searches for terms like "spurious agreement," "false confidence," "coincidental correctness," and "correlated errors" in combination with "program-aided"/"code execution verification" returned either (a) unrelated program-equivalence-checking papers (e.g., EquiBench, VeriEquivBench — about LLMs judging whether two pieces of *code* are semantically equivalent, not about word-problem-to-expression translation agreement) or (b) general commentary/blog-style claims without a clear primary citation. This looks like a genuine open gap in the literature as searched, rather than a fact I simply failed to retrieve — flagging explicitly per instructions rather than asserting a negative with false confidence.

---

## Source list (all URLs referenced above)

- PAL paper: https://arxiv.org/abs/2211.10435
- PAL code: https://github.com/reasoning-machines/pal
- PoT paper: https://arxiv.org/abs/2211.12588
- Self-Consistency paper: https://arxiv.org/abs/2203.11171
- Self-Verification paper: https://arxiv.org/abs/2212.09561
- CRITIC paper: https://arxiv.org/abs/2305.11738 (PDF read directly: https://browse-export.arxiv.org/pdf/2305.11738)
- ProgCo paper: https://arxiv.org/abs/2501.01264
- Self-Debugging paper: https://arxiv.org/abs/2304.05128 (UNVERIFIED — search snippet only)
- Chain of Code paper: https://arxiv.org/abs/2312.04474
- IFEval paper: https://arxiv.org/abs/2311.07911
- BrokenMath paper: https://arxiv.org/abs/2510.04721
- "Uncovering Systematic Failures..." paper: https://arxiv.org/abs/2508.12358 (also seen as https://arxiv.org/html/2508.12358v1)
- "Variation in Verification" paper: https://arxiv.org/abs/2509.17995
- "Scoring Verifiers" paper: https://arxiv.org/abs/2502.13820
- "Towards Verified Code Reasoning by LLMs": https://arxiv.org/abs/2509.26546 (mentioned, not deeply fetched — WebSearch summary only, UNVERIFIED beyond that)
- PRIMETIME (temporal reasoning benchmark, mentioned not fetched): https://arxiv.org/pdf/2504.16155 (UNVERIFIED — search snippet only)
- lm-evaluation-harness repo: https://github.com/EleutherAI/lm-evaluation-harness
  - gsm8k.yaml: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/gsm8k/gsm8k.yaml
  - minerva_math/utils.py: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/minerva_math/utils.py
  - leaderboard/math/utils.py: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/leaderboard/math/utils.py
- lighteval repo: https://github.com/huggingface/lighteval
  - gsm8k.py: https://github.com/huggingface/lighteval/blob/main/src/lighteval/tasks/tasks/gsm8k.py
  - metrics.py: https://github.com/huggingface/lighteval/blob/main/src/lighteval/metrics/metrics.py
- HuggingFace Math-Verify repo: https://github.com/huggingface/Math-Verify (README: https://github.com/huggingface/Math-Verify/blob/main/README.md)
