# RAG (Retrieval-Augmented Generation) Best Practices

RAG sistemleri kurarken genelde tutorial'larda atlanan ancak production (canlı) ortamlarda baş ağrıtan bazı detayları ve tecrübeleri burada özetlemek istedim.

## 1. Chunking (Metin Bölme) Stratejisi
* Metinleri sadece `chunk_size=1000` vererek rastgele bölmek genelde semantic bütünlüğü bozar. 
* **Öneri:** LangChain'deki `RecursiveCharacterTextSplitter` kullanarak, metinleri önce paragraflardan (`\n\n`), sonra cümlelerden bölmeye çalışın. Ek olarak, `chunk_overlap` değerini %10-15 civarında tutmak, bir chunk'ta yarım kalan anlamın diğerinde tamamlanmasını sağlar.

## 2. Embedding Modeli Seçimi
* OpenAI'ın `text-embedding-3-small` modeli şu an fiyat/performans olarak çok iyi. Ancak veriniz İngilizce dışında (örneğin tamamen Türkçe) veya spesifik bir alana aitse (hukuk, tıp vb.), HuggingFace üzerindeki multilingual BGE (BAAI General Embedding) modellerine göz atabilirsiniz.
* Çok büyük verilerde embedding maliyeti artar, yerel (local) modeller (örn: Ollama üzerinden mxbai-embed-large) kullanarak maliyeti sıfırlayabilirsiniz.

## 3. Vektör DB Seçimi Karar Matrisi
* **Prototip/PoC:** `ChromaDB` veya `FAISS` (Local çalışır, kurulum derdi yoktur).
* **Managed/Cloud:** `Pinecone` (Çok hızlı başlanır ama scale edince maliyetlidir).
* **Kapsamlı/Production:** `Qdrant` veya `Weaviate` (Filtreleme yetenekleri çok güçlüdür, metadata aramaları hayat kurtarır).
* **Mevcut DB'yi kullanma:** Eğer projede zaten PostgreSQL varsa `pgvector` eklentisi çoğu orta ölçekli proje için fazlasıyla yeterlidir, yeni bir altyapı maliyetinden kurtarır.

## 4. Temperature Ayarı
RAG mimarisinde LLM'in görevi yaratıcılık (creative writing) değil, **sentezlemektir**. Bu yüzden modelin `temperature` parametresini her zaman `0.0` veya `0.1` gibi çok düşük değerlerde tutun. Aksi takdirde verilen context dışına çıkıp halüsinasyon görme ihtimali çok artar.

## 5. Metadata Filtrasyonu
Sadece vektör benzerliği ile arama yapmak ("Kedi hastalıkları nelerdir?") bazen yetmez. Eğer veritabanınızda binlerce doküman varsa, aramayı daraltmak için (Örn: `category="saglik"`, `date > "2023-01-01"`) metadata filtreleri kullanın (Hybrid Search). 

> *Ufak bir not: Projelerde context'e haddinden fazla doküman (top_k=20 gibi) basmak LLM'in kafasını karıştırır (Lost in the middle problemi). Context penceresini optimize tutmak (top_k=3-5) her zaman daha tutarlı cevaplar verir.*
