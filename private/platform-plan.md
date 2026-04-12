# Plan: Azure-Hosted AI Grant Evaluation Platform (→ Local Migration)

> **⚠️ PRIVATE — do NOT push to public GitHub repo (shdaifat/AgenticGovernment)**

## TL;DR

Web app on Azure that evaluates JEDCO grant applications using Azure OpenAI (GPT-5-mini). 4 user levels. User picks the model from a dropdown. Same codebase runs on Azure, LAN Ollama, or fully local. JEDCO first, then generalize.

---

## User Levels (4)

| Level | Role | What they do | Interface |
|-------|------|-------------|-----------|
| 1. End User (الموظف) | Grant Officer | Upload app → click Evaluate → see pass/fail + reasoning | Arabic web form + model dropdown |
| 2. Rules Admin (مسؤول المعايير) | Domain Expert | Update eligibility criteria per program — no code | Admin panel: edit rules, select program |
| 3. IT Staff (تقنية المعلومات) | Deploy & maintain | Docker, Azure Portal, model config, cost monitoring | CLI + Azure Portal |
| 4. Manager (المدير) | Decision Maker | Dashboard: pass/fail rates, cost, adoption metrics | Charts + summary stats |

Level 2 is critical — rules change per JEDCO program, domain experts own them, not IT.

---

## Architecture

### Azure Stack (Demo/Product)
```
[Browser] → [Azure Static Web Apps (frontend)]
                      ↓
            [Azure Container Apps (FastAPI API)]
                      ↓
            [Azure OpenAI GPT-5-mini] ← private, no training
                      ↓
            [Azure Blob + Table Storage]
```

### Local Stack (Migration)
```
[Browser] → [nginx on LAN]
                  ↓
            [FastAPI on LAN]
                  ↓
            [Ollama on LAN server (GPU)] ← configurable URL
                  ↓
            [Local filesystem + SQLite]
```

### 3 Deployment Tiers (same codebase)

| Tier | Website | LLM | Data stays in | Use case |
|------|---------|-----|--------------|----------|
| 1. Azure + Azure OpenAI | Azure | GPT-5-mini | MS datacenter (encrypted) | Demo, pilot, remote |
| 2. Azure + LAN Ollama | Azure | Ollama on JEDCO LAN | JEDCO network only | Production, central model |
| 3. Fully Local | LAN nginx | Ollama on LAN | JEDCO building (air-gap OK) | Maximum sovereignty |

Tier 2 sweet spot: one GPU server on LAN serves all officers, IT manages one instance.

### Frontend Hybrid Mode (like Copilot)
- Browser auto-detects Ollama at configurable URL on page load
- If found → local models appear in dropdown alongside Azure models
- User picks per-evaluation: cloud or local
- Same Azure-hosted website, no redeployment needed

### Abstraction Layer
- `llm_client.py`: `LLM_BACKEND=azure|ollama` env var switches backend
- `storage_client.py`: `STORAGE_BACKEND=azure|local` env var switches storage
- `GET /models` endpoint: returns available models from active backend
- Frontend model dropdown: user picks model, sees Arabic labels + privacy indicator

---

## Azure Privacy & Compliance

Verified from Microsoft docs (April 2026):
1. Data NOT used for training
2. NOT shared with other customers or OpenAI
3. Models are stateless — nothing stored
4. AES-256 at rest, TLS in transit
5. You choose Azure region (UAE North for proximity)
6. SOC 2 Type 2, ISO 27001/27018, GDPR
7. Can disable human review for sensitive government data
8. Azure OpenAI ≠ ChatGPT — runs in your Azure tenant, not OpenAI servers

**Caveat**: Data still leaves JEDCO building encrypted to MS datacenter. LAN Ollama eliminates even that.

---

## LLM Options

| Model | Privacy | Arabic | Cost (per 1M tokens) |
|-------|---------|--------|---------------------|
| **GPT-5-mini** ⭐ | Private (MS tenant) | Excellent + reasoning | $0.25 in / $2 out |
| GPT-5-nano | Private | Good | $0.05 in / $0.40 out |
| GPT-4.1-mini | Private | Good, 1M context | $0.40 in / $1.60 out |
| GPT-5 | Private | Frontier | $1.25 in / $10 out |
| Ollama qwen3:8b | Fully on-premise | Good | Hardware only |

**Default: GPT-5-mini** — reasoning, excellent Arabic, ~$3-5/month. User can pick any model from dropdown.

---

## Implementation Phases

### Phase 1: API (Python + FastAPI)
- `api/llm_client.py` — Azure OpenAI ↔ Ollama, accepts model param
- `api/storage_client.py` — Azure Blob ↔ local files
- Routes: `POST /evaluate`, `GET /models`, `GET/PUT /criteria`, `GET /dashboard`, `POST /batch`
- Env: `LLM_BACKEND`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`, `OLLAMA_URL`

### Phase 2: Frontend (HTML/JS, Arabic RTL)
- Upload form + model dropdown (from /models) + results
- Model labels: "GPT-5-mini — سريع ودقيق", "qwen3:8b 🔒 محلي"
- Side-by-side model comparison for demo
- Rules admin panel, dashboard with charts, role-based login

### Phase 3: Azure Deployment
- Dockerfile + docker-compose
- Azure Container Apps (scales to zero), Static Web Apps (free), Blob Storage
- Azure OpenAI resource in UAE North

### Phase 4: Local Migration Kit
- `docker-compose.local.yml` with Ollama container
- `.env.local`: `LLM_BACKEND=ollama`
- One command: `docker compose -f docker-compose.local.yml up`

---

## Cost Estimate (Azure)

| Service | Est. Monthly |
|---------|-------------|
| Container Apps (scale to zero) | $0-20 |
| Azure OpenAI GPT-5-mini (~100 evals/day) | $3-5 |
| Blob Storage | $0.02 |
| Static Web Apps | Free |
| **Total** | **$3-25/month** |

---

## Existing Assets to Reuse
- `tools/batch_evaluate.py` — evaluation logic, Arabic prompt, JSON parsing
- `applications/` — 20 mock JEDCO apps (12 PASS, 8 FAIL)
- `assets/jedco-docs/` — criteria reference files

## Open Questions
1. Auth: Simple JWT (fast demo) vs Azure AD B2C (production)?
2. OCR in Phase 1? Or text-only input first?
3. Separate private repo, or private branch?
