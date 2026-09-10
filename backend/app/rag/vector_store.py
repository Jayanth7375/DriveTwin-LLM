import json
import os
import numpy as np
from typing import List, Dict, Any

class RAGVectorStore:
    """
    Knowledge Base Retrieval Engine for Automotive OEM Service Manuals.
    Uses SentenceTransformers or TF-IDF/Cosine Similarity embeddings
    for fast semantic matching against fault symptoms.
    """
    def __init__(self):
        self.documents = []
        self.doc_embeddings = None
        self.encoder = None
        self.load_knowledge_base()

    def load_knowledge_base(self):
        json_path = os.path.join(os.path.dirname(__file__), "knowledge_base", "i6_service_manual.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
                
        # Try loading SentenceTransformer model if available, else fallback to keyword/vector matching
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            texts = [f"{d['title']} {d['category']} {d['content']}" for d in self.documents]
            self.doc_embeddings = self.encoder.encode(texts, convert_to_numpy=True)
        except Exception as e:
            print(f"[RAG VectorStore] SentenceTransformer init fallback: {e}")
            self.encoder = None

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant service manual chunks for query.
        """
        if not self.documents:
            return []
            
        if self.encoder is not None and self.doc_embeddings is not None:
            query_vec = self.encoder.encode([query], convert_to_numpy=True)[0]
            # Cosine similarity
            norm_q = np.linalg.norm(query_vec) + 1e-9
            norm_docs = np.linalg.norm(self.doc_embeddings, axis=1) + 1e-9
            sims = np.dot(self.doc_embeddings, query_vec) / (norm_docs * norm_q)
            
            top_indices = np.argsort(sims)[::-1][:top_k]
            return [self.documents[idx] for idx in top_indices]
        else:
            # Fallback simple keyword relevance matcher
            query_words = set(query.lower().split())
            scored_docs = []
            for doc in self.documents:
                text = f"{doc['title']} {doc['category']} {doc['content']}".lower()
                score = sum(1 for w in query_words if w in text)
                scored_docs.append((score, doc))
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            return [d[1] for d in scored_docs[:top_k]]
