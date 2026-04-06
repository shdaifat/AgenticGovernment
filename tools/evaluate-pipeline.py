"""
JEDCO Automated Application Evaluation Pipeline
================================================
Full end-to-end pipeline that:
  1. Loads application documents from jedco-docs/
  2. Loads the JEDCO eligibility criteria reference
  3. Evaluates each application via local Ollama (no cloud, no internet)
  4. Outputs a ranked decision table as CSV + summary to console

Two modes:
  --mode ollama      Direct Ollama RAG (default, works immediately)
  --mode anythingllm Via AnythingLLM workspace API (requires API key)

Usage:
  python evaluate-pipeline.py
  python evaluate-pipeline.py --mode ollama --apps assets/jedco-docs/
  python evaluate-pipeline.py --mode anythingllm --api-key YOUR_KEY --workspace jedco-application-review

Requirements:
  pip install requests
  Ollama running with qwen3:8b loaded (fallback: qwen2.5:7b)
"""

import requests
import json
import csv
import argparse
import os
import sys
import time
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
OLLAMA_URL       = "http://localhost:11434/api/chat"
OLLAMA_MODEL     = "qwen3:8b"
ANYTHINGLLM_URL  = "http://localhost:3001"
DOCS_DIR         = os.path.join(os.path.dirname(__file__), "..", "assets", "jedco-docs")
OUTPUT_DIR       = os.path.join(os.path.dirname(__file__), "..", "assets", "jedco-docs")

# ── Prompts ──────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """أنت مقيّم محترف في مؤسسة جيدكو الأردنية (JEDCO).
مهمتك تقييم طلبات الاستفادة من برامج الدعم وفق المعايير الرسمية للمؤسسة.
كن دقيقًا وصارمًا. إذا وجدت أي سبب للرفض القاطع، اذكره فورًا.
أجب دائمًا بالتنسيق المطلوب فقط دون مقدمات أو تعليقات إضافية."""

STAGE1_ADMIN_PROMPT = """
=== وثيقة معايير الأهلية ===
{criteria}

=== طلب الاستفادة ===
{application}

مهمتك: التقييم الإداري (المرحلة الأولى)

تحقق مما يلي وأجب بالتنسيق أدناه فقط:

DOCUMENTS_PRESENT: [نعم / لا / جزئي]
MISSING_DOCS: [قائمة المستندات الناقصة أو "لا يوجد"]
COMPANY_TYPE_OK: [نعم / لا] — هل الشركة غير مساهمة عامة؟
SECTOR_ELIGIBLE: [نعم / لا] — هل القطاع مؤهل (غير تجاري/توزيع)؟
OWNERSHIP_OK: [نعم / لا] — هل الملكية خاصة 100%؟
LICENSE_VALID: [نعم / لا / غير محدد] — هل رخصة المهن سارية طوال فترة التنفيذ؟
LICENSE_ISSUE: [وصف المشكلة أو "لا يوجد"]
AGE_OK: [نعم / لا / غير محدد] — هل عمر الشركة مناسب للبرنامج؟
STAGE1_RESULT: [PASS / FAIL / INCOMPLETE]
STAGE1_NOTES: [ملاحظة موجزة بجملة واحدة]
"""

STAGE2_SCORING_PROMPT = """
=== وثيقة معايير التقييم ===
{criteria}

=== طلب الاستفادة ===
{application}

مهمتك: التقييم الفني والمالي (المرحلة الثانية) — أعطِ درجة لكل معيار:

1. الوضع المالي (0-25): الربحية، السيولة، قدرة المساهمة الذاتية
2. جودة المشروع الفني (0-40): الارتباط بأهداف البرنامج، خطة التنفيذ، الجدوى
3. أولوية القطاع (0-20): القطاعات ذات الأولوية تحصل على درجات أعلى
4. الأثر الوطني (0-15): التوظيف، التصدير، التنمية الإقليمية

أجب بهذا التنسيق فقط:
FINANCIAL_SCORE: [0-25]
TECHNICAL_SCORE: [0-40]
SECTOR_SCORE: [0-20]
IMPACT_SCORE: [0-15]
TOTAL_SCORE: [مجموع الأربعة]
RECOMMENDATION: [INVITE / REVIEW / REJECT]
STRENGTHS: [نقطة قوة رئيسية واحدة]
WEAKNESSES: [نقطة ضعف رئيسية واحدة أو "لا يوجد"]
FLAGS: [أي مخاوف خاصة أو "لا يوجد"]
"""

FINAL_SUMMARY_PROMPT = """
=== نتيجة التقييم الإداري ===
{stage1_result}

=== نتيجة التقييم الفني ===
{stage2_result}

=== طلب الاستفادة ===
{application}

بناءً على نتائج المرحلتين، اكتب تقرير تقييم نهائي موجز (4-5 جمل بالعربية) يتضمن:
- القرار النهائي: INVITE / REVIEW / REJECT
- أبرز نقاط القوة
- أبرز المخاوف أو الأسباب إذا كان الرفض
- التوصية للجنة

ابدأ بكلمة القرار مباشرة: INVITE: أو REVIEW: أو REJECT:
"""


# ── Document loaders ──────────────────────────────────────────────────────────
def load_criteria(docs_dir: str) -> str:
    """Load the v2 eligibility criteria reference."""
    path = os.path.join(docs_dir, "JEDCO-eligibility-criteria-reference-v2.txt")
    if not os.path.exists(path):
        # Fall back to v1
        path = os.path.join(docs_dir, "JEDCO-eligibility-criteria-reference.txt")
    if not os.path.exists(path):
        print("WARNING: No criteria reference file found.")
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_applications(docs_dir: str) -> list:
    """
    Load application documents. Supports:
    - .txt files matching 'mock-application-*.txt'
    - .json dataset from generate-mock-applications.py
    """
    apps = []

    # Load structured JSON dataset if exists
    json_path = os.path.join(docs_dir, "mock-applications-dataset.json")
    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as f:
            dataset = json.load(f)
        for item in dataset:
            apps.append({
                "id": item.get("id", "?"),
                "name": item.get("owner_name", "Unknown"),
                "company": item.get("company_name", ""),
                "program": item.get("program", "tattweer"),
                "text": item.get("application_text_ar", ""),
                "source": "generated-dataset",
                "ground_truth_flaw": item.get("deliberate_flaw", ""),
            })
        print(f"  Loaded {len(apps)} applications from dataset JSON")
        return apps

    # Fall back to .txt files
    import glob
    txt_files = sorted(glob.glob(os.path.join(docs_dir, "mock-application-*.txt")))
    for i, fpath in enumerate(txt_files):
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        fname = os.path.basename(fpath)
        prog = "tattweer" if "tattweer" in fname else "start-business"
        apps.append({
            "id": f"APP-MANUAL-{i+1:03d}",
            "name": fname.replace(".txt", ""),
            "company": "",
            "program": prog,
            "text": text,
            "source": fname,
            "ground_truth_flaw": "",
        })
    print(f"  Loaded {len(apps)} applications from .txt files")
    return apps


# ── Ollama caller ─────────────────────────────────────────────────────────────
def _strip_think(text: str) -> str:
    """Remove <think>...</think> blocks produced by Qwen3 thinking mode."""
    import re
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()


def call_ollama(system: str, user: str, model: str = OLLAMA_MODEL,
                temperature: float = 0.1, max_tokens: int = 1500) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=180)
        r.raise_for_status()
        return _strip_think(r.json()["message"]["content"])
    except requests.exceptions.ConnectionError:
        print("\nERROR: Ollama not running. Start it with: ollama serve")
        sys.exit(1)
    except Exception as e:
        return f"ERROR: {e}"


# ── AnythingLLM caller ────────────────────────────────────────────────────────
def call_anythingllm(message: str, workspace_slug: str, api_key: str) -> str:
    url = f"{ANYTHINGLLM_URL}/api/v1/workspace/{workspace_slug}/chat"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "message": message,
        "mode": "chat",
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=180)
        r.raise_for_status()
        data = r.json()
        return data.get("textResponse", data.get("text", str(data)))
    except requests.exceptions.ConnectionError:
        print("\nERROR: AnythingLLM not running at", ANYTHINGLLM_URL)
        sys.exit(1)
    except Exception as e:
        return f"ERROR: {e}"


# ── Parsers ───────────────────────────────────────────────────────────────────
def parse_stage1(text: str) -> dict:
    result = {
        "documents_present": "?", "missing_docs": "?",
        "company_type_ok": "?", "sector_eligible": "?",
        "ownership_ok": "?", "license_valid": "?", "license_issue": "?",
        "age_ok": "?", "stage1_result": "INCOMPLETE", "stage1_notes": "",
    }
    mapping = {
        "DOCUMENTS_PRESENT": "documents_present",
        "MISSING_DOCS": "missing_docs",
        "COMPANY_TYPE_OK": "company_type_ok",
        "SECTOR_ELIGIBLE": "sector_eligible",
        "OWNERSHIP_OK": "ownership_ok",
        "LICENSE_VALID": "license_valid",
        "LICENSE_ISSUE": "license_issue",
        "AGE_OK": "age_ok",
        "STAGE1_RESULT": "stage1_result",
        "STAGE1_NOTES": "stage1_notes",
    }
    for line in text.splitlines():
        for key, field in mapping.items():
            if line.startswith(f"{key}:"):
                result[field] = line.split(":", 1)[1].strip()
    return result


def parse_stage2(text: str) -> dict:
    result = {
        "financial_score": 0, "technical_score": 0,
        "sector_score": 0, "impact_score": 0, "total_score": 0,
        "recommendation": "REVIEW",
        "strengths": "", "weaknesses": "", "flags": "",
    }
    mapping = {
        "FINANCIAL_SCORE": "financial_score",
        "TECHNICAL_SCORE": "technical_score",
        "SECTOR_SCORE": "sector_score",
        "IMPACT_SCORE": "impact_score",
        "TOTAL_SCORE": "total_score",
        "RECOMMENDATION": "recommendation",
        "STRENGTHS": "strengths",
        "WEAKNESSES": "weaknesses",
        "FLAGS": "flags",
    }
    for line in text.splitlines():
        for key, field in mapping.items():
            if line.startswith(f"{key}:"):
                val = line.split(":", 1)[1].strip()
                if field.endswith("_score"):
                    try:
                        result[field] = int(val.split()[0])
                    except (ValueError, IndexError):
                        pass
                else:
                    result[field] = val

    # Recalculate total for integrity
    calc_total = (result["financial_score"] + result["technical_score"] +
                  result["sector_score"] + result["impact_score"])
    if calc_total > 0 and result["total_score"] == 0:
        result["total_score"] = calc_total

    # Apply thresholds
    t = result["total_score"]
    if t >= 70:
        result["recommendation"] = "INVITE"
    elif t >= 50:
        result["recommendation"] = "REVIEW"
    else:
        result["recommendation"] = "REJECT"

    return result


# ── Pipeline stages ───────────────────────────────────────────────────────────
def run_stage1(app: dict, criteria: str, mode: str,
               workspace_slug: str = "", api_key: str = ""):
    """Administrative & financial check."""
    prompt = STAGE1_ADMIN_PROMPT.format(
        criteria=criteria[:12000],  # include program-specific sections
        application=app["text"][:2500],
    )
    if mode == "anythingllm":
        raw = call_anythingllm(prompt, workspace_slug, api_key)
    else:
        raw = call_ollama(SYSTEM_PROMPT, prompt)
    return parse_stage1(raw), raw


def run_stage2(app: dict, criteria: str, mode: str,
               workspace_slug: str = "", api_key: str = ""):
    """Technical & financial scoring."""
    prompt = STAGE2_SCORING_PROMPT.format(
        criteria=criteria[:12000],
        application=app["text"][:2500],
    )
    if mode == "anythingllm":
        raw = call_anythingllm(prompt, workspace_slug, api_key)
    else:
        raw = call_ollama(SYSTEM_PROMPT, prompt, temperature=0.15)
    return parse_stage2(raw), raw


def run_final_summary(app: dict, s1: dict, s2: dict, s1_raw: str, s2_raw: str,
                      mode: str, workspace_slug: str = "", api_key: str = "") -> str:
    """Generate final committee summary."""
    prompt = FINAL_SUMMARY_PROMPT.format(
        stage1_result=s1_raw[:800],
        stage2_result=s2_raw[:800],
        application=app["text"][:1500],
    )
    if mode == "anythingllm":
        return call_anythingllm(prompt, workspace_slug, api_key)
    else:
        return call_ollama(SYSTEM_PROMPT, prompt, temperature=0.3, max_tokens=300)


# ── Main pipeline ─────────────────────────────────────────────────────────────
def evaluate_application(app: dict, criteria: str, args) -> dict:
    app_id = app["id"]
    name = app["name"][:30]

    print(f"\n{'─'*60}")
    print(f"  Application : {app_id}")
    print(f"  Applicant   : {name}")
    print(f"  Program     : {app['program']}")

    # Stage 1 — Admin check
    print(f"  Stage 1     : Administrative check...", end=" ", flush=True)
    s1, s1_raw = run_stage1(app, criteria, args.mode,
                            getattr(args, "workspace", ""),
                            getattr(args, "api_key", ""))
    s1_result = s1.get("stage1_result", "INCOMPLETE")
    print(f"{s1_result}")

    if s1.get("license_issue") and s1["license_issue"] not in ("لا يوجد", "none", "None", "?", ""):
        print(f"  ⚠ License   : {s1['license_issue']}")

    # Stage 2 — Scoring (skip if hard FAIL in stage 1)
    if s1_result == "FAIL":
        s2 = {"financial_score": 0, "technical_score": 0, "sector_score": 0,
              "impact_score": 0, "total_score": 0, "recommendation": "REJECT",
              "strengths": "—", "weaknesses": "فشل في التقييم الإداري", "flags": s1.get("stage1_notes", "")}
        s2_raw = "Skipped — Stage 1 FAIL"
        summary = f"REJECT: {s1.get('stage1_notes', 'رفض إداري')}"
        print(f"  Stage 2     : SKIPPED (hard fail)")
    else:
        print(f"  Stage 2     : Technical scoring...", end=" ", flush=True)
        s2, s2_raw = run_stage2(app, criteria, args.mode,
                                getattr(args, "workspace", ""),
                                getattr(args, "api_key", ""))
        print(f"score={s2['total_score']}/100 → {s2['recommendation']}")

        if args.summary:
            print(f"  Summary     : Generating...", end=" ", flush=True)
            summary = run_final_summary(app, s1, s2, s1_raw, s2_raw, args.mode,
                                        getattr(args, "workspace", ""),
                                        getattr(args, "api_key", ""))
            print("done")
        else:
            summary = ""

    return {
        "app_id": app_id,
        "applicant": app["name"],
        "company": app.get("company", ""),
        "program": app["program"],
        # Stage 1
        "s1_result": s1_result,
        "s1_docs_present": s1.get("documents_present", "?"),
        "s1_missing_docs": s1.get("missing_docs", "?"),
        "s1_license_valid": s1.get("license_valid", "?"),
        "s1_license_issue": s1.get("license_issue", ""),
        "s1_sector_ok": s1.get("sector_eligible", "?"),
        "s1_notes": s1.get("stage1_notes", ""),
        # Stage 2
        "score_financial_25": s2["financial_score"],
        "score_technical_40": s2["technical_score"],
        "score_sector_20": s2["sector_score"],
        "score_impact_15": s2["impact_score"],
        "total_score_100": s2["total_score"],
        "recommendation": s2["recommendation"],
        "strengths": s2.get("strengths", ""),
        "weaknesses": s2.get("weaknesses", ""),
        "flags": s2.get("flags", ""),
        "final_summary": summary,
        # Ground truth (hidden from reviewers in production)
        "ground_truth_flaw": app.get("ground_truth_flaw", ""),
    }


def main():
    global OLLAMA_MODEL
    parser = argparse.ArgumentParser(description="JEDCO Automated Application Evaluation Pipeline")
    parser.add_argument("--mode", choices=["ollama", "anythingllm"], default="ollama",
                        help="Inference mode (default: ollama)")
    parser.add_argument("--apps", type=str, default=DOCS_DIR,
                        help="Directory containing application files")
    parser.add_argument("--model", type=str, default=OLLAMA_MODEL,
                        help=f"Ollama model name (default: {OLLAMA_MODEL})")
    parser.add_argument("--api-key", type=str, default="",
                        help="AnythingLLM API key (for --mode anythingllm)")
    parser.add_argument("--workspace", type=str, default="jedco-application-review",
                        help="AnythingLLM workspace slug")
    parser.add_argument("--output", type=str,
                        default=os.path.join(OUTPUT_DIR, "pipeline-results.csv"),
                        help="Output CSV path")
    parser.add_argument("--summary", action="store_true",
                        help="Generate Arabic summary per application (slower)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit to N applications (0 = all)")
    args = parser.parse_args()

    OLLAMA_MODEL = args.model

    print(f"\n{'='*60}")
    print(f"JEDCO APPLICATION EVALUATION PIPELINE")
    print(f"{'='*60}")
    print(f"  Mode      : {args.mode}")
    print(f"  Model     : {OLLAMA_MODEL}")
    print(f"  Docs dir  : {args.apps}")
    print(f"  Output    : {args.output}")
    print(f"  Summary   : {'yes' if args.summary else 'no'}")

    # Verify backend
    if args.mode == "ollama":
        try:
            requests.get("http://localhost:11434/", timeout=5)
            print(f"  Ollama    : CONNECTED ✓")
        except:
            print("  ERROR: Ollama not reachable. Run: ollama serve")
            sys.exit(1)
    else:
        if not args.api_key:
            print("\nERROR: --api-key required for AnythingLLM mode")
            print("Get it from: AnythingLLM → Settings → API Keys → Generate")
            sys.exit(1)
        try:
            r = requests.get(f"{ANYTHINGLLM_URL}/api/health", timeout=5)
            print(f"  AnythingLLM: CONNECTED ✓ (port 3001)")
        except:
            print("  ERROR: AnythingLLM not reachable at port 3001")
            sys.exit(1)

    # Load data
    print(f"\nLoading documents...")
    criteria = load_criteria(args.apps)
    if criteria:
        print(f"  Criteria  : {len(criteria)} chars loaded")
    applications = load_applications(args.apps)
    if not applications:
        print("ERROR: No applications found. Run generate-mock-applications.py first.")
        sys.exit(1)

    if args.limit > 0:
        applications = applications[:args.limit]
        print(f"  Limit     : {args.limit} applications")

    # Run pipeline
    print(f"\nProcessing {len(applications)} applications...")
    results = []
    for app in applications:
        result = evaluate_application(app, criteria, args)
        results.append(result)
        time.sleep(0.5)

    # Sort by recommendation and score
    order = {"INVITE": 0, "REVIEW": 1, "REJECT": 2}
    results.sort(key=lambda r: (order.get(r["recommendation"], 3), -r["total_score_100"]))
    for i, r in enumerate(results):
        r["rank"] = i + 1

    # Write CSV
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    fieldnames = ["rank"] + [k for k in results[0].keys() if k != "rank"]
    with open(args.output, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(results)

    # Summary table
    invite = [r for r in results if r["recommendation"] == "INVITE"]
    review = [r for r in results if r["recommendation"] == "REVIEW"]
    reject = [r for r in results if r["recommendation"] == "REJECT"]

    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE — {len(results)} applications evaluated")
    print(f"{'='*60}")
    print(f"  INVITE  : {len(invite)}")
    print(f"  REVIEW  : {len(review)}")
    print(f"  REJECT  : {len(reject)}")

    print(f"\nTop applications:")
    print(f"  {'#':<3} {'Score':>5}  {'Rec':<8}  {'S1':<5}  Applicant")
    print(f"  {'─'*50}")
    for r in results[:min(10, len(results))]:
        print(f"  {r['rank']:<3} {r['total_score_100']:>5}  {r['recommendation']:<8}  {r['s1_result']:<5}  {r['applicant'][:30]}")

    if reject:
        print(f"\nRejected applications:")
        for r in [x for x in results if x['recommendation'] == 'REJECT']:
            reason = r['s1_notes'] or r['flags'] or r['weaknesses']
            print(f"  ✗ {r['applicant'][:30]} — {reason[:60]}")

    print(f"\nResults saved to: {args.output}")
    print(f"\nNext: open {os.path.basename(args.output)} in Excel for the ranked shortlist")


if __name__ == "__main__":
    main()
