"""
JEDCO Mock Application Generator
==================================
Uses local Ollama (qwen2.5:7b) to generate realistic fictional grant applications
for JEDCO programs to use as training demo data.

Usage:
    python generate-mock-applications.py
    python generate-mock-applications.py --count 20 --program tattweer
    python generate-mock-applications.py --count 50 --program all --output ../assets/jedco-docs/mock-dataset.json

Requirements:
    pip install requests
    Ollama running locally: ollama serve & ollama run qwen2.5:7b

Programs supported:
    tattweer       - Business development/expansion grants (up to 50,000 JOD, 70%)
    start-business - New startup grants (up to 35,000 JOD, 70%)
    tamkeen        - Employment support grants
    all            - Mix of all three

Output format: JSON array of application objects
Each application includes deliberate flaws in ~30% of cases for demo purposes.
"""

import requests
import json
import random
import argparse
import sys
import time
from datetime import datetime, timedelta

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

# Seed data for variation
JORDANIAN_GOVERNORATES = [
    "عمّان", "إربد", "الزرقاء", "العقبة", "مادبا",
    "الكرك", "البلقاء", "المفرق", "جرش", "عجلون", "الطفيلة", "معان"
]

PRIORITY_SECTORS = [
    "صناعة غذائية", "تكنولوجيا المعلومات", "صناعة دوائية",
    "صناعة نسيجية", "صناعة بلاستيكية", "خدمات صحية",
    "زراعة تقنية", "صناعة ورقية وطباعة", "صناعة إنشائية"
]

LOW_PRIORITY_SECTORS = [
    "تجارة عامة", "مطاعم وفعاليات", "وكالات سيارات",
    "استيراد وتوزيع", "عقارات"
]

FLAW_TYPES = {
    "tattweer": [
        "رخصة_منتهية",        # Operating license expires during project
        "قطاع_مستبعد",        # Excluded sector (trading/retail)
        "ملكية_اجنبية",       # Foreign majority ownership
        "شركة_مساهمة_عامة",   # Public shareholding company (excluded)
        "لا_عيب",             # No flaw — clean application
    ],
    "start-business": [
        "عمر_مشروع_اكبر_من_سنتين",  # Business older than 2 years (not a fresh start)
        "تسجيل_ناقص",               # Missing commercial registration
        "خطة_عمل_ضعيفة",            # Weak business plan (no market analysis)
        "لا_عيب",
    ],
    "tamkeen": [
        "عمال_اجانب_بنسبة_عالية",   # High % of non-Jordanian workers
        "لا_تزيد_الرواتب_عن_الحد",  # Salaries at minimum wage only
        "لا_عيب",
    ]
}

TATTWEER_PROMPT_TEMPLATE = """أنت خبير في تقديم طلبات المنح الحكومية في الأردن. اكتب طلب منحة وهمي (خيالي) ببرنامج تطوير من مؤسسة جيدكو.

المعطيات:
- اسم الشركة: {company_name}
- اسم صاحب المشروع: {owner_name}
- المحافظة: {governorate}
- القطاع: {sector}
- عدد الموظفين الحاليين: {employees}
- الإيرادات السنوية بالدينار: {revenue}
- عمر الشركة: {age} سنوات
- المبلغ المطلوب: {grant_amount} دينار أردني
- إجمالي كلفة المشروع: {total_cost} دينار
- تاريخ انتهاء رخصة الأعمال: {license_expiry}
- ملاحظة داخلية للمولّد: {flaw_note}

اكتب الطلب بالعربية بصيغة رسمية. ابدأ بـ"طلب استفادة من برنامج تطوير الأعمال". تضمّن: وصف الشركة، وصف المشروع المقترح، الأهداف (توظيف، إنتاج، تصدير)، الجدول الزمني (12 شهرًا)، وتفاصيل ميزانية المشروع. الطلب يجب أن يكون 3-4 فقرات فقط، رسمي ومقنع.

مهم: لا تذكر الملاحظة الداخلية صراحةً في النص إذا كانت تشير لعيب — فقط اجعل البيانات تعكسه ضمنيًا."""

START_BUSINESS_PROMPT_TEMPLATE = """أنت خبير في تقديم طلبات المنح الحكومية في الأردن. اكتب طلب منحة وهمي (خيالي) لبرنامج "اعمل مشروعك" من مؤسسة جيدكو.

المعطيات:
- اسم صاحب الفكرة: {owner_name}
- المحافظة: {governorate}
- قطاع الفكرة: {sector}
- وصف المشروع المقترح: {project_idea}
- المبلغ المطلوب: {grant_amount} دينار أردني
- المساهمة الذاتية: {own_contribution} دينار
- ملاحظة للمولّد: {flaw_note}

اكتب الطلب بالعربية بصيغة رسمية. تضمّن: الفكرة ووصفها، الفئة المستهدفة، الإيرادات المتوقعة خلال السنة الأولى، عدد الوظائف المتوقعة، مؤهلات مقدم الطلب. 3 فقرات فقط.

مهم: لا تذكر الملاحظة الداخلية صراحةً إذا كانت تشير لعيب."""


def generate_applicant_data(program: str, flaw: str) -> dict:
    """Generate seed data for one application."""
    owner_first = random.choice(["أحمد", "محمد", "خالد", "عمر", "يوسف",
                                  "فاطمة", "زهراء", "نور", "ريم", "سارة"])
    owner_last = random.choice(["الخالدي", "العبادي", "الزعبي", "حداد",
                                 "النسور", "الرشيد", "طوالبة", "المومني",
                                 "الشوابكة", "بني هاني"])
    owner = f"{owner_first} {owner_last}"

    gov = random.choice(JORDANIAN_GOVERNORATES)

    if flaw == "قطاع_مستبعد":
        sector = random.choice(LOW_PRIORITY_SECTORS)
    else:
        sector = random.choice(PRIORITY_SECTORS)

    company_suffixes = ["للصناعة", "للتجارة والصناعة", "للتقنية", "للإنتاج والتطوير"]
    company = f"شركة {owner_last} {random.choice(company_suffixes)}"

    # License expiry — key flaw trigger
    if flaw == "رخصة_منتهية":
        expiry = "31/12/2026"   # contract signed ~Sep 2026, expires before project end
    else:
        expiry = f"31/12/202{random.randint(7,9)}"

    employees = random.randint(5, 45)
    revenue = random.randint(80, 500) * 1000

    if program == "tattweer":
        total_cost = random.randint(30, 71) * 1000
        grant = min(int(total_cost * 0.70), 50000)
        age = random.randint(3, 15) if flaw != "عمر_مشروع_اكبر_من_سنتين" else random.randint(3, 10)
    else:
        total_cost = random.randint(20, 50) * 1000
        grant = min(int(total_cost * 0.70), 35000)
        age = 0

    own = total_cost - grant

    flaw_notes = {
        "رخصة_منتهية": f"رخصة الأعمال تنتهي في {expiry} وهو قبل انتهاء فترة التنفيذ المقدرة بـ12 شهرًا من وقت التوقيع",
        "قطاع_مستبعد": "القطاع المذكور مستبعد من برامج الدعم الصناعي (تجارة/توزيع)",
        "ملكية_اجنبية": "الشريك الأجنبي يملك 55% من الشركة — يتجاوز حد 49%",
        "شركة_مساهمة_عامة": "الشركة مدرجة في بورصة عمّان — مستبعدة من البرنامج",
        "لا_عيب": "طلب مكتمل وسليم — جميع الشروط متوفرة",
        "عمر_مشروع_اكبر_من_سنتين": "المشروع مسجل منذ أكثر من سنتين — لا يُعدّ مشروعًا ناشئًا جديدًا",
        "تسجيل_ناقص": "لم يُقدّم شهادة تسجيل لدى وزارة الصناعة والتجارة",
        "خطة_عمل_ضعيفة": "خطة العمل لا تتضمن دراسة جدوى اقتصادية أو تحليل سوق",
        "عمال_اجانب_بنسبة_عالية": "نسبة العمال الأردنيين أقل من 50%",
        "لا_تزيد_الرواتب_عن_الحد": "الرواتب المقترحة عند الحد الأدنى فقط — لا تحسين فعلي",
    }

    project_ideas = [
        "تأسيس مشغل خياطة وتصميم أزياء محلية مع منصة بيع إلكترونية",
        "إنتاج وتعبئة منتجات غذائية منزلية (مربى، مخلل، زيت زيتون)",
        "تطوير تطبيق خدمات منزلية للمحافظات",
        "ورشة صيانة معدات زراعية مع تدريب مزارعين",
        "استوديو تصميم جرافيك ومحتوى رقمي للشركات الصغيرة",
    ]

    return {
        "owner": owner,
        "company": company,
        "gov": gov,
        "sector": sector,
        "employees": employees,
        "revenue": revenue,
        "age": age,
        "license_expiry": expiry,
        "grant": grant,
        "total_cost": total_cost,
        "own": own,
        "flaw": flaw,
        "flaw_note": flaw_notes.get(flaw, "لا ملاحظات"),
        "project_idea": random.choice(project_ideas),
    }


def call_ollama(prompt: str, retries: int = 2) -> str:
    """Call local Ollama API and return the text response."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.8, "num_predict": 600}
    }
    for attempt in range(retries + 1):
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=120)
            r.raise_for_status()
            return r.json()["message"]["content"].strip()
        except requests.exceptions.ConnectionError:
            print("  ERROR: Cannot connect to Ollama. Is it running? Try: ollama serve")
            sys.exit(1)
        except Exception as e:
            if attempt < retries:
                print(f"  Retrying ({attempt+1}/{retries})...")
                time.sleep(3)
            else:
                return f"[ERROR generating application: {e}]"


def generate_one(program: str, index: int, flaw: str) -> dict:
    """Generate a single mock application."""
    data = generate_applicant_data(program, flaw)

    if program == "tattweer":
        prompt = TATTWEER_PROMPT_TEMPLATE.format(
            company_name=data["company"],
            owner_name=data["owner"],
            governorate=data["gov"],
            sector=data["sector"],
            employees=data["employees"],
            revenue=f"{data['revenue']:,}",
            age=data["age"],
            grant_amount=f"{data['grant']:,}",
            total_cost=f"{data['total_cost']:,}",
            license_expiry=data["license_expiry"],
            flaw_note=data["flaw_note"],
        )
    else:
        prompt = START_BUSINESS_PROMPT_TEMPLATE.format(
            owner_name=data["owner"],
            governorate=data["gov"],
            sector=data["sector"],
            project_idea=data["project_idea"],
            grant_amount=f"{data['grant']:,}",
            own_contribution=f"{data['own']:,}",
            flaw_note=data["flaw_note"],
        )

    print(f"  [{index+1}] Generating {program} app ({flaw})...", end=" ", flush=True)
    text = call_ollama(prompt)
    print("done")

    return {
        "id": f"APP-{datetime.now().strftime('%Y')}-{index+1:04d}",
        "program": program,
        "owner_name": data["owner"],
        "company_name": data["company"] if program == "tattweer" else None,
        "governorate": data["gov"],
        "sector": data["sector"],
        "employees": data["employees"] if program == "tattweer" else None,
        "annual_revenue_jod": data["revenue"] if program == "tattweer" else None,
        "business_age_years": data["age"] if program == "tattweer" else None,
        "requested_grant_jod": data["grant"],
        "total_project_cost_jod": data["total_cost"],
        "own_contribution_jod": data["own"],
        "license_expiry": data["license_expiry"] if program == "tattweer" else None,
        "deliberate_flaw": data["flaw"],     # GROUND TRUTH — for evaluation only
        "application_text_ar": text,
        "generated_at": datetime.now().isoformat(),
    }


def main():
    global MODEL  # noqa: PLW0603
    parser = argparse.ArgumentParser(description="Generate mock JEDCO grant applications using local LLM")
    parser.add_argument("--count", type=int, default=10, help="Number of applications (default: 10)")
    parser.add_argument("--program", choices=["tattweer", "start-business", "tamkeen", "all"],
                        default="tattweer", help="Program to generate for (default: tattweer)")
    parser.add_argument("--output", type=str,
                        default="../assets/jedco-docs/mock-applications-dataset.json",
                        help="Output JSON file path")
    parser.add_argument("--model", type=str, default=MODEL, help=f"Ollama model (default: {MODEL})")
    args = parser.parse_args()
    MODEL = args.model

    print(f"\nJEDCO Mock Application Generator")
    print(f"  Model : {MODEL}")
    print(f"  Count : {args.count}")
    print(f"  Program: {args.program}")
    print(f"  Output: {args.output}")
    print(f"  Ollama: {OLLAMA_URL}\n")

    # Verify Ollama is reachable
    try:
        ping = requests.get("http://localhost:11434/", timeout=5)
        print("  Ollama: CONNECTED\n")
    except:
        print("  ERROR: Ollama not reachable at localhost:11434")
        print("  Run: ollama serve")
        sys.exit(1)

    applications = []

    for i in range(args.count):
        # Determine program for this iteration
        if args.program == "all":
            prog = random.choice(["tattweer", "start-business", "tattweer"])  # weight toward tattweer
        else:
            prog = args.program

        # Assign flaws — ~30% have a flaw, ~70% are clean
        flaws = FLAW_TYPES.get(prog, ["لا_عيب"])
        roll = random.random()
        if roll < 0.70:
            flaw = "لا_عيب"
        else:
            flaw = random.choice([f for f in flaws if f != "لا_عيب"])

        app = generate_one(prog, i, flaw)
        applications.append(app)

        # Small pause to avoid overloading local model
        if i < args.count - 1:
            time.sleep(1)

    # Save output
    import os
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), args.output))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(applications, f, ensure_ascii=False, indent=2)

    # Summary
    total = len(applications)
    flawed = sum(1 for a in applications if a["deliberate_flaw"] != "لا_عيب")
    print(f"\nDone!")
    print(f"  Generated : {total} applications")
    print(f"  Clean     : {total - flawed}")
    print(f"  With flaws: {flawed}")
    print(f"  Saved to  : {output_path}")
    print(f"\nNext step: run score-applications.py --input {output_path}")


if __name__ == "__main__":
    main()
