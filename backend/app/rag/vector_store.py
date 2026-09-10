import json
import os
import re
import numpy as np
from typing import List, Dict, Any

class RAGVectorStore:
    """
    Knowledge Base Retrieval Engine for Automotive OEM Service Manuals.
    Uses SentenceTransformers or TF-IDF / Weighted Semantic Cosine Matching
    for fast, highly relevant retrieval against diagnostic questions & fault trees.
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
                
        # Try loading SentenceTransformer model if available
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            texts = [f"{d.get('title','')} {d.get('dtc_code','')} {d.get('category','')} {d.get('content','')}" for d in self.documents]
            self.doc_embeddings = self.encoder.encode(texts, convert_to_numpy=True)
        except Exception as e:
            print(f"[RAG VectorStore] SentenceTransformer init fallback: {e}")
            self.encoder = None

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant service manual chunks for query.
        """
        if not self.documents:
            return []
            
        if self.encoder is not None and self.doc_embeddings is not None:
            query_vec = self.encoder.encode([query], convert_to_numpy=True)[0]
            norm_q = np.linalg.norm(query_vec) + 1e-9
            norm_docs = np.linalg.norm(self.doc_embeddings, axis=1) + 1e-9
            sims = np.dot(self.doc_embeddings, query_vec) / (norm_docs * norm_q)
            top_indices = np.argsort(sims)[::-1][:top_k]
            return [self.documents[idx] for idx in top_indices]
        else:
            # High-accuracy weighted keyword relevance search engine
            query_clean = re.sub(r'[^\w\s]', ' ', query.lower())
            query_words = set(w for w in query_clean.split() if len(w) > 1)
            scored_docs = []
            
            for doc in self.documents:
                title = doc.get("title", "").lower()
                category = doc.get("category", "").lower()
                dtc = doc.get("dtc_code", "").lower()
                content = doc.get("content", "").lower()
                
                score = 0.0
                for w in query_words:
                    if w in dtc:
                        score += 10.0
                    if w in title:
                        score += 5.0
                    if w in category:
                        score += 3.0
                    if w in content:
                        score += 1.0
                        
                # Bonus for exact DTC matches like p0303 or p0299
                for w in query_words:
                    if len(w) >= 4 and w.startswith('p0') and w in (dtc + " " + content + " " + title):
                        score += 15.0
                        
                scored_docs.append((score, doc))
                
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            return [d[1] for d in scored_docs[:top_k] if d[0] > 0] or self.documents[:top_k]
