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
                await (await aiofiles.open('Cache/blog.json', mode='r')).read())
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://www.epicgames.com/fortnite/api/blog/"
                        "getPosts?category=&postsPerPage=6&offset=0&locale=en-US") as req:
                    if req.status != 200:
                        return
                    new = await req.json()
            if Cached["blogList"] != new["blogList"]:
                await (await aiofiles.open(f"Cache/blog.json", mode='w+')).write(
                    json.dumps(new, indent=2))
                print("Blog Update")
                for i in new["blogList"]:
                    old = False
                    for i2 in Cached["blogList"]:
                        if i["title"] == i2["title"]:
                            old = True
                    if old is True:
                        continue
                    else:
                        channel = self.client.get_channel(741334556015067188)
                        embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=i["title"],
                                              description=i["shareDescription"] +
                                                          f'\n\n[Link](https://www.epicgames.com/'
                                                          f'fortnite/{i["urlPattern"]})')
                        try:
                            embed.set_image(url=i["trendingImage"])
                        except KeyError:
                            pass
                        try:
                            embed.set_author(name=f'By {i["author"]}',
                                             url=f'https://www.epicgames.com/'
                                                 f'fortnite/{i["urlPattern"]}',
                                             icon_url=i["image"])
                        except KeyError:
                            embed.set_author(name=f'By {i["author"]}',
                                             url=f'https://www.epicgames.com/'
                                                 f'fortnite/{i["urlPattern"]}')
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
