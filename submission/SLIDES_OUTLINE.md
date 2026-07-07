# Slide deck outline (export to PDF; ~7 slides)

Build as HTML (reveal-style single page per slide) → print to PDF, or Google
Slides if faster. Keep text minimal; the deck is skimmed by pre-screeners.

1. **Title** — AMDA: Verify-Local-First Routing Agent. Track 1 · team-24.
   Cover art + one-liner: "Only pay for what you can't prove for free."

2. **The game** — Scoring = accuracy gate → then *fewest proxy tokens wins*.
   Local tokens = 0. Conclusion in bold: the scarce resource is **confidence
   in free answers**, not model capability.

3. **Architecture** — the cascade diagram (classify → local → verify →
   escalate). Emphasize verifiers as the novel piece: execution, label sets,
   format constraints, JSON schemas — correctness checked by code, not vibes.

4. **Token economics** — table: category × (local pass rate, escalation rate,
   expected tokens/task). ← FILL FROM BENCHMARKS. Note reasoning-model
   avoidance (thinking traces bill as output tokens).

5. **Evaluation rigor** — 228-task dev set, 5 independent generators,
   computed-gold synthetic tasks, deterministic judge mirroring the
   leaderboard. Screenshot of judge output table.

6. **Compliance & robustness** — I/O contract, env-driven config, 10-min
   budget guard with graceful degradation, remote-only fallback if local
   server dies, ≤10GB linux/amd64 image, no hardcoding.

7. **Results & close** — leaderboard position / dev-set numbers when
   available; repo + image URLs; team.
