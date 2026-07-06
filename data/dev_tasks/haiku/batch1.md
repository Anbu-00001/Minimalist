# haiku — batch 1

---PASTE BELOW THIS LINE---

[
  {
    "task_id": "text_summarisation_easy_1",
    "category": "text_summarisation",
    "difficulty": "easy",
    "prompt": "Summarize the following passage in exactly one sentence:\n\nPhotosynthesis is the process by which plants convert sunlight into chemical energy stored in glucose molecules. This process occurs primarily in the leaves, where chlorophyll absorbs light energy. Plants use this energy to combine carbon dioxide from the air with water from the soil, producing glucose and releasing oxygen as a byproduct.",
    "gold_answer": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
    "acceptance_criteria": "The summary must be exactly one sentence and capture the main inputs (sunlight, water, CO2) and outputs (glucose, oxygen) of photosynthesis."
  },
  {
    "task_id": "text_summarisation_easy_2",
    "category": "text_summarisation",
    "difficulty": "easy",
    "prompt": "Summarize the following passage in at most 20 words:\n\nThe Great Wall of China is a massive fortification system built over centuries to protect Chinese states and empires from invasions by nomadic groups from the north. Construction began as early as the 7th century BC and continued until the 17th century AD.",
    "gold_answer": "The Great Wall of China is a multi-century defensive structure built to protect against northern invasions.",
    "acceptance_criteria": "The summary must be 20 words or fewer and must identify the wall's purpose (defense) and time scale (multi-century)."
  },
  {
    "task_id": "text_summarisation_easy_3",
    "category": "text_summarisation",
    "difficulty": "easy",
    "prompt": "Summarize the following passage in at most three bullet points:\n\nElectric vehicles (EVs) are cars powered by rechargeable battery packs instead of gasoline engines. They produce zero direct emissions, reducing air pollution in urban areas. EVs have lower operating costs because electricity is cheaper than gasoline, and they require less maintenance since they have fewer moving parts. The main drawback is that charging infrastructure is still developing in many regions.",
    "gold_answer": "• EVs are powered by rechargeable batteries with zero direct emissions.\n• Lower operating costs and reduced maintenance compared to gasoline cars.\n• Charging infrastructure is still developing in many regions.",
    "acceptance_criteria": "Must contain exactly three bullet points covering emissions, cost/maintenance benefits, and infrastructure challenges."
  },
  {
    "task_id": "text_summarisation_easy_4",
    "category": "text_summarisation",
    "difficulty": "easy",
    "prompt": "Summarize the following passage in one sentence, emphasizing the main discovery:\n\nIn 2020, scientists discovered a new species of deep-sea octopus near hydrothermal vents in the Pacific Ocean. The octopus, named Grimpoteuthis imperator, has a unique translucent body and survives in extreme heat and pressure. Its discovery expands our understanding of life in Earth's most extreme environments.",
    "gold_answer": "Scientists discovered a new deep-sea octopus species near hydrothermal vents, expanding knowledge of extreme-environment life.",
    "acceptance_criteria": "One sentence that mentions the discovery location (hydrothermal vents), the organism type (octopus), and its significance (expands understanding)."
  },
  {
    "task_id": "text_summarisation_easy_5",
    "category": "text_summarisation",
    "difficulty": "easy",
    "prompt": "Condense the following passage into exactly two sentences:\n\nCoffee is the second-most traded commodity globally, after crude oil. It is grown in tropical regions called the 'bean belt' and exported to consuming countries worldwide. The coffee industry supports millions of farmers and provides livelihoods for entire communities.",
    "gold_answer": "Coffee is the world's second-most traded commodity, grown in tropical regions globally. The industry supports millions of farmers and their communities.",
    "acceptance_criteria": "Exactly two sentences; must mention coffee's global trade ranking and its impact on farmers/communities."
  },
  {
    "task_id": "text_summarisation_medium_1",
    "category": "text_summarisation",
    "difficulty": "medium",
    "prompt": "Summarize the following passage in at most 50 words, preserving key details about both benefits and limitations:\n\nArtificial intelligence has revolutionized healthcare by improving diagnostic accuracy and accelerating drug discovery. Machine learning algorithms can analyze medical imaging faster and more accurately than human radiologists in many cases. However, AI systems require massive amounts of training data, and privacy concerns about patient information remain significant barriers to broader adoption. Additionally, the 'black box' nature of some AI models makes it difficult for doctors to understand how diagnoses are reached.",
    "gold_answer": "AI improves healthcare diagnostics and drug discovery, enabling faster, more accurate analysis of medical imaging. However, challenges include data privacy, the need for large training datasets, and the opacity of AI decision-making.",
    "acceptance_criteria": "50 words or fewer; must include benefits (diagnostic accuracy, drug discovery) and at least two limitations (privacy, transparency, or data requirements)."
  },
  {
    "task_id": "text_summarisation_medium_2",
    "category": "text_summarisation",
    "difficulty": "medium",
    "prompt": "Summarize the following passage in exactly three sentences:\n\nThe Panama Canal is one of the most important waterways in the world, connecting the Atlantic and Pacific Oceans. Built between 1904 and 1914, it eliminated the need for ships to navigate around South America, reducing travel time and costs significantly. Today, approximately 6% of global maritime trade passes through the canal. However, the canal faces challenges from climate change, with rising sea levels and changing rainfall patterns affecting water levels and operational capacity. Despite these challenges, it remains critical to global commerce.",
    "gold_answer": "The Panama Canal connects the Atlantic and Pacific Oceans, eliminating the need to navigate around South America since 1914. Approximately 6% of global maritime trade passes through the canal, making it critical to commerce. Climate change threatens its operations through rising sea levels and altered rainfall patterns.",
    "acceptance_criteria": "Exactly three sentences covering: construction/purpose, importance to trade, and current challenges from climate change."
  },
  {
    "task_id": "text_summarisation_medium_3",
    "category": "text_summarisation",
    "difficulty": "medium",
    "prompt": "Summarize the following passage in at most 60 words, focusing on the main innovation and its impact:\n\nMRNA vaccines represent a revolutionary breakthrough in immunology. Unlike traditional vaccines, which use weakened viruses or viral proteins, mRNA vaccines provide the body's cells with instructions to produce the virus's spike protein themselves. This approach is faster to develop, more scalable, and more flexible than conventional methods. During the COVID-19 pandemic, mRNA vaccines were developed and deployed in less than a year, demonstrating their potential. The technology is now being explored for treating cancers and other diseases.",
    "gold_answer": "mRNA vaccines instruct cells to produce viral proteins, revolutionizing vaccine development. They are faster and more flexible than traditional vaccines, as demonstrated by COVID-19 vaccine development in under a year. The technology is expanding to treat cancers and other diseases.",
    "acceptance_criteria": "At most 60 words; must explain how mRNA vaccines work, mention their speed advantage, and note their broader applications."
  },
  {
    "task_id": "text_summarisation_medium_4",
    "category": "text_summarisation",
    "difficulty": "medium",
    "prompt": "Summarize the following passage in one paragraph of at most 75 words:\n\nBiodiversity loss is accelerating at an alarming rate due to habitat destruction, climate change, pollution, and overhunting. Scientists estimate that species are going extinct 100 to 1,000 times faster than the natural background extinction rate. The loss of biodiversity has serious consequences, including disrupted food chains, reduced crop pollination, and compromised ecosystem stability. Protecting biodiversity requires international cooperation, habitat conservation, and shifts in human consumption patterns. Many initiatives aim to preserve endangered species and restore degraded ecosystems.",
    "gold_answer": "Biodiversity is declining rapidly due to habitat destruction, climate change, pollution, and overhunting, with extinction rates 100–1,000 times faster than natural rates. This threatens food chains, pollination, and ecosystem stability. Solutions require international cooperation, habitat conservation, and changes in consumption patterns.",
    "acceptance_criteria": "At most 75 words; must cover causes, the acceleration of extinction, consequences, and potential solutions."
  },
  {
    "task_id": "text_summarisation_hard_1",
    "category": "text_summarisation",
    "difficulty": "hard",
    "prompt": "Summarize the following complex passage in exactly 40 words, balancing multiple competing perspectives:\n\nGenetic engineering in agriculture offers significant potential to increase crop yields, reduce pesticide use, and create drought-resistant plants. Proponents argue these benefits are essential to feeding a growing global population. Critics, however, express concerns about long-term environmental effects, unintended consequences in ecosystems, and corporate control of the food supply. Regulatory frameworks vary widely by country, reflecting differing cultural and scientific assessments of risk. The technology continues to evolve as research progresses.",
    "gold_answer": "Genetic engineering in agriculture promises higher yields, reduced pesticides, and drought resistance, but critics worry about ecosystem effects and corporate control. Diverse regulations reflect differing risk assessments.",
    "acceptance_criteria": "Exactly 40 words; must represent both benefits (yields, pesticides, drought resistance) and concerns (ecosystem, corporate control), plus mention regulatory variation."
  },
  {
    "task_id": "text_summarisation_hard_2",
    "category": "text_summarisation",
    "difficulty": "hard",
    "prompt": "Summarize the following passage in one to two sentences, capturing the central argument and its nuance:\n\nThe rise of social media has transformed communication and democratized information sharing, allowing marginalized voices to reach global audiences. However, the same platforms have enabled rapid spread of misinformation, created filter bubbles that reinforce existing beliefs, and contributed to increased polarization. While social media has connected people across boundaries, it has also fragmented shared reality. Some researchers argue these harms outweigh the benefits, while others contend that the technology itself is neutral and blame poor governance and algorithmic design. Striking a balance between enabling free expression and reducing harm remains one of the defining challenges of our time.",
    "gold_answer": "Social media has democratized communication but enabled misinformation and polarization, creating competing assessments of whether harms outweigh benefits. Governance and design choices, rather than the technology itself, will determine its ultimate impact.",
    "acceptance_criteria": "One to two sentences capturing both positive (democratization) and negative (misinformation, polarization) effects, plus the key debate about causation (technology vs. governance)."
  },
  {
    "task_id": "text_summarisation_hard_3",
    "category": "text_summarisation",
    "difficulty": "hard",
    "prompt": "Summarize the following interdisciplinary passage in at most 55 words, preserving the key insight about interconnection:\n\nClimate change is fundamentally altering global water cycles, with profound implications for agriculture, urban water supply, and geopolitical stability. Rising temperatures increase evaporation from oceans and soil, intensifying droughts in some regions while increasing precipitation in others. Glaciers and snowpack, which serve as natural water storage, are melting faster, disrupting seasonal water availability. These changes threaten food security, trigger mass migration, and increase competition for freshwater resources. Water scarcity and abundance are becoming weaponized in conflicts.",
    "gold_answer": "Climate change alters water cycles, intensifying droughts in some regions and floods in others, while melting glaciers disrupt water availability. These changes threaten food security, trigger migration, and fuel resource conflicts.",
    "acceptance_criteria": "At most 55 words; must convey the interconnection between climate, water, and human consequences (food, migration, conflict)."
  },
  {
    "task_id": "factual_knowledge_easy_1",
    "category": "factual_knowledge",
    "difficulty": "easy",
    "prompt": "What is the capital of Japan? Provide a one-word answer.",
    "gold_answer": "Tokyo",
    "acceptance_criteria": "The answer must be the single word 'Tokyo'."
  },
  {
    "task_id": "factual_knowledge_easy_2",
    "category": "factual_knowledge",
    "difficulty": "easy",
    "prompt": "Define photosynthesis in one sentence.",
    "gold_answer": "Photosynthesis is the process by which plants convert sunlight, water, and carbon dioxide into glucose and oxygen.",
    "acceptance_criteria": "The definition must be one sentence and identify the inputs (sunlight, water, CO2) and outputs (glucose, oxygen)."
  },
  {
    "task_id": "factual_knowledge_easy_3",
    "category": "factual_knowledge",
    "difficulty": "easy",
    "prompt": "In what year did the Titanic sink? Provide only the year as a four-digit number.",
    "gold_answer": "1912",
    "acceptance_criteria": "The answer must be the four-digit year '1912'."
  },
  {
    "task_id": "factual_knowledge_easy_4",
    "category": "factual_knowledge",
    "difficulty": "easy",
    "prompt": "Who was the first President of the United States?",
    "gold_answer": "George Washington",
    "acceptance_criteria": "The answer must name George Washington, the first U.S. President."
  },
  {
    "task_id": "factual_knowledge_medium_1",
    "category": "factual_knowledge",
    "difficulty": "medium",
    "prompt": "Explain the greenhouse effect in two to three sentences.",
    "gold_answer": "The greenhouse effect is the process by which certain gases in Earth's atmosphere trap heat from the sun. These gases, including carbon dioxide, methane, and nitrous oxide, absorb infrared radiation that would otherwise escape to space. This trapping of heat causes the planet's average temperature to rise, leading to climate change.",
    "acceptance_criteria": "Two to three sentences explaining which gases trap heat, how they work, and the resulting temperature increase."
  },
  {
    "task_id": "factual_knowledge_medium_2",
    "category": "factual_knowledge",
    "difficulty": "medium",
    "prompt": "List three key inventions of the Industrial Revolution and their approximate dates.",
    "gold_answer": "1. The steam engine (1769, James Watt) — powered factories and transportation. 2. The cotton gin (1793, Eli Whitney) — revolutionized textile production. 3. The locomotive (early 1800s, George Stephenson) — transformed transportation and trade.",
    "acceptance_criteria": "Three inventions with dates (±10 years acceptable) and brief descriptions of their significance."
  },
  {
    "task_id": "factual_knowledge_medium_3",
    "category": "factual_knowledge",
    "difficulty": "medium",
    "prompt": "What are the three branches of the U.S. government, and what is the primary responsibility of each?",
    "gold_answer": "The legislative branch (Congress) makes laws. The executive branch (President) enforces laws. The judicial branch (Supreme Court) interprets laws.",
    "acceptance_criteria": "Must identify all three branches and their primary functions: legislative (lawmaking), executive (enforcement), judicial (interpretation)."
  },
  {
    "task_id": "factual_knowledge_hard_1",
    "category": "factual_knowledge",
    "difficulty": "hard",
    "prompt": "Explain the difference between prokaryotic and eukaryotic cells, including at least three structural differences.",
    "gold_answer": "Prokaryotic cells lack a nucleus and membrane-bound organelles, with DNA in the nucleoid region; they are typically smaller and divide by binary fission. Eukaryotic cells have a nucleus containing DNA, have membrane-bound organelles like mitochondria and endoplasmic reticulum, and are generally larger; they divide by mitosis and meiosis. Prokaryotes include bacteria and archaea, while eukaryotes include animals, plants, fungi, and protists.",
    "acceptance_criteria": "Must cover nucleus presence, organelles, DNA location, size, and division methods; at least three structural differences must be stated clearly."
  },
  {
    "task_id": "factual_knowledge_hard_2",
    "category": "factual_knowledge",
    "difficulty": "hard",
    "prompt": "Describe the causes and consequences of the French Revolution in two to three sentences.",
    "gold_answer": "The French Revolution (1789–1799) was caused by Enlightenment ideas, economic crisis, food shortages, and resentment of absolute monarchy and aristocratic privilege. It resulted in the overthrow of the monarchy, the abolition of feudalism, the Declaration of the Rights of Man, and the rise of nationalist and democratic ideals. Its consequences included the spread of revolutionary ideas across Europe, Napoleon's rise to power, and the reshaping of international politics and social structures.",
    "acceptance_criteria": "Two to three sentences; must identify causes (Enlightenment, economic crisis, monarchy) and at least three major consequences (monarchy overthrow, feudalism abolition, democratic spread)."
  },
  {
    "task_id": "factual_knowledge_hard_3",
    "category": "factual_knowledge",
    "difficulty": "hard",
    "prompt": "Compare and contrast classical mechanics (Newton) and quantum mechanics, addressing at least two key differences.",
    "gold_answer": "Classical mechanics describes macroscopic objects and applies Newton's laws deterministically, predicting exact positions and velocities. Quantum mechanics governs subatomic particles and uses probability distributions, with Heisenberg's uncertainty principle preventing simultaneous exact measurement of position and momentum. Classical mechanics assumes continuous energy and motion, while quantum mechanics shows energy quantization and wave-particle duality. Quantum effects dominate at atomic scales; classical mechanics remains valid for everyday objects.",
    "acceptance_criteria": "Must explain determinism vs. probability, exact prediction vs. uncertainty principle, and energy continuity vs. quantization; at least two key differences stated clearly."
  }
]
