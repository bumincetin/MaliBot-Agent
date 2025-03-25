# MaliBot - Mali Müşavir Asistanı

MaliBot, Türkiye'deki mali müşavirler için geliştirilmiş yapay zeka destekli bir asistan uygulamasıdır. Ollama üzerinde çalışan Mistral modelini kullanarak Türkçe dil desteği ile mali müşavirlere günlük işlerinde yardımcı olur.

## Özellikler

- 🤖 Ollama (Mistral) tabanlı Türkçe dil desteği
- 📊 KDV Hesaplama Aracı
- 📚 Türk Vergi Mevzuatı Arama ve Bilgi Sorgulama
- 📄 E-Fatura PDF Analiz ve Özetleme
- ✉️ Resmi Yazışma E-posta Oluşturma
- ⏰ Beyanname Takip ve Hatırlatma Sistemi
- 🧠 FAISS/ChromaDB ile Gelişmiş Bellek Sistemi

## Kurulum

1. Ollama'yı yükleyin:
   - Windows için: https://ollama.ai/download
   - Linux için: `curl https://ollama.ai/install.sh | sh`
   - macOS için: `brew install ollama`

2. Mistral modelini indirin:
```bash
ollama pull mistral
```

3. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

4. Uygulamayı başlatın:
```bash
python main.py
```

## Proje Yapısı

```
malibot/
├── tools/           # Özel araçlar (KDV hesaplayıcı, PDF işleyici vb.)
├── memory/          # FAISS/ChromaDB bellek sistemi
├── chat/           # Sohbet yönetimi ve Ollama entegrasyonu
├── frontend/       # Gradio arayüzü
└── main.py         # Ana uygulama
```

## Kullanım

1. Gradio arayüzünü açın (varsayılan: http://localhost:7860)
2. PDF dosyalarınızı yükleyin (vergi mevzuatı, e-faturalar)
3. Sohbet başlatın ve MaliBot'a sorularınızı sorun

## Gereksinimler

- Python 3.8+
- Ollama
- Mistral modeli
- Gerekli Python paketleri (requirements.txt'de listelenmiştir)

## Lisans

MIT License 