from datetime import datetime, timedelta
from collections import defaultdict
import discord
import random
import requests
import calendar
import pytz

def Parola_Gönder(parola_uzunluğu):
    karakterler = "é!'£^#+$%½&/?\*_-@¨¨~~æß´`<>AaBbCcÇçDdEeFfGgĞğHhIıİiJjKkLlMmNnOoÖöPpRrSsŞşTtUuÜüVvYyZz1234567890"
    parola = ""
    for a in range(parola_uzunluğu):
        parola += random.choice(karakterler)
    sonuç = "Parola: " + parola
    return sonuç

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
    Sorular("Dünya'nın kendi etrafında dönme süresi nedir?", 1, "5 Saat", "24 Saat", "12 Saat"),
    Sorular("Ay'ın Dünya etrafında dönme süresi nedir?", 2, "1 Hafta", "4 Gün", "29,5 Gün"),
    Sorular("Güneş Sistemi’ndeki en soğuk gezegen hangisidir?", 2, "Merkür", "Satürn", "Neptün"),
    Sorular("Güneş Sistemi’ndeki en sıcak gezegen hangisidir?", 1, "Jüpiter", "Venüs", "Mars"),
    Sorular("Güneş'e en yakın gezegen hangisidir?", 0, "Merkür", "Venüs", "Dünya"),
    Sorular("Güneş'e en uzak gezegen hangisidir?", 2, "Satürn", "Uranüs", "Neptün"),
    Sorular("Hangisi gazsal bir gezegen değildir?", 1, "Jüpiter", "Dünya", "Satürn"),
    Sorular("Hangisi karasal bir gezegen değildir?", 0, "Jüpiter", "Venüs", "Mars"),
    Sorular("Hangisi gazsal bir gezegendir?", 0, "Satürn", "Merkür", "Venüs"),
    Sorular("Hangisi karasal bir gezegendir?", 2, "Jüpiter", "Neptün", "Mars"),
    Sorular("Güneş Sistemi’ndeki en büyük gezegen hangisidir?", 0, "Jüpiter", "Satürn", "Neptün"),
    Sorular("Güneş Sistemi’ndeki en küçük gezegen hangisidir?", 2, "Mars", "Venüs", "Merkür"),

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
    Sorular("En yavaş kara hayvanı hangisidir?", 1, "Kaplumbağa", "Tembel Hayvan", "Kirpi"),
    Sorular("En hızlı deniz hayvanı hangisidir?", 0, "Yelken Balığı", "Köpekbalığı", "Orkinos"),
    Sorular("En yavaş deniz hayvanı hangisidir?", 2, "Ahtapot", "Denizatı", "Deniz Yıldızı"),


    # Bilişim İle İlgili Sorular
    Sorular("Hangi kısa yol kopyalama işlemi yapar?", 0, "Ctrl + C", "Ctrl + X", "Ctrl + V"),
    Sorular("Hangi kısa yol yapıştırma işlemi yapar?", 2, "Ctrl + X", "Ctrl + Z", "Ctrl + V"),
    Sorular("Hangi kısa yol kesme işlemi yapar?", 1, "Ctrl + C", "Ctrl + X", "Ctrl + V"),
    Sorular("Hangi kısa yol geri alma işlemi yapar?", 2, "Ctrl + S", "Ctrl + P", "Ctrl + Z"),
    Sorular("Hangi kısa yol hepsini seçme işlemi yapar?", 0, "Ctrl + A", "Ctrl + C", "Ctrl + V"),
    Sorular("Hangi kısa yol kaydetme işlemi yapar?", 1, "Ctrl + P", "Ctrl + S", "Ctrl + Z"),
    Sorular("Hangi kısa yol yazdırma işlemi yapar?", 2, "Ctrl + S", "Ctrl + C", "Ctrl + P"),

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

    # Matematik İle İlgili Sorular
    Sorular("Hangi şeklin köşegeni yoktur?", 1, "Sekizgen", "Üçgen", "Beşgen"),
    Sorular("Hangi şeklin bütün kenar uzunlukları birbirine eşittir?", 0, "Kare", "Altıgen", "Dikdörtgen"),
    Sorular("Hangi şeklin karşılıklı kenar uzunlukları birbirine eşittir?", 1, "Üçgen", "Dikdörtgen", "Dokuzgen"),
    Sorular("Hangi şeklin karşılıklı kenar uzunlukları birbirine eşit değildir?", 2, "Kare", "Dikdörtgen", "Sekizgen"),
    Sorular("Hangi şeklin bütün açılarının uzunlukları birbirine eşittir?", 0, "Kare", "Beşgen", "Sekizgen"),
    Sorular("Hangi şeklin bütün açılarının uzunlukları birbirine eşit değildir?", 1, "Kare", "Üçgen", "Dikdörtgen"),
    Sorular("Hangi şeklin köşegen uzunlukları birbirine eşittir?", 0, "Dikdörtgen", "Altıgen", "Sekizgen"),
    Sorular("Hangi şeklin köşegen uzunlukları birbirine eşit değildir?", 2, "Dikdörtgen", "Kare", "Altıgen"),

    Sorular("Hangisi dar açıdır?", 0, "60°", "90°", "120°"),
    Sorular("Hangisi dar açı olamaz?", 2, "45°", "30°", "100°"),
    Sorular("Hangisi dik açıdır?", 1, "30°", "90°", "60°"),
    Sorular("Hangisi geniş açıdır?", 0, "120°", "75°", "40°"),
    Sorular("Hangisi geniş açı olamaz?", 2, "100°", "150°", "70°"),
    Sorular("Hangisi doğru açıdır?", 1, "55°", "180°", "85°"),
    Sorular("Hangisi tam açıdır?", 2, "320°", "280°", "360°"),

    Sorular("Hangisi çift bir sayıdır?", 0, "13598", "89547", "53273"),
    Sorular("Hangisi tek bir sayıdır?", 2, "23586", "84532", "28645"),

    Sorular("Hangisi bir asal sayıdır?", 1, "4", "7", "9"),
    Sorular("Hangisi bir asal sayı değildir?", 0, "8", "2", "5"),
]

class Hesap_Makinesi(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.input_text = ""

    async def Yazı(self, interaction: discord.Interaction):
        content_to_send = f"```{self.input_text}```" if self.input_text else ""
        await interaction.response.edit_message(content=content_to_send, view=self)

    @discord.ui.button(label = "1", style=discord.ButtonStyle.primary, row = 0)
    async def Bir(self, button, interaction: discord.Interaction):
        self.input_text += "1"; await self.Yazı(interaction)

    @discord.ui.button(label = "2", style=discord.ButtonStyle.primary, row = 0)
    async def İki(self, button, interaction: discord.Interaction):
        self.input_text += "2"; await self.Yazı(interaction)

    @discord.ui.button(label = "3", style=discord.ButtonStyle.primary, row = 0)
    async def Üç(self, button, interaction: discord.Interaction):
        self.input_text += "3"; await self.Yazı(interaction)

    @discord.ui.button(label = "+", style=discord.ButtonStyle.success, row = 0)
    async def Artı(self, button, interaction: discord.Interaction):
        self.input_text += "+"; await self.Yazı(interaction)

    @discord.ui.button(label = "4", style=discord.ButtonStyle.primary, row = 1)
    async def Dört(self, button, interaction: discord.Interaction):
        self.input_text += "4"; await self.Yazı(interaction)

    @discord.ui.button(label = "5", style=discord.ButtonStyle.primary, row = 1)
    async def Beş(self, button, interaction: discord.Interaction):
        self.input_text += "5"; await self.Yazı(interaction)

    @discord.ui.button(label = "6", style=discord.ButtonStyle.primary, row = 1)
    async def Altı(self, button, interaction: discord.Interaction):
        self.input_text += "6"; await self.Yazı(interaction)

    @discord.ui.button(label = "-", style=discord.ButtonStyle.success, row = 1)
    async def Eksi(self, button, interaction: discord.Interaction):
        self.input_text += "-"; await self.Yazı(interaction)

    @discord.ui.button(label = "7", style=discord.ButtonStyle.primary, row = 2)
    async def Yedi(self, button, interaction: discord.Interaction):
        self.input_text += "7"; await self.Yazı(interaction)

    @discord.ui.button(label = "8", style=discord.ButtonStyle.primary, row = 2)
    async def Sekiz(self, button, interaction: discord.Interaction):
        self.input_text += "8"; await self.Yazı(interaction)

    @discord.ui.button(label = "9", style=discord.ButtonStyle.primary, row = 2)
    async def Dokuz(self, button, interaction: discord.Interaction):
        self.input_text += "9"; await self.Yazı(interaction)

    @discord.ui.button(label = "x", style=discord.ButtonStyle.success, row = 2)
    async def Çarpı(self, button, interaction: discord.Interaction):
        self.input_text += "*"; await self.Yazı(interaction)

    @discord.ui.button(label = "Sıfırla", style=discord.ButtonStyle.danger, row = 3)
    async def Sıfırla(self, button, interaction: discord.Interaction):
        self.input_text = ""; await self.Yazı(interaction)

    @discord.ui.button(label = "0", style=discord.ButtonStyle.primary, row = 3)
    async def Sıfır(self, button, interaction: discord.Interaction):
        self.input_text += "0"; await self.Yazı(interaction)

    @discord.ui.button(label = "=", style=discord.ButtonStyle.primary, row = 3)
    async def Eşittir(self, button, interaction: discord.Interaction):
        try:
            self.input_text = str(eval(self.input_text))
        except:
            self.input_text = "Mesajınız Anlaşılamadı."
        await self.Yazı(interaction)

    @discord.ui.button(label = "÷", style=discord.ButtonStyle.success, row = 3)
    async def Bölü(self, button, interaction: discord.Interaction):
        self.input_text += "/"; await self.Yazı(interaction)
