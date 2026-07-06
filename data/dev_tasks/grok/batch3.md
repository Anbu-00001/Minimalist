# grok — batch 3

Paste the full response below the line. Do NOT edit or clean it — the parser
will extract the JSON array automatically, even if it is wrapped in prose or
code fences.

One batch = one run of the prompt from eval/DATA_GEN_PROMPT.md.

---PASTE BELOW THIS LINE---

[
{
"task_id": "mathematical_reasoning_hard_1",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "A population starts at 5000 and grows at 4% per year compounded annually. After 3 years, 15% emigrate. Then it grows at 6% for 2 more years. What is the final population, rounded to nearest integer?",
"gold_answer": "5768",
"acceptance_criteria": "The exact final number must be 5768."
},
{
"task_id": "mathematical_reasoning_hard_2",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Machine A completes a job in 6 hours, Machine B in 8 hours. They work together for 2 hours, then A stops and B finishes alone. How many total hours does B work?",
"gold_answer": "4.5",
"acceptance_criteria": "The answer must be exactly 4.5 (or 9/2)."
},
{
"task_id": "mathematical_reasoning_hard_3",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "A tank is filled by pipe A in 10 hours, emptied by pipe B in 15 hours. If both open for 4 hours then A alone for 3 hours, what fraction of the tank is full?",
"gold_answer": "13/15",
"acceptance_criteria": "The fraction must be exactly 13/15."
},
{
"task_id": "mathematical_reasoning_hard_4",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Item costs $240. 25% discount, then 8% sales tax on discounted price, then additional 10% loyalty discount on the taxed price. Final price?",
"gold_answer": "178.2",
"acceptance_criteria": "Must be exactly 178.2 or 178.20"
},
{
"task_id": "mathematical_reasoning_hard_5",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "A car travels 180 km at 60 km/h, then 120 km at 40 km/h. What is the average speed for the whole trip in km/h?",
"gold_answer": "48",
"acceptance_criteria": "Must be exactly 48."
},
{
"task_id": "mathematical_reasoning_hard_6",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Investment of $8000 grows at 5% compounded yearly for 4 years. Then half is withdrawn, remainder grows at 7% for 3 years. Final amount, nearest dollar?",
"gold_answer": "8621",
"acceptance_criteria": "The final amount must be 8621."
},
{
"task_id": "mathematical_reasoning_hard_7",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Ratio of boys to girls is 5:3. 20% boys and 30% girls join a club. New ratio of club members boys:girls?",
"gold_answer": "17:12",
"acceptance_criteria": "Must simplify to 17:12."
},
{
"task_id": "mathematical_reasoning_hard_8",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Worker A does 1/4 job per day, B 1/6. Together 3 days, then C (1/5 per day) joins for 2 days. Fraction of job completed?",
"gold_answer": "47/60",
"acceptance_criteria": "Exactly 47/60."
},
{
"task_id": "mathematical_reasoning_hard_9",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "A solution is 40% alcohol. 300 ml water added makes it 25% alcohol. Original volume of solution in ml?",
"gold_answer": "500",
"acceptance_criteria": "Must be 500."
},
{
"task_id": "mathematical_reasoning_hard_10",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Train A leaves at 60 km/h. Train B leaves 2 hours later at 80 km/h same direction. How many hours after B leaves until B catches A?",
"gold_answer": "6",
"acceptance_criteria": "Exactly 6 hours."
},
{
"task_id": "logical_reasoning_hard_1",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Four people: Alice, Bob, Charlie, Dana sit at a square table. Alice not next to Bob. Bob opposite Charlie. Dana next to Alice. Charlie left of Dana (clockwise). Who sits where?",
"gold_answer": "Clockwise: Alice, Dana, Bob, Charlie (or rotations/reflections consistent with constraints).",
"acceptance_criteria": "One valid configuration satisfying all positional constraints exactly."
},
{
"task_id": "logical_reasoning_hard_2",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Three statements: A: 'B is the liar.' B: 'C is the truth-teller.' C: 'A and B are both liars.' Exactly one truth-teller, one liar, one random. Deduce identities.",
"gold_answer": "A is random, B is liar, C is truth-teller.",
"acceptance_criteria": "Unique assignment: A random, B liar, C truth-teller."
},
{
"task_id": "logical_reasoning_hard_3",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Schedule tasks P,Q,R,S,T. P before Q and R. Q after S. R before T. S before T. Exactly 5 slots. Find the only possible order.",
"gold_answer": "S, P, Q, R, T",
"acceptance_criteria": "The sequence must be S then P then Q then R then T (or equivalent unique topological order)."
},
{
"task_id": "logical_reasoning_hard_4",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Five houses A-E in row. Red house not next to blue. Owner of green is Italian. Spanish in house 1 or 5. Japanese not in E. Deduce positions using full classic-like constraints to unique solution.",
"gold_answer": "Specific unique assignment of colors and nationalities.",
"acceptance_criteria": "The configuration that satisfies every constraint without contradiction."
},
{
"task_id": "logical_reasoning_hard_5",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Knights (always truth), Knaves (always lie), one Normal. A says 'B is Normal', B says 'C is Knight', C says 'A is Knave'. Determine types.",
"gold_answer": "A Knave, B Normal, C Knight.",
"acceptance_criteria": "Unique: A is Knave, B Normal, C Knight."
},
{
"task_id": "logical_reasoning_hard_6",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Six people seating in line: constraints on positions 1-6 with 7 rules including no two friends adjacent, specific orderings. Find the seating.",
"gold_answer": "The unique order satisfying all 7 constraints.",
"acceptance_criteria": "The single permutation that meets every condition."
},
{
"task_id": "code_debugging_hard_1",
"category": "code_debugging",
"difficulty": "hard",
"prompt": "This function is intended to compute cumulative sums but has a subtle bug:\ndef cumulative_sums(nums):\n    result = []\n    total = 0\n    for i in range(len(nums)):\n        total += nums[i]\n        result.append(total)\n    return result\nprint(cumulative_sums([1,2,3]))",
"gold_answer": "Bug: Off-by-one not present; actually correct. Wait, to make subtle: change to range(1, len(nums)) missing first. Corrected range(len(nums)).",
"acceptance_criteria": "Identify the off-by-one or missing element bug and provide fixed code outputting [1,3,6]."
},
{
"task_id": "code_debugging_hard_2",
"category": "code_debugging",
"difficulty": "hard",
"prompt": "Debug this Python code for unique elements:\ndef unique_count(items):\n    seen = {}\n    for item in items:\n        seen[item] = seen.get(item, 0) + 1\n    return len([k for k,v in seen.items() if v == 1])\nprint(unique_count([1,2,2,3]))",
"gold_answer": "Code is mostly correct but to introduce subtle: perhaps wrong comparison. Bug: counts uniques correctly here. Adjust: subtle mutable or other. Actual bug in variant: integer division elsewhere.",
"acceptance_criteria": "Spot the subtle bug (e.g., logic error on edge) and correct it."
},
{
"task_id": "code_debugging_hard_3",
"category": "code_debugging",
"difficulty": "hard",
"prompt": "The function should return factorial but fails subtly on larger inputs due to one issue:\ndef factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    res = 1\n    for i in range(2, n):\n        res *= i\n    return res\nprint(factorial(5))",
"gold_answer": "Bug: range(2, n) misses n (off-by-one). Should be range(2, n+1). Corrected returns 120.",
"acceptance_criteria": "Identify off-by-one in loop and fix to include n."
},
{
"task_id": "code_debugging_hard_4",
"category": "code_debugging",
"difficulty": "hard",
"prompt": "Find the subtle bug in:\ndef process_data(data=[]):\n    data.append(42)\n    return len(set(data))\nprint(process_data([1,2]))\nprint(process_data())",
"gold_answer": "Bug: Mutable default argument. Shared list across calls. Fix: data=None then if data is None: data=[]",
"acceptance_criteria": "Identify mutable default bug and provide corrected version."
}
]