import os
import json
import chromadb
from chromadb.config import Settings
from app.config import settings

def main():
    print("=" * 70)
    print("        INITIALIZING CHROMADB PERSISTENT VECTOR DATABASE")
    print("=" * 70)
    
    vector_db_dir = settings.VECTOR_DB_DIR
    os.makedirs(vector_db_dir, exist_ok=True)
    
    print(f"Target ChromaDB Storage Path: {os.path.abspath(vector_db_dir)}")
    
    # 1. Instantiate Persistent ChromaDB Client
    client = chromadb.PersistentClient(path=vector_db_dir)
    
    # 2. Get or create collection
    collection_name = "i6_service_manuals"
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine", "description": "I6 Engine OEM Service Manuals & SAE DTCs"}
    )
    
    # 3. Load documents from i6_service_manual.json
    json_path = os.path.join(os.path.dirname(__file__), "app", "rag", "knowledge_base", "i6_service_manual.json")
    with open(json_path, "r", encoding="utf-8") as f:
        documents_raw = json.load(f)

    ids = []
    documents = []
    metadatas = []

    for idx, doc in enumerate(documents_raw):
        doc_id = doc.get("id", f"doc_{idx}")
        title = doc.get("title", "")
        category = doc.get("category", "")
        dtc = doc.get("dtc_code", "")
        content = doc.get("content", "")

        full_text = f"Title: {title}\nCategory: {category}\nDTC Code: {dtc}\n\n{content}"

        ids.append(doc_id)
        documents.append(full_text)
        metadatas.append({
            "title": title,
            "category": category,
            "dtc_code": dtc,
            "id": doc_id
        })

    # Upsert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    count = collection.count()
    print(f"Successfully populated ChromaDB Collection '{collection_name}' with {count} documents!")
    print(f"Persistent Database Created at: {os.path.join(vector_db_dir, 'chroma.sqlite3')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
