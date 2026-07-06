"""Synthesize dev tasks with COMPUTED gold answers — no LLM, no refusals,
no wrong gold labels. Covers the categories where correctness is checkable:
math (arithmetic computed), logic (brute-forced unique solutions), NER
(entities injected from pools), sentiment (label known by construction).

Writes data/dev_tasks/synth/batch1.md in paste format, so parse_batches.py
picks it up like any other source.

Usage: .venv/bin/python eval/synth_tasks.py
"""
import itertools
import json
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = random.Random(42)
tasks = []


def add(cat, diff, prompt, gold, criteria, n=[0]):
    n[0] += 1
    tasks.append({"task_id": f"{cat}_{diff}_{n[0]}", "category": cat, "difficulty": diff,
                  "prompt": prompt, "gold_answer": gold, "acceptance_criteria": criteria})


# ---------- mathematical_reasoning (computed) ----------
for _ in range(4):
    c = rng.randrange(240, 900, 20); p1 = rng.choice([12, 15, 18, 25]); p2 = rng.choice([8, 10, 20]); t = rng.choice([5, 6, 8])
    gold = round(c * (1 + p1 / 100) * (1 - p2 / 100) * (1 + t / 100), 2)
    add("mathematical_reasoning", "hard",
        f"A gadget is priced at ${c}. The seller raises the price by {p1}%, then offers a "
        f"{p2}% discount on the new price. At checkout, {t}% sales tax is added to the "
        f"discounted price. What is the final amount paid, in dollars rounded to 2 decimals?",
        f"${gold}", f"Final answer must be exactly {gold} dollars (allow $ sign and rounding notation differences).")

for _ in range(4):
    a, b, c2 = rng.sample([4, 5, 6, 8, 10, 12], 3)
    hours = round(1 / (1 / a + 1 / b + 1 / c2), 2)
    gold = round(hours * 60)
    add("mathematical_reasoning", "hard",
        f"Alice paints a fence alone in {a} hours, Ben in {b} hours, and Cara in {c2} hours. "
        f"Working together at these constant rates, how many MINUTES do they need to paint "
        f"the fence? Round to the nearest whole minute.",
        f"{gold} minutes", f"Final answer must be {gold} minutes (±1 for rounding).")

for _ in range(4):
    p = rng.randrange(20000, 90000, 5000); r = rng.choice([3, 4, 6, 7]); nyr = rng.choice([3, 4, 5])
    gold = round(p * (1 + r / 100) ** nyr - p)
    add("mathematical_reasoning", "hard",
        f"A town has {p} residents. Its population grows by {r}% each year. After {nyr} years "
        f"of this growth, how many MORE residents does the town have than today? Round to the "
        f"nearest whole person.",
        f"{gold}", f"Final answer must be {gold} (±2 for rounding differences).")

# ---------- logical_reasoning (brute-forced unique solutions) ----------
NAMES = ["Priya", "Marco", "Elena", "Tom", "Aisha", "Ken", "Sofia", "Raj"]
made = 0
while made < 8:
    people = rng.sample(NAMES, 5)
    seat = {p: i for i, p in enumerate(rng.sample(people, 5))}  # position 0..4 left->right
    order = sorted(people, key=lambda p: seat[p])
    cons, texts = [], []
    x, y = order[rng.randrange(4)], None
    y = order[seat[x] + 1]
    cons.append(lambda perm, x=x, y=y: perm.index(y) - perm.index(x) == 1)
    texts.append(f"{x} sits immediately to the left of {y}.")
    z = rng.choice([p for p in people if seat[p] in (1, 2, 3)])
    cons.append(lambda perm, z=z: perm.index(z) not in (0, 4))
    texts.append(f"{z} does not sit at either end.")
    w, v = rng.sample(people, 2)
    if seat[w] > seat[v]:
        w, v = v, w
    cons.append(lambda perm, w=w, v=v: perm.index(w) < perm.index(v))
    texts.append(f"{w} sits somewhere to the left of {v}.")
    e = order[rng.choice([0, 4])]
    cons.append(lambda perm, e=e: perm.index(e) in (0, 4))
    texts.append(f"{e} sits at one of the two ends.")
    sols = [perm for perm in itertools.permutations(people)
            if all(c(list(perm)) for c in cons)]
    if len(sols) != 1:
        continue
    made += 1
    middle = sols[0][2]
    add("logical_reasoning", "hard",
        "Five friends sit in a row of five chairs, positions numbered 1 (leftmost) to 5 "
        f"(rightmost): {', '.join(sorted(people))}. Constraints: " + " ".join(texts) +
        " Exactly one arrangement satisfies all constraints. Who sits in position 3 (the middle)?",
        middle, f"The answer must name {middle} as the person in the middle seat.")

# ---------- named_entity_recognition (entities known by construction) ----------
PEOPLE = ["Dr. Lena Fischer", "Carlos Mendes", "Yuki Tanaka", "Sarah O'Brien", "Ahmed Hassan"]
ORGS = ["Novatek Industries", "the World Health Organization", "Riverside University", "Zephyr Labs", "Banco Central"]
LOCS = ["Geneva", "São Paulo", "Osaka", "Dublin", "Cairo"]
DATES = ["March 12, 2025", "October 3, 2024", "July 1, 2026", "January 15, 2026", "August 30, 2025"]
seen_ner = set()
while len(seen_ner) < 8:
    p, p2 = rng.sample(PEOPLE, 2)
    o = rng.choice(ORGS)
    l, l2 = rng.sample(LOCS, 2)
    d = rng.choice(DATES)
    if (p, p2, o, l, l2, d) in seen_ner:
        continue
    seen_ner.add((p, p2, o, l, l2, d))
    sent = (f"{p} of {o} met {p2} in {l} on {d} to discuss expanding operations to {l2}.")
    gold = json.dumps({"persons": sorted([p, p2]), "orgs": [o.replace("the ", "")],
                       "locations": sorted([l, l2]), "dates": [d]})
    add("named_entity_recognition", "medium",
        f"Extract all named entities from this sentence and return ONLY a JSON object with "
        f'keys "persons", "orgs", "locations", "dates" (each a list of strings):\n\n"{sent}"',
        gold, "JSON must contain both persons, the organization, both locations, and the date; "
              "key names exactly as specified; no extra prose.")

# ---------- sentiment_classification (label known by construction) ----------
POS = ["the battery lasts three full days", "setup took under a minute", "the display is gorgeous",
       "customer support replied within the hour"]
NEG = ["the case cracked in the first week", "the app logs me out constantly",
       "shipping took a month", "the fan noise is unbearable"]
seen_rev = set()
i = 0
while i < 8:
    fmt = 'Respond in EXACTLY this format: "LABEL: <positive|negative|mixed> | REASON: <one sentence>".'
    if i % 3 == 0:
        a, b = rng.sample(POS, 2)
        rev, label = f"Honestly, {a}, and {b}. Couldn't ask for more.", "positive"
    elif i % 3 == 1:
        a, b = rng.sample(NEG, 2)
        rev, label = f"Disappointed: {a}, plus {b}.", "negative"
    else:
        a, b = rng.choice(POS), rng.choice(NEG)
        rev, label = f"Love that {a}, but {b}.", "mixed"
    if rev in seen_rev:
        continue
    seen_rev.add(rev)
    i += 1
    add("sentiment_classification", "medium",
        f"Classify the sentiment of this product review. {fmt}\n\nReview: \"{rev}\"",
        f"LABEL: {label} | REASON: The review is {label}.",
        f"Label must be '{label}' and the response must follow the LABEL/REASON format exactly.")

# ---------- write in paste format ----------
out_dir = f"{ROOT}/data/dev_tasks/synth"
os.makedirs(out_dir, exist_ok=True)
with open(f"{out_dir}/batch1.md", "w") as f:
    f.write("# synth — generated with computed gold answers\n\n---PASTE BELOW THIS LINE---\n\n")
    json.dump(tasks, f, indent=2, ensure_ascii=False)
print(f"generated {len(tasks)} synthetic tasks -> data/dev_tasks/synth/batch1.md")
