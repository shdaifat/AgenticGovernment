# Agentic Government — Product Roadmap

## Vision
A generic AI platform where any government entity can define program rules, receive applications, and get AI-powered evaluation reports with document-level citations — so decisions are faster, fairer, and transparent.

---

## Business Model — Pay Per Use

### Pricing (Azure-Hosted)
Customers who use the cloud-hosted version on Azure pay **only for what they use** — no subscription, no seat licenses.

| What | Cost Driver | Estimated |
|------|------------|----------|
| Application evaluation | AI tokens consumed per evaluation | ~$0.05–$0.50 per application (depends on # of rules × # of documents) |
| Document processing (OCR) | Pages processed via Azure Document Intelligence | ~$0.01 per page |
| Storage | Uploaded documents stored on Azure Blob | ~$0.02 per GB/month |
| Rule testing | AI tokens during prompt experimentation | ~$0.01–$0.05 per test run |
| Applicant AI chat | AI tokens per chat message | ~$0.005 per message |
| Mock application generation | AI tokens to generate test data | ~$0.02–$0.10 per mock app |

**No platform fee. No monthly minimum. Pay only when AI runs.**

### Per-User Cost Tracking (Azure)
Azure provides **exact usage tracking per user and per application**:
- Every AI call is tagged with: `user_id`, `program_id`, `application_id`, `action_type`
- Azure API Management + Application Insights tracks tokens consumed per request
- Manager dashboard shows: "User X consumed $3.42 this month across 12 evaluations"
- Budget limits per user, per program, or per organization (auto-pause when exceeded)
- Monthly invoice breakdown: which department used how much AI, on which programs
- Azure Cost Management APIs feed directly into our reporting

### Free Tier — Local Deployment
- Customer hosts the system on their own servers
- Uses Ollama (free, open-source) instead of Azure OpenAI
- **Zero cost** — only hardware and electricity
- Same features, same interface, just local models

### Revenue Summary
| Deployment | AI Cost | Platform Fee | Total |
|-----------|---------|-------------|-------|
| Azure cloud (our hosting) | Pay per use | $0 | Usage-based |
| Customer Azure + our AI | Pay per use | $0 | Usage-based |
| Customer Azure + their Ollama | $0 | $0 | Free |
| Fully local (their servers) | $0 | $0 | Free |

The model is: **we make money when customers use Azure OpenAI through our platform**. Customers who go fully local pay nothing. This removes adoption barriers for governments.

---

## Phase 1 — Smart Applicant Portal

### 1.1 Document Upload & AI Chat
- Applicant uploads documents (PDF, images, Word) to the system
- AI reads all uploaded documents immediately (OCR for scanned, Arabic support)
- Applicant can **chat with the system** about their documents:
  - "هل وثائقي مكتملة؟" → AI checks what's uploaded vs what's typically needed
  - "ما هي البرامج المناسبة لي؟" → AI suggests matching programs based on uploaded docs
  - "هل أنا مؤهل لبرنامج ارفع قدراتك؟" → AI does a pre-check against program rules

### 1.2 Program Discovery
- Applicant sees a catalog of active government programs
- Each program shows: name, description, deadline, required documents, eligibility summary
- AI-powered **program matching**: based on uploaded documents, system ranks which programs the applicant is most likely eligible for
- Applicant selects a program to apply to

### 1.3 Pre-Submission Intelligence
- Before submitting, AI analyzes the application and tells the applicant:
  - ✅ **Strong points**: "Your commercial registration is valid until 2027"
  - ⚠️ **Missing documents**: "Program requires financial statements — not found in your uploads"
  - 🔴 **Potential blockers**: "Your business was registered less than 1 year ago — minimum is 2 years"
  - 📊 **Readiness score**: Overall percentage of how complete/strong the application is
- Applicant can upload more documents and re-check until satisfied

### 1.4 Smart Form-Filling
- Applicant selects a program → system shows the application form
- AI **reads the uploaded documents and auto-fills the form**:
  - Extracts company name, registration number, date from commercial registration PDF
  - Extracts financial figures from financial statements
  - Extracts owner name, national ID from uploaded ID documents
- Applicant reviews auto-filled fields, corrects if needed, fills remaining fields manually
- Saves time: instead of typing everything twice, the documents speak for themselves

### 1.5 Application Submission
- Applicant submits the final application
- System records: all documents, form fields, submission timestamp, readiness score
- Applicant gets a tracking number and can check status anytime
- Notifications via email/SMS on status changes

### 1.6 Application Status & Results Transparency
Applicant should never wonder "what's happening with my application?" — full visibility:

**Live Status Tracking:**
- Visual timeline showing every stage: Submitted → Documents Verified → Under AI Review → Under Human Review → Decision Made
- Each stage shows: date entered, estimated time remaining, who is handling it
- Push notifications on every stage change (email + SMS + in-app)

**Results Transparency (after decision):**
- Applicant sees the **full evaluation report** — not just "approved" or "rejected"
- Per-rule breakdown: which rules passed ✅, which failed ❌, which were borderline ⚠️
- AI reasoning shown in plain Arabic: "تم رفض الطلب لأن السجل التجاري منتهي الصلاحية بتاريخ 2024/06/15"
- Citations visible: applicant can see WHICH document and WHICH page the decision was based on
- Confidence levels shown: "AI was 95% confident about this rule" vs "AI was only 40% sure"
- If overridden by human reviewer: "المراجع غيّر القرار من رفض إلى قبول مشروط" with reviewer's reasoning
- **What to improve**: if rejected, system tells applicant exactly what to fix:
  - "أعد تقديم سجل تجاري ساري المفعول" (resubmit valid commercial registration)
  - "القوائم المالية ناقصة — أرفق كشف حساب آخر 6 أشهر" (financials incomplete — attach last 6 months bank statement)
- Comparison with successful applications (anonymized): "Applications that pass this program typically have X, Y, Z"

**Why transparency matters:**
- Builds trust in AI-assisted government decisions
- Reduces appeals (applicant already understands the reasoning)
- Applicant can fix and reapply with clear guidance
- Meets emerging government AI transparency regulations

---

## Phase 2 — Rules Studio (Program Admin)

### 2.0 Guided Onboarding — Teaching the Rule Maker
The rule maker ("prompt programmer") does NOT need technical skills. The system **teaches them** through conversation.

**Step 0: Upload Source Documents (Laws, Guidelines, Presentations)**
- Rule maker can upload the **source material** the rules come from:
  - PDF of the official program guidelines or regulations
  - Law text or legal framework document
  - PowerPoint presentation describing the program
  - Word document with eligibility criteria
  - Even a photo of a printed brochure
- AI reads ALL uploaded source documents and says:
  - "قرأت الوثائق. وجدت 8 شروط أهلية و 4 معايير تقييم. هل تريدني أبني القواعد منها؟"
  - ("I read the documents. Found 8 eligibility conditions and 4 evaluation criteria. Shall I build the rules from them?")
- AI extracts rules automatically from law books, regulations, guidelines
- Rule maker reviews, approves, or modifies each extracted rule through chat
- Source document page references are preserved: "Rule extracted from guidelines.pdf, page 12"

**Step 1: Introduction Chat**
- New rule maker opens the Rules Studio for the first time
- System greets them and starts a guided conversation:
  - "مرحباً! أنا مساعدك في بناء قواعد التقييم. أخبرني عن البرنامج الذي تريد إنشاءه — ما اسمه؟ ما هدفه؟"
  - User describes the program in plain Arabic
  - AI asks follow-up questions: "ما هي الشروط الأساسية للقبول؟", "هل هناك وثائق مطلوبة؟"
- OR if source documents were uploaded in Step 0, AI already has the rules and starts refining them

**Step 2: AI Builds the Rules .md File**
- As the rule maker talks, AI generates a **rules markdown file** automatically:
  ```markdown
  # برنامج ارفع قدراتك بالتسويق — قواعد التقييم
  
  ## Rule 1: سجل تجاري ساري المفعول
  - Type: pass/fail
  - Prompt: "تحقق من وجود سجل تجاري ساري المفعول في وثائق المتقدم..."
  - Evidence: commercial_registration
  - Weight: 3
  
  ## Rule 2: عمر الشركة أكثر من سنتين
  - Type: pass/fail
  - Prompt: "احسب عمر الشركة من تاريخ التأسيس..."
  - Evidence: commercial_registration, company_profile
  - Weight: 2
  ```
- Rule maker sees the `.md` file being built live as they chat
- They can say "عدل القاعدة الثانية" and AI updates the file instantly

**Step 3: AI Builds the Skills .md File**
- System also generates a **skills file** — how the AI should behave when evaluating:
  ```markdown
  # Skills: برنامج ارفع قدراتك بالتسويق
  
  ## Document Reading
  - Language: Arabic
  - Date format: DD/MM/YYYY (Jordanian standard)
  - Currency: JOD
  
  ## Evaluation Style
  - Be strict on eligibility rules (pass/fail)
  - Be lenient on quality rules (scored 0-10)
  - Always cite the exact page and document
  - When uncertain, mark as "Needs Review" not "Fail"
  
  ## Domain Knowledge
  - JEDCO programs target SMEs in Jordan
  - Commercial registration is issued by Ministry of Industry
  - Valid registration must show expiry date in the future
  ```
- These skills teach the AI **how to think** about this specific program
- Rule maker refines skills through chat: "خلي النظام يكون صارم أكثر على الشروط المالية"

**Step 4: Test & Iterate**
- System asks: "هل عندك طلب نموذجي نجرب عليه؟" (do you have a sample application?)
- **Option A**: Rule maker uploads a real sample → AI evaluates using `rules.md` + `skills.md`
- **Option B**: No sample? System **generates mock applications using a different LLM**:
  - System uses a separate AI model (e.g., Ollama/Gemini) to create realistic fake applications
  - Generates 3-5 mocks: some that should pass, some that should fail, some borderline
  - Mock includes fake PDFs with realistic Arabic content (names, numbers, dates)
  - This way the rule maker can test without needing real applicant data
  - Different LLM used for generation vs evaluation — avoids bias (can't grade its own homework)
- Rule maker sees results and says: "القاعدة الثالثة ما اشتغلت صح" → AI fixes it
- Loop continues until rule maker is satisfied
- Every version of the `.md` files is saved (full history)

**Key Principle: The `.md` files ARE the program configuration.**
No database forms. No complex UI. Just markdown files that a human can read and an AI can execute. The chat interface is just a friendly way to create and edit these files.

### 2.1 AI-Assisted Rule Creation
- Program admin creates a new program (name, description, deadline, budget)
- Admin defines evaluation rules by **chatting with AI in Arabic**:
  - Admin: "المتقدم لازم يكون عنده سجل تجاري ساري المفعول"
  - AI: Creates structured rule → { name, prompt, scoring: pass/fail, evidence_type }
  - Admin: "وكمان عمر الشركة لازم يكون أكثر من سنتين"
  - AI: Creates another rule with scoring logic
- Admin can refine any rule through continued conversation
- **Output: `rules.md` file** — human-readable, AI-executable

### 2.2 Rule Testing & Experimentation
- Admin uploads a **sample application** (real or mock)
- Clicks "Test All Rules" → AI evaluates the sample using the `rules.md` + `skills.md` files
- Admin sees how each rule performed: did it find the right evidence? correct verdict?
- Admin can tweak rules through chat and re-test until satisfied (experiment loop)
- Version history: every change to `.md` files is tracked with diff view
- Cost shown per test run (tokens used) — so admin knows what each evaluation costs

### 2.3 Program Configuration
- Required documents checklist (what applicant must upload)
- Custom form fields per program (text, number, date, dropdown, file)
- Scoring weights: which rules matter more (defined in `rules.md`)
- Evaluation mode: pass/fail per rule, or scored (0-10) per rule, or hybrid
- Deadline management, application limits, reviewer assignment
- All configuration stored as readable `.md` files (not hidden in database)

### 2.4 Rule Templates & Sharing
- Common rules as template `.md` files: "Valid commercial registration", "Minimum capital", "Jordanian ownership"
- Admin can import a template `.md` file and customize it through chat
- Programs can inherit rules from other programs (fork the `.md` file & modify)
- **Community library**: government entities can share rule templates with each other

---

## Phase 3 — AI Evaluation Engine

### 3.1 Document Processing Pipeline
- All applicant documents extracted with page-level tracking:
  `--- [commercial_registration.pdf] Page 1 ---`
- Arabic OCR via Azure Document Intelligence (production) or PDF.js (local)
- Table extraction, handwriting recognition for government forms
- Document classification: AI auto-detects document type (registration, financial, ID, etc.)

### 3.2 Per-Rule AI Evaluation
- For each rule, AI receives: rule definition + all applicant documents + program context
- AI produces structured output per rule:
  - **Verdict**: Pass / Fail / Needs Review
  - **Reasoning** (Arabic): Why this verdict was reached
  - **Confidence**: 0-100% (how certain the AI is)
  - **Citations**: Exact file name + page number + quoted text from document
  - **Counter-argument**: Alternative interpretation (like NOFA)
  - **Missing evidence**: What document/info would be needed if verdict is uncertain

### 3.2.1 Evaluation-Time Code Execution
LLMs are bad at math, dates, and lookups. During evaluation, the agent can **write and run code** to get exact answers:

- **Date calculations**: "Is commercial registration expired?" → agent writes Python:
  ```python
  from datetime import date
  expiry = date(2025, 3, 15)  # extracted from PDF
  today = date.today()
  is_valid = expiry > today  # True/False, no hallucination
  ```
- **Financial math**: "Is revenue above 50,000 JOD?" → agent parses financial table, sums values in code
- **Cross-document checks**: "Does the name on the ID match the name on the registration?" → string comparison in code
- **Age/duration**: "Is company older than 2 years?" → exact date arithmetic
- **Regex validation**: "Is the registration number in correct format?" → regex match
- **API calls**: agent can call external APIs during evaluation:
  - Verify commercial registration number against MoIT database
  - Check blacklist/sanctions databases
  - Pull exchange rates for foreign currency amounts

**How it works:**
- Agent decides per-rule whether it needs code (most rules are pure LLM, some need code)
- Code runs in a **sandboxed Python environment** (no file system access, no network except whitelisted APIs)
- Code output feeds back into AI reasoning: "I calculated expiry is 2025-03-15, which is in the past. FAIL."
- Rule maker can define custom validation scripts in `rules.md`:
  ```markdown
  ## Rule 5: Capital above 10,000 JOD
  - Code: extract_number(documents, "رأس المال") > 10000
  ```
- All code execution is logged (what ran, input, output) for audit trail
- Works locally too — Python sandbox runs on same server, no cloud dependency

### 3.3 Overall Evaluation Report
- Summary recommendation: Approve / Reject / Conditional / Needs More Info
- Overall confidence score (weighted average of per-rule confidence)
- Strengths summary (rules clearly met)
- Weaknesses summary (rules failed or uncertain)
- Red flags: critical issues requiring human attention
- Cost estimate per evaluation (tokens used, API cost)

### 3.4 Report Export — Multiple Formats
- AI generates evaluation report in the **format the user needs**:
  - **HTML**: Interactive report with clickable citations, expandable sections, embedded PDF viewer
  - **Excel**: Structured spreadsheet — one row per rule, columns for verdict/confidence/citations/reasoning
  - **PDF**: Printable official report with government letterhead template
  - **Word**: Editable report for manual additions before official signing
  - **JSON**: Machine-readable for integration with other systems
- Format is configurable per program (admin sets default) and per export (reviewer can choose)
- Prompt controls the output: `skills.md` defines report template, tone, sections, language

### 3.5 Batch Evaluation
- Process multiple applications in parallel
- Progress tracking with estimated completion time
- Priority queue: urgent applications first
- Rate limiting and cost controls

---

## Phase 4 — Reviewer Interface

### 4.1 Case Review Dashboard
- Reviewer sees list of assigned cases with: applicant name, program, submission date, AI recommendation, confidence level
- Sort/filter by: confidence level, recommendation, date, program
- Color-coded: 🟢 High confidence approve, 🟡 Needs review, 🔴 High confidence reject

### 4.2 Detailed Case Review
- Full AI evaluation report with per-rule breakdown
- Each rule shows: verdict, reasoning, confidence, citations
- **Click any citation** → PDF viewer opens to exact page with excerpt highlighted
- Side-by-side view: AI report on left, document viewer on right
- Counter-arguments displayed for each rule (reviewer sees both sides)

### 4.3 Human Decision Making
- Reviewer can **accept** AI recommendation per rule (one-click)
- Reviewer can **override** any rule verdict (must provide written reasoning)
- Reviewer can **request more info** from applicant (triggers notification)
- Reviewer can **escalate** to senior reviewer or manager
- All reviewer actions logged with timestamp for audit trail

### 4.4 Reviewer AI Assistant
- Reviewer can ask AI questions about the case:
  - "قارن هذا الطلب مع الطلبات المشابهة" (compare with similar applications)
  - "ما هي المخاطر الرئيسية؟" (what are the main risks?)
  - "هل هناك تناقض بين الوثائق؟" (are there contradictions between documents?)
- AI answers with citations from the applicant's documents

### 4.5 Applicant Feedback & Dispute
When results are shared with applicants (Phase 1.6), they can flag specific rules they believe were evaluated incorrectly:

- Applicant clicks **"أعترض على هذه النتيجة"** (I dispute this result) on any rule verdict
- Must provide a written reason (Arabic text) + optional supporting document
- System creates a **dispute case** linked to the original evaluation
- Assigned to a **different reviewer** (not the one who made the original decision)
- Dispute reviewer sees: original evaluation + applicant's counter-argument + all documents
- Resolution: **Upheld** (original stands), **Revised** (change verdict), **Escalated** (needs manager)
- Full dispute history stored: who disputed, when, what changed, who decided
- Aggregated dispute stats feed into Phase 5 analytics (which rules get disputed most?)

This is not a full legal appeal — it's a lightweight "second look" within the system. Legal appeals (external process) are a deployment-time policy decision, not a software feature.

### 4.6 Decision Confidence Calibration
- Track how often AI confidence matches actual human decisions over time
- If AI says 95% confident PASS but reviewers override 20% of the time → system flags this rule as **poorly calibrated**
- Dashboard shows calibration chart: AI confidence vs. actual reviewer agreement rate
- Helps rule makers improve rule wording ("Rule 3 is too vague — 40% override rate")

---

## Phase 5 — Manager Dashboard

### 5.1 Program Analytics
- Applications per program: received, in review, approved, rejected
- Average processing time per program
- AI accuracy: how often reviewers agree with AI recommendation
- Confidence distribution: histogram of AI confidence scores
- Cost tracking: total evaluation cost per program

### 5.2 Reviewer Performance
- Cases per reviewer, average review time
- Override rate: how often reviewer changes AI verdict (by rule)
- Consistency score: how consistent are different reviewers on similar cases

### 5.3 Decision Reports
- Exportable reports for management (PDF, Excel)
- Aggregated statistics per program, period, reviewer
- Audit trail: who decided what, when, with what reasoning
- Compliance report: every decision is traceable to rules + evidence + human judgment

### 5.4 System Health
- API usage and costs (tokens, calls, latency)
- Model performance monitoring (confidence calibration)
- Error tracking (failed evaluations, timeout issues)
- Storage usage (uploaded documents)

### 5.5 Rule Health & Outcome Patterns
Rules aren't static — they should get better over time based on real usage:

**Rule Effectiveness Tracker:**
- Per-rule stats: how often each rule results in PASS/FAIL/NEEDS_REVIEW
- **Override rate per rule**: if reviewers override Rule 5 in 30% of cases → rule needs rewriting
- **Dispute rate per rule**: if applicants dispute Rule 3 most often → evidence requirements unclear
- **Confidence calibration**: AI confidence vs. actual human decision (see 4.6)
- Auto-generated alert: "Rule 7 has been overridden 15 times this month — consider revising"

**Outcome Pattern Detection:**
- Aggregated outcome analysis across all evaluated applications
- Flag unexpected patterns: "Applications from [sector X] fail Rule 4 at 3× the average rate"
- Track approval/rejection trends over time (is the program getting stricter or more lenient?)
- Compare outcomes across different AI models (if using multi-model in Phase 6.2)

**Rule Improvement Suggestions:**
- AI analyzes overridden rules + dispute reasons → suggests better wording
- "Rule 3 gets overridden because it doesn't account for companies under 1 year old. Suggestion: add exception for startups"
- Rule maker can accept suggestion (creates new version) or dismiss
- All suggestions logged — builds a knowledge base per program

This turns the system into a **learning loop**: evaluate → review → detect patterns → improve rules → re-evaluate.

### 5.6 Owner AI Assistant — Ask Questions, Get Reports
The system owner can **chat with the AI to get answers and reports** about the system's data — no SQL, no code, just Arabic:

**Examples:**
- "كم طلب استقبلنا هذا الشهر؟" → AI queries DB, returns: "47 طلب — 12 مقبول، 8 مرفوض، 27 قيد المراجعة"
- "ما هي أكثر أسباب الرفض تكراراً؟" → AI generates table/chart from evaluation data
- "أريد تقرير اكسل بكل الطلبات المرفوضة مع أسباب الرفض" → AI builds and downloads Excel file
- "قارن أداء المراجعين هذا الربع" → AI produces comparison table
- "كم صرفنا على الذكاء الاصطناعي الشهر الماضي؟" → AI pulls cost data
- "ما هي القواعد الأكثر اعتراضاً؟" → AI shows rules with highest dispute/override rates
- "هل يوجد نمط غير طبيعي في التقييمات الأخيرة؟" → AI flags statistical anomalies

**Proactive Alerts (push, not just pull):**
- System auto-detects unusual patterns and notifies the owner:
  - "⚠️ Rule 5 override rate jumped from 5% to 25% this week"
  - "⚠️ Average processing time increased 3× for Program X"
  - "⚠️ AI confidence dropped below 50% on 8 applications today — check source documents"
  - "📊 Monthly summary ready: 142 applications processed, 78% approved, $12.40 spent"
- Alerts via: in-app notification, email digest (daily/weekly), or both
- Owner configures which alerts matter (turn off noise, keep critical ones)

**How it works:**
1. Owner types question in Arabic or English
2. AI translates to a **read-only database query** (SELECT only — no INSERT, UPDATE, DELETE)
3. Results shown as: tables, charts, downloadable Excel/PDF, or plain text answer
4. All queries logged for audit trail
5. No code shown to the owner — just the answer (code runs behind the scenes)

**This is read-only by design.** The owner asks questions and gets reports. No data modification, no scripts to review, no scheduling. Simple and safe.

> **Future (Phase 6.10):** Full script automation — write operations, scheduled jobs, migration scripts — with explicit approval flow. Only build this after the read-only assistant proves useful and real usage patterns emerge.

---

## Data Governance & Operational Policies

These aren't software features — they're **deployment-time policies** that each government defines. We provide templates and configuration options:

### Data Retention
- Default: uploaded documents and evaluation results retained for **3 years** (configurable per program)
- Applicant PII anonymized or deleted after retention period expires
- Evaluation metadata (statistics, patterns) kept indefinitely in aggregated/anonymous form
- Configuration: `retention_policy.md` per program — rule maker defines how long data stays

### Data Access & Privacy
- Applicant data only visible to: assigned reviewer + program manager + system admin
- No cross-program data sharing unless explicitly configured by admin
- All data access logged (who viewed what, when)
- Applicant can request data export (their application + evaluation results)
- Applicant can request data deletion (triggers removal + confirmation)

### Audit & Compliance
- **Every decision is traceable**: rule → evidence → AI evaluation → human decision → outcome
- Audit log is append-only (cannot be modified or deleted)
- Exportable audit trail for external compliance review
- Supports GDPR-style "right to explanation" — applicant gets human-readable reasoning per rule

### Deployment Security Baseline
- Authentication: configurable per deployment (none for demo, Azure AD B2C for production, National ID for government)
- Transport: HTTPS required (TLS 1.2+)
- API: rate-limited, key-authenticated for external integrations
- File uploads: virus scanning, file type validation, size limits (configurable)
- AI prompts: system prompts are read-only files (not user-editable at runtime, only by admin)
- Model inputs: applicant data is not stored by Azure OpenAI (data processing agreement required)

> These templates are shipped with the platform. Each deploying government fills in their values. We don't enforce — we enable.

---

## Phase 6 — Advanced Features

### 6.1 Multi-Language Support
- Arabic as primary language (UI, rules, reports, AI reasoning)
- English as secondary language
- Bilingual reports: Arabic + English side by side

### 6.2 Multi-Model Support
- Dropdown to select AI model per program:
  - Azure OpenAI GPT-5-mini (default, best Arabic)
  - Ollama local models (privacy-sensitive cases)
  - Claude, Gemini (alternative providers)
- Model comparison: run same application through 2 models, compare results

### 6.3 Applicant-Reviewer Communication
- Reviewer sends "request for info" → applicant gets notification
- Applicant uploads additional documents or answers questions
- AI re-evaluates affected rules automatically
- Full conversation thread stored per case

### 6.4 Appeal Process
- Rejected applicant can submit a **formal appeal** with new documents or written explanation
- System re-evaluates **only the disputed rules** with new evidence (not the entire application)
- Appeal assigned to a **different reviewer** who has not seen the original case
- Appeal reviewer sees: original evaluation (read-only) + new evidence + appeal reason
- Decision options: **Overturned** (approve), **Partially revised** (change specific rules), **Denied** (original stands)
- If appeal denied, system shows exactly which rules still fail and why
- Appeal decision tracked separately with its own audit trail
- Program manager sees appeal statistics: how many appeals, overturn rate, common reasons
- High overturn rate signals rule problems → feeds into 5.5 Rule Health metrics

### 6.5 Citizen Login & Government ID Integration
- **Login with National ID number** — citizen enters their ID (الرقم الوطني) to access the system
- Integration with government identity APIs:
  - Jordan: SANAD / National Unified Registry API
  - Generic: Any national ID verification endpoint (configurable per country)
- Auto-pull citizen data from government databases (name, DOB, address) — no manual entry
- **For organizations**: Login with commercial registration number, pull company data from MoIT registry
- SSO with government identity providers (Azure AD B2C, Keycloak, SAML)
- Fallback: email + OTP for cases where government API is not available
- All authentication logged for audit trail

### 6.6 Integration & API
- REST API for external systems to submit applications programmatically
- Webhook notifications for status changes
- Integration with national ID verification systems (see 6.5)
- Integration with commercial registry databases (auto-verify registration)
- Integration with payment gateways (if program has application fees)

### 6.7 Community Q&A Forum
- **Public community chat** where users help each other:
  - Applicants ask: "What documents do I need for program X?"
  - Rule makers share tips: "This prompt works better for financial checks"
  - Reviewers discuss: "How do you handle borderline cases?"
- **Fully open-source chat — works locally, no Azure dependency**:
  - Built on open-source real-time stack (e.g., Socket.IO / Matrix / NATS)
  - No Azure Web PubSub, no SignalR Service, no paid messaging
  - Runs on same server as the app — local, LAN, or cloud
  - WebSocket-based: lightweight, standard, works behind any firewall
- AI-assisted answers: system can auto-answer common questions from program `rules.md`
- Tagged by program, role, topic
- Upvote/downvote system — best answers rise to top
- Rule makers can pin official answers
- Searchable knowledge base built from Q&A history
- FAQ auto-generated from most-asked questions per program

### 6.8 Arabic Voice Conversation (ASR)
All chat interfaces support **Arabic speech-to-text** — talk instead of type:

- **Applicant speaks**: "هل أنا مؤهل لبرنامج دعم التسويق؟" → system hears, processes, responds
- **Rule maker speaks**: "أضف قاعدة — رأس المال لازم يكون فوق عشرة آلاف دينار" → AI creates rule
- **Reviewer speaks**: "ارفض هذا الطلب — السجل التجاري منتهي" → AI records override with reasoning
- **Owner speaks**: "اعطيني تقرير بكل الطلبات المعلقة" → AI generates report

**Technology:**
- Azure AI Speech (cloud) — best Arabic dialect support (Levantine, Gulf, Egyptian, MSA)
- Whisper (local/open-source) — runs on same server for offline deployments
- Both support real-time streaming (speak and see text appear live)
- Text-to-Speech (TTS) optional: system can read back results for accessibility

**Why this matters for government:**
- Many government employees are faster speaking Arabic than typing
- Accessibility: visually impaired users can use the full system by voice
- Field use: inspector on-site can speak observations into the system
- Conversational flow is more natural for the guided onboarding (Phase 2.0)

### 6.9 Offline / Local Deployment
- Tier 1: Full Azure cloud (Azure OpenAI + Azure hosting)
- Tier 2: Azure hosting + local Ollama LLM (data stays on-premise)
- Tier 3: Fully local deployment (no internet required)

### 6.10 Full Owner Automation — AI-Generated Scripts
Upgrade from 5.5 (read-only) to **full write access + scheduling**:

- Owner can ask AI to **modify data**: send reminders, migrate applications, clean duplicates
- AI generates Python script, shows it to owner with a clear summary of what will change
- **Write operations require explicit approval**: owner sees "This will update 23 records" → confirms
- **Script Library**: saved automations, reusable, schedulable (daily/weekly/on-trigger)
- **Cron jobs**: "every Sunday, email me a summary" → saved as scheduled task
- All scripts versioned and auditable (who ran what, when, what changed)
- Sandboxed execution: no arbitrary system access, only whitelisted DB operations + email

_Only build this after 5.5 (read-only assistant) proves useful in production._

---

## Roadmap Timeline

| Phase | Name | Priority | Dependencies |
|-------|------|----------|-------------|
| **Phase 1** | Smart Applicant Portal | 🔴 High | None |
| **Phase 2** | Rules Studio | 🔴 High | None |
| **Phase 3** | AI Evaluation Engine | 🔴 High | Phase 2 (rules) |
| **Phase 4** | Reviewer Interface | 🔴 High | Phase 3 (engine) |
| **Phase 5** | Manager Dashboard | 🟡 Medium | Phase 4 |
| **Phase 6** | Advanced Features | 🟢 Later | Phase 1-5 |

### MVP (Minimum Viable Product)
**Phase 2 + Phase 3 + Phase 4** = Admin defines rules → AI evaluates → Reviewer decides

This is the core value. Phase 1 (applicant portal) and Phase 5 (dashboard) can be added after.

### First Thing to Build
**Phase 2.0 (Guided Onboarding)** — the chat that teaches a rule maker how to build `rules.md` + `skills.md`. This is the entry point for every new customer. If this works well, the rest follows naturally.

---

## System Skills — Our Own `skills.md` Files

The Agentic Government platform itself runs on `.md` skill files — the same pattern we teach customers:

| Skill File | Purpose |
|-----------|--------|
| `system/skills/rule-extraction.md` | How to read law PDFs and extract structured rules |
| `system/skills/document-reading.md` | How to OCR and parse Arabic documents, tables, dates |
| `system/skills/evaluation.md` | How to evaluate an application: citation format, confidence scoring, counter-arguments |
| `system/skills/form-filling.md` | How to extract data from documents and map to form fields |
| `system/skills/mock-generation.md` | How to generate realistic fake applications for testing |
| `system/skills/report-generation.md` | How to format reports in HTML, Excel, PDF, Word |
| `system/skills/chat-assistant.md` | How to chat with applicants: suggest programs, check readiness |
| `system/skills/onboarding.md` | How to teach a new rule maker through guided conversation |
| `system/skills/arabic-gov.md` | Arabic government domain knowledge: document types, date formats, legal terms |

These are **open and editable** — an IT admin can customize how the platform AI behaves by editing these `.md` files. Same pattern, system-wide.

---

## Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | React / Next.js | Arabic RTL, PDF viewer, responsive |
| Backend | FastAPI (Python) | Fast, async, AI libraries |
| Database | PostgreSQL | Rules, applications, evaluations, audit log |
| PDF Processing | Azure Document Intelligence | Arabic OCR, tables, page structure |
| AI | Azure OpenAI GPT-5-mini | Best Arabic, 1M token context |
| AI (local) | Ollama | Privacy, offline |
| Storage | Azure Blob Storage | Uploaded documents |
| Auth | Azure AD B2C / JWT | Government SSO |
| Hosting | Azure App Service | Government compliance |

---

## What Makes This Unique (vs Everything Else)

| Feature | Us | NOFA | Stanford SIL | EA Auditor | Submittable | Kira |
|---------|:--:|:----:|:---:|:---:|:---:|:---:|
| Generic (any program) | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| AI scoring with citations | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Configurable rules (no code) | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Applicant AI chat | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Pre-submission intelligence | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Arabic native | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Human override + audit trail | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Counter-arguments | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Open source | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Full workflow (submit→review→decide) | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Local/offline option | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Rules from PDF/law books | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Mock app generation | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Smart form auto-fill | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export HTML/Excel/PDF | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Per-user cost tracking | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Citizen ID login | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Community Q&A | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Results transparency to applicant | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Owner automation (AI writes scripts) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Arabic voice (ASR) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
