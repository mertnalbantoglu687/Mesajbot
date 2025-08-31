import discord

import random

import requests

from discord import ui, ButtonStyle

from translate import Translator

from collections import defaultdict

from translate import Translator

from collections import defaultdict

def Parola_Gönder(pass_length):
    karakterler = "é!'£^#+$%½&/=?\*_-@¨¨~~æß´`,;<>.:AaBbCcÇçDdEeFfGgĞğHhIıİiJjKkLlMmNnOoÖöPpQqRrSsŞşTtUuÜüVvWwXxYyZz1234567890"
    parola = ""
    for a in range(pass_length):
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
        buttons = []
        for i, secenek in enumerate(self.secenekler):
            button = discord.ui.Button(
                label=secenek,
                style=discord.ButtonStyle.primary,
                custom_id=f"answer_{i}"
            )
            buttons.append(button)
        return buttons

sorular = [
    # Fen Bilimleri İle İlgili Sorular
    Sorular("Dünya'nın uydusu nedir?", 2, "Jüpiter", "Mars", "Ay"),
    Sorular("Hangi gezegen halkalara sahiptir?", 0, "Satürn", "Mars", "Venüs"),
    Sorular("Dünya'nın güneş etrafında dönme süresi nedir?", 0, "365 Gün", "24 Saat", "30 Gün"),
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

class Metin_Analizi:
    memory = defaultdict(list)

    def __init__(self, text, owner):
        Metin_Analizi.memory[owner].append(self)
        self.text = text
        self.translation_ar = self.__translate(self.text, "tr", "ar")
        self.response = "Mesajınız anlaşılamadı."

    def __translate(self, text, from_lang, to_lang):
        try:
            translator = Translator(from_lang=from_lang, to_lang=to_lang)
            return translator.translate(text)
        except:

            return "Mesajınız anlaşılamadı."
