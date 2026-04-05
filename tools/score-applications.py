"""
JEDCO Application Scoring & Ranking Engine
===========================================
Reads the mock applications JSON produced by generate-mock-applications.py,
scores each one against JEDCO's published evaluation criteria using the local LLM,
and outputs a ranked CSV ready for committee review.

Usage:
    python score-applications.py
    python score-applications.py --input ../assets/jedco-docs/mock-applications-dataset.json
    python score-applications.py --input dataset.json --output ranked-results.csv --explain

Output:
    ranked-results.csv  — ranked shortlist with scores per criterion
    evaluation-log.json — full LLM reasoning per application (with --explain)

Scoring Rubric (Tattweer program — based on JEDCO published evaluation methodology):
    1. Sector priority            (20 pts) — priority sectors score higher
    2. Employment creation        (25 pts) — new jobs created
    3. Innovation / productivity  (20 pts) — technology, process improvement
    4. Financial capacity         (20 pts) — co-investment, own funds, revenue
    5. Documentation quality      (15 pts) — completeness, clarity, business plan
    -----------------------------------------------------------------------
    TOTAL                        (100 pts)

    INVITE threshold   : >= 70 pts
    HUMAN REVIEW band  : 50-69 pts
    FLAG REJECT        : < 50 pts or any HARD FAIL (officer confirms)
"""

import requests
import json
import csv
import argparse
import sys
import time
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

# Hard disqualifiers — flag for officer confirmation on any match
HARD_FAIL_FLAWS = [
    "قطاع_مستبعد",
    "ملكية_اجنبية",
    "شركة_مساهمة_عامة",
    "رخصة_منتهية",
    "عمر_مشروع_اكبر_من_سنتين",
    "تسجيل_ناقص",
]

# Score thresholds
INVITE_THRESHOLD = 70
REVIEW_THRESHOLD = 50

SCORING_PROMPT = """أنت مقيّم محترف في مؤسسة جيدكو. قيّم الطلب التالي وفق معايير برنامج تطوير الأعمال.

نص الطلب:
{application_text}

معلومات إضافية:
- القطاع: {sector}
- المحافظة: {governorate}
- المبلغ المطلوب: {grant_amount} دينار (من إجمالي {total_cost} دينار)
- عدد الموظفين الحاليين: {employees}
- رخصة الأعمال سارية حتى: {license_expiry}

قيّم الطلب وفق المعايير التالية. أعطِ درجة لكل معيار بين 0 و العلامة القصوى فقط:

1. أولوية القطاع (0-20): هل يندرج تحت القطاعات ذات الأولوية؟ (صناعة، تكنولوجيا، دواء، غذاء، نسيج)
2. التشغيل وفرص العمل (0-25): ما حجم الوظائف الجديدة المتوقعة؟
3. الابتكار والإنتاجية (0-20): هل يتضمن تقنية جديدة أو تحسين إنتاجية قابل للقياس؟
4. القدرة المالية (0-20): هل المساهمة الذاتية كافية؟ هل الشركة مستقرة ماليًا؟
5. جودة التوثيق (0-15): هل الطلب مكتمل وواضح ومقنع؟

أجب بالتنسيق التالي فقط — لا تضف نصًا إضافيًا:
SECTOR_SCORE: [رقم]
EMPLOYMENT_SCORE: [رقم]
INNOVATION_SCORE: [رقم]
FINANCIAL_SCORE: [رقم]
DOCUMENTATION_SCORE: [رقم]
RECOMMENDATION: [INVITE أو REVIEW أو FLAG_REJECT]
REASON: [سبب موجز بجملة واحدة بالعربية]
FLAGS: [أي مخاوف واضحة، أو "لا يوجد"]"""


SCORING_PROMPT_EN = """You are a professional JEDCO program evaluator. Score the following application.

Application text (Arabic):
{application_text}

Additional data:
- Sector: {sector}
- Governorate: {governorate}  
- Grant requested: {grant_amount} JOD (of {total_cost} JOD total project)
- Current employees: {employees}
- Operating license valid until: {license_expiry}

Score each criterion — give a number between 0 and the maximum shown:

1. Sector Priority (0-20): Is this a priority sector? (manufacturing, ICT, pharma, food, textiles)
2. Employment Creation (0-25): How many new jobs will be created?
3. Innovation/Productivity (0-20): Does it include new technology or measurable productivity gain?
4. Financial Capacity (0-20): Is the co-investment adequate? Is the company financially stable?
5. Documentation Quality (0-15): Is the application complete, clear, and convincing?

Respond in this EXACT format only — no extra text:
SECTOR_SCORE: [number]
EMPLOYMENT_SCORE: [number]
INNOVATION_SCORE: [number]
FINANCIAL_SCORE: [number]
DOCUMENTATION_SCORE: [number]
RECOMMENDATION: [INVITE or REVIEW or FLAG_REJECT]
REASON: [one sentence in Arabic]
FLAGS: [any obvious concerns, or "none"]"""


def call_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 300}  # low temp for consistent scoring
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        print("  ERROR: Cannot connect to Ollama at", OLLAMA_URL)
        sys.exit(1)
    except Exception as e:
        return f"ERROR: {e}"


def parse_scores(llm_output: str) -> dict:
    """Parse the structured LLM response into a scores dict."""
    scores = {
        "sector": 0, "employment": 0, "innovation": 0,
        "financial": 0, "documentation": 0,
        "recommendation": "REVIEW", "reason": "", "flags": ""
    }
    for line in llm_output.splitlines():
        line = line.strip()
        try:
            if line.startswith("SECTOR_SCORE:"):
                scores["sector"] = int(line.split(":")[1].strip())
            elif line.startswith("EMPLOYMENT_SCORE:"):
                scores["employment"] = int(line.split(":")[1].strip())
            elif line.startswith("INNOVATION_SCORE:"):
                scores["innovation"] = int(line.split(":")[1].strip())
            elif line.startswith("FINANCIAL_SCORE:"):
                scores["financial"] = int(line.split(":")[1].strip())
            elif line.startswith("DOCUMENTATION_SCORE:"):
                scores["documentation"] = int(line.split(":")[1].strip())
            elif line.startswith("RECOMMENDATION:"):
                scores["recommendation"] = line.split(":", 1)[1].strip()
            elif line.startswith("REASON:"):
                scores["reason"] = line.split(":", 1)[1].strip()
            elif line.startswith("FLAGS:"):
                scores["flags"] = line.split(":", 1)[1].strip()
        except (ValueError, IndexError):
            pass
    scores["total"] = (scores["sector"] + scores["employment"] +
                       scores["innovation"] + scores["financial"] +
                       scores["documentation"])
    return scores


def score_application(app: dict, use_english_prompt: bool = False) -> dict:
    """Score a single application."""
    app_id = app.get("id", "?")
    flaw = app.get("deliberate_flaw", "لا_عيب")

    # Hard fail check — flag for officer review, no LLM needed
    if flaw in HARD_FAIL_FLAWS:
        print(f"  [{app_id}] HARD FAIL ({flaw}) — flagged for officer review")
        return {
            "sector": 0, "employment": 0, "innovation": 0,
            "financial": 0, "documentation": 0,
            "total": 0,
            "recommendation": "FLAG_REJECT",
            "reason": f"إحالة للمسؤول: {flaw.replace('_', ' ')}",
            "flags": flaw,
            "hard_fail": True,
            "llm_output": None,
        }

    prompt_template = SCORING_PROMPT_EN if use_english_prompt else SCORING_PROMPT
    prompt = prompt_template.format(
        application_text=app.get("application_text_ar", "")[:2000],  # truncate for context window
        sector=app.get("sector", "غير محدد"),
        governorate=app.get("governorate", "غير محدد"),
        grant_amount=f"{app.get('requested_grant_jod', 0):,}",
        total_cost=f"{app.get('total_project_cost_jod', 0):,}",
        employees=app.get("employees", 0) or "غير محدد",
        license_expiry=app.get("license_expiry", "غير محدد") or "غير محدد",
    )

    print(f"  [{app_id}] Scoring ({app.get('program','?')})...", end=" ", flush=True)
    llm_output = call_ollama(prompt)
    scores = parse_scores(llm_output)
    scores["hard_fail"] = False
    scores["llm_output"] = llm_output

    # Override recommendation based on threshold
    total = scores["total"]
    if total >= INVITE_THRESHOLD:
        scores["recommendation"] = "INVITE"
    elif total >= REVIEW_THRESHOLD:
        scores["recommendation"] = "REVIEW"
    else:
        scores["recommendation"] = "FLAG_REJECT"

    print(f"score={total}/100 → {scores['recommendation']}")
    return scores


def main():
    global MODEL  # noqa: PLW0603
    parser = argparse.ArgumentParser(description="Score and rank JEDCO grant applications")
    parser.add_argument("--input", type=str,
                        default="../assets/jedco-docs/mock-applications-dataset.json")
    parser.add_argument("--output", type=str,
                        default="../assets/jedco-docs/ranked-applications.csv")
    parser.add_argument("--explain", action="store_true",
                        help="Also save full LLM reasoning to evaluation-log.json")
    parser.add_argument("--model", type=str, default=MODEL)
    parser.add_argument("--english-prompt", action="store_true",
                        help="Use English scoring prompt instead of Arabic")
    args = parser.parse_args()
    MODEL = args.model

    # Resolve paths relative to this script
    base = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.abspath(os.path.join(base, args.input))
    output_path = os.path.abspath(os.path.join(base, args.output))

    print(f"\nJEDCO Application Scoring Engine")
    print(f"  Model : {MODEL}")
    print(f"  Input : {input_path}")
    print(f"  Output: {output_path}\n")

    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        print("Run generate-mock-applications.py first.")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        applications = json.load(f)

    print(f"Loaded {len(applications)} applications\n")

    results = []
    log = []

    for app in applications:
        scores = score_application(app, use_english_prompt=args.english_prompt)

        row = {
            "rank": None,  # filled after sorting
            "app_id": app.get("id"),
            "program": app.get("program"),
            "owner_name": app.get("owner_name"),
            "company_name": app.get("company_name", ""),
            "governorate": app.get("governorate"),
            "sector": app.get("sector"),
            "grant_requested_jod": app.get("requested_grant_jod"),
            "score_sector_20": scores["sector"],
            "score_employment_25": scores["employment"],
            "score_innovation_20": scores["innovation"],
            "score_financial_20": scores["financial"],
            "score_documentation_15": scores["documentation"],
            "total_score_100": scores["total"],
            "recommendation": scores["recommendation"],
            "hard_fail": scores["hard_fail"],
            "flags": scores["flags"],
            "reason": scores["reason"],
            # Ground truth — in real use this column would be hidden from reviewers
            "ground_truth_flaw": app.get("deliberate_flaw"),
        }
        results.append(row)

        if args.explain:
            log.append({**app, "scores": scores})

        time.sleep(0.5)

    # Sort: INVITE first, then REVIEW, then FLAG_REJECT, within each by total score descending
    order = {"INVITE": 0, "REVIEW": 1, "FLAG_REJECT": 2}
    results.sort(key=lambda r: (order.get(r["recommendation"], 3), -r["total_score_100"]))
    for i, r in enumerate(results):
        r["rank"] = i + 1

    # Write CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = list(results[0].keys())
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # Write explain log
    if args.explain:
        log_path = output_path.replace(".csv", "-llm-log.json")
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        print(f"\n  LLM log saved: {log_path}")

    # Print summary table
    invite = [r for r in results if r["recommendation"] == "INVITE"]
    review = [r for r in results if r["recommendation"] == "REVIEW"]
    reject = [r for r in results if r["recommendation"] == "FLAG_REJECT"]

    print(f"\n{'='*60}")
    print(f"SCORING COMPLETE — {len(results)} applications")
    print(f"{'='*60}")
    print(f"  INVITE      : {len(invite)}")
    print(f"  REVIEW      : {len(review)}")
    print(f"  FLAG_REJECT : {len(reject)} (officer confirms)")
    print(f"\nTop 5 Applications:")
    print(f"{'Rank':<5} {'ID':<16} {'Score':>5} {'Rec':<8} {'Applicant'}")
    print("-" * 60)
    for r in results[:5]:
        print(f"  {r['rank']:<4} {r['app_id']:<16} {r['total_score_100']:>5}  {r['recommendation']:<8} {r['owner_name']}")
    print(f"\nFull ranked list saved to: {output_path}")


if __name__ == "__main__":
    main()
