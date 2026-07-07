# Demo video script (~2 minutes, screen recording + voiceover)

Record with OBS or SimpleScreenRecorder; 1080p; unlisted YouTube upload.
Keep it under 3 minutes — judges skim.

## Shot list

**[0:00–0:15] Hook — the scoreboard logic** (slide or terminal title card)
> "Track 1 ranks agents by tokens spent — and local tokens are free. So we
> built an agent that only pays for what it can't prove for free."

**[0:15–0:45] Architecture** (show README diagram)
> "Every task is classified by cheap keyword rules, answered by a 4-billion-
> parameter model running inside the container at zero token cost, and then —
> the key step — *deterministically verified*: we execute generated code,
> validate sentiment labels, count words against the prompt's own limits,
> parse NER JSON against the requested schema. If the check passes, that
> answer ships. Free."

**[0:45–1:15] Live run** (terminal: docker run with mounted input/output)
> "Here's the full contract run: the container boots its local model in a few
> seconds, processes the task file, and writes results. Watch the route log —
> most tasks stay local; only the hard failures escalate to Fireworks through
> the judging proxy, each to the cheapest capable allowed model."
- Show: `docker run …` then `cat output/results.json | head`
- Show the stderr diagnostic line: local vs remote counts + token usage.

**[1:15–1:45] Evaluation rigor** (show eval/judge.py output table)
> "We tuned this on our own 228-task dev set across all eight categories —
> including synthetic tasks whose gold answers are computed, not generated,
> so they can't be wrong — with a deterministic judge that measures exactly
> what the leaderboard measures."

**[1:45–2:00] Close** (cover image / repo page)
> "Verify locally, escalate surgically, spend tokens only where correctness
> demands it. AMDA — built for AMD Developer Hackathon Act II."

## Recording checklist
- [ ] Terminal font ≥ 16pt, dark theme
- [ ] Pre-pull the image so the run starts instantly
- [ ] Have output/ empty before the run so the write is visible
- [ ] Mute notifications
