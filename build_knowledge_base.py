import os
import fitz
import chromadb
from sentence_transformers import SentenceTransformer
import warnings

warnings.filterwarnings("ignore")

print("==================================================")
print(" بدء تشغيل محرك بناء قاعدة المعرفة ...")
print("==================================================")

#  تحميل نموذج (Embeddings)
print(" جاري تحميل نموذج الذكاء الاصطناعي للغة العربية...")
embed_model = SentenceTransformer("intfloat/multilingual-e5-small")

#  تجهيز قاعدة البيانات
client = chromadb.PersistentClient(path="./islamic_db")
# سنقوم بإنشاء مجموعة جديدة للبيانات الضخمة
collection_name = "expert_knowledge"
try:
    client.delete_collection(name=collection_name)  # مسح القديم إن وجد للبدء على نظافة
except:
    pass
collection = client.create_collection(name=collection_name)


#  دالة (Chunking) مع الحفاظ على السياق (Overlap)
def get_chunks(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max(1, chunk_size - overlap)):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.strip()) > 30:  # تجاهل الفقرات الفارغة جداً
            chunks.append(chunk)
    return chunks


#  قراءة الكتب ومعالجتها
data_folder = "real_data"
if not os.path.exists(data_folder):
    print(f" خطأ: لم يتم العثور على مجلد '{data_folder}'. يرجى إنشاؤه ووضع الكتب فيه.")
else:
    pdf_files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
    if len(pdf_files) == 0:
        print(f" المجلد '{data_folder}' فارغ! يرجى وضع ملفات PDF بداخله.")

    total_chunks_added = 0

    for pdf_file in pdf_files:
        file_path = os.path.join(data_folder, pdf_file)
        print(f"\n جاري قراءة كتاب: {pdf_file} ...")

        doc = fitz.open(file_path)
        full_text = ""

        # استخراج النص من كل الصفحات
        for page_num in range(len(doc)):
            full_text += doc.load_page(page_num).get_text("text") + "\n"

        # تقسيم النص إلى فقرات
        chunks = get_chunks(full_text, chunk_size=300, overlap=50)
        print(f" تم تقسيم الكتاب إلى {len(chunks)} فقرة فقهية.")

        # تحويل الفقرات إلى أرقام وتخزينها
        print("💾 جاري ضخ البيانات في قاعدة المعرفة (ChromaDB)... قد يستغرق هذا بعض الوقت...")

        #  (Batches) لتجنب اختناق الذاكرة
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]

            # إنشاء (IDs) فريدة لكل فقرة
            ids = [f"{pdf_file}_chunk_{total_chunks_added + j}" for j in range(len(batch_chunks))]

            # تحويل النص لمتجهات
            embeddings = embed_model.encode(batch_chunks).tolist()

            # الحفظ في القاعدة
            collection.add(
                documents=batch_chunks,
                embeddings=embeddings,
                ids=ids
            )
            total_chunks_added += len(batch_chunks)

        print(f" انتهت معالجة كتاب: {pdf_file}")

    print("\n==================================================")
    print(f" تمت العملية بنجاح أسطوري!")
    print(f" تحتوي قاعدة معرفتك الآن على: {total_chunks_added} حُكم وفقرة شرعية مستعدة للتدقيق.")
    print("==================================================")