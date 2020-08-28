import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class poi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkstatus.start()
        except Exception as ex:
            print(ex)
            self.checkstatus.stop()
            self.checkstatus.start()

    @tasks.loop(minutes=5)
    async def checkstatus(self):
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(
                await (await aiofiles.open('Cache/poi.json', mode='r')).read())
            async with aiohttp.ClientSession() as cs:
                parameter = {"Authorization": "2fce9bf4-dcb28a26-d7e48ccf-a12cccee"}
                async with cs.get(
                        'https://fortniteapi.io/game/poi?lang=en', headers=parameter) as data:
                    if data.status != 200:
                        return
                    try:
                        new = await data.json()
                    except:
                        return
        except Exception as ex:
            print(ex)
            return
        if new is None:
            return print("LOL")
        if Cached is None:
            return print("LOL 3")
        if Cached["list"] != new["list"]:
            await (await aiofiles.open('Cache/poi.json', mode='w+')).write(
                json.dumps(new, indent=2))
            for i in new["list"]:
                if i not in Cached["list"]:
                    namegleich = False
                    for i2 in Cached["list"]:
                        if i["name"] == i2["name"]:
                            namegleich = True
                            break
                        else:
                            continue
                    if namegleich is True:
                        return
                    else:
                        print("New POI")
                        try:
                            channel = self.client.get_channel(741337230093582458)
                            name = i["name"]
                            embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=f"New POI",
                                                  description=f"New Name: {name}")
                            try:
                                embed.set_image(url=i["images"][0]["url"])
                            except:
                                pass
                            if Settings.SETTINGS.test is not True:
                                await channel.send(embed=embed)
                        except Exception as ex:
                            print(ex)

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.poi")
        except:
            pass
        try:
            self.client.load_extension("cogs.poi")
        except:
            pass


def setup(client):
    client.add_cog(poi(client))
