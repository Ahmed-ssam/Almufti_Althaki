import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore") 

print("1. جاري تحميل نموذج التضمين المصغر (قد يستغرق ثواني في المرة الأولى)...")
embed_model = SentenceTransformer("intfloat/multilingual-e5-small")

print("2. قراءة المعايير الشرعية من الملف...")
with open("standards.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("3. تقطيع النصوص إلى فقرات دقيقة...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_text(text)

print("4. إنشاء قاعدة بيانات ChromaDB المحلية...")
client = chromadb.PersistentClient(path="./islamic_db")
collection = client.get_or_create_collection(name="aaoifi_standards")

print("5. تحويل النصوص إلى متجهات وحفظها...")
for i, chunk in enumerate(chunks):
    embedding = embed_model.encode(chunk).tolist()
    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[embedding]
    )

print(" تمت العملية بنجاح! قاعدة البيانات الشرعية جاهزة الآن.")