#  المفتي الذكي (Smart Islamic Financial Auditor)

نظام متقدم للتدقيق الشرعي الآلي للعقود المالية، يعمل بالكامل محلياً (Offline) لضمان الخصوصية التامة للبيانات المالية. يعتمد النظام على معمارية RAG (Retrieval-Augmented Generation) لربط المعايير الفقهية بنماذج الذكاء الاصطناعي اللغوية.

##  المميزات الرئيسية (Features)
* **خصوصية مطلقة (Air-gapped):** يعمل محلياً بالكامل عبر محرك `Ollama` دون إرسال أي بيانات للسحابة.
* **قراءة هجينة (Hybrid Parsing):** دمج ذكي بين مكتبة `PyMuPDF` لقراءة النصوص، ومحرك `EasyOCR` لقراءة العقود الممسوحة ضوئياً والصور تلقائياً.
* **تدقيق فقهي دقيق:** استخدام قاعدة بيانات متجهة (`ChromaDB`) للبحث في المعايير الشرعية وإجبار النموذج على الفتوى من النصوص المرفقة فقط (Zero-Knowledge Constraint).
* **بث مباشر للنتائج (SSE):** معالجة وعرض نتائج التدقيق بنداً ببند في الوقت الفعلي لتجربة مستخدم سلسة.
* **واجهة تفاعلية:** واجهة احترافية مصممة خصيصاً لعرض العقود والتقارير مع رسوم بيانية تفاعلية (`Chart.js`).

##  المعمارية والتقنيات المستخدمة (Tech Stack)
* **Backend:** FastAPI, Python
* **LLM Engine:** Ollama
* **Vector Database:** ChromaDB
* **Embeddings:** SentenceTransformers (multilingual-e5-small)
* **OCR:** EasyOCR
* **Frontend:** HTML5, CSS3, Vanilla JS, Chart.js

##  طريقة التشغيل (How to Run)

**1. تهيئة بيئة العمل:**
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

2. تحميل محرك الذكاء الاصطناعي:
تأكد من تثبيت Ollama ثم حمل النموذج المحلي:

ollama pull qwen2.5:1.5b  

3. بناء قاعدة المعرفة (RAG):
python build_knowledge_base.py

4. تشغيل الخادم والواجهة:

Bash
uvicorn api:app --reload
ثم قم بفتح ملف المفتي-الذكي.html في متصفحك للبدء في تدقيق العقود!

<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/97eaaaa7-1500-43d6-9745-6154c159fa09" />
<img width="1919" height="906" alt="image" src="https://github.com/user-attachments/assets/0fd4741b-71eb-4661-bbd3-ff3a9a124bb7" />
<img width="952" height="603" alt="image" src="https://github.com/user-attachments/assets/7cef3f42-6831-4833-8c3d-3949e0d92f0a" />
<img width="1600" height="746" alt="WhatsApp Image 2026-07-31 at 7 26 47 AM" src="https://github.com/user-attachments/assets/274f3057-f40d-4445-967a-56dd1500cc52" />
