import os
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
from PIL.PngImagePlugin import PngInfo

# CustomTkinter ve TkinterDnD2'yi birleştiren köprü sınıf
class CTk_DnD(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class MetadataInjectorApp(CTk_DnD):
    def __init__(self):
        super().__init__()

        self.title("AI Metadata Enjektör & Dönüştürücü")
        self.geometry("650x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # --- Arayüz Elemanları ---
        
        # 1. Prompt Giriş Alanı
        self.prompt_label = ctk.CTkLabel(self, text="Görsellere Eklenecek Prompt:", font=("Segoe UI", 14, "bold"))
        self.prompt_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.prompt_text = ctk.CTkTextbox(self, height=120)
        self.prompt_text.pack(pady=0, padx=20, fill="x")
        self.prompt_text.insert("0.0", "Masterpiece, best quality, ultra detailed, concept art...")

        # 2. Sürükle & Bırak Alanı
        self.drop_frame = ctk.CTkFrame(self, height=150, corner_radius=10, border_width=2, border_color="#555555")
        self.drop_frame.pack(pady=20, padx=20, fill="x")
        self.drop_frame.pack_propagate(False) # Frame boyutunun içindeki label'a göre küçülmesini engeller
        
        self.drop_label = ctk.CTkLabel(
            self.drop_frame, 
            text="İşlenecek Klasörü Buraya Sürükleyip Bırakın\n(WebP, JPG, JPEG, PNG desteklenir)", 
            font=("Segoe UI", 16)
        )
        self.drop_label.pack(expand=True)
        
        # Sürükle-bırak (Drag&Drop) etkinliklerini bağlama
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.klasor_birakildi)

        # 3. Log / Konsol Alanı
        self.log_label = ctk.CTkLabel(self, text="İşlem Geçmişi:", font=("Segoe UI", 12, "bold"))
        self.log_label.pack(pady=(5, 0), padx=20, anchor="w")

        self.log_text = ctk.CTkTextbox(self, height=150, state="disabled", fg_color="#1e1e1e", text_color="#00ff00")
        self.log_text.pack(pady=(5, 20), padx=20, fill="both", expand=True)

    def log_yaz(self, mesaj):
        """Konsol ekranına log basar ve en aşağı kaydırır."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", mesaj + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.update()

    def klasor_birakildi(self, event):
        """Kullanıcı bir dosya veya klasör bıraktığında tetiklenir."""
        # tkinterdnd2'nin boşluklu yolları güvenli parse etmesi için splitlist kullanıyoruz
        yollar = self.tk.splitlist(event.data)
        if not yollar:
            return
            
        hedef_yol = yollar[0] # Sadece ilk bırakılan öğeyi al

        if not os.path.isdir(hedef_yol):
            self.log_yaz(f"[HATA] Lütfen tekil dosya yerine bir KLASÖR sürükleyin! Bırakılan: {hedef_yol}")
            return

        ortak_prompt = self.prompt_text.get("0.0", "end").strip()
        if not ortak_prompt:
            self.log_yaz("[HATA] Lütfen işleme başlamadan önce bir prompt girin!")
            return
        
        self.islem_baslat(hedef_yol, ortak_prompt)

    def islem_baslat(self, girdi_klasoru, ortak_prompt):
        self.log_yaz(f"\n--- YENİ İŞLEM BAŞLIYOR ---")
        self.log_yaz(f"Hedef: {girdi_klasoru}")
        
        # Çıktı klasörünü orijinal klasörün içine oluştur
        cikti_klasoru = os.path.join(girdi_klasoru, "PNG_Ciktilar")
        if not os.path.exists(cikti_klasoru):
            os.makedirs(cikti_klasoru)

        desteklenen_uzantilar = ('.webp', '.jpg', '.jpeg', '.png')
        basarili = 0
        hatali = 0
        
        dosyalar = [d for d in os.listdir(girdi_klasoru) if d.lower().endswith(desteklenen_uzantilar)]
        
        if not dosyalar:
            self.log_yaz("[UYARI] Klasörde desteklenen formatta (WebP, JPG, PNG) görsel bulunamadı.")
            return

        for dosya_adi in dosyalar:
            girdi_yolu = os.path.join(girdi_klasoru, dosya_adi)
            isim, _ = os.path.splitext(dosya_adi)
            cikti_yolu = os.path.join(cikti_klasoru, f"{isim}.png")

            try:
                # with bloğu kullanarak bellekte sızıntı olmasını önlüyoruz
                with Image.open(girdi_yolu) as img:
                    yeni_metadata = PngInfo()
                    # A1111 ve benzeri araçlar promptu "parameters" anahtarında arar
                    yeni_metadata.add_text("parameters", ortak_prompt)
                    yeni_metadata.add_text("Description", "Custom UI Injection")

                    if img.mode != 'RGB' and img.mode != 'RGBA':
                        img = img.convert('RGB')

                    img.save(cikti_yolu, "PNG", pnginfo=yeni_metadata)
                
                self.log_yaz(f"[+] İşlendi: {dosya_adi}")
                basarili += 1
                
            except Exception as e:
                self.log_yaz(f"[-] HATA ({dosya_adi}): {str(e)}")
                hatali += 1

        self.log_yaz(f"--- İŞLEM BİTTİ ---")
        self.log_yaz(f"Sonuç: {basarili} Başarılı, {hatali} Hatalı")
        self.log_yaz(f"Kayıt Yeri: {cikti_klasoru}\n")

if __name__ == "__main__":
    app = MetadataInjectorApp()
    app.mainloop()