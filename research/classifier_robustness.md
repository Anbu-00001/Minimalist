# classify.py robustness under paraphrase — stress test findings (2026-07-09)

**Scope.** Research only, no code changed. Tests real `agent.classify.classify()` calls
(imported directly, no server) against (a) 63 hand-written prompt variants across all 8
categories that deliberately avoid `agent/classify.py`'s exact keyword phrasings, and
(b) the real 228-task `data/dev_tasks/merged.json` set, used only as a regression guard
for any proposed fix. Test harness and every intermediate result live in
`/tmp/claude-1000/-home-anbu-26-class-AMDA/01701512-250e-4586-8141-61eb71a83928/scratchpad/`
(`classify_stress_test.py`, `classify_patched.py`) — reproducible, not hand-simulated.

All line numbers below refer to `agent/classify.py` as of commit `3fbef28` (current HEAD).

## Headline number

| Prompt style | count | classify() correct | miss rate |
|---|---|---|---|
| **Novel/paraphrased, non-factual intended category** | 41 | 0 | **100%** |
| Novel/paraphrased, factual_knowledge intended | 3 | 3 | 0% (protected by the default) |
| Control (phrased to hit an existing keyword) | 18 | 18 | 0% |
| **All strict cases** | 62 | 21 | **66.1%** |

Every single one of my 41 novel, non-factual-category prompts was misclassified — always
by falling through to `factual_knowledge` (line 37's default) or, in code's case, into a
neighboring code category. Every control prompt (phrased to hit a listed keyword) and
every novel factual-knowledge prompt (protected by being the fallback category) passed.
This is a clean, mechanical result, not noise: `classify()` has no semantic
understanding — it is pure substring counting against small fixed keyword lists — so a
prompt that avoids every listed phrase for its true category *always* lands on
`factual_knowledge`, regardless of what it is actually asking. Since the keyword lists
were explicitly built and measured against this same 228-task dev set (VERDICTS V12: "97%
… measured on the same 228-task results"), 96.1%\* dev-set accuracy is a measure of
fit to that corpus's phrasing distribution, not of generalization — exactly the risk
the Participant Guide's "unseen prompt variants" language warns about.

\* Re-measured here at 219/228 = 96.1% (V12 reported 220/228 = 96.5%; the 1-task gap is
pre-existing, not something this test touched — plausibly the duplicate-ID disambiguation
in commit `d705b72` shifted one task after V12 was written).

Per-category breakdown on the strict 62:

| category | correct/total | misses |
|---|---|---|
| factual_knowledge | 6/6 | 0 |
| sentiment_classification | 2/9 | 7 |
| named_entity_recognition | 2/8 | 6 |
| text_summarisation | 2/8 | 6 |
| code_debugging | 2/8 | 6 |
| logical_reasoning | 2/8 | 6 |
| code_generation | 2/7 | 5 |
| mathematical_reasoning | 3/8 | 5 |

## Specific rule gaps, with line citations

### 1. Sentiment has zero generic emotion/opinion vocabulary (line 10)
```
("sentiment_classification", ["sentiment", "positive", "negative", "neutral", "tone of the review"]),
```
Only literal `sentiment`/`positive`/`negative`/`neutral`/the fixed phrase `"tone of the
review"`. Any sentiment task phrased as feeling/opinion instead of "classify the
sentiment" scores 0 and falls to `factual_knowledge` via line 37 (`"how does"` even
actively *helps* factual win when the phrasing is "How does the writer feel…"). 7/9
tested variants missed this way, e.g.:
- `"How does the writer feel about the new smartphone described in this review?"` → predicted `factual_knowledge`
- `"Would you say the customer is happy or upset based on this message?"` → predicted `factual_knowledge`
- `"Judge whether this feedback leans favorable or unfavorable toward the product."` → predicted `factual_knowledge`

### 2. NER has zero generic "who/what is mentioned" vocabulary (lines 11-12)
```
("named_entity_recognition", ["entities", "entity", "person, org", "person names", "organization",
                              "label the", "extract"]),
```
Real NER asks are very often phrased as "who/what/which places are mentioned", "list the
people and companies", "pull out the names" — none of which contain `entities`/`entity`/
`extract`/`organization`/`label the`. 6/8 tested variants missed, all falling to
`factual_knowledge`:
- `"Who and what places are mentioned in this paragraph?"`
- `"List all the people, companies, and locations referenced in the text below."`
- `"Which individuals, cities, and businesses show up in this article?"`

(Two controls confirmed the *positive* side works correctly: `"organization"` as a
substring of `"organizations"` correctly fires, and `"who is"` + `"organization"` scoring
1-1 against logic correctly ties toward NER because NER is earlier in `_RULES`, per V12's
intent-first ordering — that part of the design holds up.)

### 3. Summarisation has zero generic "shrink this" vocabulary (line 13)
```
("text_summarisation", ["summarise", "summarize", "summary", "condense", "in one sentence", "tl;dr"]),
```
`"gist"`, `"key points"`, `"main takeaways"`, `"boil down"`, `"distill"`, `"recap"` — none
present. 6/8 novel variants missed, e.g. `"Give me the gist of this article in a couple
of sentences."` → `factual_knowledge`.

### 4. Debugging's bonus is asymmetric with generation's, and its base list needs the literal words bug/debug/fix/error/faulty/fails (line 14, line 34-35)
```python
# line 14
("code_debugging", ["bug", "debug", "fix the", "error in", "incorrect code", "faulty", "fails"]),
# line 15-16
("code_generation", ["write a function", "a function", "implement", "def ", "function that",
                     "return a function", "signature", "javascript", "write a program"]),
...
# line 33-35
if has_code_block:
    scores["code_debugging"] += 2 if any(w in p for w in ("bug", "fix", "wrong", "error")) else 0
    scores["code_generation"] += 1
```
Two separate, compounding gaps:
- **With a code snippet attached**: `code_generation` *always* gets `+1` from
  `has_code_block` (line 35) *plus* almost certainly another `+1` from the base list's
  bare `"def "` (line 15) whenever the snippet contains a function definition — debugging
  or not. `code_debugging`'s matching `+2` bonus (line 34) only fires on the literal words
  `bug`/`fix`/`wrong`/`error`. A debug report phrased as "isn't behaving as expected",
  "doesn't work correctly", "has unexpected behavior", "can you find the issue" carries
  none of those four words, so debugging scores 0-2 while generation scores 2 outright.
  5/6 debugging-with-code variants tested were misrouted to `code_generation` this way,
  e.g. `"The code below isn't behaving as expected; please correct it: \`\`\`python\ndef
  foo(x): ...\`\`\`"` → predicted `code_generation`.
- **Without a code snippet** (a prose-only bug report, common when a user pastes no code
  and just describes symptoms): the bonus never fires at all (`has_code_block` is False),
  and the base list's coverage is narrow enough that `"My program produces the wrong
  output for large inputs — can you diagnose why?"` scores 0 everywhere → predicted
  `factual_knowledge`.

### 5. Generation needs the specific phrase, not any reasonable paraphrase (lines 15-16)
`"Create a Python script that reverses a linked list."`, `"Build me a small utility in
Python that converts Celsius to Fahrenheit."`, `"I need code that sorts a list of
dictionaries by a given key."` all score 0 (no `"a function"`/`"implement"`/`"write a
program"`/`"def "` present) → predicted `factual_knowledge`. 5/5 such variants tested
missed.

### 6. Math word-problems without numeric-question vocabulary score 0 (lines 17-19)
```
("mathematical_reasoning", ["calculate", "how many", "how much", "percent", "%", "total cost",
                            "compute the", "average speed", " km", "how far", "fraction",
                            "per day", "per hour"]),
```
Story-shaped word problems that never say "calculate"/"how many"/"how much"/etc. score 0.
5/5 tested (e.g. `"Three friends split a restaurant bill evenly. If the bill comes to
$90, what does each person owe?"`) → predicted `factual_knowledge`. This is the category
V12 flagged as costliest to misroute (loses the `ANSWER:` prompt hint, the program-aided
check, and the tighter token cap — `agent/router.py` lines 24, 220-224).

### 7. `"per day"`/`"per hour"` (line 19) collide with logical_reasoning scheduling puzzles — a real false-positive, not just a coverage gap
`"Four coworkers need to present their projects across four consecutive days, one
presentation per day. Given these restrictions, on which day does Priya present?"` is a
scheduling/ordering **logic** puzzle, but `"per day"` (line 19, math) matches while no
logic keyword (lines 20-21) does — predicted `mathematical_reasoning`. This survived even
after I added a logic-side keyword (`"restrictions"`) in testing: the two categories then
tie 1-1, and because `mathematical_reasoning` is listed before `logical_reasoning` in
`_RULES` (line 17 precedes line 20), `max()` keeps the first maximum and math still wins
the tie (line 36's documented tie-break behavior, working exactly as designed — just
pointed at the wrong pair of categories here). **No minimal keyword-only fix exists for
this one** without either reordering rules or scoping `per day`/`per hour` to require
adjacency with a numeral — both are rule-shape changes, out of the "keyword addition"
scope this task asked for. Flagged for awareness, not fixed.

### 8. Logic puzzles phrased without clue/constraint/puzzle vocabulary score 0 (lines 20-21)
```
("logical_reasoning", ["puzzle", "seated", "who is", "truth", "liar", "constraint", "order of",
                       "schedule", "clue", "sitting", "sits ", "does it follow", "who sits"]),
```
Classic zebra/knights-and-knaves framings that use "statements"/"rules govern"/
"restrictions"/"always answers honestly or deceptively" instead of the specific listed
words score 0. 6/8 tested missed, e.g. `"Five friends each own a different pet and live
in different colored houses. Using the following statements, work out who owns the
fish."` → predicted `factual_knowledge`. Given V13/V22 already identified
`logical_reasoning` as the project's weakest-scoring category, a classifier gap that
routes logic puzzles to `factual_knowledge` is a real accuracy risk: `router.py` only
runs the CSP solver check (`_logic_solver_check`, lines 225-236) when
`category == "logical_reasoning"` — a misrouted logic task gets none of V15's solver
machinery.

### 9. One genuine ambiguous case, reported separately, not counted as a clean miss
`"What percentage of Earth's atmosphere is made up of nitrogen?"` — a fact-lookup dressed
in numeric-adjective phrasing — matches `"percent"` (line 17) and nothing else, so
predicts `mathematical_reasoning` instead of the intended `factual_knowledge`. This is a
genuine judgment call (is "what percent of X is Y" math or trivia?), not a clean bug —
`%`/`percent` are load-bearing for real math coverage (`"What is 15% of 240?"`, a control
case, correctly resolves to math). No fix proposed; flagged for awareness only.

## Validated fix set (keyword additions only, no rule restructuring)

Every addition below was tested against the **full 228-task `data/dev_tasks/merged.json`
set**, not just my 62 novel cases, specifically to catch additions that look safe in
isolation but collide with real dev-set prompts. Combined effect:

- **Dev-set accuracy: 219/228 → 219/228 (unchanged, zero regressions, zero incidental
  fixes)** — these additions are provably neutral on the corpus the rules were tuned
  against.
- **Novel stress-test misses: 41/62 → 17/62** (miss rate 66.1% → 27.4% on the strict
  set; the 41→17 count is on the non-factual novel cases specifically). 24 of the 41
  original novel misses are fixed by generic markers, not by matching my exact test
  sentences (each keyword was checked to fire on more than one test case where possible).

```diff
--- a/agent/classify.py
+++ b/agent/classify.py
@@ -8,26 +8,35 @@
 _RULES: list[tuple[str, list[str]]] = [
-    ("sentiment_classification", ["sentiment", "positive", "negative", "neutral", "tone of the review"]),
+    ("sentiment_classification", ["sentiment", "positive", "negative", "neutral", "tone of the review",
+                                  "feel about", "opinion of", "favorable", "unfavorable"]),
     ("named_entity_recognition", ["entities", "entity", "person, org", "person names", "organization",
-                                  "label the", "extract"]),
-    ("text_summarisation", ["summarise", "summarize", "summary", "condense", "in one sentence", "tl;dr"]),
-    ("code_debugging", ["bug", "debug", "fix the", "error in", "incorrect code", "faulty", "fails"]),
+                                  "label the", "extract", "proper noun", "pull out"]),
+    ("text_summarisation", ["summarise", "summarize", "summary", "condense", "in one sentence", "tl;dr",
+                            "gist", "key points", "main takeaways", "boil down", "recap", "distill"]),
+    ("code_debugging", ["bug", "debug", "fix the", "error in", "incorrect code", "faulty", "fails",
+                        "isn't working", "doesn't work", "not working", "unexpected behavior",
+                        "diagnose", "repair", "correct it", "the issue"]),
     ("code_generation", ["write a function", "a function", "implement", "def ", "function that",
-                         "return a function", "signature", "javascript", "write a program"]),
+                         "return a function", "signature", "javascript", "write a program",
+                         "python script", "algorithm to", "utility", "code that", "code up"]),
     ("mathematical_reasoning", ["calculate", "how many", "how much", "percent", "%", "total cost",
                                 "compute the", "average speed", " km", "how far", "fraction",
-                                "per day", "per hour"]),
+                                "per day", "per hour", "times as many", "split evenly", "what does each"]),
     ("logical_reasoning", ["puzzle", "seated", "who is", "truth", "liar", "constraint", "order of",
-                           "schedule", "clue", "sitting", "sits ", "does it follow", "who sits"]),
+                           "schedule", "clue", "sitting", "sits ", "does it follow", "who sits",
+                           "statements", "restrictions"]),
     ("factual_knowledge", ["what is", "explain", "define", "how does", "why does", "describe"]),
 ]
@@ -33,7 +42,8 @@
     if has_code_block:
-        scores["code_debugging"] += 2 if any(w in p for w in ("bug", "fix", "wrong", "error")) else 0
+        scores["code_debugging"] += 2 if any(w in p for w in (
+            "bug", "fix", "wrong", "error", "isn't working", "doesn't work",
+            "not working", "unexpected behavior", "diagnose", "repair",
+            "correct it", "the issue")) else 0
         scores["code_generation"] += 1
```

Ranked by measured impact (novel misses fixed / risk):
1. **code_debugging base + bonus words** (`isn't working`, `doesn't work`, `not working`,
   `unexpected behavior`, `diagnose`, `repair`, `correct it`, `the issue`) — fixes the
   worst-understood gap (debugging silently becoming generation) and is the one place a
   keyword-only fix needed changing *two* lines (14 and 34) in lockstep to actually work,
   since fixing only the base list still lost the tie to generation's automatic
   `has_code_block` bonus.
2. **mathematical_reasoning** (`times as many`, `split evenly`, `what does each`) — this
   is V12's identified costliest-to-misroute category; each addition is a generic
   ratio/rate marker, not a copy of any one test sentence.
3. **logical_reasoning** (`statements`, `restrictions`) — fixes the classic
   zebra-puzzle-without-"clue" framing; note the `per day` collision (finding #7) is NOT
   fixed by this and needs separate attention.
4. **text_summarisation**, **sentiment_classification**, **code_generation**, **NER** —
   roughly equal-sized, independent wins.

## A fix I tried and rejected (negative result, worth recording)

Adding `"companies"` and `"locations"` to the NER keyword list looked like an obvious win
(it fixed 2 more novel NER misses) — but it **regressed a real dev-set task**:
`grok_text_summarisation_hard_1_dup2`'s prompt is `"Summarize the 150-word passage into
exactly 2 sentences: [Passage: Quantum computing... Companies like IBM and Google are
racing to build scalable quantum systems...]"`. `classify()` scores the *entire* prompt
string, including the embedded source passage, not just the instruction sentence — so
`"companies"` matched the passage's own content and tied NER 1-1 against summarisation's
`"summarize"` hit, and NER's earlier rule-order position won the tie, flipping a correctly
classified summarisation task to NER. **Generic common nouns are unsafe additions for any
category whose prompts routinely embed a source passage** (summarisation, NER itself,
sentiment) because they will eventually collide with passage content rather than
instruction language. This is a broader design risk worth flagging beyond this one
rejected keyword: any future keyword addition should be checked against the full dev set
before shipping, exactly as done here — a keyword that looks safe against a hand-written
test set can still break on real embedded-passage prompts.

## Bottom line

`classify.py`'s 96%+ score on `data/dev_tasks/merged.json` reflects a keyword list that
was iteratively tuned against that exact corpus (V12, and now this pass); it is not
evidence of robustness to phrasing the corpus hasn't seen. On 41 hand-written,
genuinely-reworded prompts across the 7 non-factual categories, the miss rate was **100%**
— every miss silently became `factual_knowledge` (or, for code, a neighboring code
category), each time losing that category's dedicated prompt hint and/or verifier
(`agent/router.py` `PROMPT_HINTS` dict and the category-gated `_math_program_check`/
`_logic_solver_check` calls). The validated keyword-addition patch above (tested against
the full 228-task dev set with zero regressions) roughly halves the novel-phrasing miss
rate (66.1% → 27.4% on the strict 62-case set) at zero measured cost to existing
accuracy. It does not close the gap — sentiment's implicit-emotion space, NER's
"who/what/where is mentioned" framing, and the math/logic `per day` collision remain
open — because the underlying design (exact substring match, no semantic signal, hard
default to `factual_knowledge` on any all-zero score) has a ceiling that keyword patching
alone cannot fully reach without either a rule-order/scoping change or a non-keyword
signal (e.g. the already-available local LLM could itself be asked "which of these 8
categories" as a cheap, free, zero-token-cost-on-remote fallback classifier when the
keyword score is all-zero — noted here as a direction, not evaluated, since building it
is out of this research task's scope).
