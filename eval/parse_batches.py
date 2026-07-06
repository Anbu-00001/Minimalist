"""Parse pasted LLM responses in data/dev_tasks/*/batch*.md into one merged dev set.

Handles the usual chat-paste damage: markdown fences, prose around the JSON,
minified output, unescaped quotes (via json-repair), and truncated pastes
(salvages complete task objects).

Usage: .venv/bin/python eval/parse_batches.py
Writes: data/dev_tasks/merged.json
"""
import glob
import json
import os
import re
from collections import Counter

from json_repair import repair_json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ("task_id", "category", "prompt", "gold_answer", "acceptance_criteria")
CATEGORIES = {
    "factual_knowledge", "mathematical_reasoning", "sentiment_classification",
    "text_summarisation", "named_entity_recognition", "code_debugging",
    "logical_reasoning", "code_generation",
}
# tolerate common spelling drift from the bots
CATEGORY_ALIASES = {
    "text_summarization": "text_summarisation",
    "logical_deductive_reasoning": "logical_reasoning",
    "logical/deductive_reasoning": "logical_reasoning",
    "ner": "named_entity_recognition",
}


def _looks_like_task(t) -> bool:
    return isinstance(t, dict) and t.get("task_id") and t.get("prompt")


def extract_tasks(raw: str) -> list[dict]:
    """Pull a list of task dicts out of arbitrary pasted text.

    Tries a whole-array parse first, then a per-object salvage pass (for pastes
    that are truncated or have a syntax error partway through), and keeps
    whichever recovers more tasks.
    """
    body = raw.split("---PASTE BELOW THIS LINE---")[-1]
    # prefer a fenced block only if it actually holds the task JSON — prompts
    # themselves may contain code fences
    fence = re.search(r"```(?:json)?\s*(.*?)```", body, re.DOTALL)
    if fence and '"task_id"' in fence.group(1):
        body = fence.group(1)

    start = body.find("[")
    end = body.rfind("]")
    candidate = body[start:end + 1] if start != -1 and end > start else body
    parsed = repair_json(candidate, return_objects=True)
    if isinstance(parsed, dict):
        parsed = [parsed]
    whole = [t for t in parsed if _looks_like_task(t)] if isinstance(parsed, list) else []

    # salvage pass: split at each task-object boundary, repair chunks separately
    salvaged = []
    chunks = re.split(r'(?=\{\s*"task_id")', body)
    for chunk in chunks[1:]:  # chunks[0] is whatever precedes the first object
        chunk = chunk.rstrip().rstrip("],")
        obj = repair_json(chunk, return_objects=True)
        if isinstance(obj, list):
            obj = next((o for o in obj if _looks_like_task(o)), None)
        if _looks_like_task(obj):
            salvaged.append(obj)

    return whole if len(whole) >= len(salvaged) else salvaged


def normalise(task: dict, source: str) -> dict | None:
    cat = str(task.get("category", "")).strip().lower()
    cat = CATEGORY_ALIASES.get(cat, cat)
    if cat not in CATEGORIES:
        return None
    if not all(str(task.get(k, "")).strip() for k in REQUIRED):
        return None
    diff = str(task.get("difficulty", "medium")).strip().lower()
    diff = {"med": "medium"}.get(diff, diff)
    return {
        "task_id": f"{source}_{task['task_id']}",
        "category": cat,
        "difficulty": diff,
        "prompt": str(task["prompt"]),
        "gold_answer": str(task["gold_answer"]),
        "acceptance_criteria": str(task["acceptance_criteria"]),
        "source": source,
    }


def main() -> None:
    merged, seen_prompts = [], set()
    for path in sorted(glob.glob(f"{ROOT}/data/dev_tasks/*/batch*.md")):
        source = os.path.basename(os.path.dirname(path))
        raw = open(path, encoding="utf-8", errors="replace").read()
        if len(raw) < 600:  # untouched template
            continue
        tasks = extract_tasks(raw)
        kept = dropped = dupes = 0
        for t in tasks:
            norm = normalise(t, source)
            if norm is None:
                dropped += 1
                continue
            key = norm["prompt"].strip().lower()
            if key in seen_prompts:
                dupes += 1
                continue
            seen_prompts.add(key)
            merged.append(norm)
            kept += 1
        print(f"{os.path.relpath(path, ROOT)}: extracted {len(tasks)}, "
              f"kept {kept}, dropped {dropped}, cross-source dupes {dupes}")

    out = f"{ROOT}/data/dev_tasks/merged.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"\nwrote {len(merged)} tasks -> {os.path.relpath(out, ROOT)}")
    print("per category:", dict(sorted(Counter(t["category"] for t in merged).items())))
    print("per difficulty:", dict(Counter(t["difficulty"] for t in merged)))
    print("per source:", dict(Counter(t["source"] for t in merged)))


if __name__ == "__main__":
    main()
