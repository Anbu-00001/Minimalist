# gemini — batch 2

Paste the full response below the line. Do NOT edit or clean it — the parser
will extract the JSON array automatically, even if it is wrapped in prose or
code fences.

One batch = one run of the prompt from eval/DATA_GEN_PROMPT.md.

---PASTE BELOW THIS LINE---

\n  "org":,\n  "location":,\n  "date": ["November 1915"]\n}",
"acceptance_criteria": "The output must be a valid JSON object containing 'Albert Einstein' (person), 'Prussian Academy of Sciences' (org), 'Berlin' (location), and 'November 1915' (date)."
},
{
"task_id": "named_entity_recognition_med_2",
"category": "named_entity_recognition",
"difficulty": "medium",
"prompt": "Identify all entities from the following text and list them labeled as PERSON, ORG, LOCATION, and DATE. Be precise and do not include any explanatory commentary:\n'Ada Lovelace collaborated with Charles Babbage on the Analytical Engine at the University of London during the summer of 1843.'",
"gold_answer": "PERSON: Ada Lovelace, Charles Babbage\nORG: University of London\nLOCATION: None\nDATE: summer of 1843",
"acceptance_criteria": "The output must extract 'Ada Lovelace' and 'Charles Babbage' as PERSON, 'University of London' as ORG, 'None' as LOCATION, and 'summer of 1843' as DATE."
},
{
"task_id": "named_entity_recognition_hard_1",
"category": "named_entity_recognition",
"difficulty": "hard",
"prompt": "Extract all entities from the following sentence. Return ONLY a valid JSON object where keys are the entity names and values are their corresponding labels (choose from: PERSON, ORG, LOCATION, DATE):\n'At the historic Geneva Conference held in July 1954, representatives of France, Great Britain, the United States, the Soviet Union, and the People's Republic of China met in Switzerland to discuss the restoration of peace in Indochina, with Zhou Enlai playing a prominent role.'",
"gold_answer": "{\n  "Geneva": "LOCATION",\n  "July 1954": "DATE",\n  "France": "ORG",\n  "Great Britain": "ORG",\n  "the United States": "ORG",\n  "the Soviet Union": "ORG",\n  "the People's Republic of China": "ORG",\n  "Switzerland": "LOCATION",\n  "Indochina": "LOCATION",\n  "Zhou Enlai": "PERSON"\n}",
"acceptance_criteria": "The response must be a valid JSON object mapping the extracted entities to their correct labels, including Zhou Enlai as PERSON, July 1954 as DATE, and Switzerland/Indochina/Geneva as LOCATION."
},
{
"task_id": "code_debugging_easy_1",
"category": "code_debugging",
"difficulty": "easy",
"prompt": "The following Python function is intended to compute the factorial of a positive integer n (where n >= 1). However, it contains exactly one logical bug. Identify the bug and provide the corrected code.\n\npython\ndef calculate_factorial(n):\n    result = 1\n    for i in range(1, n):\n        result *= i\n    return result\n",
"gold_answer": "The bug is an off-by-one error in the range parameters. range(1, n) generates numbers from 1 up to n-1, which excludes the number n itself from the product. Corrected code:\n\npython\ndef calculate_factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result\n",
"acceptance_criteria": "The response must identify the off-by-one error in range(1, n) excluding n, and provide the corrected loop as range(1, n + 1)."
},
{
"task_id": "code_debugging_med_1",
"category": "code_debugging",
"difficulty": "medium",
"prompt": "The following Python function implements binary search to find the index of a target value in a sorted list. However, it contains exactly one logical/indexing bug that can lead to an infinite loop. Identify the bug and provide the corrected code.\n\npython\ndef binary_search(arr, target):\n    low = 0\n    high = len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid\n        else:\n            high = mid - 1\n    return -1\n",
"gold_answer": "The bug is in the statement low = mid. If the target is greater than the middle element, low should be set to mid + 1. Keeping low = mid causes an infinite loop when low and high are adjacent and arr[mid] < target evaluates to true, as the division will continually select the same mid index. Corrected code:\n\npython\ndef binary_search(arr, target):\n    low = 0\n    high = len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n",
"acceptance_criteria": "The response must identify that setting low = mid causes an infinite loop when search elements are adjacent, and correct it to low = mid + 1."
},
{
"task_id": "code_debugging_med_2",
"category": "code_debugging",
"difficulty": "medium",
"prompt": "The following JavaScript function is designed to slice a flat array into nested sub-arrays (chunks) of a specified maximum size. However, it contains exactly one logical/indexing bug. Identify the bug and provide the corrected code.\n\njavascript\nfunction chunkArray(arr, size) {\n    const chunked =;\n    let index = 0;\n    while (index < arr.length) {\n        chunked.push(arr.slice(index, index + size));\n        index += size - 1;\n    }\n    return chunked;\n}\n",
"gold_answer": "The bug is the line index += size - 1;. By subtracting 1 from the size, the code will include overlapping elements across chunks, and if the size is 1, it will cause an infinite loop because index will never increment. Corrected code:\n\njavascript\nfunction chunkArray(arr, size) {\n    const chunked =;\n    let index = 0;\n    while (index < arr.length) {\n        chunked.push(arr.slice(index, index + size));\n        index += size;\n    }\n    return chunked;\n}\n",
"acceptance_criteria": "The response must identify that index += size - 1 causes duplicate elements and potential infinite loops, and correct it to index += size."
},
{
"task_id": "code_debugging_hard_1",
"category": "code_debugging",
"difficulty": "hard",
"prompt": "The following Python function is designed to merge an array of intervals and return a new array of sorted, non-overlapping merged intervals. However, it contains exactly one logical bug where it fails to handle overlapping boundary edges properly. Identify the bug and provide the corrected code.\n\npython\ndef merge_intervals(intervals):\n    if not intervals:\n        return\n    intervals.sort(key=lambda x: x)\n    merged = [intervals]\n    for current in intervals[1:]:\n        prev = merged[-1]\n        if current < prev  :\n            prev   = max(prev  , current  )\n        else:\n            merged.append(current)\n    return merged\n",
"gold_answer": "The bug is in the overlap comparison condition current < prev  . By using a strict less-than comparison (<), the function fails to merge intervals that share adjacent boundaries (e.g., [1, 2] and [2, 3] are not merged, despite touch-points being considered overlapping in standard interval merging). It must be a less-than-or-equal comparison (<=). Corrected code:\n\npython\ndef merge_intervals(intervals):\n    if not intervals:\n        return\n    intervals.sort(key=lambda x: x)\n    merged = [list(intervals)]\n    for current in intervals[1:]:\n        prev = merged[-1]\n        if current <= prev  :\n            prev   = max(prev  , current  )\n        else:\n            merged.append(list(current))\n    return merged\n",
"acceptance_criteria": "The response must identify that the strict inequality < fails to merge adjacent intervals sharing a boundary and must be corrected to <=."
},
{
"task_id": "logical_reasoning_easy_1",
"category": "logical_reasoning",
"difficulty": "easy",
"prompt": "Four books (A, B, C, D) are arranged on a shelf from left to right in positions 1, 2, 3, and 4. Determine their positions based on these clues:\n1) Book C is to the left of Book A but not necessarily adjacent.\n2) Book B is in position 3.\n3) Book D is not next to Book B.",
"gold_answer": "The positions of the books from left to right (1 to 4) are:\n1: Book D\n2: Book C\n3: Book B\n4: Book A\n\nJustification:\n1. Clue 2 states Book B is in position 3.\n2. Clue 3 states Book D is not next to Book B. Since Book B is in position 3, the adjacent positions are 2 and 4. Therefore, Book D cannot be in position 2 or 4. Book D must be in position 1.\n3. This leaves positions 2 and 4 for Books A and C. Clue 1 states Book C is to the left of Book A. Thus, Book C must be in position 2 and Book A in position 4.",
"acceptance_criteria": "The response must identify the correct order: 1: D, 2: C, 3: B, 4: A, with a consistent step-by-step logical justification."
},
{
"task_id": "logical_reasoning_med_1",
"category": "logical_reasoning",
"difficulty": "medium",
"prompt": "Five runner friends (Alex, Blake, Casey, Drew, and Taylor) finished a marathon in different positions (1st through 5th). Determine their exact finishing order based on these four constraints:\n1) Alex finished somewhere before Casey but after Drew.\n2) Blake finished immediately after Taylor.\n3) Casey did not finish last.\n4) Blake did not finish 1st or 2nd.",
"gold_answer": "The finishing order from 1st to 5th is:\n1st: Drew\n2nd: Alex\n3rd: Casey\n4th: Taylor\n5th: Blake\n\nJustification:\n- From Constraint 1, Drew finished before Alex, and Alex finished before Casey. This gives the order: Drew -> Alex -> Casey.\n- From Constraint 2, Blake finished immediately after Taylor, forming the adjacent block.\n- From Constraint 4, Blake did not finish 1st or 2nd. Thus, the block can only occupy positions (2nd, 3rd), (3rd, 4th), or (4th, 5th).\n- If is in positions (4th, 5th), then Drew, Alex, and Casey must occupy positions 1st, 2nd, and 3rd respectively. This satisfies all constraints: Drew is 1st, Alex is 2nd, Casey is 3rd (not last), Taylor is 4th, Blake is 5th (not 1st or 2nd).\n- Any other configuration forces Casey into the 5th (last) position to satisfy Drew -> Alex -> Casey, which violates Constraint 3.",
"acceptance_criteria": "The response must identify the exact finishing order: 1st: Drew, 2nd: Alex, 3rd: Casey, 4th: Taylor, 5th: Blake, with logical justification."
},
{
"task_id": "logical_reasoning_med_2",
"category": "logical_reasoning",
"difficulty": "medium",
"prompt": "Four colleagues (Sarah, Mark, Kevin, Jenny) must be scheduled for a single presentation slot each on Monday, Tuesday, Wednesday, and Thursday. Determine the exact schedule based on these constraints:\n1) Sarah's presentation is earlier in the week than Mark's.\n2) Kevin's presentation is on the day immediately after Jenny's.\n3) Jenny's presentation is not on Monday.\n4) Kevin's presentation is not on Wednesday.",
"gold_answer": "The schedule is:\n- Monday: Sarah\n- Tuesday: Mark\n- Wednesday: Jenny\n- Thursday: Kevin\n\nJustification:\n1. Constraint 2 states Kevin presents immediately after Jenny, forming the consecutive block [Jenny, Kevin].\n2. Constraint 3 states Jenny cannot present on Monday. Thus, the possible positions for the block are (Tuesday, Wednesday) or (Wednesday, Thursday).\n3. Constraint 4 states Kevin cannot present on Wednesday. This eliminates the (Tuesday, Wednesday) option. Therefore, the block must be scheduled as Jenny on Wednesday and Kevin on Thursday.\n4. This leaves Monday and Tuesday for Sarah and Mark. Constraint 1 states Sarah presents earlier than Mark. Thus, Sarah must be on Monday and Mark on Tuesday.",
"acceptance_criteria": "The response must identify the schedule: Monday: Sarah, Tuesday: Mark, Wednesday: Jenny, Thursday: Kevin, with a step-by-step constraint satisfaction proof."
},
{
"task_id": "logical_reasoning_hard_1",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Five distinct colored boxes (Red, Blue, Green, Yellow, and White) are lined up from left to right in positions 1 to 5. Determine the position of each box based on these five constraints:\n1) The Red box is in the exact middle position.\n2) The Blue box is adjacent to the Red box.\n3) The White box is immediately to the right of the Red box.\n4) There is exactly one box between the Yellow and Red boxes.\n5) The Green box is to the right of the White box.",
"gold_answer": "The positions of the boxes from left to right (1 to 5) are:\n1: Yellow\n2: Blue\n3: Red\n4: White\n5: Green\n\nJustification:\n- Constraint 1: Red is in the middle (position 3).\n- Constraint 3: White is immediately to the right of Red (position 4).\n- Constraint 5: Green is to the right of White. Since White is in position 4, and position 5 is the only slot to its right, Green must be in position 5.\n- Constraint 4: There is exactly one box between Yellow and Red (position 3). Yellow must be in position 1 or 5. Since position 5 is occupied by Green, Yellow must be in position 1.\n- Position 2 is the only remaining vacant slot, which goes to Blue. This satisfies Constraint 2, as Blue (2) is adjacent to Red (3).",
"acceptance_criteria": "The response must identify the unique order of the boxes: 1: Yellow, 2: Blue, 3: Red, 4: White, 5: Green, with a clear step-by-step logical proof."
},
{
"task_id": "code_generation_easy_1",
"category": "code_generation",
"difficulty": "easy",
"prompt": "Write a Python function with the signature is_isogram(s: str) -> bool that determines if a string is an isogram. An isogram is a word with no repeating letters, consecutive or non-consecutive. The function must ignore letter casing.\n\nExamples:\n- is_isogram('Dermatoglyphics') -> True\n- is_isogram('aba') -> False\n- is_isogram('moOse') -> False",
"gold_answer": "def is_isogram(s: str) -> bool:\n    clean_s = s.lower()\n    return len(clean_s) == len(set(clean_s))",
"acceptance_criteria": "The function must correctly return a boolean indicating whether the input string has no repeating letters, ignoring case, matching all examples."
},
{
"task_id": "code_generation_med_1",
"category": "code_generation",
"difficulty": "medium",
"prompt": "Write a Python function with the signature validate_ip(ip: str) -> bool that determines if a given string is a valid IPv4 address. A valid IPv4 address must be in the form 'X.X.X.X' where each X is an integer between 0 and 255 inclusive, with no leading zeros (except for the single digit '0').\n\nExamples:\n- validate_ip('192.168.1.1') -> True\n- validate_ip('192.168.01.1') -> False\n- validate_ip('256.100.50.25') -> False\n- validate_ip('192.168.1') -> False",
"gold_answer": "def validate_ip(ip: str) -> bool:\n    parts = ip.split('.')\n    if len(parts)!= 4:\n        return False\n    for part in parts:\n        if not part.isdigit():\n            return False\n        if len(part) > 1 and part == '0':\n            return False\n        val = int(part)\n        if val < 0 or val > 255:\n            return False\n    return True",
"acceptance_criteria": "The function must split the IP address by '.', verify exactly 4 parts, ensure each part consists of digits with no leading zeros (unless it's '0'), and ensure the integer value is between 0 and 255 inclusive."
},
{
"task_id": "code_generation_med_2",
"category": "code_generation",
"difficulty": "medium",
"prompt": "Write a JavaScript function with the signature findUniqueEmailAddresses(emails) that filters a list of email strings and returns the number of unique email addresses. Each email contains a local name and a domain name separated by '@'. In addition to lowercase letters, the local name may contain '.' or '+'. If you add periods '.' between some characters in the local name portion of an email address, mail sent there will be forwarded to the same address without dots in the local name. If you add a plus '+' in the local name, everything after the first plus sign will be ignored. These rules do not apply to the domain name.\n\nExamples:\n- findUniqueEmailAddresses(['test.email+alex@leetcode.com', 'test.e.mail+bob.cathy@leetcode.com', 'testemail+david@lee.tcode.com']) -> 2\n- findUniqueEmailAddresses(['a@b.com', 'c@d.com']) -> 2",
"gold_answer": "function findUniqueEmailAddresses(emails) {\n    const uniqueEmails = new Set();\n    for (const email of emails) {\n        const parts = email.split('@');\n        if (parts.length!== 2) continue;\n        let local = parts;\n        const domain = parts;\n        const plusIndex = local.indexOf('+');\n        if (plusIndex!== -1) {\n            local = local.substring(0, plusIndex);\n        }\n        local = local.replace(/\./g, '');\n        uniqueEmails.add(${local}@${domain});\n    }\n    return uniqueEmails.size;\n}",
"acceptance_criteria": "The function must correctly parse each email, apply the local-name rules (ignoring characters after '+' and stripping periods), and return the correct count of unique email addresses."
},
{
"task_id": "code_generation_hard_1",
"category": "code_generation",
"difficulty": "hard",
"prompt": "Write a Python function with the signature longest_consecutive_sequence(nums: list[int]) -> int that finds the length of the longest consecutive elements sequence in an unsorted list of integers. Your algorithm must run in O(n) time complexity.\n\nExamples:\n- longest_consecutive_sequence() -> 4\n- longest_consecutive_sequence() -> 9",
"gold_answer": "def longest_consecutive_sequence(nums: list[int]) -> int:\n    num_set = set(nums)\n    longest_streak = 0\n    for num in num_set:\n        if num - 1 not in num_set:\n            current_num = num\n            current_streak = 1\n            while current_num + 1 in num_set:\n                current_num += 1\n                current_streak += 1\n            longest_streak = max(longest_streak, current_streak)\n    return longest_streak",
"acceptance_criteria": "The function must correctly compute the length of the longest consecutive sequence in O(n) time complexity using a set to perform O(1) lookups."
}
]