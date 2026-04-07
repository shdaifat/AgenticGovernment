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

## Step 3 — Verify Python Installation

1. Open **Command Prompt** or **PowerShell**
2. Type:
   ```
   python --version
   ```
   Should show Python 3.8 or higher

3. Install required packages:
   ```
   pip install requests
   ```

---

## Step 4 — Test the Evaluation Pipeline

1. Navigate to the project folder:
   ```
   cd c:\Projects\AgenticGovernment
   ```

2. Run the evaluation pipeline to test all components:
   ```
   python tools/evaluate-pipeline.py --model qwen3:8b --summary
   ```

3. Expected output:
   - Process 1–2 applications from `assets/jedco-docs/`
   - Generate `results.json`, `results.html`, `results.pdf`
   - Show scores and recommendations

---

## Step 5 — Smoke Test

### Test 1: Ollama directly
```
ollama run qwen3:8b "You are a JEDCO evaluator. What are the Tattweer program requirements?"
```
→ Should respond with program information ✅

### Test 2: Evaluation pipeline
```
cd c:\Projects\AgenticGovernment
python tools/evaluate-pipeline.py --model qwen3:8b --limit 2 --summary
```
→ Should generate a ranked report with scores and flags ✅

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
