import pandas as pd
import matplotlib.pyplot as plt

# 1. VERİLERİ OKUMA
# Dünya Bankası verilerinde ilk 4 satır açıklama olduğu için 'skiprows=4' ile onları atlıyoruz.
verim_data = pd.read_csv("API_AG.YLD.CREL.KG_DS2_en_csv.csv", skiprows=4)
gubre_data = pd.read_csv("API_AG.CON.FERT.ZS_DS2_en_csv.csv", skiprows=4)

# 2. GÜBRE VERİSİNİ DÜZENLEME
# Sütun isimleri arasında dolaşıp sadece rakam olanları (yılları) buluyoruz.
yil_sutunlari = []
for col in gubre_data.columns:
    if col.isdigit():
        yil_sutunlari.append(col)

# 'melt' komutu ile yan yana duran yılları alt alta satır haline getiriyoruz.
gubre_duzenli = gubre_data.melt(id_vars=["Country Name"], value_vars=yil_sutunlari, var_name="Yil", value_name="Gubre_Miktari")

# Tüm ülkeler arasından sadece Türkiye'yi seçiyoruz ve yılı sayıya çeviriyoruz.
gubre_tr = gubre_duzenli[gubre_duzenli["Country Name"] == "Turkiye"].copy()
gubre_tr["Yil"] = gubre_tr["Yil"].astype(int)

# 3. VERİM VERİSİNİ DÜZENLEME
# Aynı düzenleme işlemlerini (yılları satıra çevirme ve filtreleme) verim verisi için de yapıyoruz.
verim_duzenli = verim_data.melt(id_vars=["Country Name"], value_vars=yil_sutunlari, var_name="Yil", value_name="Verim_Miktari")
verim_tr = verim_duzenli[verim_duzenli["Country Name"] == "Turkiye"].copy()
verim_tr["Yil"] = verim_tr["Yil"].astype(int)

# 4. TABLOLARI BİRLEŞTİRME
# İki tabloyu "Yil" sütunu üzerinden eşleştirip tek bir tablo yapıyoruz.
tablo = pd.merge(gubre_tr, verim_tr, on=["Country Name", "Yil"], how="inner")

# Eksik veri olan satırları temizliyoruz ve yılları sıralıyoruz.
tablo = tablo.dropna()
tablo = tablo.sort_values("Yil")

# 5. GRAFİK ÇİZME
# Grafik çerçevesini ve çizim alanını oluşturuyoruz.
cerceve, sol_eksen = plt.subplots(figsize=(11, 6))

# SOL EKSEN (Gübre Verisi)
# İlk eksene gübre verilerini kırmızı renk ile çizdiriyoruz.
sol_eksen.set_xlabel('Yıl')
sol_eksen.set_ylabel('Gübre Tüketimi (kg/hektar)', color='red')
cizim1 = sol_eksen.plot(tablo["Yil"], tablo["Gubre_Miktari"], color='red', linewidth=2, marker='o', label="Gübre Tüketimi")
sol_eksen.tick_params(axis='y', labelcolor='red')
sol_eksen.grid(True, linestyle='--', alpha=0.5)

# SAĞ EKSEN (Verim Verisi)
# Verim ve gübre değerleri sayısal olarak çok farklı olduğu için ikinci bir eksen (twinx) oluşturuyoruz.
sag_eksen = sol_eksen.twinx() 
sag_eksen.set_ylabel('Tahıl Verimi (kg/hektar)', color='blue')
cizim2 = sag_eksen.plot(tablo["Yil"], tablo["Verim_Miktari"], color='blue', linewidth=2, marker='s', label="Tahıl Verimi")
sag_eksen.tick_params(axis='y', labelcolor='blue')

# LEJANT AYARLARI
# İki farklı çizimi birleştirip sol üst köşede tek bir kutu içinde gösteriyoruz.
toplam_cizimler = cizim1 + cizim2
etiketler = [c.get_label() for c in toplam_cizimler]
sol_eksen.legend(toplam_cizimler, etiketler, loc="upper left")

# Başlık ekleyip grafiği gösteriyoruz.
plt.title("Türkiye: Gübre Kullanımı ve Tarımsal Verim İlişkisi")
plt.show()