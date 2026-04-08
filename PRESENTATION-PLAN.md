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

### ACT 3: VIBE CODING — From Manual to Automated (Slides 8–12) 🔄 NEEDS REWRITE

**Current slides 8–12 are outdated.** Replace with the following new flow:

#### Slide 8 — "ما شاهدتموه اليوم هو Vibe Coding" (NEW)
- You already watched me build this presentation using Copilot
- I described what I wanted → Copilot wrote the HTML/CSS/Arabic
- I checked, adjusted, pushed → the slides you're reading now
- Same pattern: describe the problem → AI writes the solution → you verify
- **This is vibe coding. You don't write code — you describe what you want.**

#### Slide 9 — "الأدوات المطلوبة" — Setup (NEW)
- Table:
  | Tool | What | Where | Cost |
  |------|------|-------|------|
  | VS Code | محرر الأكواد | code.visualstudio.com | مجاني |
  | GitHub Copilot | مساعد ذكي داخل VS Code | Extensions tab | مجاني (2000 إكمال/شهر) |
  | Python | يشغّل البرنامج | python.org | مجاني |
- Simple install steps (or pre-installed on training laptops)

#### Slide 10 — "⚠️ تحذير: بياناتكم تذهب للسحابة" — Cloud Warning (NEW)
- Copilot / ChatGPT / Gemini = cloud-based
- Your prompts and code ARE sent to external servers
- **NEVER use real applicant data** — names, IDs, financials
- That's exactly why we generate **mock data**
- Later: mention Ollama as the offline alternative for real data
- **هذا هو الفرق بين التدريب والتطبيق الحقيقي**

#### Slide 11 — "تمرين: أنشئ 20 طلباً وهمياً" — Generate Mock Data (NEW)
- Open Copilot in VS Code
- Paste the 6 JEDCO rules
- Prompt (Arabic): "أنشئ 20 طلب منحة وهمي بالعربية كملفات نصية منفصلة. خليط من مقبول ومرفوض. نوّع أسباب الرفض."
- Copilot generates 20 text files → save to `applications/` folder
- **This is their first real vibe coding moment**
- The 20 applications will be pre-generated and committed to the repo for reference

#### Slide 12 — "تمرين: قيّم الـ 20 طلباً تلقائياً" — Run Automation (NEW)
- Prompt Copilot: "اكتب برنامج Python يقرأ جميع الطلبات من مجلد applications/ ويقيّم كل طلب حسب شروط JEDCO الستة ويخرج النتائج كتقرير HTML وملف Excel"
- Copilot generates the script
- Run: `python evaluate.py`
- Output: HTML report + Excel file with مقبول/مرفوض for all 20
- **Same logic they did manually in Gemini — but automated**

#### Slide 12b — "النتيجة: يدوي مقابل تلقائي" (UPDATE existing)
- Side by side:
  | يدوي (Gemini) | تلقائي (Python) |
  |---|---|
  | 100 محادثة جديدة | أمر واحد |
  | يومان | 90 دقيقة |
  | نسخ يدوي للنتائج | تقرير HTML + Excel جاهز |
  | أخطاء بشرية | نفس المنطق كل مرة |

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

### Mock Applications (20 files)
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

### Evaluation Script
- **Location:** `tools/evaluate.py` (or use existing `evaluate-pipeline.py`)
- **Input:** reads all `.txt` files from `applications/`
- **Rules:** hardcoded 6 JEDCO criteria (no API needed for rule-checking)
- **Output:** `results.html` + `results.xlsx`
- **Note:** For training, this can use Gemini API or Ollama — decide based on internet access

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
