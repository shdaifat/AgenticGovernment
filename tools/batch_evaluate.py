#!/usr/bin/env python3
"""
batch_evaluate.py — Evaluate JEDCO grant applications using Ollama (local LLM).

Usage:
    python batch_evaluate.py                    # Evaluate all apps in ../applications/
    python batch_evaluate.py --model qwen3:8b   # Use a specific model
    python batch_evaluate.py --output results   # Output to results/ folder

Requires: pip install requests
Requires: Ollama running locally (ollama serve)
"""

import argparse
import json
import os
import glob
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

OLLAMA_URL = "http://localhost:11434/api/generate"

EVALUATION_PROMPT = """أنت موظف تقييم في المؤسسة الأردنية لتطوير المشاريع الاقتصادية (JEDCO).
مهمتك تطبيق شروط برنامج "ارفع قدراتك بالتسويق" بصرامة تامة على الطلب المقدَّم أدناه.

شروط الأهلية الإلزامية:
١. تسجيل الشركة — مسجلة رسمياً في الأردن، ليست مساهمة عامة
٢. عمر الشركة — سنتان أو أكثر عند التقديم
٣. الملكية — خاصة 100%، أردنية ≥ 51%
٤. عدد الموظفين — 1 إلى 249 حسب الضمان الاجتماعي
٥. نسبة التمويل — لا تتجاوز 70% من إجمالي التكاليف
٦. الحالة مع JEDCO — أغلقت جميع ملفات المنح السابقة
القطاعات المؤهلة: صناعي · حرفي · زراعي · خدمي (يُستثنى التجاري)

قواعد العمل:
- إذا لم يستوفِ الطلب أي شرط إلزامي → رفض فوري
- لا تضف رأياً شخصياً أو تقييماً خارج الشروط المحددة

--- بداية الطلب ---
{application_text}
--- نهاية الطلب ---

أجب بهذا التنسيق بالضبط (JSON):
{{
  "company_name": "اسم الشركة",
  "registration": "نعم أو لا",
  "company_age": "نعم أو لا",
  "ownership": "نعم أو لا",
  "employees": "نعم أو لا",
  "funding_ratio": "نعم أو لا",
  "previous_files": "نعم أو لا",
  "sector_eligible": "نعم أو لا",
  "decision": "مقبول أو مرفوض",
  "reason": "سبب القرار في جملة واحدة"
}}

لا تكتب أي كلام قبل أو بعد الـ JSON."""


def evaluate_application(app_text, model):
    """Send one application to Ollama for evaluation."""
    prompt = EVALUATION_PROMPT.format(application_text=app_text)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 500},
    }

    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()

    raw = resp.json().get("response", "")
    # Strip <think>...</think> tags if present (Qwen3 reasoning)
    import re
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()

    # Extract JSON from response
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(raw[start:end])
    else:
        return {"error": "Could not parse JSON", "raw_response": raw[:500]}


def generate_html_report(results, output_dir):
    """Generate an Arabic HTML report from evaluation results."""
    html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>تقرير تقييم طلبات المنح — JEDCO</title>
<style>
body { font-family: 'Segoe UI', Tahoma, sans-serif; margin: 20px; background: #f5f6fa; color: #2c3e50; }
h1 { color: #1a5276; text-align: center; }
.meta { text-align: center; color: #7f8c8d; margin-bottom: 20px; }
table { border-collapse: collapse; width: 100%; max-width: 1000px; margin: 0 auto; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
th { background: #1a5276; color: white; padding: 10px 12px; text-align: right; }
td { padding: 8px 12px; border-bottom: 1px solid #eee; text-align: right; }
tr:nth-child(even) { background: #f8f9fa; }
.pass { color: #27ae60; font-weight: bold; }
.fail { color: #c0392b; font-weight: bold; }
.summary { max-width: 1000px; margin: 20px auto; display: flex; gap: 16px; justify-content: center; }
.summary .card { background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }
.summary .card .num { font-size: 2.5em; font-weight: bold; }
.summary .card .label { color: #7f8c8d; }
</style>
</head>
<body>
<h1>تقرير تقييم طلبات المنح</h1>
<p class="meta">برنامج "ارفع قدراتك بالتسويق" — JEDCO | DATE</p>
""".replace("DATE", datetime.now().strftime("%Y-%m-%d %H:%M"))

    passed = sum(1 for r in results if r.get("decision") == "مقبول")
    failed = len(results) - passed

    html += f"""<div class="summary">
<div class="card"><div class="num">{len(results)}</div><div class="label">إجمالي الطلبات</div></div>
<div class="card"><div class="num pass" style="color:#27ae60">{passed}</div><div class="label">مقبول</div></div>
<div class="card"><div class="num fail" style="color:#c0392b">{failed}</div><div class="label">مرفوض</div></div>
</div>"""

    html += """<table>
<thead><tr>
<th>#</th><th>الشركة</th><th>التسجيل</th><th>العمر</th><th>الملكية</th><th>الموظفين</th><th>التمويل</th><th>ملفات سابقة</th><th>القطاع</th><th>النتيجة</th><th>الملاحظات</th>
</tr></thead><tbody>"""

    for i, r in enumerate(results, 1):
        if "error" in r:
            html += f'<tr><td>{i}</td><td colspan="10">خطأ في التقييم: {r.get("error","")}</td></tr>'
            continue
        dec_class = "pass" if r.get("decision") == "مقبول" else "fail"
        html += f"""<tr>
<td>{i}</td>
<td>{r.get('company_name','—')}</td>
<td>{'✅' if r.get('registration')=='نعم' else '❌'}</td>
<td>{'✅' if r.get('company_age')=='نعم' else '❌'}</td>
<td>{'✅' if r.get('ownership')=='نعم' else '❌'}</td>
<td>{'✅' if r.get('employees')=='نعم' else '❌'}</td>
<td>{'✅' if r.get('funding_ratio')=='نعم' else '❌'}</td>
<td>{'✅' if r.get('previous_files')=='نعم' else '❌'}</td>
<td>{'✅' if r.get('sector_eligible')=='نعم' else '❌'}</td>
<td class="{dec_class}">{r.get('decision','—')}</td>
<td>{r.get('reason','—')}</td>
</tr>"""

    html += """</tbody></table>
<p class="meta" style="margin-top:30px;">تم إنشاء هذا التقرير تلقائياً بواسطة نظام التقييم بالذكاء الاصطناعي — يتطلب مراجعة بشرية قبل اتخاذ أي قرار</p>
</body></html>"""

    path = os.path.join(output_dir, "results.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    parser = argparse.ArgumentParser(description="Evaluate JEDCO grant applications using Ollama")
    parser.add_argument("--apps", default=os.path.join(os.path.dirname(__file__), "..", "applications"),
                        help="Path to applications folder")
    parser.add_argument("--model", default="qwen3:8b", help="Ollama model name")
    parser.add_argument("--output", default=os.path.join(os.path.dirname(__file__), "..", "results"),
                        help="Output directory for reports")
    args = parser.parse_args()

    # Find application files
    pattern = os.path.join(args.apps, "app-*.txt")
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No application files found in: {args.apps}")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    print(f"Found {len(files)} applications")
    print(f"Model: {args.model}")
    print(f"Output: {args.output}")
    print("-" * 60)

    results = []
    start_time = time.time()

    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        print(f"[{i}/{len(files)}] Evaluating: {filename} ... ", end="", flush=True)

        with open(filepath, "r", encoding="utf-8") as f:
            app_text = f.read()

        try:
            result = evaluate_application(app_text, args.model)
            result["_file"] = filename
            results.append(result)
            dec = result.get("decision", "?")
            print(f"{'✅' if dec == 'مقبول' else '❌'} {dec}")
        except Exception as e:
            results.append({"error": str(e), "_file": filename})
            print(f"⚠️ Error: {e}")

    elapsed = time.time() - start_time

    # Save JSON
    json_path = os.path.join(args.output, "results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Save HTML report
    html_path = generate_html_report(results, args.output)

    print("-" * 60)
    passed = sum(1 for r in results if r.get("decision") == "مقبول")
    failed = len(results) - passed
    print(f"Done! {len(results)} applications evaluated in {elapsed:.0f} seconds")
    print(f"  مقبول (PASS): {passed}")
    print(f"  مرفوض (FAIL): {failed}")
    print(f"  JSON: {json_path}")
    print(f"  HTML: {html_path}")


if __name__ == "__main__":
    main()
