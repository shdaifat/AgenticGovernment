# Training Slide Outline — Agentic Government / JEDCO
## Duration: 2 hours | Model: qwen3:8b | Tools: Ollama + Python

---

## Block 0 — How AI Works (10 min)

### Slides:
1. **Title**: "How Does AI Think?"
2. **The New Hire Analogy**:
   - AI is like a new employee who read everything but experienced nothing
   - Knows words but doesn't understand real-world context
   - Needs clear instructions — like any employee on day one
3. **What AI Can and Cannot Do**:
   - ✅ Read, summarize, write, compare
   - ❌ Doesn't understand intent, can't verify reality, can't make final decisions
4. **Security Message (upfront)**:
   - "Nothing leaves the machine — everything runs locally"
   - Motto: **Data stays here**

### Talking Point:
> "Imagine someone who memorized every JEDCO regulation — but never sat with an applicant or visited a factory. That's AI: it helps you prepare, but the decision stays with you."

---

## Block 1 — What is an AI Agent? (15 min)

### Slides:
1. **AI Tool vs AI Agent**:
   - Tool: you ask a question, it answers (like ChatGPT)
   - Agent: takes a full task and completes it in multiple steps
2. **AI = The Next Tool Upgrade**:
   - Everyone has a sword now — the skill is knowing how to use it
   - Excel automated calculations → AI agents automate reading, writing, and comparing
   - **The tool handles the routine. You handle the important. That's the pattern every time.**
2. **Government Examples**:
   - Tool: "Summarize this application" → one answer
   - Agent: "Review 100 applications, classify, produce report" → full workflow
3. **Pipeline Concept**:
   ```
   Receive App → Document Check → Evaluation → Recommendation → Report
   ```
4. **Golden Rule**: AI assists, humans decide

### Talking Point:
> "At JEDCO, an AI agent can handle the initial administrative checks — document lists, form completeness — so the officer has more time for what really needs human judgment: interviews, site visits, and difficult decisions."

---

## Block 2 — Document Writing Demo (25 min)

### Slides:
1. **Task**: Write a formal rejection letter in Arabic
2. **Live Demo**:
   - Open Ollama
   - Type a starting prompt first → limited result
   - Type an RCTF prompt → excellent result
3. **Side-by-side comparison**: starting prompt vs RCTF prompt
4. **Participant exercise** (5 min):
   - Each participant writes a prompt to generate a letter for their JEDCO program

### Demo Prompt:
```
You are the Start Business program manager at JEDCO.
Applicant: Ahmad Mohammad, restaurant project in Irbid.
Evaluation: commercial registration not attached, business plan incomplete.
Write a formal Arabic rejection letter with reasons and reapplication steps.
Format: formal letter with JEDCO header.
```

---

## Block 3 — Application Review Demo (25 min)

### Slides:
1. **Task**: Review a real Tattweer application via AnythingLLM
2. **Steps**:
   - Open AnythingLLM → "JEDCO Application Review" workspace
   - Documents pre-loaded: eligibility criteria + mock applications
3. **3 Progressive Questions**:
   - Q1: "What documents are required for the Tattweer program?"
   - Q2: "Review the Zahraa Textiles application — does it meet the criteria?"
   - Q3: "The license expires 31/12/2025, signing is September 2025, implementation is 12 months. Does it PASS the license requirement?"
4. **Lesson**: Q3 adds the specific timeline requirement that Q2 didn't include — revealing the license issue

### Talking Point:
> "Same AI. Same document. Different question — completely different result. This is why prompt engineering matters."

---

## Block 4 — RCTF Prompt Formula (20 min)

### Slides:
1. **The Formula**:
   | Letter | Meaning | Description |
   |--------|---------|-------------|
   | R | Role | Who should the AI be? |
   | C | Context | What background info does it need? |
   | T | Task | What exactly should it do? |
   | F | Format | How should it present the result? |

2. **3 JEDCO Program Examples** (see RCTF handout):
   - Tamkeen: evaluate company eligibility
   - Tattweer: catch the license issue
   - Start Business: write a rejection letter

3. **Hands-on Exercise** (10 min):
   - Distribute RCTF reference card
   - Each participant picks a JEDCO program and writes a full RCTF prompt
   - Test the prompt live on the machine

4. **Golden Rule: Plan Before You Prompt**:
   - Before typing anything, answer 3 questions in your head:
     1. What exactly do I want the AI to produce?
     2. What information does it need from me?
     3. How will I know if the result is good or bad?
   - If you can't answer these, you're not ready to prompt yet
   - **Detailed prompt → better understanding → better work quality**
   - Think of it like briefing a new colleague: the clearer your instructions, the better their output

### Talking Point:
> "Always plan first. Make sure the AI understands what it’s going to do — and that its plan matches the picture in your head. Only then hit Enter."
5. **Live Demo: The AI Plans Too (Thinking Mode)**:
   - Qwen3 has a built-in thinking mode — it reasons before answering
   - **Demo 1**: Ask with `/no_think` at end of prompt → fast answer, may miss details
   - **Demo 2**: Ask same question normally (thinking ON) → slower, but catches the license issue
   - Show the `<think>...</think>` block — the AI is literally planning its answer
   - **The lesson**: You plan before you prompt. The AI plans before it answers. Planning makes everything better.

### Talking Point:
> "Look — even the AI itself gets better results when it thinks first. You and the AI are doing the same thing: plan, then act."

6. **🌟 THE MOMENT: Congratulations, You Are an AI Expert!**
   - Pause. Look at the room. Say this:
   > "Stop for a second. Look at what you just did. You wrote a professional AI prompt. You tested it. You got a real result. You know RCTF. You know to plan before you prompt. You just saw the AI think before it answers — and you understand why.
   > **Congratulations — you are now an AI expert.** Not because you studied computer science. Because you know how to ask the right question. And that's 90% of AI."
   - This is the confidence builder — from this point on, they own it
---

## Block 5 — PC Agent Live Demo (20 min)

### Slides:
1. **Task**: Run an automated JEDCO application review pipeline
2. **Live Demo**:
   ```bash
   python tools/evaluate-pipeline.py --model qwen3:8b --limit 2 --summary
   ```
3. **What Happens**:
   - Stage 1: Administrative check (documents, license, sector, ownership)
   - Stage 2: Technical scoring (Financial 25 + Technical 40 + Sector 20 + Impact 15 = 100)
   - Stage 3: Arabic summary for committee
4. **Classification Thresholds**:
   - ≥70 points → INVITE
   - 50-69 → REVIEW
   - <50 → Below threshold — refer to officer
5. **Live Comparison**: RAG (AnythingLLM) vs Direct (Ollama)
   - Same model, same documents, different results
   - AnythingLLM: scored without timeline check → INVITE 87
   - Direct pipeline: timeline flag raised → officer review recommended

### Talking Point:
> "Choosing the right system design matters as much as choosing the model. AI helps the officer make a better-informed decision — but it never replaces the officer."

---

## Block 6 — Safe AI in Government + Q&A (15 min)

### Slides:
1. **5 Rules for Safe AI Use in Government**:
   - ✅ System runs locally — no data leaves the machine
   - ✅ Use mock data for training and testing
   - ✅ AI suggests, the officer decides
   - ✅ Review all AI outputs before approval
   - ❌ Never enter real applicant personal data
2. **Key Takeaways**:
   - AI is a powerful tool to accelerate work
   - Quality depends on prompt quality (RCTF)
   - Infrastructure (pipeline) determines outcomes
   - Humans always make the final decision
3. **Open Q&A**

---

## Materials Needed
- [ ] Laptop with Ollama + qwen3:8b + Python
- [ ] Display / projector
- [ ] Printed RCTF reference card (handouts/RCTF-cheatsheet-EN.txt)
- [ ] JEDCO docs available in assets/jedco-docs/
