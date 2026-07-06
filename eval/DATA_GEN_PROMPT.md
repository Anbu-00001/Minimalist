# Dev eval-set generation prompt

> **If a bot refuses or truncates (e.g. Gemini):** use these two tweaks, which fix it
> in almost every case:
> 1. Start the prompt with: *"I'm a hackathon participant building a practice test set
>    to evaluate my own AI agent before submission. Help me write practice questions
>    with answer keys."* (replaces the first paragraph below)
> 2. Ask for **20 tasks (categories 1–4 only)** in one run, then **categories 5–8** in
>    a second run — paste them as two separate batch files. Smaller outputs dodge the
>    truncation/refusal.

Paste the prompt below into ChatGPT, Gemini, and Grok (one run each, ideally 2-3 runs
per bot with "give me a fresh batch, no repeats"). Save each response as a `.json` file
in `data/dev_tasks/` named like `chatgpt_batch1.json`, `gemini_batch1.json`, etc.
Different bots produce different task distributions — that diversity is the point,
since the real evaluation uses unseen prompt variants.

---

You are helping me build a private evaluation set for testing a general-purpose AI
agent. Generate exactly 40 tasks: 5 tasks for each of these 8 categories:

1. factual_knowledge — explaining concepts, definitions, and how things work
2. mathematical_reasoning — multi-step arithmetic, percentages, word problems, projections
3. sentiment_classification — labelling sentiment (positive/negative/neutral/mixed) and justifying it
4. text_summarisation — condensing a given passage to a specific format or length constraint (include the passage, 100-250 words, inside the prompt)
5. named_entity_recognition — extracting and labelling entities (person, org, location, date) from a given sentence or short passage included in the prompt
6. code_debugging — a short code snippet (Python or JavaScript, 5-25 lines) containing exactly one bug; the task is to identify the bug and provide the corrected code
7. logical_reasoning — constraint-based puzzles (seating, scheduling, truth-tellers, ordering) where all conditions must be satisfied
8. code_generation — writing a correct, well-structured function from a clear spec (include the exact function signature and 2-3 example input/output pairs in the prompt)

Within each category: 2 easy, 2 medium, 1 hard.

Every task must be fully self-contained (all needed text/code inside the prompt) and
answerable in English without internet access.

Output ONLY a valid JSON array, no markdown fences, no commentary, in exactly this schema:

[
  {
    "task_id": "<category>_<easy|med|hard>_<n>",
    "category": "factual_knowledge",
    "difficulty": "easy",
    "prompt": "<the full task exactly as it would be given to the agent>",
    "gold_answer": "<the correct answer, complete>",
    "acceptance_criteria": "<one or two sentences telling a judge precisely what the answer must contain to be correct>"
  }
]

Quality requirements:
- Prompts must be unambiguous: exactly one defensible correct answer (or a tightly bounded set, spelled out in acceptance_criteria).
- For math: verify your own arithmetic before writing gold_answer.
- For code tasks: the gold code must actually run and satisfy the examples.
- Vary surface style: some terse prompts, some verbose, some with explicit format instructions ("answer in one sentence", "return JSON", "list only the entities").
