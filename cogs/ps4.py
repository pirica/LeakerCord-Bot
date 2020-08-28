import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class ps4(commands.Cog):
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

    @tasks.loop(seconds=45)
    async def checkstatus(self):
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(
                await (await aiofiles.open('Cache/ps4.json', mode='r')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://store.playstation.com/store/api/chihiro/00_09_000/container/DE/de/999/EP1464-CUSA07669_00-FORTNITETESTING1') as data:
                    new = await data.json()
        except Exception as ex:
            print(ex)
            return
        if new is None:
            return
        if Cached is None:
            return
        if Cached["images"] != new["images"]:
            for i in new["images"]:
                if i not in Cached["images"]:
                    channel = self.client.get_channel(741334681420824646)
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                          title=f"Detected new Image at the Sony (Playstation) Store")
                    embed.set_image(url=i["url"])
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=embed)

        # TRAILER
        if Cached["mediaList"]["previews"] != new["mediaList"]["previews"]:
            for i in new["mediaList"]["previews"]:
                if i not in Cached["mediaList"]["previews"]:
                    channel = self.client.get_channel(741334681420824646)
                    if Settings.SETTINGS.test is False:
                        await channel.send(i["url"])

        # INGAME SCREENS
        if Cached["mediaList"]["screenshots"] != new["mediaList"]["screenshots"]:
            for i in new["mediaList"]["screenshots"]:
                if i not in Cached["mediaList"]["screenshots"]:
                    channel = self.client.get_channel(741334681420824646)
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                          title=f"Detected new Image at the Sony (Playstation) Store")
                    embed.set_image(url=i["url"])
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=embed)

        await (await aiofiles.open('Cache/ps4.json', mode='w+')).write(
            json.dumps(new, indent=2))

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.ps4")
        except:
            pass
        try:
            self.client.load_extension("cogs.ps4")
        except:
            pass


def setup(client):
    client.add_cog(ps4(client))
