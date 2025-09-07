from discord.ext import commands, tasks
from dotenv import load_dotenv
from Mantık import *
import discord
import os
import re

load_dotenv(override = True)

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix = "", intents = intents)

kullanıcı_yanıtları = {}
kullanıcı_soruları = {}
kullanıcı_cevapları = {}

async def Kullanıcıya_Soru_Gönder(channel, user_id):
    soru_görünümü = kullanıcı_soruları[user_id][kullanıcı_yanıtları[user_id]]
    soru = sorular[soru_görünümü]
    görüntü = discord.ui.View()
    for button in soru.Düğmeler():
        görüntü.add_item(button)
    await channel.send(soru.text, view = görüntü)

@bot.event
async def on_ready():
    print("Mesajbot Açıldı.")

async def Beğenme(message, response_text):
    await message.channel.send(response_text)
    if random.randint(1, 2) == 1:
        await message.add_reaction("👍🏻")

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
        await Beğenme(message,"Sana da merhaba.")

    elif re.fullmatch(r"\s*(n+a+s+ı+l+s+ı+n|n+a+s+i+l+s+i+n|i+y+i\s*m+i+s+i+n)\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await Beğenme(message,"İyiyim, sorduğun için teşekkür ederim.")

    elif re.fullmatch(r"\s*(a+d+|a+d+ı+n?|a+d+i+n?)\s*(\s*n+e)?\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await Beğenme(message,"Benim Adım Mesajbot.")

    elif re.fullmatch(r"\s*(i+s+m+ı+n?|i+s+i+m+)\s*(\s*n+e)?\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await Beğenme(message,"Benim ismim Mesajbot.")

    elif re.fullmatch(r"\s*s+e+n+i+\s*(k+i+m|y+a+p+a+n|y+ı+z+ı+l+m+a+y+a+n|y+ı+z+ı+l+m+a+y+a+n+ı+n)\s*(a+d+ı|a+d+i|i+s+m+i)?\s*(n+e)?\s*\??\s*", cleaned_content, re.IGNORECASE):
        await Beğenme(message,"Beni Mert NALBANTOĞLU yazılımladı.")

    elif re.fullmatch(r"\s*s+\s*e+\s*n+\s*\s*n+\s*e+\s*s+\s*i+\s*n\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        await Beğenme(message,"Ben bir yapay zekayım.")

    elif re.fullmatch(r"\s*t+\s*e+\s*ş+\s*e+\s*k+\s*ü+\s*r+\s*(l+e+r+|e+d+e+r+i+m+)?\s*(\?*)\s*", cleaned_content):
        await Beğenme(message,"Rica ederim, her zaman yanındayım. Bir sorun olduğunda sormaktan çekinme.")

    elif re.fullmatch(r"\s*(p+a+r+o+l+a|s+i+f+r+e|ş+i+f+r+e)(\s*(a+t|b+e+l+i+r+l+e|g+ö+n+d+e+r|y+o+l+l+a))?\s*(\?*)\s*", cleaned_content):
        await Beğenme(message,Parola_Gönder(25))

    elif re.fullmatch(r"\s*e+\s*m+\s*o+\s*j+\s*i+(\s*(a+t|g+ö+n+d+e+r|y+o+l+l+a))?\s*(\?*)\s*", cleaned_content):
        await Beğenme(message,Emoji_Gönder())

    elif re.fullmatch(r"(t+a+r+i+h|t+a+r+i+h+i|t+a+r+i+h\s*g+ö+s+t+e+r|t+a+r+i+h\s*g+ö+s+t+e+r+i|t+a+r+i+h\s*g+o+s+t+e+r|t+a+r+i+h\s*g+o+s+t+e+r+i|t+a+r+i+h\s*n+e|t+a+r+i+h+i\s*s+ö+y+l+e|t+a+r+i+h+i\s*s+o+y+l+e|t+a+r+i+h\s*s+ö+y+l+e|t+a+r+i+h\s*s+o+y+l+e|hangi\s+t+a+r+i+h+t+e+y+i+z)\s*\?*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        gün = f"{şimdi.day:02}"
        ay = f"{şimdi.month:02}"
        yıl = şimdi.year
        await Beğenme(message,f"Tarih: {gün}.{ay}.{yıl}")

    elif re.fullmatch(r"\s*(hangi\s+mevsimdeyiz|mevsimimiz\s*ne|mevsim\s*ne|mevsim|mevsimimiz|mevsimi\s*(?:söyle|soyle)|mevsim\s*(?:söyle|soyle)|mevsimlerden\s*hangisindeyiz|mevsimlerden\s*ne|mevsimlerden\s*hangisindeyiz|mevsimlerden\s*hangisi|bu\s+mevsim\s*ne)\s*\?*\s*",cleaned_content, re.IGNORECASE):
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

        await Beğenme(message,f"Mevsim: {mevsim}")

    elif re.fullmatch(r"(kaçıncı\s+mevsimdeyiz|mevsimimiz\s+kaçıncı\s+mevsim|bu\s+mevsim\s+kaçıncı\s+mevsim|mevsimlerden\s+kaçıncı\s+mevsimdeyiz|mevsimlerden\s+kaçıncıdayız)\s*\?*", cleaned_content, re.IGNORECASE):
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

        await Beğenme(message,f"{mevsim_numarası}. mevsimdeyiz.")

    elif re.fullmatch(r"\s*(kaçıncı\s+yıldayız|kaç\s+yıl(?:ındayız|ındayız\s*söyle|ındayız\s*soyle)?|hangi\s+yıldayız|yılımız\s*ne|yıl(?:ı|ı)?\s*(?:söyle|soyle)?|yılımızı\s*(?:söyle|soyle)?|yıllardan\s+ne|yıllardan\s+hangi\s+yıldayız|yıllardan\s+kaçıncıdayız|yıllardan\s+kaçıncı\s+yıldayız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        yıl = şimdi.year
        await Beğenme(message,f"Yıl: {yıl}")

    elif re.fullmatch(r"\s*(kaçıncı\s+aydayız|kaçıncı\s+aydayız\s*(?:söyle|soyle)?|aylardan\s+kaçıncı\s+aydayız|aylardan\s+kaçıncıdayız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay = şimdi.month
        await Beğenme(message,f"{ay}. aydayız.")

    elif re.fullmatch(r"\s*(?:bu\s+)?(bu\s+haftanın\s+kaçıncı\s+gün(ü)?|bugün\s+haftanın\s+kaçıncı\s+günü|haftanın\s+kaçıncı\s+gün(ü)?n(d)eyiz|haftanın\s+günlerinden\s+kaçıncıdayız|haftanın\s+günlerinden\s+kaçıncı\s+gündeyiz|bu\s+haftanın\s+kaçıncı\s+günündeyiz)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        gün = şimdi.isoweekday()
        await Beğenme(message,f"Haftanın {gün}. günündeyiz.")

    elif re.fullmatch(r"\s*(?:bu\s+)?(bugün\s+)?(ay(ın)?|ayın)\s+kaçıncı\s+gün(ü)?(ndeyiz)?|ayın\s+günlerinden\s+kaçıncıdayız|ayın\s+günlerinden\s+kaçıncı\s+gün(ü)?d?eyiz\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        gün = şimdi.day
        await Beğenme(message,f"Ayın {gün}. günündeyiz.")

    elif re.fullmatch(r"\s*(?:bu\s+)?ay\s+kaç\s+gün( olacak| sürecek)?|bulunduğumuz\s+ay\s+kaç\s+gün|olduğumuz\s+ay\s+kaç\s+gün|içinde\s+bulunduğumuz\s+ay\s+kaç\s+gün|içerisinde\s+bulunduğumuz\s+ay\s+kaç\s+gün|bu\s+ayın\s+günleri\s+kaç\s+tane\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        gün = (datetime(şimdi.year, şimdi.month % 12 + 1, 1) - timedelta(days=1)).day
        await Beğenme(message,f"Bu ay {gün} gün.")

    elif re.fullmatch(r"\s*(?:bu\s+)?(bugün\s+)?(ay(ın)?|ayın)\s+kaçıncı\s+hafta(sı)?(ndayız)?|ayın\s+haftalarından\s+kaçıncıdayız|ayın\s+haftalarından\s+kaçıncı\s+hafta(sı)?d?ndayız\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ayın_ilk_günü = datetime(şimdi.year, şimdi.month, 1, tzinfo=pytz.timezone("Europe/Istanbul"))
        hafta = ((şimdi - ayın_ilk_günü).days // 7) + 1
        await Beğenme(message,f"Bu ayın {hafta}. haftasındayız.")

    elif re.fullmatch(r"\s*(bugün\s+)?(yıl(ın)?|bu\s+yıl|yılın\s+günlerinden|yılın\s+günlerinden\s+kaçıncı)\s+kaçıncı\s+gün(ü)?(ndeyiz)?\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        gün = şimdi.timetuple().tm_yday
        await Beğenme(message,f"Yılın {gün}. günündeyiz.")

    elif re.fullmatch(r"\s*(bu\s+yılın\s+kaçıncı\s+haftasındayız|yılın\s+kaçıncı\s+haftasındayız|yılın\s+haftalarından\s+kaçıncıdayız|yılın\s+haftalarından\s+kaçıncı\s+haftasındayız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        hafta = şimdi.isocalendar()[1]
        await Beğenme(message,f"Yılın {hafta}. haftasındayız.")

    elif re.fullmatch(r"\s*(bu\s+yılın\s+kaçıncı\s+ayındayız|yılın\s+kaçıncı\s+ayındayız|yılın\s+aylarından\s+kaçıncıdayız|yılın\s+aylarından\s+kaçıncı\s+aydayız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay = şimdi.month
        await Beğenme(message,f"Yılın {ay}. ayındayız.")

    elif re.fullmatch(r"\s*(yılın\s+mevsimlerinden\s+kaçıncıdayız|mevsimlerden\s+kaçıncıdayız|yılın\s+mevsimlerinden\s+kaçıncı\s+mevsimdeyiz|yılın\s+mevsimlerinden\s+kaçıncı\s+mevsimindeyiz|mevsimlerden\s+kaçıncı\s+mevsimdeyiz|bu\s+yılın\s+kaçıncı\s+mevsimindeyiz)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay_numarası = şimdi.month

        if ay_numarası in [3, 4, 5]:
            mevsim = 1
        elif ay_numarası in [6, 7, 8]:
            mevsim = 2
        elif ay_numarası in [9, 10, 11]:
            mevsim = 3
        elif ay_numarası in [12, 1, 2]:
            mevsim = 4

        await Beğenme(message,f"Yılın {mevsim}. mevsimindeyiz.")

    elif re.fullmatch(r"\s*(?:bu\s+)?(bugün\s+mevsimin\s+kaçıncı\s+günü|mevsimin\s+kaçıncı\s+günü|mevsimin\s+kaçıncı\s+günündeyiz|bu\s+mevsimin\s+kaçıncı\s+günündeyiz|bu\s+mevsimin\s+günlerinden\s+kaçıncıdayız|mevsimin\s+günlerinden\s+kaçıncı\s+gündeyiz)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay = şimdi.month
        gün = şimdi.day

        if ay in [3, 4, 5]:
            mevsim_numarası = 1
            mevsim_ayları = [3, 4, 5]
        elif ay in [6, 7, 8]:
            mevsim_numarası = 2
            mevsim_ayları = [6, 7, 8]
        elif ay in [9, 10, 11]:
            mevsim_numarası = 3
            mevsim_ayları = [9, 10, 11]
        elif ay in [12, 1, 2]:
            mevsim_numarası = 4
            mevsim_ayları = [12, 1, 2]

        gün = (datetime(şimdi.year, ay, gün) - datetime(şimdi.year, mevsim_ayları[0], 1)).days + 1

        await Beğenme(message,f"Bu mevsimin {gün}. günündeyiz.")

    elif re.fullmatch(r"\s*(?:bu\s+)?(mevsimin\s+kaçıncı\s+haftasındayız|mevsimin\s+haftalarından\s+kaçıncıdayız|mevsimin\s+haftalarından\s+kaçıncı\s+haftadayız|mevsimin\s+haftalarından\s+kaçıncı\s+haftasındayız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay_numarası = şimdi.month

        if ay_numarası in [12, 1, 2]:
            mevsim = "Kış"
            başlangıç_ay = 12
        elif ay_numarası in [3, 4, 5]:
            mevsim = "İlkbahar"
            başlangıç_ay = 3
        elif ay_numarası in [6, 7, 8]:
            mevsim = "Yaz"
            başlangıç_ay = 6
        elif ay_numarası in [9, 10, 11]:
            mevsim = "Sonbahar"
            başlangıç_ay = 9

        mevsim_başlangıcı = datetime(şimdi.year, başlangıç_ay, 1, tzinfo=pytz.timezone("Europe/Istanbul"))
        hafta = ((şimdi - mevsim_başlangıcı).days // 7) + 1

        await Beğenme(message,f"Bu mevsiminin {hafta}. haftasındayız.")

    elif re.fullmatch(r"\s*(?:bu\s+)?(mevsimin\s+haftalarından\s+kaçıncıdayız|mevsimin\s+haftalarından\s+kaçıncı\s+haftadayız|mevsimin\s+haftalarından\s+kaçıncı\s+haftasındayız|mevsimin\s+kaçıncı\s+haftasındayız|bu\s+mevsimin\s+kaçıncı\s+haftasındayız|mevsimin\s+kaçıncı\s+haftadayız|bu\s+mevsimin\s+kaçıncı\s+haftadayız|mevsimin\s+aylarından\s+kaçıncıdayız|mevsimin\s+aylarından\s+kaçıncı\s+aydayız|mevsimin\s+aylarından\s+kaçıncı\s+ayındayız|mevsimin\s+kaçıncı\s+ayındayız|bu\s+mevsimin\s+kaçıncı\s+ayındayız|mevsimin\s+kaçıncı\s+aydayız|bu\s+mevsimin\s+kaçıncı\s+aydayız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        ay_numarası = şimdi.month

        if ay_numarası in [12, 1, 2]:
            mevsim = "Kış"
            ay = (ay_numarası - 12 + 1) if ay_numarası == 12 else (ay_numarası)
        elif ay_numarası in [3, 4, 5]:
            mevsim = "İlkbahar"
            ay = ay_numarası - 3 + 1
        elif ay_numarası in [6, 7, 8]:
            mevsim = "Yaz"
            ay = ay_numarası - 6 + 1
        elif ay_numarası in [9, 10, 11]:
            mevsim = "Sonbahar"
            ay = ay_numarası - 9 + 1

        await Beğenme(message,f"Bu mevsiminin {ay}. ayındayız.")

    elif re.fullmatch(r"\s*(ne\s+ayındayız|hangi\s+aydayız|ayımız\s*ne|ay(?:ı)?\s*(?:söyle|soyle)?|ayımızı\s*(?:söyle|soyle)?|aylardan\s+ne|aylardan\s+hangisindeyiz|aylardan\s+hangi\s+aydaız)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
                 "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        ay = aylar[şimdi.month - 1]
        await Beğenme(message,f"Ay: {ay}")

    elif re.fullmatch(r"\s*(g+ü+n|g+ü+n+ü\s*s+ö+y+l+e|b+u+g+ü+n+ü\s*s+ö+y+l+e|g+ü+n+ü\s*s+o+y+l+e|b+u+g+ü+n+ü\s*s+o+y+l+e|g+ü+n\s*n+e|g+ü+n+l+e+r+d+e+n\s*n+e|b+u+g+ü+n\s+g+ü+n+l+e+r+d+e+n\s+n+e|b+u+g+ü+n\s+h+a+n+g+i\s+g+ü+n|b+u+g+ü+n\s+g+ü+n+l+e+r+d+e+n\s+h+a+n+g+i+s+i|g+ü+n+l+e+r+d+e+n\s+h+a+n+g+i+s+i|g+ü+n+l+e+r+d+e+n\s+h+a+n+g+i\s+g+ü+n|g+ü+n+l+e+r+d+e+n\s+n+e)\s*\?*\s*", cleaned_content, re.IGNORECASE):
        şimdi = datetime.now(pytz.timezone("Europe/Istanbul"))
        günler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        gün = günler[şimdi.weekday()]
        await Beğenme(message,f"Bugün: {gün}")

    elif re.fullmatch(r"\s*s+\s*a+\s*a+\s*t+\s*(?:i|)\s*(?:k+a+ç+|k+a+ç+t+ı+r*|s+ö+l+e|s+o+l+e|o+l+d+u+|g+ö+s+t+e+r|g+o+s+t+e+r)?\s*(\?*)\s*", cleaned_content, re.IGNORECASE):
        timezone = pytz.timezone("Europe/Istanbul")
        şimdi = datetime.now(timezone)
        await Beğenme(message,f"Saat: {şimdi.strftime('%H:%M:%S')}")

    elif re.fullmatch(r"\s*[\d.,\+\-\*/xX:÷\s]+=?\?*\s*", cleaned_content):
        expression = re.sub(r"[=?]+", "", cleaned_content).strip()
        expression = re.sub(r"[,.]+", ".", expression)
        expression = expression.replace("x", "*").replace("X", "*")
        expression = expression.replace(":", "/").replace("÷", "/")
        expression = re.sub(r"(\+)+", "+", expression)
        expression = re.sub(r"(-)+", "-", expression)
        expression = re.sub(r"(\*)+", "*", expression)
        expression = re.sub(r"(/)+", "/", expression)
        sonuç = eval(expression)

        if isinstance(sonuç, float) and sonuç.is_integer():
            sonuç = int(sonuç)
    
        await Beğenme(message,f"Sonuç: {sonuç}")

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

    elif re.search(r"\s*(?:c+e+v+i+r+|ç+e+v+i+r+|a+r+a+p+ç+a\s*(?:c+e+v+i+r+|y+a+z+)?)(?:\s*[:=]?\s*)?", cleaned_content, re.IGNORECASE):
        text_to_translate = re.sub(r"\s*(?:c+e+v+i+r+|ç+e+v+i+r+|a+r+a+p+ç+a\s*(?:c+e+v+i+r+|y+a+z+)?)(?:\s*[:=]?\s*)?", "", cleaned_content, flags=re.IGNORECASE)
        Metin_Analizi(text_to_translate, message.author.name)
        görüntü = Düğme_Görünümleri(message.author.name)
        await message.channel.send("Mesajı arapçaya çevirmek için lütfen aşağıdaki düğmeye basınız.", view=görüntü)
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
