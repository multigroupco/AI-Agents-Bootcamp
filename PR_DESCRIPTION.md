# Pull Request: 🚀 6 Haftalık Müfredat Slayt Destesi, Teknik Mimari Diyagramları ve Görsel Prompt Seti

## 📋 Özet (Overview)
Bu Pull Request, **Türkiye Veri Topluluğu AI Agents Bootcamp** repository'sine kapsamlı sunum materyalleri, modüler teknik mimari diyagramları ve yapay zekâ destekli görsel üretim promptları kazandırmaktadır. 

Mevcut repository yapısına zarar vermeden, tüm sunum ve görselleştirme kaynakları modüler bir `presentation/` dizini altında toplanmış ve hem eğitmenlerin hem de öğrencilerin kolayca erişebileceği biçimde belgelenmiştir.

---

## 🎯 Yapılan Değişiklikler ve Motivasyon (Motivation & Changes)

1. **Modüler Sunum Dosyası (`presentation/slides/bootcamp_deck.md`):**
   - 6 haftalık müfredatın tamamını kapsayan, **Marp** ve **Slidev** uyumlu modern slayt destesi eklendi.
   - Her hafta için net teknik odak noktaları (Tokenizasyon, ReAct, Hybrid RAG, Multi-Agent LangGraph, Observability) ve eğitmenlere rehberlik eden detaylı **Speaker Notes** (konuşmacı notları) entegre edildi.
   - Koyu tema (Dark mode) ve Türkiye Veri Topluluğu renk paletine (`#0F172A`, `#38BDF8`, `#A78BFA`) uygun özel CSS stilleri tanımlandı.

2. **Teknik Mimari Diyagramları (`presentation/assets/diagrams/`):**
   - GitHub Markdown ve Mermaid araçlarıyla %100 uyumlu, yüksek okunurluklu 3 temel mimari diyagram oluşturuldu:
     * `single_agent_cycle.mmd`: ReAct (Thought-Action-Observation) döngüsü ve karar matrisi.
     * `advanced_rag_flow.mmd`: Ingestion, Dense+Sparse Hybrid Retrieval, Reciprocal Rank Fusion (RRF) ve Cross-Encoder Reranker boru hattı.
     * `multi_agent_orchestration.mmd`: Supervisor/Orchestrator, Worker Agent'lar (Researcher, Coder, Critic) ve paylaşılan State Graph mimarisi.

3. **Kapsamlı Teknik Ders Notları & Rehber (`presentation/docs/curriculum_deep_dive.md`):**
   - 6 haftanın tamamını kapsayan teorik arka plan, BPE tokenizasyon, Pydantic şemaları, Hibrit Arama & RRF formülleri, Bi-Encoder vs Cross-Encoder karşılaştırmaları, LangGraph durum yönetimi, Tracing ve bitirme projesi rubric'i eklendi.

4. **Görsel Üretim Promptları (`presentation/prompts/image_generation.md`):**
   - Midjourney v6, Flux.1 ve DALL-E 3 uyumlu; repo kapak görseli, slayt bölüm ayraçları ve sosyal medya duyuru kartları için optimize edilmiş fotogerçekçi ve 3D izometrik prompt şablonları hazırlandı.

5. **Kullanım Kılavuzu (`presentation/README.md`):**
   - Sunumları VS Code veya Marp CLI ile PDF / HTML olarak derleme adımları belgelendi.

---

## 📂 Eklenen / Güncellenen Dosyalar Ağacı (File Tree)

```
AI-Agents-Bootcamp/
├── PR_DESCRIPTION.md                      # [YENİ] Detaylı Pull Request şablonu
└── presentation/                          # [YENİ] Sunum ve görselleştirme ana dizini
    ├── README.md                          # [YENİ] Sunum dizini rehberi ve CLI komutları
    ├── docs/
    │   └── curriculum_deep_dive.md         # [YENİ] 6 haftalık kapsamlı teknik ders notları
    ├── slides/
    │   └── bootcamp_deck.md               # [YENİ] 6 haftalık Marp/Slidev uyumlu sunum destesi
    ├── assets/
    │   └── diagrams/                      # [YENİ] Mermaid.js mimari diyagram kaynakları
    │       ├── single_agent_cycle.mmd     # [YENİ] Tekil Agent ReAct Döngüsü
    │       ├── advanced_rag_flow.mmd      # [YENİ] Gelişmiş RAG Akışı
    │       └── multi_agent_orchestration.mmd # [YENİ] Multi-Agent İletişim Mimarisi
    └── prompts/
        └── image_generation.md            # [YENİ] Midjourney / Flux / DALL-E görsel promptları
```

---

## 🖼️ Mimari Diyagram Önizlemeleri (Architecture Previews)

### 1. Tekil Agent Döngüsü (ReAct Pattern)
```mermaid
flowchart TD
    User(["👤 Kullanıcı İstemi"]):::userNode --> Thought["🧠 Akıl Yürütme (Thought)"]:::thoughtNode
    Thought --> Decision{"Aksiyon Gerekli mi?"}:::decisionNode
    Decision -->|Evet| Action["⚡ Araç Çağrısı (Tool Action)"]:::actionNode
    Action --> ToolExec["🛠️ Tool İcrası (API/Search/DB)"]:::toolNode
    ToolExec --> Observation["👁️ Gözlem (Observation)"]:::obsNode
    Observation --> Thought
    Decision -->|Hayır| FinalAnswer(["🎯 Nihai Çözüm"]):::finalNode

    classDef userNode fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef thoughtNode fill:#0f172a,stroke:#a855f7,stroke-width:2px,color:#fff;
    classDef actionNode fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#fff;
    classDef toolNode fill:#1e293b,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef obsNode fill:#1e293b,stroke:#06b6d4,stroke-width:2px,color:#fff;
    classDef decisionNode fill:#1e1b4b,stroke:#6366f1,stroke-width:2px,color:#fff;
    classDef finalNode fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#fff;
```

### 2. Gelişmiş RAG Boru Hattı (Hybrid Search & Reranking)
```mermaid
flowchart LR
    Q(["Kullanıcı Sorgusu"]) --> H["Dense (Vektör) + Sparse (BM25)"]
    H --> RRF["Reciprocal Rank Fusion"]
    RRF --> Rerank["Cross-Encoder Reranker"]
    Rerank --> LLM["LLM Sentezi & Yanıt"]

    classDef default fill:#1e293b,stroke:#38bdf8,stroke-width:1.5px,color:#fff;
```

### 3. Çoklu Ajan ve Supervisor Orkestrasyonu
```mermaid
flowchart TB
    Client(["Kullanıcı Görevi"]) --> Sup["Supervisor Agent"]
    Sup <--> State[("Shared State")]
    Sup --> W1["Researcher Agent"]
    Sup --> W2["Coder Agent"]
    State --> Critic["Reviewer / Critic"]
    Critic --> Sup

    classDef default fill:#1e293b,stroke:#a855f7,stroke-width:1.5px,color:#fff;
```

---

## ✅ Kontrol Listesi (Checklist)

- [x] Tüm dosyalar projenin mevcut kök dizini yapısına zarar vermeyecek şekilde izole bir `presentation/` dizininde konumlandırıldı.
- [x] Slaytlar standart Markdown ve Marp CLI / VS Code Marp uzantısıyla tam uyumlu formatta test edildi.
- [x] Mermaid diyagram sözdizimleri GitHub Markdown üzerinde sorunsuz render edilecek şekilde doğrulandı.
- [x] Görsel üretim promptları Midjourney v6, Flux.1 ve DALL-E 3 parametrelerine uygun hazırlandı.
- [x] Her hafta için eğitmen konuşma notları (Speaker Notes) eksiksiz eklendi.

---

## 💬 Topluluk Katkı Notu (Contributor's Note)

Bu içerikler, **Türkiye Veri Topluluğu**'nun açık kaynak ve paylaşım kültürünü desteklemek, bootcamp katılımcılarına dünya standartlarında görsel ve teknik eğitim materyali sunmak amacıyla titizlikle hazırlanmıştır. İncelemenizi ve geri bildirimlerinizi rica ederim. Katkı sağlamaktan mutluluk duyarım! 🚀
