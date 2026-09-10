# 📊 AI Agents Bootcamp - Sunum & Görsel Materyalleri

Bu dizin, **Türkiye Veri Topluluğu AI Agents Bootcamp** eğitiminin 6 haftalık sunum slaytlarını, teknik mimari diyagramlarını ve görsel üretim promptlarını içerir.

## 📂 Dizin Yapısı

```
presentation/
├── README.md                           # Bu dokümantasyon
├── docs/
│   └── curriculum_deep_dive.md         # 6 haftalık kapsamlı teknik ders notları & teorik rehber
├── slides/
│   └── bootcamp_deck.md                # 6 haftalık Marp / Slidev uyumlu sunum destesi
├── assets/
│   └── diagrams/                       # Modüler Mermaid.js mimari diyagramları
│       ├── single_agent_cycle.mmd       # Tekil Agent Döngüsü (ReAct)
│       ├── advanced_rag_flow.mmd        # Gelişmiş RAG Mimarisi
│       └── multi_agent_orchestration.mmd # Çoklu Ajan ve Supervisor Mimarisi
└── prompts/
    └── image_generation.md             # Midjourney / Flux / DALL-E görsel promptları
```

---

## 🚀 Slaytları Görüntüleme ve Dışa Aktarma

Slaytlar, Markdown standardında [Marp](https://marp.app/) ve [Slidev](https://sli.dev/) araçlarıyla %100 uyumlu olarak hazırlanmıştır.

### 1. VS Code ile Canlı Önizleme (Önerilen)
1. VS Code üzerinde **Marp for VS Code** eklentisini kurun.
2. `presentation/slides/bootcamp_deck.md` dosyasını açın.
3. Sağ üstteki **Marp Preview** ikonuna tıklayarak sunumu slayt formatında anlık görüntüleyin.
4. VS Code komut paletinden (`Ctrl+Shift+P` / `Cmd+Shift+P`) `Marp: Export Slide Deck` seçeneğiyle **PDF** veya **HTML** olarak dışa aktarın.

### 2. Marp CLI ile Terminalden Çıktı Alma
```bash
# HTML formatında interaktif sunum oluşturma
npx @marp-team/marp-cli@latest presentation/slides/bootcamp_deck.md -o presentation/slides/bootcamp_deck.html

# PDF formatında yüksek çözünürlüklü dışa aktarma
npx @marp-team/marp-cli@latest presentation/slides/bootcamp_deck.md --pdf -o presentation/slides/bootcamp_deck.pdf
```

---

## 📐 Mimari Diyagramları (Mermaid.js)

`presentation/assets/diagrams/` altındaki diyagramlar:
- GitHub arayüzünde Markdown blokları içinde doğrudan görselleştirilebilir.
- [Mermaid Live Editor](https://mermaid.live/) üzerinden SVG veya PNG formatında dışa aktarılabilir.
- Sunum slaytları içine gömülü olarak yerleştirilmiştir.
