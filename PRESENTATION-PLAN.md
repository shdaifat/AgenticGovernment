# Presentation Plan — How We Built an AI Grant Evaluation System from Scratch

> **Audience:** Non-technical JEDCO staff and government decision-makers
> **Format:** HTML slides (reveal.js), hosted on GitHub Pages
> **Language:** English with Arabic examples — switch to full Arabic version later
> **Goal:** Show step-by-step how anyone with a computer can build this — and that an AI agent helped build it

---

## Slide Deck Structure

### ACT 1: THE STARTING POINT (5 slides)

#### Slide 1 — Title
- "How We Built an AI-Powered Grant Review System — From Zero"
- Subtitle: "No subscriptions. No cloud. Just a laptop."
- JEDCO logo + date

#### Slide 2 — What We Started With
- A regular laptop (Intel i7, 16GB RAM, NVIDIA RTX 2060 — 6GB GPU)
- Windows 11
- No AI tools installed
- No data
- No budget for AI subscriptions
- **Visual:** Empty desktop screenshot

#### Slide 3 — What We Ended With
- A working system that:
  - Reads grant applications (Arabic PDFs)
  - Checks documents against eligibility criteria
  - Scores applications automatically
  - Flags compliance issues
  - Produces a ranked report with recommendations
- All running locally — no internet needed
- **Visual:** Screenshot of results.html report

#### Slide 4 — The Key Insight: An Agent Built an Agent
- We used a coding AI (GitHub Copilot in VS Code) to build the evaluation AI
- We didn't write code — we wrote instructions in plain language
- The coding agent wrote Python, created files, ran commands
- The evaluation agent reads applications and produces reports
- **Diagram:**
  ```
  YOU (plain language instructions)
    → Agent 1: Copilot (writes code)
      → Agent 2: Evaluation Pipeline (reads applications)
        → Report (human reviews and decides)
  ```

#### Slide 5 — Everything Is Free
| Tool | What it does | Cost |
|------|-------------|------|
| VS Code | Code editor / agent workspace | Free |
| GitHub Copilot (Free tier) | Coding agent — writes code from instructions | Free |
| Ollama | Runs AI models locally | Free |
| Qwen3 8B | Arabic + English language model | Free |
| Python | Runs the pipeline | Free |
| Git + GitHub | Hosts and shares the project | Free |

---

### ACT 2: HOW WE BUILT IT — STEP BY STEP (10 slides)

#### Slide 6 — Step 1: Install the AI Brain
- Download Ollama (ollama.com) — 5 minutes
- Pull the model: `ollama pull qwen3:8b` — 10 minutes
- Test it: `ollama run qwen3:8b "ما هي شروط أهلية برنامج تطوير؟"`
- **Visual:** Terminal screenshot showing Ollama running
- **Talking point:** "This is the AI. It runs on YOUR computer. Nothing goes to the internet."

#### Slide 7 — Step 2: Install the Builder (Copilot)
- Open VS Code → install GitHub Copilot extension → sign in (free)
- Open the chat panel → start giving instructions
- **Visual:** VS Code with Copilot chat panel open
- **Talking point:** "This is Agent 1. You talk to it. It writes code."

#### Slide 7b — Test Manually First (Like Using ChatGPT)
- **Before automating, let's verify the AI works for evaluation tasks**
- Open Ollama interactive mode: `ollama run qwen3:8b`
- Test with a natural question:
  ```
  >>> You are a JEDCO evaluator. Does this company with 3 employees 
      qualify for Tattweer?
  ```
- Ollama responds correctly: "No, Tattweer requires minimum 5 employees..."
- **The problem we're trying to solve:**
  - This works great! But now imagine:
  - 100 applications to evaluate
  - Type the same prompt 100 times?
  - Copy-paste answers into a spreadsheet?
- **Transition:** "This is why we automate →"
- **Talking point:** "Manual testing proves the concept. Now let's eliminate the repetition."

#### Slide 8 — Step 3: We Had No Data — So We Made It
- Real JEDCO applications are confidential
- We told Copilot: "Create a realistic mock application for JEDCO's Start Business program"
- It generated: applicant details, budget, action plan, documents checklist
- All in Arabic, matching JEDCO's actual format
- **Show:** Side-by-side: the prompt we gave vs. the mock application it created
- **Prompt example:**
  ```
  Create a realistic mock application for JEDCO's "Start Business" program.
  Include: applicant data, project description, budget table, action plan,
  expected impact, and document checklist. All in Arabic. Use fake names
  and numbers. Make it look like a real JEDCO application form.
  ```
- **Output:** (show mock-application-start-business-AR.txt excerpt)

#### Slide 9 — Step 4: Feed It the Rules
- We downloaded JEDCO's official program documents (PDFs from jedco.gov.jo)
- We compiled eligibility criteria, scoring rubrics, and evaluation methodology
- We told Copilot: "Create a comprehensive eligibility reference from these documents"
- The AI organized JEDCO's own rules into a structured format the evaluation pipeline can use
- **Show:** Excerpt from JEDCO-eligibility-criteria-reference-v2.txt
- **Key point:** "The AI doesn't invent rules. It applies YOUR rules to YOUR applications."

#### Slide 10 — Step 5: Build the Pipeline (fixing real problems)
- We told Copilot: "Write a Python script that reads applications, checks eligibility, scores them, and produces a report"
- **It didn't work perfectly the first time. Here's what happened:**

  **Problem 1: Qwen thinking out loud**
  - Qwen3 has a "thinking mode" — it wraps internal reasoning in `<think>...</think>` tags
  - Our first output included raw thinking text mixed with the actual evaluation
  - **Fix:** We added code to strip `<think>` blocks from the output
  - **Before:** `<think>Let me analyze this application...</think> Score: 80`
  - **After:** `Score: 80`

  **Problem 2: Inconsistent scoring format**
  - Sometimes Qwen returned `Score: 80/100`, sometimes `80 points`, sometimes a paragraph
  - **Fix:** We refined the prompt to demand: "Output ONLY a JSON object with score and recommendation"
  - **Before prompt:** "Score this application"
  - **After prompt:** "Score this application. Output ONLY valid JSON: {\"score\": <number>, \"recommendation\": \"INVITE|REVIEW|REJECT\", \"reasoning\": \"...\"}"

  **Problem 3: Arabic text encoding**
  - Some Arabic characters were garbled in the output
  - **Fix:** Added `ensure_ascii=False` to JSON output and UTF-8 encoding everywhere

  **Problem 3: Eligibility checks lacked context**
  - Without full criteria in the prompt, AI made inconsistent eligibility decisions
  - **Fix:** We pass the ENTIRE eligibility rubric with every prompt — no missing context, no guessing
  - **Lesson:** Better structure beats complex frameworks. Direct > RAG.

- **Talking point:** "Every problem had a fix. The coding agent helped us find it. This is normal — even experts iterate."

#### Slide 11 — Step 6: Good Prompts = Good Results
- The RCTF Formula: **R**ole, **C**ontext, **T**ask, **F**ormat
- **Bad prompt:**
  ```
  "هل هذا الطلب جيد؟"
  (Is this application good?)
  ```
  → Vague, general answer — useless for evaluation

- **Good prompt (RCTF):**
  ```
  Role: أنت مسؤول تقييم في JEDCO تطبّق معايير برنامج تطوير بصرامة.
  Context: رخصة المهن تنتهي في 31/12/2025 وتوقيع العقد في أيلول 2025.
  Task: هل يستوفي الطلب شرط صلاحية الرخصة طوال فترة التنفيذ (12 شهراً)؟
  Format: كلمة واحدة أولاً (مستوفي/غير مستوفي) ثم التوضيح.
  ```
  → "غير مستوفي — الرخصة تنتهي في الشهر الرابع من التنفيذ"

- **Show actual pipeline prompts and outputs side-by-side**

#### Slide 12 — Step 7: Run and Test
- Command: `python tools/evaluate-pipeline.py --model qwen3:8b --summary`
- Pipeline processes each application in ~90 seconds
- **Show actual output:**
  ```
  Application: Start Business — Ahmad (Sweets Factory)
  Admin Check: INCOMPLETE (missing commercial registration)
  Score: 80/100 → INVITE
  
  Application: Tattweer — Zahraa Textiles
  Admin Check: PASS
  Score: 93/100 → INVITE
  ```
- **Talking point:** "We verify against known answers. The mock applications have intentional issues — we check if the AI catches them."

#### Slide 12b — What We Just Automated
- **Visualization:** Side-by-side comparison
  ```
  MANUAL (What you did)          →  AUTOMATE  →        AUTOMATED (What Python does)
  • Open Ollama chat                               • Read 100 applications
  • Type prompts                                   • Send same prompts to Ollama
  • Read answers                                   • Collect all answers
  • Copy to spreadsheet                            • Format into reports
  × 100 apps = HOURS                              × 100 apps = MINUTES
  ```
- **Key insight:** Same tests. Same AI. Same logic. Python just removes manual repetition.
- **Talking point:** "Remember when we tested it manually with ChatGPT-style interaction? This Python pipeline does exactly that — but 100 times automatically. The intelligence is the same. The speed is different."

#### Slide 13 — Step 8: Generate Reports
- Pipeline produces:
  - **results.json** — machine-readable data
  - **results.html** — formatted report in browser
  - **results.pdf** — printable version
- Report includes: ranked shortlist, per-application breakdown, flagged issues, recommendations
- **Visual:** Screenshot of results.html
- **Talking point:** "This is what the officer sees. Not raw AI output — a formatted, professional report."

---

### ACT 3: WHAT'S NEXT — FROM DEMO TO REAL SYSTEM (5 slides)

#### Slide 14 — Where Can This Run?
| Deployment | Who uses it | Data stays... | Cost |
|-----------|------------|--------------|------|
| **Your laptop** | Just you | On your laptop | Free |
| **Office LAN** | Your team | In the office | Free (existing hardware) |
| **JEDCO server** | All JEDCO staff | On JEDCO infrastructure | Hardware: ~8,000 JOD |
| **Internet** | Applicants + staff | On rented server | ~20 JOD/month |

- **Key message:** Start on your laptop today. Scale when ready.

#### Slide 15 — The Applicant's Experience (Web Portal Vision)
- Applicant visits JEDCO portal
- Uploads application PDF + supporting documents
- System immediately checks: "You're missing the operating license"
- Applicant uploads the missing file
- System confirms: "All documents received — your application is under review"
- Officer receives the application pre-screened with AI-assisted score
- **Talking point:** "The applicant gets faster feedback. The officer gets a head start."

#### Slide 16 — What About Scanned Documents?
- Many JEDCO applications arrive as scanned paper (images, not text)
- **Solution:** OCR (Optical Character Recognition)
  - Scanned PDF → OCR reads the image → produces Arabic text → AI evaluates
  - **Tools:** Tesseract (free, open source) or Surya (better for Arabic)
  - Same pipeline, one extra step at the beginning
- **Visual:**
  ```
  Scanned Paper → [OCR: image→text] → Arabic Text → [AI: evaluate] → Report
  Text PDF       →                     Arabic Text → [AI: evaluate] → Report
  ```

#### Slide 17 — Don't Be Afraid of the Code
- You never need to understand the code
- You need to understand:
  - **What goes IN:** documents, criteria, a good prompt
  - **What comes OUT:** a report with scores and recommendations
  - **Whether the output is correct:** compare against your expertise
- The code is a black box — like Excel formulas. You care about the result.
- If the output is wrong → fix the prompt, not the code
- **Analogy:** You don't need to understand how a car engine works to drive. You need to know where you're going.

#### Slide 18 — Summary & Next Steps
- **What we proved today:**
  - You can build an AI evaluation system with free tools on one laptop
  - A coding agent built it — you gave instructions in plain language
  - The system reads Arabic applications and applies JEDCO's own rules
  - All data stays local — nothing goes to the cloud
- **What's coming:**
  - Video tutorials for each step (link placeholder)
  - Web portal prototype (applicant upload → officer review)
  - Arabic OCR for scanned documents
  - Integration with JEDCO's existing systems

---

## Technical Notes for Building the Presentation

### Format
- **reveal.js** — HTML slide framework, works in any browser
- Single file: `docs/index.html`
- Host via GitHub Pages → `shdaifat.github.io/AgenticGovernment`
- Mobile-friendly, supports Arabic RTL

### Content to Capture Before Building
- [ ] Screenshot: empty desktop (starting point)
- [ ] Screenshot: VS Code with Copilot chat showing a prompt
- [ ] Screenshot: terminal running `ollama pull qwen3:8b`
- [ ] Screenshot: terminal running `evaluate-pipeline.py`
- [ ] Screenshot: results.html report
- [ ] Screenshot: the `<think>` tag problem (before/after)
- [ ] Screenshot: AnythingLLM "not found" vs pipeline correct answer

### Slides That Need Real Output Examples
- Slide 8: exact prompt used to create mock application + excerpt of output
- Slide 10: actual `<think>` tag example, actual JSON format fix
- Slide 11: actual RCTF prompt and actual AI response (Arabic)
- Slide 12: actual pipeline terminal output
- Slide 13: actual results.html screenshot

### Video Placeholders (for later)
- [ ] Video: Installing Ollama and pulling a model
- [ ] Video: Using Copilot to create a file from scratch
- [ ] Video: Running the evaluation pipeline
- [ ] Video: Reading the HTML report
- [ ] Video: Writing a good prompt vs bad prompt

---

## Private Folder Structure (gitignored, local only)

```
private/
  JEDCO-AI-Grant-Management-Proposal-AR.md   ← financial proposal (Arabic)
  JEDCO-AI-Grant-Management-Proposal-EN.md   ← financial proposal (English)
  brainstorming/
    meeting-notes.md                          ← notes from JEDCO meetings
    pricing-options.md                        ← pricing tiers for deployment
    timeline-estimates.md                     ← implementation timeline
    competitor-analysis.md                    ← other AI tools JEDCO might consider
  screenshots/                                ← captured screenshots for slides
```
