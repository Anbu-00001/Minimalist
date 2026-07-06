# Batch 3 — targeted prompts (one for Grok, one for Gemini)

Two different missions. Paste Grok's into `data/dev_tasks/grok/batch3.md`,
Gemini's into `data/dev_tasks/gemini/batch3.md`. Ctrl+S after pasting.

---

## GROK batch 3 — "hard mode" (escalation-boundary tasks)

I'm a hackathon participant building a practice test set to evaluate my own AI
agent before submission. I need HARD tasks — ones a small 4B language model
would typically get wrong but a strong large model gets right. Generate exactly
20 tasks:

- 10 × mathematical_reasoning — multi-step word problems mixing percentages,
  ratios, compound growth, unit conversions, and work/rate problems. Each needs
  3-6 chained computation steps. No trick questions: hard but unambiguous, with
  a single exact numeric answer.
- 6 × logical_reasoning — constraint puzzles with 4-6 entities and 5-8
  interacting constraints (seating, scheduling, truth-tellers/liars) where
  naive reasoning gives a wrong-but-plausible answer. Exactly one valid solution.
- 4 × code_debugging — Python snippets (10-25 lines) with exactly one SUBTLE
  bug: off-by-one, mutable default argument, integer division, shadowed
  variable, wrong comparison in edge case. The code must LOOK correct.

Difficulty: all "hard". Verify your own arithmetic and run your own logic
before writing gold_answer — a wrong gold answer poisons my eval set.

Output ONLY a valid JSON array, no markdown fences, no commentary:

[
  {
    "task_id": "<category>_hard_<n>",
    "category": "mathematical_reasoning",
    "difficulty": "hard",
    "prompt": "<the full self-contained task>",
    "gold_answer": "<the correct answer, complete>",
    "acceptance_criteria": "<what a judge must check, incl. the exact final number where applicable>"
  }
]

---

## GEMINI batch 3 — "format-follower" (strict output-format tasks)

I'm a hackathon participant building a practice test set to evaluate my own AI
agent before submission. I need tasks that test STRICT output-format
compliance — where the answer content is easy but the required format is
demanding. Generate exactly 20 tasks:

- 6 × sentiment_classification — reviews with mixed or sarcastic sentiment;
  require answers in an exact format like "LABEL: <positive|negative|mixed> |
  REASON: <one sentence>". Include the required format in the prompt.
- 5 × text_summarisation — include a 100-200 word passage in the prompt;
  require exact constraints: "exactly one sentence", "at most 12 words",
  "exactly 3 bullet points, each under 8 words".
- 5 × named_entity_recognition — include a 2-3 sentence passage; require the
  answer as strict JSON, e.g. {"persons": [], "orgs": [], "locations": [],
  "dates": []}, with the schema spelled out in the prompt.
- 4 × factual_knowledge — easy content, strict format: "exactly two
  sentences", "a numbered list of exactly 3 items", "one word only".

Difficulty: content easy/medium, format strict. The gold_answer must itself
follow the required format EXACTLY, and acceptance_criteria must state both the
content check and the format check.

Output ONLY a valid JSON array (no markdown fences, no commentary) in this schema:

[
  {
    "task_id": "<category>_fmt_<n>",
    "category": "sentiment_classification",
    "difficulty": "medium",
    "prompt": "<the full self-contained task, including the exact required output format>",
    "gold_answer": "<correct answer in exactly the required format>",
    "acceptance_criteria": "<content check + format check>"
  }
]
