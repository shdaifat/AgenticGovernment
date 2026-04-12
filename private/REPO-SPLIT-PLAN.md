# Repo Split Plan — GitHub (Training) + Bitbucket (Product)

## Goal
Split into two repos on **two different platforms**:
- `shdaifat/AgenticGovernment` on **GitHub** (PUBLIC) — training slides, mock apps, tools, handouts
- `bahbish/AgenticGovernment` on **Bitbucket** (PRIVATE) — product: MVP, ROADMAP, skills, platform code

## Why This Split Works
- `private/` is already in `.gitignore` → product files have **never been pushed to GitHub**
- GitHub repo already IS the training repo — just needs minor cleanup
- Product repo starts fresh on Bitbucket with clean first commit
- No data leakage risk — product files were never in GitHub history

---

## Pre-Flight Checks

```bash
# Verify current repo is clean
cd c:\Projects\AgenticGovernment
git status

# Confirm private/ is gitignored (product files never pushed)
git ls-files private/
# Should return NOTHING — confirms no product files in git history

# Verify gh CLI (optional — only needed for GitHub cleanup)
gh auth status
```

---

## Phase 1 — Create Product Repo on Bitbucket (SAFE — fresh start)

### 1.1 Create repo on Bitbucket (web UI)
1. Go to https://bitbucket.org/bahbish/
2. Click **Create repository**
3. Repository name: `AgenticGovernment`
4. Access level: **Private**
5. Include a README: **No**
6. Version control: **Git**
7. Click **Create repository**

### 1.2 Create local product folder
```bash
mkdir c:\Projects\AgenticGov
cd c:\Projects\AgenticGov
git init
```

### 1.3 Copy product files (flatten — no more private/ prefix)
```bash
# Product docs → root
cp c:\Projects\AgenticGovernment\private\ROADMAP.md          .
cp c:\Projects\AgenticGovernment\private\MVP-PLAN.md         .
cp c:\Projects\AgenticGovernment\private\platform-plan.md    .
cp c:\Projects\AgenticGovernment\private\REPO-SPLIT-PLAN.md  .
cp c:\Projects\AgenticGovernment\private\AGENTIC-STATE-SUMMARY-AND-COMPARISON.md .

# Proposals and brainstorming
cp -r c:\Projects\AgenticGovernment\private\brainstorming\   brainstorming\
cp -r c:\Projects\AgenticGovernment\private\screenshots\     screenshots\

# Copy specific proposal docs
cp c:\Projects\AgenticGovernment\private\JEDCO-AI-Grant-Management-Proposal-AR.md .
cp c:\Projects\AgenticGovernment\private\JEDCO-AI-Grant-Management-Proposal-EN.md .

# Skip: The-Agentic-State-Vision-Paper.pdf (large binary, re-download if needed)
# Skip: xxx (temp file)
```

### 1.4 Create product README.md
```markdown
# Agentic Government

AI-powered government case evaluation platform.

## Documentation
- [ROADMAP](ROADMAP.md) — 6-phase product roadmap
- [MVP Plan](MVP-PLAN.md) — 7-step implementation plan
- [Platform Plan](platform-plan.md) — architecture and pricing

## Training Materials
JEDCO training materials: https://github.com/shdaifat/AgenticGovernment
```

### 1.5 Create product .gitignore
```gitignore
# Secrets
.env
.env.*
*.key
*.pem

# Python
__pycache__/
*.py[cod]
.venv/
venv/
*.egg-info/

# Node
node_modules/

# OS
.DS_Store
Thumbs.db

# VS Code
.vscode/settings.json
.vscode/launch.json

# Runtime data
projects/
*.log
logs/

# Large binaries (download separately)
*.pdf
```

### 1.6 Initial commit and push
```bash
cd c:\Projects\AgenticGov
git add -A
git commit -m "Initial commit — Agentic Government product platform

Product docs, roadmap, MVP plan, and architecture.
Training materials remain at: https://github.com/shdaifat/AgenticGovernment"

git remote add origin https://bitbucket.org/bahbish/AgenticGovernment.git
git push -u origin master
```

### 1.7 Verify
```bash
# Check remote
git remote -v
# Should show: origin https://bitbucket.org/bahbish/AgenticGovernment.git

# Check files
git ls-files
# Should show: ROADMAP.md, MVP-PLAN.md, platform-plan.md, README.md, etc.
# Should NOT show: slides/, applications/, tools/, private/
```

**⏸ CHECKPOINT 1: Open https://bitbucket.org/bahbish/AgenticGovernment in browser. Do you see the product files? If yes, proceed.**

---

## Phase 2 — Clean Up GitHub Training Repo

The GitHub repo is already a training repo (product files were gitignored).
Minor cleanup: remove stale files, update README.

### 2.1 Clone training repo to its own folder
```bash
git clone https://github.com/shdaifat/AgenticGovernment.git c:\Projects\jedco-ai-training
cd c:\Projects\jedco-ai-training
```

### 2.2 Clean up non-training files
```bash
# Remove empty/stale files
git rm -f results.html results.json results.pdf 2>/dev/null
git rm -rf secrets/ 2>/dev/null
```

### 2.3 Update .gitignore (simplify — no more private/ concept)
Remove these lines from `.gitignore`:
- `private/`
- `assets/jedco-docs/JEDCO-AI-Grant-Management-Proposal*`
- `results.html`, `results.json`, `results.pdf`

### 2.4 Update README.md for training focus
```markdown
# JEDCO AI Grant Evaluation — Training Materials

Training slides, mock Arabic applications, and evaluation tools for the JEDCO AI grant management system.

## Contents
- `slides/` — Training presentation outlines
- `docs/` — GitHub Pages (interactive slides)
- `applications/` — 20 mock Arabic grant applications
- `tools/` — batch_evaluate.py, evaluate-pipeline.py
- `handouts/` — Cheatsheets and quick references
- `demos/` — Demo scripts
- `assets/` — JEDCO documents and images

## Live Slides
https://shdaifat.github.io/AgenticGovernment/

## Product Platform
Product development has moved to a private repository.
```

### 2.5 Commit and push
```bash
git add -A
git commit -m "Clean up: training-only repo, remove stale files, update README"
git push origin master
```

### 2.6 Verify GitHub Pages still work
Open https://shdaifat.github.io/AgenticGovernment/ — slides should load unchanged.

**⏸ CHECKPOINT 2: GitHub Pages work? README updated? No product files visible? Proceed.**

---

## Phase 3 — Retire Old Local Folder

### 3.1 Verify both repos work
```bash
# Training (GitHub)
cd c:\Projects\jedco-ai-training
git pull origin master
git log --oneline -3

# Product (Bitbucket)
cd c:\Projects\AgenticGov
git pull origin master
git log --oneline -3
```

### 3.2 Remove old combined folder
```bash
# ⚠ Only after both repos are confirmed working!
# The old folder is no longer needed — everything is in the two new folders.
rm -rf c:\Projects\AgenticGovernment
```

Or rename it as backup:
```bash
mv c:\Projects\AgenticGovernment c:\Projects\AgenticGovernment-ARCHIVE
```

**⏸ CHECKPOINT 3: Both repos confirmed. Old folder archived or removed.**

---

## Final State

```
c:\Projects\
├── jedco-ai-training\           → github.com/shdaifat/AgenticGovernment (PUBLIC)
│   ├── applications\            20 mock Arabic apps
│   ├── assets\                  JEDCO docs
│   ├── demos\                   Demo scripts
│   ├── docs\                    GitHub Pages (interactive slides)
│   ├── handouts\                Cheatsheets
│   ├── slides\                  Training outlines
│   ├── tools\                   batch_evaluate.py, evaluate-pipeline.py
│   ├── PRESENTATION-PLAN.md
│   ├── README.md                Training-focused
│   └── README-AR.md
│
└── AgenticGov\                  → bitbucket.org/bahbish/AgenticGovernment (PRIVATE)
    ├── ROADMAP.md               Product roadmap (6 phases)
    ├── MVP-PLAN.md              Implementation plan (7 steps)
    ├── platform-plan.md         Architecture & pricing
    ├── REPO-SPLIT-PLAN.md       This file
    ├── brainstorming\           Ideas and research
    ├── screenshots\             Product screenshots
    ├── JEDCO-AI-Grant-*         Proposal docs
    ├── README.md                Product-focused
    ├── .gitignore               Simplified
    └── mvp\                     ← Future: product code goes here
        ├── app.py
        ├── ai.py
        ├── pdf.py
        ├── pipeline.py
        ├── static\index.html
        └── system\skills\
```

---

## URL Reference

| What | URL |
|------|-----|
| Training slides (GitHub Pages) | https://shdaifat.github.io/AgenticGovernment/ |
| Training repo (GitHub) | https://github.com/shdaifat/AgenticGovernment |
| Product repo (Bitbucket) | https://bitbucket.org/bahbish/AgenticGovernment |

**Note:** GitHub Pages URL stays the same — no links break.

---

## Bitbucket Authentication

When you `git push` to Bitbucket for the first time, you'll need credentials:
- **HTTPS**: Use an **App Password** (not your login password)
  1. Go to https://bitbucket.org/account/settings/app-passwords/
  2. Create app password with **Repositories: Read + Write** permissions
  3. Username: `bahbish` (workspace name)
  4. Password: the app password you just created
- **SSH** (alternative): Add SSH key at https://bitbucket.org/account/settings/ssh-keys/

---

## Rollback

| Problem | Fix |
|---------|-----|
| Bitbucket repo not needed | Delete at bitbucket.org → Repository Settings → Delete |
| GitHub cleanup went wrong | `cd jedco-ai-training && git revert HEAD && git push` |
| Old folder deleted too early | Product files are on Bitbucket, training files are on GitHub — you can re-clone both |
| Need to move product back to GitHub | Change remote: `git remote set-url origin https://github.com/...` |
