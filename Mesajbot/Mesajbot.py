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
    print("Mesajbot Açıldı.")

@bot.event
async def on_interaction(interaction: discord.Interaction):
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

    elif re.fullmatch(r"(t+a+r+i+h|t+a+r+i+h+i|t+a+r+i+h\s*g+ö+s+t+e+r|t+a+r+i+h\s*g+ö+s+t+e+r+i|t+a+r+i+h\s*g+o+s+t+e+r|t+a+r+i+h\s*g+o+s+t+e+r+i|t+a+r+i+h\s*n+e|t+a+r+i+h+i\s*s+ö+y+l+e|t+a+r+i+h+i\s*s+o+y+l+e|t+a+r+i+h\s*s+ö+y+l+e|t+a+r+i+h\s*s+o+y+l+e|hangi\s+t+a+r+i+h+t+e+y+i+z)\s*\?*", cleaned_content):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        gün = f"{şimdi.day:02}"
        ay = f"{şimdi.month:02}"
        yıl = şimdi.year
        await message.channel.send(f"Tarih: {gün}.{ay}.{yıl}")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(hangi\s+m+e+v+s+i+m+d+e+y+i+z|m+e+v+s+i+m+i+m+i+z\s*n+e|m+e+v+s+i+m\s*n+e|m+e+v+s+i+m|m+e+v+s+i+m+i+m+i+z|m+e+v+s+i+m+i\s+s+ö+y+l+e|m+e+v+s+i+m+i\s+s+o+y+l+e|m+e+v+s+i+m\s+s+ö+y+l+e|m+e+v+s+i+m\s+s+o+y+l+e)\s*\?*\s*",cleaned_content,re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay_numarası = şimdi.month

        if ay_numarası in [3, 4, 5]:
            mevsim = "İlkbahar"
        elif ay_numarası in [6, 7, 8]:
            mevsim = "Yaz"
        elif ay_numarası in [9, 10, 11]:
            mevsim = "Sonbahar"
        elif ay_numarası in [12, 1, 2]:
            mevsim = "Kış"
        await message.channel.send(f"Mevsim: {mevsim}")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.search(r"(kaçıncı\s+mevsimdeyiz|mevsimimiz\s+kaçıncı\s+mevsim|bu\s+mevsim\s+kaçıncı\s+mevsim)\s*\?*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay_numarası = şimdi.month

        if ay_numarası in [3, 4, 5]:
            mevsim_numarası = 1
        elif ay_numarası in [6, 7, 8]:
            mevsim_numarası = 2
        elif ay_numarası in [9, 10, 11]:
            mevsim_numarası = 3
        elif ay_numarası in [12, 1, 2]:
            mevsim_numarası = 4

        await message.channel.send(f"{mevsim_numarası}. mevsimdeyiz.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(kaçıncı\s+yıldayız|kaç\s+yıl(?:ındayız|ındayız\s*söyle|ındayız\s*soyle)?|hangi\s+yıldayız|yılımız\s*ne|yıl(?:ı|ı)?\s*(?:söyle|soyle)?|yılımızı\s*(?:söyle|soyle)?)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        await message.channel.send(f"Yıl: {şimdi.year}")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(kaçıncı\s+aydayız|kaçıncı\s+aydayız\s*(?:söyle|soyle)?)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        await message.channel.send(f"{şimdi.month}. aydayız.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(bu\s+haftanın\s+kaçıncı\s+gün(ü)?|bugün\s+haftanın\s+kaçıncı\s+günü|haftanın\s+kaçıncı\s+gün(ü)?n(d)eyiz)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        haftanin_gunu = şimdi.isoweekday()
        await message.channel.send(f"Haftanın {haftanin_gunu}. günündeyiz.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(bugün\s+)?(ay(ın)?|bu\s+ayın)\s+kaçıncı\s+gün(ü)?(ndeyiz)?\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ayın_günü = şimdi.day
        await message.channel.send(f"Ayın {ayın_günü}. günündeyiz.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(bu\s+ay\s+kaç\s+gün( olacak| sürecek)?|buay\s+kaç\s+gün( olacak| sürecek)?|bu\s+ay\s+kaç\s+gün|bulunduğumuz\s+ay\s+kaç\s+gün|olduğumuz\s+ay\s+kaç\s+gün|içinde\s+bulunduğumuz\s+ay\s+kaç\s+gün|içerisinde\s+bulunduğumuz\s+ay\s+kaç\s+gün)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ayın_günü_sayısı = (datetime(şimdi.year, şimdi.month % 12 + 1, 1) - timedelta(days=1)).day
        await message.channel.send(f"Bu ay {ayın_günü_sayısı} gün.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(bugün\s+)?(yıl(ın)?|bu\s+yıl)\s+kaçıncı\s+gün(ü)?(ndeyiz)?\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        yılın_günü = şimdi.timetuple().tm_yday
        await message.channel.send(f"Yılın {yılın_günü}. günündeyiz.")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(ne\s+ayındayız|hangi\s+aydayız|ayımız\s*ne|ay(?:ı)?\s*(?:söyle|soyle)?|ayımızı\s*(?:söyle|soyle)?)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        ay = aylar[şimdi.month - 1]
        await message.channel.send(f"Ay: {ay}")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(g+ü+n|g+ü+n+ü\s*s+ö+y+l+e|b+u+g+ü+n+ü\s*s+ö+y+l+e|g+ü+n+ü\s*s+o+y+l+e|b+u+g+ü+n+ü\s*s+o+y+l+e|g+ü+n\s*n+e|g+ü+n+l+e+r+d+e+n\s*n+e|b+u+g+ü+n\s+g+ü+n+l+e+r+d+e+n\s+n+e|b+u+g+ü+n\s+h+a+n+g+i\s+g+ü+n|b+u+g+ü+n\s+g+ü+n+l+e+r+d+e+n\s+h+a+n+g+i+s+i)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        haftanın_günleri = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        bugün = haftanın_günleri[şimdi.weekday()]
        await message.channel.send(f"Bugün: {bugün}")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*s+\s*a+\s*a+\s*t+\s*(?:i|)\s*(?:k+a+ç+|k+a+ç+t+ı+r*|s+ö+l+e|s+o+l+e|o+l+d+u+|g+ö+s+t+e+r|g+o+s+t+e+r)?\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        timezone = pytz.timezone("Europe/Istanbul")
        şimdi = datetime.now(timezone)
        await message.channel.send(f"Saat: {şimdi.strftime('%H:%M:%S')}")
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\bhesap\b|\bhesap\s*makine(si)?\b", cleaned_content, re.IGNORECASE):
        görüntü = Hesap_Makinesi()
        await message.channel.send(view=görüntü)
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"s+o+r+u*r*|s+o*r*|s+o+r+u+\s*s+o+r*|s+o+r+u+l+a*r*|s+o*r+u+l+a*r\s+s+o*r*", cleaned_content, re.IGNORECASE):
        user_id = message.author.id
        if user_id not in kullanıcı_yanıtları:
            kullanıcı_yanıtları[user_id] = 0
            soru_sayisi = random.randint(10, 25)
            sorulacak_soru = random.sample(range(len(sorular)), soru_sayisi)
            kullanıcı_soruları[user_id] = sorulacak_soru
        await Kullanıcıya_Soru_Gönder(message.channel, user_id)
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")

    elif re.fullmatch(r"\s*(?:c+e+v+i+r+|ç+e+v+i+r+|a+r+a+p+ç+a\s*(?:c+e+v+i+r+|y+a+z+)?)(?:\s*[:=]?\s*)?", cleaned_content, re.IGNORECASE):
        text_to_translate = re.sub(r"\s*(?:c+e+v+i+r+|ç+e+v+i+r+|a+r+a+p+ç+a\s*(?:c+e+v+i+r+|y+a+z+)?)(?:\s*[:=]?\s*)?", "", cleaned_content, flags=re.IGNORECASE)
        Metin_Analizi(text_to_translate, message.author.name)
        görüntü = Düğme_Görünümleri(message.author.name)
        await message.channel.send("Mesajı arapçaya çevirmek için lütfen aşağıdaki düğmeye basınız.", view = görüntü)
        if random.randint(1, 2) == 1:
            await message.add_reaction("👍🏻")
    else:
        await message.channel.send("Mesajınız anlaşılamadı.")

class Düğme_Görünümleri(discord.ui.View):
    def __init__(self, owner):
        super().__init__(timeout=None)
        self.owner = owner

    @discord.ui.button(label="Arapçaya Çevir", style=discord.ButtonStyle.primary)
    async def Arapçaya_Çevirme(self, button: discord.ui.Button, interaction: discord.Interaction):
        obj = Metin_Analizi.memory[self.owner][-1]
        await interaction.response.send_message(obj.translation_ar, ephemeral=True)

bot.run(TOKEN)
