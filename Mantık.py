import discord

import requests

import random

def Parola(pass_length):
    karakterler = "é!'£^#+$%½&/=?\*_-@¨¨~~æß´`,;<>.:AaBbCcÇçDdEeFfGgĞğHhIıİiJjKkLlMmNnOoÖöPpQqRrSsŞşTtUuÜüVvWwXxYyZz1234567890"
    sifre = ""
    for a in range(pass_length):
        sifre += random.choice(karakterler)
    return sifre

def Surat():
    emoji = "\U0001f642"
    return random.choice(emoji)

def Oyun():
    secim = ["https://hub.kodland.org/en/project/289819","https://hub.kodland.org/en/project/308651","https://hub.kodland.org/en/project/296170"]
    return random.choice(secim)

def Ördek():    
    url = "https://random-d.uk/api/random"
    res = requests.get(url)
    data = res.json()
    return data["url"]

def Köpek():    
    url = "https://random.dog/woof.json"
    res = requests.get(url)
    data = res.json()
    return data["url"]