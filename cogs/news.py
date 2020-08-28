import json
import traceback
from datetime import datetime

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

from Settings import SETTINGS


class news(commands.Cog):
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
        await self.client.wait_until_ready()
        try:
            old = json.loads(await (await aiofiles.open('Cache/news.json', mode='r', errors='ignore')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://fortnite-api.com/v1/news') as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        for key in new["data"].keys():
            try:
                for news in new["data"][key]["motds"]:
                    if not news in old["data"][key]["motds"]:
                        if key == "creative":
                            if news in new["data"]["br"]["motds"]:
                                continue
                        channel = self.client.get_channel(742369658857848912)
                        embed=discord.Embed(color=SETTINGS.embedcolor, title=str(key).upper() + " - " + news["title"], description=news["body"])
                        embed.timestamp=datetime.utcnow()
                        embed.set_image(url=news["image"])
                        await channel.send(embed=embed)
            except:
                continue
        await (await aiofiles.open('Cache/news.json', mode='w+')).write(
            json.dumps(new, indent=2))

    def cog_unload(self):
        self.check.stop()
        try:
            self.client.unload_extension("cogs.news")
        except:
            pass
        try:
            self.client.load_extension("cogs.news")
        except:
            pass


def setup(client):
    client.add_cog(news(client))
