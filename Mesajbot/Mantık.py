from datetime import datetime, timedelta
from collections import defaultdict
import discord
import random
import requests
import calendar
import sqlite3
import asyncio
import base64
import pytz
import time
import json
import os

from dotenv import load_dotenv

load_dotenv()

API_ANAHTARI = os.environ.get("API_ANAHTARI")
GİZLİ_ANAHTAR = os.environ.get("GİZLİ_ANAHTAR")

Oyunlar = {}

RENKLER = ["🟦","🟥","🟨","🟩","🟧"]

def Parola_Gönder(en_az_uzunluk, en_çok_uzunluk):
    karakterler = "é!'^+%½&/?*_-@´`<>AaBbCcÇçDdEeFfGgĞğHhIıİiJjKkLlMmNnOoÖöPpRrSsŞşTtUuÜüVvYyZz1234567890"
    parola_uzunluğu = random.randint(en_az_uzunluk, en_çok_uzunluk)
    parola = "".join(random.choice(karakterler) for _ in range(parola_uzunluğu))
    return "Parola: " + parola

def Emoji_Gönder():
    emoji = "\U0001f642"
    return random.choice(emoji)

class Sorular:
    def __init__(self, text, answer_id, *seçenekler):
        self.text = text
        self.answer_id = answer_id
        self.seçenekler = seçenekler

    def Düğmeler(self):
        düğmeler = []
        for a, seçenek in enumerate(self.seçenekler):
            button = discord.ui.Button(
                label = seçenek,
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
        await interaction.response.edit_message(content = content_to_send, view = self)

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

def Labirent(boyut=11):
    if boyut % 2 == 0:
        boyut += 1

    labirent = [[1]*boyut for _ in range(boyut)]

    def Kaz(x, y):
        yönler = [(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(yönler)
        labirent[y][x] = 0
        for dx, dy in yönler:
            nx, ny = x+dx, y+dy
            if 1 <= nx < boyut-1 and 1 <= ny < boyut-1 and labirent[ny][nx] == 1:
                labirent[y+dy//2][x+dx//2] = 0
                Kaz(nx, ny)

    Kaz(1, 1)
    giriş_y = random.randrange(1, boyut-1, 2)
    labirent[giriş_y][0] = 0
    labirent[giriş_y][1] = 0
    giriş = (0, giriş_y)
    çıkış_y = random.randrange(1, boyut-1, 2)
    labirent[çıkış_y][boyut-1] = 0
    labirent[çıkış_y][boyut-2] = 0
    çıkış = (boyut-1, çıkış_y)

    return labirent, giriş, çıkış

def Harita_Çiz(oyun):
    çizim = ""
    for y, row in enumerate(oyun["labirent"]):
        for x, val in enumerate(row):
            if (x, y) == (oyun["x"], oyun["y"]):
                çizim += "🔴"
            elif val == 1:
                çizim += "⬛"
            else:
                çizim += "🟩"
        çizim += "\n"
    return çizim

def Sırayı_Güncelle(renk_sayısı, uzunluk):
    return [random.randint(0, renk_sayısı - 1) for _ in range(uzunluk)]

async def Geri_Sayım(message, oyun):
    harita = Harita_Çiz(oyun)

    for a in ["3️⃣", "2️⃣", "1️⃣"]:
        await message.edit(content = f"{harita}\nHazır ol: {a}",view = None)
        await asyncio.sleep(1)

async def Sırayı_Göster(message, oyun):
    harita = Harita_Çiz(oyun)

    await Geri_Sayım(message, oyun)

    for a in oyun["sıra"]:
        emoji = oyun["renkler"][a]
        await message.edit(
            content = f"{harita}\nSıralamayı ezberle: {emoji}",
            view = None
        )
        await asyncio.sleep(1)

        await message.edit(content = f"{harita}\n...", view = None)
        await asyncio.sleep(0.3)

class Renk_Düğmeleri(discord.ui.Button):
    def __init__(self, index, emoji, view):
        super().__init__(
            style=discord.ButtonStyle.secondary,emoji=emoji)
        self.index = index
        self.view_ref = view

    async def callback(self, interaction):
        await self.view_ref.Kontrol(interaction, self.index)

class Yön_Düğmeleri(discord.ui.Button):
    def __init__(self, emoji, dx, dy, kullanıcı_kimliği):
        super().__init__(
            style=discord.ButtonStyle.secondary,emoji=emoji)
        self.dx = dx
        self.dy = dy
        self.kullanıcı_kimliği = kullanıcı_kimliği

    async def callback(self, interaction):
        oyun = Oyunlar[self.kullanıcı_kimliği]

        if not oyun["hareket_hakkı"]:
            await interaction.response.defer()
            return

        nx = oyun["x"] + self.dx
        ny = oyun["y"] + self.dy

        if oyun["labirent"][ny][nx] == 0:
            oyun["x"], oyun["y"] = nx, ny

        if (oyun["x"], oyun["y"]) == oyun["çıkış"]:
            await interaction.response.edit_message(content = f"Kazandın.\n\nPuan: {oyun['puan']}\nDoğru Sayısı: {oyun['doğru']}\nYanlış Sayısı: {oyun['yanlış']}",view = None)
            return

        oyun["hareket_hakkı"] = False

        await interaction.response.edit_message(content = Harita_Çiz(oyun),view = None)
        await asyncio.sleep(0.8)
        await Sırayı_Göster(interaction.message, oyun)
        await interaction.message.edit(
            content = Harita_Çiz(oyun),
            view = Renk_Girme_Düğmeleri(self.kullanıcı_kimliği))

class Düğmeler(discord.ui.View):
    def __init__(self, kullanıcı_kimliği):
        super().__init__(timeout=30)
        oyun = Oyunlar[kullanıcı_kimliği]
        x, y = oyun["x"], oyun["y"]
        l = oyun["labirent"]

        if y > 0 and l[y-1][x] == 0:
            self.add_item(Yön_Düğmeleri("⬆️",0,-1,kullanıcı_kimliği))
        if y < len(l)-1 and l[y+1][x] == 0:
            self.add_item(Yön_Düğmeleri("⬇️",0,1,kullanıcı_kimliği))
        if x > 0 and l[y][x-1] == 0:
            self.add_item(Yön_Düğmeleri("⬅️",-1,0,kullanıcı_kimliği))
        if x < len(l)-1 and l[y][x+1] == 0:
            self.add_item(Yön_Düğmeleri("➡️",1,0,kullanıcı_kimliği))

class Renk_Girme_Düğmeleri(discord.ui.View):
    def __init__(self, kullanıcı_kimliği):
        super().__init__(timeout=60)
        self.kullanıcı_kimliği = kullanıcı_kimliği
        oyun = Oyunlar[kullanıcı_kimliği]

        for a in range(oyun["renk_sayısı"]):
            self.add_item(Renk_Düğmeleri(a, oyun["renkler"][a], self))

    async def Kontrol(self, interaction, secim):
        await interaction.response.defer()
        oyun = Oyunlar[self.kullanıcı_kimliği]

        def Bilgi_Yazısı(oyun, baslik):
            return (f"{baslik}\n\n"f"Doğru Sayısı: {oyun['doğru']}\n"f"Yanlış Sayısı: {oyun['yanlış']}\n"f"Puan: {oyun['puan']}")

        oyun["giriş"].append(secim)

        if oyun["giriş"] != oyun["sıra"][:len(oyun["giriş"])]:
            oyun["yanlış"] += 1
            oyun["giriş"] = []

            await interaction.message.edit(content = Harita_Çiz(oyun) + "\n" + Bilgi_Yazısı(oyun, "Sıralamayı yanlış girdin."),view = None)
            await asyncio.sleep(3)
            await Sırayı_Göster(interaction.message, oyun)
            await interaction.message.edit(content = Harita_Çiz(oyun),view = Renk_Girme_Düğmeleri(self.kullanıcı_kimliği))
            return

        if len(oyun["giriş"]) == len(oyun["sıra"]):
            oyun["puan"] += 1
            oyun["doğru"] += 1
            oyun["giriş"] = []

            if oyun["doğru"] % 4 == 0 and oyun["renk_sayısı"] < 5:
                oyun["renk_sayısı"] += 1

            oyun["renkler"] = random.sample(RENKLER, oyun["renk_sayısı"])
            oyun["sıra"] = Sırayı_Güncelle(oyun["renk_sayısı"],len(oyun["sıra"]) + 1)
            await interaction.message.edit(content = Harita_Çiz(oyun) + "\n" +Bilgi_Yazısı(oyun, "Sıralamayı doğru girdin."),view = None)
            await asyncio.sleep(3)
            oyun["hareket_hakkı"] = True
            await interaction.message.edit(content = Harita_Çiz(oyun) + "\nGitmek istediğin yönü seç:", view=Düğmeler(self.kullanıcı_kimliği))
