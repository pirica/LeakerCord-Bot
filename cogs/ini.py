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

    @tasks.loop(seconds=30)
    async def check(self):
        await self.client.wait_until_ready()
        try:
            old = json.loads(await (await aiofiles.open('Cache/ini.json', mode='r', errors='ignore')).read())
            token = json.loads(await (await aiofiles.open('Cache/authtoken.json', mode='r', errors='ignore')).read())
            token = token["accessToken"]
            async with aiohttp.ClientSession() as cs:
                headers = {"Authorization": f"bearer {token}"}
                async with cs.get(
                        'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/cloudstorage/system',
                        headers=headers) as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        await (await aiofiles.open('Cache/ini.json', mode='w+')).write(
            json.dumps(new, indent=2))
        for i in new:
            if i not in old:
                async with aiohttp.ClientSession() as cs:
                    headers = {"Authorization": f"bearer {token}"}
                    async with cs.get(
                            f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/cloudstorage/system/{i["uniqueFilename"]}',
                            headers=headers) as data:
                        if data.status != 200:
                            continue
                        oldd = await (
                            await aiofiles.open(f'Cache/ini/{i["filename"]}', mode='r', encoding="utf8")).read()
                        text = str(await data.text())
                        templist = []
                        changes = ""
                        for line in text.splitlines():
                            if line in oldd.splitlines():
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
                                    f"Detected Changes for **{i['filename']}**", file=file)
                            else:
                                await self.client.get_channel(743191744161775758).send(
                                    f"Detected Changes for **{i['filename']}**\n```ini\n{i2}\n```")
                        async with aiofiles.open(f"Cache/ini/{i['filename']}", mode="w+", encoding="utf8") as file:
                            await file.write(text)

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
