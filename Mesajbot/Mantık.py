from datetime import datetime, timedelta
from collections import defaultdict
import discord
import sqlite3
import random
import requests
import pytz

VERİ_TABANI = "Veri_Tabanı.db"

def Parola_Gönder(parola_uzunluğu):
    karakterler = "é!'£^#+$%½&/=?\*_-@¨¨~~æß´`,;<>.:AaBbCcÇçDdEeFfGgĞğHhIıİiJjKkLlMmNnOoÖöPpQqRrSsŞşTtUuÜüVvWwXxYyZz1234567890"
    parola = ""
    for a in range(parola_uzunluğu):
        parola += random.choice(karakterler)
    sonuc = "Parola: " + parola
    return sonuc

def Emoji_Gönder():
    emoji = "\U0001f642"
    return random.choice(emoji)

class Sorular:
    def __init__(self, text, answer_id, *secenekler):
        self.text = text
        self.answer_id = answer_id
        self.secenekler = secenekler

    def Düğmeler(self):
        düğmeler = []
        for a, secenek in enumerate(self.secenekler):
            button = discord.ui.Button(
                label = secenek,
                style = discord.ButtonStyle.primary,
                custom_id = f"answer_{a}"
            )
            düğmeler.append(button)
        return düğmeler

sorular = [
    # Fen Bilimleri İle İlgili Sorular
    Sorular("Dünya'nın uydusu nedir?", 2, "Jüpiter", "Mars", "Ay"),
    Sorular("Hangi gezegen halkalara sahiptir?", 0, "Satürn", "Mars", "Venüs"),
    Sorular("Dünya'nın güneş etrafında dönme süresi nedir?", 0, "365 Gün 6 Saat", "24 Saat", "30 Gün"),
    Sorular("Dünya'nın kendi etrafında dönme süresi kaç saattir?", 1, "5 Saat", "24 Saat", "12 Saat"),
    Sorular("Ay'ın Dünya etrafında dönme süresi nedir?", 2, "1 Hafta", "4 Gün", "29,5 Gün"),
    Sorular("Güneş Sistemi’ndeki en soğuk gezegen hangisidir?", 2, "Merkür", "Plüton", "Neptün"),
    Sorular("Güneş Sistemi’ndeki en sıcak gezegen hangisidir?", 1, "Jüpiter", "Venüs", "Mars"),

    Sorular("Hangi enerji kaynağı yenilenebilir değildir?", 0, "Petrol", "Güneş", "Rüzgâr"),

    Sorular("Hangi madde suyu emebilir?", 0, "Sünger", "Cam", "Metal"),

    Sorular("Hangi madde elektrik iletkenidir?", 1, "Tahta", "Bakır", "Cam"),
    Sorular("Hangi madde elektrik yalıtkanıdır?", 1, "Metal", "Tahta", "Bakır"),

    Sorular("İnsanlar hangi gazı solur?", 2, "Karbondioksit", "Azot", "Oksijen"),

    # Hayat Bilgisi İle İlgili Sorular
    Sorular("Hangisi bir tatlı türüdür?", 2, "Lahana", "Ekmek", "Baklava"),
    Sorular("Hangi meyve sarıdır?", 2, "Çilek", "Karpuz", "Muz"),
    Sorular("Hangi meyve ekşi tadıyla bilinir?", 0, "Limon", "Karpuz", "Çilek"),

    Sorular("Hangisi bir doğal afet değildir?", 1, "Deprem", "Araba Kazası", "Yangın"),

    # Hayvanlar İle İlgili Sorular
    Sorular("Hangi hayvan dikenlidir?", 0, "Kirpi", "Kedi", "Köpek"),
    Sorular("Hangi hayvan yuvasını ağaçta yapar?", 1, "Aslan", "Karga", "Fare"),
    Sorular("Hangi hayvan uçamaz?", 1, "Kartal", "Fil", "Serçe"),
    Sorular("Hangi hayvan suda yaşar?", 0, "Balık", "Kedi", "Kuş"),
    Sorular("En hızlı kara hayvanı hangisidir?", 1, "Aslan", "Çita", "At"),

    # Bilişim İle İlgili Sorular
    Sorular("Hangi kısa yol kopyalama işlemi yapar?", 0, "Ctrl + C", "Ctrl + X", "Ctrl + V"),
    Sorular("Hangi kısa yol yapıştırma işlemi yapar?", 2, "Ctrl + X", "Ctrl + Z", "Ctrl + V"),
    Sorular("Hangi kısa yol kesme işlemi yapar?", 1, "Ctrl + C", "Ctrl + X", "Ctrl + V"),
    Sorular("Hangi kısa yol geri alma işlemi yapar?", 2, "Ctrl + S", "Ctrl + P", "Ctrl + Z"),
    Sorular("Hangi kısa yol hepsini seçme işlemi yapar?", 0, "Ctrl + A", "Ctrl + C", "Ctrl + V"),
    Sorular("Hangi kısa yol kaydetme işlemi yapar?", 1, "Ctrl + P", "Ctrl + S", "Ctrl + Z"),
    Sorular("Hangi kısa yol yazdırma işlemi yapar?", 2, "Ctrl + S", "Ctrl + C", "Ctrl + P"),

    Sorular("Hangisi teknolojik bir cihaz değildir?", 1, "Tablet", "Masa", "Bilgisayar"),

    # Türkçe İle İlgili Sorular
    Sorular("Bir gün kaç saattir?", 0, "24", "12", "60"),
    Sorular("Bir saat kaç dakikadır?", 0, "60", "100", "24"),
    Sorular("Bir dakika kaç saniyedir?", 0, "60", "100", "30"),
    Sorular("Bir yıl kaç aydır?", 0, "12", "10", "6"),
    Sorular("Bir mevsim kaç aydır?", 0, "3", "5", "8"),
    Sorular("Bir hafta kaç gündür?", 0, "7", "5", "10"),
    Sorular("Bir hafta kaç saattir?", 1, "120", "168", "144"),
    Sorular("Bir saat kaç dakikadır?", 0, "60", "24", "100"),
    Sorular("Bir gün kaç dakikadır?", 1, "1200", "1440", "1000"),
    Sorular("Bir yılda kaç tane mevsim vardır?", 0, "4", "2", "9"),

    Sorular("Türk alfabesinde kaç harf vardır?", 0, "29", "26", "32"),
]

class Hesap_Makinesi(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.input_text = ""

    async def Yazı(self, interaction: discord.Interaction):
        content_to_send = f"```{self.input_text}```" if self.input_text else ""
        await interaction.response.edit_message(content=content_to_send, view=self)

    @discord.ui.button(label="1", style=discord.ButtonStyle.primary, row=0)
    async def Bir(self, button, interaction: discord.Interaction):
        self.input_text += "1"; await self.Yazı(interaction)

    @discord.ui.button(label="2", style=discord.ButtonStyle.primary, row=0)
    async def İki(self, button, interaction: discord.Interaction):
        self.input_text += "2"; await self.Yazı(interaction)

    @discord.ui.button(label="3", style=discord.ButtonStyle.primary, row=0)
    async def Üç(self, button, interaction: discord.Interaction):
        self.input_text += "3"; await self.Yazı(interaction)

    @discord.ui.button(label="+", style=discord.ButtonStyle.success, row=0)
    async def Artı(self, button, interaction: discord.Interaction):
        self.input_text += "+"; await self.Yazı(interaction)

    @discord.ui.button(label="4", style=discord.ButtonStyle.primary, row=1)
    async def Dört(self, button, interaction: discord.Interaction):
        self.input_text += "4"; await self.Yazı(interaction)

    @discord.ui.button(label="5", style=discord.ButtonStyle.primary, row=1)
    async def Beş(self, button, interaction: discord.Interaction):
        self.input_text += "5"; await self.Yazı(interaction)

    @discord.ui.button(label="6", style=discord.ButtonStyle.primary, row=1)
    async def Altı(self, button, interaction: discord.Interaction):
        self.input_text += "6"; await self.Yazı(interaction)

    @discord.ui.button(label="-", style=discord.ButtonStyle.success, row=1)
    async def Eksi(self, button, interaction: discord.Interaction):
        self.input_text += "-"; await self.Yazı(interaction)

    @discord.ui.button(label="7", style=discord.ButtonStyle.primary, row=2)
    async def Yedi(self, button, interaction: discord.Interaction):
        self.input_text += "7"; await self.Yazı(interaction)

    @discord.ui.button(label="8", style=discord.ButtonStyle.primary, row=2)
    async def Sekiz(self, button, interaction: discord.Interaction):
        self.input_text += "8"; await self.Yazı(interaction)

    @discord.ui.button(label="9", style=discord.ButtonStyle.primary, row=2)
    async def Dokuz(self, button, interaction: discord.Interaction):
        self.input_text += "9"; await self.Yazı(interaction)

    @discord.ui.button(label="x", style=discord.ButtonStyle.success, row=2)
    async def Çarpı(self, button, interaction: discord.Interaction):
        self.input_text += "*"; await self.Yazı(interaction)

    @discord.ui.button(label="Sıfırla", style=discord.ButtonStyle.danger, row=3)
    async def Sıfırla(self, button, interaction: discord.Interaction):
        self.input_text = ""; await self.Yazı(interaction)

    @discord.ui.button(label="0", style=discord.ButtonStyle.primary, row=3)
    async def Sıfır(self, button, interaction: discord.Interaction):
        self.input_text += "0"; await self.Yazı(interaction)

    @discord.ui.button(label="=", style=discord.ButtonStyle.primary, row=3)
    async def Eşittir(self, button, interaction: discord.Interaction):
        try:
            self.input_text = str(eval(self.input_text))
        except:
            self.input_text = "Mesajınız Anlaşılamadı."
        await self.Yazı(interaction)

    @discord.ui.button(label="÷", style=discord.ButtonStyle.success, row=3)
    async def Bölü(self, button, interaction: discord.Interaction):
        self.input_text += "/"; await self.Yazı(interaction)

beceriler = [(_,) for _ in ["Python", "SQL", "API", "Discord"]]

durumlar = [(_,) for _ in [
    "Prototip yapılmaya başlandı.",
    "Prototip geliştirme aşamasında.",
    "Prototip tamamlandı."
]]

class Veritabani_Yöneticisi:
    def __init__(self, veritabani):
        self.veritabani = veritabani

    def Tablolar(self):
        bağlantı = sqlite3.connect(self.veritabani)
        with bağlantı:
            bağlantı.execute("""CREATE TABLE IF NOT EXISTS projeler (
                                    proje_numarası INTEGER PRIMARY KEY,
                                    kullanıcı_numarası INTEGER,
                                    proje_İsmi TEXT NOT NULL,
                                    açıklama TEXT,
                                    link TEXT,
                                    durum INTEGER,
                                    FOREIGN KEY(durum) REFERENCES durum(durum)
                                )""")
            bağlantı.execute("""CREATE TABLE IF NOT EXISTS beceriler (
                                    beceri INTEGER PRIMARY KEY,
                                    beceri_ismi TEXT
                                )""")
            bağlantı.execute("""CREATE TABLE IF NOT EXISTS proje_beceriler (
                                    proje_numarası INTEGER,
                                    beceri INTEGER,
                                    FOREIGN KEY(proje_numarası) REFERENCES projeler(proje_numarası),
                                    FOREIGN KEY(beceri) REFERENCES beceriler(beceri)
                                )""")
            bağlantı.execute("""CREATE TABLE IF NOT EXISTS durum (
                                    durum INTEGER PRIMARY KEY,
                                    durum_ismi TEXT
                                )""")
            bağlantı.commit()

    def __Çoklu_Ekle(self, sql, veri):
        bağlantı = sqlite3.connect(self.veritabani)
        with bağlantı:
            bağlantı.executemany(sql, veri)
            bağlantı.commit()

    def __Veri_Seç(self, sql, veri=tuple()):
        bağlantı = sqlite3.connect(self.veritabani)
        with bağlantı:
            imleç = bağlantı.cursor()
            imleç.execute(sql, veri)
            return imleç.fetchall()

    def Varsayılanı_Ekle(self):
        self.__Çoklu_Ekle("INSERT INTO beceriler (beceri_ismi) VALUES(?)", beceriler)
        self.__Çoklu_Ekle("INSERT INTO durum (durum_ismi) VALUES(?)", durumlar)

    def Proje_Ekle(self, kullanıcı_numarası, proje_ismi, açıklama, link, durum):
        bağlantı = sqlite3.connect(self.veritabani)
        with bağlantı:
            bağlantı.execute(
                "INSERT INTO projeler (kullanıcı_numarası, proje_İsmi, açıklama, link, durum) VALUES (?, ?, ?, ?, ?)",
                (kullanıcı_numarası, proje_ismi, açıklama, link, durum)
            )
            bağlantı.commit()

    def Projeleri_Getir(self):
        return self.__Veri_Seç("SELECT * FROM projeler")

    def Proje_Getir_By_Id(self, proje_id):
        return self.__Veri_Seç("SELECT * FROM projeler WHERE proje_numarası = ?", (proje_id,))

    def Proje_Durumunu_Güncelle(self, proje_id, durum):
        bağlantı = sqlite3.connect(self.veritabani)
        with bağlantı:
            bağlantı.execute("UPDATE projeler SET durum = ? WHERE proje_numarası = ?", (durum, proje_id))
            bağlantı.commit()

    def Projeyi_Sil(self, proje_id):
        bağlantı = sqlite3.connect(self.veritabani)
        with bağlantı:
            bağlantı.execute("DELETE FROM projeler WHERE proje_numarası = ?", (proje_id,))
            bağlantı.commit()

if __name__ == "__main__":
    yonetici = Veritabani_Yöneticisi(VERİ_TABANI)
    yonetici.Tablolar()
    yonetici.Varsayılanı_Ekle()

    yonetici.Proje_Ekle(
        1,
        "Discord Yardımcı Bot",
        "Discord için moderasyon ve eğlence botu",
        "https://github.com/mertnalbantoglu687/Mesajbot.git",
        2
    )

    print(yonetici.Projeleri_Getir())
