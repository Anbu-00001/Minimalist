# gemini — batch 1

Paste the full response below the line. Do NOT edit or clean it — the parser
will extract the JSON array automatically, even if it is wrapped in prose or
code fences.

One batch = one run of the prompt from eval/DATA_GEN_PROMPT.md.

---PASTE BELOW THIS LINE---

\n}",
    "acceptance_criteria": "The response must be a valid JSON object containing 'main_thesis' under 15 words and 'key_causes' containing exactly three elements from the text."
  },
  {
    "task_id": "text_summarisation_hard_1",
    "category": "text_summarisation",
    "difficulty": "hard",
    "prompt": "Read the following passage about Earth's changing rotation. Summarize it in exactly 50 words. The summary must include the exact numbers '1.8' and '600' and must end with the word 'dynamics'.\n\nPassage:\n'Earth's rotation is not constant; it is slowly decelerating over geological timescales. This rotational deceleration is primarily caused by tidal friction from gravitational interactions with the Moon and Sun. On average, the length of a single day increases by approximately 1.8 seconds per century. This tiny shift accumulates over millions of years; indeed, scientific evidence shows that about 600 million years ago, a day on Earth lasted just 21 hours. Measuring these microscopic variations is vital for precise timekeeping systems and satellite navigation, which must account for these shifting rotational dynamics.'",
    "gold_answer": "Earth's rotation is decelerating by 1.8 seconds per century, meaning 600 million years ago a day was only twenty-one hours. This slow deceleration, driven by gravitational tides, requires advanced satellite systems and navigation networks to adjust timekeeping algorithms to account for these changing planetary rotational dynamics.",
    "acceptance_criteria": "The summary must be exactly 50 words long, include the numbers '1.8' and '600', and end with the word 'dynamics'."
  },
  {
    "task_id": "named_entity_recognition_easy_1",
    "category": "named_entity_recognition",
    "difficulty": "easy",
    "prompt": "Extract and label all entities belonging to the categories PERSON, ORG, LOCATION, and DATE from the following sentence. List each category as a bullet point:\n'On March 15, 44 BC, Julius Caesar was assassinated in the Theatre of Pompey in Rome.'",
    "gold_answer": "- PERSON: Julius Caesar\n- ORG: None\n- LOCATION: Theatre of Pompey, Rome\n- DATE: March 15, 44 BC",
    "acceptance_criteria": "The response must extract 'Julius Caesar' (PERSON), 'Theatre of Pompey' and 'Rome' (LOCATION), and 'March 15, 44 BC' (DATE) as bullet points."
  },
  {
    "task_id": "named_entity_recognition_easy_2",
    "category": "named_entity_recognition",
    "difficulty": "easy",
    "prompt": "Extract and label all entities belonging to the categories PERSON, ORG, LOCATION, and DATE from the following sentence. List only the entities found:\n'Albert Einstein presented his general theory of relativity to the Prussian Academy of Sciences in Berlin on November 25, 1915.'",
    "gold_answer": "- PERSON: Albert Einstein\n- ORG: Prussian Academy of Sciences\n- LOCATION: Berlin\n- DATE: November 25, 1915",
    "acceptance_criteria": "The output must extract 'Albert Einstein' (PERSON), 'Prussian Academy of Sciences' (ORG), 'Berlin' (LOCATION), and 'November 25, 1915' (DATE)."
  },
  {
    "task_id": "named_entity_recognition_med_1",
    "category": "named_entity_recognition",
    "difficulty": "medium",
    "prompt": "Extract all entities from the following text and return them as a JSON object with keys 'person', 'org', 'location', and 'date'. If an entity category has no values in the text, return an empty array:\n'In 1942, the Australian Army clashed with Japanese forces during the Battle of Kokoda, a conflict fought across the territory of Papua New Guinea.'",
    "gold_answer": "{\n  \"person\":,\n  \"org\": [\"Australian Army\", \"Japanese forces\"],\n  \"location\": [\"Papua New Guinea\"],\n  \"date\": [\"1942\"]\n}",
    "acceptance_criteria": "The response must be a valid JSON object extracting 'Australian Army' and 'Japanese forces' as ORG, 'Papua New Guinea' as LOCATION, and '1942' as DATE."
  },
  {
    "task_id": "named_entity_recognition_med_2",
    "category": "named_entity_recognition",
    "difficulty": "medium",
    "prompt": "Extract all entities from the following historical paragraph and list them labeled as PERSON, ORG, LOCATION, and DATE. Do not write any other commentary:\n'At the Yalta Conference in February 1945, Franklin D. Roosevelt of the United States, Winston Churchill of the United Kingdom, and Joseph Stalin of the Soviet Union met in the Crimea to discuss the post-war reorganization of Europe.'",
    "gold_answer": "PERSON: Franklin D. Roosevelt, Winston Churchill, Joseph Stalin\nORG: United States, United Kingdom, Soviet Union\nLOCATION: Yalta, Crimea, Europe\nDATE: February 1945",
    "acceptance_criteria": "The response must correctly categorize Roosevelt, Churchill, and Stalin as PERSON; US, UK, and Soviet Union as ORG; Yalta, Crimea, and Europe as LOCATION; and February 1945 as DATE."
  },
  {
    "task_id": "named_entity_recognition_hard_1",
    "category": "named_entity_recognition",
    "difficulty": "hard",
    "prompt": "Perform a precise entity extraction (categories: PERSON, ORG, LOCATION, DATE) on the complex text below. Return ONLY a valid JSON object with the keys 'person', 'org', 'location', and 'date'. Ensure multi-word or compound names are fully extracted:\n'On December 10, 1901, the first Nobel Prize in Chemistry was awarded to Jacobus Henricus van 't Hoff by the Royal Swedish Academy of Sciences in Stockholm, Sweden, for his work on chemical dynamics.'",
    "gold_answer": "{\n  \"person\": [\"Jacobus Henricus van 't Hoff\"],\n  \"org\":,\n  \"location\":,\n  \"date\":\n}",
    "acceptance_criteria": "The output must be a valid JSON object parsing 'Jacobus Henricus van 't Hoff' as PERSON, 'Royal Swedish Academy of Sciences' as ORG, 'Stockholm' and 'Sweden' as LOCATION, and 'December 10, 1901' as DATE."
  },
  {
    "task_id": "code_debugging_easy_1",
    "category": "code_debugging",
    "difficulty": "easy",
    "prompt": "The following Python function is designed to check if all values in a list exceed a given threshold. However, it contains exactly one logical bug. Identify the bug and provide the corrected code.\n\n```python\ndef check_threshold(values, threshold):\n    # Check if all values exceed threshold\n    for val in values:\n        if val <= threshold:\n            return False\n        else:\n            return True\n```",
    "gold_answer": "The bug is the early return of `True` inside the `else` block during the first iteration. This causes the function to return `True` as long as the first element exceeds the threshold, skipping the evaluation of the remaining values. Corrected code:\n\n```python\ndef check_threshold(values, threshold):\n    # Check if all values exceed threshold\n    for val in values:\n        if val <= threshold:\n            return False\n    return True\n```",
    "acceptance_criteria": "The response must explain that the `else` return causes an premature termination of the loop, and provide the code with `return True` outside the loop."
  },
  {
    "task_id": "code_debugging_easy_2",
    "category": "code_debugging",
    "difficulty": "easy",
    "prompt": "The following Python function is intended to calculate the average score of a list, but it contains exactly one logical bug. Identify the bug and provide the corrected code.\n\n```python\ndef calculate_average(scores):\n    # Calculate the average score\n    total = 0\n    for i in range(1, len(scores)):\n        total += scores[i]\n    return total / len(scores)\n```",
    "gold_answer": "The bug is an off-by-one indexing error in the `range` start parameter. `range(1, len(scores))` starts counting at index 1, meaning the first score at index 0 is skipped in the summation. Corrected code:\n\n```python\ndef calculate_average(scores):\n    # Calculate the average score\n    total = 0\n    for i in range(0, len(scores)):\n        total += scores[i]\n    return total / len(scores)\n```",
    "acceptance_criteria": "The response must identify that starting the loop range at 1 skips the index 0 element, and show the loop corrected to start at 0."
  },
  {
    "task_id": "code_debugging_med_1",
    "category": "code_debugging",
    "difficulty": "medium",
    "prompt": "The following Python function is designed to append a value to a list and display its state, but it contains exactly one bug. Identify the bug and provide the corrected code.\n\n```python\ndef append_to_list(val, my_list=):\n    # Append val to my_list with tracking\n    my_list.append(val)\n    print(f\"List state: {my_list}\")\n    return my_list\n```",
    "gold_answer": "The bug is the use of a mutable default argument (`my_list=`). In Python, default arguments are evaluated only once at function definition time, meaning that subsequent calls to the function without an explicit list parameter will append to and modify the exact same list instance. Corrected code:\n\n```python\ndef append_to_list(val, my_list=None):\n    # Append val to my_list with tracking\n    if my_list is None:\n        my_list =\n    my_list.append(val)\n    print(f\"List state: {my_list}\")\n    return my_list\n```",
    "acceptance_criteria": "The response must identify the mutable default list bug and correct it by using the standard `None` sentinel pattern inside the function signature."
  },
  {
    "task_id": "code_debugging_med_2",
    "category": "code_debugging",
    "difficulty": "medium",
    "prompt": "The following JavaScript function is meant to return an array of closures, each returning its respective index value. However, it contains exactly one scoping bug. Identify the bug and provide the corrected code.\n\n```javascript\nfunction createFunctions() {\n    var callbacks =;\n    for (var i = 0; i < 5; i++) {\n        callbacks.push(function() {\n            return i;\n        });\n    }\n    return callbacks;\n}\n```",
    "gold_answer": "The bug is the use of `var` to declare the loop variable `i`. Because `var` is function-scoped rather than block-scoped, all callbacks capture the exact same variable reference, meaning they will all return `5` (the final value of `i` after loop termination). Corrected code:\n\n```javascript\nfunction createFunctions() {\n    var callbacks =;\n    for (let i = 0; i < 5; i++) {\n        callbacks.push(function() {\n            return i;\n        });\n    }\n    return callbacks;\n}\n```",
    "acceptance_criteria": "The response must explain how `var` scoping causes closures to share a single variable reference, and resolve it by changing `var i` to `let i`."
  },
  {
    "task_id": "code_debugging_hard_1",
    "category": "code_debugging",
    "difficulty": "hard",
    "prompt": "The following Python function is designed to open a file, read its content, and return it as an integer, handling clean-up. However, it contains exactly one logical bug. Identify the bug and provide the corrected code.\n\n```python\ndef parse_file_integer(filepath):\n    # Read an integer from a file, handle clean-up\n    try:\n        f = open(filepath, 'r')\n        content = f.read().strip()\n        return int(content)\n    finally:\n        if 'f' in locals():\n            f.close()\n        return -1\n```",
    "gold_answer": "The bug is the `return -1` statement inside the `finally` block. In Python, executing a `return` (or `break`/`continue`) statement inside a `finally` block suppresses and discards any active exception (such as `FileNotFoundError` or `ValueError`) raised in the `try` block, preventing proper error propagation. Corrected code:\n\n```python\ndef parse_file_integer(filepath):\n    # Read an integer from a file, handle clean-up\n    with open(filepath, 'r') as f:\n        content = f.read().strip()\n        return int(content)\n```",
    "acceptance_criteria": "The response must identify that the `return` statement in the `finally` block suppresses exceptions raised in the `try` block, and provide corrected code (preferably using a `with` statement context manager)."
  },
  {
    "task_id": "logical_reasoning_easy_1",
    "category": "logical_reasoning",
    "difficulty": "easy",
    "prompt": "Three friends, Alice, Bob, and Charlie, are standing in a single-file line. Determine their positions from first (1st) to last (3rd) based on these clues:\n1) Alice is not first.\n2) Charlie is standing immediately behind Alice.",
    "gold_answer": "The positions of the friends from 1st to 3rd are:\n1st: Bob\n2nd: Alice\n3rd: Charlie\n\nJustification:\nAlice cannot be in the 1st position according to Clue 1. If Alice were in the 3rd (last) position, Charlie could not stand behind her according to Clue 2. Thus, Alice must be in the 2nd position, and Charlie must be immediately behind her in the 3rd position. This leaves Bob to occupy the 1st position.",
    "acceptance_criteria": "The response must identify the unique order as 1st: Bob, 2nd: Alice, and 3rd: Charlie, with a logical explanation."
  },
  {
    "task_id": "logical_reasoning_easy_2",
    "category": "logical_reasoning",
    "difficulty": "easy",
    "prompt": "On an island, residents are either Knights (who always tell the truth) or Knaves (who always lie). You meet two residents, A and B. A says: 'At least one of us is a Knave.' Determine the identities of A and B, justifying your answer.",
    "gold_answer": "A is a Knight, and B is a Knave.\n\nJustification:\nAssume A is a Knave. If A is a Knave, A's statement ('At least one of us is a Knave') would have to be false, meaning both of them are Knights. However, A cannot be both a Knight and a Knave. Therefore, our assumption is false, and A must be a Knight. Since A is a Knight, A's statement must be true. Since A is a Knight, for 'At least one of us is a Knave' to be true, B must be a Knave.",
    "acceptance_criteria": "The response must identify A as a Knight and B as a Knave, demonstrating the logical impossibility of A being a Knave."
  },
  {
    "task_id": "logical_reasoning_med_1",
    "category": "logical_reasoning",
    "difficulty": "medium",
    "prompt": "Five colleagues (Emily, Frank, Grace, Henry, Ivy) are sitting in a row of five seats, numbered 1 to 5 from left to right. Determine the seating positions of all five colleagues based on these constraints:\n1) Emily is sitting in seat 3.\n2) Frank is sitting to the immediate right of Grace.\n3) Henry is sitting in an even-numbered seat.\n4) Ivy is not sitting next to Emily.\n5) Ivy is sitting to the left of Emily.",
    "gold_answer": "The seating positions from left to right are:\n- Seat 1: Ivy\n- Seat 2: Henry\n- Seat 3: Emily\n- Seat 4: Grace\n- Seat 5: Frank\n\nJustification:\nBy Constraint 1, Emily is in seat 3. Constraint 5 says Ivy sits to the left of Emily (seats 1 or 2). Constraint 4 says Ivy is not next to Emily, so she cannot be in seat 2. Therefore, Ivy must be in seat 1. Frank and Grace must sit adjacent to each other (with Frank immediately to the right of Grace, forming a Grace-Frank block). Since seats 1 and 3 are occupied, the only adjacent free seats left are 4 and 5. Thus, Grace sits in seat 4 and Frank sits in seat 5. This leaves seat 2 as the only available position for Henry, which satisfies Constraint 3 since seat 2 is an even-numbered seat.",
    "acceptance_criteria": "The response must identify the exact seating positions: Seat 1: Ivy, Seat 2: Henry, Seat 3: Emily, Seat 4: Grace, Seat 5: Frank."
  },
  {
    "task_id": "logical_reasoning_med_2",
    "category": "logical_reasoning",
    "difficulty": "medium",
    "prompt": "Four tasks (P, Q, R, and S) must be scheduled from Monday to Thursday, with exactly one task scheduled per day. Determine the exact daily schedule based on these three constraints:\n1) P is scheduled on either Monday or Tuesday.\n2) Q is scheduled on the day immediately after R.\n3) S is scheduled on Thursday.",
    "gold_answer": "The daily task schedule is:\n- Monday: P\n- Tuesday: R\n- Wednesday: Q\n- Thursday: S\n\nJustification:\nAccording to Constraint 3, S is scheduled on Thursday. This leaves Monday, Tuesday, and Wednesday as available days. Constraint 2 states Q is scheduled on the day immediately after R, which means R and Q must form a consecutive block (R, then Q). This block can occupy either (Monday, Tuesday) or (Tuesday, Wednesday). If the block occupies (Monday, Tuesday), then Wednesday is left for P, which violates Constraint 1 (P must be on Monday or Tuesday). Therefore, the R-Q block must occupy Tuesday and Wednesday, leaving Monday as the only available day for P. This satisfies all constraints.",
    "acceptance_criteria": "The response must output the exact schedule: Monday: P, Tuesday: R, Wednesday: Q, Thursday: S."
  },
  {
    "task_id": "logical_reasoning_hard_1",
    "category": "logical_reasoning",
    "difficulty": "hard",
    "prompt": "Five events (A, B, C, D, and E) must be scheduled from Monday to Friday, with exactly one event per day. Determine the exact daily schedule based on these seven constraints:\n1) B is scheduled on a day immediately adjacent to D (either the day before or the day after).\n2) C must be scheduled earlier in the week than A.\n3) E cannot be scheduled on Monday or Friday.\n4) There is exactly one day between the scheduling of A and D.\n5) D is scheduled later in the week than B.\n6) C is not scheduled on Tuesday.\n7) D is not scheduled on Wednesday.",
    "gold_answer": "The daily event schedule is:\n- Monday: C\n- Tuesday: E\n- Wednesday: A\n- Thursday: B\n- Friday: D\n\nJustification:\nFrom Constraints 1 and 5, B and D are adjacent and D is later than B, forming a consecutive block 'B, D'. Constraint 4 states there is exactly one day between A and D. This leaves two possible patterns: either 'A, [day], B, D' (where A is before D) or 'B, D, [day], A' (where A is after D). Let's test both:\n\nCase 1: 'A, [day], B, D' (requiring 4 consecutive days).\n- Sub-case 1a: Monday: A, Tuesday: [free], Wednesday: B, Thursday: D. This leaves Tuesday and Friday for C and E. E cannot be on Friday (Constraint 3), so E must be on Tuesday and C on Friday. This violates Constraint 2 (C must be earlier than A, since A is Monday and C is Friday).\n- Sub-case 1b: Tuesday: A, Wednesday: [free], Thursday: B, Friday: D. This leaves Monday and Wednesday for C and E. E cannot be on Monday (Constraint 3), so E must be on Wednesday and C on Monday. This satisfies all constraints: Monday: C, Tuesday: A, Wednesday: E, Thursday: B, Friday: D. However, this violates Constraint 4 (there must be exactly one day between A and D; here, A is Tuesday and D is Friday, leaving two days between them). Wait, let's look at the phrasing 'exactly one day between the scheduling of A and D'. This means the sequence must be 'A, [one day], D', which is 'A, B, D' (since B is before D). Let's test the 'A, B, D' block (requiring 3 consecutive days):\n  - If Monday: A, Tuesday: B, Wednesday: D. This violates Constraint 7 (D is not scheduled on Wednesday).\n  - If Tuesday: A, Wednesday: B, Thursday: D. This leaves Monday and Friday for C and E. E cannot be on Monday or Friday (Constraint 3), making this invalid.\n  - If Wednesday: A, Thursday: B, Friday: D. This leaves Monday and Tuesday for C and E. E cannot be on Monday (Constraint 3), so E must be on Tuesday, and C on Monday. This satisfies all constraints: Monday: C (not Tuesday), Tuesday: E (not Mon/Fri), Wednesday: A, Thursday: B, Friday: D. Constraint 2 is met because C (Monday) is earlier than A (Wednesday). This is a valid schedule.\n\nCase 2: 'B, D, [day], A'. Since B and D must form 'B, D', and there is exactly one day between D and A, the block is 'B, D, [day], A' (4 consecutive days).\n- Sub-case 2a: Monday: B, Tuesday: D, Wednesday: [free], Thursday: A. This leaves Wednesday and Friday for C and E. E cannot be on Friday, so E must be on Wednesday and C on Friday. This violates Constraint 2 (C earlier than A, since A is Thursday and C is Friday).\n- Sub-case 2b: Tuesday: B, Wednesday: D, Thursday: [free], Friday: A. This violates Constraint 7 (D is not on Wednesday).\n\nTherefore, the unique schedule is: Monday: C, Tuesday: E, Wednesday: A, Thursday: B, Friday: D.",
    "acceptance_criteria": "The response must determine the exact schedule as Monday: C, Tuesday: E, Wednesday: A, Thursday: B, Friday: D, backed by a consistent logical deduction."
  },
  {
    "task_id": "code_generation_easy_1",
    "category": "code_generation",
    "difficulty": "easy",
    "prompt": "Write a Python function with the signature `reverse_words(s: str) -> str` that reverses each individual word in a sentence but preserves the original order of the words and spaces.\n\nExamples:\n- `reverse_words('hello world')` -> `'olleh dlrow'`\n- `reverse_words('Python is fun')` -> `'nohtyP si nuf'`",
    "gold_answer": "def reverse_words(s: str) -> str:\n    return \" \".join(word[::-1] for word in s.split(\" \"))",
    "acceptance_criteria": "The function must reverse the internal character sequence of each individual word while preserving word order and whitespace."
  },
  {
    "task_id": "code_generation_easy_2",
    "category": "code_generation",
    "difficulty": "easy",
    "prompt": "Write a JavaScript function with the signature `convertTemperature(temp, toUnit)` where `temp` is a number representing a temperature, and `toUnit` is a string that is either 'C' or 'F'. If `toUnit` is 'F', convert the temperature from Celsius to Fahrenheit. If `toUnit` is 'C', convert it from Fahrenheit to Celsius. Round the result to exactly one decimal place.\n\nExamples:\n- `convertTemperature(0, 'F')` -> `32` or `32.0`\n- `convertTemperature(100, 'C')` -> `37.8`\n- `convertTemperature(-40, 'F')` -> `-40` or `-40.0`",
    "gold_answer": "function convertTemperature(temp, toUnit) {\n    let result;\n    if (toUnit === 'F') {\n        result = (temp * 9 / 5) + 32;\n    } else if (toUnit === 'C') {\n        result = (temp - 32) * 5 / 9;\n    }\n    return parseFloat(result.toFixed(1));\n}",
    "acceptance_criteria": "The function must execute accurate temperature conversions and return a number rounded to exactly one decimal place."
  },
  {
    "task_id": "code_generation_med_1",
    "category": "code_generation",
    "difficulty": "medium",
    "prompt": "Write a Python function with the signature `group_anagrams(strs: list[str]) -> list[list[str]]` that groups a list of strings into sub-lists of anagrams. The sorting of sub-lists or individual elements inside sub-lists does not matter.\n\nExamples:\n- `group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])` -> `[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]`\n- `group_anagrams([''])` -> `[['']]`",
    "gold_answer": "def group_anagrams(strs: list[str]) -> list[list[str]]:\n    from collections import defaultdict\n    anagrams = defaultdict(list)\n    for s in strs:\n        sorted_s = \"\".join(sorted(s))\n        anagrams[sorted_s].append(s)\n    return list(anagrams.values())",
    "acceptance_criteria": "The function must group words that share identical character frequencies into isolated sub-lists."
  },
  {
    "task_id": "code_generation_med_2",
    "category": "code_generation",
    "difficulty": "medium",
    "prompt": "Write a Python function with the signature `run_length_encode(s: str) -> str` that performs basic run-length encoding. If the encoded string is not strictly shorter than the original input string, the function must return the original string.\n\nExamples:\n- `run_length_encode('aabcccccaaa')` -> `'a2b1c5a3'`\n- `run_length_encode('abcd')` -> `'abcd'`",
    "gold_answer": "def run_length_encode(s: str) -> str:\n    if not s:\n        return \"\"\n    encoded =\n    current_char = s\n    count = 1\n    for char in s[1:]:\n        if char == current_char:\n            count += 1\n        else:\n            encoded.append(f\"{current_char}{count}\")\n            current_char = char\n            count = 1\n    encoded.append(f\"{current_char}{count}\")\n    encoded_str = \"\".join(encoded)\n    return encoded_str if len(encoded_str) < len(s) else s",
    "acceptance_criteria": "The function must compress sequential characters, returning the compressed version only if its length is strictly less than the original input."
  },
  {
    "task_id": "code_generation_hard_1",
    "category": "code_generation",
    "difficulty": "hard",
    "prompt": "Write a Python class `Trie` that implements a prefix tree data structure. The class must support the following three methods:\n- `insert(word: str) -> None`: Inserts the string `word` into the trie.\n- `search(word: str) -> bool`: Returns `True` if the string `word` is in the trie, and `False` otherwise.\n- `startsWith(prefix: str) -> bool`: Returns `True` if there is a previously inserted string `word` that has the prefix `prefix`, and `False` otherwise.\n\nExamples:\n- `trie = Trie(); trie.insert('apple'); trie.search('apple')` -> `True`\n- `trie.search('app')` -> `False`\n- `trie.startsWith('app')` -> `True`",
    "gold_answer": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end_of_word = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str) -> None:\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                node.children[char] = TrieNode()\n            node = node.children[char]\n        node.is_end_of_word = True\n\n    def search(self, word: str) -> bool:\n        node = self.root\n        for char in word:\n            if char not in node.children:\n                return False\n            node = node.children[char]\n        return node.is_end_of_word\n\n    def startsWith(self, prefix: str) -> bool:\n        node = self.root\n        for char in prefix:\n            if char not in node.children:\n                return False\n            node = node.children[char]\n        return True",
    "acceptance_criteria": "The class must successfully implement insert, exact search, and prefix matching operations using a trie node architecture."
  }
]