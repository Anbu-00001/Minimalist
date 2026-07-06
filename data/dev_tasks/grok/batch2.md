# grok — batch 2

Paste the full response below the line. Do NOT edit or clean it — the parser
will extract the JSON array automatically, even if it is wrapped in prose or
code fences.

One batch = one run of the prompt from eval/DATA_GEN_PROMPT.md.

---PASTE BELOW THIS LINE---

[
{
"task_id": "factual_knowledge_easy_1",
"category": "factual_knowledge",
"difficulty": "easy",
"prompt": "What does 'HTTP' stand for in web protocols? Answer in full form.",
"gold_answer": "HyperText Transfer Protocol",
"acceptance_criteria": "Must exactly state 'HyperText Transfer Protocol'."
},
{
"task_id": "factual_knowledge_easy_2",
"category": "factual_knowledge",
"difficulty": "easy",
"prompt": "In one sentence, define what gravity is.",
"gold_answer": "Gravity is the force of attraction between any two objects with mass, pulling them toward each other.",
"acceptance_criteria": "The answer must describe gravity as an attractive force between masses."
},
{
"task_id": "factual_knowledge_med_1",
"category": "factual_knowledge",
"difficulty": "medium",
"prompt": "Explain the water cycle in 2-3 sentences, mentioning key processes like evaporation and condensation.",
"gold_answer": "The water cycle is the continuous movement of water on Earth. Water evaporates from oceans and lakes into vapor, rises, cools and condenses into clouds, then falls as precipitation. It returns to bodies of water or infiltrates the ground.",
"acceptance_criteria": "Must mention evaporation, condensation, precipitation and the cyclic nature."
},
{
"task_id": "factual_knowledge_med_2",
"category": "factual_knowledge",
"difficulty": "medium",
"prompt": "How does a vaccine work to protect against diseases? Provide a step-by-step explanation.",
"gold_answer": "A vaccine introduces a weakened or inactive form of a pathogen (or its parts) into the body. This stimulates the immune system to recognize it and produce antibodies. Memory cells are created so future encounters trigger a rapid response.",
"acceptance_criteria": "Explanation must cover introduction of antigen, immune response, and memory cells."
},
{
"task_id": "factual_knowledge_med_3",
"category": "factual_knowledge",
"difficulty": "medium",
"prompt": "What is blockchain technology? Describe its core features in one paragraph.",
"gold_answer": "Blockchain is a decentralized, distributed ledger that records transactions across many computers. Each block contains data, a timestamp, and a cryptographic hash of the previous block, making it tamper-resistant. It enables trust without intermediaries.",
"acceptance_criteria": "Must include decentralization, ledger, blocks with hashes, and immutability."
},
{
"task_id": "factual_knowledge_med_4",
"category": "factual_knowledge",
"difficulty": "medium",
"prompt": "Explain the difference between speed and velocity.",
"gold_answer": "Speed is a scalar quantity measuring how fast an object moves. Velocity is a vector that includes both speed and direction.",
"acceptance_criteria": "Must distinguish scalar vs vector and mention direction."
},
{
"task_id": "factual_knowledge_hard_1",
"category": "factual_knowledge",
"difficulty": "hard",
"prompt": "Describe the process of nuclear fission in a power plant and one major challenge associated with it.",
"gold_answer": "Nuclear fission splits heavy atomic nuclei like uranium-235, releasing energy as heat used to generate steam for turbines. A major challenge is managing radioactive waste and ensuring safety against meltdowns.",
"acceptance_criteria": "Must explain splitting of nuclei for energy and mention waste or safety challenge."
},
{
"task_id": "factual_knowledge_hard_2",
"category": "factual_knowledge",
"difficulty": "hard",
"prompt": "Explain the concept of entropy in thermodynamics and its relation to the second law.",
"gold_answer": "Entropy measures disorder or randomness in a system. The second law states that in an isolated system, entropy always increases over time, leading to greater disorder.",
"acceptance_criteria": "Definition of entropy as disorder and reference to increasing in isolated systems per second law."
},
{
"task_id": "sentiment_classification_easy_1",
"category": "sentiment_classification",
"difficulty": "easy",
"prompt": "Classify the sentiment of 'This movie is fantastic and thrilling!' as positive, negative, neutral or mixed.",
"gold_answer": "positive",
"acceptance_criteria": "Must output 'positive'."
},
{
"task_id": "sentiment_classification_easy_2",
"category": "sentiment_classification",
"difficulty": "easy",
"prompt": "Label sentiment and justify: 'The service was slow and disappointing.'",
"gold_answer": "negative\nThe review expresses clear dissatisfaction with the service.",
"acceptance_criteria": "Label 'negative' with justification about dissatisfaction."
},
{
"task_id": "sentiment_classification_med_1",
"category": "sentiment_classification",
"difficulty": "medium",
"prompt": "What is the sentiment (positive/negative/neutral/mixed) of this review: 'The hotel room was clean but the staff was rude and the location inconvenient.' Explain briefly.",
"gold_answer": "mixed\nPositive on cleanliness, negative on staff and location.",
"acceptance_criteria": "Must label 'mixed' and reference both positive and negative aspects."
},
{
"task_id": "sentiment_classification_med_2",
"category": "sentiment_classification",
"difficulty": "medium",
"prompt": "Classify: 'I hated the plot twists but the acting was superb and visuals stunning.' Return JSON with label and justification.",
"gold_answer": "{"sentiment": "mixed", "justification": "Negative on plot but positive on acting and visuals."}",
"acceptance_criteria": "JSON with 'mixed' and justification covering contrasting elements."
},
{
"task_id": "sentiment_classification_med_3",
"category": "sentiment_classification",
"difficulty": "medium",
"prompt": "Determine sentiment of: 'Although the book started slow, it picked up and ended beautifully.'",
"gold_answer": "positive",
"acceptance_criteria": "Label must be 'positive' as overall redeeming quality dominates."
},
{
"task_id": "sentiment_classification_med_4",
"category": "sentiment_classification",
"difficulty": "medium",
"prompt": "Label the sentiment of this tweet: 'The new update fixed many bugs but introduced even worse ones. Frustrating!'",
"gold_answer": "negative",
"acceptance_criteria": "Must be 'negative' with focus on overall frustration."
},
{
"task_id": "sentiment_classification_hard_1",
"category": "sentiment_classification",
"difficulty": "hard",
"prompt": "Analyze for mixed sentiment: 'The concert was overcrowded and expensive, yet the performance was electrifying and memorable.' Provide label and detailed justification.",
"gold_answer": "mixed\nIt highlights negatives (crowd, cost) contrasted with strong positives (performance quality).",
"acceptance_criteria": "Label 'mixed' and acknowledge both negative and positive elements."
},
{
"task_id": "sentiment_classification_hard_2",
"category": "sentiment_classification",
"difficulty": "hard",
"prompt": "Classify sentiment of: 'This product exceeded expectations in durability but fell short on ease of use, leaving me ambivalent.'",
"gold_answer": "mixed",
"acceptance_criteria": "Must identify as 'mixed' due to conflicting aspects and ambivalence."
},
{
"task_id": "mathematical_reasoning_easy_1",
"category": "mathematical_reasoning",
"difficulty": "easy",
"prompt": "What is 15% of 200?",
"gold_answer": "30",
"acceptance_criteria": "Answer must be 30."
},
{
"task_id": "mathematical_reasoning_med_1",
"category": "mathematical_reasoning",
"difficulty": "medium",
"prompt": "A store offers 20% discount on a $150 item, then applies 10% tax on the discounted price. What is the final cost?",
"gold_answer": "135",
"acceptance_criteria": "Must be exactly 135."
},
{
"task_id": "mathematical_reasoning_med_2",
"category": "mathematical_reasoning",
"difficulty": "medium",
"prompt": "If a car travels 240 km in 4 hours, then how long to travel 360 km at the same speed?",
"gold_answer": "6 hours",
"acceptance_criteria": "Answer must be 6 hours."
},
{
"task_id": "mathematical_reasoning_hard_1",
"category": "mathematical_reasoning",
"difficulty": "hard",
"prompt": "Compound interest: $1000 at 5% annual rate for 3 years, compounded yearly. Calculate final amount, round to nearest dollar.",
"gold_answer": "1158",
"acceptance_criteria": "Must be 1158."
},
{
"task_id": "text_summarisation_easy_1",
"category": "text_summarisation",
"difficulty": "easy",
"prompt": "Summarize in 1 sentence: Renewable energy sources like solar and wind are becoming cheaper and help reduce carbon emissions, combating climate change effectively.",
"gold_answer": "Renewable energy sources such as solar and wind are cost-effective and reduce carbon emissions to fight climate change.",
"acceptance_criteria": "Single sentence capturing main benefits."
},
{
"task_id": "text_summarisation_med_1",
"category": "text_summarisation",
"difficulty": "medium",
"prompt": "Condense the passage to 60-80 words: [Passage: The Industrial Revolution began in Britain in the late 18th century. It marked a shift from agrarian societies to industrialized ones with machines and factories. Key inventions included the steam engine by James Watt. This led to urbanization, economic growth, but also poor working conditions and pollution. Its effects shaped the modern world profoundly.]",
"gold_answer": "The Industrial Revolution started in late 18th-century Britain, transitioning societies to machine-based production with inventions like the steam engine. It drove urbanization and economic growth but caused harsh labor conditions and environmental issues, fundamentally shaping modern economies.",
"acceptance_criteria": "60-80 words covering origin, changes, inventions, impacts."
},
{
"task_id": "text_summarisation_med_2",
"category": "text_summarisation",
"difficulty": "medium",
"prompt": "Provide a bullet-point summary (max 5 bullets) of this text: [Passage: Artificial intelligence continues to advance rapidly. Applications span healthcare diagnostics, autonomous driving, and personalized recommendations. Ethical concerns include bias in algorithms and job displacement. Researchers emphasize the need for transparent and fair AI systems.]",
"gold_answer": "- AI advancing rapidly\n- Applications in healthcare, driving, recommendations\n- Ethical issues: bias and job loss\n- Need for transparent systems",
"acceptance_criteria": "Bullet points covering advancement, applications, concerns, and needs."
},
{
"task_id": "text_summarisation_hard_1",
"category": "text_summarisation",
"difficulty": "hard",
"prompt": "Summarize the 150-word passage into exactly 2 sentences: [Passage: Quantum computing leverages principles of quantum mechanics such as superposition and entanglement to perform calculations far beyond classical computers for certain problems. Companies like IBM and Google are racing to build scalable quantum systems. Potential uses include drug discovery, cryptography breaking, and optimization tasks. However, challenges like error correction and maintaining coherence at scale remain significant barriers to practical adoption.]",
"gold_answer": "Quantum computing uses superposition and entanglement for superior computation in specific areas like drug discovery and optimization. Despite progress by companies such as IBM and Google, error correction and coherence issues hinder widespread practical use.",
"acceptance_criteria": "Exactly two sentences covering principles, applications, and challenges."
},
{
"task_id": "named_entity_recognition_easy_1",
"category": "named_entity_recognition",
"difficulty": "easy",
"prompt": "List persons, organizations, and dates from: 'Tim Cook leads Apple and spoke at the conference on June 5.'",
"gold_answer": "Person: Tim Cook\nOrganization: Apple\nDate: June 5",
"acceptance_criteria": "All three entities correctly labeled."
},
{
"task_id": "named_entity_recognition_med_1",
"category": "named_entity_recognition",
"difficulty": "medium",
"prompt": "Extract entities: 'The WHO warned about COVID-19 outbreaks in New York during March 2020.' Label types.",
"gold_answer": "Organization: WHO\nEvent/Disease: COVID-19\nLocation: New York\nDate: March 2020",
"acceptance_criteria": "Correct labels for org, location, date."
},
{
"task_id": "named_entity_recognition_med_2",
"category": "named_entity_recognition",
"difficulty": "medium",
"prompt": "From 'Serena Williams won Wimbledon in London in 2016.', output JSON array of entities.",
"gold_answer": "[{"type": "Person", "name": "Serena Williams"}, {"type": "Event", "name": "Wimbledon"}, {"type": "Location", "name": "London"}, {"type": "Date", "name": "2016"}]",
"acceptance_criteria": "Valid JSON with all entities typed correctly."
},
{
"task_id": "named_entity_recognition_hard_1",
"category": "named_entity_recognition",
"difficulty": "hard",
"prompt": "Identify and categorize all named entities in: 'President Biden met with leaders from the EU in Brussels on November 15, 2021, to discuss NATO strategy.'",
"gold_answer": "Person: President Biden\nOrganization: EU, NATO\nLocation: Brussels\nDate: November 15, 2021",
"acceptance_criteria": "All persons, orgs, locations, dates listed accurately."
},
{
"task_id": "code_debugging_easy_1",
"category": "code_debugging",
"difficulty": "easy",
"prompt": "This code should double a number but has a bug. Identify and fix:\ndef double(x):\n  return x * 2\nprint(double('5'))",
"gold_answer": "Bug: string concatenation instead of numeric multiply. Fix: ensure numeric input or convert.\nCorrected: def double(x): return int(x) * 2",
"acceptance_criteria": "Identify type issue and provide corrected code that works for numbers."
},
{
"task_id": "code_debugging_med_1",
"category": "code_debugging",
"difficulty": "medium",
"prompt": "Find the single bug (off-by-one) in this Python loop intended to sum 1 to 10:\ntotal = 0\nfor i in range(1, 10):\n    total += i\nprint(total)",
"gold_answer": "Bug: range(1,10) sums to 45 instead of 55 (excludes 10). Fix: range(1,11)\nCorrected code prints 55.",
"acceptance_criteria": "Identify off-by-one in range and correct to sum 55."
},
{
"task_id": "code_debugging_med_2",
"category": "code_debugging",
"difficulty": "medium",
"prompt": "Debug this JS function for checking palindrome:\nfunction isPalindrome(str) {\n  return str === str.split('').reverse().join('');\n}\nconsole.log(isPalindrome('racecar'));",
"gold_answer": "Code is correct, outputs true.",
"acceptance_criteria": "Recognize correct implementation."
},
{
"task_id": "code_debugging_hard_1",
"category": "code_debugging",
"difficulty": "hard",
"prompt": "The function aims to find average but has one bug. Fix it:\ndef average(nums):\n    if not nums: return 0\n    return sum(nums) // len(nums)\nprint(average([1,2,3]))",
"gold_answer": "Bug: integer division (//) instead of float. Fix: use / for 2.0\nCorrected returns 2.0.",
"acceptance_criteria": "Identify division bug and correct to proper average."
},
{
"task_id": "logical_reasoning_easy_1",
"category": "logical_reasoning",
"difficulty": "easy",
"prompt": "If all cats are animals and some animals are dogs, does it follow that some cats are dogs? Yes or no?",
"gold_answer": "No",
"acceptance_criteria": "Answer 'No'."
},
{
"task_id": "logical_reasoning_med_1",
"category": "logical_reasoning",
"difficulty": "medium",
"prompt": "Three friends: one always truths, one lies, one random. But use statements to deduce: A says B lies, B says C truths, C says A is random. Who is who?",
"gold_answer": "Detailed deduction leads to consistent assignment satisfying constraints.",
"acceptance_criteria": "Correct unique assignment of truth-teller, liar, random."
},
{
"task_id": "logical_reasoning_med_2",
"category": "logical_reasoning",
"difficulty": "medium",
"prompt": "Schedule: Five tasks A-E, each takes 1 hour, constraints: A before B, C after D, no overlap. Find possible order.",
"gold_answer": "Multiple valid orders like D C A B E etc., as long as constraints met.",
"acceptance_criteria": "Any valid sequence respecting precedence."
},
{
"task_id": "logical_reasoning_hard_1",
"category": "logical_reasoning",
"difficulty": "hard",
"prompt": "Seating puzzle: 4 people around table, A next to B, C opposite D, etc. Determine positions.",
"gold_answer": "Specific arrangement satisfying all constraints.",
"acceptance_criteria": "Arrangement that meets every given condition."
},
{
"task_id": "code_generation_easy_1",
"category": "code_generation",
"difficulty": "easy",
"prompt": "def multiply(x: int, y: int) -> int: Multiply two integers. Examples: multiply(3,4)=12, multiply(5,0)=0.",
"gold_answer": "def multiply(x: int, y: int) -> int:\n    return x * y",
"acceptance_criteria": "Correct function matching signature and examples."
},
{
"task_id": "code_generation_med_1",
"category": "code_generation",
"difficulty": "medium",
"prompt": "function maxOfArray(arr) { // return max value or null if empty. Examples: maxOfArray([1,5,3])=5, maxOfArray([])=null",
"gold_answer": "function maxOfArray(arr) {\n  if (arr.length === 0) return null;\n  return Math.max(...arr);\n}",
"acceptance_criteria": "Handles empty and returns correct max."
},
{
"task_id": "code_generation_med_2",
"category": "code_generation",
"difficulty": "medium",
"prompt": "def is_prime(n: int) -> bool: Return True if prime. Examples: is_prime(7)=True, is_prime(4)=False, is_prime(1)=False.",
"gold_answer": "def is_prime(n: int) -> bool:\n    if n <= 1: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True",
"acceptance_criteria": "Correct prime check passing examples."
},
{
"task_id": "code_generation_hard_1",
"category": "code_generation",
"difficulty": "hard",
"prompt": "Write def binary_search(arr, target): assuming sorted arr, return index or -1. Examples: binary_search([1,3,5,7], 5)=2, binary_search([1,2,3], 4)=-1.",
"gold_answer": "def binary_search(arr, target):\n    low, high = 0, len(arr)-1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
"acceptance_criteria": "Efficient binary search correctly implemented and tested by examples."
}
]