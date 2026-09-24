import os
import logging
from typing import List, Optional
try:
    from dotenv import load_dotenv
    from openai import OpenAI
except ImportError:
    raise ImportError("Gerekli kütüphaneler eksik. Lütfen 'pip install openai python-dotenv' komutunu çalıştırın.")

# Loglama ayarları (Senior dokunuşu)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Basit bir in-memory dummy vector store (örnek amaçlı)
# Gerçek projelerde ChromaDB, Pinecone vb. kullanılmalı.
KNOWLEDGE_BASE = [
    "AI Agent'lar, LLM'leri sadece metin üretmek için değil, araç (tool) kullanmak ve karar vermek için kullanan sistemlerdir.",
    "RAG (Retrieval-Augmented Generation), LLM'lerin halüsinasyon görmesini engellemek için dış bilgi kaynaklarıyla beslenmesi tekniğidir.",
    "ReAct (Reasoning and Acting) mimarisi, agent'ların düşünme ve eyleme geçme adımlarını birleştirir."
]

class SimpleRAG:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyasını kontrol edin.")
            raise ValueError("OPENAI_API_KEY eksik.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini" # Maliyet optimizasyonu için mini model
    
    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        """
        Sorguya en uygun dokümanları getirir. 
        Not: Burada TF-IDF veya Embedding tabanlı gerçek bir arama yerine 
        örnek amaçlı basit bir kelime eşleşmesi simüle edilmiştir.
        """
        logger.info(f"Sorgu için dokümanlar aranıyor: '{query}'")
        
        # Basit heuristic: query içindeki kelimeler dokümanda geçiyor mu?
        query_terms = query.lower().split()
        scored_docs = []
        
        for doc in KNOWLEDGE_BASE:
            score = sum(1 for term in query_terms if term in doc.lower())
            scored_docs.append((score, doc))
            
        # Skorlara göre sırala ve top_k kadarını al
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        retrieved = [doc for score, doc in scored_docs if score > 0][:top_k]
        
        # Eğer hiç eşleşme yoksa fallback olarak ilk dokümanı ver (demo için)
        if not retrieved:
            retrieved = KNOWLEDGE_BASE[:1]
            
        logger.info(f"{len(retrieved)} adet ilgili doküman bulundu.")
        return retrieved

    def generate(self, query: str, context: List[str]) -> Optional[str]:
        """
        Gelen context'i kullanarak LLM'den cevap üretir.
        """
        context_str = "\n".join([f"- {c}" for c in context])
        system_prompt = (
            "Sen yardımcı bir AI asistanısın. Sana verilen 'Context' bilgisini "
            "kullanarak kullanıcının sorusuna cevap ver. Eğer cevap context içinde "
            "yoksa, uydurmak (hallucinate) yerine 'Bu bilgiye sahip değilim' de."
        )
        
        user_prompt = f"Context:\n{context_str}\n\nSoru: {query}"
        
        logger.info("LLM'e istek atılıyor...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1 # RAG senaryolarında düşük temperature tercih edilir
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API isteği sırasında hata oluştu: {e}")
            return None

    def query(self, user_query: str) -> str:
        """
        Uçtan uca RAG pipeline'ı (Retrieve -> Generate).
        """
        docs = self.retrieve(user_query)
        answer = self.generate(user_query, docs)
        return answer or "Cevap üretilemedi."

if __name__ == "__main__":
    try:
        rag_system = SimpleRAG()
        soru = "RAG nedir ve ne işe yarar?"
        
        print("\n" + "="*40)
        print(f"Soru: {soru}")
        print("="*40)
        
        cevap = rag_system.query(soru)
        
        print("\nCevap:")
        print(cevap)
        print("="*40 + "\n")
        
    except ValueError as ve:
        print(f"Kurulum hatası: {ve}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
