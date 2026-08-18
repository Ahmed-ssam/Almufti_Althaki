<div align="center">

# 🕌 المفتي الذكي
### Smart Islamic Financial Auditor

نظام متقدم للتدقيق الشرعي الآلي للعقود المالية

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-LLM%20Engine-black.svg)](https://ollama.com/)
[![License](https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg)]()

</div>

---

## 📖 نظرة عامة

**المفتي الذكي** نظام آلي للتدقيق الشرعي للعقود المالية، مصمم للعمل **بالكامل دون اتصال بالإنترنت (Offline)** لضمان الخصوصية التامة للبيانات المالية الحساسة.

يعتمد النظام على معمارية **RAG (Retrieval-Augmented Generation)** لربط المعايير الفقهية الشرعية بنماذج الذكاء الاصطناعي اللغوية، بحيث تكون كل فتوى أو ملاحظة تدقيق مستندة حصراً إلى النصوص المرجعية المرفقة.

---

## ✨ المميزات الرئيسية

| الميزة | الوصف |
|---|---|
| 🔒 **خصوصية مطلقة (Air-gapped)** | يعمل محلياً بالكامل عبر محرك `Ollama` دون إرسال أي بيانات إلى السحابة |
| 📄 **قراءة هجينة (Hybrid Parsing)** | دمج ذكي بين `PyMuPDF` لقراءة النصوص و`EasyOCR` لقراءة العقود الممسوحة ضوئياً والصور تلقائياً |
| ⚖️ **تدقيق فقهي دقيق** | استخدام قاعدة بيانات متجهة (`ChromaDB`) للبحث في المعايير الشرعية، مع إجبار النموذج على الإجابة من النصوص المرفقة فقط (Zero-Knowledge Constraint) |
| ⚡ **بث مباشر للنتائج (SSE)** | معالجة وعرض نتائج التدقيق بنداً ببند في الوقت الفعلي لتجربة مستخدم سلسة |
| 🖥️ **واجهة تفاعلية** | واجهة احترافية مصممة لعرض العقود والتقارير مع رسوم بيانية تفاعلية عبر `Chart.js` |

---

## 🛠️ المعمارية والتقنيات المستخدمة

| الطبقة | التقنية |
|---|---|
| **Backend** | FastAPI, Python |
| **LLM Engine** | Ollama |
| **Vector Database** | ChromaDB |
| **Embeddings** | SentenceTransformers (`multilingual-e5-small`) |
| **OCR** | EasyOCR |
| **Frontend** | HTML5, CSS3, Vanilla JS, Chart.js |

---

## 🚀 طريقة التشغيل

### 1️⃣ تهيئة بيئة العمل

```bash
python -m venv venv
source venv/bin/activate   # على نظام Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ تحميل محرك الذكاء الاصطناعي

تأكد من تثبيت **Ollama**، ثم قم بتحميل النموذج المحلي:

```bash
ollama pull qwen2.5:1.5b
```

### 3️⃣ بناء قاعدة المعرفة (RAG)

```bash
python build_knowledge_base.py
```

### 4️⃣ تشغيل الخادم والواجهة

```bash
uvicorn api:app --reload
```

ثم افتح ملف `المفتي-الذكي.html` في متصفحك للبدء في تدقيق العقود! 🎉

---

## 🖼️ لقطات من النظام

<div align="center">

<img width="900" alt="واجهة النظام 1" src="https://github.com/user-attachments/assets/97eaaaa7-1500-43d6-9745-6154c159fa09" />

<img width="900" alt="واجهة النظام 2" src="https://github.com/user-attachments/assets/0fd4741b-71eb-4661-bbd3-ff3a9a124bb7" />

<img width="600" alt="واجهة النظام 3" src="https://github.com/user-attachments/assets/7cef3f42-6831-4833-8c3d-3949e0d92f0a" />

<img width="900" alt="واجهة النظام 4" src="https://github.com/user-attachments/assets/274f3057-f40d-4445-967a-56dd1500cc52" />

</div>
