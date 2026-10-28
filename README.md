# 💉 Prompt Injector (AI Metadata Enjektör & Dönüştürücü)

**Prompt Injector**, yapay zeka tarafından üretilmiş veya harici görsellerin (WebP, JPG, JPEG, PNG) metadata'sına toplu olarak prompt enjekte eden, formatlarını Automatic1111 / WebUI standartlarıyla tam uyumlu PNG'ye dönüştüren modern bir masaüstü uygulamasıdır.

Sürükle & bırak (Drag and Drop) desteği ve modern karanlık teması (CustomTkinter) sayesinde tek tıkla yüzlerce görseli işleyebilirsiniz.

---

## ✨ Özellikler

- **📁 Klasör Bazlı Sürükle & Bırak:** İstediğiniz klasörü doğrudan pencereye bırakın; içindeki tüm görseller otomatik algılanır.
- **🖼️ Çoklu Format Desteği:** `.webp`, `.jpg`, `.jpeg` ve `.png` formatındaki tüm görselleri destekler.
- **🤖 A1111 / Stable Diffusion Standart Uyumu:** Prompt metnini doğrudan PNG chunk'larında `parameters` anahtarına yazar. Böylece Automatic1111, ComfyUI, Civitai ve PromptVault gibi araçlar promptu anında tanır.
- **🛡️ Orijinalleri Koruma:** Orijinal dosyalarınıza dokunulmaz; dönüştürülen görseller ilgili klasörün içinde `PNG_Ciktilar/` adında yeni bir klasöre kaydedilir.
- **⚡ Hazır EXE Desteği:** Python kurulu olmasa bile `dist/enjektor.exe` üzerinden doğrudan çalıştırılabilir.

---

## 🚀 Hızlı Başlangıç

### Yöntem 1: Hazır `.exe` ile Çalıştırma
[dist/enjektor.exe](dist/enjektor.exe) dosyasını indirip çift tıklayarak hemen kullanmaya başlayabilirsiniz.

### Yöntem 2: Python Kaynak Kodundan Çalıştırma

1. **Gereksinimleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Uygulamayı başlatın:**
   ```bash
   python enjektor.py
   ```

---

## 🛠️ Bağımsız `.exe` Olarak Yeniden Derleme (Build)

Uygulamayı tek dosya halinde `.exe` yapmak isterseniz:

```bash
pyinstaller enjektor.spec
```

Derlenen çalıştırılabilir dosya `dist/enjektor.exe` içerisine oluşturulacaktır.

---

## 📋 Nasıl Kullanılır?

1. Uygulamayı açın.
2. Üst kısımdaki metin kutusuna görsellere gömmek istediğiniz **Prompt**'u yazın.
3. Görsellerinizin bulunduğu klasörü **"İşlenecek Klasörü Buraya Sürükleyip Bırakın"** alanına sürükleyin.
4. İşlem tamamlandığında görselleriniz ilgili klasör içerisindeki `PNG_Ciktilar` klasörüne A1111 metadata'sı eklenmiş PNG formatında kaydedilir.

---

## 📄 Lisans
MIT License
