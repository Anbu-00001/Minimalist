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
from .router import solve


def main() -> int:
    start = time.monotonic()
    deadline = start + config.TOTAL_BUDGET_S

    try:
        with open(config.INPUT_PATH, encoding="utf-8") as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"FATAL: cannot read {config.INPUT_PATH}: {e}", file=sys.stderr)
        return 1

    results, diagnostics = [], []
    for task in tasks:
        try:
            r = solve(task, deadline)
        except Exception as e:  # one bad task must not sink the run
            r = {"task_id": task.get("task_id", "?"), "answer": "Unable to answer.",
                 "route": f"error:{type(e).__name__}", "category": "?"}
        diagnostics.append(r)
        results.append({"task_id": r["task_id"], "answer": r["answer"]})

    os.makedirs(os.path.dirname(config.OUTPUT_PATH), exist_ok=True)
    with open(config.OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False)

    elapsed = time.monotonic() - start
    routes = [d["route"] for d in diagnostics]
    print(f"done: {len(results)} tasks in {elapsed:.1f}s | "
          f"local: {sum(r.startswith('local') for r in routes)} | "
          f"remote: {sum(r.startswith('remote') for r in routes)} | "
          f"scored tokens: {remote.usage}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
