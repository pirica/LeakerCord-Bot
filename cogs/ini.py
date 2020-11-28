import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks


class ini(commands.Cog):
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

    @tasks.loop(seconds=220)
    async def check(self):
        await self.client.wait_until_ready()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://api.peely.de/v1/ini') as data:
                if data.status != 200:
                    return
                new = await data.json()
        for i in new:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        f'https://api.peely.de/v1/ini/files/{i}') as data:
                    if data.status != 200:
                        continue
                    try:
                        old = await (
                            await aiofiles.open(f'Cache/ini/{i}', mode='r', encoding="utf8")).read()
                    except:
                        old = ""
                    text = str(await data.text())
                    templist = []
                    changes = ""
                    for oldline in old.splitlines():
                        if oldline not in text.splitlines():
                            if oldline == "":
                                continue
                            changes += f"- {oldline}\n"

                    for line in text.splitlines():
                        if line in old.splitlines():
                            continue
                        else:
                            changes += f"+ {line}\n"
                    templist.append(changes)
                    for i2 in templist:
                        if i2 == "":
                            continue
                        if len(i2) > 1500:
                            async with aiofiles.open("Cache/temp.txt", mode="w+", encoding="utf8") as file:
                                await file.write(str(i2))
                            file = discord.File("Cache/temp.txt")
                            await self.client.get_channel(743191744161775758).send(
                                f"Detected Changes in **{i}**", file=file)
                        else:
                            await self.client.get_channel(743191744161775758).send(
                                f"Detected changes in **{i}**\n```diff\n{i2}\n```")
                    async with aiofiles.open(f"Cache/ini/{i}", mode="w+", encoding="utf8") as file:
                        await file.write(text)
        print("Fertig")

    def cog_unload(self):
        self.check.stop()
        try:
            self.client.unload_extension("cogs.ini")
        except:
            pass
        try:
            self.client.load_extension("cogs.ini")
        except:
            pass


def setup(client):
    client.add_cog(ini(client))
