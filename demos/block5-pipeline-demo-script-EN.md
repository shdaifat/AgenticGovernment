# Block 5 — PC Agent Live Demo Script
AI-Powered Grant Application Pipeline
Training: Agentic Government @ JEDCO
Duration: 20 minutes

TRAINER SETUP (before the session)
- Ollama running: qwen3:8b loaded
- AnythingLLM open with JEDCO Application Review workspace (also using qwen3:8b)
- This script open on second monitor
- n8n running locally at http://localhost:5678 (optional)
- assets/jedco-docs/ files uploaded to AnythingLLM

NARRATIVE (say this to the audience)
"JEDCO receives hundreds — sometimes thousands — of applications
every program cycle. Staff expertise is most valuable in interviews,
field visits, and complex decisions. What if an AI assistant could
handle the routine paperwork — document checks, form validation —
so staff can focus on the work that truly needs their judgment?

Let me show you what that looks like — running entirely
on this laptop, no cloud, no data leaving the room."

#### STAGE 1 — INTAKE & DOCUMENT CHECK (3 min)
WHAT TO SHOW:
  Open AnythingLLM → JEDCO Application Review workspace

TYPE THIS PROMPT:
  "You are a JEDCO intake officer. Review both applications in
  this workspace. For each one, confirm which required documents
  are present and which are missing. Output a table."

EXPECTED OUTPUT:
  A table comparing both applications against the document checklist.
  - Start Business: missing commercial registration (intentional)
  - Tattweer: all present (but license issue hidden for now)

**TRAINER TALKING POINT:**
  "In seconds, the AI scanned both applications and produced a
  document checklist. This is the initial administrative check
  the AI handles first — so the officer can direct their attention
  straight to evaluation and the cases that need expert judgment."

#### STAGE 2 — ELIGIBILITY SCORING (5 min)
WHAT TO SHOW:
  Same workspace, new prompt

TYPE THIS PROMPT:
  "You are a JEDCO evaluator. Score the Tattweer application
  (Zahraa Textiles) against the following criteria. Give a score
  out of 10 for each, then a total out of 50:

## 1. Sector priority (high-value 5 sectors)
## 2. Employment creation potential
## 3. Innovation / technology component
## 4. Financial capacity of applicant
## 5. Completeness and quality of documentation

  Show scores as a table. Then give a final recommendation:
  INVITE / REVIEW / REJECT"

EXPECTED OUTPUT:
  Scored table + recommendation. Should score high on sector
  (textiles = high-value) and employment, medium on innovation.

**TRAINER TALKING POINT:**
  "This scoring rubric is based on JEDCO's own published selection
  priorities. The AI applies the same criteria every time,
  giving the officer a consistent starting point.
  The human reviewer then validates the score and adds their
  professional judgment — context the AI simply cannot have."

#### STAGE 3 — HIDDEN ISSUE DETECTION (4 min)
WHAT TO SHOW:
  Demonstrate the difference between vague and precise prompting

PROMPT 1 (vague — show this first):
  "Does the Zahraa Textiles application have any problems?"

PROMPT 2 (RCTF — show this second):
  "You are a JEDCO program officer applying Tattweer rules strictly.
  The operating license must be valid throughout the 12-month
  implementation period. The license expires 31/12/2025 and signing
  is September 2025. Does this application PASS or FAIL this
  requirement? One word first, then explain."

EXPECTED RESULT:
  Prompt 1: general — AI returns overview without checking the license timeline
  Prompt 2: FAIL — clear reasoning about expiry during implementation

**TRAINER TALKING POINT:**
  "Same AI. Same documents. Different prompt — completely different
  result. This is why prompt engineering is a professional skill,
  not a trick. In government work, catching every compliance detail
  matters — and AI can help double-check. The quality of your
  question determines the quality of the answer."

#### STAGE 3B — RAG vs DIRECT: WHY ARCHITECTURE MATTERS (3 min)
WHAT TO SHOW:
  Live comparison — same question, same model, two different methods

#### STEP 1: Ask AnythingLLM (RAG mode):
  Open AnythingLLM → JEDCO Application Review workspace
  TYPE: "What is the minimum number of employees required for the
         Tattweer program?"

  EXPECTED: Partial result — AnythingLLM retrieves most similar
  chunks, which may not include the specific section needed.
  (Tested result: "Not found in the provided context" — even
  though the answer IS in the uploaded document)

#### STEP 2: Run direct Ollama pipeline:
  python tools/evaluate-pipeline.py --model qwen3:8b --limit 2

  EXPECTED: Catches license issue, correct scoring, precise answers
  because the FULL criteria text is injected into every prompt.

**TRAINER TALKING POINT:**
  "Look at what just happened. Same model — qwen3:8b. Same
  document. Two different results.

  AnythingLLM uses RAG: it splits the document into small chunks
  and retrieves the most 'similar' ones. If the relevant chunk
  isn't retrieved, the AI simply doesn't have the answer.

  The direct pipeline injects the FULL criteria into every prompt.
  The AI sees everything — and catches what matters.

  This is a core AI engineering decision. For JEDCO grant review,
  where every eligibility clause matters, architecture choice
  is something JEDCO’s technical and program teams should
  evaluate together."

  "AnythingLLM is excellent for staff Q&A and exploration.
  For AI-assisted compliance checks that officers review,
  direct injection gives more reliable results."

#### STAGE 4 — AUTOMATED RANKING CONCEPT (3 min)
WHAT TO SHOW:
  Explain the ranking pipeline (no live demo needed — use diagram)

SAY THIS:
  "Imagine 4,000 applications. Each one goes through an initial
  AI pre-check of documents and eligibility. Officers review
  all flagged items. The system produces a baseline ranked list
  sorted by score for the committee to review.

  Staff now focus their expertise on the cases that matter most —
  the ones where professional judgment makes the real difference."

PIPELINE VISUAL (draw or show):
  4,000 apps
    → AI document pre-check (officer reviews flags) → ~3,400 pass
    → AI baseline score (officer validates) → ranked list
    → Top 40: INVITE (committee-approved)
    → Middle 200: DETAILED OFFICER REVIEW (expert judgment)
    → Remainder: AI drafts response, officer batch-reviews before sending

#### STAGE 5 — PROGRESS REPORTING AUTOMATION (3 min)
WHAT TO SHOW:
  Open n8n OR describe the workflow concept

SAY THIS:
  "Once contracts are signed, the pipeline continues. Every 4 weeks,
  the system automatically sends a progress report request to each
  beneficiary. When they submit, the AI reads it and checks:
  - Are milestones on track per the Action Plan?
  - Is financial spend in line with the approved budget?
  - Are there any red flags requiring a field visit?

  The officer receives a one-page summary per project — not a
  stack of 40 manual reports to read."

SAMPLE PROMPT (show in AnythingLLM):
  "You are a JEDCO monitoring officer. The Zahraa Textiles project
  is in month 3. They report: machines installed, ERP delayed by
  2 weeks, first training session completed. Budget spent: 18,000
  JOD of 35,000 JOD approved. Is this project on track?
  Flag any risks. Output: ON TRACK / AT RISK / CRITICAL"

#### STAGE 6 — PROGRAM CLOSURE EVALUATION (2 min)
WHAT TO SHOW:
  Final evaluation concept

SAMPLE PROMPT:
  "You are a JEDCO evaluator at program closure for Zahraa Textiles.
  Original targets: 6 new jobs, 1800 units/month production,
  ISO 9001 certification, first Saudi export shipment.
  
  Actual results: 5 new jobs, 1600 units/month, ISO pending,
  export shipment completed.
  
  Financial: 33,500 JOD of 35,000 JOD disbursed.
  
  Score overall project completion (%) and financial completion (%).
  Recommend: FULL CLOSURE / PARTIAL CLOSURE / FLAG FOR AUDIT"

**TRAINER TALKING POINT:**
  "The AI produces a consistent closure assessment for every project.
  Staff validate and sign off. The audit trail is complete and
  every project gets the same thorough review."

CLOSING MESSAGE (1 min)
"Everything you just saw ran on this laptop.
No internet connection. No cloud. No subscription.
Your documents never left this room.

This is what AI-assisted work looks like in 2026.
AI is a tool JEDCO staff can choose to use when it helps.
The key skill is knowing how to ask the right questions —
and that’s something JEDCO evaluators already excel at."

### Demo Files Used
- assets/jedco-docs/mock-application-tattweer-AR.txt
- assets/jedco-docs/mock-application-start-business-AR.txt
- assets/jedco-docs/JEDCO-eligibility-criteria-reference.txt
- Tool: AnythingLLM + Ollama qwen3:8b (local, thinking mode enabled)
- Fallback model: qwen2.5:7b

KEY DEMO INSIGHT (Stage 3B):
  AnythingLLM (RAG) missed minimum employee count → "Not found"
  Direct Ollama pipeline (full context injection) → "Minimum 5 employees"
  Same model. Same document. Architecture determines accuracy.
