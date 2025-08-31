from discord.ext import commands, tasks
from Mantık import *
import discord
import os
import re

from dotenv import load_dotenv
load_dotenv(override=True)

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

kullanıcı_yanıtları = {}
kullanıcı_soruları = {}
kullanıcı_cevapları = {}

async def Kullanıcıya_Soru_Gönder(channel, user_id):
    soru_görünümü = kullanıcı_soruları[user_id][kullanıcı_yanıtları[user_id]]
    soru = sorular[soru_görünümü]
    görüntü = discord.ui.View()
    for button in soru.Düğmeler():
        görüntü.add_item(button)
    await channel.send(soru.text, view=görüntü)

@bot.event
async def on_ready():
    print(f"Mesajbot Açıldı.")

@bot.event
async def Sorularla_Etkileşim(interaction: discord.Interaction):
    kullanıcı_kimliği = interaction.user.id
    soru_görünümü = kullanıcı_soruları[kullanıcı_kimliği][kullanıcı_yanıtları[kullanıcı_kimliği]]
    soru = sorular[soru_görünümü]
    özel_kimlik = interaction.data["custom_id"]
    seçilen_görünüm = int(özel_kimlik.split("_")[1])
    if kullanıcı_kimliği not in kullanıcı_cevapları:
        kullanıcı_cevapları[kullanıcı_kimliği] = {"Doğru Cevaplar": 0, "Yanlış Cevaplar": 0}
    if seçilen_görünüm == soru.answer_id:
        kullanıcı_cevapları[kullanıcı_kimliği]["Doğru Cevaplar"] += 1
        await interaction.response.send_message("Doğru bildin.", ephemeral=True)
    else:
        kullanıcı_cevapları[kullanıcı_kimliği]["Yanlış Cevaplar"] += 1
        await interaction.response.send_message(
            f"Yanlış bildin. Doğru cevap {soru.secenekler[soru.answer_id]} olacaktı.",
            ephemeral=True
        )
    kullanıcı_yanıtları[kullanıcı_kimliği] += 1
    if kullanıcı_yanıtları[kullanıcı_kimliği] >= len(kullanıcı_soruları[kullanıcı_kimliği]):
        skor = kullanıcı_cevapları[kullanıcı_kimliği]
        await interaction.followup.send(
            f"Sorular bitti.\nSoru Sayısı: {len(kullanıcı_soruları[kullanıcı_kimliği])}\nDoğru Cevaplar: {skor['Doğru Cevaplar']}\nYanlış Cevaplar: {skor['Yanlış Cevaplar']}",
            ephemeral=True
        )
        del kullanıcı_yanıtları[kullanıcı_kimliği]
        del kullanıcı_soruları[kullanıcı_kimliği]
        del kullanıcı_cevapları[kullanıcı_kimliği]
    else:
        await Kullanıcıya_Soru_Gönder(interaction.channel, kullanıcı_kimliği)

@bot.event
async def on_message(message):
    cleaned_content = message.content.lower()
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if re.fullmatch(r"\s*m+\s*e+\s*r+\s*h+\s*a+\s*b+\s*a+\s*", cleaned_content):
        await message.channel.send("Sana da merhaba.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(n+a+s+ı+l+s+ı+n|n+a+s+i+l+s+i+n|i+y+i\s*m+i+s+i+n)\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await message.channel.send("İyiyim, sorduğun için teşekkür ederim.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(a+d+|a+d+ı+n?|a+d+i+n?)\s*(\s*n+e)?\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await message.channel.send("Benim Adım Mesajbot.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(i+s+m+ı+n?|i+s+i+m+)\s*(\s*n+e)?\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await message.channel.send("Benim ismim Mesajbot.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*s+e+n+i+\s*(k+i+m|y+a+p+a+n|y+ı+z+ı+l+m+a+y+a+n|y+ı+z+ı+l+m+a+y+a+n+ı+n)\s*(a+d+ı|a+d+i|i+s+m+i)?\s*(n+e)?\s*\??\s*", cleaned_content, re.IGNORECASE):
        await message.channel.send("Beni Mert NALBANTOĞLU yazılımladı.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*s+\s*a+\s*n+\s*a+\s*\s*g+\s*u+\s*v+\s*e+\s*n+\s*i+\s*b+\s*i+\s*l+\s*i+\s*r+\s*\s*m+\s*i+\s*y+\s*i+\s*m|\s*s+\s*e+n+\s*\s*g+\s*u+\s*v+\s*e+\s*n+\s*i+\s*l+\s*i+\s*r+\s*m+\s*i+\s*n|\s*g+\s*u+\s*v+\s*e+\s*n+\s*i+\s*l+\s*i+\s*r(\s*m+\s*i+\s*n)?", cleaned_content, re.IGNORECASE):
        await message.channel.send("Evet, bana güvenebilirsin.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*s+\s*e+\s*n+\s*\s*n+\s*e+\s*s+\s*i+\s*n\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await message.channel.send("Ben bir yapay zekayım.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*t+\s*e+\s*ş+\s*e+\s*k+\s*ü+\s*r+\s*(l+e+r+|e+d+e+r+i+m+)?\s*(\?*)\s*", cleaned_content):
        await message.channel.send("Rica ederim, her zaman yanındayım. Bir sorun olduğunda sormaktan çekinme.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(p+a+r+o+l+a|s+i+f+r+e|ş+i+f+r+e)(\s*(a+t|b+e+l+i+r+l+e|g+ö+n+d+e+r|y+o+l+l+a))?\s*(\?*)\s*", cleaned_content):
        await message.channel.send(Parola_Gönder(25))
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*e+\s*m+\s*o+\s*j+\s*i+(\s*(a+t|g+ö+n+d+e+r|y+o+l+l+a))?\s*(\?*)\s*", cleaned_content):
        await message.channel.send(Emoji_Gönder())
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    if re.fullmatch(r"\b(hesap(\s*makine(si|s[iı])|)\s*(aç|yap|çalıştır)?|hesapla)\b", cleaned_content, re.IGNORECASE):
        görüntü = Hesap_Makinesi()
        await message.channel.send(view = görüntü)
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"s+o+r+u*r*|s+o*r*|s+o+r+u+\s*s+o+r*|s+o+r+u+l+a*r*|s+o*r+u+l+a*r\s+s+o*r*", cleaned_content, re.IGNORECASE):
        user_id = message.author.id
        if user_id not in kullanıcı_yanıtları:
            kullanıcı_yanıtları[user_id] = 0
            soru_sayisi = random.randint(10, 25)
            order = random.sample(range(len(sorular)), soru_sayisi)
            kullanıcı_soruları[user_id] = order
        await Kullanıcıya_Soru_Gönder(message.channel, user_id)
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.search(r"\s*(?:c+e+v+i+r+|ç+e+v+i+r+|a+r+a+p+ç+a\s*(?:c+e+v+i+r+|y+a+z+)?)(?:\s*[:=]?\s*)?", cleaned_content, re.IGNORECASE):
        text_to_translate = re.sub(r"\s*(?:c+e+v+i+r+|ç+e+v+i+r+|a+r+a+p+ç+a\s*(?:c+e+v+i+r+|y+a+z+)?)(?:\s*[:=]?\s*)?", "", cleaned_content, flags=re.IGNORECASE)
        Metin_Analizi(text_to_translate, message.author.name)
        görüntü = Düğme_Görünümleri(message.author.name)
        await message.channel.send("Mesajı arapçaya çevirmek için lütfen aşağıdaki düğmeye basınız.", view = görüntü)
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

class Düğme_Görünümleri(discord.ui.View):
    def __init__(self, owner):
        super().__init__(timeout=None)
        self.owner = owner

    @discord.ui.button(label="Arapçaya Çevir", style=discord.ButtonStyle.primary)
    async def Arapçaya_Çevirme(self, button: discord.ui.Button, interaction: discord.Interaction):
        obj = Metin_Analizi.memory[self.owner][-1]
        await interaction.response.send_message(obj.translation_ar, ephemeral=True)

bot.run(TOKEN)
