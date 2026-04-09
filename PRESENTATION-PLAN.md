# Presentation Plan — How We Built an AI Grant Evaluation System from Scratch

> **Audience:** Non-technical JEDCO staff and government decision-makers
> **Format:** HTML slides (Swiper.js), hosted on GitHub Pages
> **Language:** Arabic-first (slides in Arabic, UI labels in English where needed)
> **Goal:** Show step-by-step how anyone with a computer can build this — and that an AI agent helped build it
> **Live URL:** https://shdaifat.github.io/AgenticGovernment/

---

## Training Flow Summary (Updated April 2026)

### Phase 1 — Manual with Free Web AI (Gemini + ChatGPT)
Trainees use free browser tools — no installation, no code.
1. **Gemini reads JEDCO website** → extracts 6 eligibility rules
2. **ChatGPT generates 2 mock applications** (1 PASS, 1 FAIL)
3. **Gemini evaluates each application** against the rules → مقبول/مرفوض

### Phase 2 — The Scaling Problem
After doing it manually for 2 applications, trainees see the pain:
- 100 طلب × محادثة جديدة × لصق الشروط × لصق الطلب = يومان كاملان

### Phase 3 — Vibe Coding: From Manual to Automated
Trainees watch the trainer use VS Code + Copilot to automate the same process:
1. **Setup:** Install VS Code + Copilot (free tier) + Python
2. **⚠️ Cloud warning:** Copilot/ChatGPT/Gemini are cloud-based — NEVER use real data
3. **Generate 20 mock applications** using Copilot (first vibe coding exercise)
4. **Build evaluation script** using Copilot prompt → Python script
5. **Run it** → HTML report + Excel output for all 20 applications

### Why this order works:
- Phase 1 teaches the LOGIC (rules → applications → evaluation)
- Phase 2 creates the PAIN (this is impossible at scale)
- Phase 3 shows the SOLUTION (same logic, automated)
- Trainees who are not technical still understand what the pipeline does

---

### Tool Selection — Why Gemini + ChatGPT for Phase 1

| Tool | Website Reading | Arabic Quality | Installation | Cost |
|------|----------------|---------------|--------------|------|
| **Gemini** ✅ | ✅ Reads live URLs | Excellent | None — browser | Free (Google account) |
| **ChatGPT** ✅ | ❌ Can't browse URLs | Very good for generation | None — browser | Free (OpenAI account) |
| Claude.ai | ❌ Limited browsing | Very good | None — browser | Free (limited) |
| Ollama (local) | ❌ No browsing | Good (Qwen3) | Yes — install needed | Free but needs hardware |

**Gemini** reads the JEDCO website directly → extracts rules + evaluates.
**ChatGPT** generates realistic mock applications from rules.
**Together** they cover the full workflow without any installation.

---

### JEDCO Program Used in Training

- **Program:** "ارفع قدراتك بالتسويق" (Raise Your Marketing Capabilities)
- **URL:** https://www.jedco.gov.jo/AR/ListDetails/دليل_الخدمات/7/28
- **6 Eligibility Rules:**
  1. تسجيل الشركة — مسجلة رسمياً، ليست مساهمة عامة
  2. عمر الشركة — سنتان أو أكثر
  3. الملكية — خاصة 100%، أردنية ≥51%
  4. عدد الموظفين — 1 إلى 249 (ضمان اجتماعي)
  5. نسبة التمويل — لا تتجاوز 70%
  6. الحالة مع JEDCO — أغلقت جميع ملفات سابقة
- **Grant:** 70% of cost, max 15,000 JD, 1-year execution
- **Sectors:** صناعي · حرفي · زراعي · خدمي (يُستثنى التجاري)

### Mock Applications Created

- **أدفانز-ج** (PASS): شركة صناعية، 4 سنوات، 18 موظفاً، 15,000 د.أ
- **سوا** (FAIL): شركة خدمية، 14 شهراً، 6 موظفين، 12,000 د.أ — رفض بسبب العمر

---

## Slide Deck Structure

### ACT 1: THE STARTING POINT (Slides 1–5) ✅ DONE

| # | Slide | Status |
|---|-------|--------|
| 1 | Title — "How We Built an AI-Powered Grant Review System" | ✅ |
| 2 | What We Started With (laptop, no tools, no data, no budget) | ✅ |
| 3 | What We Built (reads, checks, scores, flags, reports) | ✅ |
| 4 | AI Tools Chained: You → Gemini → ChatGPT → Pipeline → Report | ✅ |
| 5 | Everything Is Free ($0 total) | ✅ |

---

### ACT 2: MANUAL PHASE — Learn the Logic (Slides 6–7b-2) ✅ DONE

| # | Slide | Content | Status |
|---|-------|---------|--------|
| 6 | Gemini Step 1 — give it JEDCO URL + extraction prompt | Arabic prompt with live URL | ✅ |
| 6b | Gemini Output — 6-rule table + grant details | Real Gemini response | ✅ |
| 7 | ChatGPT Step 2 — generate 2 mock applications | Arabic prompt + side-by-side summary | ✅ |
| 7-A | أدفانز-ج full application (PASS) | Verbatim ChatGPT output | ✅ |
| 7-B | سوا full application (FAIL) | Verbatim ChatGPT output | ✅ |
| 7b | Gemini Step 3 — Arabic evaluation prompt | Full JEDCO-employee role prompt | ✅ |
| 7b-2 | Gemini responses — مقبول + مرفوض | Real Gemini PASS/FAIL output | ✅ |

---

### ACT 2.5: THE SCALING PROBLEM (Slide 7c) ✅ DONE

| # | Slide | Content | Status |
|---|-------|---------|--------|
| 7c | "الآن تخيّلوا... 100 طلب" | 4 red pain points + time estimate + green automation CTA | ✅ |

---

### ACT 3: FROM MANUAL TO AUTOMATED (Slides 8–12) 🔄 REWRITING

> **✅ DECISION MADE (April 2026):** Open WebUI as primary tool + Python batch script for demo.
> DocETL dropped (requires OpenAI API key, Ollama support experimental).
> VS Code shown briefly as "how I built all of this" — not trainee exercise.

---

#### SHARED SLIDES (all paths)

**Slide 8 — "ما شاهدتموه اليوم هو Vibe Coding"**
- You already watched me build this presentation using Copilot
- Same pattern you used with Gemini: describe → AI does → you verify
- **This is vibe coding. You don't write code — you describe what you want.**

**Slide 9 — "⚠️ تحذير: بياناتكم تذهب للسحابة"**
- Copilot / ChatGPT / Gemini = cloud-based LLMs
- Your prompts and data ARE sent to external servers
- **NEVER use real applicant data** — names, IDs, financials
- That's why we generate **mock data** for training
- For real data: use Ollama (local, offline) — data never leaves the building
- **هذا هو الفرق بين التدريب والتطبيق الحقيقي**

---

#### PATH A: DocETL (Browser UI — Test 1, Run 1000) ⭐ RECOMMENDED

> **Best for:** Non-technical trainees. Zero code. Generic for any task.
> **Trainee experience:** Open browser → upload files → write prompt → test on 1 → run on 1000 → download Excel
> **Setup:** Docker + Ollama on trainer's laptop or LAN server

**Why DocETL:**
- Generic framework — works for ANY document + ANY prompt + ANY criteria
- Visual browser UI, no VS Code, no terminal
- "Test on 1, then batch 1000" is the core workflow
- Connects to Ollama (local LLM) — data stays on machine
- Free, open source (docetl.org)

**Slide 10A — "الأداة: DocETL — جرّب على واحد، طبّق على ألف"**
- What is DocETL: a browser tool for batch document processing with AI
- Show the UI: upload area, prompt editor, output preview
- Key concept: same prompt you wrote for Gemini works here — but for 1000 files
- Table:
  | Gemini (manual) | DocETL (automated) |
  |---|---|
  | 1 محادثة = 1 طلب | 1 أمر = 1000 طلب |
  | لصق الشروط كل مرة | الشروط محفوظة |
  | نسخ النتيجة يدوياً | تصدير Excel تلقائي |
  | سحابة (cloud) | محلي (Ollama) |

**Slide 11A — "تمرين: جهّز 20 طلباً وهمياً"**
- Use ChatGPT or Copilot to generate 20 mock Arabic applications
- Or: download the 20 pre-generated files from the repo (`applications/` folder)
- Upload them into DocETL

**Slide 12A — "تمرين: قيّم الـ 20 طلباً في DocETL"**
- Paste the same Gemini evaluation prompt (slide 7b)
- Select output format: مقبول/مرفوض + السبب
- Test on 1 application → verify output matches Gemini's answer
- Click "Run All" → processes all 20
- Export Excel → done
- **Same logic. Same prompt. 20× faster. No code.**

**Slide 12bA — "النتيجة: يدوي مقابل DocETL"**
- Side by side comparison (same as 12b but DocETL-specific)

---

#### PATH B: Open WebUI (ChatGPT-like Interface on LAN)

> **Best for:** Trainees who liked Gemini/ChatGPT. Feels familiar.
> **Trainee experience:** Open browser → chat in Arabic → upload files → get answers
> **Setup:** Docker + Ollama on LAN server
> **Limitation:** Chat-based, not batch-optimized. Employee processes 1 at a time (but much faster than Gemini because rules are pre-loaded via RAG).

**Slide 10B — "الأداة: Open WebUI — ChatGPT على شبكتكم"**
- Looks like ChatGPT but runs on your office network
- Uses Ollama (local) — data never leaves the room
- Upload JEDCO criteria once → all conversations use them (RAG)
- Each employee gets a login
- Free, open source

**Slide 11B — "تمرين: قيّم طلبات في Open WebUI"**
- Open browser → go to LAN address
- Type: "قيّم هذا الطلب" + paste application text
- Get: مقبول/مرفوض + السبب
- No need to paste criteria every time (pre-loaded)

**Slide 12B — "متى نحتاج أكثر من Open WebUI؟"**
- Good for: 1-by-1 conversation, ad-hoc questions, exploring
- Not ideal for: batch 1000 files, automated reports, Excel export
- For batch: need DocETL or custom pipeline

---

#### PATH C: VS Code + Copilot (Vibe Coding)

> **Best for:** Showing the "future" of how software is built.
> **Trainee experience:** Watch trainer describe → Copilot writes code → run → results
> **Setup:** VS Code + Copilot (free tier) + Python
> **Limitation:** Trainees found this intimidating. Best as demo, not exercise.

**Slide 10C — "الأدوات المطلوبة"**
- VS Code + Copilot (free) + Python
- Install steps or pre-installed on training laptops

**Slide 11C — "تمرين: أنشئ 20 طلباً وهمياً بـ Copilot"**
- Open Copilot chat in VS Code
- Prompt: "أنشئ 20 طلب منحة وهمي بالعربية..."
- Copilot generates 20 text files → save to `applications/`
- First vibe coding moment

**Slide 12C — "تمرين: اكتب برنامج التقييم بـ Copilot"**
- Prompt: "اكتب برنامج Python يقرأ جميع الطلبات ويقيّم كل طلب حسب شروط JEDCO الستة ويخرج تقرير HTML + Excel"
- Copilot generates the script
- Run: `python evaluate.py`
- Output: HTML + Excel

---

#### PATH COMPARISON

| Criteria | A: DocETL | B: Open WebUI | C: VS Code |
|----------|-----------|---------------|------------|
| Trainee skill needed | Browser only | Browser only | VS Code + terminal |
| Batch processing (1000) | ✅ Core feature | ❌ 1-by-1 chat | ✅ Script runs all |
| Prompt experimentation | ✅ Test 1 → run 1000 | ✅ Natural chat | ⚠️ Edit code/prompt |
| Excel/HTML export | ✅ Built-in | ❌ Manual copy | ✅ Script output |
| Generic (any task) | ✅ Any doc + any prompt | ✅ Any question | ⚠️ Need new script |
| Offline (real data safe) | ✅ Ollama | ✅ Ollama | ⚠️ Copilot is cloud |
| Setup complexity | Docker (1 command) | Docker (1 command) | 3 installs |
| Intimidation factor | Low | Very low | High |
| Best for | Batch evaluation | Ad-hoc questions | Building systems |

**✅ DECISION:** PATH B (Open WebUI) as main + simple Python batch script for 100-app demo.

**Why this combination:**
- Open WebUI = familiar ChatGPT interface, Ollama native, no API keys, fully offline
- 131k GitHub stars = battle-tested, huge community, Arabic-friendly
- Knowledge/RAG = upload JEDCO rules once, every conversation uses them
- Model presets = create "مُقيّم JEDCO" agent, employees open → paste app → get answer
- Python script (trainer demo) = shows batch capability without requiring trainees to code
- DocETL dropped: UI requires OpenAI API key, Ollama support is experimental with caveats
- VS Code kept as brief demo only: "this is how I built these slides"

---

### ACT 4: RESULTS & DEPLOYMENT (Slides 13–18) — KEEP/UPDATE

| # | Slide | Content | Status |
|---|-------|---------|--------|
| 13 | Reports — HTML + Excel output | Show actual report screenshot | 🔄 Update to show Excel too |
| 14 | Where Can This Run? (laptop → LAN → server → internet) | Deployment options table | ✅ Keep |
| 15 | Applicant Portal Vision (web upload → pre-screening) | Future vision | ✅ Keep |
| 16 | OCR for Scanned Documents | Scanned PDF → text → AI | ✅ Keep |
| 17 | Don't Fear the Code (black box analogy) | You care about input/output, not code | ✅ Keep |
| 18 | Summary & Next Steps | What we proved + what's coming | ✅ Keep |

---

## Repository Assets to Create

### Mock Applications (20 files) — NEEDED FOR ALL PATHS
- **Location:** `applications/` folder in repo root
- **Format:** Arabic text files, one per application
- **Mix:** ~12 PASS, ~8 FAIL with varied rejection reasons:
  - عمر أقل من سنتين (age)
  - مساهمة عامة (company type)
  - ملكية أجنبية أكثر من 49% (ownership)
  - أكثر من 249 موظف (employees)
  - نسبة تمويل أعلى من 70% (funding ratio)
  - ملفات سابقة مفتوحة (previous files)
- **Naming:** `app-01-اسم-الشركة.txt` through `app-20-اسم-الشركة.txt`

### Path-Specific Assets

**If PATH A (DocETL):**
- `docker-compose.yml` — DocETL + Ollama setup
- `docetl-pipeline.yaml` — pre-built pipeline config for JEDCO evaluation
- README with setup instructions

**If PATH B (Open WebUI):**
- `docker-compose.yml` — Open WebUI + Ollama setup
- `criteria.txt` — JEDCO rules for RAG upload
- README with setup instructions

**If PATH C (VS Code):**
- `tools/evaluate.py` — Python evaluation script
- Requirements file for dependencies
- README with setup instructions

### Output Samples (for slides)
- `results/results.html` — sample HTML report
- `results/results.xlsx` — sample Excel output
- Screenshots of the chosen tool in action

---

## Technical Notes

### Hosting
- **Swiper.js 11** via CDN — vertical slides, mousewheel + keyboard navigation
- Single file: `docs/index.html`
- GitHub Pages: `docs/` folder on `master` branch
- Mobile-friendly, Arabic RTL supported

### Key URLs
- Gemini: https://gemini.google.com
- ChatGPT: https://chatgpt.com
- VS Code: https://code.visualstudio.com
- Ollama (offline): https://ollama.com

### Screenshots Still Needed
- [ ] VS Code with Copilot chat generating mock applications
- [ ] Terminal running `evaluate.py` on 20 applications
- [ ] HTML report output showing 20 evaluated applications
- [ ] Excel output with مقبول/مرفوض columns
- [ ] DocETL browser UI (if PATH A chosen)
- [ ] Open WebUI chat interface (if PATH B chosen)

---

## Next Steps (in order)

1. **✅ DECIDE:** Open WebUI + Python batch script (April 9, 2026)
2. **⬜ Generate 20 mock applications** → commit to `applications/`
3. **⬜ Rewrite slides 8–12** (vibe coding → cloud warning → Open WebUI → batch demo → comparison)
4. **⬜ Create Python batch evaluation script** → `tools/batch_evaluate.py`
5. **⬜ Create Open WebUI docker-compose** → `tools/docker-compose.yml`
6. **⬜ Update slides 13–18** (add Excel output, update deployment table)
7. **⬜ Capture screenshots** for Open WebUI
8. **⬜ Push and test live**
