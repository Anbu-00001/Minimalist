"""Container entrypoint. Contract (Participant Guide):
  read /input/tasks.json -> [{"task_id", "prompt"}]
  write /output/results.json -> [{"task_id", "answer"}]  (valid JSON or score zero)
  exit 0 on success, within the 10-minute budget.

Design rule: never crash, never miss a task_id — a weak answer for one task
costs a little accuracy; malformed/missing output costs the whole run.
"""
import json
import os
import sys
import time

from . import config, remote
from .classify import classify
from .router import solve

# Processing order under time pressure: cheapest/most-reliable categories
# first, so if the deadline guard ever has to shed tasks, the placeholders
# land on the fewest possible tasks — and on the slowest, weakest category
# (logic) rather than on four code tasks (cap4 batch1, 2026-07-12). The
# OUTPUT file keeps the input's task order regardless; only the solving
# order changes.
_SPEED_ORDER = {
    "mathematical_reasoning": 0,    # expression path, ~2 tiny decodes, ~13s
    "sentiment_classification": 1,  # local cap 48, ~18s
    "factual_knowledge": 2,         # local cap 56, ~22s
    "named_entity_recognition": 3,  # local cap 128, ~28s
    "text_summarisation": 4,        # local cap 88 + long prefill, ~45s
    "code_generation": 5,           # local cap 128, ~45s
    "code_debugging": 6,            # local cap 128 + long prompt, ~50s
    "logical_reasoning": 7,         # gen + CSP-solver translate, ~65s; also
                                    # the weakest category — sheds first
}
# (updated 2026-07-12 evening: code_debugging was ranked 0 from its
# straight-to-remote era; under pure-local it is among the slowest, and the
# stale rank made an all-code dev batch starve its codegen tasks into
# deadline placeholders.)


def main() -> int:
    start = time.monotonic()
    deadline = start + config.TOTAL_BUDGET_S

    try:
        with open(config.INPUT_PATH, encoding="utf-8") as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"FATAL: cannot read {config.INPUT_PATH}: {e}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(config.OUTPUT_PATH), exist_ok=True)

    answered: dict = {}

    def flush() -> None:
        """Atomically write answered-so-far + placeholders for the rest, in
        the INPUT's task order (never assume the grader joins on task_id),
        so a hard external kill at ANY moment still leaves a valid, complete
        file (chaos test 2026-07-12: a blackholed proxy ran the old
        single-write design 80s past budget — a kill there = zero output)."""
        full = [{"task_id": t.get("task_id", "?"),
                 "answer": answered.get(t.get("task_id", "?"), "Unable to answer.")}
                for t in tasks]
        tmp = config.OUTPUT_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(full, f, ensure_ascii=False)
        os.replace(tmp, config.OUTPUT_PATH)

    diagnostics = []
    flush()  # valid output exists from second zero
    ordered = sorted(tasks, key=lambda t: _SPEED_ORDER.get(
        classify(t.get("prompt", "")), 8))
    for task in ordered:
        if time.monotonic() >= deadline:  # budget gone: placeholders are
            break                         # already on disk for the rest
        try:
            r = solve(task, deadline)
        except Exception as e:  # one bad task must not sink the run
            r = {"task_id": task.get("task_id", "?"), "answer": "Unable to answer.",
                 "route": f"error:{type(e).__name__}", "category": "?"}
        diagnostics.append(r)
        answered[r["task_id"]] = r["answer"]
        flush()

    elapsed = time.monotonic() - start
    routes = [d["route"] for d in diagnostics]
    print(f"done: {len(answered)} tasks in {elapsed:.1f}s | "
          f"local: {sum(r.startswith('local') for r in routes)} | "
          f"remote: {sum(r.startswith('remote') for r in routes)} | "
          f"scored tokens: {remote.usage}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
