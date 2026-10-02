# Üç proje için etkileşimli sunum demoları

`index.html` dosyasını Chrome, Safari veya Edge ile açın. İnternet, sunucu, kurulum veya API anahtarı gerekmez. Üst sekmelerle proje değiştirin. Sunumun FinSight, ShopOps ve TrialMatch slaytlarındaki bağlantılar ilgili demoyu yeni sekmede açar.

Bu paket, bitmiş ürünün kullanıcı deneyimini örnek verilerle gösteren bir sunum demosudur. Bootcamp'in tam Temel/Hedef teslimi değildir. LLM çağrısı, RAG, MCP, gerçek veri entegrasyonu ve ölçülmüş agent değerlendirmesi içermez. Ekrandaki adımlar gerçek kod kontrolleridir; modelin düşüncesi veya bir agent trace'i olarak sunulmaz.

## 9 dakikalık gösterim

### FinSight — 3 dakika

1. Atlas Yazılım ile araştırma özetini açın. Gelir, marj ve büyümenin ilişkisini gösterin.
2. Kaynak satırlarını açıp 2024 gelirinin 1.188, net kârın 190 olduğunu gösterin. Marj = 190 / 1.188.
3. Nova'yı seçin: farklı veriyle sonuç değişir. İki şirketi karşılaştırın.
4. “Bu hisseyi almalı mıyım?” görevini seçip kapsam reddini gösterin.

Söylenecek cümle: “Bu örnekte hesap ve kaynak ilişkisini gösteriyoruz. Öğrenci projesinde kayıtlar SEC'ten gelecek, retrieval ve agent katmanı bu sonuca ulaşacak.”

### ShopOps — 3 dakika

1. 1001 siparişinde “Vazgeçtim” seçin. 240 BRL tutarı, onay kutusunu ve talep oluşturmayı gösterin.
2. Oluşturulan talep sonrası ikinci talebin engellendiğini gösterin.
3. 1002 için “Vazgeçtim”: ürün penceresi kapalıdır, gecikme nedeniyle yalnız 80 BRL kargo talep edilebilir. “Ürün hasarlı” seçilince 700 BRL ve kıdemli inceleme çıkar.
4. 2001 ile olmayan 9999 siparişlerinin aynı “bulunamadı” yanıtını verdiğini gösterin.

Söylenecek cümle: “İade tutarını ve yetkiyi model belirlemiyor. Burada çalışan örnek kuralları görüyoruz; gerçek projede aynı kurallar sunucudaki tool katmanında uygulanmalı.”

### TrialMatch — 3 dakika

1. 54 yaş, HER2 pozitif sentetik vakayı açın. ECOG eksik olduğu için ilgili kriter UNKNOWN'dır.
2. ECOG değerini 1 yapın; ilgili örnek kriterin değiştiğini gösterin.
3. “Beyin metastazı var” vakasını seçip kriterin NOT_MET olduğunu gösterin.
4. “Eksik bilgiler” vakasına geçin. Eksik verinin otomatik olarak olumlu değerlendirilmediğini anlatın.

Söylenecek cümle: “Bunlar gerçek NCT kayıtları değil, kurgusal protokoller. Gerçek sistemde kaynak kriteri, tarih ve hekim incelemesi gerekecek.”

## Kapsam ve veri

- FinSight: iki kurgusal şirket, üç yıllık sayısal kayıt, hesap ve kaynak satırı; SEC veya yatırım tavsiyesi yok.
- ShopOps: beş sentetik sipariş; R0/R1, durum kontrolü, R6–R11 kapsamındaki gösterim kuralları. Voucher dağılımı R12, satıcı gecikmesi R13, operasyon SQL ve yorum analizi gösterilmez. Tarayıcıdaki müşteri seçimi bir gerçek kimlik doğrulama sistemi değildir.
- TrialMatch: üç kurgusal protokol, yapılandırılmış sentetik profil, deterministik kriter karşılaştırması. Klinik doğrulama, serbest metin çıkarımı, API sorgusu, PII tespiti veya tedavi önerisi yok.
- İade kayıtları sekme belleğindedir. “Demoyu sıfırla” veya sayfa yenileme kayıtları siler. Gerçek ödeme yapılmaz.
- Veri kümesi bu demo için oluşturuldu; SEC, Olist ve ClinicalTrials.gov'dan alınmış veri içermez.

## Kontrol

`node --test engine.test.cjs`

Finans hesabı, 14 günlük sınır, hasarlı ürün penceresi, yetkisiz kayıt, açık onay, yinelenen talep, eksik ve uyumsuz kriter test edilir.

## Dosyalar

- `engine.js`: veri ve hesap/karar fonksiyonları.
- `app.js`: kullanıcı etkileşimleri ve sonuçlar.
- `style.css`: duyarlı görsel düzen.
- `index.html`: giriş sayfası.

Sunumla birlikte paylaşırken `Final_Projeler/Demolar` ve `Final_Projeler/Sunum` konumlarını koruyun.
