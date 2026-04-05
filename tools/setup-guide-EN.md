# Setup Guide — Pre-Training Day Installation
## Agentic Government / JEDCO
### Estimated time: ~30 minutes

---

## Requirements
- Windows 10 or 11
- NVIDIA GPU with 6GB+ VRAM (RTX 2060 or better)
- Free disk space: at least 15 GB
- Internet connection (for downloads only — training runs fully offline)

---

## Step 1 — Install Ollama

1. Open browser: **https://ollama.com/download**
2. Select **Windows** and click **Download**
3. Run `OllamaSetup.exe`
4. Follow installer steps (Next → Next → Install)
5. Open **Command Prompt** or **PowerShell**
6. Type:
   ```
   ollama --version
   ```
   Should show version number (e.g., `ollama version 0.20.2`)

### ⚠️ If the command is not recognized:
Add Ollama to PATH manually:
```
set PATH=%PATH%;%LOCALAPPDATA%\Programs\Ollama
```

---

## Step 2 — Download qwen3:8b Model

1. In the same terminal, type:
   ```
   ollama pull qwen3:8b
   ```
2. Wait for download (5.2 GB — takes 10-20 min depending on connection)
3. Test the model:
   ```
   ollama run qwen3:8b "Hello, what is your role?"
   ```
4. Model should respond in English ✅
5. To exit the chat, type: `/bye`

---

## Step 3 — Install AnythingLLM

1. Open browser: **https://anythingllm.com/download**
2. Select **Windows** and click **Download**
3. Run `AnythingLLMDesktop.exe`
4. Follow installer steps
5. After opening the app:
   - Select **Ollama** as the LLM Provider
   - URL: `http://localhost:11434`
   - Select model: **qwen3:8b**
   - Click **Save**

---

## Step 4 — Create Workspace and Upload Documents

1. In AnythingLLM, click **New Workspace**
2. Name it: `JEDCO Application Review`
3. Click the upload icon
4. Upload these files from `assets/jedco-docs/`:
   - `JEDCO-eligibility-criteria-reference-v2.txt`
   - `mock-application-start-business-AR.txt`
   - `mock-application-tattweer-AR.txt`
5. Wait for document embedding to complete

---

## Step 5 — Smoke Test

### Test 1: Ollama directly
```
ollama run qwen3:8b "You are a JEDCO evaluator. What are the Tattweer program requirements?"
```
→ Should respond with program information ✅

### Test 2: AnythingLLM
- Open `JEDCO Application Review` workspace
- Type: "What documents are required for the Tattweer program?"
→ Should respond based on uploaded documents ✅

### Test 3: Automated pipeline (optional)
```
cd c:\Projects\AgenticGovernment
python tools/evaluate-pipeline.py --model qwen3:8b --limit 2
```
→ Should show evaluation for 2 applications ✅

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ollama` not recognized | Add to PATH (see Step 1) |
| Slow download | Check internet connection, use faster network |
| AnythingLLM can't find Ollama | Ensure Ollama is running: `ollama list` |
| Model very slow | Close other apps, confirm GPU is being used |
| Python error | Ensure Python 3.8+ installed, run `pip install requests` |

---

## ✅ Ready for Training Day!
If all 3 tests pass, the machine is ready for the training session.
