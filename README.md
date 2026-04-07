# Agentic Government — AI Workshop for JEDCO Staff

> **🇯🇴 [اقرأ هذا الملف بالعربية](README-AR.md)**

A 2-hour hands-on workshop introducing [JEDCO](https://www.jedco.gov.jo) staff to practical AI tools in their daily workflows — document writing, funding application review, and task automation. Local LLM, no data leaves the machine.

## Think of It This Way

> Everyone has the tool now — the skill is knowing how to use it. Excel automated calculations. AI agents automate reading, writing, and comparing documents. The officer still decides. The tool handles the repetitive parts so you focus on what actually needs your expertise.

## Host Organization

**[Jordan Enterprise Development Corporation (JEDCO)](https://www.jedco.gov.jo)** — est. 1972, Amman, Jordan

**JEDCO Active Programs (referenced in demos):**

| Program | Purpose |
|---------|---------|
| **Tamkeen** | SME capacity building and skills development |
| **Start Business** | Startup launch support |
| **Tattweer** | Business development and growth |
| **Quality Life at Home** | Home-based business support |
| **Ship Your Export** | Export facilitation for SMEs |
| **Exhibitions & Bazaars** | Market access through trade events |

**Staff Daily Workflows (training is built around these):**
- Reviewing SME/startup funding applications and deciding eligibility
- Writing funding decision letters and program reports (in Arabic)
- Coordinating with international donors and partners
- Managing rural productivity and employment programs

## Training Structure

| # | Block | Duration | JEDCO Context |
|---|-------|----------|---------------|
| 0 | How AI Works (New Hire Analogy) | 10 min | AI read everything, experienced nothing |
| 1 | What is an AI Agent? | 15 min | General concepts, government examples |
| 2 | Document Writing Demo | 25 min | Draft a funding decision letter in Arabic |
| 3 | Application Review Demo | 25 min | Review a mock Tattweer/Tamkeen application via the evaluation pipeline |
| 4 | RCTF Prompt Formula | 20 min | Examples from JEDCO program contexts |
| 5 | PC Agent Live Demo | 20 min | Automate repetitive application processing steps |
| 6 | Safe AI in Government + Q&A | 15 min | Jordan data protection + government AI principles |

## Tools Stack (Local / Private — No Cloud, No Data Leaving the Machine)

| Tool | Role | Why |
|------|------|-----|
| **Ollama** | Local LLM runtime | No API key, no internet required |
| **qwen3:8b** | Primary language model (5.2 GB) | Latest Qwen3, Arabic, thinking mode, tool calling, fits 6GB VRAM |
| **qwen2.5:7b** | Fallback model (4.7 GB) | Proven, fast, Arabic support |
| **gemma3:4b-it-qat** | Lightweight model (4.0 GB) | Vision support, 128K context |
| **gemma4:e4b** | Experimental (9.6 GB) | 128K context, thinking, partial VRAM on 6GB GPU |
| **Python + Ollama** | Evaluation Pipeline | Direct document evaluation with Qwen3 |
| **faster-whisper** | Arabic speech-to-text | `pip install faster-whisper`, runs on CUDA |

## Arabic Language Pipeline

```
Spoken Arabic → Whisper large-v3 (faster-whisper, CUDA) → Arabic text → qwen3:8b via Ollama → Output
```

## Hardware Requirements

**Development machine (this repo):** Intel i7-10750H · 16 GB RAM · NVIDIA RTX 2060 — **6 GB VRAM**

| Model | Size | Fits 6GB? | Status | Use case |
|-------|------|-----------|--------|----------|
| `gemma3:4b-it-qat` | 4.0 GB | ✅ | Installed | General, vision, 128K context |
| `qwen2.5:7b` | 4.7 GB | ✅ | Installed | Arabic, multilingual, fast |
| `qwen3:8b` | 5.2 GB | ✅ | **Installed — Default** | Latest Qwen3, thinking, tool calling |
| `gemma4:e4b` | 9.6 GB | ⚠️ partial | Installed | 128K context, spills to RAM |
| `qwen3:14b` | 9.3 GB | ❌ | — | Too large for 6GB |

> Run one model at a time. **`qwen3:8b` is the recommended model** — tested and verified on this machine with the JEDCO pipeline.

## Repository Structure

```
slides/      # Training outline per block (Arabic + English)
demos/       # Step-by-step demo scripts (block 2, 3, 5)
handouts/    # RCTF cheat sheet & participant cards (Arabic + English)
tools/       # Python pipeline scripts + setup guides
assets/      # Mock JEDCO applications, eligibility criteria, PDFs
secrets/     # ⚠️ Gitignored — never commit credentials here
```

## Pre-Training Checklist

- [ ] Install Ollama — download at [ollama.com](https://ollama.com)
- [ ] Pull the model: `ollama pull qwen3:8b` (5.2 GB)
- [ ] Run the evaluation pipeline: `python tools/evaluate-pipeline.py --model qwen3:8b`
- [ ] Run smoke test: `ollama run qwen3:8b "مرحبا، ما هو دورك؟"`
- [ ] See [`tools/setup-guide-AR.md`](tools/setup-guide-AR.md) or [`tools/setup-guide-EN.md`](tools/setup-guide-EN.md) for full instructions

## Roadmap — Web Application Portal

A self-service portal where applicants upload their application directly and receive AI-assisted pre-screening before officer review.

### Phase 1 — Upload & Document Check (MVP)
- [ ] Web form: applicant uploads application PDF + supporting documents
- [ ] Automatic document checklist — flags missing files before submission
- [ ] Applicant receives confirmation email with checklist status
- [ ] Officer dashboard: view incoming applications, sorted by completeness
- **Tech:** FastAPI backend + React frontend, hosted on JEDCO internal server

### Phase 2 — AI Pre-Screening
- [ ] Uploaded application auto-evaluated against program eligibility criteria
- [ ] AI generates preliminary score + flags (same pipeline as `evaluate-pipeline.py`)
- [ ] Officer sees: application, AI score, flagged issues — side by side
- [ ] Officer confirms, adjusts, or overrides each AI recommendation
- [ ] Full audit trail: every AI output + officer action logged
- **Tech:** Ollama API integration, PostgreSQL for application data

### Phase 3 — Applicant Tracking & Status
- [ ] Applicant portal: check application status (received → under review → decision)
- [ ] Automated notifications at each stage (email / SMS)
- [ ] Officer can request missing documents directly through the portal
- [ ] Applicant uploads corrections without resubmitting the full application

### Phase 4 — Post-Award Monitoring
- [ ] Beneficiary submits progress reports through the portal
- [ ] AI reads report and generates project status summary for the officer
- [ ] Dashboard: all active projects, color-coded (on track / at risk / critical)
- [ ] Closure evaluation auto-generated when contract period ends

### Architecture Overview
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Applicant  │────▶│  Web Portal  │────▶│  Officer     │
│  (browser)  │     │  FastAPI +   │     │  Dashboard   │
│             │◀────│  React       │◀────│  (review +   │
│  uploads +  │     │              │     │   decide)    │
│  tracks     │     └──────┬───────┘     └─────────────┘
│  status     │            │
└─────────────┘     ┌──────▼───────┐
                    │  AI Engine   │
                    │  Ollama +    │
                    │  qwen3:8b    │
                    │  (local)     │
                    └──────┬───────┘
                    ┌──────▼───────┐
                    │  PostgreSQL  │
                    │  (all data   │
                    │   on-prem)   │
                    └──────────────┘
```

### Key Principles
- **All data stays on JEDCO infrastructure** — no external cloud
- **AI assists, officer decides** — every AI output requires human confirmation
- **Arabic-first UI** — RTL layout, Arabic labels, bilingual option
- **Audit trail** — every action logged for transparency and accountability
