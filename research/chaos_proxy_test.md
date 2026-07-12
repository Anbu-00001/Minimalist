# Chaos test: shipped image vs a hostile/degraded judging proxy — 2026-07-11/12

Deadline for this report: 08:00 IST 2026-07-12.

## Why this run exists

The organizers' backend is publicly overloaded ("delays and errors, large
queue"). Our shipped image `ghcr.io/anbu-00001/amda-agent:latest` routes
`factual_knowledge`, `named_entity_recognition`, and `text_summarisation`
remote-first (`agent/router.py` `REMOTE_FIRST`), with a retry ladder: up to
2 preference models, doubled to 3 attempts for `REMOTE_FIRST` categories,
each attempt going through `openai.OpenAI(max_retries=1)` (2 HTTP tries per
attempt) — worst case ≈ 6 HTTP attempts per remote-first task (independently
confirmed in `research/token_thrift_audit.md` §5). All of that was measured
only under a *healthy* remote (`research/remote_path_validation.md`,
`research/verify_local_decision.md`). This run asks: what happens when the
remote is dead, hanging, slow, or unauthenticated — does the image still
satisfy the hard contract (exit 0, valid JSON, every `task_id` answered,
under the runtime budget) without any code changes?

**No image or repo code was modified for this test.** Every run used the
existing local image `ghcr.io/anbu-00001/amda-agent:latest` (local id
`fb43f519c9a8`) unmodified.

## Method

- Fixed constraints for every scenario: `docker run --rm --memory=4g
  --memory-swap=4g --cpus=2`, `test_io/practice_tasks.json` (8 tasks) mounted
  read-only at `/input/tasks.json`, a fresh output dir mounted at `/output`,
  `-e TOTAL_BUDGET_S=540`.
- `REQUEST_TIMEOUT_S` was left at its `agent/config.py` default (25s) in
  every scenario — the repo's `.env` does not override it.
- Wall time was measured around the `docker run` invocation itself (`date
  +%s.%N` immediately before/after), so it includes image startup + local
  llama-server boot (~3-6s observed) + all 8 tasks + output flush — a
  slightly stricter measure than the in-container "done: N tasks in Xs" line
  main.py prints to stderr.
- Real credentials (`.env`) were used only for scenarios 3 and 4, read
  programmatically from the file; never echoed to any log or this report.
  Scenario 3's delay-proxy script reads `.env` directly on the host and
  re-injects the real `Authorization` header itself — the container's own
  `FIREWORKS_API_KEY` env var was set to an unused placeholder string, so
  the real key never entered the container's environment at all.
- Success bar per scenario: **exit 0 AND valid JSON AND 8/8 task_ids present
  AND wall time < 540s.**

## Result table

| # | Scenario | Exit code | Valid JSON | task_ids | Wall time | "Unable to answer." | Scored tokens (in/out/calls) | Bar met? |
|---|---|---|---|---|---|---|---|---|
| 1 | DEAD PROXY (connect-refused) | 0 | yes | 8/8 | 222.7s | 3/8 | 0 / 0 / 0 | **PASS** |
| 2 | BLACKHOLE PROXY (connect-timeout) | 0 | yes | 8/8 | **619.9s** | 3/8 | 0 / 0 / 0 | **FAIL — over budget** |
| 3 | SLOW PROXY (~20s latency, succeeds) | 0 | yes | 8/8 | 219.9s | 0/8 | 410 / 132 / 5 | **PASS** |
| 4 | AUTH-BROKEN (401) | 0 | yes | 8/8 | 212.2s | 3/8 | 0 / 0 / 0 | **PASS** |

Every scenario's `results.json` was syntactically valid JSON, a list of
exactly 8 objects, with all 8 expected `task_id`s present and no duplicates
or omissions. In every scenario where the remote call could not possibly
succeed (1, 2, 4), the scored-token meter stayed at exactly
`{'input_tokens': 0, 'output_tokens': 0, 'calls': 0}` — confirming failed
calls never record token usage, in any of the three distinct failure modes
tested (instant refusal, hung connection, 401). Scenario 3, the one case
where the remote call was reachable and correctly authenticated, shows real
non-zero usage (5 successful calls, 410 in / 132 out), which is the correct
and expected behavior, not a bug.

## Scenario 1 — DEAD PROXY (connect-refused)

`FIREWORKS_BASE_URL=http://127.0.0.1:9/v1` (port 9 inside the container,
nothing listening — instant `ECONNREFUSED`).

- `entrypoint: local model ready after 4s`
- `done: 8 tasks in 212.6s | local: 1 | remote: 0 | scored tokens: {'input_tokens': 0, 'output_tokens': 0, 'calls': 0}`
- Wall time 222.7s, well inside the 540s budget — nearly all of it is real
  local-CPU inference (2 vCPUs) across the 8 tasks; the dead-proxy remote
  failures themselves cost effectively nothing (sub-millisecond refusals).
- 3/8 "Unable to answer.": `practice-01` (factual_knowledge, REMOTE_FIRST —
  no local fallback attempted for this category by design, and both remote
  attempts refused instantly), `practice-06` (code_debugging) and
  `practice-07` (logical_reasoning) — both escalated after local
  verification failed/was inconclusive, the single-model remote attempt
  refused instantly, and the final local last-resort retry
  (`agent/router.py` ~300-324) also failed to produce a usable answer on
  this run (model-quality variance from the second temperature-0.7 sample,
  not a proxy/timing issue — plenty of budget, ~330s, remained unused).
- Bar: **met** on every dimension.

## Scenario 2 — BLACKHOLE PROXY (connect-timeout) — FAILS THE BAR

`FIREWORKS_BASE_URL=http://10.255.255.1:9999/v1` (non-routable IP; verified
separately with `wget -T2` that connections genuinely hang with no ICMP
rejection, consistent with a true black hole rather than a fast
network-unreachable error).

- `entrypoint: local model ready after 4s`
- `done: 8 tasks in 611.4s | local: 2 | remote: 0 | scored tokens: {'input_tokens': 0, 'output_tokens': 0, 'calls': 0}`
- **Wall time 619.9s — 80s (≈15%) over the 540s `TOTAL_BUDGET_S` target.**
- Exit code was still 0 and `results.json` was still valid and complete
  (8/8 task_ids, 3/8 "Unable to answer.": `practice-01`, `practice-07`,
  `practice-08`) — because nothing external interrupted the process in this
  test. **The process ran to natural completion 80s past its own intended
  deadline; no internal mechanism forced it to stop earlier.**
- Token meter still correctly reads all-zero — a hung/timed-out call also
  never records usage.

### Exact failure mode (root cause, from reading the code)

`agent/router.py`'s `solve()` has no deadline check inside the remote-
escalation loop:

```python
for model in models:
    remote_answer = remote.complete(remote_prompt, model=model,
                                    max_tokens=cap, system=SYSTEM)
    ...
```

This loop always runs every scheduled model attempt (up to 2, doubled to
`models + models[:1]` for `REMOTE_FIRST` categories) to completion or to its
own timeout, **regardless of how much of `deadline` remains.** Each
`remote.complete()` call goes through `agent/remote.py`'s
`OpenAI(timeout=REQUEST_TIMEOUT_S, max_retries=1)`, so on a hanging
connection a single call can legitimately take up to ~2×25s = 50s before
giving up. `REMOTE_FIRST` categories (factual_knowledge,
named_entity_recognition, text_summarisation — 3 of the 8 practice tasks)
skip local generation entirely and go straight to this loop with 2 attempts
= up to 100s worst case, *always* incurred against a black hole since the
call can never succeed. `agent/main.py`'s outer per-task loop
(`for task in tasks: r = solve(task, deadline)`) also never checks
`time.monotonic()` against `deadline` between tasks — a budget already
exhausted by earlier tasks does not stop later tasks from independently
running their own full remote-retry ladder.

`deadline` is used only as an *advisory* signal inside `solve()` — it gates
whether to attempt extra local verification steps (`time_left > 60/90`) and
whether to attempt one last local retry before giving up
(`deadline - time.monotonic() > REQUEST_TIMEOUT_S + 5`) — but it never gates
the remote-escalation loop itself, which is exactly the code path a hanging
proxy exercises.

Compounding this: `agent/main.py` writes `results.json` **exactly once**,
only after every task in the input has been fully processed
(`json.dump(results, f, ...)` runs after the `for task in tasks` loop
completes — there is no incremental or atomic partial write during the
loop). `agent/config.py`'s own comment describes `TOTAL_BUDGET_S=540` as
deliberately set with "headroom" below "a 10-minute hard cap on the judging
VM" — implying the intended safety margin is ~60s. The measured overrun
here (619.9s) is close to and could plausibly exceed that presumed 600s
external cap too, depending on real judging-VM enforcement details we
cannot observe from here. **If anything external enforces a wall-clock kill
at or near that boundary (the judging harness itself, a wrapper script, a
cgroup limit), the process would very likely be killed before
`results.json` is ever written — turning "one bad category on one task"
into zero output for the entire run.** This was not independently
reproduced with a forced external kill in this test (a supplementary
`timeout 600 docker run ...` run was started but aborted early to prioritize
finishing the four required scenarios; the `write-once` behavior itself was
confirmed directly by reading `agent/main.py`, independent of that aborted
run). This is reasoned risk analysis grounded in the code and the measured
80s overrun, not an empirically observed kill event — flagged as such.

### Minimal fix proposals (not implemented by this test — analysis only)

1. Give the connect phase its own short deadline, separate from the full
   read timeout, so a black-holed (packet-drop) proxy fails fast instead of
   riding the full `REQUEST_TIMEOUT_S` per attempt.
2. Add a per-task deadline check in `agent/main.py`'s main loop: once
   `time.monotonic() >= deadline`, stop calling `solve()` for the remaining
   tasks and directly emit a cheap fallback answer for every remaining
   `task_id`, bounding the total overrun to at most one task's worth of
   work no matter how many tasks remain.
3. Add a deadline check inside the `for model in models:` remote-escalation
   loop (`agent/router.py`, the loop starting ~line 276) as a second layer:
   break out (falling through to the existing local last-resort /
   `"Unable to answer."` path) once `deadline - time.monotonic() <= 0`,
   instead of unconditionally trying every scheduled model — this still
   matters even with fix 1, since a "connects fine but never sends a
   response" (slow-loris-style) hang still rides the full read timeout on
   every retry/model attempt.
4. **Highest leverage, still open:** write `results.json`
   incrementally/defensively — flush an atomically-renamed partial file
   after each task is solved, not only once at the very end. This is the
   one change that converts "the run gets killed near the boundary" from a
   total zero into a partial-credit result, directly serving the code's own
   documented design rule ("malformed/missing output costs the whole run").

**Update, post-measurement:** while this test was in progress, `agent/remote.py`
was changed in the working tree to address fix 1 directly — the client's
`timeout=` argument is now `httpx.Timeout(config.REQUEST_TIMEOUT_S,
connect=5.0)` instead of the previous single scalar timeout, so the connect
phase now gets its own 5s deadline instead of riding the full 25s read
timeout. This targets exactly the failure mode scenario 2 measured (a
non-routable IP, which is a pure connect-phase hang) and, worked through the
same arithmetic as above, should shrink the worst-case blackhole overhead
from ~400s to roughly ~80s of remote-hang time across the 8 practice tasks —
likely enough to bring total wall time back under the 540s budget for this
specific failure shape. **This fix is in the source tree only — it is not
in the already-built image (`ghcr.io/anbu-00001/amda-agent:latest`, id
`fb43f519c9a8`) that every measurement in this report was run against, and
would need a rebuild to take effect for submission.** It also does not
close fixes 2-4: a slow-loris-style hang (connects immediately, then never
sends a response body) would still ride the full read timeout on every
attempt, and `results.json` is still written exactly once, so the
structural risk of total output loss under an external kill near the
boundary is reduced in likelihood by fix 1 but not eliminated.

## Scenario 3 — SLOW PROXY (~20s latency, succeeds)

Real Cerebras endpoint (`FIREWORKS_BASE_URL` from `.env`) reached through a
host-side Python delay-proxy (`0.0.0.0:8899`, sleeps 20s per request, then
forwards via `httpx` and re-injects the real `Authorization` header read
directly from `.env` — the container never saw the real key). Container
reached the proxy via the Docker bridge gateway (`172.17.0.1:8899`).

- `entrypoint: local model ready after 3s`
- `done: 8 tasks in 212.9s | local: 3 | remote: 5 | scored tokens: {'input_tokens': 410, 'output_tokens': 132, 'calls': 5}`
- Wall time 219.9s, well inside budget. All 5 proxied requests logged `200`
  at the proxy (visible in the proxy's access log, no headers/keys logged).
- **0/8 "Unable to answer."** — every task got a real, on-topic answer; the
  ~20.5s round trip (20s sleep + real network latency) stays comfortably
  under the 25s `REQUEST_TIMEOUT_S`, so no call needed a retry.
- Bar: **met** on every dimension; this is the cleanest of the four runs.

## Scenario 4 — AUTH-BROKEN (401)

Real `FIREWORKS_BASE_URL` from `.env`, `FIREWORKS_API_KEY=invalid_key_test`.

- `entrypoint: local model ready after 3s`
- `done: 8 tasks in 204.8s | local: 2 | remote: 0 | scored tokens: {'input_tokens': 0, 'output_tokens': 0, 'calls': 0}`
- Wall time 212.2s, well inside budget — a 401 fails fast (no timeout
  waiting), similar in shape to the dead-proxy case.
- 3/8 "Unable to answer." (`practice-01`, `practice-06`, `practice-07`) —
  same pattern as scenario 1, consistent with model-quality variance in the
  final local retry rather than anything time-budget related.
- Bar: **met** on every dimension.

## Final verdict

**Not fully safe to leave frozen as-is.** Three of the four hostile
scenarios (dead proxy, slow-but-working proxy, broken auth) comfortably
clear every bar item, each finishing in ~210-220s — under 40% of the 540s
budget — with correct zero-token accounting on every failed call. Those
three failure shapes (instant refusal, 401, and a proxy that's merely slow)
are handled safely by the shipped image exactly as designed.

The exception is the **BLACKHOLE PROXY (hung connection)** scenario, which
is not a contrived edge case — a publicly overloaded backend under "large
queue" load is a plausible source of exactly this failure shape (accepted
connections that never respond, as opposed to clean refusals). This run
measured a **reproducible 80-second (≈15%) overrun of `TOTAL_BUDGET_S`**,
with exit 0 and valid/complete output only because nothing external
interrupted the process in this test. The root cause is structural and
confirmed by direct code reading, not speculative: `agent/router.py`'s
remote-retry loop and `agent/main.py`'s per-task loop are both blind to the
deadline once entered, and `results.json` is written exactly once, at the
very end, with no incremental fallback. Given `agent/config.py`'s own
comment implies only ~60s of headroom was budgeted against a presumed
10-minute external hard cap, and the measured overrun both exceeds the
internal budget and eats most or all of that presumed headroom, this is a
real — not theoretical — risk of the entire run scoring zero if the actual
judging infrastructure enforces a wall-clock cutoff anywhere near that
boundary, which is a normal thing for judging infrastructure to do.

Recommendation: item 4 above (incremental/defensive `results.json` writes)
is the highest-leverage, lowest-risk fix still open and is worth raising to
the owner before the submission freezes. A fix for the specific connect-hang
mechanism scenario 2 exercised has already landed in the source tree
(`agent/remote.py`'s split connect/read timeout, noted above) — but **the
currently-shipped, already-built image does not contain it**, since Docker
images are immutable snapshots and no rebuild has happened since. If that
image is what actually gets frozen and submitted, the blackhole-overrun risk
measured in this report still applies to it exactly as measured. If the
image is rebuilt from the current source tree before the freeze, this
specific failure shape is very likely resolved (though not re-measured
here — a rebuild would need its own quick scenario-2 re-run to confirm)
and only the residual, lower-probability slow-loris / write-once risk would
remain. Everything else measured here (scenarios 1, 3, 4) supports shipping
either version of the image unchanged.
