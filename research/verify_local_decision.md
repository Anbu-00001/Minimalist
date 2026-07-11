# Verify-local-first vs remote-first — the endgame decision — 2026-07-11/12

STATUS: DRAFT IN PROGRESS — being filled in as the live run completes. Trust
timestamps over completeness if you are reading this mid-run.

Question: can a verified-local-first routing mode (escalate only on
verification failure, i.e. `REMOTE_FIRST = set()`) match the shipped
remote-first image's gate accuracy on the same 56-task stratified sample? If
yes, ship it and drop scored tokens from ~1.2-2.7k to near-zero.

## Method

- Baseline: `ghcr.io/anbu-00001/amda-agent:latest` digest `fb43f519`, HEAD
  `f4d5353`, exactly the run graded in `research/final_gate_projection.md`
  (51/56 = 91.1% artifact-corrected). `REMOTE_FIRST = {"factual_knowledge",
  "named_entity_recognition", "text_summarisation"}`.
- Experiment: same HEAD, working tree copied to a scratch directory (`.git`
  excluded, `models/` copied so the build is self-contained), exactly ONE
  line changed in `agent/router.py`: `REMOTE_FIRST = {"factual_knowledge",
  "named_entity_recognition", "text_summarisation"}` -> `REMOTE_FIRST =
  set()`. Verified via `diff -rq` against the original `agent/` tree that
  this is the only difference. Built as `amda-verify-local-exp`, never
  pushed anywhere (confirmed local-only tag).
- Sample: the IDENTICAL 56-task sample and 4 batch files from
  `eval/tmp_final_gate/batch{1..4}/input/tasks.json` (byte-identical, diffed
  before the run) — same tasks, same order, same batching.
- Run: 4 SEQUENTIAL docker batches, `--memory=4g --memory-swap=4g --cpus=2`,
  `TOTAL_BUDGET_S=540 REMOTE_RPM_LIMIT=5`, key/url/models from `.env`
  (never printed). Outputs + container logs in `eval/tmp_verify_local/`.
- Grading: same judge logic as `eval/judge.py`
  (`eval/tmp_verify_local/grade_all.py`, byte-for-byte the same script as
  `eval/tmp_final_gate/grade_all.py` except the working directory), then
  every fail/unsure manually re-verified with the same artifact-corrected
  methodology (code executed, logic brute-forced, paraphrases read against
  acceptance criteria) — extra scrutiny on factual_knowledge, NER,
  text_summarisation, since the 51/56 baseline never measured LOCAL answers
  for those three categories.
- Sentiment probe: the 2 sentiment_classification tasks that failed in the
  final-gate run (both shipped from the LOCAL route in that run — batch4's
  container log shows `local: 7 | remote: 7` for a batch of 7 sentiment + 7
  summarisation tasks, and summarisation was remote-first in that image, so
  all 7 local answers were the sentiment tasks) were sent directly to the
  remote model (`gemma-4-31b` via the Cerebras stand-in, `curl` to
  `$FIREWORKS_BASE_URL/chat/completions`), replicating the exact request
  `agent/remote.py`/`agent/router.py` would construct (system prompt,
  `REMOTE_SUFFIX`, `max_tokens=48`, `temperature=0` — sentiment has no
  `REMOTE_HINTS` entry).

## Results — placeholder, filled in after grading

(table, per-category deltas, flip diagnoses, token counts, sentiment probe
result, and final recommendation go here)
