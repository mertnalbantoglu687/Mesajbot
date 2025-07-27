import random

class resim:
    async def get_name(self):
        url = f"https://random-d.uk/api/random{self.resim_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["forms"][0]["name"]
                else:
                    return resim,resim.name
    async def get_image(self):
        url = f"https://random-d.uk/api/random{self.resim_number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data["sprites"]["front_defauld"]
                    return img_url
                return None
    async def info(self):
        return "isim"
