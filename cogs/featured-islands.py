import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class news(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.check_newisland.start()
        except:
            self.check_newisland.stop()
            self.check_newisland.start()

    @tasks.loop(minutes=10)
    async def check_newisland(self):
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(
                await (await aiofiles.open('Cache/calendar.json', mode='r')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://benbotfn.tk/api/v1/calendar') as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            print(ex)
            return
        try:
            if Cached["channels"]["featured-islands"]["states"][0]["state"]["islandCodes"] != new["channels"]["featured-islands"]["states"][0]["state"]["islandCodes"]:
                print("New featured islands")
                await (await aiofiles.open('Cache/calendar.json', mode='w+')).write(
                    json.dumps(new, indent=2))
                for island in new["channels"]["featured-islands"]["states"][0]["state"]["islandCodes"]:
                    if not island in Cached["channels"]["featured-islands"]["states"][0]["state"]["islandCodes"]:
                        id = island.split("?")
                        async with aiohttp.ClientSession() as cs:
                            parameter = {"Authorization": "2fce9bf4-dcb28a26-d7e48ccf-a12cccee"}
                            async with cs.get(
                                    f'https://fortniteapi.io/creative/island?code={id[0]}', headers=parameter) as data:
                                if data.status != 200:
                                    return
                                new2 = await data.json()
                        if Settings.SETTINGS.test is True:
                            return
                        channel = self.client.get_channel(741334635778146364)
                        embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                              title="New Featured Island: " + new2["island"]["title"])
                        embed.add_field(name=f"Description:", value=new2["island"]["introduction"])
                        tags = ".\n"
                        for tag in new2["island"]["tags"]:
                            tags += tag + "\n"
                        embed.add_field(name=f"Tags:", value=tags)
                        embed.add_field(name=f"Code:", value=f"[{id[0]}](https://epicgames.com/fn/{id[0]})")
                        embed.set_image(url=new2["island"]["image"])
                        await channel.send(embed=embed)
        except KeyError:
            print("Key error featured islands")
            traceback.print_exc()
            return
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            print(ex)
            return

    def cog_unload(self):
        self.check_newisland.stop()
        print("check_newisland LOOP BEENDET")
        try:
            self.client.unload_extension("cogs.featured-islands")
        except:
            print("CANOT UNLOAD EXTENSION featured-islands")
        try:
            self.client.load_extension("cogs.featured-islands")
        except:
            print("CANOT RELOAD EXTENSION featured-islands")


def setup(client):
    client.add_cog(news(client))
