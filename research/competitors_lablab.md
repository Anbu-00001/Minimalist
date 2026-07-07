# Competitor & Peer Intelligence — AMD Developer Hackathon: ACT II (Track 1)

Collection log only. No synthesis/strategy recommendations included. Every bullet has a URL. Verbatim quotes are in quotes; paraphrases are marked (paraphrase). Anything unconfirmed is marked UNVERIFIED.

Method note: lablab.ai blocks direct fetch (Cloudflare); all lablab.ai URLs below were fetched via `https://r.jina.ai/<url>` prefix per the workaround.

---

## 1. Main Act II hackathon page

Source: https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii

- Event dates: "Jul 6 4:00 PM Coordinated Universal Time Hackathon Kick-off" ... "Jul 11 4:00 PM Coordinated Universal Time End of Submissions!" (verbatim from Event Schedule section).
- Track 1 official description (verbatim): "Build an AI agent that completes a fixed set of tasks autonomously by deciding in real time whether to use a **local model** or call a **remote model via Fireworks AI credits**. The goal: pick the cheapest option every time, without falling below the accuracy threshold." Followed by: "💡All models and tokens used locally count as **zero** toward the final score." and "Want to fine-tune your router? Go for it. Prompt-based and fine-tuned approaches are scored exactly the same way: token count and output accuracy."
- Track 1 prizes: 🥇 1st $2,500 / 🥈 2nd $1,500 / 🥉 3rd $1,000 (verbatim structure from page). Plus a separate "Best Use of Gemma via Fireworks — $1,000" prize under Track 1.
- Track 1 is scored via **leaderboard** (quote): "Scoring varies by track. **Tracks 1 and 2** are ranked via **leaderboard**. **Track 3 — Unicorn Track** is evaluated by judges using the criteria below."
- Judging criteria listed for Track 3 (Creativity/Originality, Product/Market Potential, Completeness, Use of AMD Platforms) — not applicable to Track 1 since Track 1 is leaderboard-ranked.
- Page includes a "## Submitted concepts, prototypes and pitches" heading and a "## Teams: AMD Developer Hackathon: ACT II / Check out the roster and find teams to join" heading, but **no actual team/submission entries render in the static/jina fetch** — likely client-side/JS-loaded and not yet populated (consistent with event still in progress as of today, 2026-07-07, deadline 2026-07-11).
- Participant Guide PDF linked (not fetched, Google Drive): https://drive.google.com/file/d/1UGpOZiGGGBqQhGQxX7g19QAA-Dq9hPKk/view?usp=sharing
- `/teams`, `/submissions`, `/projects`, `/leaderboard` sub-paths on the Act II event were tried directly and did NOT return roster/submission data:
  - https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/teams → renders cookie-consent boilerplate only, then a 404 image ("![Image 5: 404]") in the body.
  - https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/submissions → same cookie-consent boilerplate, no content shown.
  - https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/projects → same cookie-consent boilerplate, no content shown.
  - https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/leaderboard → "upstream connect error or disconnect/reset before headers. reset reason: connection termination" (fetch failed).

## 2. Known Act II team subpages (as given + discovered via web search)

All fetched via `https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/<slug>`. As of 2026-07-07, **every team below shows "Team Leader hasn't made a submission yet."** No Track 1 routing/architecture strategy hints were present on any of these pages (they are pre-submission team profile pages only, most containing 1–2 sentence "Team Idea" blurbs and member list, not tech design).

- **/blaze** — "Blaze": Team Idea (verbatim): "a two-person team pairing AI (with product execution (build, demo, polish). Building a narrow, real-world AI solution for AMD ACT II's Unicorn Track." Members: Muzakkir Shaik (mailtomuzzu30101), suhail shaik (shaiksuhail085654863). → Targets Track 3 (Unicorn), not Track 1. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/blaze
- **/armageddon** — "Armageddon": Team Idea (verbatim): "Solo AI developer building innovative, scalable solutions with AMD technologies to solve real-world challenges through intelligent design." Member: Aritra Biswas (Slowcascade). No track specified. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/armageddon
- **/hackq** — "HackQ": Team Idea (verbatim): "Our key strength is coordination and respectfulness." Members: Samarth Waghrulkar (samarth_waghrulkar880), "Unknown Hacker" (sikky60655514). No track specified. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/hackq
- **/indian-ai-warrior** — "Indian ai warrior": Team Idea (verbatim): "Builders of ai agent." Member: "Unknown Hacker" (sonurajgupta200337451). No track specified. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/indian-ai-warrior
- **/spanther** — "Spanther": Team Idea (verbatim): "A founder team working in neurotechnology, building eye-tracking products that train focus and attention." Member: Aziz (aziz106). No track specified — sounds product/Unicorn-oriented, not Track 1. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/spanther
- **/practers** — "Practers": Team Idea (verbatim): "Imagining a world where skills speak louder than resumes." Member: "Unknown Hacker" (fahadkorba50536). No track specified. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/practers
- **/codestorm-hub** — "CodeStorm Hub": Team Idea (verbatim): "Creating unified platform for Pets." Member: Syed Salman Reza (syed-reza98, Software Engineer, github.com/syed-reza98). No track specified. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/codestorm-hub
- **/cipher** — "Cipher": Team Idea (verbatim): "Cracking the code. Building the future." Member: Ghavish Subratty (Ghavish12). No track specified. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/cipher
- **/hivize** — "Hivize": Team Idea (verbatim): "Hivize is an AI-powered platform helping creators and startups generate marketing content, branding, and business assets using modern AI tools." Member: Tharusha Dilhara (Bee49). Product/Unicorn-oriented, not Track 1. URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/hivize
- **/architects-on-giants** — "Architects-on-Giants": Team Idea (verbatim): "Telidhu Broh Nen Em cheyyali" [non-English/garbled]. Member: JOSHI SANKARSH (24955a661964805). No submission yet per this page, despite an "Agent Rerouter" project appearing associated with this team-slug elsewhere (see section 3 — unresolved discrepancy). URL: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/architects-on-giants

## 3. Real Act II submissions found (via "Explore more applications" cross-links and web search)

Source page: https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/himawari/video-captioning-agent

- **Himawari — "Video Captioning Agent"** (Track 2 submission, not Track 1, but same event/same team pool): verbatim: "Video Captioning Agent is our Track 2 submission for the AMD Developer Hackathon. The system takes a video URL as input and produces captions in the four required styles: formal, sarcastic, humorous_tech, and humorous_non_tech. The pipeline downloads the video, uses ffprobe to measure duration, then samples frames with ffmpeg at roughly one frame every five seconds, clamped between 8 and 20 frames. These frames are sent to Claude Haiku 4.5 as a vision request to produce a factual scene description. A second structured-output call rewrites that description into all requested caption styles in one JSON response." Tech tags shown: Claude Code, Codex, Anthropic Claude. GitHub: https://github.com/Arush777/himawari-fanboys . Demo: https://himawari-fanboys-nurukajmmvhcv3ppqzzusp.streamlit.app/ . Created "on July 06, 2026" (i.e., kickoff day — fast submission).
- Same page's "Explore more applications" module named several other Act II projects with one-line descriptions (captured verbatim as shown, from card text — not opened individually except where noted):
  - "ArchMind: AI Software Architect" — team **ThunderBIRDS** — "ArchMind transforms any codebase into an intelligent knowledge graph that AI agents can reason over... " Link shown: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/thunderbirds/archmind-ai-software-architect — **this URL 404'd when fetched directly** ("Even AI can't find this page"). UNVERIFIED whether project truly exists at that slug; card text came from the recommendation widget only.
  - "ROCmPorter Agent" — team **HACKER_IS_BACK** — "Local AI assistant that scans CUDA-heavy GitHub repos, finds AMD ROCm migration blockers, and exports verified review-ready patch artifacts." Link shown: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/hackerisback/rocmporter-agent — **also 404'd on direct fetch.**
  - "Agent Rerouter" — team **Architects-on-Giants** — card text was just the raw URL/invite link, no description rendered cleanly. Link shown: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/architects-on-giants/agent-rerouter — **404'd on direct fetch** (twice, including with cache-bypass header). Note: this is the SAME team slug as section 2's "architects-on-giants" team page, which currently says "Team Leader hasn't made a submission yet" — direct contradiction/staleness between the recommendation widget and the team page. Unresolved; flagging as UNVERIFIED pending re-check closer to deadline. Given the name and Track 1's routing theme, this is the single most Track-1-sounding project name found in this research, but its actual content could NOT be verified.
  - "TokenPilot: Local Token Router for Coding Agents" — team **Waycode Labs** — card text (verbatim): "TokenPilot is a local-first MCP + CLI layer that scans repos, prepares compact coding-agent briefs, routes work through cheap/local paths first, and reports estimated paid-token savings." Link shown: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/waycode-labs/tokenpilot-local-token-router-for-coding-agents — **404'd on direct fetch.** Same caveat as above: name/description strongly resonates with Track 1's local-vs-remote routing theme, but page content unverifiable at fetch time.
  - "Greenops" (displayed as "GreenOps Optimizer") — team **Kage Shogun** — "GreenOps Optimizer is an automated FinOps/GreenOps pipeline that nightly scans AWS environments for idle and wasteful resources (EC2, RDS, EBS, ELB, etc.), automatically remediates them based on policies, estimates cost savings." Link shown: https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/kage-shogun/greenops — **404'd on direct fetch.**
- All five direct-fetch attempts above returned GitHub-style 404 page text: "# Even AI can't find this page / Looks like we took a wrong turn somewhere!..." — consistent with either (a) these being recommendation-widget entries for OTHER/future hackathons not yet live at that exact slug, (b) stale/cached links, or (c) the projects being unpublished/draft. Could not determine which. Not fabricating further detail beyond what's quoted above.

## 4. GitHub repos found for Act II (via web search)

- **arnavja/amd-hackathon-2026** — team "Byte Titans". README (as of commit `a8045c5`, "Initialize scaffold for AMD Hackathon ACT II", dated Jun 15, 2026 — i.e., BEFORE kickoff): verbatim: "Repo for the AMD Developer Hackathon ACT II (July 6–11, 2026)." Team: Arnav Jain (@arnavja), Kalpit Phogat (@kalpitphogat), Lakshya Jain (@anonymousz77), Manvil (@ManvilB). Stack section verbatim: "**Hardware:** AMD Instinct MI300X (via AMD Developer Cloud, $100 credits per member) / **GPU stack:** ROCm (not CUDA) / **Framework:** PyTorch with ROCm build / **Project idea:** TBD — challenge details revealed July 6." Judging criteria as they recorded it (verbatim, note this differs from the official page's Track-specific criteria — may be a generic/older lablab rubric they copied): "1. Application of Technology / 2. Presentation / 3. Business Value / 4. Originality." No Track 1 strategy content yet (repo is a pre-kickoff scaffold only — src/, notebooks/, scripts/, docs/ all empty scaffolding per the tree listing). URL: https://github.com/arnavja/amd-hackathon-2026/blob/main/README.md
- **GiorgiBurjaliani/webfinalproject issue #20** — this is an automated hackathon-listing/aggregator issue, not a team's own repo. Verbatim fields: "**Organizer:** AMD & lablab.ai", "**Format:** Online", "**Funding:** Free", "**Region:** Worldwide", "**End Date:** 2026-07-11", "**Official URL:** https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii". No strategy content. URL: https://github.com/GiorgiBurjaliani/webfinalproject/issues/20
- **CG-Guy/ordoflow-amd-hackathon-demo** — "OrdoFlow". Important: this repo targets the **prior/first** "AMD Developer Hackathon" (link in its own README points to https://lablab.ai/ai-hackathons/amd-developer, NOT amd-developer-hackathon-act-ii), and that event's "Track 1" was "AI Agents & Agentic Workflows" (a different rubric than Act II's token-efficient-routing Track 1). Verbatim: "GitHub: The linked repo is our public hackathon pack (architecture, samples, deck/video links, judging alignment). Full production source lives in a separate private repository..." Repo layout includes `docs/COPILOT_SIDECAR_RUNBOOK.md ← Track 1 sidecar modes (source in private repo)`. Live product: https://www.ordoflows.com/ . Not directly comparable to our Act II Track 1, but shows one team's submission-packaging pattern (public "safe" repo + private real code, judging-alignment doc). URL: https://github.com/CG-Guy/ordoflow-amd-hackathon-demo

## 5. Prior event: "AMD Developer Hackathon" (predecessor to Act II — no official "Act I" label found on lablab.ai)

Source: https://r.jina.ai/https://lablab.ai/ai-hackathons/amd-developer (page titled "[Recap] AMD Developer Hackathon")

- Dates/format (verbatim): "Hybrid / Monday, May 4 2026 - 2:00 PM Coordinated Universal Time" ... "📍 On-site Venue (May 9-10): MindsDB SF AI Collective, 3154 17th St, San Francisco, California, USA" ... "📍On-site participation is by invitation only."
- Scale (verbatim numbers shown on page): "10775 Participants / 2621 Teams / 481 AI Applications."
- **This prior event's tracks were NOT the same as Act II's.** Verbatim: "🤖 Track 1: AI Agents & Agentic Workflows (Best Track for Beginners)" / "⚡ Track 2: Fine-Tuning on AMD GPUs (Advanced / GPU-Intensive)" / "🎨 Track 3: Vision & Multimodal AI." There is **no token-efficient-routing / hybrid local-vs-remote-model track in this prior event** — that concept appears new to Act II. (This is a negative finding: no direct precedent located for Act II's specific Track 1 rubric.)
- Prize pool (verbatim): "🏆 Total Prize Pool: $22,500+ / $20,000 cash prizes... plus AMD hardware, Hugging Face, and Qwen special rewards." Grand Prize $5,000; per-track 1st/2nd/3rd $2,500/$1,500 or $2,500/$1,000 (Fine-Tuning 2nd place shown as $1,500; AI Agents 2nd place shown as $2,500 — page literally lists differing 2nd-place amounts per track, quoted as-is, not normalized).
- Special prizes: Hugging Face Space "most likes" prize, and a "Qwen Special Reward — Best use of Qwen in each track" (10M Qwen tokens per team member).
- "Winners and Finalists" section header text (verbatim, appears to be stale/leftover copy even on this "Recap" page): "We are in the process of selecting the finalist teams. Your voice matters! Vote on your favorite projects in the section below. Join us for the winner announcement stream, which will be streamed live on Twitch." — i.e., the page does not explicitly state final ranked winners in prose; it does show a "Winner Submissions 🏆" gallery of 13 named projects (below) without per-project 1st/2nd/3rd labels visible in the fetched markdown.
- **Winner Submissions 🏆 gallery (13 projects, verbatim short descriptions):**
  - "CatalystMD: AI-Powered Drug Discovery Platform" — team **CatalystMD** — "an AI-powered drug discovery platform that helps scientists find promising drug candidates for difficult disease targets."
  - "Chaos Economy: Multi-Agent RL Market Simulator" — team **TechMavericks** — "Multi-agent RL sim: 4 traders, market maker & SEC regulator trained via GRPO on Llama-3.2. 250 steps of emergent financial crisis..."
  - "REPOMIND" — team **REPOMIND** — "Open-source repo-scale coding agent verified on AMD MI300X. Single GPU, Qwen3-Coder-Next-FP8, 256K context. 31/31 users at 8K-64K, 3/3 needle 200K, 9/9 correct on pytorch/vision (1.3M tokens). 124-min stress test, AITER tuning A/B. MIT."
  - "XIAO Field Copilot" — team **Go ahead** — "A multimodal hardware support copilot that identifies Seeed XIAO boards from photos..."
  - "BrainConnect - ASD" — team **XonKore** — "analyzes brain scans to help detect Autism Spectrum Disorder."
  - "Strike Lab" — team **Strike Lab** — "AI-powered biomechanical platform that transforms smartphone footage of football strikes into professional-grade performance reports."
  - "AgentReady" — team **SoloDev** — "We built two robots that try 46 sneaky attacks on every famous AI agent. 13 of 13 got fooled. Then we open an auto-fix GitHub PR. All on one AMD MI300X."
  - "Automato" — team **BISAKOLAI** — "Vision-Native RPA that automates software like humans... Qwen 3.6 AI, a pinecone database, and pygetui..."
  - "Eidolon" — team **God_Axis** — "Hypernetwork that generates task-specific LoRA adapters on-the-fly from few-shot examples, enabling instant domain specialization of LLMs without per-task fine-tuning."
  - "Boardroom" — team **APEX101** — "Four specialist AI agents — Analyst, Skeptic, Strategist, and Auditor — deliberate over any uploaded document... Built on Llama 3.1 70B running on AMD Instinct MI300X with vLLM prefix caching."
  - "StudioMI300 - cinematic reel from one prompt" — team **StudioMI300** — "One prompt becomes a 30-second cinematic reel... Qwen3.5-35B + FLUX.2 klein + Wan2.2-I2V + ACE-Step + Kokoro."
  - "Lumi, AI voice helper for elderly with dementia" — team **AlphaZero** — "domain fine-tuned AI voice companion for dementia care, built on AMD MI300X... Ranked 7th on EQ-Bench 3 out of 46 models."
  - "AtlasOps" — team **Da Big Three** — "coordinates four specialist agents against live Kubernetes incidents—with real observability tools, approvals, Chaos Mesh scenarios..."
  - No explicit judges' written comments/scores accompany any of these entries in the fetched markdown.
- Other (non-winner) "Submitted concepts, prototypes and pitches" from this same prior event, of note for the routing/orchestration angle (paraphrase where noted):
  - "Adaptive Cognitive Runtime: Autonomous Engineering" — team **maindevhoon** — verbatim: "CogniRoute is an AI orchestration that allocates reasoning acros[s] agents instead of relying on one monolithic model. Heavyweight reasoning models handle planning & verification, while lightweight workers execute scoped implementation tasks." (Conceptually close to a "routing" idea, but for the OLD event's Track 1 = AI Agents track, not Act II's token-efficient-routing track.)
  - "OrdoFlow — AI Quote-to-Cash Copilot (AMD Track 1)" appears in this recap's submissions list too (same project as GitHub repo in section 4).
  - "FinTracker AI- Intelligent Finance Router" — name contains "Router" but appears to be a personal-finance tracking tool, not a model-routing agent (title only captured, description not opened).
  - "SentinelMesh" — mentioned inline (paraphrase): built for "Track 1: AI Agents," ingests live syslog data at 2.4 TB/s with 4 autonomous agents on MI300X GPUs — old event's Track 1, unrelated to token routing.
- No dedicated hackathon-specific leaderboard with numeric scores was found; the only "Leaderboard" link on the page points to lablab.ai's site-wide user leaderboard (https://lablab.ai/leaderboard), not a hackathon-specific score table.

## 6. lablab.ai general reference pages

- **Recent Winners** — https://r.jina.ai/https://lablab.ai/apps/recent-winners — This page currently lists winners from the **BrightData "AI Agents & Web Data" hackathon** and the **"Milan AI Week" / AI Agent Olympics hackathon** — **no AMD Developer Hackathon (Act II or prior) entries appear on this page** as of fetch time. Listed for completeness; not relevant to our Track 1 competitors. Example entries (verbatim project names/teams, unrelated to AMD): "Wayfinder" (1st place, Bright Data hackathon), "Kraken Alpha Agent" (1st place, Milan AI Week), etc.
- **Hackathon Guidelines** — https://r.jina.ai/https://lablab.ai/ai-articles/hackathon-guidelines — Generic step-by-step participation guide (profile → register → connect Discord → team → submit). Submission form fields listed verbatim: "Submission Title (max 50 characters)", "Short Description (Summary) (max 255 characters)", "Long Description (minimum 100 words)", "Main Tracks", "Technologies", "Cover Image (16:9)", "Video Presentation (under 300MB, within 5 minutes)", "GitHub Repository", "Demo Application Platform", "Demo Application URL". No AMD/Track-1-specific rubric detail beyond what's already in the Participant Guide PDF.

## 7. Blocked / inaccessible sources

- https://web3voyager.com/event/amd-developer-hackathon-act-ii/ — Cloudflare-style challenge even via r.jina.ai proxy: "Checking your browser before accessing... Warning: Target URL returned error 403: Forbidden."
- https://x.com/AIatAMD/status/2070526900951232841 — r.jina.ai returned: `{"code":403,"name":"AbuseAlleviationError",...,"message":"Anonymous access to domain x.com blocked until Tue Jul 07 2026 06:53:51 GMT... due to previous abuse found on https://x.com/blocmates: DDoS attack suspected"}` — could not read tweet content ("BUT WAIT! It is not over! AMD Developer Hackathon: Act II ..." per search snippet only, not verified in full).
- https://x.com/lablabai/status/2037263372014514272 — same AbuseAlleviationError block. Search-snippet-only text (UNVERIFIED, not independently confirmed): "NEW -> AMD Developer Hackathon with @AIatAMD: Build blazing AI Agents & Production-ready Apps on next-level GPUs. Free access to one of the most powerful GPUs. May 4-10, 2026. $10K & Radeon AI PRO R9700." Note this $10K figure conflicts with the $22,500+ figure shown on the official recap page (section 5) — could not reconcile; possibly an early/pre-launch tweet before the prize pool was finalized/increased, but UNVERIFIED.
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/teams — loads cookie banner + 404 image only (see section 1).
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/leaderboard — connection error via proxy.
- "TokenSage" — a project name repeatedly surfaced verbatim in WebSearch tool's own synthesized summaries (paraphrase of tool output): "a hybrid AI routing system that intelligently directs simple queries to a local AMD Ryzen AI NPU and complex queries to cloud LLMs..." — **UNVERIFIED**: despite three separate targeted searches ("Agent Rerouter"/"TokenSage" AMD hackathon routing NPU / "TokenSage" lablab.ai AMD hackathon / TokenSage lablab.ai hackathon), no actual source URL for a project called "TokenSage" was ever returned in the underlying search-result link lists — only the search tool's own prose repeated the claim without citation. Do not treat as confirmed; no lablab.ai or GitHub page for "TokenSage" was located or fetched.

## 8. More Act II team subpages found via web search

- **/hackerisback** and other team slugs referenced only through the himawari "explore more" widget (section 3) were not independently confirmed as real team pages (only the project-detail sub-slugs were tried and 404'd; the bare team pages like `/thunderbirds`, `/hackerisback`, `/waycode-labs`, `/kage-shogun` were not separately fetched in this pass).
- No additional genuine Act II team pages beyond those in sections 2 and 3 were found via web search in this session.

## 9. Hacker News search results

Searched via `hn.algolia.com/api/v1/search` (relevance) and `search_by_date` for: "AMD hackathon", "lablab.ai", "AMD Fireworks hackathon", "token-efficient routing agent", "AMD Developer Hackathon Act". Only two genuinely on-topic hits found (both about the **prior/first** hackathon, not Act II):

- **umairyousif2280**, comment on "Ask HN: What are you working on? (May 2026)", 2026-05-11: verbatim: "I recently built this project for AMD AI Hackathon. At it's core, it's a local first debugging tool thats powered by Qwen 3.5:9b. You give it a repo and an error log and It finds the root cause, suggests a fix, shows the bug propagation and the files it went through. The fix it suggests is in a diff format so its very easy to apply the fix." Repo: https://github.com/umairyousif239/AxionSys . Comment URL: https://news.ycombinator.com/item?id=48099552
- **lhl**, comment on "Show HN: Real-time AI Voice Chat at ~500ms Latency", 2025-05-06: verbatim: "Maybe of interest, I built and open-sourced a similar (web-based) end-to-end voice project last year for an AMD Hackathon: https://github.com/lhl/voicechat2 ... As a submission for an AMD Hackathon, one big thing is that I tested all the components to work with RDNA3 cards." Note: dated 2025-05-06 ("last year" relative to a 2025 post) — this refers to a **different, earlier** AMD hackathon (pre-2026), not the current Act II or even the May 2026 event. Comment URL: https://news.ycombinator.com/item?id=43901834
- Queries "AMD Fireworks hackathon" and "token-efficient routing agent" on HN Algolia returned **zero hits** (verbatim: `"hits": 0`).
- No HN discussion of "AMD Developer Hackathon: ACT II" specifically, and no HN discussion of Track 1 / token-efficient routing / Fireworks token counting for this event, was found.

## 10. Reddit / Medium search results

- Reddit: `site:reddit.com AMD Developer Hackathon lablab 2026` — WebSearch tool returned **no links** ("No links found").
- Medium: `site:medium.com "AMD Developer Hackathon" lablab` — WebSearch tool returned **no Medium.com results**; all links returned were lablab.ai/AMD/GitHub/HuggingFace/LinkedIn pages already covered elsewhere in this log.
- No Reddit or Medium posts about this event (Act II or the prior one) were located.

## 11. Hugging Face community write-ups (prior/first hackathon — Fine-Tuning track, not Act II Track 1)

Fetched by direct `curl` (not via r.jina.ai, since huggingface.co blocked the jina proxy with an AbuseAlleviationError at fetch time: `"Anonymous access to domain huggingface.co blocked... due to previous abuse found on https://huggingface.co/spaces/awacke1/Image-to-Line-Drawings"`). Direct curl to huggingface.co worked.

- **"MedQA: Fine-Tuning a Clinical AI on AMD ROCm — No CUDA Required"** — HF Community Article, published May 8, 2026, by Harikrishna (HK2184) / byline "Harikrishna Sivanand Iyer and Srijan Sivaram", org `lablab-ai-amd-developer-hackathon`. URL: https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/medqa
  - Verbatim: "A complete walkthrough of LoRA fine-tuning Qwen3-1.7B on MedMCQA using AMD MI300X, built for the AMD Developer Hackathon on lablab.ai."
  - Results table (verbatim values): Trainable parameters ~2.2M (0.15% of total); Training time on MI300X ~5 minutes; Dataset size used 2,000 samples; Baseline MedMCQA accuracy ~45%; Framework PyTorch + ROCm 6.1.
  - "Challenges and Fixes" table (verbatim, genuine post-mortem content): NaN loss → root cause "Mixed precision instability" → fix "Switched from bfloat16 → fp16"; GPU not detected → "Missing ROCm env variables" → fix "Set ROCR_VISIBLE_DEVICES, HIP_VISIBLE_DEVICES, HSA_OVERRIDE_GFX_VERSION"; bitsandbytes unsupported → "No ROCm build of bitsandbytes" → fix "Dropped quantization entirely — MI300X has enough VRAM"; Garbage inference output → "Tokenizer padding misconfigured" → fix "Set pad_token = eos_token and fixed padding_side"; Trainer eval errors → "Transformers version mismatch" → fix "Pinned transformers>=4.40.0".
  - Model: https://huggingface.co/HK2184/medqa-qwen3-lora . GitHub: https://github.com/HK2184/MedQA-Medical-AI-on-AMD-ROCm . This is for the **prior/first** hackathon's Fine-Tuning track, not Act II Track 1 — included as the most detailed genuine "post-mortem" style write-up found for any AMD×lablab hackathon in this research.
  - Same author's other articles listed under "More from this author" (titles only, not opened): "MachinaCheck: Building a Multi-Agent CNC Manufacturability System on AMD MI300X" (May 10, 2026) and "OncoAgent: A Dual-Tier Multi-Agent Framework for Privacy-Preserving Oncology Clinical Decision Support" (May 9, 2026) — both appear to be from the same prior hackathon's Agents track, based on "Multi-Agent" framing; not independently verified/opened.
- HuggingFace Hub API query for org `lablab-ai-amd-developer-hackathon` models (https://huggingface.co/api/models?author=lablab-ai-amd-developer-hackathon) returned 14 models, all evidently from the **prior/first** hackathon (no Act II equivalent org/models found): `SentinelBrain-14B-MoE-v0.1`, `MediAgent`, `asd-interpreter-merged`, `Ghost-Coder-Qwen2.5-32B-LoR`, `CyberSecQwen-4B`, `medqa-qwen3-lora`, `RetinoAgent-weights`, `OncoAgent-v1.0-27B`, `OncoAgent-v1.0-9B`, `Qwen-security-auditor-14b`, `Qwen-security-builder-14b`, `RasoSpeak`, `mindforge-qwen-lora-amd-hackathon`, `movimento`. None of these names suggest a token-routing project; they map to the old event's Agents/Fine-Tuning/Vision tracks (medical, security, CNC, oncology, etc.).

## 12. lablab-ai/community-content blog (GitHub, prior hackathon)

Source (fetched via raw.githubusercontent.com after r.jina.ai/github.com hit its own rate-limit block): https://raw.githubusercontent.com/lablab-ai/community-content/main/blog/en/from-zero-to-ai-builder-amd-developer-program.mdx (rendered page: https://lablab.ai — GitHub path: https://github.com/lablab-ai/community-content/blob/main/blog/en/from-zero-to-ai-builder-amd-developer-program.mdx)

- Title (verbatim): "From Zero to AI Builder with AMD: MI300X GPUs for AI Hackathons", author `stevekimoi`.
- States the prior hackathon has **four** tracks (verbatim): "AI Agents & Agentic Workflows", "Fine-Tuning on AMD GPUs", "Vision & Multimodal AI", "Build in Public" (this fourth item is a prize track/challenge, matching the "🚢 Extra Challenge: Ship It + Build in Public" from the official recap page in section 5 — the blog counts it as a 4th "track").
- Closing line states a prize figure that conflicts sharply with all other sources (verbatim, flagged as likely erroneous/unverified): "the AMD Developer Hackathon is running now with $1.1M in prizes across four tracks." — Contradicts the recap page's "$22,500+" (section 5) and HackPost's "$20,000 + AMD Radeon AI PRO R9700 GPU" (section 13). Not reconciled; recording as-is per instructions not to invent/resolve.
- No Track-1-style token-routing content (this article predates/is unrelated to Act II).

## 13. Third-party hackathon aggregator: HackPost

- https://hackpost.io/hackathons/amd-developer — lists the **prior/first** AMD Developer Hackathon. Verbatim: "A compute-heavy build sprint for teams shipping AI systems on AMD infrastructure." Event snapshot (verbatim): "Prize pool: $20,000 + AMD Radeon AI PRO R9700 GPU" / "Participants: 5,537" / "MAY 4 - 11" / "San Francisco, CA + online". Note the participant count (5,537) **conflicts** with lablab.ai's own recap page figure of 10,775 participants (section 5) — third-party aggregator data appears stale or measured at a different point in time; not reconciled, recorded as-is.
- Tried guessing an Act II listing at https://hackpost.io/hackathons/amd-developer-hackathon-act-ii , /amd-developer-act-ii , /amd-act-ii — all three returned HTTP 200 but with body text "That listing may have been removed or the URL may be incorrect." — **no Act II listing exists on HackPost** as of fetch time.

## 14. UNVERIFIED / discrepancy notes (consolidated)

- "TokenSage" project — see section 7. Never found a real source URL despite 3 targeted searches. Do not treat as a real Act II submission.
- "Agent Rerouter" (Architects-on-Giants) and "TokenPilot: Local Token Router for Coding Agents" (Waycode Labs) — names/descriptions surfaced via a recommendation widget on a real, verified Act II submission page (himawari's), but the specific project URLs 404'd on direct fetch, and the team's own page (architects-on-giants) says no submission has been made yet. Genuinely unresolved — could be real submissions not yet live at that slug, or stale/broken recommendation links. Flagged, not fabricated further.
- Prize-pool figures for the **prior/first** AMD Developer Hackathon vary by source: lablab.ai recap page says "$22,500+" (section 5); a since-blocked tweet snippet said "$10K" (section 7); lablab-ai's own community-content blog said "$1.1M" (section 12); HackPost said "$20,000 + AMD Radeon AI PRO R9700 GPU" (section 13); the AMD.com blog article said "$20,000" (section — see amd_blog fetch). These are not reconciled here — recorded as found, per source.
- Participant/team counts for the prior hackathon also vary: lablab.ai recap page = 10,775 participants / 2,621 teams / 481 applications (section 5); HackPost = 5,537 participants (section 13); a WebSearch-tool-synthesized paragraph (not a primary source, do not cite as fact) claimed "10,766 total participants across 2,626 teams, with 477 final submissions across 5 tracks" — this synthesis number is UNVERIFIED and conflicts slightly with the primary source in section 5; the lablab.ai recap page numbers (section 5) are the most directly-sourced and should be preferred over any WebSearch-tool prose summaries.

---

## Sources (all URLs visited or attempted in this research session)

Successfully fetched (via r.jina.ai proxy unless noted):
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/teams (loaded but no roster content — cookie banner + 404 image only)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/submissions (loaded but no content shown)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/projects (loaded but no content shown)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/blaze
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/armageddon
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/hackq
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/indian-ai-warrior
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/spanther
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/practers
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/codestorm-hub
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/cipher
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/hivize
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/architects-on-giants
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/himawari/video-captioning-agent
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/architects-on-giants/agent-rerouter (404 — "Even AI can't find this page")
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/waycode-labs/tokenpilot-local-token-router-for-coding-agents (404)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/thunderbirds/archmind-ai-software-architect (404)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/hackerisback/rocmporter-agent (404)
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/kage-shogun/greenops (404)
- https://lablab.ai/ai-hackathons/amd-developer (prior event recap page)
- https://lablab.ai/ai-hackathons/amd-developer/hackai (prior event team page, no submission)
- https://lablab.ai/apps/recent-winners (no AMD-specific entries)
- https://lablab.ai/ai-articles/hackathon-guidelines
- https://github.com/GiorgiBurjaliani/webfinalproject/issues/20
- https://github.com/arnavja/amd-hackathon-2026/blob/main/README.md
- https://github.com/CG-Guy/ordoflow-amd-hackathon-demo
- https://www.amd.com/en/developer/resources/technical-articles/2026/build-across-the-ai-stack--join-the-amd-x-lablab-ai-hackathon-.html
- https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/medqa (fetched via direct curl, not jina — jina blocked huggingface.co)
- https://huggingface.co/api/models?author=lablab-ai-amd-developer-hackathon (direct API call)
- https://raw.githubusercontent.com/lablab-ai/community-content/main/blog/en/from-zero-to-ai-builder-amd-developer-program.mdx (fetched via raw.githubusercontent.com after jina blocked github.com)
- https://hackpost.io/hackathons/amd-developer
- https://hn.algolia.com/api/v1/search?query=AMD%20hackathon (and search_by_date variants with queries: "lablab.ai", "AMD Fireworks hackathon", "token-efficient routing agent", "AMD Developer Hackathon Act")
- https://news.ycombinator.com/item?id=48099552 (via HN Algolia API text, not separately fetched)
- https://news.ycombinator.com/item?id=43901834 (via HN Algolia API text, not separately fetched)

Attempted but blocked/inaccessible:
- https://web3voyager.com/event/amd-developer-hackathon-act-ii/ — 403 Forbidden even via jina proxy.
- https://x.com/AIatAMD/status/2070526900951232841 — jina proxy AbuseAlleviationError (anonymous access to x.com blocked).
- https://x.com/lablabai/status/2037263372014514272 — same AbuseAlleviationError.
- https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/leaderboard — connection error via proxy.
- https://hackpost.io/hackathons/amd-developer-hackathon-act-ii — HTTP 200 but "listing may have been removed" (no Act II page exists).
- https://hackpost.io/hackathons/amd-developer-act-ii — same, no listing.
- https://hackpost.io/hackathons/amd-act-ii — same, no listing.
- https://github.com/lablab-ai/community-content/blob/main/blog/en/from-zero-to-ai-builder-amd-developer-program.mdx — jina proxy AbuseAlleviationError on github.com (worked instead via raw.githubusercontent.com, see above).

WebSearch queries run (tool-mediated, not direct fetches — results/links already folded into sections above):
- "AMD Developer Hackathon" "Act II" github routing agent Track 1
- "AMD Developer Hackathon: ACT II" lablab.ai team submission
- "Agent Rerouter" lablab.ai AMD hackathon
- "TokenPilot" lablab.ai AMD hackathon token router
- "TokenSage" AMD hackathon routing NPU
- TokenSage lablab.ai hackathon
- "AMD Developer Hackathon" "ACT II" reddit OR twitter OR x.com Track 1 routing
- site:github.com "amd-developer-hackathon" OR "amd hackathon act ii" router 2026
- site:reddit.com AMD Developer Hackathon lablab 2026
- site:medium.com "AMD Developer Hackathon" lablab
- "amd-developer-hackathon-act-ii" Track 1 router github OR devpost
