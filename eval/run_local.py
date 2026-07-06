"""Run the agent against the merged dev set without Docker.

Usage: .venv/bin/python eval/run_local.py [N]   (N = task subsample, default all)

Reports per-category routing and scored-token usage, and writes
eval/results_dev.json with answers for judging (eval/judge.py, later).
Honors a local .env for FIREWORKS_API_KEY etc.
"""
import json
import os
import random
import sys
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# lightweight .env loader (dev only)
env_file = os.path.join(ROOT, ".env")
if os.path.exists(env_file):
    for line in open(env_file):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from agent import config, remote  # noqa: E402
from agent.router import solve  # noqa: E402

def main() -> None:
    tasks = json.load(open(f"{ROOT}/data/dev_tasks/merged.json"))
    if len(sys.argv) > 1:
        random.seed(0)
        tasks = random.sample(tasks, min(int(sys.argv[1]), len(tasks)))

    deadline = time.monotonic() + config.TOTAL_BUDGET_S
    out, t0 = [], time.monotonic()
    for i, task in enumerate(tasks):
        r = solve(task, deadline)
        r["true_category"] = task["category"]
        r["gold_answer"] = task["gold_answer"]
        r["acceptance_criteria"] = task["acceptance_criteria"]
        out.append(r)
        print(f"[{i+1}/{len(tasks)}] {task['task_id']}: route={r['route']} "
              f"cat={r['category']}({'ok' if r['category']==task['category'] else 'MISS'})",
              flush=True)

    elapsed = time.monotonic() - t0
    path = f"{ROOT}/eval/results_dev.json"
    json.dump(out, open(path, "w"), indent=2, ensure_ascii=False)

    print(f"\n{len(out)} tasks in {elapsed:.1f}s ({elapsed/max(len(out),1):.1f}s/task)")
    print("routes:", dict(Counter(r["route"] for r in out)))
    cat_acc = sum(r["category"] == r["true_category"] for r in out) / max(len(out), 1)
    print(f"classifier accuracy: {cat_acc:.0%}")
    print("scored tokens:", remote.usage)
    print(f"wrote {os.path.relpath(path, ROOT)}")

if __name__ == "__main__":
    main()
