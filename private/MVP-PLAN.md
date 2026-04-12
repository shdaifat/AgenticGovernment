# MVP Implementation Plan — Agentic Government

## What We're Building
A web app with two screens:

**Screen 1: Build Your Rules**
Upload program documents → AI extracts rules → chat to refine → test with mock data

**Screen 2: Evaluate Applications**
Upload applicant documents → AI evaluates against rules → see report → download

---

## File Structure

```
mvp/
├── app.py                          # FastAPI backend (all endpoints)
├── ai.py                           # Azure OpenAI + Ollama caller (swap layer)
├── pdf.py                          # PDF text extraction with page markers
├── pipeline.py                     # Evaluation pipeline (ported from evaluate-pipeline.py)
├── static/
│   └── index.html                  # Single-page app (2 tabs, Arabic RTL)
├── system/
│   └── skills/
│       ├── rule-extraction.md      # How to read source docs and extract structured rules
│       ├── evaluation.md           # How to evaluate: citations, confidence, counter-arguments
│       └── mock-generation.md      # How to generate realistic test applications
├── projects/                       # Runtime: user project data (gitignored)
│   └── {project-id}/
│       ├── sources/                # Uploaded source docs (laws, guidelines)
│       ├── rules.md                # AI-generated rules
│       ├── skills.md               # AI-generated program-specific skills
│       ├── applications/           # Uploaded applicant docs
│       └── results/                # Evaluation outputs (JSON, HTML, Excel)
├── requirements.txt
├── Dockerfile
├── .env.example                    # AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, etc.
└── README.md
```

---

## Build Order (7 Steps)

### Step 1: System Skills (the brain)
Write the 3 system prompt files that drive all AI behavior.

**`system/skills/rule-extraction.md`**
```
Input: raw text from uploaded source documents (laws, guidelines, presentations)
Task: extract ALL evaluation rules as structured markdown

For each rule found, output:
## Rule N: [name in Arabic]
- Type: pass/fail | scored (0-10) | scored (0-N)
- Prompt: "[the exact question to ask when evaluating an application]"
- Evidence: [which document types to look in]
- Weight: [1-5, how important]
- Source: [filename, page number where this rule was found]
- Notes: [any edge cases or clarifications]

Instructions:
- Read the ENTIRE document before extracting rules
- Distinguish between hard eligibility rules (pass/fail) and quality scoring criteria
- Preserve the original Arabic wording for rule names
- Include the page reference for traceability
- If a rule is ambiguous, note it and suggest two interpretations
- Output ALL rules — don't summarize or skip any
```

**`system/skills/evaluation.md`**
```
Input: rules.md + all applicant documents (with page markers)
Task: evaluate each rule and produce structured JSON

For each rule, output:
{
  "rule_id": "Rule N",
  "rule_name": "[Arabic name]",
  "verdict": "PASS | FAIL | NEEDS_REVIEW",
  "score": null or 0-N,
  "reasoning": "[Arabic explanation, 2-3 sentences]",
  "confidence": 0-100,
  "citations": [
    {"file": "filename.pdf", "page": N, "excerpt": "[exact quoted text]"}
  ],
  "counter_argument": "[alternative interpretation, 1 sentence]",
  "missing_evidence": "[what document/info would help, or null]"
}

Instructions:
- For each rule, search ALL documents for relevant evidence
- Quote exact text from documents — don't paraphrase
- Page references must be exact (from --- [file] Page N --- markers)
- Confidence 90+ = clear evidence found, no ambiguity
- Confidence 50-89 = evidence found but interpretation needed
- Confidence <50 = evidence weak or missing, mark NEEDS_REVIEW
- If you need to calculate dates, numbers, or comparisons — say so explicitly
  (the system will run code to verify your calculation)
- Counter-argument: always give the opposing interpretation
- NEVER make up citations — if you can't find evidence, say so
```

**`system/skills/mock-generation.md`**
```
Input: rules.md (the program's evaluation rules)
Task: generate N realistic mock applications in Arabic

For each mock, output:
{
  "id": "MOCK-XXX",
  "expected_result": "PASS | FAIL | BORDERLINE",
  "deliberate_flaw": "[description or null]",
  "applicant_name": "[realistic Arabic name]",
  "company_name": "[realistic Arabic company name]",
  "application_text": "[full application text in Arabic with realistic details]"
}

Instructions:
- Generate a mix: ~40% should pass, ~30% should fail, ~30% borderline
- For FAIL cases, include exactly ONE deliberate flaw that violates a specific rule
- Make details realistic: Jordanian company names, JOD amounts, real sectors
- Include dates, registration numbers, financial figures
- Each mock should be 300-500 words in Arabic
- DO NOT make flaws obvious — a human reviewer should need to think about it
```

**Files to create**: 3 markdown files in `mvp/system/skills/`

---

### Step 2: AI Caller Layer (`ai.py`)
Thin wrapper that calls either Azure OpenAI or Ollama with the same interface.

```python
# Core function signature:
async def chat(
    system_prompt: str,
    user_message: str,
    model: str = None,          # None = use default from .env
    temperature: float = 0.1,
    max_tokens: int = 2000,
    stream: bool = False,       # For chat UI streaming
) -> str | AsyncGenerator:

# Config from .env:
# AI_PROVIDER=azure          # or "ollama"
# AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com
# AZURE_OPENAI_KEY=xxx
# AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
# OLLAMA_URL=http://localhost:11434
# OLLAMA_MODEL=qwen3:8b
```

**Key**: Same interface, swap provider with one env var. Demo runs on Azure OpenAI. Dev/local runs on Ollama.

**Reuse from**: `evaluate-pipeline.py` → `call_ollama()` function. Add `call_azure_openai()` using `openai` Python SDK.

---

### Step 3: PDF Extraction (`pdf.py`)
Extract text from uploaded PDFs with page markers.

```python
async def extract_text(file_path: str) -> str:
    """
    Returns text with page markers:
    --- [filename.pdf] Page 1 ---
    Text of page 1...
    --- [filename.pdf] Page 2 ---
    Text of page 2...
    """

# Two backends:
# 1. PyMuPDF (fitz) — free, works locally, good for digital PDFs
# 2. Azure Document Intelligence — Arabic OCR, scanned docs ($0.01/page)
#    Use when PyMuPDF returns too little text (scanned document detection)
```

**Packages**: `pymupdf` (primary), `azure-ai-documentintelligence` (fallback for scanned).

---

### Step 4: Pipeline (`pipeline.py`)
Port the evaluation logic from `evaluate-pipeline.py` to use the new components.

```python
async def extract_rules(project_id: str) -> str:
    """Read source docs → call AI with rule-extraction skill → save rules.md"""
    sources_text = load_all_sources(project_id)   # pdf.py
    skill = load_skill("rule-extraction.md")
    rules_md = await ai.chat(skill, sources_text)
    save_rules(project_id, rules_md)
    return rules_md

async def generate_mocks(project_id: str, count: int = 5) -> list:
    """Read rules.md → call AI with mock-generation skill → save mock apps"""
    rules = load_rules(project_id)
    skill = load_skill("mock-generation.md")
    mocks = await ai.chat(skill, f"Rules:\n{rules}\n\nGenerate {count} mock applications.")
    save_mocks(project_id, mocks)
    return mocks

async def evaluate_application(project_id: str, app_text: str) -> dict:
    """Rules.md + app documents → call AI with evaluation skill → structured result"""
    rules = load_rules(project_id)
    skill = load_skill("evaluation.md")
    prompt = f"=== Rules ===\n{rules}\n\n=== Application Documents ===\n{app_text}"
    result = await ai.chat(skill, prompt, temperature=0.1)
    return parse_evaluation(result)

async def evaluate_batch(project_id: str) -> list:
    """Run evaluate_application for all uploaded apps"""
    # Reuse logic from evaluate-pipeline.py main loop
```

**Reuse from**: `evaluate-pipeline.py` → `run_stage1()`, `run_stage2()`, `parse_stage1()`, `parse_stage2()`, `write_html_report()`

Major changes:
- Merge stage1 + stage2 into one evaluation pass per rule (not per stage)
- Use `rules.md` instead of hardcoded JEDCO prompts
- Add citation extraction from page markers
- async throughout

---

### Step 5: FastAPI Backend (`app.py`)
All API endpoints.

```
POST /api/projects                          → Create new project
GET  /api/projects/{id}                     → Get project info + status

POST /api/projects/{id}/sources             → Upload source documents
POST /api/projects/{id}/extract-rules       → AI extracts rules from sources
GET  /api/projects/{id}/rules               → Get current rules.md
PUT  /api/projects/{id}/rules               → Save edited rules.md

POST /api/projects/{id}/chat                → Chat to refine rules (SSE streaming)

POST /api/projects/{id}/generate-mocks      → Generate mock applications
POST /api/projects/{id}/test-rules          → Run pipeline against mocks
GET  /api/projects/{id}/test-results        → Get test results

POST /api/projects/{id}/applications        → Upload real applications
POST /api/projects/{id}/evaluate            → Run full evaluation pipeline
GET  /api/projects/{id}/results             → Get evaluation results
GET  /api/projects/{id}/results/export      → Download HTML or Excel

GET  /                                      → Serve index.html
```

**No auth for MVP**. Project ID is a UUID. Share the URL with the customer.

---

### Step 6: Frontend (`static/index.html`)
Single HTML file, two tabs.

**Tab 1: بناء القواعد (Build Rules)**
```
┌─────────────────────────────────────────────────────────┐
│  📁 ارفع وثائق البرنامج (قوانين، أنظمة، تعليمات)        │
│  [Upload Zone — drag & drop PDFs]                       │
│                                                         │
│  [استخرج القواعد]  ← button, calls /extract-rules      │
│                                                         │
│  ┌─────────────────────┬───────────────────────────────┐│
│  │                     │                               ││
│  │   💬 Chat           │   📄 rules.md                 ││
│  │                     │                               ││
│  │   "غير القاعدة 3"   │   ## Rule 1: سجل تجاري...     ││
│  │   "أضف شرط..."     │   ## Rule 2: عمر الشركة...     ││
│  │                     │   ## Rule 3: ...               ││
│  │                     │                               ││
│  └─────────────────────┴───────────────────────────────┘│
│                                                         │
│  [اصنع بيانات تجريبية]  [جرّب القواعد]                  │
│                                                         │
│  Test Results Table (if test was run)                    │
└─────────────────────────────────────────────────────────┘
```

**Tab 2: تقييم الطلبات (Evaluate Applications)**
```
┌─────────────────────────────────────────────────────────┐
│  📁 ارفع وثائق المتقدمين                                │
│  [Upload Zone — multiple applicant PDF bundles]         │
│                                                         │
│  [قيّم الطلبات]  ← button, calls /evaluate             │
│                                                         │
│  Progress bar (when running)                            │
│                                                         │
│  Results Table:                                         │
│  # │ المتقدم │ الدرجة │ التوصية │ نقاط القوة │ المخاوف  │
│  ──┼─────────┼────────┼────────┼───────────┼──────────│
│  1 │ أحمد... │  78    │ مقبول  │ ...       │ ...      │
│  2 │ سارة... │  45    │ مرفوض  │ ...       │ ...      │
│                                                         │
│  Click any row → expand: per-rule breakdown + citations │
│                                                         │
│  [تحميل HTML]  [تحميل Excel]                            │
└─────────────────────────────────────────────────────────┘
```

**Tech**: Vanilla HTML + CSS + JS. No React, no build step. Arabic RTL. Fetch API for endpoints, EventSource for streaming chat. Markdown rendering with a small library (marked.js).

---

### Step 7: Deploy to Azure

```bash
# One-time setup
az group create -n agentic-gov-demo -l eastus
az webapp up -n agentic-gov-demo -g agentic-gov-demo --runtime PYTHON:3.12

# Or Docker
docker build -t agentic-gov-mvp .
az containerapp up -n agentic-gov -g agentic-gov-demo --image agentic-gov-mvp
```

**Azure resources needed:**
| Resource | Purpose | Cost |
|----------|---------|------|
| Azure App Service (B1) | Host the web app | ~$13/month |
| Azure OpenAI (GPT-4o-mini) | AI calls | Pay per use (~$0.15/1M input) |
| Azure Blob Storage | Uploaded documents | ~$0.02/GB/month |
| Azure Document Intelligence (optional) | Arabic OCR for scanned PDFs | $0.01/page |

**Total for demo**: ~$15/month + a few dollars in AI usage.

---

## Reuse Map from evaluate-pipeline.py

| Existing Code | Reuse In | Changes |
|--------------|----------|---------|
| `SYSTEM_PROMPT` | `system/skills/evaluation.md` | Expand with citation format |
| `STAGE1_ADMIN_PROMPT` | Absorbed into rules.md per-rule prompts | No longer hardcoded |
| `STAGE2_SCORING_PROMPT` | Absorbed into rules.md per-rule prompts | No longer hardcoded |
| `call_ollama()` | `ai.py` | Add Azure OpenAI option |
| `parse_stage1()`, `parse_stage2()` | `pipeline.py` | Merge into single per-rule parser |
| `write_html_report()` | `pipeline.py` or `app.py` export endpoint | Adapt for per-rule citations |
| `load_applications()` | `app.py` upload endpoint | From files → from HTTP upload |
| `load_criteria()` | Replaced by `rules.md` | Dynamic, not static file |

---

## What's NOT in MVP

- No login / auth (just share URL)
- No applicant self-service portal
- No reviewer workflow (accept/override per rule)
- No status tracking
- No voice (ASR)
- No community Q&A
- No code execution (pure LLM evaluation only)
- No database (file system + JSON only)
- No multi-tenant (one project at a time is fine for demo)

---

## Definition of Done

MVP is done when:
1. Customer opens URL
2. Uploads their program's law/guidelines PDF
3. AI extracts rules, customer refines via chat
4. Customer generates mock applications, tests rules
5. Customer uploads real applicant PDFs
6. Gets ranked evaluation report with per-rule verdicts and citations
7. Downloads report as HTML
