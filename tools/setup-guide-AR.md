# دليل التجهيز — تثبيت الأدوات قبل يوم التدريب
## Agentic Government / JEDCO
### الوقت المطلوب: ٣٠ دقيقة تقريباً

---

## المتطلبات
- ويندوز ١٠ أو ١١
- كرت شاشة NVIDIA بذاكرة ٦ جيجا أو أكثر (RTX 2060 أو أفضل)
- مساحة فارغة على القرص: ١٥ جيجا على الأقل
- اتصال إنترنت (للتحميل فقط — التدريب يعمل بدون إنترنت)

---

## الخطوة ١ — تثبيت Ollama

1. افتح المتصفح وادخل على: **https://ollama.com/download**
2. اختر **Windows** واضغط **Download**
3. شغّل ملف `OllamaSetup.exe`
4. اتبع خطوات التثبيت (Next → Next → Install)
5. بعد التثبيت، افتح **Command Prompt** أو **PowerShell**
6. اكتب:
   ```
   ollama --version
   ```
   يجب أن يظهر رقم الإصدار (مثل: `ollama version 0.20.2`)

### ⚠️ إذا لم يعمل الأمر:
أضف Ollama إلى PATH يدوياً:
```
set PATH=%PATH%;%LOCALAPPDATA%\Programs\Ollama
```

---

## الخطوة ٢ — تحميل نموذج qwen3:8b

1. في نفس نافذة الأوامر، اكتب:
   ```
   ollama pull qwen3:8b
   ```
2. انتظر التحميل (٥.٢ جيجا — يستغرق ١٠-٢٠ دقيقة حسب سرعة الإنترنت)
3. بعد الانتهاء، اختبر النموذج:
   ```
   ollama run qwen3:8b "مرحباً، ما هو دورك؟"
   ```
4. يجب أن يرد النموذج بالعربية ✅
5. للخروج من المحادثة اكتب: `/bye`

---

## الخطوة ٣ — تثبيت AnythingLLM

1. افتح المتصفح وادخل على: **https://anythingllm.com/download**
2. اختر **Windows** واضغط **Download**
3. شغّل ملف `AnythingLLMDesktop.exe`
4. اتبع خطوات التثبيت
5. بعد فتح البرنامج:
   - اختر **Ollama** كمزود النموذج (LLM Provider)
   - URL: `http://localhost:11434`
   - اختر نموذج: **qwen3:8b**
   - اضغط **Save**

---

## الخطوة ٤ — إنشاء مساحة عمل وتحميل المستندات

1. في AnythingLLM، اضغط **New Workspace**
2. سمّها: `JEDCO Application Review`
3. اضغط على أيقونة التحميل (Upload)
4. حمّل الملفات التالية من مجلد `assets/jedco-docs/`:
   - `JEDCO-eligibility-criteria-reference-v2.txt`
   - `mock-application-start-business-AR.txt`
   - `mock-application-tattweer-AR.txt`
5. انتظر حتى يتم فهرسة المستندات (Embedding)

---

## الخطوة ٥ — اختبار شامل

### اختبار ١: Ollama مباشرة
```
ollama run qwen3:8b "أنت مقيّم في JEDCO. ما هي شروط برنامج تطوير؟"
```
→ يجب أن يرد بمعلومات عن البرنامج ✅

### اختبار ٢: AnythingLLM
- افتح مساحة عمل `JEDCO Application Review`
- اكتب: "ما هي المستندات المطلوبة لبرنامج تطوير؟"
→ يجب أن يرد بناءً على المستندات المحمّلة ✅

### اختبار ٣: المسار الآلي (اختياري)
```
cd c:\Projects\AgenticGovernment
python tools/evaluate-pipeline.py --model qwen3:8b --limit 2
```
→ يجب أن يظهر تقييم لطلبين ✅

---

## استكشاف الأخطاء

| المشكلة | الحل |
|---------|------|
| `ollama` غير معروف | أضف المسار إلى PATH (انظر الخطوة ١) |
| التحميل بطيء | تأكد من اتصال الإنترنت، أو استخدم شبكة أسرع |
| AnythingLLM لا يرى Ollama | تأكد أن Ollama يعمل: `ollama list` |
| النموذج بطيء جداً | أغلق البرامج الأخرى، تأكد من استخدام كرت الشاشة |
| خطأ في Python | تأكد من تثبيت Python 3.8+ وتشغيل `pip install requests` |

---

## ✅ جاهز للتدريب!
إذا نجحت جميع الاختبارات الثلاثة، الجهاز جاهز ليوم التدريب.
