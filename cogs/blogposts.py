import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class blogpost(commands.Cog):
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
                await (await aiofiles.open('Cache/blog.json', mode='r', encoding="utf8")).read())
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://api.peely.de/v1/blogposts/normal") as req:
                    if req.status != 200:
                        return
                    new = await req.json()
            if Cached != new:
                await (await aiofiles.open(f"Cache/blog.json", mode='w+', encoding="utf8")).write(
                    json.dumps(new, indent=2))
                print("Blog Update")
                for i in new['data']["blogposts"]:
                    old = False
                    for i2 in Cached["data"]['blogposts']:
                        if i["title"] == i2["title"]:
                            old = True
                    if old is True:
                        continue
                    else:
                        channel = self.client.get_channel(741334556015067188)
                        embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=i["title"],
                                              description=i["description"] +
                                                          f'\n\n[Link]({i["url"]})')
                        embed.set_author(name=f'By {i["author"]}',
                                         url=f'{i["url"]}')
                        try:
                            embed.set_image(url=i['url'])
                        except:
                            pass
                        await channel.send(embed=embed)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            return
        await self.client.wait_until_ready()

        try:
            Cached = json.loads(
                await (await aiofiles.open('Cache/compblog.json', mode='r', encoding="utf8")).read())
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://api.peely.de/v1/blogposts/competitive") as req:
                    if req.status != 200:
                        return
                    new = await req.json()
            if Cached != new:
                await (await aiofiles.open(f"Cache/compblog.json", mode='w+', encoding="utf8")).write(
                    json.dumps(new, indent=2))
                print("Comp Blog Update")
                for i in new["data"]["blogposts"]:
                    old = False
                    for i2 in Cached["data"]['blogposts']:
                        if i["title"] == i2["title"]:
                            old = True
                    if old is True:
                        continue
                    else:
                        channel = self.client.get_channel(741334556015067188)
                        embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=i["title"],
                                              description=i["description"] +
                                                          f'\n\n[Link]({i["url"]})')
                        try:
                            embed.set_image(url=i['url'])
                        except:
                            pass
                        embed.set_author(name=f'By {i["author"]}',
                                         url=f'{i["url"]}')
                        await channel.send(embed=embed)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            return

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.blogpost")
        except:
            pass
        try:
            self.client.load_extension("cogs.blogpost")
        except:
            pass


def setup(client):
    client.add_cog(blogpost(client))
