import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class storechanges(commands.Cog):
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

    @tasks.loop(seconds=30)
    async def checkstatus(self):
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(
                await (await aiofiles.open('Cache/gameinfo.json', mode='r')).read())
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://store-content.ak.epicgames.com/"
                        "api/en-US/content/products/fortnite") as req:
                    if req.status != 200:
                        return
                    new = await req.json()
            if Cached["pages"][0]["data"]["gallery"]["galleryImages"] != new["pages"][0]["data"]["gallery"][
                "galleryImages"]:
                await (await aiofiles.open(f"Cache/gameinfo.json", mode='w+')).write(
                    json.dumps(new, indent=2))
                for i in new["pages"][0]["data"]["gallery"]["galleryImages"]:
                    if i in Cached["pages"][0]["data"]["gallery"]["galleryImages"]:
                        continue
                    channel = self.client.get_channel(741334681420824646)
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                          title=f"Detected new Image at the Epic Games Store")
                    embed.set_image(url=i["src"])
                    await channel.send(embed=embed)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            return

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.storechanges")
        except:
            pass
        try:
            self.client.load_extension("cogs.storechanges")
        except:
            pass


def setup(client):
    client.add_cog(storechanges(client))
