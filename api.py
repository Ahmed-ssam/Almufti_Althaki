from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import fitz
import easyocr
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import json
import requests

#  خادم FastAPI
app = FastAPI(title="المفتي الذكي - نظام التدقيق الشرعي المالي")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  إعدادات
print("جاري تحميل قاعدة المعرفة المحلية...")
embed_model = SentenceTransformer("intfloat/multilingual-e5-small")

client = chromadb.PersistentClient(path="./islamic_db")
collection = client.get_collection(name="expert_knowledge")

print("جاري تحميل محرك الـ OCR (EasyOCR)...")
# دعم اللغتين العربية والإنجليزية
ocr_reader = easyocr.Reader(['ar', 'en'])

print(" النظام جاهز للعمل!")


#  (Endpoint)
@app.post("/upload-contract/")
async def audit_contract(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename.lower()

    def event_generator():
        full_text = ""

        #  التحقق من نوع الملف
        if filename.endswith(".pdf"):
            doc = fitz.open(stream=content, filetype="pdf")

            # قراءة الصفحات (نصي + بصري)
            for page in doc:
                text_blocks = page.get_text("blocks")
                page_text = ""

                for b in text_blocks:
                    text_block = b[4].strip().replace('\n', ' ')
                    if len(text_block) > 20:
                        page_text += text_block + "\n\n"

                #   الصفحة شبه فارغة من النصوص الرقمية
                if len(page_text.strip()) < 50:
                    print(" صفحة PDF مصورة مكتشفة. جاري تشغيل محرك EasyOCR...")
                    pix = page.get_pixmap()
                    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

                    ocr_results = ocr_reader.readtext(img_array, detail=0, paragraph=True)
                    page_text = "\n\n".join(ocr_results) + "\n\n"

                full_text += page_text

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            print(" تم رفع ملف صورة. جاري استخراج النص عبر EasyOCR مباشرة...")
            # EasyOCR يدعم قراءة الصور مباشرة من الـ Bytes
            ocr_results = ocr_reader.readtext(content, detail=0, paragraph=True)
            full_text = "\n\n".join(ocr_results) + "\n\n"

        else:
            # في حال رفع ملف غير مدعوم
            error_data = {
                "index": 0,
                "original_clause": f"الملف المرفوع: {file.filename}",
                "audit_result": "⚠️ صيغة الملف غير مدعومة. يرجى رفع ملف PDF أو صورة بصيغة (JPG/PNG/JPEG)."
            }
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'status': 'done'})}\n\n"
            return

        #  تقسيم النص
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "البند", "المادة", ".", "؛", " "]
        )

        # وضع الاختبار
        clauses = text_splitter.split_text(full_text)[:5]

        # إذا لم يتم استخراج أي نص (صورة فارغة مثلاً)
        if not clauses:
            yield f"data: {json.dumps({'index': 0, 'original_clause': 'مستند فارغ', 'audit_result': 'لم يتمكن النظام من قراءة أي نصوص في هذا الملف.'}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'status': 'done'})}\n\n"
            return

        for i, clause in enumerate(clauses):
            clause_embedding = embed_model.encode([clause]).tolist()
            results = collection.query(query_embeddings=clause_embedding, n_results=1)

            # سحب بيانات التوثيق
            standards_text = ""
            if results.get('documents') and results['documents'][0]:
                for doc_idx, doc_text in enumerate(results['documents'][0]):
                    meta_dict = {}
                    if results.get('metadatas') and results['metadatas'][0] and results['metadatas'][0][doc_idx]:
                        meta_dict = results['metadatas'][0][doc_idx]

                    page_num = meta_dict.get('page', 'غير محدد')
                    source_name = meta_dict.get('source', 'المعايير الشرعية')
                    standards_text += f"[المرجع: {source_name} - صفحة: {page_num}]\n{doc_text}\n---\n"
            else:
                standards_text = "لا توجد معايير مطابقة."

            prompt = f"""
            مهمتك الوحيدة هي مطابقة "البند" مع "المعايير المرفقة" فقط.
            تحذير صارم: يُمنع منعاً باتاً استخدام أي معلومات، أو فتاوى، أو آراء من ذاكرتك السابقة. 
            يجب أن يكون حكمك مبنياً 100% على النص الموجود في "المعايير الفقهية المرجعية" أدناه. إذا لم تجد حكماً واضحاً في المعايير المرفقة، فاكتب ببساطة "لا توجد معايير كافية للتقييم".

            البند المراد تدقيقه:
            {clause}

            المعايير الفقهية المرجعية:
            {standards_text}

            أجب باختصار والتزم بهذا الهيكل الرقمي نصاً:
            1. الحالة: (متوافق / غير متوافق / يحتاج مراجعة)
            2. السبب: (استخرج السبب من النص المرفق فقط)
            3. البديل المقترح: (انسخه من النص المرفق إن وجد)
            4. التوثيق: (انسخ نص المرجع ورقم الصفحة الموجود في المعايير المرفقة)
            """

            try:
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "qwen2.5:1.5b",
                        "messages": [
                            {"role": "system",
                             "content": "أنت مساعد ذكي ومختص بالتدقيق المالي الإسلامي. أجب باللغة العربية بوضوح ودقة بناء على السياق المعطى لك فقط."},
                            {"role": "user", "content": prompt}
                        ],
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "num_predict": 512,
                            "stop": ["user", "User", "ملاحظة:", "أعتذر", "\n\n\n"]
                        }
                    },
                    timeout=300
                )
                response.raise_for_status()
                audit_text = response.json()["message"]["content"]

            except Exception as e:
                print(f" Error in Local API call: {e}")
                audit_text = " **خطأ تقني:** تعذر الاتصال بمحرك Ollama المحلي أو استغرق وقتاً طويلاً. تأكد أن البرنامج يعمل."

            data = {
                "index": i + 1,
                "original_clause": clause,
                "audit_result": audit_text
            }

            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            time.sleep(1)

        yield f"data: {json.dumps({'status': 'done'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")