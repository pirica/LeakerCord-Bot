import json
import traceback
from datetime import datetime

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

from Settings import SETTINGS


class temp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.check.start()
        except Exception as ex:
            print(ex)
            self.check.stop()
            self.check.start()

    @tasks.loop(seconds=60)
    async def check(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.epicgames.com/fortnite/de/home?sessionInvalidated=true&lang=en") as response:
                content = await response.read()
            liste = []
            for i in str(content).split("Fortnite V2 - Teaser Message"):
                try:
                    string = i.split("}")[0].split("\",\"message\":\"")[1].split("\"")[0]
                    string = string.replace("\\xe2\\x80\\x99", "'")
                    liste.append(string)
                except:
                    continue
        old = json.loads(
                await (await aiofiles.open('Cache/temp.json', mode='r')).read())
        for i in liste:
            if i in old:
                continue
            else:
                await self.client.get_channel(747531044315594853).send(embed=discord.Embed(color=SETTINGS.embedcolor, title="New String detected", description=str(i)))
        await (await aiofiles.open('Cache/temp.json', mode='w+')).write(
            json.dumps(liste, indent=2))


    def cog_unload(self):
        self.check.stop()
        try:
            self.client.unload_extension("cogs.temp")
        except:
            pass
        try:
            self.client.load_extension("cogs.temp")
        except:
            pass


def setup(client):
    client.add_cog(temp(client))
